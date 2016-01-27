# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
"""
BitBake 'Fetch' NPM implementation

The NPM fetcher is used to retrieve files from the npmjs repository

Usage in the recipe:

    SRC_URI = "npm://www.npmjs.com/package/colors"
    SRCREV = "0.0.0"

    npm://registry.npmjs.org/${PN}/-/${PN}-${PV}.tgz  would become npm://registry.npmjs.org;name=${PN};ver=${PV}
    The fetcher all triggers off the existence of ud.localpath. If that exists and has the ".done" stamp, its assumed the fetch is good/done

"""

import os
import sys
import urllib
import json
import subprocess
import signal
import bb
from   bb import data
from   bb.fetch2 import FetchMethod
from   bb.fetch2 import FetchError
from   bb.fetch2 import runfetchcmd
from   bb.fetch2 import logger
from   bb.fetch2 import UnpackError
from   distutils import spawn

def subprocess_setup():
    # Python installs a SIGPIPE handler by default. This is usually not what
    # non-Python subprocesses expect.
    # SIGPIPE errors are known issues with gzip/bash
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

class Npm(FetchMethod):

    """Class to fetch urls via 'npm'"""
    def init(self, d):
        pass

    def supports(self, ud, d):
        """
        Check to see if a given url can be fetched with npm
        """
        return ud.type in ['npm']

    def debug(self, msg):
        logger.debug(1, "NpmFetch: %s", msg)

    def urldata_init(self, ud, d):
        """
        init NPM specific variable within url data
        """
        if 'downloadfilename' in ud.parm:
            ud.basename = ud.parm['downloadfilename']
        else:
            ud.basename = os.path.basename(ud.path)

        ud.localfile = data.expand(urllib.unquote(ud.basename), d)
        ud.parm['subdir'] = "npmpkg"

        self.basecmd = d.getVar("FETCHCMD_wget", True) or "/usr/bin/env wget -t 2 -T 30 -nv --passive-ftp --no-check-certificate"

    def need_update(self, ud, d):
        if os.path.exists(ud.localpath):
            return False
        return True

    def supports_srcrev(self):
        return False

    def sortable_revision(self, ud, d, name):
        return False

    def _runwget(self, ud, d, command, quiet):
        logger.debug(2, "Fetching %s using command '%s'" % (ud.url, command))
        bb.fetch2.check_network_access(d, command)
        runfetchcmd(command, d, quiet)

    def _unpackdep(self, pkg, data, destdir, dldir, d):
       file = data[pkg]['tgz']
       logger.debug(2, "file to extract is %s" % file)
       if file.endswith('.tgz') or file.endswith('.tar.gz') or file.endswith('.tar.Z'):
            cmd = 'tar xz --strip 1 --no-same-owner -f %s/%s' % (dldir, file)
       else:
            bb.fatal("NPM package %s downloaded not a tarball!" % file)

       # Change to subdir before executing command
       save_cwd = os.getcwd();
       if not os.path.exists(destdir):
           os.makedirs(destdir)
       os.chdir(destdir)
       path = d.getVar('PATH', True)
       if path:
            cmd = "PATH=\"%s\" %s" % (path, cmd)
       bb.note("Unpacking %s to %s/" % (file, os.getcwd()))
       ret = subprocess.call(cmd, preexec_fn=subprocess_setup, shell=True)
       os.chdir(save_cwd)

       if ret != 0:
            raise UnpackError("Unpack command %s failed with return value %s" % (cmd, ret), ud.url)
 
       if 'deps' not in data[pkg]:
            return
       for dep in data[pkg]['deps']:
           self._unpackdep(dep, data[pkg]['deps'], "%s/node_modules/%s" % (destdir, dep), dldir, d)


    def unpack(self, ud, destdir, d):
        dldir = d.getVar("DL_DIR", True)
        pv = d.getVar("PV", True)
        pn = d.getVar("PN", True)
        depdumpfile = "%s-%s.deps.json" % (pn, pv)
        with open("%s/%s" % (dldir, depdumpfile)) as datafile:
            workobj = json.load(datafile)
        dldir = os.path.dirname(ud.localpath)

        self._unpackdep(pn, workobj,  "%s/npmpkg" % destdir, dldir, d)

    def _getdependencies(self, pkg, data, d, ud):
        fetchcmd = "npm view %s dist.tarball" % pkg
        logger.debug(2, "Calling getdeps on %s" % pkg)
        output = runfetchcmd(fetchcmd, d, True)
        data[pkg] = {}
        data[pkg]['tgz'] = os.path.basename(output).rstrip()
        self._runwget(ud, d, "%s %s" % (self.basecmd, output.rstrip()), False)
        #fetchcmd = "npm view %s@%s dependencies --json" % (pkg, version)
        fetchcmd = "npm view %s dependencies --json" % (pkg)
        output = runfetchcmd(fetchcmd, d, True)
        if output == "{}\n" or len(output) ==  1:
            logger.debug(2, "no deps found for %s" % pkg)
            return
        depsfound = json.loads(output)
        data[pkg]['deps'] = {}
        for dep in depsfound:
            self._getdependencies(dep, data[pkg]['deps'], d, ud)

    def download(self, ud, d):
        """Fetch url"""
        jsondepobj = {}
        #fetchcmd = self.basecmd
        # NPM registry uses http
        #fetchcmd += " " + ud.url.replace("npm://", "http://")
        #self._runwget(ud, d, fetchcmd, False)
        pv = d.getVar("PV", True)
        pn = d.getVar("PN", True)

        self._getdependencies(pn, jsondepobj, d, ud)

        depdumpfile = "%s-%s.deps.json" % (pn, pv)
        with open(depdumpfile, 'w') as outfile:
            json.dump(jsondepobj, outfile)
