from toaster_utils import *
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ToasterDriver(object):

    def __init__(self):
        self.base_url = ToasterTestsConfig.base_url
        self.log = LOG
        if not ToasterTestsConfig.initialized:
            ToasterTestsConfig.initialize()
        self.driver = self.setup_browser()

    def setup_browser(self, *browser_path):
        browser = ToasterTestsConfig.browser
        self.log.info('browser: %s' % browser)
        if browser == "firefox":
            driver = webdriver.Firefox()
        elif browser == "chrome":
            driver = webdriver.Chrome()
        elif browser == "ie":
            driver = webdriver.Ie()
        else:
            driver = None
            print "unrecognized browser type, please check"
        driver.implicitly_wait(30)
        return driver

    @staticmethod
    def browser_delay():
        """
        currently this is a workaround for some chrome test.
        Sometimes we need a delay to accomplish some operation.
        But for firefox, mostly we don't need this.
        To be discussed
        """
        if ToasterTestsConfig.browser == "chrome":
            time.sleep(1)
        return

    def go_to_base_url(self, maximize_window=True):
        self.log.info('Accessing URL %s' % str(self.base_url))
        if maximize_window:
            self.driver.maximize_window()
        self.driver.get(self.base_url)

    def clean_up(self):
        self.log.info('quiting driver')
        self.driver.quit()

    def check_active_popup_element_for_text(self, text_check_list):
        # give it 1 sec so the pop-up becomes the "active_element"
        time.sleep(1)
        element = self.driver.switch_to.active_element
        for text_item in text_check_list:
            if text_item not in element.text:
                self.log.error("didn't find text item '%s' in popup" % str(text_item))
        # any better way to close this pop-up? ... TBD
        element.send_keys(webdriver.common.keys.Keys.ESCAPE)

    def get_table_row_nr(self, table_id):
        table = self.driver.find_element_by_id(table_id)
        rows = table.find_elements_by_tag_name("tr")
        return len(rows) - 1  # first row represents the table header

    def get_table_head_text(self, table_id):
        table = self.driver.find_element_by_id(table_id)
        first_row = table.find_element_by_tag_name("tr")
        head_cells = first_row.find_elements_by_tag_name("th")
        return [str(cell.text) for cell in head_cells if len(cell.text) > 0]