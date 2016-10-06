import sys
import os
import logging
import unittest
import time
import platform
import shutil, argparse, configparser, json
import errno
import re

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import strftime, gmtime
from selenium.common.exceptions import NoSuchElementException



sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
    '../', 'tests', 'browser')) # XXX: Test tool should insert the path




if not 'TOASTER_TESTS_BROWSER' in os.environ:
    os.environ['TOASTER_TESTS_BROWSER'] = 'firefox'
if not 'TOASTER_URL' in os.environ:
    os.environ['TOASTER_URL'] = 'http://localhost:8000'


logging.basicConfig()


from selenium_helpers_base import SeleniumTestCaseBase


#class SeleniumTestCaseBaseHelper(unittest.TestCase):

class ToasterFunctionalTests(SeleniumTestCaseBase):
    _url = os.environ['TOASTER_URL']
    _logger = logging.getLogger()
    _logger.setLevel(logging.INFO)


    @classmethod
    def setUpClass(cls):
        SeleniumTestCaseBase.setUpClass()
        cls.log = cls.logger_create()

    def mkdir_p(self, dir):
        try:
            os.makedirs(dir)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(dir):
                pass
            else:
                raise



    def setup_browser(self, *browser_path):
        self.browser = eval(self.parser.get('toaster_test_' + self.target_suite, 'test_browser'))
        print(self.browser)
        if self.browser == "firefox":
            driver = webdriver.Firefox()
        elif self.browser == "chrome":
            driver = webdriver.Chrome()
        elif self.browser == "ie":
            driver = webdriver.Ie()
        else:
            driver = None
            print("unrecognized browser type, please check")
        self.driver = driver
        self.driver.implicitly_wait(30)
        return self.driver



    def setUp(self):

        self.screenshot_sequence = 1
        self.verificationErrors = []
        self.accept_next_alert = True
        self.host_os = platform.system().lower()
        if os.getenv('TOASTER_SUITE'):
            self.target_suite = os.getenv('TOASTER_SUITE')
        else:
            self.target_suite = self.host_os

        self.parser = configparser.ConfigParser()
        self.parser.read('toaster_test.cfg')
        self.base_url = eval(self.parser.get('toaster_test_' + self.target_suite, 'toaster_url'))

        # create log dir . Currently , we put log files in log/tmp. After all
        # test cases are done, move them to log/$datetime dir
        self.log_tmp_dir = os.path.abspath(sys.path[0]) + os.sep + 'log' + os.sep + 'tmp'
        try:
            self.mkdir_p(self.log_tmp_dir)
        except OSError :
            logging.error("%(asctime)s Cannot create tmp dir under log, please check your privilege")
        # self.log = self.logger_create()
        # driver setup
        #self.setup_browser()



    def get_case_number(self):
        """
        what case are we running now
        """
        funcname = sys._getframe(1).f_code.co_name
        caseno_str = funcname.strip('test_')
        try:
            caseno = int(caseno_str)
        except ValueError:
            print("get case number error! please check if func name is test_xxx")
            return False
        return caseno


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




    def get_table_element(self, table_id, *coordinate):
        if len(coordinate) == 0:
            #return whole-table element
            element_xpath = "//*[@id='" + table_id + "']"
            try:
                element = self.driver.find_element_by_xpath(element_xpath)
            except NoSuchElementException as e:
                raise
            return element
        row = coordinate[0]

        if len(coordinate) == 1:
            #return whole-row element
            element_xpath = "//*[@id='" + table_id + "']/tbody/tr[" + str(row) + "]"
            try:
                element = self.driver.find_element_by_xpath(element_xpath)
            except NoSuchElementException as e:
                return False
            return element
        #now we are looking for an element with specified X and Y
        column = coordinate[1]

        element_xpath = "//*[@id='" + table_id + "']/tbody/tr[" + str(row) + "]/td[" + str(column) + "]"
        try:
            element = self.driver.find_element_by_xpath(element_xpath)
        except NoSuchElementException as e:
            return False
        return element





    def find_element_by_link_text_in_table(self, table_id, link_text):
        """
        Assume there're multiple suitable "find_element_by_link_text".
        In this circumstance we need to specify "table".
        """
        try:
            table_element = self.get_table_element(table_id)
            element = table_element.find_element_by_link_text(link_text)
        except NoSuchElementException as e:
            print('no element found')
            raise
        return element

    def get_URL(self):
         rc=self.get_page_source()
         project_url=re.search("(projectPageUrl\s:\s\")(.*)(\",)",rc)
         return project_url.group(2)

         

