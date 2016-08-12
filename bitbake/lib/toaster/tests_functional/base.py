import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
    '../', 'tests', 'browser')) # XXX: Test tool should insert the path
if not 'TOASTER_TESTS_BROWSER' in os.environ:
    os.environ['TOASTER_TESTS_BROWSER'] = 'firefox'
if not 'TOASTER_URL' in os.environ:
    os.environ['TOASTER_URL'] = 'http://localhost:8000'
import logging
logging.basicConfig()

from selenium_helpers_base import SeleniumTestCaseBase

class ToasterFunctionalTests(SeleniumTestCaseBase):
        _url = os.environ['TOASTER_URL']
        _logger = logging.getLogger()
        _logger.setLevel(logging.INFO)
