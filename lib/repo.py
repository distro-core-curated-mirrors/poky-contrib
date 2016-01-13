import inspect
import os
import utils
import git

class RepoException(Exception):
    pass

# We need to differentiate errors from clean/fetch/branch and failures when
# branching
class PatchException(Exception):
    pass

class Repo(object):
    def __init__(self, series, revision, repodir, tempbasedir):
        self.series = series
        self.revision = revision
        self.repodir = repodir
        self.tempbasedir = tempbasedir

        # get the rest of the variables from the git's configuration
        self._setup()

    @property
    def mboxurl(self):
        return "%s/api/1.0/series/%s/revisions/%s/mbox/" % (self.url,
                                                            self.series,
                                                            self.revision)

    @property
    def tempdir(self):
        return "%s/patchtest-%s-%s" % (self.tempbasedir, self.series, self.revision)

    @property
    def branchname(self):
        return "patchtest-%s-%s" % (self.series, self.revision)

    @property
    def head(self):
        if not hasattr(self, 'head_id'):
            cmds = [
                {'cmd':['git', 'rev-parse', 'HEAD']}
            ]
            self.head_id = utils.exec_cmds(cmds, self.repodir)[0]['stdout']
        return self.head_id

    def _setup(self):
        try:
            self.repo = git.Repo(self.repodir)
        except git.exc.InvalidGitRepositoryError:
            raise RepoException('Not a git repository.')

        config = self.repo.config_reader()

        try:
            patchwork_section = 'patchwork "%s"' % 'default'
            self.url = config.get(patchwork_section, 'url')
            self.project = config.get(patchwork_section, 'project')
        except:
            raise RepoException('patchwork url/project configuration is not available')

        try:
            patchtest_section = 'patchtest "%s"' % 'default'
            self.stable = config.get(patchtest_section, 'stable')
        except:
            self.stable = 'origin/master'

        if not os.path.exists(self.tempdir):
            os.makedirs(self.tempdir)

    def _exec(self, cmds):
        stack = inspect.stack()
        taskname = stack[1][3]
        return utils.exec_cmds(cmds, self.repodir, self.tempdir, taskname)

    def clean(self, removebranch=False):
        git_pw_poll = '.git-pw.%s.poll.timestamp' % self.project
        print git_pw_poll
        cmds = [
            {'cmd':['git', 'clean', '-df', '-e', '.git-pw.%s.poll.timestamp' % self.project]},
            {'cmd':['git', 'am', '--abort'], 'ignore_error':True},
            {'cmd':['git', 'reset', '--hard']},
            {'cmd':['git', 'checkout', self.stable]},
        ]

        if removebranch:
            cmds.append({'cmd':['git', 'branch', '-D', self.branchname]})

        if not utils.all_succeed(self._exec(cmds)):
            raise RepoException('Repository cannot be cleaned')

    def fetch(self):
        remote, branch = self.stable.split('/')
        cmds = [
            {'cmd':['git', 'fetch', '%s' % remote]},
        ]
        if not utils.all_succeed(self._exec(cmds)):
            raise RepoException('Repository cannot be fetched')

    def branch(self):
        cmds = [
            {'cmd':['git', 'checkout', '%s' % self.stable]},
            {'cmd':['git', 'checkout', '-b', self.branchname], 'ignore_error':True},
        ]

        if not utils.all_succeed(self._exec(cmds)):
            raise RepoException('Repo cannot be branched')

    def patch(self):
        cmds = [
            {'cmd':['git', 'pw', 'mbox', self.series, '-r', self.revision]},
            {'cmd':['git', 'pw', 'apply', self.series, '-r', self.revision]},
        ]

        if not utils.all_succeed(self._exec(cmds)):
            msg = "The series/revision cannot be merge on a top of %s/%s" % (self.stable, self.head)
            raise PatchException, msg

    def post(self, testname, state, summary):
        cmds = [
            {'cmd':['git', 'pw', 'post-result',
                    self.series,
                    testname,
                    state,
                    '--summary', summary,
                    '--revision', self.revision]},
        ]

        if not utils.all_succeed(self._exec(cmds)):
            raise RepoException('POST requests cannot be done to %s' % self.url)

