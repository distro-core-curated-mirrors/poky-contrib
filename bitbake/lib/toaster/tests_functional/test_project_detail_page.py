from base import * #ToasterFunctionalTests

import time 

class ToasterProjectDetailPage(ToasterFunctionalTests):
    def test_project_detail_page(self):
        rc=self.driver.get(self._url)
        print(rc) #erase this
        #while True:
        #    time.sleep(1)
        #self.assertNotEqual(rc, None, "Selenium driver get {0} returns None".format(self._url))


        ##############
        #  CASE 1514 #
        ##############
    def test_1514(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("To start building, create your first Toaster project").click()
        self.driver.find_element_by_id("new-project-name").send_keys("selenium-project")
        self.driver.find_element_by_xpath("//select[@name='projectversion']/option[text()='1']").click()
        self.driver.find_element_by_id("create-project-button").click()
        try:
            self.find_element(By.ID,"project-created-notification")
        except:
            self.fail(msg='Project creation notification not shown')
