import unittest
import tempfile
import shutil
import os
import glob
import logging
import subprocess
import oeqa.utils.ftools as ftools
from oeqa.utils.decorators import testcase
from oeqa.selftest.base import oeSelfTest
from oeqa.utils.commands import runCmd, bitbake, get_bb_var
from oeqa.utils.httpserver import HTTPService

class oeKernelDevelopment(oeSelfTest):
    """
    # Test Plan: 94
    # This code is planned to be part of the automation for Linux Kernel Development
    # Contains: 
    """
    def setUp(self):
        """ Test case setup function """
        super(oeKernelDevelopment, self).setUp()
        self.workspacedir = os.path.join(self.builddir, 'workspace')
    
    @testcase (1527)
    def test_creating_and_preparing_a_layer(self):
        # Create a temp directory to store the new layer
        tmpdir = tempfile.mkdtemp(prefix='meta-kerneldev')
        try:
            # Create workspace layer with suctum path
            result = runCmd('devtool create-workspace %s' % tmpdir)
            self.assertTrue(os.path.isfile(os.path.join(tmpdir, 'conf','layer.conf')), msg = "No workspace created. devtool output: %s " % result.output)
            result = runCmd('bitbake-layers show-layers')
            self.assertIn(tmpdir, result.output)
            
            # Create the layer configuration file
            layer_config="""
# We have a conf and classes directory, add to BBPATH
BBPATH .= ":${LAYERDIR}"
# We have recipes-* directories, add to BBFILES
BBFILES += "${LAYERDIR}/recipes/*/*.bb \
            ${LAYERDIR}/recipes/*.bbappend"
BBFILE_COLLECTIONS += "mylayer"
BBFILE_PATTERN_mylayer = "^${LAYERDIR}/"
BBFILE_PRIORITY_mylayer = "5"
            """ 
            with open(os.path.join(tmpdir, 'conf', 'layer.conf'), 'a+') as f:
                f. write(layer_config)

            # try creating a workspace layer with the default path
            self.track_for_cleanup(self.workspacedir)
            self.add_command_to_tearDown('bitbake-layers remove-layer */workspace')
            result = runCmd('devtool create-workspace')
            self.assertTrue(os.path.isfile(os.path.join(self.workspacedir, 'conf', 'layer.conf')), msg = "No workspace created. devtool output: %s " %result.output)
            result = runCmd('bitbake-layers show-layers')
            self.assertNotIn(tmpdir, result.output)
            self.assertIn(self.workspacedir, result.output)
        finally:
            shutil.rmtree(tmpdir)




if __name__ == '__main__':
    unittest.main()
