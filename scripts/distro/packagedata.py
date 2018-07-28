import os

# yuck
def read_pkgdata(fn, pkg=None):
    import codecs
    pkgdata = {}

    def decode(str):
        c = codecs.getdecoder("unicode_escape")
        return c(str)[0]

    if os.access(fn, os.R_OK):
        import re
        f = open(fn, 'r')
        lines = f.readlines()
        f.close()
        r = re.compile("([^:]+):\s*(.*)")
        for l in lines:
            m = r.match(l)
            if m:
                pkgdata[m.group(1)] = decode(m.group(2))

    # remove suffixies if required
    if pkg:
        new = {}
        for var in pkgdata:
            newvar = var.replace("_" + pkg, "")
            if newvar == var and var + "_" + pkg in pkgdata:
                continue
            new[newvar] = pkgdata[var]
        pkgdata = new
    return pkgdata

class PackageData:
    def __init__(self, directory):
        self.base = directory

    def pkgdata_from_runtime_package(self, package):
        # use target-relative names (ie after debian.bbclass)
        path = os.path.join(self.base, "runtime-reverse", package)
        # need to know the effective package name (not the real name) as that's what is used in keys in the pkgdata
        effective_pkg = os.path.basename(os.readlink(path))
        return read_pkgdata(path, effective_pkg)
