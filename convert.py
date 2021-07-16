#!/usr/bin/env python3

import re
import os
import tempfile
import shutil
import mimetypes

packagevars = ["FILES", "RDEPENDS", "RRECOMMENDS", "SUMMARY", "DESCRIPTION", "RSUGGESTS", "RPROVIDES", "RCONFLICTS", "PKG", "ALLOW_EMPTY", 
              "pkg_postrm", "pkg_postinst_ontarget", "pkg_postinst", "INITSCRIPT_NAME", "INITSCRIPT_PARAMS", "DEBIAN_NOAUTONAME", "ALTERNATIVE",
              "PKGE", "PKGV", "PKGR", "USERADD_PARAM", "GROUPADD_PARAM", "CONFFILES", "SYSTEMD_SERVICE", "LICENSE", "SECTION", "pkg_preinst", 
              "pkg_prerm", "RREPLACES", "GROUPMEMS_PARAM", "SYSTEMD_AUTO_ENABLE", "SKIP_FILEDEPS", "PRIVATE_LIBS", "PACKAGE_ADD_METADATA", "INSANE_SKIP", "DEBIANNAME"]

imagevars = ["IMAGE_CMD", "EXTRA_IMAGECMD"]
packagevars = packagevars + imagevars

package_re = {}
for exp in packagevars:
    package_re[exp] = (re.compile('(^|[\'"\s]+)' + exp + '_'), r"\1" + exp + ":")

vars = ["class-native", "class-target", "append", "prepend", "remove", "riscv32", "riscv64", "qemuarm", "qemux86", "x86"]
vars = vars + ["libc-musl", "task-compile", "x86-x32", "qemuall", "task-install", "toolchain-clang", "armv5", "armv6", "armv4", "powerpc64"]
vars = vars + ["armeb", "arm", "aarch64", "class-cross-canadian", "pn-", "mips64", "mydistro", "libc-glibc", "linux-muslx32", "class-devupstream"]
vars = vars + ["linux-gnux32", "mingw32", "qemumips", "qemuppc", "qemuriscv", "poky", "powerpc", "mipsarch", "nios2", "darwin"]
vars = vars + ["class-cross", "task-clean", "virtclass-multilib", "task-image-complete", "task-populate-sdk", "task-image-qa", "task-rm_work"]

vars_re = {}
for exp in vars:
    vars_re[exp] = (re.compile('((^|[\'"\s])[A-Za-z0-9_\-:${}]+)_' + exp), r"\1:" + exp)

skips = ["LICENSE_PATH", "FILES_INFO", "LICENSE_DIRECTORY", "LICENSE_FLAGS", "PKG_CONFIG", "PKG_CHECK", "LICENSE_CREATE", "PACKAGE_ADD_METADATA_IPK"]
skips = skips + ["ALTERNATIVE_LINK_NAME", "ALTERNATIVE_TARGET", "ALTERNATIVE_PRIORITY", "FILES_SOLIBSDEV", "PKG_TYPE", "LICENSE_EXCLUSION", "IMAGE_CMD_TAR"]
skips = skips + ["LICENSE_FILES_DIRECTORY", "LICENSE_FLAGS_WHITELIST", "LICENSE_PACKAGE_SUFFIX", "PACKAGE_ADD_METADATA_RPM", "PACKAGE_ADD_METADATA_DEB"]
skips = skips + ["parser_append", "recipe_to_append", "extra_append", "to_remove", "show_appends", "applied_appends", "file_appends", "handle_remove"]
skips = skips + ["expanded_removes", "color_remove", "test_remove", "empty_remove", "toaster_prepend", "num_removed", "licfiles_append", "_write_append"]
skips = skips + ["no_report_remove", "test_prepend", "test_append", "multiple_append", "test_remove", "shallow_remove", "do_remove_layer", "first_append"]
skips = skips + ["parser_remove", "to_append", "no_remove", "bblayers_add_remove", "bblayers_remove", "apply_append", "is_x86", "base_dep_prepend"]
skips = skips + ["autotools_dep_prepend", "go_map_arm", "alt_remove_links", "systemd_append_file", "file_append", "process_file_darwin"]
skips = skips + ["run_loaddata_poky", "determine_if_poky_env", "do_populate_poky_src", "libc_cv_include_x86_isa_level"]
#Problems:
#   A:append_foo = "X"
#        self.d.setVar("TEST:remove_inactiveoverride", "val")
# RDEPENDS_${PN}-ptest_append_libc-glibc (bash.inc)
# arc override

subs = {
    'r = re.compile("([^:]+):\s*(.*)")' : 'r = re.compile("(^.+?):\s+(.*)")',
    "val = d.getVar('%s_%s' % (var, pkg))" : "val = d.getVar('%s:%s' % (var, pkg))",
    "f.write('%s_%s: %s\\n' % (var, pkg, encode(val)))" : "f.write('%s:%s: %s\\n' % (var, pkg, encode(val)))",
    "d.getVar('%s_%s' % (scriptlet_name, pkg))" : "d.getVar('%s:%s' % (scriptlet_name, pkg))",
    'ret.append(v + "_" + p)' : 'ret.append(v + ":" + p)',
}

def processfile(fn):
    try:
        fh, abs_path = tempfile.mkstemp()
        with os.fdopen(fh, 'w') as new_file:
            with open(fn, "r") as old_file:
                for line in old_file:
                    skip = False
                    for s in skips:
                        if "${FILES_SOLIBSDEV}" in line or "${IMAGE_CMD_TAR}" in line:
                            continue
                        if s in line:
                            skip = True
                            if "ptest_append" in line:
                                skip = False
                    if "base_dep_prepend" in line and line.startswith("BASEDEPENDS_class"):
                        line = line.replace("BASEDEPENDS_class", "BASEDEPENDS:class")
                        skip = True
                    if "autotools_dep_prepend" in line and line.startswith("DEPENDS_prepend"):
                        line = line.replace("DEPENDS_prepend", "DEPENDS:prepend")
                        skip = True
                    for sub in subs:
                        if sub in line:
                            line = line.replace(sub, subs[sub])
                            skip = True
                    if not skip:
                        for pvar in packagevars:
                            line = package_re[pvar][0].sub(package_re[pvar][1], line)
                        for var in vars:
                            line = vars_re[var][0].sub(vars_re[var][1], line)
                    if "pkg_postinst:ontarget" in line:
                        line = line.replace("pkg_postinst:ontarget", "pkg_postinst_ontarget")
                    new_file.write(line)
        shutil.copymode(fn, abs_path)
        os.remove(fn)
        shutil.move(abs_path, fn)
    except UnicodeDecodeError:
        pass

for root, dirs, files in os.walk("/media/build2/poky-override/"):
   for name in files:
      if name == "convert.py":
          continue
      fn = os.path.join(root, name)
      if os.path.islink(fn):
          continue
      if "/.git/" in fn or fn.endswith(".html") or fn.endswith(".patch") or fn.endswith(".m4"):
          continue     
      if fn.startswith("/media/build2/poky-override/build/"):
          continue
      processfile(fn)

