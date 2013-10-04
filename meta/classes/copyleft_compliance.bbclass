# Deploy sources for recipes for compliance with copyleft-style licenses
# Defaults to using symlinks, as it's a quick operation, and one can easily
# follow the links when making use of the files (e.g. tar with the -h arg).
#
# By default, includes all GPL and LGPL, and excludes CLOSED and Proprietary.
#
# vi:sts=4:sw=4:et

# Need the copyleft_should_include
inherit archiver

COPYLEFT_SOURCES_DIR ?= '${DEPLOY_DIR}/copyleft_sources'

python do_prepare_copyleft_sources () {
    """Populate a tree of the recipe sources and emit patch series files"""
<<<<<<< HEAD
    import os.path
=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
    import shutil

    p = d.getVar('P', True)
    included, reason = copyleft_should_include(d)
    if not included:
        bb.debug(1, 'copyleft: %s is excluded: %s' % (p, reason))
        return
    else:
        bb.debug(1, 'copyleft: %s is included: %s' % (p, reason))

    sources_dir = d.getVar('COPYLEFT_SOURCES_DIR', True)
<<<<<<< HEAD
    dl_dir = d.getVar('DL_DIR', True)
=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
    src_uri = d.getVar('SRC_URI', True).split()
    fetch = bb.fetch2.Fetch(src_uri, d)
    ud = fetch.ud

<<<<<<< HEAD
    pf = d.getVar('PF', True)
    dest = os.path.join(sources_dir, pf)
    shutil.rmtree(dest, ignore_errors=True)
    bb.utils.mkdirhier(dest)

    for u in ud.values():
        local = os.path.normpath(fetch.localpath(u.url))
        if local.endswith('.bb'):
            continue
        elif local.endswith('/'):
            local = local[:-1]

        if u.mirrortarball:
            tarball_path = os.path.join(dl_dir, u.mirrortarball)
            if os.path.exists(tarball_path):
                local = tarball_path

        oe.path.symlink(local, os.path.join(dest, os.path.basename(local)), force=True)

    patches = src_patches(d)
    for patch in patches:
        _, _, local, _, _, parm = bb.fetch.decodeurl(patch)
=======
    locals = (fetch.localpath(url) for url in fetch.urls)
    localpaths = [local for local in locals if not local.endswith('.bb')]
    if not localpaths:
        return

    pf = d.getVar('PF', True)
    dest = os.path.join(sources_dir, pf)
    shutil.rmtree(dest, ignore_errors=True)
    bb.mkdirhier(dest)

    for path in localpaths:
        os.symlink(path, os.path.join(dest, os.path.basename(path)))

    patches = src_patches(d)
    for patch in patches:
        _, _, local, _, _, parm = bb.decodeurl(patch)
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
        patchdir = parm.get('patchdir')
        if patchdir:
            series = os.path.join(dest, 'series.subdir.%s' % patchdir.replace('/', '_'))
        else:
            series = os.path.join(dest, 'series')

        with open(series, 'a') as s:
            s.write('%s -p%s\n' % (os.path.basename(local), parm['striplevel']))
}

addtask prepare_copyleft_sources after do_fetch before do_build
<<<<<<< HEAD
do_prepare_copyleft_sources[dirs] = "${WORKDIR}"
=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
do_build[recrdeptask] += 'do_prepare_copyleft_sources'
