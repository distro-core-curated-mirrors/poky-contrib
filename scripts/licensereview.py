#! /usr/bin/env python3

import argparse
import hashlib

import os
import sys
scripts_path = os.path.dirname(os.path.realpath(__file__))
lib_path = scripts_path + "/lib"
sys.path.insert(0, lib_path)
import scriptpath
scriptpath.add_bitbake_lib_path()

import bb.tinfoil
import bb.fetch
import bb.utils

def write_html(context, output):
    import jinja2
    env = jinja2.Environment(
        # TODO not hardcoded path
        loader=jinja2.FileSystemLoader("/home/ross/Yocto/poky/scripts"),
        autoescape=jinja2.select_autoescape()
    )
    template = env.get_template("licensereview.html")
    with open(output, "wt") as f:
        f.write(template.render(context))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="licensereview")
    # TODO: more ways of listing what to report on.
    parser.add_argument("layers", nargs="+", help="layer names", metavar="LAYER")
    parser.add_argument("-o", "--output", required=True)
    args = parser.parse_args()

    context = {
        "layers": args.layers,
        "recipes": {},
    }

    with bb.tinfoil.Tinfoil() as tinfoil:
        recipes = []
        tinfoil.prepare()

        # Sanity check the layers
        all_layers = set(tinfoil.config_data.getVar("BBFILE_COLLECTIONS").split())
        missing = set(args.layers) - all_layers
        if missing:
            print(f"Cannot find the following layers: {', '.join(missing)}", file=sys.stderr)
            sys.exit(1)
        
        # Collect all recipes in the specified layers
        for recipe in tinfoil.all_recipes():
            # Skip virtual recipes
            if recipe.fn.startswith("virtual:"):
                continue

            layer = bb.utils.get_file_layer(recipe.fn, tinfoil.config_data)
            if layer in args.layers:
                recipes.append(recipe)

        # Unpack all the recipes we collected
        tinfoil.build_targets([r.pn for r in recipes], "unpack")

        for recipe in recipes:
            rd = tinfoil.parse_recipe_file(recipe.fn)
            sourcedir = rd.getVar("S")

            recipe_context = {
                "license": rd.getVar("LICENSE"),
                "texts": {}
            }

            license_checksums = rd.getVar("LIC_FILES_CHKSUM")
            if not license_checksums:
                print(f"No checksums for {recipe.pn}", file=sys.stderr)
                continue
            license_checksums = license_checksums.split()

            for url in license_checksums:
                (method, host, path, user, password, params) = bb.fetch.decodeurl(url)
                if method != "file":
                    print(f"Not sure how to handle {method}", file=sys.stderr)
                    continue

                # Thanks to join()s special behaviour with / in components, we can
                # just do this to handle relative and absolute paths.
                filename = os.path.join(sourcedir, path)
                # Line numbers are 1-based
                beginline = int(params.get("beginline", 1)) - 1
                endline = int(params.get("endline", 1)) - 1

                hasher = hashlib.md5()
                with open(filename, "rb") as f:
                    if beginline or endline:
                        lines = f.readlines()
                        if not endline:
                            endline = len(lines)
                        lines = lines[beginline:endline]

                        licensetext = []
                        for l in lines:
                            licensetext.append(l.decode("utf-8", errors="replace").rstrip())
                            hasher.update(l)
                        licensetext = "\n".join(licensetext)
                    else:
                        contents = f.read()
                        hasher.update(contents)
                        licensetext = contents.decode("utf-8", errors="replace")
                real_md5 = hasher.hexdigest()

                if real_md5 != params["md5"]:
                    print(f"MD5 mismatch for {filename}", file=sys.stderr)
                    continue
                recipe_context["texts"][path] = licensetext

            context["recipes"][recipe.pn] = recipe_context

    write_html(context, args.output)
