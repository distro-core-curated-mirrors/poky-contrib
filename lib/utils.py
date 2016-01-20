#!/bin/python

import os
import subprocess
import logging

class CmdException(Exception):
    pass

def exec_cmd(cmd, cwd, ignore_error=False):
    """
         Input:
            cmd: dict containing 'cmd' and 'ignore_error' as keys:
                       {'cmd':[<cmd>], 'ignore_error':True}

             NOTE: the key 'ignore_error' is optional; if not included, the
             default is the one specify in the corresponding argument

             cwd: directory where commands are executed

         Output: dict containing the following key/values
             {'cmd':<cmd>,
              'ignore_error':<True|False>,
              'stdout':<stdout>,
              'stderr':<stderr>,
              'returncode':<returncode>}
    """
    _cmd = map(str, cmd['cmd'])
    p = subprocess.Popen(_cmd,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         cwd=cwd)
    (stdout, stderr) = p.communicate()

    _ignore_error = ignore_error
    if cmd.has_key('ignore_error'):
        _ignore_error = cmd['ignore_error']

    if not _ignore_error and p.returncode:
        raise CmdException, 'Command failed to execute: %s' % ' '.join(_cmd)

    return {'cmd':_cmd,
            'ignore_error': ignore_error,
            'stdout':stdout.strip(),
            'stderr':stderr.strip(),
            'returncode':p.returncode}

def exec_cmds(cmds, cwd):
    """ Executes commands

         Input:
             cmds: Array of commands
             cwd: directory where commands are executed

         Output: Array of output commands
    """
    results = []
    _cmds = cmds

    for cmd in _cmds:
        result = exec_cmd(cmd, cwd)
        results.append(result)

    return results

def all_succeed(results):
    def _succeed(res):
        if res['ignore_error']:
            return True
        else:
            return res['returncode'] == 0

    boolean_returncodes = map(_succeed, results)
    return all(boolean_returncodes)

def logger_create(name):
    logger = logging.getLogger(name)
    loggerhandler = logging.StreamHandler()
    loggerhandler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.addHandler(loggerhandler)
    logger.setLevel(logging.INFO)
    return logger
