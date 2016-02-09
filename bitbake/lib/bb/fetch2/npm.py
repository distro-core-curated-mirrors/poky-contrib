# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
"""
BitBake 'Fetch' NPM implementation

The NPM fetcher is used to retrieve files from the npmjs repository

Usage in the recipe:

    SRC_URI = "npm://www.npmjs.com/package/colors"
    Suported SRC_URI options are:

    - name
    - version

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

    def clean(self, ud, d):
         bb.utils.remove(ud.bbnpmmanifest, True)
         # todo remove npm/${PN} dir

    def urldata_init(self, ud, d):
        """
        init NPM specific variable within url data
        """
        if 'downloadfilename' in ud.parm:
            ud.basename = ud.parm['downloadfilename']
        else:
            ud.basename = os.path.basename(ud.path)

        # can't call it ud.name otherwise fetcher base class will start doing md5stuff
        # TODO: find a way to get an md5/sha256 manifest of pkg & all deps
        ud.pkgname = ud.parm.get("name", None)
        if not ud.pkgname:
            raise ParameterError("NPM fetcher requires a name parameter")
        ud.version = ud.parm.get("version", None)
        if not ud.version:
            raise ParameterError("NPM fetcher requires a version parameter")
        ud.bbnpmmanifest = "%s-%s.deps.json" % (ud.pkgname, ud.version)
        ud.registry = "http://%s" % ud.basename

        self.basecmd = d.getVar("FETCHCMD_wget", True) or "/usr/bin/env wget -t 2 -T 30 -nv --passive-ftp --no-check-certificate"

    def need_update(self, ud, d):
        if os.path.exists(ud.bbnpmmanifest):
            return False
        return True

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
        depdumpfile = "%s-%s.deps.json" % (ud.pkgname, ud.version)
        with open("%s/%s" % (dldir, depdumpfile)) as datafile:
            workobj = json.load(datafile)
        dldir = os.path.dirname(ud.localpath)

        self._unpackdep(ud.pkgname, workobj,  "%s/npmpkg" % destdir, dldir, d)

    def _getdependencies(self, pkg, data, version, d, ud):
        pkgfullname = pkg
        if version:
            pkgfullname += "@%s" % version
        logger.debug(2, "Calling getdeps on %s" % pkg)
        fetchcmd = "npm view %s dist.tarball --registry %s" % (pkgfullname, ud.registry)
        output = runfetchcmd(fetchcmd, d, True)
        # npm may resolve multiple versions
        outputarray = output.splitlines()
        # we just take the latest version npm resolved
        #logger.debug(2, "Output URL is %s - %s - %s" % (ud.basepath, ud.basename, ud.localfile))
        outputurl = outputarray[len(outputarray)-1].rstrip()
        if (len(outputarray) > 1):
            # remove the preceding version/name from npm output and then the
            # first and last quotes
            outputurl = outputurl.split(" ")[1][1:-1]
        data[pkg] = {}
        data[pkg]['tgz'] = os.path.basename(outputurl)
        self._runwget(ud, d, "%s %s" % (self.basecmd, outputurl), False)
        #fetchcmd = "npm view %s@%s dependencies --json" % (pkg, version)
        fetchcmd = "npm view %s dependencies --json --registry %s" % (pkgfullname, ud.registry)
        output = runfetchcmd(fetchcmd, d, True)
        try:
          depsfound = json.loads(output)
        except:
            # just assume there is no deps to be loaded here
            return
        data[pkg]['deps'] = {}
        for dep, version in depsfound.iteritems():
            self._getdependencies(dep, data[pkg]['deps'], version, d, ud)

    def _getshrinkeddependencies(self, pkg, data, version, d, ud, manifest):
        logger.debug(2, "NPM shrinkwrap file is %s" % data)
        outputurl = "invalid"
        if ('resolved' not in data):
            # will be the case for ${PN}
            fetchcmd = "npm view %s@%s dist.tarball --registry %s" % (pkg, ud.version, ud.registry)
            outputurl = runfetchcmd(fetchcmd, d, True)
        else:
            outputurl = data['resolved']
        self._runwget(ud, d, "%s %s" % (self.basecmd, outputurl), False)
        manifest[pkg] = {}
        manifest[pkg]['tgz'] = os.path.basename(outputurl).rstrip()
        manifest[pkg]['deps'] = {}
        if 'dependencies' in data:
            for obj in data['dependencies']:
                logger.debug(2, "Found dep is %s" % str(obj))
                self._getshrinkeddependencies(obj, data['dependencies'][obj], data['dependencies'][obj]['version'], d, ud, manifest[pkg]['deps'])

    def download(self, ud, d):
        """Fetch url"""
        jsondepobj = {}
        shrinkobj = {}

        shwrf = d.getVar('NPM_SHRINKWRAP', True)
        logger.debug(2, "NPM shrinkwrap file is %s" % shwrf)
        with open("%s" % (shwrf)) as datafile:
            shrinkobj = json.load(datafile)

        if ('name' not in shrinkobj):
            self._getdependencies(ud.pkgname, jsondepobj, ud.version, d, ud)
        else:
            self._getshrinkeddependencies(ud.pkgname, shrinkobj, ud.version, d, ud, jsondepobj)

        with open(ud.bbnpmmanifest, 'w') as outfile:
            json.dump(jsondepobj, outfile)
