SUMMARY = "Image which includes world packages"

WORLD_IMAGE_EXCLUDE ?= "epiphany webkitgtk qt4 forktest nss meta-world-pkgdata"

def extend_image_install(d):
    if not d.getVar("BB_WORKERCONTEXT", False):
        return ""

    import oe.packagedata

    pkgdatadir = d.getVar("PKGDATA_DIR")

    packagelist = []

    files = os.listdir(pkgdatadir)
    for pn in filter(lambda f: not os.path.isdir(os.path.join(pkgdatadir, f)), files):
        try:
            pkgdata = oe.packagedata.read_pkgdatafile(os.path.join(pkgdatadir, pn))
        except OSError:
            continue

        packages = pkgdata.get("PACKAGES") or ""

        for pkg in packages.split():
            if pkg.endswith("-dbg"):
                continue
            if pkg.endswith("-dev"):
                continue
            if pkg != pn:
                continue
            if not os.path.exists(os.path.join(pkgdatadir, "runtime", pn + ".packaged")):
                continue
            if pkg.startswith("nativesdk-"):
                continue
            if pkg in ["kbd", "dropbear", "console-tools", "packagegroup-core-ssh-dropbear"]:
                continue
            packagelist.append(pkg)

    return " ".join(packagelist)

IMAGE_INSTALL_append = "${@extend_image_install(d)}"

python calculate_extra_depends() {
    exclude = '${WORLD_IMAGE_EXCLUDE}'.split()
    for p in world_target:
        if p == self_pn:
            continue

        if p in exclude:
            continue

        deps.append(p)
}

inherit image