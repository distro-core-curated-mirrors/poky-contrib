#! /usr/bin/env python3

import argparse
import datetime

import os
import sys
scripts_path = os.path.dirname(os.path.realpath(__file__))
lib_path = scripts_path + "/lib"
sys.path.insert(0, lib_path)
import scriptpath
scriptpath.add_bitbake_lib_path()
scriptpath.add_oe_lib_path()

import bb.tinfoil
import bb.fetch
import bb.utils
import oe.recipeutils
import oe.patch

def cached(cachefile):
    """
    A function that creates a decorator which will use "cachefile" for caching the results of the decorated function "fn".
    """
    def decorator(fn):
        def wrapped(*args, **kwargs):
            import pickle
            if os.path.exists(cachefile):
                    with open(cachefile, 'rb') as cachehandle:
                        print("using cached result from '%s'" % cachefile)
                        return pickle.load(cachehandle)
            res = fn(*args, **kwargs)
            with open(cachefile, 'wb') as cachehandle:
                print("saving result to cache '%s'" % cachefile)
                pickle.dump(res, cachehandle)
            return res
        return wrapped
    return decorator

recipes = ("virtual/kernel",
           "scp-firmware",
           "trusted-firmware-a",
           "trusted-firmware-m",
           "edk2-firmware",
           "u-boot",
           "optee-os")

def is_old(version, upstream):
    if "+git" in version:
        # strip +git and see if this is a post-release snaoshot
        version = version.replace("+git", "")
    return version != upstream

def write_html(context, output):
    import jinja2

    template_dir = os.path.dirname(os.path.abspath(__file__))

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        autoescape=jinja2.select_autoescape()
    )
    env.tests["old"] = is_old
    template = env.get_template("machine-summary.html")
    output.write(template.render(context))

def trim_pv(pv):
    """
    Strip anything after +git from the PV
    """
    return "".join(pv.partition("+git")[:2])

@cached("harvest_data.pickle")
def harvest_data(machines, recipes):
    # Queue of recipes that we're still looking for upstream releases for
    to_check = list(recipes)

    # Upstream releases
    releases = {}
    # Machines to recipes to versions
    versions = {}

    for machine in machines:
        # TODO progress bar
        os.environ["MACHINE"] = machine
        with bb.tinfoil.Tinfoil() as tinfoil:
            versions[machine] = {}

            # TODO silence reconnecting message
            tinfoil.prepare(quiet=2)
            for recipe in recipes:
                try:
                    d = tinfoil.parse_recipe(recipe)
                except bb.providers.NoProvider:
                    continue

                details = versions[machine][recipe] = {}
                details["recipe"] = d.getVar("PN")
                details["version"] = trim_pv(d.getVar("PV"))
                details["patched"] = bool(oe.patch.src_patches(d))

                if recipe in to_check:
                    try:
                        info = oe.recipeutils.get_recipe_upstream_version(d)
                        releases[recipe] = info["version"]
                        to_check.remove(recipe)
                    except (bb.providers.NoProvider, KeyError):
                        pass

    return releases, versions

# TODO releases logic only mostly works as we assume qemuarm64 is first.
# Will one run with PARSE_ALL_RECIPES let me see all recipes for upstream checks?
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="machine-summary-report")
    parser.add_argument("machines", nargs="+", help="machine names", metavar="MACHINE")
    parser.add_argument("-o", "--output", required=True, type=argparse.FileType('w', encoding='UTF-8'))
    args = parser.parse_args()

    context = {}
    context["timestamp"] = str(datetime.datetime.now().strftime("%c"))
    # TODO: include git describe for meta-arm
    context["recipes"] = sorted(recipes)
    context["releases"], context["data"] = harvest_data(args.machines, recipes)
    write_html(context, args.output)
