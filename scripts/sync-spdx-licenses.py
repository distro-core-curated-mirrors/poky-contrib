#! /usr/bin/env python3
#
# SPDX-License-Identifier: GPL-2.0-only

import json
import argparse
import urllib.request
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Pull the latest SPDX license files")
    parser.add_argument(
        "--corebase",
        help="Path to OE-core",
        type=Path,
        default=Path(__file__).parent.parent,
    )

    args = parser.parse_args()

    with urllib.request.urlopen(
        "https://raw.githubusercontent.com/spdx/license-list-data/master/json/licenses.json"
    ) as f:
        data = f.read().decode("utf-8")

    licenses = json.loads(data)

    for lic in licenses["licenses"]:
        print(f"Processing {lic['licenseId']}")
        details_url = lic["detailsUrl"]

        with urllib.request.urlopen(details_url) as f:
            details = json.load(f)

        lic_text_file = (
            args.corebase / "meta" / "files" / "common-licenses" / lic["licenseId"]
        )
        with lic_text_file.open("w") as f:
            f.write(details["licenseText"])

    lic_json = args.corebase / "meta" / "files" / "spdx-licenses.json"
    with lic_json.open("w") as f:
        f.write(data)


if __name__ == "__main__":
    sys.exit(main())
