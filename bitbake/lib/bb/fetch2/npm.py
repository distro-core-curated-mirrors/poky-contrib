# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
"""
BitBake 'Fetch' NPM implementation

The NPM fetcher is used to retrieve files from the npmjs repository

Usage in the recipe:

    SRC_URI = "npm://www.npmjs.com/package/colors"
    SRCREV = "0.0.0"

"""

import os
import sys
import urllib
import json
import bb
from   bb import data
from   bb.fetch2 import FetchMethod
from   bb.fetch2 import FetchError
from   bb.fetch2 import runfetchcmd
from   bb.fetch2 import logger
from   distutils import spawn

class Npm(FetchMethod):
    jsondeps = dict()

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
        return True

    def sortable_revision(self, ud, d, name):
        return False, ud.identifier

    def _runwget(self, ud, d, command, quiet):
        logger.debug(2, "Fetching %s using command '%s'" % (ud.url, command))
        bb.fetch2.check_network_access(d, command)
        runfetchcmd(command, d, quiet)

    def ___unpack_crap_unused(self, ud, destdir, d):
        file = urldata.localpath
        if file.endswith('.tgz') or file.endswith('.tar.gz') or file.endswith('.tar.Z'):
            cmd = 'tar xz --no-same-owner -f %s' % file
        else:
            bb.fatal("NPM package %s downloaded not a tarball!" % file)

        # Change to subdir before executing command
        save_cwd = os.getcwd();
        os.chdir(rootdir)
        if 'subdir' in urldata.parm:
            newdir = ("%s/%s" % (rootdir, urldata.parm.get('subdir')))
            bb.utils.mkdirhier(newdir)
            os.chdir(newdir)

        path = data.getVar('PATH', True)
        if path:
            cmd = "PATH=\"%s\" %s" % (path, cmd)
        bb.note("Unpacking %s to %s/" % (file, os.getcwd()))
        ret = subprocess.call(cmd, preexec_fn=subprocess_setup, shell=True)

        os.chdir(save_cwd)

        if ret != 0:
            raise UnpackError("Unpack command %s failed with return value %s" % (cmd, ret), urldata.url)

    def download(self, ud, d):
        """Fetch url"""
        fetchcmd = self.basecmd
        # NPM registry uses http
        fetchcmd += " " + ud.url.replace("npm://", "http://")
        self._runwget(ud, d, fetchcmd, False)
        pv = d.getVar("PV", True)
        pn = d.getVar("PN", True)
        # force non lazy json output with --json
        fetchcmd = "npm view %s@%s dependencies --json" % (pn, pv)
        logger.debug(2, "fetchcmd is %s" % (fetchcmd))
        output = runfetchcmd(fetchcmd, d, True)
        logger.debug(2, "output is %s" % (output))
		# if a node package has a deps field which is empty in package.json npm
        # will return {}
        logger.debug(2, "output length is %d" % len(output))
        if output == "{}\n" or len(output) ==  1:
            logger.debug(2, "no deps found for %s" % pn)
        else:
            self.jsondeps = json.loads(output)
            for dep in self.jsondeps.keys():
                fetchcmd = "npm view %s dist.tarball" % dep
                output = runfetchcmd(fetchcmd, d, True)
                ud.parm['subdir'] = "npmpkg/deps"
                self._runwget(ud, d, self.basecmd + " " + output, False)
