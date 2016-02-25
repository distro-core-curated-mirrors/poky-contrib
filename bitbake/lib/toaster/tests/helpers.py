#!/usr/bin/env python

# Toaster helper for clone/setup/start/stop
#
# Copyright (C) 2016 Intel Corporation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import subprocess
import os
import shutil
import signal
import tempfile

from proc.core import find_processes

TOASTER_TEST_BRANCH = 'toaster_tests'
VENV_NAME = 'venv'
SHELL_CMD = os.environ['SHELL'] if 'SHELL' in os.environ else "/bin/bash"
TOASTER_BUILD_DIR_NAME = 'build'

def _check_output1(*popenargs, **kwargs):
    """
        Almost the same as subprocess.check_output but change the stdout from
        PIPE to tempfile to avoid deadlocks when trying to read the PIPE using
        communicate(). This scenario can be seen calling toaster_start on failure
        scenarios.

        This causes a little overhead by the tempfile.
    """

    f = tempfile.TemporaryFile(mode='rw+')
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    process = subprocess.Popen(stdout=f, *popenargs, **kwargs)
    retcode = process.wait()

    f.flush()
    os.fsync(f.fileno())
    f.seek(0, 0)
    output = f.read()
    f.close()

    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise subprocess.CalledProcessError(retcode, cmd, output=output)
    return output

class ToasterHelper(object):
    def __init__(self, directory, repo, repo_ref='master', port='8000',
            build_dir=TOASTER_BUILD_DIR_NAME):
        self.directory = directory
        self.repo = repo
        self.repo_ref = repo_ref
        self.port = port
        self.build_dir = build_dir

    def _execute_command(self, cmd):
        return _check_output1([SHELL_CMD, "-c", "cd %s; %s" % \
            (self.directory, cmd)], stderr=subprocess.STDOUT)

    def _execute_command_oe(self, cmd):
        return self._execute_command("source oe-init-build-env %s; %s"\
            % (self.build_dir, cmd))

    def _execute_command_oe_venv(self, cmd):
        return self._execute_command_oe("source %s/bin/activate; %s"\
                % (VENV_NAME, cmd))

    def clone(self, rm=False):
        if os.path.exists(self.directory):
            if rm:
                shutil.rmtree(self.directory)
            else:
                raise IOError

        subprocess.check_output([SHELL_CMD, "-c", "git clone %s %s" %\
            (self.repo, self.directory)], stderr=subprocess.STDOUT)
        self._execute_command("git checkout %s; git branch %s; git checkout %s;"\
            % (self.repo_ref, TOASTER_TEST_BRANCH, TOASTER_TEST_BRANCH))

    def setup(self):
        self._execute_command_oe("virtualenv %s" % VENV_NAME)
        self._execute_command_oe_venv("pip install -r" \
            " ../bitbake/toaster-requirements.txt")
        self._execute_command_oe_venv("pip install -r" \
            " ../bitbake/toaster-tests-requirements.txt")

    def start(self):
        return self._execute_command_oe_venv("source %s/bitbake/bin/toaster"\
            " start webport=%s" % (self.directory, self.port))

    def _stop_force(self):
        """
            The _stop_force method iterates over the /proc and search for toaster path
            in the process cmdline then send SIGKILL for every matched process.
        """

        pids = []
        for p in find_processes():
            if len(p.cmdline) > 1 and \
                os.path.basename(p.cmdline[0]) == 'python' and \
                p.cmdline[1].startswith(self.directory):
                    pids.append(p.pid)

        for pid in pids:
            try:
                print "killing ",pid
                os.kill(pid, signal.SIGKILL)
            except:
                pass

        return ''

    def stop(self, force=False):
        """
            The stop method have force mode because toaster without production
            setup have known issues when is on load, the server response 503
            service unavailable.
        """
        if force:
            return self._stop_force()
        else:
            return self._execute_command_oe_venv("source %s/bitbake/bin/toaster"\
                " stop webport=%s" % (self.directory, self.port))

    def get_sqlite_path(self):
        return os.path.join(self.directory, self.build_dir, 'toaster.sqlite')

    def get_conf_path(self):
        output = self._execute_command_oe_venv("source %s/bitbake/bin/toaster"\
            " start webport=%s; echo $TOASTER_CONF;" % \
            (self.directory, self.port))

        return output.split()[-1]

DEFAULT_WORK_DIRECTORY = '/tmp/toaster'
DEFAULT_POKY_URL = 'http://git.yoctoproject.org/git/poky.git'
DEFAULT_POKY_BRANCH = 'master'
DEFAULT_WEB_PORT = '8000'

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Toaster helper',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-a", "--action", choices=['clone', 'setup', 'start', 'stop'],
        required=True,
        help="Action to execute can be clone/setup/start/stop")
    parser.add_argument("-d", "--work-directory", default=DEFAULT_WORK_DIRECTORY,
        help="Directory for setup toaster, default: %s" % DEFAULT_WORK_DIRECTORY)
    parser.add_argument("-u", "--url-repository", default=DEFAULT_POKY_URL,
        help="GIT repository for setup toaster, default %s" % DEFAULT_POKY_URL)
    parser.add_argument("-r", "--revision", default=DEFAULT_POKY_BRANCH,
        help="GIT repository revision (branch, tag, hash) for setup toaster" \
        ", default: %s" % DEFAULT_POKY_BRANCH)
    parser.add_argument("-p", "--web-port", default=DEFAULT_WEB_PORT,
        help="Web port for start toaster server, default: %s" % DEFAULT_WEB_PORT)
    parser.add_argument("-b", "--build-dir", default=TOASTER_BUILD_DIR_NAME,
        help="Toaster build directory name, default: %s" % TOASTER_BUILD_DIR_NAME)

    args = parser.parse_args()

    try:
        th = ToasterHelper(args.work_directory, args.url_repository,
            args.revision, args.web_port, args.build_dir)
        if args.action == 'stop':
            th.stop(force=True)
        else:
            getattr(th, args.action)()
    except subprocess.CalledProcessError as e:
        print e.output
        raise
    except IOError as e:
        if args.action == 'clone':
            print "ERROR: Directory exists: %s" % args.work_directory
        raise

    sys.exit(0)
