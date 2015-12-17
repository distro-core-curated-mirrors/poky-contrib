#!/bin/python

import os
import subprocess

def store_log(results, temp_dir, task_name):

    logfile = "%s/log.%s" % (temp_dir, task_name)
    runfile = "%s/run.%s" % (temp_dir, task_name)

    rf = open(runfile, 'w')
    lf = open(logfile, 'w')

    for res in results:
        cmd, stdout = res['cmd'], res['stdout']
        rf.write("%s\n" % ' '.join(cmd))
        lf.write(str(stdout))

    rf.close()
    lf.close()

    return (rf.name, lf.name)

def exec_cmds(cmds, cwd, temp_dir=None, task_name=None):
    """" Executes cmds and store logs if temp_dir is non-None

         Input:
             cmds: Array of dictionaries, containing the commands
                   [
                       {'cmd':[<cmd1>]},
                       {'cmd':[<cmd2>], 'ignore_error':True},
                       .
                       .
                       .
                       {'cmd':[<cmdn>]},
                   ]
             NOTE: the key ignore_error is optional; if not included, the
             output will set it as 'ignore_error':False

             cwd: directory where commands are executed

         Output:
         [{'cmd':<cmd>,
           'ignore_error':<True|False>,
           'stdout':<stdout>,
           'stderr':<stderr>,
           'returncode':<returncode>},
           .
           .
           .
          {'cmd':<cmd>,
           'ignore_error':<True|False>,
           'stdout':<stdout>,
           'stderr':<stderr>,
           'returncode':<returncode>},
         ]
    """
    results = []
    _cmds = cmds

    for cmd in _cmds:
        _cmd = map(str, cmd['cmd'])
        p = subprocess.Popen(_cmd,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             cwd=cwd)
        (stdout, stderr) = p.communicate()

        if cmd.has_key('ignore_error'):
            ignore_error = cmd['ignore_error']
        else:
            ignore_error = False

        result = {
            'cmd':_cmd,
            'ignore_error': ignore_error,
            'stdout':stdout,
            'stderr':stderr,
            'returncode':p.returncode
        }
        results.append(result)

    if temp_dir:
        store_log(results, temp_dir, task_name)

    return results

def get_mbox_url(pw_url, series, revision):
    return  "%s/api/1.0/series/%s/revisions/%s/mbox/" % (pw_url, series, revision)

def get_commit_id(commit, cwd):
    cmds = [
        {'cmd':['git', 'rev-parse', commit]}
    ]
    return exec_cmds(cmds, cwd)[0]['stdout']

def get_scm_url(pw_url, pw_project):
    # TODO: we should generalize to any other repository
    return  "http://git.yoctoproject.org/git/poky"

def get_temp_dir(base_dir, series, revision):
    return "%s/%s-%s" % (base_dir, series, revision)

def branch_name(series, revision):
    return "series-%s-revision-%s" % (series, revision)

def all_succeed(results):
    def _succeed(res):
        if res['ignore_error']:
            return True
        else:
            return res['returncode'] == 0

    boolean_returncodes = map(_succeed, results)
    return all(boolean_returncodes)

def post(series, revision, test_name, state, summary, url, cwd):
    """ Post results """
    cmds = [
        {'cmd':['git', 'pw', 'post-result',
                series,
                test_name,
                state,
                '--summary', summary,
                '--revision', revision,
                '--url', url]},
    ]

    ret = exec_cmds(cmds, cwd)
    if not all_succeed(ret):
        msg =  "Results for test %s could not be POSTed (check PW user's credentials)" % test_name
        msg += " for series/revision: %s/%s" %  (series, revision)
        raise Exception, msg

