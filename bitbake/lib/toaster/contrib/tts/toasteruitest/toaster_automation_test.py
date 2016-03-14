#!/usr/bin/python
# Copyright

# DESCRIPTION
# This is toaster automation base class and test cases file

# History:
# 2015.03.09  inital version
# 2015.03.23  adding toaster_test.cfg, run_toastertest.py so we can run case by case from outside

# Briefs:
# This file is comprised of 3 parts:
# I:   common utils like sorting, getting attribute.. etc
# II:  base class part, which complies with unittest frame work and
#      contains class selenium-based functions
# III: test cases
#      to add new case: just implement new test_xxx() function in class toaster_cases

# NOTES for cases:
# case 946:
# step 6 - 8 needs to be observed using screenshots
# case 956:
# step 2 - 3 needs to be run manually

import unittest, time, re, sys, getopt, os, logging, string, errno, exceptions
import shutil, argparse, ConfigParser, platform, json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import sqlite3 as sqlite


###########################################
#                                         #
# PART I: utils stuff                     #
#                                         #
###########################################

class Listattr(object):
    """
    Set of list attribute. This is used to determine what the list content is.
    Later on we may add more attributes here.
    """
    NULL = "null"
    NUMBERS = "numbers"
    STRINGS = "strings"
    PERCENT = "percentage"
    SIZE = "size"
    UNKNOWN = "unknown"


def get_log_root_dir():
    max_depth = 5
    parent_dir = '../'
    for number in range(0, max_depth):
        if os.path.isdir(sys.path[0] + os.sep + (os.pardir + os.sep)*number + 'log'):
            log_root_dir = os.path.abspath(sys.path[0] + os.sep + (os.pardir + os.sep)*number + 'log')
            break

    if number == (max_depth - 1):
        print 'No log dir found. Please check'
        raise Exception

    return log_root_dir


def mkdir_p(dir):
    try:
        os.makedirs(dir)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dir):
            pass
        else:
            raise


def get_list_attr(testlist):
    """
    To determine the list content
    """
    if not testlist:
        return Listattr.NULL
    listtest = testlist[:]
    try:
        listtest.remove('')
    except ValueError:
        pass
    pattern_percent = re.compile(r"^([0-9])+(\.)?([0-9])*%$")
    pattern_size = re.compile(r"^([0-9])+(\.)?([0-9])*( )*(K)*(M)*(G)*B$")
    pattern_number = re.compile(r"^([0-9])+(\.)?([0-9])*$")
    def get_patterned_number(pattern, tlist):
        count = 0
        for item in tlist:
            if re.search(pattern, item):
                count += 1
        return count
    if get_patterned_number(pattern_percent, listtest) == len(listtest):
        return Listattr.PERCENT
    elif get_patterned_number(pattern_size, listtest) == len(listtest):
        return Listattr.SIZE
    elif get_patterned_number(pattern_number, listtest) == len(listtest):
        return Listattr.NUMBERS
    else:
        return Listattr.STRINGS


def is_list_sequenced(testlist):
    """
    Function to tell if list is sequenced
    Currently we may have list made up of: Strings ; numbers ; percentage ; time; size
    Each has respective way to determine if it's sequenced.
    """
    test_list = testlist[:]
    try:
        test_list.remove('')
    except ValueError:
        pass

    if get_list_attr(testlist) == Listattr.NULL :
        return True

    elif get_list_attr(testlist) == Listattr.STRINGS :
        return (sorted(test_list) == test_list)

    elif get_list_attr(testlist) == Listattr.NUMBERS :
        list_number = []
        for item in test_list:
            list_number.append(eval(item))
        return (sorted(list_number) == list_number)

    elif get_list_attr(testlist) == Listattr.PERCENT :
        list_number = []
        for item in test_list:
            list_number.append(eval(item.strip('%')))
        return (sorted(list_number) == list_number)

    elif get_list_attr(testlist) == Listattr.SIZE :
        list_number = []
        # currently SIZE is splitted by space
        for item in test_list:
            if item.split()[1].upper() == "KB":
                list_number.append(1024 * eval(item.split()[0]))
            elif item.split()[1].upper() == "MB":
                list_number.append(1024 * 1024 * eval(item.split()[0]))
            elif item.split()[1].upper() == "GB":
                list_number.append(1024 * 1024 * 1024 * eval(item.split()[0]))
            else:
                list_number.append(eval(item.split()[0]))
        return (sorted(list_number) == list_number)

    else:
        print 'Unrecognized list type, please check'
        return False


def is_list_inverted(testlist):
    """
    Function to tell if list is inverted
    Currently we may have list made up of: Strings ; numbers ; percentage ; time; size
    Each has respective way to determine if it's inverted.
    """
    test_list = testlist[:]
    try:
        test_list.remove('')
    except ValueError:
        pass

    if get_list_attr(testlist) == Listattr.NULL :
        return True

    elif get_list_attr(testlist) == Listattr.STRINGS :
        return (sorted(test_list, reverse = True) == test_list)

    elif get_list_attr(testlist) == Listattr.NUMBERS :
        list_number = []
        for item in test_list:
            list_number.append(eval(item))
        return (sorted(list_number, reverse = True) == list_number)

    elif get_list_attr(testlist) == Listattr.PERCENT :
        list_number = []
        for item in test_list:
            list_number.append(eval(item.strip('%')))
        return (sorted(list_number, reverse = True) == list_number)

    elif get_list_attr(testlist) == Listattr.SIZE :
        list_number = []
        # currently SIZE is splitted by space. such as 0 B; 1 KB; 2 MB
        for item in test_list:
            if item.split()[1].upper() == "KB":
                list_number.append(1024 * eval(item.split()[0]))
            elif item.split()[1].upper() == "MB":
                list_number.append(1024 * 1024 * eval(item.split()[0]))
            elif item.split()[1].upper() == "GB":
                list_number.append(1024 * 1024 * 1024 * eval(item.split()[0]))
            else:
                list_number.append(eval(item.split()[0]))
        return (sorted(list_number, reverse = True) == list_number)

    else:
        print 'Unrecognized list type, please check'
        return False

def replace_file_content(filename, item, option):
    f = open(filename)
    lines = f.readlines()
    f.close()
    output = open(filename, 'w')
    for line in lines:
        if line.startswith(item):
            output.write(item + " = '" + option + "'\n")
        else:
            output.write(line)
    output.close()

def extract_number_from_string(s):
    """
    extract the numbers in a string. return type is 'list'
    """
    return re.findall(r'([0-9]+)', s)

# Below is decorator derived from toaster backend test code
class NoParsingFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == 100

def LogResults(original_class):
    orig_method = original_class.run

    from time import strftime, gmtime
    caller = 'toaster'
    timestamp = strftime('%Y%m%d%H%M%S',gmtime())
    logfile = os.path.join(os.getcwd(),'results-'+caller+'.'+timestamp+'.log')
    linkfile = os.path.join(os.getcwd(),'results-'+caller+'.log')

    #rewrite the run method of unittest.TestCase to add testcase logging
    def run(self, result, *args, **kws):
        orig_method(self, result, *args, **kws)
        passed = True
        testMethod = getattr(self, self._testMethodName)
        #if test case is decorated then use it's number, else use it's name
        try:
            test_case = testMethod.test_case
        except AttributeError:
            test_case = self._testMethodName

        class_name = str(testMethod.im_class).split("'")[1]

        #create custom logging level for filtering.
        custom_log_level = 100
        logging.addLevelName(custom_log_level, 'RESULTS')

        def results(self, message, *args, **kws):
            if self.isEnabledFor(custom_log_level):
                self.log(custom_log_level, message, *args, **kws)
        logging.Logger.results = results

        logging.basicConfig(filename=logfile,
                            filemode='w',
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            datefmt='%H:%M:%S',
                            level=custom_log_level)
        for handler in logging.root.handlers:
            handler.addFilter(NoParsingFilter())
        local_log = logging.getLogger(caller)

        #check status of tests and record it

        for (name, msg) in result.errors:
            if (self._testMethodName == str(name).split(' ')[0]) and (class_name in str(name).split(' ')[1]):
                local_log.results("Testcase "+str(test_case)+": ERROR")
                local_log.results("Testcase "+str(test_case)+":\n"+msg)
                passed = False
        for (name, msg) in result.failures:
            if (self._testMethodName == str(name).split(' ')[0]) and (class_name in str(name).split(' ')[1]):
                local_log.results("Testcase "+str(test_case)+": FAILED")
                local_log.results("Testcase "+str(test_case)+":\n"+msg)
                passed = False
        for (name, msg) in result.skipped:
            if (self._testMethodName == str(name).split(' ')[0]) and (class_name in str(name).split(' ')[1]):
                local_log.results("Testcase "+str(test_case)+": SKIPPED")
                passed = False
        if passed:
            local_log.results("Testcase "+str(test_case)+": PASSED")

        # Create symlink to the current log
        if os.path.exists(linkfile):
            os.remove(linkfile)
        os.symlink(logfile, linkfile)

    original_class.run = run

    return original_class


###########################################
#                                         #
# PART II: base class                     #
#                                         #
###########################################

@LogResults
class toaster_cases_base(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.log = cls.logger_create()

    def setUp(self):
        self.screenshot_sequence = 1
        self.verificationErrors = []
        self.accept_next_alert = True
        self.host_os = platform.system().lower()
        if os.getenv('TOASTER_SUITE'):
            self.target_suite = os.getenv('TOASTER_SUITE')
        else:
            self.target_suite = self.host_os

        self.parser = ConfigParser.SafeConfigParser()
        self.parser.read('toaster_test.cfg')
        self.base_url = eval(self.parser.get('toaster_test_' + self.target_suite, 'toaster_url'))

        # create log dir . Currently , we put log files in log/tmp. After all
        # test cases are done, move them to log/$datetime dir
        self.log_tmp_dir = os.path.abspath(sys.path[0]) + os.sep + 'log' + os.sep + 'tmp'
        try:
            mkdir_p(self.log_tmp_dir)
        except OSError :
            logging.error("%(asctime)s Cannot create tmp dir under log, please check your privilege")
        # self.log = self.logger_create()
        # driver setup
        self.setup_browser()
        self.driver.implicitly_wait(10)
        self.driver.get(self.base_url)
        self.driver.find_element_by_css_selector("a[href='/toastergui/projects/']").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("selenium-project").click()
        time.sleep(1)
        try:
            machine_text = self.driver.find_element_by_id("project-machine-name")
            if (machine_text.text != "qemux86"):
                self.driver.find_element_by_id("change-machine-toggle").click()
                time.sleep(1)
                self.driver.find_element_by_id("machine-change-input").clear()
                self.driver.find_element_by_id("machine-change-input").send_keys("qemux86")
                self.driver.find_element_by_id("machine-change-input").send_keys(Keys.ENTER)
                self.driver.find_element_by_id("machine-change-btn").click()
                time.sleep(1)
        except:
            logging.error("Could not reset machine back to default value; attempting to continue test")
            pass
        layer = True
        while (layer):
            try:
                delete_button = self.driver.find_element_by_xpath("//*[@id='layers-in-project-list']/li[4]/span")
                delete_button.click()
                self.driver.find_element_by_link_text("Configuration").click()
            except:
                layer = False

        default_distro = "poky"
        default_fstypes = "ext3 jffs2 tar.bz2"
        default_package = "package_rpm"
        default_install = "Not set"

        self.driver.find_element_by_link_text("BitBake variables").click()
        current_distro = self.driver.find_element_by_id("distro").text
        if (current_distro != default_distro):
            self.driver.find_element_by_id('change-distro-icon').click()
            time.sleep(1)
            self.driver.find_element_by_id('new-distro').clear()
            self.driver.find_element_by_id('new-distro').send_keys(default_distro)
            self.driver.find_element_by_id('apply-change-distro').click()
        time.sleep(2)
        
        current_fstypes = self.driver.find_element_by_id("image_fstypes").text
        if (current_fstypes != default_fstypes):
            self.driver.find_element_by_id("change-image_fstypes-icon").click()
            active_checkboxes = default_fstypes.split()
            checkboxes = self.driver.find_elements_by_class_name("fs-checkbox-fstypes")
            for element in checkboxes:
                if (element.get_attribute("checked")):
                    element.click()
            for element in checkboxes:
                if (element.get_attribute("value") in active_checkboxes):
                    element.click()
            self.driver.find_element_by_id("apply-change-image_fstypes").click()

        current_install = self.driver.find_element_by_id("image_install").text
        if (current_install != default_install):
            try:
                self.driver.find_element_by_id("delete-image_install-icon").click()
                #wait for animation to finish
                time.sleep(4)
            except:
                pass

        current_package = self.driver.find_element_by_id("package_classes").text
        if (current_package != default_package):
            self.driver.find_element_by_id("change-package_classes-icon").click()
            time.sleep(1)
            select = Select(self.driver.find_element_by_id("package_classes-select"))
            select.select_by_visible_text("package_rpm")
            first_box = self.driver.find_element_by_id("package_class_1_input")
            second_box = self.driver.find_element_by_id("package_class_1_input")
            if (first_box.get_attribute("checked")):
                first_box.click()
            if (second_box.get_attribute("checked")):
                second_box.click()
            self.driver.find_element_by_id("apply-change-package_classes").click()
        time.sleep(2)

    @staticmethod
    def logger_create():
        log_file = "toaster-auto-" + time.strftime("%Y%m%d%H%M%S") + ".log"
        if os.path.exists("toaster-auto.log"): os.remove("toaster-auto.log")
        os.symlink(log_file, "toaster-auto.log")

        log = logging.getLogger("toaster")
        log.setLevel(logging.DEBUG)

        fh = logging.FileHandler(filename=log_file, mode='w')
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        log.addHandler(fh)
        log.addHandler(ch)

        return log


    def setup_browser(self, *browser_path):
        self.browser = eval(self.parser.get('toaster_test_' + self.target_suite, 'test_browser'))
        print self.browser
        if self.browser == "firefox":
            driver = webdriver.Firefox()
        elif self.browser == "chrome":
            driver = webdriver.Chrome()
        elif self.browser == "ie":
            driver = webdriver.Ie()
        else:
            driver = None
            print "unrecognized browser type, please check"
        self.driver = driver
        self.driver.implicitly_wait(30)
        return self.driver


    def save_screenshot(self,  **log_args):
        """
        This function is used to save screen either by os interface or selenium interface.
        How to use:
        self.save_screenshot(screenshot_type = 'native'/'selenium', log_sub_dir = 'xxx',
                             append_name = 'stepx')
        where native means screenshot func provided by OS,
        selenium means screenshot func provided by selenium webdriver
        """
        types = [log_args.get('screenshot_type')]
        # when no screenshot_type is specified
        if types == [None]:
            types = ['native', 'selenium']
        # normally append_name is used to specify which step..
        add_name = log_args.get('append_name')
        if not add_name:
            add_name = '-'
        # normally there's no need to specify sub_dir
        sub_dir = log_args.get('log_sub_dir')
        if not sub_dir:
            # use casexxx as sub_dir name
            sub_dir = 'case' + str(self.case_no)
        for item in types:
            log_dir = self.log_tmp_dir + os.sep + sub_dir
            mkdir_p(log_dir)
            log_path = log_dir + os.sep +  self.browser + '-' +\
                    item + '-' + add_name + '-' + str(self.screenshot_sequence) + '.png'
            if item == 'native':
                if self.host_os == "linux":
                    os.system("scrot " + log_path)
                elif self.host_os=="darwin":
                    os.system("screencapture -x " + log_path)
            elif item == 'selenium':
                self.driver.get_screenshot_as_file(log_path)
            self.screenshot_sequence += 1

    def browser_delay(self):
        """
        currently this is a workaround for some chrome test.
        Sometimes we need a delay to accomplish some operation.
        But for firefox, mostly we don't need this.
        To be discussed
        """
        if self.browser == "chrome":
            time.sleep(1)
        return


# these functions are not contained in WebDriver class..
    def find_element_by_text(self, string):
        return self.driver.find_element_by_xpath("//*[text()='" + string + "']")


    def find_elements_by_text(self, string):
        return self.driver.find_elements_by_xpath("//*[text()='" + string + "']")


    def find_element_by_text_in_table(self, table_id, text_string):
        """
        This is used to search some certain 'text' in certain table
        """
        try:
            table_element = self.get_table_element(table_id)
            element = table_element.find_element_by_xpath("//*[text()='" + text_string + "']")
        except NoSuchElementException, e:
            print 'no element found'
            raise
        return element


    def find_element_by_link_text_in_table(self, table_id, link_text):
        """
        Assume there're multiple suitable "find_element_by_link_text".
        In this circumstance we need to specify "table".
        """
        try:
            table_element = self.get_table_element(table_id)
            element = table_element.find_element_by_link_text(link_text)
        except NoSuchElementException, e:
            print 'no element found'
            raise
        return element


    def find_elements_by_link_text_in_table(self, table_id, link_text):
        """
        Search link-text in certain table. This helps to narrow down search area.
        """
        try:
            table_element = self.get_table_element(table_id)
            element_list = table_element.find_elements_by_link_text(link_text)
        except NoSuchElementException, e:
            print 'no element found'
            raise
        return element_list


    def find_element_by_partial_link_text_in_table(self, table_id, link_text):
        """
        Search element by partial link text in certain table.
        """
        try:
            table_element = self.get_table_element(table_id)
            element = table_element.find_element_by_partial_link_text(link_text)
            return element
        except NoSuchElementException, e:
            print 'no element found'
            raise


    def find_elements_by_partial_link_text_in_table(self, table_id, link_text):
        """
        Assume there're multiple suitable "find_partial_element_by_link_text".
        """
        try:
            table_element = self.get_table_element(table_id)
            element_list = table_element.find_elements_by_partial_link_text(link_text)
            return element_list
        except NoSuchElementException, e:
            print 'no element found'
            raise


    def find_element_by_xpath_in_table(self, table_id, xpath):
        """
        This helps to narrow down search area. Especially useful when dealing with pop-up form.
        """
        try:
            table_element = self.get_table_element(table_id)
            element = table_element.find_element_by_xpath(xpath)
        except NoSuchElementException, e:
            print 'no element found'
            raise
        return element


    def find_elements_by_xpath_in_table(self, table_id, xpath):
        """
        This helps to narrow down search area. Especially useful when dealing with pop-up form.
        """
        try:
            table_element = self.get_table_element(table_id)
            element_list = table_element.find_elements_by_xpath(xpath)
        except NoSuchElementException, e:
            print 'no elements found'
            raise
        return element_list


    def shortest_xpath(self, pname, pvalue):
        return "//*[@" + pname + "='" + pvalue + "']"


#usually elements in the same column are with same class name. for instance: class="outcome" .TBD
    def get_table_column_text(self, attr_name, attr_value):
        c_xpath = self.shortest_xpath(attr_name, attr_value)
        elements = self.driver.find_elements_by_xpath(c_xpath)
        c_list = []
        for element in elements:
            c_list.append(element.text)
        return c_list


    def get_table_column_text_by_column_number(self, table_id, column_number):
        c_xpath = "//*[@id='" + table_id + "']//td[" + str(column_number) + "]"
        elements = self.driver.find_elements_by_xpath(c_xpath)
        c_list = []
        for element in elements:
            c_list.append(element.text)
        return c_list


    def get_table_head_text(self, *table_id):
#now table_id is a tuple...
        if table_id:
            thead_xpath = "//*[@id='" + table_id[0] + "']//thead//th[text()]"
            elements = self.driver.find_elements_by_xpath(thead_xpath)
            c_list = []
            for element in elements:
                if element.text:
                    c_list.append(element.text)
            return c_list
#default table on page
        else:
            return self.driver.find_element_by_xpath("//*/table/thead").text



    def get_table_element(self, table_id, *coordinate):
        if len(coordinate) == 0:
#return whole-table element
            element_xpath = "//*[@id='" + table_id + "']"
            try:
                element = self.driver.find_element_by_xpath(element_xpath)
            except NoSuchElementException, e:
                raise
            return element
        row = coordinate[0]

        if len(coordinate) == 1:
#return whole-row element
            element_xpath = "//*[@id='" + table_id + "']/tbody/tr[" + str(row) + "]"
            try:
                element = self.driver.find_element_by_xpath(element_xpath)
            except NoSuchElementException, e:
                return False
            return element
#now we are looking for an element with specified X and Y
        column = coordinate[1]

        element_xpath = "//*[@id='" + table_id + "']/tbody/tr[" + str(row) + "]/td[" + str(column) + "]"
        try:
            element = self.driver.find_element_by_xpath(element_xpath)
        except NoSuchElementException, e:
            return False
        return element


    def get_table_data(self, table_id, row_count, column_count):
        row = 1
        Lists = []
        while row <= row_count:
            column = 1
            row_content=[]
            while column <= column_count:
                s= "//*[@id='" + table_id + "']/tbody/tr[" + str(row) +"]/td[" + str(column) + "]"
                v = self.driver.find_element_by_xpath(s).text
                row_content.append(v)
                column = column + 1
                print("row_content=",row_content)
            Lists.extend(row_content)
            print Lists[row-1][0]
            row = row + 1
        return Lists

    # The is_xxx_present functions only returns True/False
    # All the log work is done in test procedure, so we can easily trace back
    # using logging
    def is_text_present (self, patterns):
        for pattern in patterns:
            if str(pattern) not in self.driver.page_source:
                print 'Text "'+pattern+'" is missing'
                return False
        return True


    def is_element_present(self, how, what):
        try:
            self.driver.find_element(how, what)
        except NoSuchElementException, e:
            print 'Could not find element '+str(what)+' by ' + str(how)
            return False
        return True


    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True


    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True


    def get_case_number(self):
        """
        what case are we running now
        """
        funcname = sys._getframe(1).f_code.co_name
        caseno_str = funcname.strip('test_')
        try:
            caseno = int(caseno_str)
        except ValueError:
            print "get case number error! please check if func name is test_xxx"
            return False
        return caseno


    def tearDown(self):
        self.log.info(' END: CASE %s log \n\n' % str(self.case_no))
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


###################################################################
#                                                                 #
# PART III: test cases                                            #
# please refer to                                                 #
# https://bugzilla.yoctoproject.org/tr_show_case.cgi?case_id=xxx  #
#                                                                 #
###################################################################

# Note: to comply with the unittest framework, we call these test_xxx functions
# from run_toastercases.py to avoid calling setUp() and tearDown() multiple times


class toaster_cases(toaster_cases_base):
        ##############
        #  CASE 901  #
        ##############
    def test_901(self):
        # the reason why get_case_number is not in setUp function is that
        # otherwise it returns "setUp" instead of "test_xxx"
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        # open all columns
        self.driver.find_element_by_id("edit-columns-button").click()
        # adding explicitly wait for chromedriver..-_-
        self.browser_delay()
        self.driver.find_element_by_id("started_on").click()
        self.browser_delay()
        self.driver.find_element_by_id("time").click()
        self.driver.find_element_by_id("edit-columns-button").click()
        # dict: {lint text name : actual class name}
        table_head_dict = {'Outcome':'outcome', 'Recipe':'target', 'Machine':'machine', 'Started on':'started_on', 'Completed on':'completed_on', \
                'Errors':'errors_no', 'Warnings':'warnings_no', 'Time':'time'}
        for key in table_head_dict:
            try:
                self.driver.find_element_by_link_text(key).click()
            except Exception, e:
                self.log.error("%s cannot be found on page" % key)
                raise
            column_list = self.get_table_column_text("class", table_head_dict[key])
            # after 1st click, the list should be either sequenced or inverted, but we don't have a "default order" here
            # the point is, after another click, it should be another order
            if is_list_inverted(column_list):
                self.driver.find_element_by_link_text(key).click()
                column_list = self.get_table_column_text("class", table_head_dict[key])
                self.assertTrue(is_list_sequenced(column_list), msg=("%s column not in order" % key))
            else:
                self.assertTrue(is_list_sequenced(column_list), msg=("%s column not sequenced" % key))
                self.driver.find_element_by_link_text(key).click()
                column_list = self.get_table_column_text("class", table_head_dict[key])
                self.assertTrue(is_list_inverted(column_list), msg=("%s column not inverted" % key))
        self.log.info("case passed")


        ##############
        #  CASE 902  #
        ##############
    def test_902(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        # Could add more test patterns here in the future. Also, could search some items other than target column in future..
        patterns = ["minimal", "sato"]
        for pattern in patterns:
            ori_target_column_texts = self.get_table_column_text("class", "target")
            print ori_target_column_texts
            self.driver.find_element_by_id("search").clear()
            self.driver.find_element_by_id("search").send_keys(pattern)
            self.driver.find_element_by_id("search-button").click()
            new_target_column_texts = self.get_table_column_text("class", "target")
            # if nothing found, we still count it as "pass"
            if new_target_column_texts:
                for text in new_target_column_texts:
                    self.assertTrue(text.find(pattern), msg=("%s item doesn't exist " % pattern))
            self.driver.find_element_by_css_selector("i.icon-remove").click()
            target_column_texts = self.get_table_column_text("class", "target")
            self.assertTrue(ori_target_column_texts == target_column_texts, msg=("builds changed after operations"))


        ##############
        #  CASE 903  #
        ##############
    def test_903(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        # when opening a new page, "started_on" is not displayed by default
        self.driver.find_element_by_id("edit-columns-button").click()
        # currently all the delay are for chrome driver -_-
        self.browser_delay()
        self.driver.find_element_by_id("started_on").click()
        self.driver.find_element_by_id("edit-columns-button").click()
        # step 4
        items = ["Outcome", "Completed on", "Started on"]
        for item in items:
            try:
                temp_element = self.find_element_by_text_in_table('otable', item)
                # this is how we find "filter icon" in the same level as temp_element(where "a" means clickable, "i" means icon)
                self.assertTrue(temp_element.find_element_by_xpath("..//*/a/i[@class='icon-filter filtered']"))
            except Exception,e:
                self.assertFalse(True, msg=(" %s cannot be found! %s" % (item, e)))
                raise
        # step 5-6
        temp_element = self.find_element_by_link_text_in_table('otable', 'Outcome')
        temp_element.find_element_by_xpath("..//*/a/i[@class='icon-filter filtered']").click()
        self.browser_delay()
        # the 2nd option, whatever it is
        self.driver.find_element_by_xpath("(//input[@name='filter'])[2]").click()
        # click "Apply" button
        self.driver.find_element_by_xpath("//*[@id='filter_outcome']//*[text()='Apply']").click()
        # save screen here
        time.sleep(1)
        self.save_screenshot(screenshot_type='selenium', append_name='step5')
        temp_element = self.find_element_by_link_text_in_table('otable', 'Completed on')
        temp_element.find_element_by_xpath("..//*/a/i[@class='icon-filter filtered']").click()
        self.browser_delay()
        self.driver.find_element_by_xpath("//*[@id='filter_completed_on']//*[text()='Apply']").click()
        # save screen here to compare to previous one
        # please note that for chrome driver, need a little break before saving
        # screen here -_-
        self.browser_delay()
        self.save_screenshot(screenshot_type='selenium', append_name='step6')
        self.driver.find_element_by_id("search").clear()
        self.driver.find_element_by_id("search").send_keys("core-image")
        self.driver.find_element_by_id("search-button").click()


        ##############
        #  CASE 904  #
        ##############
    def test_904(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_partial_link_text("core-image").click()
        self.driver.find_element_by_link_text("Tasks").click()
        self.table_name = 'otable'
        # This is how we find the "default" rows-number!
        rows_displayed = int(Select(self.driver.find_element_by_css_selector("select.pagesize")).first_selected_option.text)
        print rows_displayed
        self.assertTrue(self.get_table_element(self.table_name, rows_displayed), msg=("not enough rows displayed"))
        self.assertFalse(self.get_table_element(self.table_name, rows_displayed + 1), \
                         msg=("more rows displayed than expected"))
        # Search text box background text is "Search tasks"
        self.assertTrue(self.driver.find_element_by_xpath("//*[@id='searchform']/*[@placeholder='Search tasks']"),\
                        msg=("background text doesn't exist"))

        self.driver.find_element_by_id("search").clear()
        self.driver.find_element_by_id("search").send_keys("busybox")
        self.driver.find_element_by_id("search-button").click()
        self.browser_delay()
        self.save_screenshot(screenshot_type='selenium', append_name='step5')
        self.driver.find_element_by_css_selector("i.icon-remove").click()
        # Save screen here
        self.save_screenshot(screenshot_type='selenium', append_name='step5_2')
        self.driver.find_element_by_id("edit-columns-button").click()
        self.driver.find_element_by_id("cpu_used").click()
        self.driver.find_element_by_id("disk_io").click()
        self.driver.find_element_by_id("recipe_version").click()
        self.driver.find_element_by_id("time_taken").click()
        self.driver.find_element_by_id("edit-columns-button").click()
        # The operation is the same as case901
        # dict: {lint text name : actual class name}
        table_head_dict = {'Order':'order', 'Recipe':'recipe_name', 'Task':'task_name', 'Executed':'executed', \
                           'Outcome':'outcome', 'Cache attempt':'cache_attempt', 'Time (secs)':'time_taken', 'CPU usage':'cpu_used', \
                           'Disk I/O (ms)':'disk_io'}
        for key in table_head_dict:
        # This is tricky here: we are doing so because there may be more than 1
        # same-name link_text in one page. So we only find element inside the table
            self.find_element_by_link_text_in_table(self.table_name, key).click()
            column_list = self.get_table_column_text("class", table_head_dict[key])
        # after 1st click, the list should be either sequenced or inverted, but we don't have a "default order" here
        # the point is, after another click, it should be another order
        # the first case is special:this means every item in column_list is the same, so
        # after one click, either sequenced or inverted will be fine
            if (is_list_inverted(column_list) and is_list_sequenced(column_list)) \
                or (not column_list) :
                self.find_element_by_link_text_in_table(self.table_name, key).click()
                column_list = self.get_table_column_text("class", table_head_dict[key])
                self.assertTrue(is_list_sequenced(column_list) or is_list_inverted(column_list), \
                                msg=("%s column not in any order" % key))
            elif is_list_inverted(column_list):
                self.find_element_by_link_text_in_table(self.table_name, key).click()
                column_list = self.get_table_column_text("class", table_head_dict[key])
                self.assertTrue(is_list_sequenced(column_list), msg=("%s column not in order" % key))
            else:
                self.assertTrue(is_list_sequenced(column_list), msg=("%s column not in order" % key))
                self.find_element_by_link_text_in_table(self.table_name, key).click()
                column_list = self.get_table_column_text("class", table_head_dict[key])
                self.assertTrue(is_list_inverted(column_list), msg=("%s column not inverted" % key))
        # step 8-10
        # filter dict: {link text name : filter table name in xpath}
        filter_dict = {'Executed':'filter_executed', 'Outcome':'filter_outcome', 'Cache attempt':'filter_cache_attempt'}
        for key in filter_dict:
            temp_element = self.find_element_by_link_text_in_table(self.table_name, key)
            # find the filter icon besides it.
            # And here we must have break (1 sec) to get the popup stuff
            temp_element.find_element_by_xpath("..//*[@class='icon-filter filtered']").click()
            self.browser_delay()
            avail_options = self.driver.find_elements_by_xpath("//*[@id='" + filter_dict[key] + "']//*[@name='filter'][not(@disabled)]")
            for number in range(0, len(avail_options)):
                avail_options[number].click()
                self.browser_delay()
                # click "Apply"
                self.driver.find_element_by_xpath("//*[@id='" + filter_dict[key]  + "']//*[@type='submit']").click()
                # insert screen capture here
                self.browser_delay()
                self.save_screenshot(screenshot_type='selenium', append_name='step8')
                # after the last option was clicked, we don't need operation below anymore
                if number < len(avail_options)-1:
                     try:
                        temp_element = self.find_element_by_link_text_in_table(self.table_name, key)
                        temp_element.find_element_by_xpath("..//*[@class='icon-filter filtered']").click()
                        avail_options = self.driver.find_elements_by_xpath("//*[@id='" + filter_dict[key] + "']//*[@name='filter'][not(@disabled)]")
                     except:
                        print "in exception"
                        self.find_element_by_text("Show all tasks").click()
#                        self.driver.find_element_by_xpath("//*[@id='searchform']/button[2]").click()
                        temp_element = self.find_element_by_link_text_in_table(self.table_name, key)
                        temp_element.find_element_by_xpath("..//*[@class='icon-filter filtered']").click()
                        avail_options = self.driver.find_elements_by_xpath("//*[@id='" + filter_dict[key] + "']//*[@name='filter'][not(@disabled)]")
                     self.browser_delay()
        # step 11
        for item in ['order', 'task_name', 'executed', 'outcome', 'recipe_name', 'recipe_version']:
            try:
                self.find_element_by_xpath_in_table(self.table_name, "./tbody/tr[1]/*[@class='" + item + "']/a").click()
            except NoSuchElementException, e:
            # let it go...
                print 'no item in the colum' + item
            # insert screen shot here
            self.save_screenshot(screenshot_type='selenium', append_name='step11')
            self.driver.back()
        # step 12-14
        # about test_dict: please refer to testcase 904 requirement step 12-14
        test_dict = {
            'Time':{
                'class':'time_taken',
                'check_head_list':['Recipe', 'Task', 'Executed', 'Outcome', 'Time (secs)'],
                'check_column_list':['cpu_used', 'cache_attempt', 'disk_io', 'order', 'recipe_version']
            },
            'CPU usage':{
                'class':'cpu_used',
                'check_head_list':['Recipe', 'Task', 'Executed', 'Outcome', 'CPU usage'],
                'check_column_list':['cache_attempt', 'disk_io', 'order', 'recipe_version', 'time_taken']
            },
            'Disk I/O':{
                'class':'disk_io',
                'check_head_list':['Recipe', 'Task', 'Executed', 'Outcome', 'Disk I/O (ms)'],
                'check_column_list':['cpu_used', 'cache_attempt', 'order', 'recipe_version', 'time_taken']
            }
        }
        for key in test_dict:
            self.find_element_by_partial_link_text_in_table('nav', 'core-image').click()
            self.find_element_by_link_text_in_table('nav', key).click()
            head_list = self.get_table_head_text('otable')
            for item in test_dict[key]['check_head_list']:
                self.assertTrue(item in head_list, msg=("%s not in head row" % item))
            column_list = self.get_table_column_text('class', test_dict[key]['class'])
            self.assertTrue(is_list_inverted(column_list), msg=("%s column not inverted" % key))

            self.driver.find_element_by_id("edit-columns-button").click()
            for item2 in test_dict[key]['check_column_list']:
                self.driver.find_element_by_id(item2).click()
            self.driver.find_element_by_id("edit-columns-button").click()
            # TBD: save screen here


        ##############
        #  CASE 906  #
        ##############
    def test_906(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.find_element_by_link_text_in_table('nav', 'Packages').click()
        # find "bash" in first column (Packages)
        self.driver.find_element_by_xpath("//*[@id='otable']//td[1]//*[text()='bash']").click()
        # save sceen here to observe...
        # step 6
        self.driver.find_element_by_partial_link_text("Generated files").click()
        head_list = self.get_table_head_text('otable')
        for item in ['File', 'Size']:
            self.assertTrue(item in head_list, msg=("%s not in head row" % item))
        c_list = self.get_table_column_text('class', 'path')
        self.assertTrue(is_list_sequenced(c_list), msg=("column not in order"))
        # step 7
        self.driver.find_element_by_partial_link_text("Runtime dependencies").click()
        # save sceen here to observe...
        # note that here table name is not 'otable'
        head_list = self.get_table_head_text('dependencies')
        for item in ['Package', 'Version', 'Size']:
            self.assertTrue(item in head_list, msg=("%s not in head row" % item))
        c_list = self.get_table_column_text_by_column_number('dependencies', 1)
        self.assertTrue(is_list_sequenced(c_list), msg=("list not in order"))
        texts = ['Size', 'License', 'Recipe', 'Recipe version', 'Layer', \
                     'Layer commit']
        self.failUnless(self.is_text_present(texts))


        ##############
        #  CASE 910  #
        ##############
    def test_910(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        image_type="core-image-minimal"
        test_package1="busybox"
        test_package2="lib"
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text(image_type).click()
        self.driver.find_element_by_link_text("Recipes").click()
        self.save_screenshot(screenshot_type='selenium', append_name='step3')

        self.table_name = 'otable'
        # This is how we find the "default" rows-number!
        rows_displayed = int(Select(self.driver.find_element_by_css_selector("select.pagesize")).first_selected_option.text)
        print rows_displayed
        self.assertTrue(self.get_table_element(self.table_name, rows_displayed))
        self.assertFalse(self.get_table_element(self.table_name, rows_displayed + 1))

        # Check the default table is sorted by Recipe
        tasks_column_count = len(self.driver.find_elements_by_xpath("/html/body/div[2]/div/div[2]/div[2]/table/tbody/tr/td[1]"))
        print tasks_column_count
        default_column_list = self.get_table_column_text_by_column_number(self.table_name, 1)
        #print default_column_list

        self.assertTrue(is_list_sequenced(default_column_list))

        # Search text box background text is "Search recipes"
        self.assertTrue(self.driver.find_element_by_xpath("//*[@id='searchform']/*[@placeholder='Search recipes']"))

        self.driver.find_element_by_id("search").clear()
        self.driver.find_element_by_id("search").send_keys(test_package1)
        self.driver.find_element_by_id("search-button").click()
        # Save screen here
        self.save_screenshot(screenshot_type='selenium', append_name='step4')
        self.driver.find_element_by_css_selector("i.icon-remove").click()
        self.save_screenshot(screenshot_type='selenium', append_name='step4_2')

        self.driver.find_element_by_id("edit-columns-button").click()
        self.driver.find_element_by_id("depends_on").click()
        self.driver.find_element_by_id("layer_version__branch").click()
        self.driver.find_element_by_id("layer_version__layer__commit").click()
        self.driver.find_element_by_id("depends_by").click()
        self.driver.find_element_by_id("edit-columns-button").click()

        self.find_element_by_link_text_in_table(self.table_name, 'Recipe').click()
        # Check the inverted table by Recipe
        # Recipe doesn't have class name
        #inverted_tasks_column_count = len(self.driver.find_elements_by_xpath("/html/body/div[2]/div/div[2]/div[2]/table/tbody/tr/td[1]"))
        #print inverted_tasks_column_count
        #inverted_column_list = self.get_table_column_text_by_column_number(self.table_name, 1)
        #print inverted_column_list

        #self.driver.find_element_by_partial_link_text("zlib").click()
        #self.driver.back()
        #self.assertTrue(is_list_inverted(inverted_column_list))
        #self.find_element_by_link_text_in_table(self.table_name, 'Recipe').click()

        table_head_dict = {'Recipe':'recipe__name', 'Recipe file':'recipe_file', 'Section':'recipe_section', \
                'License':'recipe_license', 'Layer':'layer_version__layer__name', \
                'Layer branch':'layer_version__branch'}
        for key in table_head_dict:
            self.find_element_by_link_text_in_table(self.table_name, key).click()
            column_list = self.get_table_column_text("class", table_head_dict[key])
            if (is_list_inverted(column_list) and is_list_sequenced(column_list)) \
                    or (not column_list) :
                self.find_element_by_link_text_in_table(self.table_name, key).click()
                column_list = self.get_table_column_text("class", table_head_dict[key])
                self.assertTrue(is_list_sequenced(column_list) or is_list_inverted(column_list))
                self.driver.find_element_by_partial_link_text("acl").click()
                self.driver.back()
                self.assertTrue(is_list_sequenced(column_list) or is_list_inverted(column_list))
                # Search text box background text is "Search recipes"
                self.assertTrue(self.driver.find_element_by_xpath("//*[@id='searchform']/*[@placeholder='Search recipes']"))
                self.driver.find_element_by_id("search").clear()
                self.driver.find_element_by_id("search").send_keys(test_package2)
                self.driver.find_element_by_id("search-button").click()
                column_search_list = self.get_table_column_text("class", table_head_dict[key])
                self.assertTrue(is_list_sequenced(column_search_list) or is_list_inverted(column_search_list))
                self.driver.find_element_by_css_selector("i.icon-remove").click()
            elif is_list_inverted(column_list):
                self.find_element_by_link_text_in_table(self.table_name, key).click()
                column_list = self.get_table_column_text("class", table_head_dict[key])
                self.assertTrue(is_list_sequenced(column_list))
                self.driver.find_element_by_partial_link_text("acl").click()
                self.driver.back()
                self.assertTrue(is_list_sequenced(column_list))
                # Search text box background text is "Search recipes"
                self.assertTrue(self.driver.find_element_by_xpath("//*[@id='searchform']/*[@placeholder='Search recipes']"))
                self.driver.find_element_by_id("search").clear()
                self.driver.find_element_by_id("search").send_keys(test_package2)
                self.driver.find_element_by_id("search-button").click()
                column_search_list = self.get_table_column_text("class", table_head_dict[key])
                self.assertTrue(is_list_sequenced(column_search_list))
                self.driver.find_element_by_css_selector("i.icon-remove").click()
            else:
                self.assertTrue(is_list_sequenced(column_list),  msg=("list %s not sequenced" % key))
                self.find_element_by_link_text_in_table(self.table_name, key).click()
                column_list = self.get_table_column_text("class", table_head_dict[key])
                self.assertTrue(is_list_inverted(column_list))
                try:
                    self.driver.find_element_by_partial_link_text("acl").click()
                except:
                    self.driver.find_element_by_partial_link_text("zlib").click()
                self.driver.back()
                self.assertTrue(is_list_inverted(column_list))
                # Search text box background text is "Search recipes"
                self.assertTrue(self.driver.find_element_by_xpath("//*[@id='searchform']/*[@placeholder='Search recipes']"))
                self.driver.find_element_by_id("search").clear()
                self.driver.find_element_by_id("search").send_keys(test_package2)
                self.driver.find_element_by_id("search-button").click()
                column_search_list = self.get_table_column_text("class", table_head_dict[key])
                #print column_search_list
                self.assertTrue(is_list_inverted(column_search_list))
                self.driver.find_element_by_css_selector("i.icon-remove").click()

        # Bug 5919
        for key in table_head_dict:
            print key
            self.find_element_by_link_text_in_table(self.table_name, key).click()
            self.driver.find_element_by_id("edit-columns-button").click()
            self.driver.find_element_by_id(table_head_dict[key]).click()
            self.driver.find_element_by_id("edit-columns-button").click()
            self.browser_delay()
            # After hide the column, the default table should be sorted by Recipe
            tasks_column_count = len(self.driver.find_elements_by_partial_link_text("acl"))
            #print tasks_column_count
            default_column_list = self.get_table_column_text_by_column_number(self.table_name, 1)
            #print default_column_list
            self.assertTrue(is_list_sequenced(default_column_list))

        self.driver.find_element_by_id("edit-columns-button").click()
        self.driver.find_element_by_id("recipe_file").click()
        self.driver.find_element_by_id("recipe_section").click()
        self.driver.find_element_by_id("recipe_license").click()
        self.driver.find_element_by_id("layer_version__layer__name").click()
        self.driver.find_element_by_id("edit-columns-button").click()


        ##############
        #  CASE 911  #
        ##############
    def test_911(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.find_element_by_link_text_in_table('nav', 'Recipes').click()
        # step 3-5
        self.driver.find_element_by_id("search").clear()
        self.driver.find_element_by_id("search").send_keys("lib")
        self.driver.find_element_by_id("search-button").click()
        # save screen here for observation
        self.save_screenshot(screenshot_type='selenium', append_name='step5')
        # step 6
        self.driver.find_element_by_css_selector("i.icon-remove").click()
        self.driver.find_element_by_id("search").clear()
        # we deliberately want "no result" here
        self.driver.find_element_by_id("search").send_keys("no such input")
        self.driver.find_element_by_id("search-button").click()
        try:
            self.find_element_by_text("Show all recipes").click()
        except:
            self.fail(msg='Could not identify blank page elements')

        ##############
        #  CASE 912  #
        ##############
    def test_912(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.find_element_by_link_text_in_table('nav', 'Recipes').click()
        # step 3
        head_list = self.get_table_head_text('otable')
        for item in ['Recipe', 'Recipe version', 'Recipe file', 'Section', 'License', 'Layer']:
            self.assertTrue(item in head_list, msg=("item %s not in head row" % item))
        self.driver.find_element_by_id("edit-columns-button").click()
        self.driver.find_element_by_id("depends_on").click()
        self.driver.find_element_by_id("layer_version__branch").click()
        self.driver.find_element_by_id("layer_version__layer__commit").click()
        self.driver.find_element_by_id("depends_by").click()
        self.driver.find_element_by_id("edit-columns-button").click()
        # check if columns selected above is shown
        check_list = ['Dependencies', 'Layer branch', 'Layer commit', 'Reverse dependencies']
        head_list = self.get_table_head_text('otable')
        time.sleep(2)
        print head_list
        for item in check_list:
            self.assertTrue(item in head_list, msg=("item %s not in head row" % item))
        # un-check 'em all
        self.driver.find_element_by_id("edit-columns-button").click()
        self.driver.find_element_by_id("depends_on").click()
        self.driver.find_element_by_id("layer_version__branch").click()
        self.driver.find_element_by_id("layer_version__layer__commit").click()
        self.driver.find_element_by_id("depends_by").click()
        self.driver.find_element_by_id("edit-columns-button").click()
        # don't exist any more
        head_list = self.get_table_head_text('otable')
        for item in check_list:
            self.assertFalse(item in head_list, msg=("item %s should not be in head row" % item))


        ##############
        #  CASE 913  #
        ##############
    def test_913(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.find_element_by_link_text_in_table('nav', 'Recipes').click()
        # step 3
        head_list = self.get_table_head_text('otable')
        for item in ['Recipe', 'Recipe version', 'Recipe file', 'Section', 'License', 'Layer']:
            self.assertTrue(item in head_list, msg=("item %s not in head row" % item))
        # step 4
        self.driver.find_element_by_id("edit-columns-button").click()
        # save screen
        self.browser_delay()
        self.save_screenshot(screenshot_type='selenium', append_name='step4')
        self.driver.find_element_by_id("edit-columns-button").click()


        ##############
        #  CASE 914  #
        ##############
    def test_914(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        image_type="core-image-minimal"
        test_package1="busybox"
        test_package2="gdbm"
        test_package3="gettext-native"
        driver = self.driver
        driver.maximize_window()
        driver.get(self.base_url)
        driver.find_element_by_link_text(image_type).click()
        driver.find_element_by_link_text("Recipes").click()
        driver.find_element_by_link_text(test_package1).click()

        self.table_name = 'information'

        tasks_row_count = len(driver.find_elements_by_xpath("//*[@id='"+self.table_name+"']/table/tbody/tr/td[1]"))
        tasks_column_count = len(driver.find_elements_by_xpath("//*[@id='"+self.table_name+"']/table/tbody/tr[1]/td"))
        print 'rows: '+str(tasks_row_count)
        print 'columns: '+str(tasks_column_count)

        Tasks_column = self.get_table_column_text_by_column_number(self.table_name, 2)
        print ("Tasks_column=", Tasks_column)

        key_tasks=["do_fetch", "do_unpack",  "do_patch", "do_configure", "do_compile", "do_install", "do_package", "do_build"]
        i = 0
        while i < len(key_tasks):
            if key_tasks[i] not in Tasks_column:
                print ("Error! Missing key task: %s" % key_tasks[i])
            else:
                print ("%s is in tasks" % key_tasks[i])
            i = i + 1

        if Tasks_column.index(key_tasks[0]) != 0:
            print ("Error! %s is not in the right position" % key_tasks[0])
        else:
            print ("%s is in right position" % key_tasks[0])

        if Tasks_column[-1] != key_tasks[-1]:
            print ("Error! %s is not in the right position" % key_tasks[-1])
        else:
            print ("%s is in right position" % key_tasks[-1])

        driver.find_element_by_partial_link_text("Packages (").click()
        packages_name = driver.find_element_by_partial_link_text("Packages (").text
        print packages_name
        packages_num = int(filter(str.isdigit, repr(packages_name)))
        print packages_num

        #switch the table to show more than 10 rows at a time
        self.driver.find_element_by_xpath("//*[@id='packages-built']/div[1]/div/select").click()
        Select(driver.find_element_by_xpath("//*[@id='packages-built']/div[1]/div/select")).select_by_value('150')
        self.driver.find_element_by_xpath("//*[@id='packages-built']/div[1]/div/select").send_keys(Keys.ENTER)

        packages_row_count = len(driver.find_elements_by_xpath("//*[@id='otable']/tbody/tr/td[1]"))
        print packages_row_count

        if packages_num != packages_row_count:
            print ("Error! The packages number is not correct")
        else:
            print ("The packages number is correct")

        driver.find_element_by_partial_link_text("Build dependencies (").click()
        depends_name = driver.find_element_by_partial_link_text("Build dependencies (").text
        print depends_name
        depends_num = int(filter(str.isdigit, repr(depends_name)))
        print depends_num

        if depends_num == 0:
            depends_message = repr(driver.find_element_by_css_selector("div.alert.alert-info").text)
            print depends_message
            if depends_message.find("has no build dependencies.") < 0:
                print ("Error! The message isn't expected.")
            else:
                print ("The message is expected")
        else:
            depends_row_count = len(driver.find_elements_by_xpath("//*[@id='dependencies']/table/tbody/tr/td[1]"))
            print depends_row_count
            if depends_num != depends_row_count:
                print ("Error! The dependent packages number is not correct")
            else:
                print ("The dependent packages number is correct")

        driver.find_element_by_partial_link_text("Reverse build dependencies (").click()
        rdepends_name = driver.find_element_by_partial_link_text("Reverse build dependencies (").text
        print rdepends_name
        rdepends_num = int(filter(str.isdigit, repr(rdepends_name)))
        print rdepends_num

        if rdepends_num == 0:
            rdepends_message = repr(driver.find_element_by_css_selector("#brought-in-by > div.alert.alert-info").text)
            print rdepends_message
            if rdepends_message.find("has no reverse build dependencies.") < 0:
                print ("Error! The message isn't expected.")
            else:
                print ("The message is expected")
        else:
            print ("The reverse dependent packages number is correct")

        driver.find_element_by_link_text("Recipes").click()
        driver.find_element_by_link_text(test_package2).click()
        driver.find_element_by_partial_link_text("Packages (").click()
        driver.find_element_by_partial_link_text("Build dependencies (").click()
        driver.find_element_by_partial_link_text("Reverse build dependencies (").click()


        driver.find_element_by_link_text("Recipes").click()
        driver.find_element_by_link_text(test_package3).click()

        native_tasks_row_count = len(driver.find_elements_by_xpath("//*[@id='information']/table/tbody/tr/td[1]"))
        native_tasks_column_count = len(driver.find_elements_by_xpath("//*[@id='information']/table/tbody/tr[1]/td"))
        print native_tasks_row_count
        print native_tasks_column_count

        Native_Tasks_column = self.get_table_column_text_by_column_number(self.table_name, 2)
        print ("Native_Tasks_column=", Native_Tasks_column)

        native_key_tasks=["do_fetch", "do_unpack",  "do_patch", "do_configure", "do_compile", "do_install", "do_build"]
        i = 0
        while i < len(native_key_tasks):
            if native_key_tasks[i] not in Native_Tasks_column:
                print ("Error! Missing key task: %s" % native_key_tasks[i])
            else:
                print ("%s is in tasks" % native_key_tasks[i])
            i = i + 1

        if Native_Tasks_column.index(native_key_tasks[0]) != 0:
            print ("Error! %s is not in the right position" % native_key_tasks[0])
        else:
            print ("%s is in right position" % native_key_tasks[0])

        if Native_Tasks_column[-1] != native_key_tasks[-1]:
            print ("Error! %s is not in the right position" % native_key_tasks[-1])
        else:
            print ("%s is in right position" % native_key_tasks[-1])

        driver.find_element_by_partial_link_text("Packages (").click()
        native_packages_name = driver.find_element_by_partial_link_text("Packages (").text
        print native_packages_name
        native_packages_num = int(filter(str.isdigit, repr(native_packages_name)))
        print native_packages_num

        if native_packages_num != 0:
            print ("Error! Native task shouldn't have any packages.")
        else:
            native_package_message = repr(driver.find_element_by_css_selector("#packages-built > div.alert.alert-info").text)
            print native_package_message
            if native_package_message.find("does not build any packages.") < 0:
                print ("Error! The message for native task isn't expected.")
            else:
                print ("The message for native task is expected.")

        driver.find_element_by_partial_link_text("Build dependencies (").click()
        native_depends_name = driver.find_element_by_partial_link_text("Build dependencies (").text
        print native_depends_name
        native_depends_num = int(filter(str.isdigit, repr(native_depends_name)))
        print native_depends_num

        native_depends_row_count = len(driver.find_elements_by_xpath("//*[@id='dependencies']/table/tbody/tr/td[1]"))
        print native_depends_row_count

        if native_depends_num != native_depends_row_count:
            print ("Error! The dependent packages number is not correct")
        else:
            print ("The dependent packages number is correct")

        driver.find_element_by_partial_link_text("Reverse build dependencies (").click()
        native_rdepends_name = driver.find_element_by_partial_link_text("Reverse build dependencies (").text
        print native_rdepends_name
        native_rdepends_num = int(filter(str.isdigit, repr(native_rdepends_name)))
        print native_rdepends_num

        native_rdepends_row_count = len(driver.find_elements_by_xpath("//*[@id='brought-in-by']/table/tbody/tr/td[1]"))
        print native_rdepends_row_count

        if native_rdepends_num != native_rdepends_row_count:
            print ("Error! The reverse dependent packages number is not correct")
        else:
            print ("The reverse dependent packages number is correct")

        driver.find_element_by_link_text("Recipes").click()


        ##############
        #  CASE 915  #
        ##############
    def test_915(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        # step 3
        self.find_element_by_link_text_in_table('nav', 'Configuration').click()
        self.driver.find_element_by_link_text("BitBake variables").click()
        # step 4
        self.driver.find_element_by_id("search").clear()
        self.driver.find_element_by_id("search").send_keys("lib")
        self.driver.find_element_by_id("search-button").click()
        # save screen to see result
        self.browser_delay()
        self.save_screenshot(screenshot_type='selenium', append_name='step4')
        # step 5
        self.driver.find_element_by_css_selector("i.icon-remove").click()
        head_list = self.get_table_head_text('otable')
        print head_list
        print len(head_list)
        self.assertTrue(head_list == ['Variable', 'Value', 'Set in file', 'Description'], \
                        msg=("head row contents wrong"))
        # step 8
        # search other string. and click "Variable" to re-sort, check if table
        # head is still the same
        self.driver.find_element_by_id("search").clear()
        self.driver.find_element_by_id("search").send_keys("poky")
        self.driver.find_element_by_id("search-button").click()
        self.find_element_by_link_text_in_table('otable', 'Variable').click()
        head_list = self.get_table_head_text('otable')
        self.assertTrue(head_list == ['Variable', 'Value', 'Set in file', 'Description'], \
                        msg=("head row contents wrong"))
        self.find_element_by_link_text_in_table('otable', 'Variable').click()
        head_list = self.get_table_head_text('otable')
        self.assertTrue(head_list == ['Variable', 'Value', 'Set in file', 'Description'], \
                        msg=("head row contents wrong"))


        ##############
        #  CASE 916  #
        ##############
    def test_916(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        # step 2-3
        self.find_element_by_link_text_in_table('nav', 'Configuration').click()
        self.driver.find_element_by_link_text("BitBake variables").click()
        variable_list = self.get_table_column_text('class', 'variable_name')
        self.assertTrue(is_list_sequenced(variable_list), msg=("list not in order"))
        # step 4
        self.find_element_by_link_text_in_table('otable', 'Variable').click()
        variable_list = self.get_table_column_text('class', 'variable_name')
        self.assertTrue(is_list_inverted(variable_list), msg=("list not inverted"))
        self.find_element_by_link_text_in_table('otable', 'Variable').click()
        # step 5
        # searching won't change the sequentiality
        self.driver.find_element_by_id("search").clear()
        self.driver.find_element_by_id("search").send_keys("lib")
        self.driver.find_element_by_id("search-button").click()
        variable_list = self.get_table_column_text('class', 'variable_name')
        self.assertTrue(is_list_sequenced(variable_list), msg=("list not in order"))


        ##############
        #  CASE 923  #
        ##############
    def test_923(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        # Step 2
        # default sequence in "Completed on" column is inverted
        c_list = self.get_table_column_text('class', 'completed_on')
        self.assertTrue(is_list_inverted(c_list), msg=("list not inverted"))
        # step 3
        self.driver.find_element_by_id("edit-columns-button").click()
        self.driver.find_element_by_id("started_on").click()
        self.driver.find_element_by_id("time").click()
        self.driver.find_element_by_id("edit-columns-button").click()
        head_list = self.get_table_head_text('otable')
        for item in ['Outcome', 'Recipe', 'Machine', 'Started on', 'Completed on', 'Failed tasks', 'Errors', 'Warnings', 'Time', "Image files", "Project"]:
            self.failUnless(item in head_list, msg=item+' is missing from table head.')


        ##############
        #  CASE 924  #
        ##############
    def test_924(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        # Please refer to case 924 requirement
        # default sequence in "Completed on" column is inverted
        c_list = self.get_table_column_text('class', 'completed_on')
        self.assertTrue(is_list_inverted(c_list), msg=("list not inverted"))
        # Step 4
        # click Errors , order in "Completed on" should be disturbed. Then hide
        # error column to check if order in "Completed on" can be restored
#THIS TEST IS NO LONGER VALID DUE TO DESIGN CHANGES. LEAVING IN PENDING UPDATES TO DESIGN
        #self.find_element_by_link_text_in_table('otable', 'Errors').click()
        #self.driver.find_element_by_id("edit-columns-button").click()
        #self.driver.find_element_by_id("errors_no").click()
        #self.driver.find_element_by_id("edit-columns-button").click()
        # Note: without time.sleep here, there'll be unpredictable error..TBD
        time.sleep(1)
        c_list = self.get_table_column_text('class', 'completed_on')
        self.assertTrue(is_list_inverted(c_list), msg=("list not inverted"))


        ##############
        #  CASE 940  #
        ##############
    def test_940(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        # Step 2-3
        self.find_element_by_link_text_in_table('nav', 'Packages').click()
        check_head_list = ['Package', 'Package version', 'Size', 'Recipe']
        head_list = self.get_table_head_text('otable')
        self.assertTrue(head_list == check_head_list, msg=("head row not as expected"))
        # Step 4
        # pulldown menu
        option_ids = ['recipe__layer_version__layer__name', 'recipe__layer_version__branch', \
                      'recipe__layer_version__layer__commit', 'license', 'recipe__version']
        self.driver.find_element_by_id("edit-columns-button").click()
        for item in option_ids:
            if not self.driver.find_element_by_id(item).is_selected():
                self.driver.find_element_by_id(item).click()
        self.driver.find_element_by_id("edit-columns-button").click()
        # save screen here to observe that 'Package' and 'Package version' is
        # not selectable
        self.browser_delay()
        self.save_screenshot(screenshot_type='selenium', append_name='step4')


        ##############
        #  CASE 941  #
        ##############
    def test_941(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        # Step 2-3
        self.find_element_by_link_text_in_table('nav', 'Packages').click()
        # column -- Package
        column_list = self.get_table_column_text_by_column_number('otable', 1)
        self.assertTrue(is_list_sequenced(column_list), msg=("list not in order"))
        self.find_element_by_link_text_in_table('otable', 'Size').click()


        ##############
        #  CASE 942  #
        ##############
    def test_942(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.driver.find_element_by_link_text("Packages").click()
        #get initial table header
        head_list = self.get_table_head_text('otable')
        #remove the Recipe column from table header
        self.driver.find_element_by_id("edit-columns-button").click()
        self.driver.find_element_by_id("recipe__name").click()
        self.driver.find_element_by_id("edit-columns-button").click()
        #get modified table header
        new_head = self.get_table_head_text('otable')
        self.assertTrue(head_list > new_head)

        ##############
        #  CASE 943  #
        ##############
    def test_943(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.driver.find_element_by_link_text("Packages").click()
        #search for the "bash" package -> this should definitely be present
        self.driver.find_element_by_id("search").clear()
        self.driver.find_element_by_id("search").send_keys("bash")
        self.driver.find_element_by_id("search-button").click()
        #check for the search result message "XX packages found"
        self.assertTrue(self.is_text_present("packages found"), msg=("no packages found text"))


        ##############
        #  CASE 944  #
        ##############
    def test_944(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        # step 1: test Recipes page stuff
        self.driver.find_element_by_link_text("Recipes").click()
        # for these 3 items, default status is not-checked
        self.driver.find_element_by_id("edit-columns-button").click()
        self.driver.find_element_by_id("layer_version__branch").click()
        self.driver.find_element_by_id("layer_version__layer__commit").click()
        self.driver.find_element_by_id("edit-columns-button").click()
        # otable is the recipes table here
        otable_head_text = self.get_table_head_text('otable')
        for item in ["Layer", "Layer branch", "Layer commit"]:
            self.failIf(item not in otable_head_text, msg=item+' not in table head.')
        # click the fist recipe, whatever it is
        self.get_table_element("otable", 1, 1).click()
        self.assertTrue(self.is_text_present(["Layer", "Layer branch", "Layer commit", "Recipe file"]), \
                        msg=("text not in web page"))

        # step 2: test Packages page stuff. almost same as above
        self.driver.back()
        self.browser_delay()
        self.driver.find_element_by_link_text("Packages").click()
        self.driver.find_element_by_id("edit-columns-button").click()
        self.driver.find_element_by_id("recipe__layer_version__layer__name").click()
        self.driver.find_element_by_id("recipe__layer_version__branch").click()
        self.driver.find_element_by_id("recipe__layer_version__layer__commit").click()
        self.driver.find_element_by_id("edit-columns-button").click()
        otable_head_text = self.get_table_head_text("otable")
        for item in ["Layer", "Layer branch", "Layer commit"]:
            self.assertFalse(item not in otable_head_text, msg=("item %s should be in head row" % item))
        # click the fist recipe, whatever it is
        self.get_table_element("otable", 1, 1).click()
        self.assertTrue(self.is_text_present(["Layer", "Layer branch", "Layer commit"]), \
                        msg=("text not in web page"))

        # step 3: test Packages core-image-minimal(images) stuff. almost same as above. Note when future element-id changes...
        self.driver.back()
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.driver.find_element_by_id("edit-columns-button").click()
        self.driver.find_element_by_id("layer_name").click()
        self.driver.find_element_by_id("layer_branch").click()
        self.driver.find_element_by_id("layer_commit").click()
        self.driver.find_element_by_id("edit-columns-button").click()
        otable_head_text = self.get_table_head_text("otable")
        for item in ["Layer", "Layer branch", "Layer commit"]:
            self.assertFalse(item not in otable_head_text, msg=("item %s should be in head row" % item))
        # click the fist recipe, whatever it is
        self.get_table_element("otable", 1, 1).click()
        self.assertTrue(self.is_text_present(["Layer", "Layer branch", "Layer commit"]), \
                        msg=("text not in web page"))

        # step 4: check Configuration page
        self.driver.back()
        self.driver.find_element_by_link_text("Configuration").click()
        otable_head_text = self.get_table_head_text()
        self.assertTrue(self.is_text_present(["Layer", "Layer branch", "Layer commit"]), \
                        msg=("text not in web page"))


        ##############
        #  CASE 945  #
        ##############
    def test_945(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        for item in ["Packages", "Recipes", "Tasks"]:
            self.driver.get(self.base_url)
            self.driver.find_element_by_link_text("core-image-minimal").click()
            self.driver.find_element_by_link_text(items).click()

            # this may be page specific. If future page content changes, try to replace it with new xpath
            xpath_showrows = "/html/body/div[4]/div/div/div[2]/div[2]/div[2]/div/div/div[2]/select"
            xpath_table = "html/body/div[4]/div/div/div[2]/div[2]/table/tbody"#"id=('otable')/tbody"
            self.driver.find_element_by_xpath(xpath_showrows).click()
            rows_displayed = int(self.driver.find_element_by_xpath(xpath_showrows + "/option[2]").text)

            # not sure if this is a Selenium Select bug: If page is not refreshed here, "select(by visible text)" operation will go back to 100-row page
            # Sure we can use driver.get(url) to refresh page, but since page will vary, we use click link text here
            self.driver.find_element_by_link_text(items).click()
            Select(self.driver.find_element_by_css_selector("select.pagesize")).select_by_visible_text(str(rows_displayed))
            self.failUnless(self.is_element_present(By.XPATH, xpath_table + "/tr[" + str(rows_displayed) +"]"))
            self.failIf(self.is_element_present(By.XPATH, xpath_table + "/tr[" + str(rows_displayed+1) +"]"))

            # click 1st package, then go back to check if it's still those rows shown.
            self.driver.find_element_by_xpath(xpath_otable + "/tr[1]/td[1]/a").click()
            time.sleep(3)
            self.driver.find_element_by_link_text(item).click()
            self.assertTrue(self.is_element_present(By.XPATH, xpath_otable + "/tr[" + str(option_tobeselected) +"]"),\
                            msg=("Row %d should exist" %option_tobeselected))
            self.assertFalse(self.is_element_present(By.XPATH, xpath_otable + "/tr[" + str(option_tobeselected+1) +"]"),\
                            msg=("Row %d should not exist" %(option_tobeselected+1)))



        ##############
        #  CASE 946  #
        ##############
    def test_946(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.driver.find_element_by_link_text("Configuration").click()
        # step 3-4
        check_list = ["Summary", "BitBake variables"]
        for item in check_list:
            if not self.is_element_present(how=By.LINK_TEXT, what=item):
                self.log.error("%s not found" %item)
        if not self.is_text_present(['Layers', 'Layer', 'Layer branch', 'Layer commit']):
            self.log.error("text not found")
        # step 5
        self.driver.find_element_by_link_text("BitBake variables").click()
        if not self.is_text_present(['Variable', 'Value', 'Set in file', 'Description']):
            self.log.error("text not found")
        # This may be unstable because it's page-specific
        # step 6: this is how we find filter beside "Set in file"
        temp_element = self.find_element_by_text_in_table('otable', "Set in file")
        temp_element.find_element_by_xpath("..//*/a/i[@class='icon-filter filtered']").click()
        self.browser_delay()
        self.driver.find_element_by_xpath("(//input[@name='filter'])[3]").click()
        btns = self.driver.find_elements_by_css_selector("button.btn.btn-primary")
        for btn in btns:
            try:
                btn.click()
                break
            except:
                pass
        # save screen here
        self.browser_delay()
        self.save_screenshot(screenshot_type='selenium', append_name='step6')
        self.driver.find_element_by_id("edit-columns-button").click()
        # save screen here
        # step 7
        # we should manually check the step 6-8 result using screenshot
        self.browser_delay()
        self.save_screenshot(screenshot_type='selenium', append_name='step7')
        self.driver.find_element_by_id("edit-columns-button").click()
        # step 9
        # click the 1st item, no matter what it is
        self.driver.find_element_by_xpath("//*[@id='otable']/tbody/tr[1]/td[1]/a").click()
        # give it 1 sec so the pop-up becomes the "active_element"
        time.sleep(1)
        element = self.driver.switch_to.active_element
        check_list = ['Order', 'Configuration file', 'Operation', 'Line number']
        for item in check_list:
            if item not in element.text:
                self.log.error("%s not found" %item)
        # any better way to close this pop-up? ... TBD
        element.find_element_by_class_name("close").click()
        # step 10 : need to manually check "Yocto Manual" in saved screen
        self.driver.find_element_by_css_selector("i.icon-share.get-info").click()
        # save screen here
        time.sleep(5)
        self.save_screenshot(screenshot_type='native', append_name='step10')


        ##############
        #  CASE 947  #
        ##############
    def test_947(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.find_element_by_link_text_in_table('nav', 'Configuration').click()
        # step 2
        self.driver.find_element_by_link_text("BitBake variables").click()
        # step 3
        def xpath_option(column_name):
            # return xpath of options under "Edit columns" button
            return self.shortest_xpath('id', 'navTab') + self.shortest_xpath('id', 'editcol') \
                + self.shortest_xpath('id', column_name)
        self.driver.find_element_by_id('edit-columns-button').click()
        # by default, option "Description" and "Set in file" were checked
        self.driver.find_element_by_xpath(xpath_option('description')).click()
        self.driver.find_element_by_xpath(xpath_option('file')).click()
        self.driver.find_element_by_id('edit-columns-button').click()
        check_list = ['Description', 'Set in file']
        head_list = self.get_table_head_text('otable')
        for item in check_list:
            self.assertFalse(item in head_list, msg=("item %s should not be in head row" % item))
        # check these 2 options and verify again
        self.driver.find_element_by_id('edit-columns-button').click()
        self.driver.find_element_by_xpath(xpath_option('description')).click()
        self.driver.find_element_by_xpath(xpath_option('file')).click()
        self.driver.find_element_by_id('edit-columns-button').click()
        head_list = self.get_table_head_text('otable')
        for item in check_list:
            self.assertTrue(item in head_list, msg=("item %s not in head row" % item))


        ##############
        #  CASE 948  #
        ##############
    def test_948(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.find_element_by_link_text_in_table('nav', 'Configuration').click()
        self.driver.find_element_by_link_text("BitBake variables").click()
        #get number of variables visible by default
        number_before_search = self.driver.find_element_by_class_name('page-header').text
        # search for a while...
        self.driver.find_element_by_id("search").clear()
        self.driver.find_element_by_id("search").send_keys("BB")
        self.driver.find_element_by_id("search-button").click()
        #get number of variables visible after search
        number_after_search = self.driver.find_element_by_class_name('page-header').text
        self.assertTrue(number_before_search > number_after_search, msg=("items should be less after search"))


        ##############
        #  CASE 949  #
        ##############
    def test_949(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.find_element_by_link_text_in_table('nav', 'core-image-minimal').click()
        # step 3
        try:
            self.driver.find_element_by_partial_link_text("Packages included")
            self.driver.find_element_by_partial_link_text("Directory structure")
        except Exception,e:
            self.log.error(e)
            self.assertFalse(True)
        # step 4
        head_list = self.get_table_head_text('otable')
        for item in ['Package', 'Package version', 'Size', 'Dependencies', 'Reverse dependencies', 'Recipe']:
            self.assertTrue(item in head_list, msg=("item %s not in head row" % item))
        # step 5-6
        self.driver.find_element_by_id("edit-columns-button").click()
        selectable_class = 'checkbox'
        # minimum-table : means unselectable items
        unselectable_class = 'checkbox muted'
        selectable_check_list = ['Dependencies', 'Layer', 'Layer branch', 'Layer commit', \
                                 'License', 'Recipe', 'Recipe version', 'Reverse dependencies', \
                                 'Size', 'Size over total (%)']
        unselectable_check_list = ['Package', 'Package version']
        selectable_list = list()
        unselectable_list = list()
        selectable_elements = self.driver.find_elements_by_xpath("//*[@id='editcol']//*[@class='" + selectable_class + "']")
        unselectable_elements = self.driver.find_elements_by_xpath("//*[@id='editcol']//*[@class='" + unselectable_class + "']")
        for element in selectable_elements:
            selectable_list.append(element.text)
        for element in unselectable_elements:
            unselectable_list.append(element.text)
        # check them
        for item in selectable_check_list:
            self.assertTrue(item in selectable_list, msg=("%s not found in dropdown menu" % item))
        for item in unselectable_check_list:
            self.assertTrue(item in unselectable_list, msg=("%s not found in dropdown menu" % item))
        self.driver.find_element_by_id("edit-columns-button").click()
        # step 7
        self.driver.find_element_by_partial_link_text("Directory structure").click()
        head_list = self.get_table_head_text('dirtable')
        for item in ['Directory / File', 'Symbolic link to', 'Source package', 'Size', 'Permissions', 'Owner', 'Group']:
            self.assertTrue(item in head_list, msg=("%s not found in Directory structure table head" % item))

        ##############
        #  CASE 950  #
        ##############
    def test_950(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        # step3&4: so far we're not sure if there's "successful build" or "failed
        # build".If either of them doesn't exist, we can still go on other steps
        check_list = ['Configuration', 'Tasks', 'Recipes', 'Packages', 'Time', 'CPU usage', 'Disk I/O']
        has_successful_build = 1
        has_failed_build = 1
        try:
            pass_icon = self.driver.find_element_by_xpath("//*[@class='icon-ok-sign success']")
        except Exception:
            self.log.info("no successful build exists")
            has_successful_build = 0
            pass
        if has_successful_build:
            pass_icon.click()
            # save screen here to check if it matches requirement.
            self.browser_delay()
            self.save_screenshot(screenshot_type='selenium', append_name='step3_1')
            for item in check_list:
                try:
                    self.find_element_by_link_text_in_table('nav', item)
                except Exception:
                    self.assertFalse(True, msg=("link  %s cannot be found in the page" % item))
            # step 6
            check_list_2 = ['Packages included', 'Total package size', \
                      'License manifest', 'Image files']
            self.assertTrue(self.is_text_present(check_list_2), msg=("text not in web page"))
            self.driver.back()
        try:
            fail_icon = self.driver.find_element_by_xpath("//*[@class='icon-minus-sign error']")
        except Exception:
            has_failed_build = 0
            self.log.info("no failed build exists")
            pass
        if has_failed_build:
            fail_icon.click()
            # save screen here to check if it matches requirement.
            self.browser_delay()
            self.save_screenshot(screenshot_type='selenium', append_name='step3_2')
            for item in check_list:
                try:
                    self.find_element_by_link_text_in_table('nav', item)
                except Exception:
                    self.assertFalse(True, msg=("link  %s cannot be found in the page" % item))
            # step 7 involved
            check_list_3 = ['Machine', 'Distro', 'Layers', 'Total number of tasks', 'Tasks executed', \
                      'Tasks not executed', 'Reuse', 'Recipes built', 'Packages built']
            self.assertTrue(self.is_text_present(check_list_3), msg=("text not in web page"))
            self.driver.back()


        ##############
        #  CASE 951  #
        ##############
    def test_951(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        # currently test case itself isn't responsible for creating "1 successful and
        # 1 failed build"
        has_successful_build = 1
        has_failed_build = 1
        try:
            fail_icon = self.driver.find_element_by_xpath("//*[@class='icon-minus-sign error']")
        except Exception:
            has_failed_build = 0
            self.log.info("no failed build exists")
            pass
        # if there's failed build, we can proceed
        if has_failed_build:
            self.driver.find_element_by_partial_link_text("error").click()
            self.driver.back()
        # not sure if there "must be" some warnings, so here save a screen
        self.browser_delay()
        self.save_screenshot(screenshot_type='selenium', append_name='step4')


        ##############
        #  CASE 955  #
        ##############
    def test_955(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.log.info(" You should manually create all images before test starts!")
        # So far the case itself is not responsable for creating all sorts of images.
        # So assuming they are already there
        # step 2
        self.driver.find_element_by_link_text("core-image-minimal").click()
        # save screen here to see the page component


        ##############
        #  CASE 956  #
        ##############
    def test_956(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        # step 2-3 need to run manually
        self.log.info("step 2-3: checking the help message when you hover on help icon of target,\
                       tasks, recipes, packages need to run manually")
        self.driver.find_element_by_partial_link_text("Manual").click()
        if not self.is_text_present("Manual"):
            self.log.error("please check [Toaster manual] link on page")
            self.failIf(True)

####################################################################################################
# Starting project tests ###########################################################################
####################################################################################################

        ##############
        #  CASE 1100 #
        ##############
    def test_1100(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)

        self.driver.find_element_by_css_selector("a[href='/toastergui/projects/']").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("selenium-project").click()
        time.sleep(1)
        self.driver.find_element_by_partial_link_text("BitBake variables").click()
        time.sleep(1)

        distro_text = self.driver.find_element_by_id("distro").text
        self.assertTrue((distro_text == "poky"), msg="DISTRO variable has unexpected value")

        image_fstypes_text = self.driver.find_element_by_id("image_fstypes").text
        self.assertTrue((image_fstypes_text == "ext3 jffs2 tar.bz2"), msg="IMAGE_FSTYPES variable has unexpected value")

        image_install_text = self.driver.find_element_by_id("image_install").text
        self.assertTrue((image_install_text == "Not set"), msg="IMAGE_INSTALL_append variable has unexpected value")

        package_classes_text = self.driver.find_element_by_id("package_classes").text
        self.assertTrue((package_classes_text == "package_rpm"), msg="PACKAGE_CLASSES variable has unexpected value")

        variable_text = self.driver.find_element_by_id("variable").text
        variable_placeholder = self.driver.find_element_by_id("variable").get_attribute("placeholder")
        self.assertTrue((variable_text == ""), msg="Variable textbox is not empty")
        self.assertTrue((variable_placeholder == "Type variable name"), msg="Variable placeholder has unexpected value")

        value_text = self.driver.find_element_by_id("value").text
        value_placeholder = self.driver.find_element_by_id("value").get_attribute("placeholder")
        self.assertTrue((value_text == ""), msg="Value textbox is not empty")
        self.assertTrue((value_placeholder == "Type variable value"), msg="Value placeholder has unexpected value")

        button_enabled = self.driver.find_element_by_id("add-configvar-button").is_enabled()
        self.assertFalse((button_enabled), msg="Add variable button is enabled; it should not be")

        ##############
        #  CASE 1102 #
        ##############
    def test_1102(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)

        self.driver.find_element_by_css_selector("a[href='/toastergui/projects/']").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("selenium-project").click()
        time.sleep(1)
        self.driver.find_element_by_partial_link_text("BitBake variables").click()
        time.sleep(1)

        #checking distro variable elements
        try:
            self.driver.find_element_by_id("change-distro-icon").click()
        except:
            self.fail("Unable to find distro edit button")

        edit_distro_element = self.driver.find_element_by_id("new-distro")
        edit_distro_value = edit_distro_element.get_attribute("value")
        self.assertTrue((edit_distro_value == 'poky'), msg="DISTRO edit box has unexpected value")

        edit_distro_element.clear()
        #workaround code; using clear() does not make the interface recognise the text box is now empty, so we need to send a key and then delete it so get the save button to be disabled
        #this does not happen when interacting with the interface manually
        edit_distro_element.send_keys("a")
        edit_distro_element.send_keys(Keys.BACKSPACE)
        #end workaround
        edit_distro_save_button = self.driver.find_element_by_id("apply-change-distro")
        self.assertFalse((edit_distro_save_button.is_enabled()), msg="distro save changes button still active with empty value; should not be")

        edit_distro_element.send_keys("poky tiny")
        distro_error_text = self.driver.find_element_by_id("distro-error-message").text
        self.assertTrue((distro_error_text == "A valid distro name cannot include spaces"), msg="Error message is missing when inputting incorrect value in DISTRO variable")
        self.driver.find_element_by_id("cancel-change-distro").click()

        #checking image_fstype variable elements
        image_fstypes_text = self.driver.find_element_by_id("image_fstypes").text
        image_fstypes_values = image_fstypes_text.split()

        try:
            self.driver.find_element_by_id("change-image_fstypes-icon").click()
        except:
            self.fail("Unable to find image_fstype edit button")

        edit_image_fstype_element = self.driver.find_element_by_id("filter-image_fstypes")
        checkboxes = self.driver.find_elements_by_class_name("fs-checkbox-fstypes")
        active_checkboxes = []

        for element in checkboxes:
            if (element.get_attribute("checked")):
                active_checkboxes.append(element.get_attribute("value"))
        self.assertTrue((sorted(image_fstypes_values) == sorted(active_checkboxes)), msg = "list of checked values does not match list of values found at page load")

        for element in checkboxes:
            if (element.get_attribute("value") in active_checkboxes):
                element.click()
        image_fstype_error_text = self.driver.find_element_by_id("fstypes-error-message").text
        self.assertTrue((image_fstype_error_text == "You must select at least one image type"), msg="Error message is missing when inputting incorrect value in image_fstype variable")
        fstype_button = self.driver.find_element_by_id("apply-change-image_fstypes")
        self.assertFalse((fstype_button.is_enabled()), msg="Save changes button for image_fstype is still active with empty values; it should not be")

        for element in checkboxes:
            if (element.get_attribute("value") in active_checkboxes):
                element.click()
            if (element.get_attribute("value") == "cpio"):
                element.click()
        self.driver.find_element_by_id("apply-change-image_fstypes").click()
        time.sleep(1)

        image_fstypes_text_new = self.driver.find_element_by_id("image_fstypes").text
        image_fstypes_values_new = image_fstypes_text_new.split()
        active_checkboxes_new = list(active_checkboxes)
        active_checkboxes_new.append("cpio")
        self.assertTrue(set(image_fstypes_values_new) == set(active_checkboxes_new), msg="Values after edit for image_fstypes do not match checkboxes selected")

        #resetting to defaults
        self.driver.find_element_by_id("change-image_fstypes-icon").click()
        checkboxes = self.driver.find_elements_by_class_name("fs-checkbox-fstypes")
        for element in checkboxes:
            if (element.get_attribute("checked")):
                element.click()
        for element in checkboxes:
            if (element.get_attribute("value") in active_checkboxes):
                element.click()
        self.driver.find_element_by_id("apply-change-image_fstypes").click()

        #checking image_install_append variable elements
        try:
            self.driver.find_element_by_id("change-image_install-icon").click()
            time.sleep(1)
        except:
            self.fail("Unable to find image_install_append edit button")

        edit_image_install_element = self.driver.find_element_by_id("new-image_install")
        edit_image_install_value = edit_image_install_element.get_attribute("value")
        self.assertTrue((edit_image_install_value == ""), msg="IMAGE_INSTALL_append edit box has unexpected value")
        image_install_placeholder = edit_image_install_element.get_attribute("placeholder")
        self.assertTrue((image_install_placeholder == "Type one or more package names"), msg="IMAGE_INSTALL_append edit box placeholder missing or has unexpected value")

        edit_image_install_element.clear()
        #workaround code; using clear() does not make the interface recognise the text box is now empty, so we need to send a key and then delete it so get the save button to be disabled
        #this does not happen when interacting with the interface manually
        edit_image_install_element.send_keys("a")
        edit_image_install_element.send_keys(Keys.BACKSPACE)
        #end workaround
        edit_image_install_save_button = self.driver.find_element_by_id("apply-change-image_install")
        self.assertFalse((edit_image_install_save_button.is_enabled()), msg="IMAGE_INSTALL_append save changes button still active with empty value; should not be")

        edit_image_install_element.send_keys("package1")
        edit_image_install_save_button.click()
        time.sleep(1)

        image_install_text_new = self.driver.find_element_by_id("image_install").text
        self.assertTrue((image_install_text_new == "package1"), msg="Saved IMAGE_INSTALL_append value does not match input sent")

        try:
            self.driver.find_element_by_id("delete-image_install-icon").click()
            #wait for animation to finish
            time.sleep(4)
        except:
            self.fail("Unable to locate delete button for option IMAGE_INSTALL_append")

        image_install_text_deleted = self.driver.find_element_by_id("image_install").text
        self.assertTrue((image_install_text_deleted == "Not set"), msg="Saved IMAGE_INSTALL_append value was not deleted")
        image_install_delete = self.driver.find_element_by_id("delete-image_install-icon")
        self.assertFalse((image_install_delete.is_displayed()), msg="IMAGE_INSTALL_append delete button still visible with unset value; it should not be")

        #checking package_classes variable elements
        package_classes_text = self.driver.find_element_by_id("package_classes").text
        try:
            self.driver.find_element_by_id("change-package_classes-icon").click()
            time.sleep(1)
        except:
            self.fail("Unable to find package_classes edit button")

        select_package_classes = Select(self.driver.find_element_by_id("package_classes-select"))
        selected_package_classes = select_package_classes.first_selected_option.text
        self.assertTrue((package_classes_text == selected_package_classes), msg="Selected option for package_classes does not match selection detected on page load")

        options_list = []
        for option in select_package_classes.options:
            options_list.append(option.get_attribute('value'))

        packages_list = ["package_deb", "package_ipk", "package_rpm"]
        self.assertTrue((set(options_list) == set(packages_list)), msg = "Unexpected values in dropdown box for package_classes")

        self.driver.find_element_by_id("package_class_1_input").click()
        self.driver.find_element_by_id("package_class_2_input").click()

        self.driver.find_element_by_id("apply-change-package_classes").click()
        time.sleep(1)

        package_classes_text_new = self.driver.find_element_by_id("package_classes").text
        package_classes_text_new = package_classes_text_new.split()

        self.assertTrue((set(package_classes_text_new) == set(packages_list)), msg="PACKAGE_CLASSES after modification does not match selected options")

        #resetting to defaults
        self.driver.find_element_by_id("change-package_classes-icon").click()
        time.sleep(1)
        self.driver.find_element_by_id("package_class_1_input").click()
        self.driver.find_element_by_id("package_class_2_input").click()
        self.driver.find_element_by_id("apply-change-package_classes").click()
        time.sleep(1)

        #adding variables
        add_variable_button = self.driver.find_element_by_id("add-configvar-button")
        self.assertFalse((add_variable_button.is_enabled()), msg="Add variable button active when it shouldn't be")

        self.driver.find_element_by_id("variable").send_keys("variable_name_here")
        self.assertFalse((add_variable_button.is_enabled()), msg="Add variable button active when it shouldn't be")

        self.driver.find_element_by_id("value").send_keys("variable_value_here")
        self.assertTrue((add_variable_button.is_enabled()), msg="Add variable button is not active when it should be")

        add_variable_button.click()
        time.sleep(1)

        #because every variable added gets a unique ID, we will have to reverse engineer the current ID from the variable name
        new_variable = self.driver.find_element_by_xpath("//*[contains(text(), 'variable_name_here')]")
        new_id = new_variable.get_attribute('id')
        id_breakdown = new_id.split('_')
        id_number = id_breakdown[3]
        delete_button_id = 'config_var_trash_' + str(id_number)
        new_variable_text_id = 'config_var_value_'  + str(id_number)
        new_variable_edit_value_id = 'new-config_var_' + str(id_number)
        change_config_form = 'change-config_var-form_' + str(id_number)
        new_variable_save_value = self.driver.find_element_by_xpath("//*[@id='"+change_config_form+"']/div/button[1]")
        new_variable_cancel = self.driver.find_element_by_xpath("//*[@id='"+change_config_form+"']/div/button[2]")
        new_variable_edit_button = self.driver.find_element_by_xpath("//*[@id='configvar-list']/div/dd/i")

        new_variable_edit_button.click()
        new_variable_edit_value = self.driver.find_element_by_id(new_variable_edit_value_id)
        new_variable_edit_value.clear()
        #workaround code; using clear() does not make the interface recognise the text box is now empty, so we need to send a key and then delete it so get the save button to be disabled
        #this does not happen when interacting with the interface manually
        new_variable_edit_value.send_keys("a")
        new_variable_edit_value.send_keys(Keys.BACKSPACE)
        #end workaround
        self.assertFalse((new_variable_save_value.is_enabled()), msg="IMAGE_INSTALL_append save changes button still active with empty value; should not be")
        new_variable_cancel.click()

        self.driver.find_element_by_id(delete_button_id).click()
        #wait for animations to run, otherwise variable is not deleted
        time.sleep(5)

        self.driver.find_element_by_id("variable").send_keys(" /")
        new_variable_error_text = self.driver.find_element_by_id("new-variable-error-message").text
        time.sleep(1)
        self.assertTrue((new_variable_error_text == "A valid variable name can only include letters, numbers, underscores, dashes, and cannot include spaces"), \
                         msg="Error message missing when inputting improper variable name")

        self.driver.find_element_by_id("variable").clear()
        self.driver.find_element_by_id("variable").send_keys("distro")
        time.sleep(1)
        new_variable_error_text = self.driver.find_element_by_id("new-variable-error-message").text
        self.assertTrue((new_variable_error_text == "This variable is already set in this page, edit its value instead"), msg="Error message missing when inputting existing variable name")

        ##############
        #  CASE 1110 #
        ##############
    def test_1110(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)

        self.driver.find_element_by_css_selector("a[href='/toastergui/projects/']").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("selenium-project").click()
        time.sleep(1)
        self.driver.find_element_by_partial_link_text("Layers").click()
        time.sleep(1)

        self.driver.find_element_by_id("search-input-layerstable").send_keys("meta-acer")
        time.sleep(1)
        self.driver.find_element_by_id("search-submit-layerstable").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("meta-acer").click()
        time.sleep(1)

        crumbs_list = self.driver.find_elements_by_class_name("breadcrumb")
        self.assertTrue((("selenium-project" in crumbs_list[0].text) and ("Compatible layers" in crumbs_list[0].text) and ("meta-acer (master)" in crumbs_list[0].text)), \
                       msg="Breadcrumbs have unexpected values")

        self.driver.find_element_by_link_text("selenium-project").click()
        time.sleep(1)
        self.driver.back()
        time.sleep(1)
        self.assertTrue((self.is_text_present("meta-acer")), msg="Returning from breadcrumb failed")

        self.driver.find_element_by_link_text("Compatible layers").click()
        time.sleep(1)
        self.driver.back()
        time.sleep(1)
        self.assertTrue((self.is_text_present("meta-acer")), msg="Returning from breadcrumb failed")

        URL_link = self.driver.find_element_by_xpath("//a[@href='http://github.com/shr-distribution/meta-smartphone/']")
        self.assertTrue((URL_link.is_displayed()), msg="Could not find repository URL external link")
        subdir_link = self.driver.find_element_by_xpath("//a[@href='http://github.com/shr-distribution/meta-smartphone/tree/master/meta-acer']")
        self.assertTrue((subdir_link.is_displayed()), msg="Could not find repository subdirectory external link")

        add_layer_button = self.driver.find_element_by_id("add-remove-layer-btn")
        button_text = add_layer_button.text
        self.assertTrue((button_text == "Add the meta-acer layer to your project"), msg="Button text different than expected")

        try:
            add_layer_button.click()
            time.sleep(1)
        except:
            self.fail(msg="Unable to click on the add layer button")

        title = self.driver.find_element_by_id("title")
        title_text = title.text
        self.assertTrue((title_text == "meta-acer"), msg="Cannot find dependencies pop-up window")
        self.driver.find_element_by_xpath("//*[@id='dependencies-modal-form']/div[3]/button[2]").click()

        self.assertTrue((self.is_text_present("Summary")), msg="Cannot find summary entry")
        self.assertTrue((self.is_text_present("Description")), msg="Cannot find description entry")
        self.assertTrue((self.is_text_present("Repository URL")), msg="Cannot find repository URL entry")
        self.assertTrue((self.is_text_present("Repository subdirectory")), msg="Cannot find repository subdirectory entry")
        self.assertTrue((self.is_text_present("Git revision")), msg="Cannot find git revision entry")
        self.assertTrue((self.is_text_present("Layer dependencies")), msg="Cannot find layer dependencies entry")

        try:
            self.driver.find_element_by_xpath("//a[@href='#recipes']").click()
            time.sleep(1)
        except:
            self.fail(msg="Cannot find recipes tab")

        add_layer_button = self.driver.find_element_by_id("add-remove-layer-btn")
        button_text = add_layer_button.text
        self.assertTrue((button_text == "Add the meta-acer layer to your project to enable these recipes"), msg="Button text different than expected")

        table_head = self.get_table_head_text("recipestable")
        self.assertTrue((set(table_head) == set(["Recipe", "Version", "Description", "Build recipe"])), msg="Recipes table head has unexpected values")

        try:
            self.driver.find_element_by_xpath("//a[@href='#machines']").click()
            time.sleep(1)
        except:
            self.fail(msg="Cannot find machines tab")

        add_layer_button = self.driver.find_element_by_id("add-remove-layer-btn")
        button_text = add_layer_button.text
        self.assertTrue((button_text == "Add the meta-acer layer to your project to enable these machines"), msg="Button text different than expected")

        table_head = self.get_table_head_text("machinestable")
        self.assertTrue((set(table_head) == set(["Machine", "Description", "Select machine"])), msg="Recipes table head has unexpected values")

        try:
            self.driver.find_element_by_xpath("//a[@href='#information']").click()
            time.sleep(1)
        except:
            self.fail(msg="Cannot find layer details tab")

        ##############
        #  CASE 1111 #
        ##############
    def test_1111(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)

        self.driver.find_element_by_css_selector("a[href='/toastergui/projects/']").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("selenium-project").click()
        time.sleep(1)
        #making sure there are no other layers in the project other than the defaults(in particular meta-selftest
        layer = True
        while (layer):
            try:
                delete_button = self.driver.find_element_by_xpath("//*[@id='layers-in-project-list']/li[4]/span")
                delete_button.click()
                self.driver.find_element_by_link_text("Configuration").click()
            except:
                layer = False
        self.driver.find_element_by_partial_link_text("Layers").click()
        time.sleep(1)

        self.driver.find_element_by_id("search-input-layerstable").send_keys("meta-acer")
        time.sleep(1)
        self.driver.find_element_by_id("search-submit-layerstable").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("meta-acer").click()
        time.sleep(1)

        try:
            self.driver.find_element_by_xpath("//a[@href='#recipes']").click()
            time.sleep(1)
        except:
            self.fail(msg="Cannot find recipes tab")
        build_recipe_button = self.driver.find_element_by_xpath("//table[@id='recipestable']/tbody/tr/td[4]/button")
        self.assertFalse((build_recipe_button.is_enabled()), msg="Build recipe button active before layer was added to project")

        try:
            self.driver.find_element_by_xpath("//a[@href='#machines']").click()
            time.sleep(1)
        except:
            self.fail(msg="Cannot find machines tab")
        select_machine_button = self.driver.find_element_by_xpath("//table[@id='machinestable']/tbody/tr/td[3]/a")
        self.assertTrue((select_machine_button.get_attribute('disabled')), msg="Select machine button active before layer was added to project")

        try:
            self.driver.find_element_by_xpath("//a[@href='#information']").click()
            time.sleep(1)
        except:
            self.fail(msg="Cannot find layers details tab")

        add_layer_button = self.driver.find_element_by_id("add-remove-layer-btn")
        try:
            add_layer_button.click()
            time.sleep(1)
        except:
            self.fail(msg="Unable to click on the add layer button")

        try:
            self.driver.find_element_by_xpath("//*[@id='dependencies-modal-form']/div[3]/button[1]").click()
        except:
            self.fail(msg="Unable to click on the add layers button in the dependencies pop-up window")

        time.sleep(5)
        add_layer_button = self.driver.find_element_by_id("add-remove-layer-btn")
        button_text = add_layer_button.text
        self.assertTrue((button_text == "Remove the meta-acer layer from your project"), msg="Button text different than expected")

        alert = self.driver.find_element_by_id("alert-area")
        alert_message = alert.text
        self.assertTrue(("You have added 3 layers to your project: meta-acer and its dependencies meta-android, meta-oe" in alert_message), msg="Alert message not found or text wrong")

        try:
            self.driver.find_element_by_xpath("//a[@href='#recipes']").click()
            time.sleep(1)
        except:
            self.fail(msg="Cannot find recipes tab")
        build_recipe_button = self.driver.find_element_by_xpath("//table[@id='recipestable']/tbody/tr/td[4]/button")
        self.assertTrue((build_recipe_button.is_enabled()), msg="Build recipe button not active after layer was added to project")

        try:
            self.driver.find_element_by_xpath("//a[@href='#machines']").click()
            time.sleep(1)
        except:
            self.fail(msg="Cannot find machines tab")
        select_machine_button = self.driver.find_element_by_xpath("//table[@id='machinestable']/tbody/tr/td[3]/a")
        self.assertFalse((select_machine_button.get_attribute('disabled')), msg="Select machine button not active after layer was added to project")
        select_machine_button.click()
        time.sleep(2)
        machine_text = self.driver.find_element_by_id("project-machine-name").text
        self.assertTrue((machine_text == "a500"), "Machine not changed after using 'Select machine' button")

        ##############
        #  CASE 1112 #
        ##############
    def test_1112(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)

        self.driver.find_element_by_css_selector("a[href='/toastergui/projects/']").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("selenium-project").click()
        time.sleep(1)
        self.driver.find_element_by_partial_link_text("Import layer").click()
        time.sleep(1)

        import_button = self.driver.find_element_by_id("import-and-add-btn")
        self.assertFalse((import_button.is_enabled()), msg="Import layer button active before all requirement are filled out; it should not be")

        try:
            self.driver.find_element_by_id("import-layer-name").send_keys("meta-selftest")
        except:
            self.fail(msg="Cannot find layer name text box")

        try:
            self.driver.find_element_by_id("layer-git-repo-url").send_keys("git://git.yoctoproject.org/poky")
        except:
            self.fail(msg="Cannot find git repo text box")

        try:
            self.driver.find_element_by_id("layer-subdir").send_keys("meta-selftest")
        except:
            self.fail(msg="Cannot find repo subdirectory text box")

        try:
            self.driver.find_element_by_id("layer-git-ref").send_keys("master")
        except:
            self.fail(msg="Cannot find git revision text box")

        add_dependency_button = self.driver.find_element_by_id("add-layer-dependency-btn")
        self.assertTrue((add_dependency_button.get_attribute("disabled")), msg="Add dependency button active before layer text box is filled out")

        try:
            self.driver.find_element_by_id("layer-dependency").send_keys("meta-acer")
            self.driver.find_element_by_id("layer-dependency").send_keys(Keys.ENTER)
            time.sleep(1)
        except:
            self.fail(msg="Cannot find layer dependency text box")

        self.assertFalse((add_dependency_button.get_attribute("disabled")), msg="Add dependency button not active after layer text box filled out")
        add_dependency_button.click()

        try:
            self.driver.find_element_by_xpath("//ul[@id='layer-deps-list']/li[2]/span").click()
            time.sleep(1)
        except:
            self.fail(msg="Unable to delete added dependency layer")

        default_dependency = self.driver.find_element_by_xpath("//ul[@id='layer-deps-list']/li/a")
        self.assertTrue((default_dependency.text == "openembedded-core"), msg="Default layer dependency has unexpected value")

        delete_default_dependency = self.driver.find_element_by_xpath("//ul[@id='layer-deps-list']/li/span")
        self.assertTrue((delete_default_dependency.is_enabled()), msg="Delete button for default dependency either missing or inactive")

        self.assertTrue((import_button.is_enabled()), msg="Import layer button not active after all requirement are filled out; it should be")
        import_button.click()
        time.sleep(1)

        self.assertTrue((self.is_text_present("meta-selftest")), msg="Unable to verify layer was added to project")

        ##############
        #  CASE 1113 #
        ##############
    def test_1113(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)

        self.driver.find_element_by_css_selector("a[href='/toastergui/projects/']").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("selenium-project").click()
        time.sleep(1)
        self.driver.find_element_by_partial_link_text("Layers").click()
        time.sleep(1)

        self.driver.find_element_by_id("search-input-layerstable").send_keys("meta-selftest")
        self.driver.find_element_by_id("search-submit-layerstable").click()

        self.driver.find_element_by_link_text("meta-selftest").click()

        try:
            self.driver.find_element_by_xpath("//a[@href='#recipes']").click()
            time.sleep(1)
        except:
            self.fail(msg="Cannot find recipes tab")
        no_recipe_message = self.driver.find_element_by_id("no-recipes-yet")
        print no_recipe_message.text
        self.assertTrue(no_recipe_message, msg="Unable to find notification of missing recipes")

        try:
            self.driver.find_element_by_xpath("//a[@href='#machines']").click()
            time.sleep(1)
        except:
            self.fail(msg="Cannot find machines tab")
        no_machine_message = self.driver.find_element_by_id("no-machines-yet")
        print no_machine_message.text
        self.assertTrue(no_machine_message, msg="Unable to find notification of missing machines")

        try:
            self.driver.find_element_by_xpath("//a[@href='#information']").click()
            time.sleep(1)
        except:
            self.fail(msg="Cannot find layers details tab")

        add_layer_button = self.driver.find_element_by_id("add-remove-layer-btn")
        try:
            add_layer_button.click()
            time.sleep(1)
        except:
            self.fail(msg="Unable to click on the add layer button")

        add_layer_button = self.driver.find_element_by_id("add-remove-layer-btn")
        button_text = add_layer_button.text
        self.assertTrue((button_text == "Remove the meta-selftest layer from your project"), msg="Button text different than expected")

        alert = self.driver.find_element_by_id("alert-area")
        alert_message = alert.text
        self.assertTrue(("You have added 1 layer to your project: meta-selftest" in alert_message), msg="Alert message not found or text wrong")

        add_layer_button.click()

        self.assertTrue((self.is_text_present("Summary")), msg="Cannot find summary entry")
        self.assertTrue((self.is_text_present("Description")), msg="Cannot find description entry")
        self.assertTrue((self.is_text_present("Repository URL")), msg="Cannot find repository URL entry")
        self.assertTrue((self.is_text_present("Repository subdirectory")), msg="Cannot find repository subdirectory entry")
        self.assertTrue((self.is_text_present("Git revision")), msg="Cannot find git revision entry")
        self.assertTrue((self.is_text_present("Layer dependencies")), msg="Cannot find layer dependencies entry") 

        edit_repo_button = self.driver.find_element_by_xpath("//div[@id='information']/dl/dd/i")
        self.assertTrue(edit_repo_button.is_displayed(), msg="Unable to find edit repository URL button")
        edit_repo_button.click()
        edit_repo_text = self.driver.find_element_by_xpath("//form[@id='change-repo-form']/div/input")
        self.assertTrue(edit_repo_text.is_displayed(), msg="Unable to find edit repository text box")
        edit_repo_text.clear()
        edit_repo_text.send_keys("new_repo_here")
        try:
            self.driver.find_element_by_xpath("//form[@id='change-repo-form']/div/button").click()
            time.sleep(1)
        except:
            self.Fail(msg="Unable to save new repo")
        repo_text = self.driver.find_element_by_xpath("//div[@id='information']/dl/dd[1]/span")
        self.assertTrue(repo_text.text == "new_repo_here", msg="repo value not updated after change")

        edit_subdir_button = self.driver.find_element_by_id("change-subdir")
        self.assertTrue(edit_subdir_button.is_displayed(), msg="Unable to find change subdirectory button")
        edit_subdir_button.click()
        edit_subdir_text = self.driver.find_element_by_xpath("//form[@id='change-subdir-form']/div/input")
        edit_subdir_text.clear()
        edit_subdir_text.send_keys("new-subdir")
        try:
            self.driver.find_element_by_xpath("//form[@id='change-subdir-form']/div/button").click()
            time.sleep(1)
        except:
            self.Fail(msg="Unable to save new subdir")
        subdir_text = self.driver.find_element_by_xpath("//div[@id='information']/dl/dd[2]/span[2]")
        self.assertTrue(subdir_text.text == "new-subdir", msg="subdir value not updated after change")
        delete_subdir_button = self.driver.find_element_by_xpath("//div[@id='information']/dl/dd[2]/span[3]")
        self.assertTrue(delete_subdir_button.is_displayed(), msg="Unable to find delete subdirectory button")
        delete_subdir_button.click()
        time.sleep(2)
        subdir_text = self.driver.find_element_by_xpath("//div[@id='information']/dl/dd[2]/span[1]")
        self.assertTrue(subdir_text.text == "Not set", msg="subdir value not deleted after delete button was pressed")
        edit_revision_button = self.driver.find_element_by_xpath("//div[@id='information']/dl/dd[3]/i")
        self.assertTrue(edit_revision_button.is_displayed(), msg="Unable to find edit revision button")
        edit_revision_button.click()
        edit_revision_text = self.driver.find_element_by_xpath("//div[@id='information']/dl/dd[3]/form/div/input")
        edit_revision_text.clear()
        edit_revision_text.send_keys("master")
        try:
            self.driver.find_element_by_xpath("//div[@id='information']/dl/dd[3]/form/div/button").click()
            time.sleep(1)
        except:
            self.Fail(msg="Unable to save new revision")
        revision_text = self.driver.find_element_by_xpath("//div[@id='information']/dl/dd[3]/span")
        self.assertTrue(revision_text.text == "master", msg="revision value not updated after change")
        delete_dep_button = self.driver.find_element_by_xpath("//ul[@id='layer-deps-list']/li/span")
        self.assertTrue(delete_dep_button.is_displayed(), msg="Unable to find delete dependency button")
        add_dep_text = self.driver.find_element_by_id("layer-dep-input")
        self.assertTrue(add_dep_text.is_displayed(), msg="Unable to find add dependency text box")
        add_dep_button = self.driver.find_element_by_id("add-layer-dependency-btn")
        self.assertTrue(add_dep_button.is_displayed(), msg="Unable to find add dependency button")

        #we need to find a better way to ID the next few elements; maybe ask DEV to add IDs?
        edit_summary_button = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[4]/dl/dd[1]/i")
        self.assertTrue(edit_summary_button.is_displayed(), msg="Unable to find edit summary button")
        edit_desc_button = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[4]/dl/dd[2]/i")
        self.assertTrue(edit_desc_button.is_displayed(), msg="Unable to find edit description button")

        edit_summary_button.click()
        time.sleep(1)
        edit_summary_text = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[4]/dl/dd[1]/form/textarea")
        self.assertTrue(edit_summary_text.is_displayed(), msg="Unable to find edit summary text area")
        edit_summary_text.send_keys("test summary here")
        edit_summary_save = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[4]/dl/dd[1]/form/button")
        try:
            edit_summary_save.click()
            time.sleep(1)
        except:
            self.Fail(msg="Unable to save new summary")
        delete_summary = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[4]/dl/dd[1]/span[3]")
        try:
            delete_summary.click()
            time.sleep(2)
        except:
            self.Fail("Unable to delete custom summary")

        edit_desc_button.click()
        time.sleep(1)
        edit_desc_text = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[4]/dl/dd[2]/form/textarea")
        self.assertTrue(edit_desc_text.is_displayed(), msg="Unable to find edit description text area")
        edit_desc_text.send_keys("test description here")
        edit_desc_save = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[4]/dl/dd[2]/form/button")
        try:
            edit_desc_save.click()
            time.sleep(1)
        except:
            self.Fail(msg="Unable to save new description")
        delete_desc = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[4]/dl/dd[2]/span[3]")
        try:
            delete_desc.click()
            time.sleep(2)
        except:
            self.Fail("Unable to delete custom description")

        ##############
        #  CASE 1398 #
        ##############
    def test_1398(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)

        self.driver.find_element_by_css_selector("a[href='/toastergui/projects/']").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("selenium-project").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Layers").click()
        time.sleep(1)

        self.driver.find_element_by_id("search-input-layerstable").send_keys("meta-acer")
        self.driver.find_element_by_id("search-submit-layerstable").click()
        time.sleep(2)

        self.driver.find_element_by_link_text("meta-acer").click()
        time.sleep(1)

        self.driver.find_element_by_id("add-remove-layer-btn").click()
        time.sleep(1)

        try:
            self.driver.find_element_by_xpath("//*[@id='dependencies-modal-form']/div[3]/button[1]").click()
            time.sleep(2)
        except:
            self.fail(msg="Unable to click on the add layers button in the dependencies pop-up window")

        self.driver.find_element_by_link_text("Compatible layers").click()
        time.sleep(1)

        self.driver.find_element_by_id("search-input-layerstable").send_keys("meta-oe")
        self.driver.find_element_by_id("search-submit-layerstable").click()
        time.sleep(2)

        self.driver.find_element_by_link_text("meta-oe").click()
        time.sleep(1)

        self.driver.find_element_by_id("add-remove-layer-btn").click()
        time.sleep(1)

        self.driver.find_element_by_link_text("selenium-project").click()
        time.sleep(1)

        self.driver.find_element_by_id("build-input").send_keys("core-image-minimal")
        time.sleep(1)
        self.driver.find_element_by_id("build-button").click()
        time.sleep(1)

        try:
            self.driver.find_element_by_xpath("//div[@class='progress']").is_displayed()
        except:
            print "Unable to start new build"
            self.fail(msg="Unable to start new build")
        count = 1
        self.timeout = 20
        failflag = False
        try:
            self.driver.refresh()
            time.sleep(1)
            print "First check starting"
            while (self.driver.find_element_by_xpath("//div[@class='progress']").is_displayed()):
                #print "Looking for build in progress"
                print 'Build running for '+str(count)+' minutes'
                count += 1
                if (count > self.timeout):
                    failflag = True
                    print 'Build took longer than expected to complete; Failing due to possible build stuck.'
                    self.fail()
                time.sleep(60)
                self.driver.refresh()
        except:
           try:
                if failflag:
                    self.fail(msg="Build took longer than expected to complete; Failing due to possible build stuck.")
                print "Looking for failed build"
                self.driver.find_element_by_xpath("//div[@class='alert build-result alert-error']").is_displayed()
           except:
                if failflag:
                    self.fail(msg="Build took longer than expected to complete; Failing due to possible build stuck.")
                self.fail(msg="Could not find expected failed build")

        self.driver.find_element_by_link_text("core-image-minimal").click()
        time.sleep(1)

        download_log = self.driver.find_elements_by_xpath("//*[contains(text(), 'Download build log')]")
        self.assertTrue(download_log.is_displayed(), msg="Cannot find download log button")

        #resetting to defaults
        self.driver.find_element_by_link_text("selenium-project").click()
        layer = True
        while (layer):
            try:
                delete_button = self.driver.find_element_by_xpath("//*[@id='layers-in-project-list']/li[4]/span")
                delete_button.click()
                self.driver.find_element_by_link_text("Configuration").click()
            except:
                layer = False

        ##############
        #  CASE 1408 #
        ##############
    def test_1408(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        time.sleep(2)

        try:
            self.driver.find_element_by_xpath("//i[@class='icon-ok-sign success']").click()
            time.sleep(1)
        except:
            self.fail(msg="Unable to find successful build")

        self.driver.find_element_by_link_text("Configuration").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("BitBake variables").click()
        time.sleep(1)

        filtered = self.driver.find_element_by_xpath("//i[@class='icon-filter filtered']")
        self.assertTrue(filtered.is_enabled() ,msg="Could not find filtered column")

        filtered_column = self.get_table_column_text("class", "description")
        if '' in filtered_column:
            self.fail(msg="At least one element in the description column is blank; filter failed!")

        ##############
        #  CASE 1409 #
        ##############
    def test_1409(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        time.sleep(2)

        try:
            self.driver.find_element_by_xpath("//i[@class='icon-ok-sign success']").click()
            time.sleep(1)
        except:
            self.fail(msg="Unable to find successful build")

        self.driver.find_element_by_link_text("Recipes").click()
        time.sleep(1)
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(1)
        self.driver.find_element_by_id("depends_on").click()
        time.sleep(1)
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(1)

        self.driver.find_element_by_xpath("//table[@id='otable']/tbody/tr[1]/td[3]/a").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("/html/body/div[5]/div[2]/ul/li[1]/a").click()
        time.sleep(1)

        self.assertTrue(self.is_text_present("License"),msg="Could not confirm we reached a recipe page")

        ##############
        #  CASE 1410 #
        ##############
    def test_1410(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)

        self.driver.find_element_by_css_selector("a[href='/toastergui/projects/']").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("selenium-project").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Image recipes").click()
        time.sleep(1)

        self.driver.find_element_by_id("edit-columns-button").click()
        self.driver.find_element_by_id("checkbox-recipe-file").click()
        self.driver.find_element_by_id("edit-columns-button").click()

        #saving current windows element
        main_window = self.driver.current_window_handle
        #open external link
        link_button = self.driver.find_element_by_xpath("//table[@id='imagerecipestable']/tbody/tr[1]/td[4]/a")
        try:
            #open link in new tab instead of new window
            link_button.send_keys(Keys.CONTROL + Keys.RETURN)
            time.sleep(1)
        except:
            self.fail(msg="Could not click on external link button")

        #switch to new opened tab
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
        self.assertTrue(self.is_text_present("Angstrom-distribution"), msg="Unable to confirm new tab is the expected one")
        #close new tab
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
        time.sleep(1)

        self.driver.find_element_by_link_text("Software recipes").click()
        time.sleep(1)
        self.driver.find_element_by_id("edit-columns-button").click()
        self.driver.find_element_by_id("checkbox-recipe-file").click()
        self.driver.find_element_by_id("edit-columns-button").click()

        #saving current windows element
        main_window = self.driver.current_window_handle
        #open external link
        link_button = self.driver.find_element_by_xpath("//table[@id='softwarerecipestable']/tbody/tr[1]/td[4]/a")
        try:
            #open link in new tab instead of new window
            link_button.send_keys(Keys.CONTROL + Keys.RETURN)
            time.sleep(1)
        except:
            self.fail(msg="Could not click on external link button")

        #switch to new opened tab
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
        self.assertTrue(self.is_text_present("flihp"), msg="Unable to confirm new tab is the expected one")
        #close new tab
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

        ##############
        #  CASE 1411 #
        ##############
    def test_1411(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        time.sleep(2)

        try:
            self.driver.find_element_by_xpath("//i[@class='icon-ok-sign success']").click()
            time.sleep(1)
        except:
            self.fail(msg="Unable to find successful build")

        self.driver.find_element_by_link_text("Packages").click()
        time.sleep(1)

        self.driver.find_element_by_link_text("Size").click()
        sizes_list = self.get_table_column_text("class", "size sizecol")
        if '' in sizes_list:
            self.fail(msg="At least one element in the sizes column is blank")

        ##############
        #  CASE 1140 #
        ##############
    def test_1140(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get("http://localhost:8000/admin/")
        time.sleep(2)

        self.driver.find_element_by_id("id_username").send_keys("toaster_admin")
        time.sleep(1)
        self.driver.find_element_by_id("id_password").send_keys("qwe123")
        time.sleep(1)
        self.driver.find_element_by_xpath("//input[@value='Log in']").click()
        time.sleep(1)

        self.driver.find_element_by_link_text("Build environments").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("BuildEnvironment object").click()
        time.sleep(1)

        sourcedir = self.driver.find_element_by_id("id_sourcedir").get_attribute('value')
        builddir = self.driver.find_element_by_id("id_builddir").get_attribute('value')

        builddir2 = str(builddir) + "2"

        self.driver.find_element_by_link_text("Build environments").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Add build environment").click()
        time.sleep(1)
    
        self.driver.find_element_by_id("id_address").send_keys("2")
        self.driver.find_element_by_id("id_sourcedir").send_keys(str(sourcedir))
        self.driver.find_element_by_id("id_builddir").send_keys(str(builddir2))
       
        options = Select(self.driver.find_element_by_id("id_betype"))
        options.select_by_visible_text("local")

        self.driver.find_element_by_xpath("//input[@value='Save']").click()
        time.sleep(2)

        self.driver.get(self.base_url)
        self.driver.find_element_by_css_selector("a[href='/toastergui/projects/']").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("selenium-project").click()
        time.sleep(1)

        self.driver.find_element_by_id("build-input").send_keys("core-image-sato")
        time.sleep(1)
        self.driver.find_element_by_id("build-button").click()
        time.sleep(2)

        self.driver.find_element_by_id("build-input").send_keys("core-image-minimal")
        time.sleep(1)
        self.driver.find_element_by_id("build-button").click()
        time.sleep(2)

        progress_list = self.driver.find_elements_by_xpath("//div[@class='progress']")
        self.assertTrue(len(progress_list) > 1,msg="Could not find 2 progress bars visible")

        count = 1
        self.timeout = 340
        failflag = False
        try:
            self.driver.refresh()
            time.sleep(1)
            while (self.driver.find_element_by_xpath("//div[@class='progress']").is_displayed()):
                print 'Build running for '+str(count)+' minutes'
                count += 5
                if (count > self.timeout):
                    failflag = True
                    print 'Build took longer than expected to complete; Failing due to possible build stuck.'
                    self.fail()
                time.sleep(300)
                self.driver.refresh()
        except:
            if failflag:
                self.fail(msg="Build took longer than expected to complete; Failing due to possible build stuck.")
            print "Looking for successful builds"
            build_list = self.driver.find_elements_by_xpath("//div[@class='alert build-result alert-success']")
            self.assertTrue((len(build_list) > 1), msg="Could not find successful builds")
