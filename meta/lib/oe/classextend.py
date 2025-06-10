#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: GPL-2.0-only
#

import collections
import bb.filter

@bb.filter.filter_proc()
def native_filter(val, pn, bpn, regex=False, selfref=True):
    deps = val
    if not deps:
        return
    deps = bb.utils.explode_deps(deps)
    newdeps = []
    for dep in deps:
        if regex and dep.startswith("^") and dep.endswith("$"):
            newdeps.append(dep[:-1].replace(pn, bpn) + "-native$")
        elif dep == pn:
            if not selfref:
                continue
            newdeps.append(dep)
        elif "-cross-" in dep:
            newdeps.append(dep.replace("-cross", "-native"))
        elif not dep.endswith("-native"):
            # Replace ${PN} with ${BPN} in the dependency to make sure
            # dependencies on, e.g., ${PN}-foo become ${BPN}-foo-native
            # rather than ${BPN}-native-foo-native.
            newdeps.append(dep.replace(pn, bpn) + "-native")
        else:
            newdeps.append(dep)
    return " ".join(newdeps)


@bb.filter.filter_proc()
def suffix_filter(val, extname):
    def add_suffix(val, extname):
        if val.endswith(("-native", "-native-runtime")) or ('nativesdk-' in val) or ('cross-canadian' in val) or ('-crosssdk-' in val):
            return val
        if val.startswith("kernel-") or val == "virtual/kernel":
            return val
        if val.startswith("rtld"):
            return val
        if val.endswith("-crosssdk"):
            return val
        if val.endswith("-" + extname):
            val = val.replace("-" + extname, "")
        if val.startswith("virtual/"):
            # Assume large numbers of dashes means a triplet is present and we don't need to convert
            if val.count("-") >= 3 and val.endswith(("-go",)):
                return val
            subs = val.split("/", 1)[1]
            if not subs.startswith(extname):
                return "virtual/" + extname + "-" + subs
            return val
        if val.startswith("/") or (val.startswith("${") and val.endswith("}")):
            return val
        if not val.startswith(extname):
            return extname + "-" + val
        return val

    deps = bb.utils.explode_dep_versions2(val)
    newdeps = collections.OrderedDict()
    for dep in deps:
        newdeps[add_suffix(dep, extname)] = deps[dep]
    return bb.utils.join_deps(newdeps, False)


def get_packages(d):
    pkgs = d.getVar("PACKAGES_NONML")
    extcls = d.getVar("EXTENDERCLASS")
    return extcls.rename_packages_internal(pkgs)

def get_depends(varprefix, d):
    extcls = d.getVar("EXTENDERCLASS")
    return extcls.map_depends_variable(varprefix + "_NONML")

class ClassExtender(object):
    def __init__(self, extname, d):
        self.extname = extname
        self.d = d
        self.pkgs_mapping = []
        self.d.setVar("EXTENDERCLASS", self)

    def extend_name(self, name):
        if name.startswith("kernel-") or name == "virtual/kernel":
            return name
        if name.startswith("rtld"):
            return name
        if name.endswith("-crosssdk"):
            return name
        if name.endswith("-" + self.extname):
            name = name.replace("-" + self.extname, "")
        if name.startswith("virtual/"):
            # Assume large numbers of dashes means a triplet is present and we don't need to convert
            if name.count("-") >= 3 and name.endswith(("-go",)):
                return name
            subs = name.split("/", 1)[1]
            if not subs.startswith(self.extname):
                return "virtual/" + self.extname + "-" + subs
            return name
        if name.startswith("/") or (name.startswith("${") and name.endswith("}")):
            return name
        if not name.startswith(self.extname):
            return self.extname + "-" + name
        return name

    def map_variable(self, varname, setvar = True):
        var = self.d.getVar(varname)
        if not var:
            return ""
        var = var.split()
        newvar = []
        for v in var:
            newvar.append(self.extend_name(v))
        newdata =  " ".join(newvar)
        if setvar:
            self.d.setVar(varname, newdata)
        return newdata

    def map_regexp_variable(self, varname, setvar = True):
        var = self.d.getVar(varname)
        if not var:
            return ""
        var = var.split()
        newvar = []
        for v in var:
            if v.startswith("^" + self.extname):
                newvar.append(v)
            elif v.startswith("^"):
                newvar.append("^" + self.extname + "-" + v[1:])
            else:
                newvar.append(self.extend_name(v))
        newdata =  " ".join(newvar)
        if setvar:
            self.d.setVar(varname, newdata)
        return newdata

    def map_depends(self, dep):
        if dep.endswith(("-native", "-native-runtime")) or ('nativesdk-' in dep) or ('cross-canadian' in dep) or ('-crosssdk-' in dep):
            return dep
        else:
            # Do not extend for that already have multilib prefix
            var = self.d.getVar("MULTILIB_VARIANTS")
            if var:
                var = var.split()
                for v in var:
                    if dep.startswith(v):
                        return dep
            return self.extend_name(dep)

    def map_depends_variable(self, varname, suffix = ""):
        # We need to preserve EXTENDPKGV so it can be expanded correctly later
        if suffix:
            varname = varname + ":" + suffix
        orig = self.d.getVar("EXTENDPKGV", False)
        self.d.setVar("EXTENDPKGV", "EXTENDPKGV")
        deps = self.d.getVar(varname)
        if not deps:
            self.d.setVar("EXTENDPKGV", orig)
            return
        deps = bb.utils.explode_dep_versions2(deps)
        newdeps = collections.OrderedDict()
        for dep in deps:
            newdeps[self.map_depends(dep)] = deps[dep]

        if not varname.endswith("_NONML"):
            self.d.renameVar(varname, varname + "_NONML")
            self.d.setVar(varname, "${@oe.classextend.get_depends('%s', d)}" % varname)
            self.d.appendVarFlag(varname, "vardeps", " " + varname + "_NONML")
        ret = bb.utils.join_deps(newdeps, False).replace("EXTENDPKGV", "${EXTENDPKGV}")
        self.d.setVar("EXTENDPKGV", orig)
        return ret

    def map_packagevars(self):
        for pkg in (self.d.getVar("PACKAGES").split() + [""]):
            self.map_depends_variable("RDEPENDS", pkg)
            self.map_depends_variable("RRECOMMENDS", pkg)
            self.map_depends_variable("RSUGGESTS", pkg)
            self.map_depends_variable("RPROVIDES", pkg)
            self.map_depends_variable("RREPLACES", pkg)
            self.map_depends_variable("RCONFLICTS", pkg)
            self.map_depends_variable("PKG", pkg)

    def rename_packages(self):
        for pkg in (self.d.getVar("PACKAGES") or "").split():
            if pkg.startswith(self.extname):
               self.pkgs_mapping.append([pkg.split(self.extname + "-")[1], pkg])
               continue
            self.pkgs_mapping.append([pkg, self.extend_name(pkg)])

        self.d.renameVar("PACKAGES", "PACKAGES_NONML")
        self.d.setVar("PACKAGES", "${@oe.classextend.get_packages(d)}")

    def rename_packages_internal(self, pkgs):
        self.pkgs_mapping = []
        for pkg in (self.d.expand(pkgs) or "").split():
            if pkg.startswith(self.extname):
               self.pkgs_mapping.append([pkg.split(self.extname + "-")[1], pkg])
               continue
            self.pkgs_mapping.append([pkg, self.extend_name(pkg)])

        return " ".join([row[1] for row in self.pkgs_mapping])

    def rename_package_variables(self, variables):
        for pkg_mapping in self.pkgs_mapping:
            if pkg_mapping[0].startswith("${") and pkg_mapping[0].endswith("}"):
                continue
            for subs in variables:
                self.d.renameVar("%s:%s" % (subs, pkg_mapping[0]), "%s:%s" % (subs, pkg_mapping[1]))

class NativesdkClassExtender(ClassExtender):
    def map_depends(self, dep):
        if dep.startswith(self.extname):
            return dep
        if dep.endswith(("-native", "-native-runtime")) or ('nativesdk-' in dep) or ('-cross-' in dep) or ('-crosssdk-' in dep):
            return dep
        else:
            return self.extend_name(dep)
