#
# Copyright (C) 2020 Agilent Technologies, Inc.
#
# SPDX-License-Identifier: GPL-2.0-only
#

REVRECORD_INCFILE_NAME    ??= "revs.inc"
#REVRECORD_JSON_FILE_NAME  ??= "revs.json"

REVRECORD_TOPDIR = "${TOPDIR}/revs"
REVRECORD_SESSION_DIR = "${REVRECORD_TOPDIR}/${REVRECORD_DATETIME}"

# A per-multiconfig directory (or just the REVRECORD_SESSION_DIR if multiconfig isn't enabled) for output
REVRECORD_MC_DIR = "${REVRECORD_SESSION_DIR}${@"/${BB_CURRENT_MC}" if d.getVar("BBMULTICONFIG") else ""}"

# See event handler at bottom - some trickery is needed to keep this in sync across multiconfigs
REVRECORD_DATETIME = "${DATETIME}"

def get_effective_srcrev_var(d, name):
    """ Determine the effective SRCREV variable for given SRC_URI name. """
    # Based on code in fetch2/__init__.py
    pn = d.getVar("PN")
    attempts = []
    if name != '' and pn:
        attempts.append("SRCREV_{0}_pn-{1}".format(name, pn))
    if name != '':
        attempts.append("SRCREV_{0}".format(name))
    if pn:
        attempts.append("SRCREV_pn-{0}".format(pn))
    attempts.append("SRCREV")

    return next(filter(lambda v: v in d, attempts), None)

def get_unexpanded_src_uris_by_name(d, only_scm=True):
    """ Return dict of SRC_URI entry name => unexpanded SRC_URI entry """
    import collections
    ret = {}
    src_uris = collections.deque()

    def enqueue_var_contents(v):
        src_uris.extend(oe.recipeutils.split_var_value(d.getVar(v, False) or ""))

    enqueue_var_contents("SRC_URI")
    while src_uris:
        unexpanded_entry = src_uris.popleft()
        expanded = d.expand(unexpanded_entry)
        if not expanded:
            continue
        try:
            fetcher = bb.fetch.Fetch([expanded], d)
            ud = fetcher.ud[fetcher.urls[0]]
            if only_scm and not ud.method.supports_srcrev():
                continue
            uri_name = ud.parm.get("name") or "default"
            ret[uri_name] = unexpanded_entry
        except bb.fetch2.NoMethodError:
            expanded = expanded.strip()
            # If the expanded "entry" is actually more than one entry, then maybe the
            # unexpanded entry is a variable deref.
            if len(expanded.split()) == 1:
                raise

            if unexpanded_entry[0:2] == "${" and unexpanded_entry[-1] == "}" and unexpanded_entry[2:-1] in d:
                # Add the contents of the variable to the processing queue
                enqueue_var_contents(unexpanded_entry[2:-1])
            else:
                # There's only so much we can do. We won't be able to handle something weird like:
                #   SRC_URI = "${A}${C}"
                #   A = "git://"
                #   C = "git@host/path;branch=${BRANCH}"
                # since there's no (easy) way to partially expand SRC_URI just up to the leaf variables.
                raise NotImplementedError("Unable to process SRC_URI entry: {0}".format(unexpanded_entry))

    return ret

def get_srcrev_values(d):
    """ Return the version strings for the current recipe """
    fetcher = bb.fetch.Fetch(d.getVar('SRC_URI').split(), d)
    urldata = fetcher.ud
    scms = [u for u in urldata if urldata[u].method.supports_srcrev()]

    dict_srcrevs = {}
    uds = {}
    for scm in scms:
        ud = urldata[scm]
        for name in ud.names:
            rev = ud.method.sortable_revision(ud, d, name)
            dict_srcrevs[name] = rev[1]
            uds[name] = ud
    return dict_srcrevs, uds

def extract_src_uri_param_var(src_uri, param):
    """
    Given an unexpanded SRC_URI entry |src_uri| and parameter name |param|, searches
    for an assignment to that parameter. If found, and the assignment consists of
    dereferencing a single variable, returns name of the variable. Otherwise returns None.

    For example, given src_uri="git://repo;branch=${BRANCH}" and param="branch",
    this method would return "BRANCH".
    """
    import re
    regex = re.compile(param + r"=\${(?P<var>[a-zA-Z0-9\-_+./~]+)}")
    m = regex.search(src_uri)
    if m:
        return m.group("var")
    return None

def handle_recipe_parsed(d):
    if bb.data.inherits_class("externalsrc", d):
        return

    # Skip recipe if there are no srcrev-supporting SRC_URIs
    revs, uds = get_srcrev_values(d)
    if not revs:
        return

    unexpanded_by_name = get_unexpanded_src_uris_by_name(d)

    inclines = []
    pn = d.getVar("PN")
    for name in sorted(revs):
        var = get_effective_srcrev_var(d, name)

        # We only care about SRCREV that is set to AUTOREV (which will cause it to report as AUTOINC).
        if d.getVar(var) != "AUTOINC":
            continue

        # Add _pn- override if not already present
        if "_pn-" not in var:
            var = "{0}_pn-{1}".format(var, pn)

        inclines.append('{0} = "{1}"'.format(var, revs[name]))

        # Depending on the fetcher scheme, there may be other parameters we want to capture
        raw_src_uri = unexpanded_by_name[name]
        ud = uds[name]
        if ud.type == "git":
            # Also want to capture branch; TODO what about tags?
            ref = ud.unresolvedrev[name]
            branch_var = extract_src_uri_param_var(raw_src_uri, "branch")
            if branch_var:
                inclines.append('{0}_pn-{1} = "{2}"'.format(branch_var, pn, ref))

    pndir = d.expand("${REVRECORD_MC_DIR}/${PN}")
    if inclines:
        bb.utils.mkdirhier(pndir)
        incfile = os.path.join(pndir, d.getVar("REVRECORD_INCFILE_NAME"))
        with open(incfile, "w") as f:
            f.write("\n".join(inclines))

def handle_parse_completed(d):
    outdir = d.getVar("REVRECORD_MC_DIR")
    bb.utils.mkdirhier(outdir)

    # Aggregate all the per-PN revs files into a unified one at the base of the outdir
    incfile_name = d.getVar("REVRECORD_INCFILE_NAME")
    revsfile = os.path.join(outdir, incfile_name)
    with open(revsfile, "w") as f:
        for root, dirs, files in os.walk(outdir):
            # Sorted by PN
            dirs.sort()
            if root == outdir:
                continue

            pn = os.path.basename(root)
            with open(os.path.join(root, incfile_name), "r") as g:
                f.write("# {0}\n".format(pn))
                f.writelines(line for line in g)
                f.write("\n\n")

python revrecord_handler() {
    if isinstance(e, bb.event.MultiConfigParsed):
        # Propogate REVRECORD_DATETIME (as set in the base configuration) to all multiconfigs
        for key in e.mcdata:
            if key != "":
                e.mcdata[key].setVar("REVRECORD_DATETIME", e.mcdata[""].getVar("REVRECORD_DATETIME"))
    elif isinstance(e, bb.event.ParseStarted):
        session_dir = d.getVar("REVRECORD_SESSION_DIR")
        bb.utils.mkdirhier(session_dir)

        # Set up a convienence symlink
        topdir = d.getVar("REVRECORD_TOPDIR")
        latest_dir = os.path.join(topdir, "latest")
        if os.path.exists(latest_dir):
            os.unlink(latest_dir)
        os.symlink(session_dir, latest_dir)
    elif isinstance(e, bb.event.RecipeParsed):
        handle_recipe_parsed(d)
    elif isinstance(e, bb.event.ParseCompleted):
        handle_parse_completed(d)

        # Also need to do it once for each multiconfig
        for mc in (d.getVar("BBMULTICONFIG") or "").split():
            if mc:
                mcdata = bb.data.createCopy(d)
                mcdata.setVar("BB_CURRENT_MC", mc)
                handle_parse_completed(mcdata)

        # TODO: merge all multiconfig-level revs.inc into a global revs.inc; but how to handle conflicts?
}

addhandler revrecord_handler
revrecord_handler[eventmask] = " \
    bb.event.MultiConfigParsed \
    bb.event.ParseCompleted \
    bb.event.ParseStarted \
    bb.event.RecipeParsed \
"
