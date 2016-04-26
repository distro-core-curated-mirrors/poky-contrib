#!/usr/bin/env python

import git
import sys
import requests
import argparse
import os

def patchwork_alive(repodir):
    repo = git.Repo(repodir)
    config = repo.config_reader()
    patchwork_section = 'patchwork "%s"' % 'default'
    url = config.get(patchwork_section, 'url')
    url_api = "%s/api/1.0" % url

    alive = False
    try:
        alive = requests.get(url_api).status_code == 200
    except requests.exceptions.ConnectionError:
        pass

    return alive

def main(repodir):
    if patchwork_alive(repodir):
        print "instance alive: %s" % repodir
        return 0
    else:
        print "instance not alive: %s" % repodir
        return -1

if __name__ == '__main__':
    rc = -1

    parser = argparse.ArgumentParser()
    parser.add_argument('-C',
                        dest='repodir',
                        required=True,
                        help="Name of the repository")

    args = parser.parse_args()

    try:
        rc = main(args.repodir)
    except:
        import traceback
        traceback.print_exc(5)

    sys.exit(rc)
