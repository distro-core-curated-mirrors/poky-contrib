#! /usr/bin/env python3
#
# SPDX-License-Identifier: GPL-2.0-only

import json
import argparse
import urllib3
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

    http = urllib3.PoolManager()
    r = http.request("GET", "https://raw.githubusercontent.com/spdx/license-list-data/master/json/licenses.json")

    license_str = r.data.decode("utf-8")
    lic_json = args.corebase / "meta" / "files" / "spdx-licenses.json"
    with lic_json.open("w") as f:
        f.write(license_str)

    licenses = json.loads(license_str)
    for lic in licenses["licenses"]:
        print(f"Processing {lic['licenseId']}")
        details_url = lic["detailsUrl"]

        r = http.request("GET", details_url)
        details = json.loads(r.data.decode("utf-8"))

        lic_text_file = (
            args.corebase / "meta" / "files" / "common-licenses" / lic["licenseId"]
        )
        with lic_text_file.open("w") as f:
            f.write(details["licenseText"])

if __name__ == "__main__":
    sys.exit(main())
