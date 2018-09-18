#!/usr/bin/python
#
# DESCRIPTION
# This is script has baseclass and contains class selenium-based functions.
#
import ConfigParser
import logging
import os
import platform
import sys
import time
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from Utility import LogResults
from Utility import mkdir_p

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
        self.log_tmp_dir = os.path.abspath(sys.path[0]) + os.sep + 'log' + os.sep + 'tmp'
        try:
            mkdir_p(self.log_tmp_dir)
        except OSError :
            logging.error("%(asctime)s Cannot create tmp dir under log, please check your privilege")
        self.setup_browser()

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

    def save_screenshot(self,  **log_args):
        types = [log_args.get('screenshot_type')]
        if types == [None]:
            types = ['native', 'selenium']
        add_name = log_args.get('append_name')
        if not add_name:
            add_name = '-'
        sub_dir = log_args.get('log_sub_dir')
        if not sub_dir:
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
    def find_element_by_text(self, string):
        return self.driver.find_element_by_xpath("//*[text()='" + string + "']")

    def find_elements_by_text(self, string):
        return self.driver.find_elements_by_xpath("//*[text()='" + string + "']")

    def find_element_by_text_in_table(self, table_id, text_string):
        try:
            table_element = self.get_table_element(table_id)
            element = table_element.find_element_by_xpath("//*[text()='" + text_string + "']")
        except NoSuchElementException as e:
            print('no element found')
            raise
        return element

    def find_element_by_link_text_in_table(self, table_id, link_text):
        try:
            table_element = self.get_table_element(table_id)
            element = table_element.find_element_by_link_text(link_text)
        except NoSuchElementException as e:
            print('no element found')
            raise
        return element


    def find_elements_by_link_text_in_table(self, table_id, link_text):
        try:
            table_element = self.get_table_element(table_id)
            element_list = table_element.find_elements_by_link_text(link_text)
        except NoSuchElementException as e:
            print('no element found')
            raise
        return element_list

    def find_element_by_partial_link_text_in_table(self, table_id, link_text):
        try:
            table_element = self.get_table_element(table_id)
            element = table_element.find_element_by_partial_link_text(link_text)
            return element
        except NoSuchElementException as e:
            print('no element found')
            raise

    def find_elements_by_partial_link_text_in_table(self, table_id, link_text):
        try:
            table_element = self.get_table_element(table_id)
            element_list = table_element.find_elements_by_partial_link_text(link_text)
            return element_list
        except NoSuchElementException as e:
            print('no element found')
            raise

    def find_element_by_xpath_in_table(self, table_id, xpath):
        try:
            table_element = self.get_table_element(table_id)
            element = table_element.find_element_by_xpath(xpath)
        except NoSuchElementException as e:
            print('no element found')
            raise
        return element

    def find_elements_by_xpath_in_table(self, table_id, xpath):
        try:
            table_element = self.get_table_element(table_id)
            element_list = table_element.find_elements_by_xpath(xpath)
        except NoSuchElementException as e:
            print('no elements found')
            raise
        return element_list

    def shortest_xpath(self, pname, pvalue):
        return "//*[@" + pname + "='" + pvalue + "']"

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
        if table_id:
            thead_xpath = "//*[@id='" + table_id[0] + "']//thead//th[text()]"
            elements = self.driver.find_elements_by_xpath(thead_xpath)
            c_list = []
            for element in elements:
                if element.text:
                    c_list.append(element.text)
            return c_list
        else:
            return self.driver.find_element_by_xpath("//*/table/thead").text

    def get_table_element(self, table_id, *coordinate):
        if len(coordinate) == 0:
            element_xpath = "//*[@id='" + table_id + "']"
            try:
                element = self.driver.find_element_by_xpath(element_xpath)
            except NoSuchElementException as e:
                raise
            return element
        row = coordinate[0]

        if len(coordinate) == 1:
            element_xpath = "//*[@id='" + table_id + "']/tbody/tr[" + str(row) + "]"
            try:
                element = self.driver.find_element_by_xpath(element_xpath)
            except NoSuchElementException as e:
                return False
            return element
        column = coordinate[1]

        element_xpath = "//*[@id='" + table_id + "']/tbody/tr[" + str(row) + "]/td[" + str(column) + "]"
        try:
            element = self.driver.find_element_by_xpath(element_xpath)
        except NoSuchElementException as e:
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
            print(Lists[row-1][0])
            row = row + 1
        return Lists

    def is_text_present (self, patterns):
        for pattern in patterns:
            if str(pattern) not in self.driver.page_source:
                print('Text "'+pattern+'" is missing')
                return False
        return True

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(how, what)
        except NoSuchElementException as e:
            print('Could not find element '+str(what)+' by ' + str(how))
            return False
        return True

    def get_case_number(self):
        funcname = sys._getframe(1).f_code.co_name
        caseno_str = funcname.strip('test_')
        try:
            caseno = int(caseno_str)
        except ValueError:
            print("get case number error! please check if func name is test_xxx")
            return False
        return caseno

    def tearDown(self):
        self.log.info(' END: CASE %s log \n\n' % str(self.case_no))
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)