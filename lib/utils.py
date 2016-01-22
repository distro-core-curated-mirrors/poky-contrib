#!/bin/python

import os
import subprocess
import logging

class CmdException(Exception):
    """ Simple exception class where its attributes are the ones passed when instantiated """
    def __init__(self, cmd):
        self._cmd = cmd
    def __getattr__(self, name):
        value = None
        if self._cmd.has_key(name):
            value = self._cmd[name]
        return value

def exec_cmd(cmd, cwd, ignore_error=False, input=None, strip=True):
    """
         Input:

            cmd: dict containing the following keys:

                cmd : the command itself as an array of strings
                ignore_error: if False, no exception is raised
                strip: indicates if strip is done on the output (stdout and stderr)
                input: input data to the command (stdin)

            NOTE: keys 'ignore_error' and 'input' are optional; if not included,
            the defaults are the ones specify in the arguments
            cwd: directory where commands are executed
            ignore_error: raise CmdException if command fails to execute and
            this value is False
            input: input data (stdin) for the command

         Output: dict containing the following keys:

             cmd: the same as input
             ignore_error: the same as input
             strip: the same as input
             input: the same as input
             stdout: Standard output after command's execution
             stderr: Standard error after command's execution
             returncode: Return code after command's execution

    """
    cmddefaults = {
        'cmd':'',
        'ignore_error':ignore_error,
        'strip':strip,
        'input':input
    }

    # update input values if necessary
    cmddefaults.update(cmd)

    _cmd = cmddefaults

    if not _cmd['cmd']:
        raise CmdException({'cmd':None, 'stderr':'no command given'})

    _command = map(str, _cmd['cmd'])
    p = subprocess.Popen(_command,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         cwd=cwd)


    # execute the command and strip output
    (_stdout, _stderr) = p.communicate(_cmd['input'])
    if _cmd['strip']:
        _stdout, _stderr = map(str.strip, [_stdout, _stderr])

    # generate the result
    result = _cmd
    result.update({'cmd':_command,'stdout':_stdout,'stderr':_stderr,'returncode':p.returncode})

    # launch exception if necessary
    if not _cmd['ignore_error'] and p.returncode:
        raise CmdException(result)

    return result

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
