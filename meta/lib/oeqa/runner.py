import os
import logging
import sys
import time
import unittest
import oeqa.utils.ftools as ftools
from oeqa.utils.commands import bitbake, get_bb_var, get_test_layer


class Tc:
    """ Holds information about test cases """

    def __init__(self, tcname, tcclass, tcmodule, tcid=None, tctag=None):
        self.tcname = tcname
        self.tcclass = tcclass
        self.fullpath = '.'.join([tcmodule, tcclass, tcname])
        # Trim prefix from tcmodule
        self.tcmodule = tcmodule.split('.')[-1]
        self.tcid = tcid
        # A test case can have multiple tags (as tuples) otherwise str will suffice
        self.tctag = tctag


class Runner:

    def __init__(self, caller, base_class, test_mod_dir):
        """
        :param caller: eg. selftest, test-recipe (log files will use this name)
        :param base_class: eg. oeSelfTest, RecipeTests
        :param test_mod_dir: eg oeqa.selftest, oeqa.recipetests
        """

        self.caller = caller
        self.base_class = base_class
        self.test_mod_dir = test_mod_dir
        self.log = self.logger_create(self.caller)
        self.builddir = os.environ.get("BUILDDIR")

    @staticmethod
    def logger_create(log_name):
        """ Create logger obj with logging file as <log_name-date.log> and symlink to it as <log_name.log> """

        log_link = '%s.log' % log_name
        log_file = '%s-%s.log' % (log_name, time.strftime("%Y-%m-%d_%H:%M:%S"))

        if os.path.exists(log_link):
            os.remove(log_link)
        os.symlink(log_file, log_link)

        log = logging.getLogger(log_name)
        log.setLevel(logging.DEBUG)

        fh = logging.FileHandler(filename=log_file, mode='w')
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        log.addHandler(fh)
        log.addHandler(ch)

        return log

    def preflight_check(self):
        """ Check that the environment is sourced, meta-selftest included in bblayers and current dir is BUILDDIR """

        self.log.info("Checking that everything is in order before running the tests")

        if not self.builddir:
            self.log.error("BUILDDIR isn't set. Did you forget to source your build environment setup script?")
            return False

        if os.getcwd() != self.builddir:
            self.log.info("Changing cwd to %s" % self.builddir)
            os.chdir(self.builddir)

        if "meta-selftest" not in get_bb_var("BBLAYERS"):
            self.log.error("You don't seem to have the meta-selftest layer in BBLAYERS")
            return False

        self.log.info("Running bitbake -p")
        bitbake("-p")

        return True

    def add_include(self, include_files, include_to):
        """ Include in include_to (local.conf, bblayers.conf) the specified files """

        include_msg_header = "# include added by %s\n" % self.caller
        include_msg = include_msg_header
        if isinstance(include_files, (list, tuple)):
            for f in include_files:
                include_msg += 'include %s\n' % f
        else:
            include_msg += 'include %s\n' % include_files

        if include_msg_header not in ftools.read_file(os.path.join(self.builddir, 'conf', include_to)):
            self.log.info("Adding: %s in %s" % (include_files, include_to))
            ftools.append_file(os.path.join(self.builddir, 'conf', include_to), include_msg)

    def remove_include(self, remove_files, remove_from):
        """ Remove from remove_from (local.conf, bblayers.conf) the specified files """

        if self.builddir is None:
            return

        remove_msg_header = "# include added by %s\n" % self.caller
        remove_msg = remove_msg_header
        if isinstance(remove_files, (list, tuple)):
            for f in remove_files:
                remove_msg += 'include %s\n' % f
        else:
            remove_msg += 'include %s\n' % remove_files

        if remove_msg_header in ftools.read_file(os.path.join(self.builddir, 'conf', remove_from)):
            self.log.info("Removing the include from %s" % remove_from)
            ftools.remove_from_file(os.path.join(self.builddir, 'conf', remove_from), remove_msg)

    def remove_inc_files(self, remove_inc_list):
        """ Remove remove_inc_list from BUILDDIR/conf/ """

        # Also remove the test_recipe.inc if available
        try:
            for root, _, files in os.walk(get_test_layer()):
                pass
            for f in files:
                if f == 'test_recipe.inc':
                    os.remove(os.path.join(root, f))
        except (AttributeError, OSError,) as e:    # AttributeError may happen if BUILDDIR is not set
            pass

        # log.info('Removing: %s' % remove_inc_list)
        for incl_file in remove_inc_list:
            try:
                os.remove(os.path.join(self.builddir, 'conf', incl_file))
            except:
                pass

    # FIXME: this method duplicates some of the code. Keep it here for now
    def get_tests(self, exclusive_modules=[], include_hidden=False):
        testslist = []
        prefix = self.test_mod_dir.__name__
        for x in exclusive_modules:
            testslist.append('.'.join([prefix, x]))
        if not testslist:
            for testpath in self.test_mod_dir.__path__:
                files = sorted([f for f in os.listdir(testpath) if f.endswith('.py') and not (f.startswith('_') and not
                                include_hidden) and not f.startswith('__') and f != 'base.py'])
                for f in files:
                    module = '.'.join([prefix, os.path.splitext(f)[0]])
                    if module not in testslist:
                        testslist.append(module)

        return testslist

    def get_tests_from_module(self, tmod):
        """ Get a list of Tcs from module extending the base_class """

        tlist = []

        try:
            import importlib
            modlib = importlib.import_module(tmod)
            for mod in vars(modlib).values():
                if isinstance(mod, type(self.base_class)) and issubclass(mod, self.base_class) and mod is not self.base_class:
                    for test in dir(mod):
                        if test.startswith('test_') and hasattr(vars(mod)[test], '__call__'):
                            # Get test case id and feature tag
                            # NOTE: if testcase decorator or feature tag are not set it will throw an error
                            try:
                                tid = vars(mod)[test].test_case
                            except:
                                print 'DEBUG: tc id missing for ' + str(test)
                                tid = None
                            try:
                                ttag = vars(mod)[test].tag__feature
                            except:
                                # print 'DEBUG: feature tag missing for ' + str(test)
                                ttag = None

                            tlist.append(Tc(test, mod.__name__, mod.__module__, tid, ttag))
        except:
            pass

        return tlist

    def get_all_tests(self):
        """ Get all test from test_mod_dir (eg. oeqa.selftest) that extends base_class (eg. oeSelfTest)"""

        tmodules = set()
        testlist = []
        prefix = self.test_mod_dir.__name__

        # Get all the test modules (except the hidden ones)
        for tpath in self.test_mod_dir.__path__:
            files = sorted([f for f in os.listdir(tpath) if f.endswith('.py') and not
                            f.startswith(('_', '__')) and f != 'base.py'])
            for f in files:
                tmodules.add('.'.join([prefix, os.path.splitext(f)[0]]))

        # Get all the tests from modules
        tmodules = sorted(list(tmodules))

        for tmod in tmodules:
            testlist += self.get_tests_from_module(tmod)

        return testlist

    def list_tests(self):
        """ List all available tests """

        ts = self.get_all_tests()

        print '%-4s\t%-20s\t%-60s\t%-25s\t%-20s' % ('id', 'tag', 'name', 'class', 'module')
        print '_' * 150
        for t in ts:
            if isinstance(t.tctag, (tuple, list)):
                print '%-4s\t%-20s\t%-60s\t%-25s\t%-20s' % (t.tcid, ', '.join(t.tctag), t.tcname, t.tcclass, t.tcmodule)
            else:
                print '%-4s\t%-20s\t%-60s\t%-25s\t%-20s' % (t.tcid, t.tctag, t.tcname, t.tcclass, t.tcmodule)
        print '_' * 150
        print 'Total found:\t %s' % len(ts)

    def list_tags(self):
        """
        Get all tags set to test cases
        Note: This is useful when setting tags to test cases
        Note: The list of tags should be kept as minimal as possible
        """

        tags = set()
        all_tests = self.get_all_tests()

        for tc in all_tests:
            if isinstance(tc.tctag, (tuple, list)):
                tags.update(set(tc.tctag))
            else:
                tags.add(tc.tctag)

        print 'Tags:\t%s' % ', '.join(str(x) for x in tags)

    def get_testsuite_by(self, criteria, keyword):
        """
        Get a testsuite based on 'keyword'
        :param criteria: name, class, module, id, tag
        :param keyword: a list of tests, classes, modules, ids, tags
        """
        ts = set()
        all_tests = self.get_all_tests()

        if criteria == 'name':
            for tc in all_tests:
                if tc.tcname in keyword:
                    ts.add((tc.tcid, tc.tctag, tc.tcname, tc.tcclass, tc.tcmodule))

        elif criteria == 'class':
            for tc in all_tests:
                if tc.tcclass in keyword:
                    ts.add((tc.tcid, tc.tctag, tc.tcname, tc.tcclass, tc.tcmodule))

        elif criteria == 'module':
            for tc in all_tests:
                if tc.tcmodule in keyword:
                    ts.add((tc.tcid, tc.tctag, tc.tcname, tc.tcclass, tc.tcmodule))
        elif criteria == 'id':
            for tc in all_tests:
                if str(tc.tcid) in keyword:
                    ts.add((tc.tcid, tc.tctag, tc.tcname, tc.tcclass, tc.tcmodule))
        elif criteria == 'tag':
            for tc in all_tests:
                # tc can have multiple tags (as list or tuple) otherwise as str
                if isinstance(tc.tctag, (list, tuple)):
                    for tag in tc.tctag:
                        if str(tag) in keyword:
                            ts.add((tc.tcid, tc.tctag, tc.tcname, tc.tcclass, tc.tcmodule))
                elif str(tc.tctag) in keyword:
                    ts.add((tc.tcid, tc.tctag, tc.tcname, tc.tcclass, tc.tcmodule))

        return sorted(list(ts))

    # NOTE: I would probably merge create_testsuite_by and get_testsuite_by into one method
    def create_testsuite_by(self, criteria, keyword):
        """
        Create a testsuite based on 'keyword'
        :param criteria: name, class, module, id, tag
        :param keyword: a list of tests, classes, modules, ids, tags
        """

        ts = set()
        all_tests = self.get_all_tests()

        if criteria == 'name':
            for tc in all_tests:
                if tc.tcname in keyword:
                    ts.add(tc.fullpath)

        elif criteria == 'class':
            for tc in all_tests:
                if tc.tcclass in keyword:
                    ts.add(tc.fullpath)

        elif criteria == 'module':
            for tc in all_tests:
                if tc.tcmodule in keyword:
                    ts.add(tc.fullpath)
        elif criteria == 'id':
            for tc in all_tests:
                if str(tc.tcid) in keyword:
                    ts.add(tc.fullpath)
        elif criteria == 'tag':
            for tc in all_tests:
                # tc can have multiple tags (as list or tuple) otherwise as str
                if isinstance(tc.tctag, (list, tuple)):
                    for tag in tc.tctag:
                        if str(tag) in keyword:
                            ts.add(tc.fullpath)
                elif tc.tctag in keyword:
                    ts.add(tc.fullpath)

        return sorted(list(ts))

    def list_testsuite_by(self, criteria, keyword):
        """
        List a testsuite based on 'keyword'
        :param criteria: name, class, module, id, tag
        :param keyword: a list of tests, classes, modules, ids, tags
        """

        ts = self.get_testsuite_by(criteria, keyword)

        print '%-4s\t%-20s\t%-60s\t%-25s\t%-20s' % ('id', 'tag', 'name', 'class', 'module')
        print '_' * 150
        for t in ts:
            if isinstance(t[1], (tuple, list)):
                print '%-4s\t%-20s\t%-60s\t%-25s\t%-20s' % (t[0], ', '.join(t[1]), t[2], t[3], t[4])
            else:
                print '%-4s\t%-20s\t%-60s\t%-25s\t%-20s' % t
        print '_' * 150
        print 'Filtering by:\t %s' % criteria
        print 'Looking for:\t %s' % ', '.join(str(x) for x in keyword)
        print 'Total found:\t %s' % len(ts)

    @staticmethod
    def coverage_setup(run_tests, run_all_tests):
        """ Set up the coverage measurement for the testcases to be run """
        builddir = os.environ.get("BUILDDIR")
        coveragerc = "%s/.coveragerc" % builddir
        data_file = "%s/.coverage." % builddir
        data_file += ((run_tests and '.'.join(run_tests)) or (run_all_tests and "all_tests") or "")
        if os.path.isfile(data_file):
            os.remove(data_file)
        with open(coveragerc, 'w') as cps:
            cps.write("[run]\n")
            cps.write("data_file = %s\n" % data_file)
            cps.write("branch = True\n")
            # Measure just BBLAYERS, scripts and bitbake folders
            cps.write("source = \n")
            for layer in get_bb_var('BBLAYERS').split():
                cps.write("    %s\n" % layer)
            corebase = get_bb_var('COREBASE')
            cps.write("    %s\n" % os.path.join(corebase, 'scripts'))
            cps.write("    %s\n" % os.path.join(corebase, 'bitbake'))

            return coveragerc

    @staticmethod
    def coverage_report():
        """ Loads the coverage data gathered and reports it back """
        try:
            # Coverage4 uses coverage.Coverage
            from coverage import Coverage
        except:
            # Coverage under version 4 uses coverage.coverage
            from coverage import coverage as Coverage

        import cStringIO as StringIO
        from coverage.misc import CoverageException

        cov_output = StringIO.StringIO()
        # Creating the coverage data with the setting from the configuration file
        cov = Coverage(config_file=os.environ.get('COVERAGE_PROCESS_START'))
        try:
            # Load data from the data file specified in the configuration
            cov.load()
            # Store report data in a StringIO variable
            cov.report(file = cov_output, show_missing=False)
            print "\n%s" % cov_output.getvalue()
        except CoverageException as e:
            # Show problems with the reporting. Since Coverage4 not finding  any data to report raises an exception
            print "%s" % str(e)
        finally:
            cov_output.close()

    @classmethod
    def buildResultClass(cls, args):
        """Build a Result Class to use in the testcase execution"""

        class StampedResult(unittest.TextTestResult):
            """
            Custom TestResult that prints the time when a test starts.  As oe-selftest
            can take a long time (ie a few hours) to run, timestamps help us understand
            what tests are taking a long time to execute.
            If coverage is required, this class executes the coverage setup and reporting.
            """
            def startTest(self, test):
                import time
                self.stream.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " - ")
                super(StampedResult, self).startTest(test)

            def startTestRun(self):
                """ Setup coverage before running any testcase """
                if args.coverage:
                    try:
                        # check if user can do coverage
                        import coverage
                        print "Coverage is enabled"

                        # In case the user has not set the variable COVERAGE_PROCESS_START,
                        # create a default one and export it. The COVERAGE_PROCESS_START
                        # value indicates where the coverage configuration file resides
                        # More info on https://pypi.python.org/pypi/coverage
                        if not os.environ.get('COVERAGE_PROCESS_START'):
                            os.environ['COVERAGE_PROCESS_START'] = cls.coverage_setup(args.run_tests, args.run_all_tests)

                        self.coverage_installed = True
                    except:
                        print '\n'.join(["python coverage is not installed",
                                         "Make sure your coverage takes into account sub-process",
                                         "More info on https://pypi.python.org/pypi/coverage"])
                        self.coverage_installed = False

            def stopTestRun(self):
                """ Report coverage data after the testcases are run """

                if args.coverage and self.coverage_installed:
                    with open(os.environ['COVERAGE_PROCESS_START']) as ccf:
                        print "Coverage configuration file (%s)" % os.environ.get('COVERAGE_PROCESS_START')
                        print "==========================="
                        print "\n%s" % "".join(ccf.readlines())

                    print "Coverage Report"
                    print "==============="

                    cls.coverage_report()

        return StampedResult
