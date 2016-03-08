# Toaster setup test case
#
# Copyright (C) 2015-2016 Intel Corporation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from toaster.tests.base import ToasterTestCase

class ToasterSetupTestCase(ToasterTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.close()

    def is_text_present (self, patterns):
        for pattern in patterns:
            if str(pattern) not in self.driver.page_source:
                self.logger.debug(pattern)
                return False
        return True

    def test_setupToaster(self):
        self.driver.maximize_window()
        self.driver.get(self.opts.toaster_url)
        try:
            self.driver.find_element_by_css_selector("a[href='/toastergui/projects/']").click()
            self.driver.find_element_by_link_text("selenium-project").click()
        except:
            self.driver.find_element_by_id("new-project-button").click()
            time.sleep(5)
            self.driver.find_element_by_id("new-project-name").send_keys("selenium-project")
            self.driver.find_element_by_id("create-project-button").click()

        time.sleep(5)

        #queue up a core-image-minimal
        self.driver.find_element_by_id("build-input").send_keys("core-image-minimal")
        self.driver.find_element_by_id("build-button").click()
        time.sleep(5)
        #queue up a core-image-sato
        self.driver.find_element_by_id("build-input").send_keys("core-image-sato")
        self.driver.find_element_by_id("build-button").click()
        time.sleep(5)

        #go back to the main project page
        self.driver.find_element_by_css_selector("a[href='/toastergui/projects/']").click()
        time.sleep(5)
        self.driver.find_element_by_link_text("selenium-project").click()
        time.sleep(5)

        #move to all builds page
        self.driver.find_element_by_css_selector("a[href='/toastergui/builds/']").click()
#        self.driver.refresh()
        time.sleep(5)

        #check progress bar is displayed to signal a build has started
        try:
            while (self.driver.find_element_by_xpath("//div[@class='progress']").is_displayed()):
                self.logger.info('Builds are running ...')
                self.driver.refresh()
                time.sleep(15)
        except:
            pass

        self.logger.info("Looking for successful build...")
        if (self.driver.find_element_by_xpath("//div[@class='alert build-result alert-success project-name']").is_displayed()):
            self.logger.info("Builds complete!")
        else:
            self.fail(msg="Builds did not complete successfully.")
