from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import bitbake, get_bb_vars
import os
import shutil
import glob


class MulticonfigTests(OESelftestTestCase):

    def setUpLocal(self):
        self.bbvars = get_bb_vars(['TOPDIR', 'DEPLOY_DIR', 'MACHINE'])

        self.machines = ['qemux86', 'qemuarm', 'qemumips']
        self.recipes = ['core-image-minimal', 'core-image-sato', \
                'core-image-minimal-dev']
        self.test_recipe = 'core-image-sato'

        self.conf_cmds = ["multiconfig:config%s:%s" % (x, self.recipes[x]) \
                for x in range(3)]

        self.mconf = os.path.join(self.bbvars['TOPDIR'], 'conf', 'multiconfig')
        os.mkdir(self.mconf)
        for n in range(3):
            conf_file = os.path.join(self.mconf, 'config%s.conf' % n)
            with open(conf_file, 'w') as f:
                f.write('MACHINE = "%s"\n' % self.machines[n])
        features = 'BBMULTICONFIG = "%s"' % " ".join(["config%s" % x \
                for x in range(3)])
        self.write_config(features)

    def tearDownLocal(self):
        shutil.rmtree(self.mconf)

    def check_recipe(self, machine, recipe, unique=True):
        built_tar = "%s-%s.tar.bz2" % (recipe, machine)
        recipe_paths = glob.iglob(os.path.join(self.bbvars['DEPLOY_DIR'], \
                    'images', '**', "%s-*.tar.bz2" % recipe))
        recipe_tars = [os.path.basename(x) for x in recipe_paths]
        hyphen_c = recipe.count('-') + machine.count('-') + 1
        recipe_tars = [ x for x in recipe_tars if x.count('.') == 2 \
                    and x.count('-') == hyphen_c]

        self.assertLess(0,len(recipe_tars),"Recipe %s was not built for %s"\
                    % (recipe, machine))
        self.assertEqual(True, built_tar in recipe_tars, "Wrong machine was " \
                    " built, expected %s." % machine)
        if unique:
            self.assertLess(len(recipe_tars), 2, "Recipe %s was built " \
                "for machines other than %s" % (recipe, machine))

    def clean_builds(self):
        bitbake('-c clean %s' % " ".join(self.conf_cmds))
        bitbake('-c clean %s' % " ".join(self.recipes))
        bitbake('-c clean multiconfig:*:%s' % self.test_recipe)

    def test_different_configs(self):
        """
        Summary: Check multiconfig using 2 diferent machines
        Expected: 1. All recipes can be build using the right conf
                  2. Recipes aren't build for more confs than intended
        Product: oe-core
        Author: Humberto Ibarra <humberto.ibarra.lopez@intel.com>
        """
        self.clean_builds()
        bitbake(" ".join(self.conf_cmds))

        # Check that proper builds were done and only for the required recipes
        for x in range(3):
            self.check_recipe(self.machines[x], self.recipes[x])

    def test_general_recipe(self):
        """
        Summary: Check multiconfig and a general recipe at the same time
        Expected: 1. The multiconfig recipe can be build
                  2. The other recipe can be build for the machine in local.conf
        Product: oe-core
        Author: Humberto Ibarra <humberto.ibarra.lopez@intel.com>
        """
        self.clean_builds()
        bitbake('%s %s' % (self.conf_cmds[0], self.test_recipe))

        # Check that recipe[0] was only built for config0
        self.check_recipe(self.machines[0], self.recipes[0])

        # Check that core-image-sato was built for general config
        self.check_recipe(self.bbvars['MACHINE'], self.test_recipe)

    def test_multiconfig_globbing(self):
        """
        Summary: Check multiconfig globbing
        Expected: 1. The globbing feature works for multiconfig
        Product: oe-core
        Author: Humberto Ibarra <humberto.ibarra.lopez@intel.com>
        """
        self.clean_builds()
        bitbake('multiconfig:*:%s' % self.test_recipe)

        # Check that recipe was built for all configs
        for machine in self.machines:
            self.check_recipe(machine, self.test_recipe, False)
