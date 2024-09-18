# Checks related to the patch's author
#
# Copyright (C) 2016 Intel Corporation
#
# SPDX-License-Identifier: GPL-2.0-only

import base
import collections
import patterns
import pyparsing
import re
import subprocess
from patchtest_parser import PatchtestParser

def headlog():
    output = subprocess.check_output(
        "cd %s; git log --pretty='%%h#%%aN#%%cD:#%%s' -1" % PatchtestParser.repodir,
        universal_newlines=True,
        shell=True
        )
    return output.split('#')

class TestMbox(base.Base):

    # base paths of main yocto project sub-projects
    paths = {
        'oe-core': ['meta-selftest', 'meta-skeleton', 'meta', 'scripts'],
        'bitbake': ['bitbake'],
        'documentation': ['documentation'],
        'poky': ['meta-poky','meta-yocto-bsp'],
        'oe': ['meta-filesystems', 'meta-gnome', 'meta-initramfs',
               'meta-multimedia', 'meta-networking','meta-oe',
               'meta-perl', 'meta-python', 'meta-webserver', 'meta-xfce']
        }

    Project = collections.namedtuple('Project', ['name', 'listemail', 'gitrepo', 'paths'])

    bitbake = Project(name='Bitbake', listemail='bitbake-devel@lists.openembedded.org', gitrepo='http://git.openembedded.org/bitbake/', paths=paths['bitbake'])
    doc     = Project(name='Documentantion', listemail='yocto@yoctoproject.org', gitrepo='http://git.yoctoproject.org/cgit/cgit.cgi/yocto-docs/', paths=paths['documentation'])
    poky    = Project(name='Poky', listemail='poky@yoctoproject.org', gitrepo='http://git.yoctoproject.org/cgit/cgit.cgi/poky/', paths=paths['poky'])
    oe      = Project(name='oe', listemail='openembedded-devel@lists.openembedded.org', gitrepo='http://git.openembedded.org/meta-openembedded/', paths=paths['oe'])


    def test_signed_off_by_presence(self):
        for commit in self.commits:
            # skip those patches that revert older commits, these do not required the tag presence
            if patterns.mbox_revert_shortlog_regex.search_string(commit.shortlog):
                continue
            if not patterns.signed_off_by.search_string(commit.payload):
                self.fail('Mbox is missing Signed-off-by. Add it manually or with "git commit --amend -s"',
                          commit=commit)

    def test_shortlog_format(self):
        for commit in self.commits:
            shortlog = commit.shortlog
            if not shortlog.strip():
                self.skip('Empty shortlog, no reason to execute shortlog format test')
            else:
                # no reason to re-check on revert shortlogs
                if shortlog.startswith('Revert "'):
                    continue
                try:
                    patterns.shortlog.parseString(shortlog)
                except pyparsing.ParseException as pe:
                    self.fail('Commit shortlog (first line of commit message) should follow the format "<target>: <summary>"',
                              commit=commit)

    def test_shortlog_length(self):
        for commit in self.commits:
            # no reason to re-check on revert shortlogs
            shortlog = re.sub('^(\[.*?\])+ ', '', commit.shortlog)
            if shortlog.startswith('Revert "'):
                continue
            l = len(shortlog)
            if l > patterns.mbox_shortlog_maxlength:
                self.fail('Edit shortlog so that it is %d characters or less (currently %d characters)' % (patterns.mbox_shortlog_maxlength, l),
                          commit=commit)

    def test_series_merge_on_head(self):
        if PatchtestParser.repo.patch.branch != "master":
            self.skip(
                "Skipping merge test since patch is not intended"
                " for master branch. Target detected is %s"
                % PatchtestParser.repo.patch.branch
            )
        if not PatchtestParser.repo.canbemerged:
            commithash, author, date, shortlog = headlog()
            self.fail(
                "Series does not apply on top of target branch %s"
                % PatchtestParser.repo.patch.branch,
                data=[
                    (
                        "Targeted branch",
                        "%s (currently at %s)"
                        % (PatchtestParser.repo.patch.branch, commithash),
                    )
                ],
            )

    def test_target_mailing_list(self):
        """Check for other targeted projects"""

        # a meta project may be indicted in the message subject, if this is the case, just fail
        # TODO: there may be other project with no-meta prefix, we also need to detect these
        project_regex = pyparsing.Regex("\[(?P<project>meta-.+)\]")
        for commit in self.commits:
            match = project_regex.search_string(commit.subject)
            if match:
                self.fail('Series sent to the wrong mailing list or some patches from the series correspond to different mailing lists',
                          commit=commit)

        for patch in self.patchset:
            folders = patch.path.split('/')
            base_path = folders[0]
            for project in [self.bitbake, self.doc, self.oe, self.poky]:
                if base_path in project.paths:
                    self.fail('Series sent to the wrong mailing list or some patches from the series correspond to different mailing lists',
                              data=[('Suggested ML', '%s [%s]' % (project.listemail, project.gitrepo)),
                                    ('Patch\'s path:', patch.path)])

    def test_mbox_format(self):
        if self.unidiff_parse_error:
            self.fail('Series has malformed diff lines. Create the series again using git-format-patch and ensure it applies using git am',
                      data=[('Diff line',self.unidiff_parse_error)])

    def test_commit_message_presence(self):
        for commit in self.commits:
            if not commit.commit_message.strip():
                self.fail('Please include a commit message on your patch explaining the change', commit=commit)

    def test_bugzilla_entry_format(self):
        for commit in self.commits:
            if not patterns.mbox_bugzilla.search_string(commit.commit_message):
                self.skip("No bug ID found")
            elif not patterns.mbox_bugzilla_validation.search_string(commit.commit_message):
                self.fail('Bugzilla issue ID is not correctly formatted - specify it with format: "[YOCTO #<bugzilla ID>]"', commit=commit)

    def test_author_valid(self):
        for commit in self.commits:
            for invalid in patterns.invalid_submitters:
                if invalid.search_string(commit.author):
                    self.fail('Invalid author %s. Resend the series with a valid patch author' % commit.author, commit=commit)

    def test_non_auh_upgrade(self):
        for commit in self.commits:
            if patterns.auh_email in commit.commit_message:
                self.fail('Invalid author %s. Resend the series with a valid patch author' % patterns.auh_email, commit=commit)
