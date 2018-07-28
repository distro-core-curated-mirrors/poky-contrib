#! /usr/bin/env python3

import subprocess
import functools
import re
import os
import packagedata

@functools.lru_cache()
def get_bb_environment(target=None):
    args = ['bitbake', '-e']
    if target:
        args += [target]
    return subprocess.check_output(args).decode('utf-8')

@functools.lru_cache()
def get_bitbake_var(variable, target=None):
    environment = get_bb_environment(target)

    var_re = re.compile(r'^(export )?(?P<var>\w+(_.*)?)="(?P<value>.*)"$')
    unset_re = re.compile(r'^unset (?P<var>\w+)')

    lastline = None
    for line in environment.splitlines():
        match = var_re.match(line)
        val = None
        if match:
            val = match.group('value')
        else:
            match = unset_re.match(line)
            if match:
                # Handle [unexport] variables
                if lastline.startswith('#   "'):
                    val = lastline.split('"')[1]
        if val:
            var = match.group('var')
            if var == variable:
                return val
        lastline = line

def manifest_iterator(filename):
    """
    Given a filename for an image manifest, return an iterator returning
    (package, arch, version) tuples.
    """
    with open(filename) as f:
        for line in f:
            (package, arch, version) = line.split()
            yield (package, arch, version)


target = "core-image-minimal" # TODO argparse
deploy_dir = get_bitbake_var("DEPLOY_DIR_IMAGE", target)
image_name = get_bitbake_var("IMAGE_LINK_NAME", target)
pkgdata_dir = get_bitbake_var("PKGDATA_DIR", target)

pkgdata = packagedata.PackageData(pkgdata_dir)
manifest = os.path.join(deploy_dir, "%s.manifest" % (image_name))
seen = set()

for (package, arch, version) in manifest_iterator(manifest):
    try:
        data = pkgdata.pkgdata_from_runtime_package(package)
        recipe = data["PN"]
        seen.add(recipe)
    except Exception:
        print("WARNING: cannot find recipe for %s" % package)
        seen.add(package)

for recipe in sorted(seen):
    print(recipe)
