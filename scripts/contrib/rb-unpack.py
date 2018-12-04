#! /usr/bin/env python3

import argparse, os, sys, logging, glob, subprocess

scripts_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/..')
sys.path = sys.path + [scripts_path + '/lib']
import scriptpath
scriptpath.add_bitbake_lib_path()

import bb.tinfoil

parser = argparse.ArgumentParser(description='Extract package')
parser.add_argument("package")
parser.add_argument("--format", "-f")
args = parser.parse_args()

with bb.tinfoil.Tinfoil() as tinfoil:
    tinfoil.prepare()
    d = tinfoil.config_data

    if args.format:
        pkgformat = args.format
    else:
        pkgformat = d.getVar("PACKAGE_CLASSES").split()[0].replace("package_", "")
    deploy_dir = d.getVar("DEPLOY_DIR_%s" % pkgformat.upper())

    recipe = tinfoil.get_recipe_info(args.package)

    matches = glob.glob(os.path.join(deploy_dir, "*", "%s*%s-*.%s" % (recipe.pn, recipe.pv, pkgformat)))
    matches.sort(key=lambda x: len(x))
    filename = matches[0]

    # TODO argparse
    unpackdir = "%s-unpacked" % recipe.pn
    # TODO if present, empty?
    os.makedirs(unpackdir)
    if pkgformat == "rpm":
        # TODO: use .run()
        cpio = subprocess.check_output(["rpm2cpio.sh", filename])
        subprocess.check_output(["cpio", "--extract", "--quiet"], input=cpio, cwd=unpackdir)
        print("Unpacked to %s" % unpackdir)
    else:
        # TODO
        assert False
