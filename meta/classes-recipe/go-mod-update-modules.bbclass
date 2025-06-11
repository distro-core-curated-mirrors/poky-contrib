addtask do_update_modules after do_configure
do_update_modules[nostamp] = "1"
do_update_modules[network] = "1"

python do_update_modules() {
    import subprocess, tempfile, json, re, urllib.parse
    from oe.license_finder import find_licenses

    def unescape_path(path):
        """Unescape capital letters using exclamation points."""
        return re.sub(r'!([a-z])', lambda m: m.group(1).upper(), path)

    def fold_uri(uri):
        """Fold URI for sorting shorter module paths before longer."""
        return uri.replace(';', ' ').replace('/', '!')

    # TODO duplicated in recipetools
    def tidy_licenses(value):
        """Flat, split and sort licenses"""
        from oe.license import flattened_licenses
        def _choose(a, b):
            str_a, str_b  = sorted((" & ".join(a), " & ".join(b)), key=str.casefold)
            return ["(%s | %s)" % (str_a, str_b)]
        if not isinstance(value, str):
            value = " & ".join(value)
        return sorted(list(set(flattened_licenses(value, _choose))), key=str.casefold)

    def parse_existing_licenses():
        hashes = {}
        for url in d.getVar("LIC_FILES_CHKSUM").split():
            (method, host, path, user, pswd, parm) = bb.fetch.decodeurl(url)
            if "spdx" in parm:
                hashes[parm["md5"]] = urllib.parse.unquote_plus(parm["spdx"])
        return hashes

    bpn = d.getVar("BPN")
    thisdir = d.getVar("THISDIR")

    mod_dir = tempfile.mkdtemp(prefix='go-mod-')
    # TODO remove when done
    #d.setVar('GOMODCACHE', mod_dir)
    env = dict(os.environ, GOMODCACHE=mod_dir)

    # TODO this feels magic
    source = d.expand("${WORKDIR}/${GO_SRCURI_DESTSUFFIX}")

    # TODO is this needed in the refresh case?
    output = subprocess.check_output(("go", "mod", "edit", "-json"), cwd=source, env=env, text=True)
    go_mod = json.loads(output)

    output = subprocess.check_output(("go", "list", "-json=Dir,Module", "-deps", f"{go_mod['Module']['Path']}/..."), cwd=source, env=env, text=True)

    #
    # Licenses
    #

    # load hashes from the existing licenses.inc
    extra_hashes = parse_existing_licenses()

    # The output of this isn't actually valid JSON, but a series of dicts.
    # Wrap in [] and join the dicts with ,
    # Very frustrating that the json parser in python can't repeatedly
    # parse from a stream.
    pkgs = json.loads('[' + output.replace('}\n{', '},\n{') + ']')
    # Collect licenses for the dependencies.
    licenses = set()
    lic_files_chksum = []
    lic_files = {}
    for pkg in pkgs:
        mod = pkg.get('Module', None)
        if not mod or mod.get('Main', False):
            continue

        path = os.path.relpath(mod['Dir'], mod_dir)
        for license_name, license_file, license_md5 in find_licenses(mod['Dir'], d, first_only=True, extra_hashes=extra_hashes):
            lic_files[os.path.join(path, license_file)] = (license_name, license_md5)

    for lic_file in lic_files:
        license_name, license_md5 = lic_files[lic_file]
        if license_name == "Unknown":
            bb.warn(f"Unknown license: {lic_file} {license_md5}")

        licenses.add(lic_files[lic_file][0])
        lic_files_chksum.append(
            f'file://pkg/mod/{lic_file};md5={license_md5};spdx={urllib.parse.quote_plus(license_name)}')

    licenses_filename = os.path.join(thisdir, f"{bpn}-licenses.inc")
    with open(licenses_filename, "w") as f:
        f.write(f'LICENSE += "& {" & ".join(tidy_licenses(licenses))}"\n\n')
        f.write('LIC_FILES_CHKSUM += "\\\n')
        for lic in sorted(lic_files_chksum, key=fold_uri):
            f.write('    ' + lic + ' \\\n')
        f.write('"\n')

    #
    # Sources
    #

    # Collect the module cache files downloaded by the go list command as
    # the go list command knows best what the go list command needs and it
    # needs more files in the module cache than the go install command as
    # it doesn't do the dependency pruning mentioned in the Go module
    # reference, https://go.dev/ref/mod, for go 1.17 or higher.
    src_uris = []
    downloaddir = os.path.join(mod_dir, 'cache', 'download')
    for dirpath, _, filenames in os.walk(downloaddir):
        # We want to process files under @v directories
        path, base = os.path.split(os.path.relpath(dirpath, downloaddir))
        if base != '@v':
            continue

        path = unescape_path(path)
        zipver = None
        for name in filenames:
            ver, ext = os.path.splitext(name)
            if ext == '.zip':
                chksum = bb.utils.sha256_file(os.path.join(dirpath, name))
                src_uris.append(f'gomod://{path};version={ver};sha256sum={chksum}')
                zipver = ver
                break
        for name in filenames:
            ver, ext = os.path.splitext(name)
            if ext == '.mod' and ver != zipver:
                chksum = bb.utils.sha256_file(os.path.join(dirpath, name))
                src_uris.append(f'gomod://{path};version={ver};mod=1;sha256sum={chksum}')


    go_mods_filename = os.path.join(thisdir, f"{bpn}-go-mods.inc")
    with open(go_mods_filename, "w") as f:
        f.write('SRC_URI += "\\\n')
        for uri in sorted(src_uris, key=fold_uri):
            f.write('    ' + uri + ' \\\n')
        f.write('"\n')

    subprocess.check_output(("go", "clean", "-modcache"), cwd=source, env=env, text=True)
}

# This doesn't work as we need to wipe the inc files first so we don't try looking for LICENSE files that don't yet exist
# RECIPE_UPGRADE_EXTRA_TASKS += "do_update_modules"
