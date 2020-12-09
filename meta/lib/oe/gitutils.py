#
# SPDX-License-Identifier: GPL-2.0-only
#

import os
import bb.process


def find_git_repos(pth, toplevel=False):
    """
    Find git repositories under a path
    """
    repos = []
    if toplevel and os.path.isdir(os.path.join(pth, '.git')):
        repos.append(pth)
    for root, dirs, _ in os.walk(pth):
        if '.git' in dirs:
            dirs.remove('.git')
        for dfn in dirs:
            dfp = os.path.join(root, dfn)
            if os.path.isdir(os.path.join(dfp, '.git')) and dfp not in repos:
                repos.append(dfp)
    return repos


def get_repo_status(repodir):
    """
    Check if a git repository is clean or not
    """
    stdout, _ = bb.process.run('git status --porcelain', cwd=repodir)
    return stdout
