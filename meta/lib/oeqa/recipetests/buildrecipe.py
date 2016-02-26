from oeqa.recipetests.base import RecipeTests
from oeqa.selftest.base import get_available_machines
from oeqa.utils.commands import bitbake, get_tasks_for_recipe, get_bb_var, ftools, get_all_bbappends
import logging
import os
import random


class BuildRecipeTests(RecipeTests):

    log = logging.getLogger('test-recipe.build-recipe')

    def test_build_recipe_for_all_major_architectures(self):
        """ Build the recipe with all major architectures(qemux86, qemux86-64, qemuarm, qemuppc, qemumips) """

        machines = get_available_machines()
        qemu_machines = [m for m in machines if 'qemu' in m]

        # Build the recipe for all major architectures
        for m in qemu_machines:
            self.log.info('Building recipe "%s" for architecture "%s"' % (self.testrecipe, m))
            self.write_config('MACHINE = "%s"' % m)
            bitbake(self.testrecipe)

    def test_rebuild_recipe_from_sstate_1(self):
        """ Rebuild the recipe from sstate with sstate file for the recipe """
        bitbake(self.testrecipe)
        bitbake('-c clean %s' % self.testrecipe)
        bitbake(self.testrecipe)

    def test_rebuild_recipe_from_sstate_2(self):
        """ Rebuild the recipe from sstate without sstate file for the recipe """
        bitbake(self.testrecipe)
        bitbake('-c cleansstate %s' % self.testrecipe)
        bitbake(self.testrecipe)

    def test_cleaning_operations_on_recipe(self):
        """ Perform cleaning operations on the recipe(cleansstate, clean, cleanall) """

        clean_tasks = ['cleansstate', 'clean', 'cleanall']

        for task in clean_tasks:
            bitbake(self.testrecipe)
            self.log.info('Performing %s for recipe %s' % (task, self.testrecipe))
            bitbake('-c %s %s' % (task, self.testrecipe))

    def test_force_major_tasks_on_recipe(self):
        """ Force all major tasks on the recipe (bitbake -C <task> <recipe>) """
        major_tasks = ['unpack', 'patch', 'configure', 'compile', 'install', 'populate_sysroot', 'package',
                       'package_write_rpm', 'package_write_deb', 'package_write_ipk']

        feature = 'PACKAGE_CLASSES = "package_rpm package_deb package_ipk"\n'
        self.write_config(feature)

        available_tasks = get_tasks_for_recipe(self.testrecipe)

        for task in major_tasks:
            # Check if task is available for recipe
            if task not in available_tasks:
                self.log.warning('Task %s not available for recipe %s' % (task, self.testrecipe))
                continue
            # Force task on recipe
            self.log.info('Forcing task %s' % task)
            bitbake('-C %s %s' % (task, self.testrecipe))

    def test_combinations_of_bbappend(self):
        """ Selectively use each combination of .bbappend files with the recipe """

        test_recipe_pv = get_bb_var('PV', self.testrecipe)
        recipe_append_file = self.testrecipe + '_' + test_recipe_pv + '.bbappend'

        bbappend_msgs = {1: 'msg 1', 2: 'msg 2', 3: 'msg 3', 4: 'msg 4'}
        bbappend_files = {}

        # Install all bbappends for recipe
        for i in bbappend_msgs:
            recipe_append_dir = self.testrecipe + '_test_' + str(i)
            recipe_append_path = os.path.join(self.testlayer_path, 'recipes-test', recipe_append_dir, recipe_append_file)
            os.mkdir(os.path.join(self.testlayer_path, 'recipes-test', recipe_append_dir))
            feature = 'SUMMARY += "%s"\n' % bbappend_msgs[i]
            ftools.write_file(recipe_append_path, feature)
            bbappend_files[i] = recipe_append_path

        self.add_command_to_tearDown('rm -rf %s' % os.path.join(self.testlayer_path, 'recipes-test',
                                                                self.testrecipe + '_test_*'))

        test_recipe_bb = '%s_%s.bb' % (self.testrecipe, test_recipe_pv)
        all_bbappends = get_all_bbappends()
        self.log.info('All bbappends for recipe %s: %s' % (self.testrecipe, all_bbappends.get(test_recipe_bb)))

        # Build recipe with all bbappends
        bitbake(self.testrecipe)

        # Mask two random bbappends (some times it might be the same one, which is ok)
        for i in range(len(bbappend_files)):
            choice1 = random.choice(bbappend_msgs.keys())
            choice2 = random.choice(bbappend_msgs.keys())
            mask1 = bbappend_files.get(choice1)
            mask2 = bbappend_files.get(choice2)

            feature = 'BBMASK = "%s"\n' % mask1
            feature += 'BBMASK += "%s"\n' % mask2
            self.write_config(feature)
            self.log.info('Applied MASKs [%s, %s]' % (mask1, mask2))

            # Make sure the masked bbappends don't show up
            current_bbappends = get_all_bbappends()
            self.log.info('Current bbappends for recipe %s: %s' % (self.testrecipe, current_bbappends.get(test_recipe_bb)))
            self.assertNotIn(mask1, current_bbappends.get(test_recipe_bb))
            self.assertNotIn(mask2, current_bbappends.get(test_recipe_bb))

            # Make sure the summary was updated
            current_summary = get_bb_var('SUMMARY', self.testrecipe)
            self.log.info('Current summary: "%s"' % current_summary)
            self.assertNotIn(bbappend_msgs.get(choice1), current_summary)
            self.assertNotIn(bbappend_msgs.get(choice2), current_summary)

            # Build recipe with custom bbappends
            bitbake(self.testrecipe)
