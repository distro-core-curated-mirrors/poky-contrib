#! /usr/bin/env python3
#
# BitBake Toaster functional tests implementation
#
# Copyright (C) 2017 Intel Corporation
#
# SPDX-License-Identifier: GPL-2.0-only
#

import os
import subprocess
import signal
import time
import re

from tests.browser.selenium_helpers_base import SeleniumTestCaseBase
from tests.builds.buildtest import load_build_environment
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumFunctionalTestCase(SeleniumTestCaseBase):
    wait_toaster_time = 5

    @classmethod
    def setUpClass(cls):
        # So that the buildinfo helper uses the test database'
        if os.environ.get('DJANGO_SETTINGS_MODULE', '') != \
            'toastermain.settings_test':
            raise RuntimeError("Please initialise django with the tests settings:  " \
                "DJANGO_SETTINGS_MODULE='toastermain.settings_test'")

        load_build_environment()

        # start toaster
        cmd = "bash -c 'source toaster start'"
        p = subprocess.Popen(
            cmd,
            cwd=os.environ.get("BUILDDIR"),
            shell=True)
        if p.wait() != 0:
            raise RuntimeError("Can't initialize toaster")

        super(SeleniumFunctionalTestCase, cls).setUpClass()
        cls.live_server_url = 'http://localhost:8000/'

    @classmethod
    def tearDownClass(cls):
        super(SeleniumFunctionalTestCase, cls).tearDownClass()

        # XXX: source toaster stop gets blocked, to review why?
        # from now send SIGTERM by hand
        time.sleep(cls.wait_toaster_time)
        builddir = os.environ.get("BUILDDIR")

        with open(os.path.join(builddir, '.toastermain.pid'), 'r') as f:
            toastermain_pid = int(f.read())
            os.kill(toastermain_pid, signal.SIGTERM)
        with open(os.path.join(builddir, '.runbuilds.pid'), 'r') as f:
            runbuilds_pid = int(f.read())
            os.kill(runbuilds_pid, signal.SIGTERM)


    def get_URL(self):
         rc=self.get_page_source()
         project_url=re.search("(projectPageUrl\s:\s\")(.*)(\",)",rc)
         return project_url.group(2)


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
    def create_new_project(self, project_name):
        """
        Assume there're multiple suitable "find_element_by_link_text".
        In this circumstance we need to specify "table".
        """
        self.get('')
        self.driver.find_element_by_id("new-project-button").click()
        self.driver.find_element_by_id("new-project-name").send_keys(project_name)
        self.driver.find_element_by_id('projectversion').click()
        self.driver.find_element_by_id("create-project-button").click()
        time.sleep(20)
    def build_recipie(self,recipie_name,project_name):
        #self.get('')
        self.driver.find_element_by_id("build-input").click()
        time.sleep(10)
        self.driver.find_element_by_id("build-input").send_keys(recipie_name)
        time.sleep(5)
        self.driver.find_element_by_id("build-button").click()
        time.sleep(5)
        try:
            WebDriverWait(self.driver,700).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="latest-builds"]//span[@class="rebuild-btn alert-link danger pull-right"]')))
            time.sleep(5)
            self.fail(msg=" Fail Build is not successful for test case  {} ".format(project_name))
            #logger.info("Fail Build is not successful for test case  {} ".format(project_name))
        except:
            WebDriverWait(self.driver, 8000).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="latest-builds"]//span[@class="rebuild-btn alert-link info pull-right"]')))
            time.sleep(5)

    def search_element(self, search_table_name,search_submit_button,serach_key):
        self.driver.find_element_by_id(search_table_name).click()
        self.driver.find_element_by_id(search_table_name).send_keys(serach_key)
        self.driver.find_element_by_id(search_submit_button).click()
        time.sleep(20)
    def edit_specicific_checkbox(self,checkbox_name):
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(5)
        self.driver.find_element_by_id(checkbox_name).click()
        time.sleep(5)
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(5)

