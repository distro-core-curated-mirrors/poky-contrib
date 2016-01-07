from oeqa.recipetests.base import RecipeTests
from oeqa.selftest.base import get_available_machines
from oeqa.utils.commands import bitbake, get_tasks_for_recipe
import logging


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
