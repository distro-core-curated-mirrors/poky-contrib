import os
import subprocess
import logging

def dict_append_new(d, k, v):
    if k in d:
        d[k].append(v)
    else:
        d[k] = [v]

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

    _command = [str(e) for e in _cmd['cmd']]
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

# Patchwork - automated patch tracking system
# Copyright (C) 2008 Jeremy Kerr <jk@ozlabs.org>
#
# This file is part of the Patchwork package.
#
# Patchwork is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Patchwork is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Patchwork; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import re

_hunk_re = re.compile('^\@\@ -\d+(?:,(\d+))? \+\d+(?:,(\d+))? \@\@')
_filename_re = re.compile('^(---|\+\+\+) (\S+)')

def parse_patch(text):
    patchbuf = ''
    commentbuf = ''
    buf = ''

    # state specified the line we just saw, and what to expect next
    state = 0
    # 0: text
    # 1: suspected patch header (diff, ====, Index:)
    # 2: patch header line 1 (---)
    # 3: patch header line 2 (+++)
    # 4: patch hunk header line (@@ line)
    # 5: patch hunk content
    # 6: patch meta header (rename from/rename to)
    #
    # valid transitions:
    #  0 -> 1 (diff, ===, Index:)
    #  0 -> 2 (---)
    #  1 -> 2 (---)
    #  2 -> 3 (+++)
    #  3 -> 4 (@@ line)
    #  4 -> 5 (patch content)
    #  5 -> 1 (run out of lines from @@-specifed count)
    #  1 -> 6 (rename from / rename to)
    #  6 -> 2 (---)
    #  6 -> 1 (other text)
    #
    # Suspected patch header is stored into buf, and appended to
    # patchbuf if we find a following hunk. Otherwise, append to
    # comment after parsing.

    # line counts while parsing a patch hunk
    lc = (0, 0)
    hunk = 0

    for line in text.split('\n'):
        line += '\n'

        if state == 0:
            if line.startswith('diff ') or line.startswith('===') \
                    or line.startswith('Index: '):
                state = 1
                buf += line

            elif line.startswith('--- '):
                state = 2
                buf += line

            else:
                commentbuf += line

        elif state == 1:
            buf += line
            if line.startswith('--- '):
                state = 2

            if line.startswith('rename from ') or line.startswith('rename to '):
                state = 6

        elif state == 2:
            if line.startswith('+++ '):
                state = 3
                buf += line

            elif hunk:
                state = 1
                buf += line

            else:
                state = 0
                commentbuf += buf + line
                buf = ''

        elif state == 3:
            match = _hunk_re.match(line)
            if match:

                def fn(x):
                    if not x:
                        return 1
                    return int(x)

                lc = map(fn, match.groups())

                state = 4
                patchbuf += buf + line
                buf = ''

            elif line.startswith('--- '):
                patchbuf += buf + line
                buf = ''
                state = 2

            elif hunk and line.startswith('\ No newline at end of file'):
                # If we had a hunk and now we see this, it's part of the patch,
                # and we're still expecting another @@ line.
                patchbuf += line

            elif hunk:
                state = 1
                buf += line

            else:
                state = 0
                commentbuf += buf + line
                buf = ''

        elif state == 4 or state == 5:
            if line.startswith('-'):
                lc[0] -= 1
            elif line.startswith('+'):
                lc[1] -= 1
            elif line.startswith('\ No newline at end of file'):
                # Special case: Not included as part of the hunk's line count
                pass
            else:
                lc[0] -= 1
                lc[1] -= 1

            patchbuf += line

            if lc[0] <= 0 and lc[1] <= 0:
                state = 3
                hunk += 1
            else:
                state = 5

        elif state == 6:
            if line.startswith('rename to ') or line.startswith('rename from '):
                patchbuf += buf + line
                buf = ''

            elif line.startswith('--- '):
                patchbuf += buf + line
                buf = ''
                state = 2

            else:
                buf += line
                state = 1

        else:
            raise Exception("Unknown state %d! (line '%s')" % (state, line))

    commentbuf += buf

    if patchbuf == '':
        patchbuf = None

    if commentbuf == '':
        commentbuf = None

    return (patchbuf, commentbuf)
