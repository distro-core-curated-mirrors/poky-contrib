#! /usr/bin/env python
# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
#
# BitBake Toaster Implementation
#
# Copyright (C) 2013-2016 Intel Corporation
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
#
# The Wait class and some of SeleniumDriverHelper and SeleniumTestCase are
# modified from Patchwork, released under the same licence terms as Toaster:
# https://github.com/dlespiau/patchwork/blob/master/patchwork/tests.browser.py

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from tests.browser.selenium_helpers_base import SeleniumTestCaseBase

"""
Helper methods for creating Toaster Selenium tests which run within
the context of Django unit tests.
"""

import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException, \
        StaleElementReferenceException, TimeoutException

def create_selenium_driver(browser='chrome'):
    # set default browser string based on env (if available)
    env_browser = os.environ.get('TOASTER_TESTS_BROWSER')
    if env_browser:
        browser = env_browser

    if browser == 'chrome':
        return webdriver.Chrome(
            service_args=["--verbose", "--log-path=selenium.log"]
        )
    elif browser == 'firefox':
        return webdriver.Firefox()
    elif browser == 'marionette':
        capabilities = DesiredCapabilities.FIREFOX
        capabilities['marionette'] = True
        return webdriver.Firefox(capabilities=capabilities)
    elif browser == 'ie':
        return webdriver.Ie()
    elif browser == 'phantomjs':
        return webdriver.PhantomJS()
    else:
        msg = 'Selenium driver for browser %s is not available' % browser
        raise RuntimeError(msg)

class Wait(WebDriverWait):
    """
    Subclass of WebDriverWait with predetermined timeout and poll
    frequency. Also deals with a wider variety of exceptions.
    """
    _TIMEOUT = 10
    _POLL_FREQUENCY = 0.5

    def __init__(self, driver):
        super(Wait, self).__init__(driver, self._TIMEOUT, self._POLL_FREQUENCY)

    def until(self, method, message=''):
        """
        Calls the method provided with the driver as an argument until the
        return value is not False.
        """

        end_time = time.time() + self._timeout
        while True:
            try:
                value = method(self._driver)
                if value:
                    return value
            except NoSuchElementException:
                pass
            except StaleElementReferenceException:
                pass

            time.sleep(self._poll)
            if time.time() > end_time:
                break

        raise TimeoutException(message)

    def until_not(self, method, message=''):
        """
        Calls the method provided with the driver as an argument until the
        return value is False.
        """

        end_time = time.time() + self._timeout
        while True:
            try:
                value = method(self._driver)
                if not value:
                    return value
            except NoSuchElementException:
                return True
            except StaleElementReferenceException:
                pass

            time.sleep(self._poll)
            if time.time() > end_time:
                break

        raise TimeoutException(message)

class SeleniumTestCase(StaticLiveServerTestCase):
    """
    NB StaticLiveServerTestCase is used as the base test case so that
    static files are served correctly in a Selenium test run context; see
    https://docs.djangoproject.com/en/1.9/ref/contrib/staticfiles/#specialized-test-case-to-support-live-testing
    """
    pass
