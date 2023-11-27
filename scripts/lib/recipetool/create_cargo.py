# Recipe creation tool - cargo support plugin
#
# Copyright (c) 2023 BayLibre, SAS
# Author: Julien Stephan <jstephan@baylibre.com>
#
# SPDX-License-Identifier: GPL-2.0-only
#

import logging
import os
from recipetool.create import RecipeHandler

logger = logging.getLogger("recipetool")

tinfoil = None


def tinfoil_init(instance):
    global tinfoil
    tinfoil = instance


class CargoRecipeHandler(RecipeHandler):
    """
    Base class to support rust crate
    """

    # The supported metadata list
    # Exaustive list available here: https://doc.rust-lang.org/cargo/reference/manifest.html#the-manifest-format
    manifest_package_table = [
        "name",
        "version",
        "homepage",
        "description",
        "license",
        "license-file",
        "dependencies",
    ]

    bbvar_map = {
        "name": "PN",
        "version": "PV",
        "homepage": "HOMEPAGE",
        "description": "SUMMARY",
        "license": "LICENSE",
    }

    def __init__(self):
        pass

    def process(
        self, srctree, classes, lines_before, lines_after, handled, extravalues
    ):
        if "buildsystem" in handled:
            return False

        # Check for non-zero size Cargo.toml file
        manifestfiles = RecipeHandler.checkfiles(srctree, ["Cargo.toml"])
        for fn in manifestfiles:
            if os.path.getsize(fn):
                break
        else:
            return False

        manifest = os.path.join(srctree, "Cargo.toml")

        lockfile = RecipeHandler.checkfiles(srctree, ["Cargo.lock"])
        if lockfile == []:
            logger.error(
                "No cargo lock found, this is not yet supported, falling back to another method"
            )
            return False

        try:
            import tomllib
        except ImportError:
            try:
                import tomli as tomllib
            except ImportError:
                logger.exception(
                    "Neither 'tomllib' nor 'tomli' could be imported. Please use python3.11 or above or install tomli module"
                )
                return False
            except Exception:
                logger.exception("Failed to parse pyproject.toml")
                return False

        try:
            with open(manifest, "rb") as f:
                config = tomllib.load(f)

            metadata = config["package"]

            if metadata:
                for field, value in metadata.items():
                    if field in self.manifest_package_table:
                        if field == "license":
                            # license field is an SPDX 2.1 license expression
                            # https://doc.rust-lang.org/cargo/reference/manifest.html#the-license-and-license-file-fields
                            value = value.replace("AND", "&")
                            value = value.replace("OR", "|")
                            # even if deprecated we can still find some old crate using "/" to separate mulitple licenses
                            value = value.replace("/", " & ")
                        elif field == "license-file":
                            # TODO: handle this properly
                            continue

                        extravalues[self.bbvar_map[field]] = value

            if "dependencies" in extravalues:
                lines_after.append("include ${BPN}-crates.inc")
                extravalues.pop("dependencies")
            classes.append("cargo")
            classes.append("cargo-update-recipe-crates")
            handled.append("buildsystem")
        except Exception:
            logger.exception(
                "Failed to correctly handle Cargo.toml, falling back to another method"
            )
            return False


def register_recipe_handlers(handlers):
    # We need to make sure these are ahead of the makefile fallback handler
    handlers.append((CargoRecipeHandler(), 80))
