import time
import re 

from base import ToasterFunctionalTests
from selenium.webdriver.common.action_chains import ActionChains

class ToasterProjectDetailPage(ToasterFunctionalTests):

        ##############
        #  CASE 1514 #
        ##############
    def test_1514(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self._url)
        self.driver.find_element_by_link_text("To start building, create your first Toaster project").click()
        self.driver.find_element_by_id("new-project-name").send_keys("selenium-project")
        self.driver.find_element_by_id('projectversion').click()
        self.driver.find_element_by_id("create-project-button").click()
        self.wait_until_visible('#project-created-notification')
        self.assertTrue(self.element_exists('#project-created-notification'),'Project creation notification not shown')




        ##############
        #  CASE 1515 #
        ##############
    def test_1515(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self._url)
        self.wait_until_visible('#projectstable')
        self.find_element_by_link_text_in_table('projectstable', 'selenium-project').click()        


        self.assertTrue(self.element_exists('#config-nav'),'Configuration Tab does not exist')
        project_URL=self.get_URL()
        self.driver.find_element_by_xpath('//a[@href="'+project_URL+'"]').click()

        
        try:
            self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li/a[@href="+'"'+project_URL+'customimages/"'+"]").click()
            self.assertTrue(re.search("Custom images",self.driver.find_element_by_xpath("//div[@class='col-md-10']").text),'Custom images information is not loading properly')
        except:
            self.fail(msg='No Custom images tab available')



        try:
            self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li/a[@href="+'"'+project_URL+'images/"'+"]").click()
            self.assertTrue(re.search("Compatible image recipes",self.driver.find_element_by_xpath("//div[@class='col-md-10']").text),'The Compatible image recipes information is not loading properly')
        except:
            self.fail(msg='No Compatible image tab available')


        try:
            self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li/a[@href="+'"'+project_URL+'softwarerecipes/"'+"]").click()
            self.assertTrue(re.search("Compatible software recipes",self.driver.find_element_by_xpath("//div[@class='col-md-10']").text),'The Compatible software recipe information is not loading properly')
        except:
            self.fail(msg='No Compatible software recipe tab available') 
        
        
        try:
            self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li/a[@href="+'"'+project_URL+'machines/"'+"]").click()
            self.assertTrue(re.search("Compatible machines",self.driver.find_element_by_xpath("//div[@class='col-md-10']").text),'The Compatible machine information is not loading properly')
        except:
            self.fail(msg='No Compatible machines tab available')
        

        try:
            self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li/a[@href="+'"'+project_URL+'layers/"'+"]").click()
            self.assertTrue(re.search("Compatible layers",self.driver.find_element_by_xpath("//div[@class='col-md-10']").text),'The Compatible layer information is not loading properly')
        except:
            self.fail(msg='No Compatible layers tab available')
        
        try:
            self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li/a[@href="+'"'+project_URL+'configuration"'+"]").click()
            self.assertTrue(re.search("Bitbake variables",self.driver.find_element_by_xpath("//div[@class='col-md-10']").text),'The Bitbake variables information is not loading properly')
        except:
            self.fail(msg='No Bitbake variables tab available')





        ##############
        #  CASE 1516 #
        ##############

    def test_1516(self):

        self.case_no = self.get_case_number()
        project_URL=self.get_URL()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self._url)
        self.wait_until_visible('#projectstable')
        self.find_element_by_link_text_in_table('projectstable', 'selenium-project').click()

        try:
           self.assertTrue(self.element_exists('#machine-section'),'Machine section for the project configuration page does not exist')
           self.assertTrue(re.search("qemux86",self.driver.find_element_by_xpath("//span[@id='project-machine-name']").text),'The machine type is not assigned')
           self.driver.find_element_by_xpath("//span[@id='change-machine-toggle']").click()
           self.wait_until_visible('#select-machine-form')
           self.wait_until_visible('#cancel-machine-change') 
           self.driver.find_element_by_xpath("//form[@id='select-machine-form']/a[@id='cancel-machine-change']").click()
        except:
           self.fail(msg='The machine information is wrong in the configuration page')



        try:
           self.driver.find_element_by_xpath("//div[@id='no-most-built']")
        except:
           self.fail(msg='No Most built information in project detail page')


        try:
           self.assertTrue(re.search("Yocto Project master",self.driver.find_element_by_xpath("//span[@id='project-release-title']").text),'The project release is not defined')
        except:
           self.fail(msg='No project release title information in project detail page')


        try:
           self.driver.find_element_by_xpath("//div[@id='layer-container']")
           self.assertTrue(re.search("3",self.driver.find_element_by_xpath("//span[@id='project-layers-count']").text),'There should be 3 layers listed in the layer count')
           self.assertTrue(re.search("openembedded-core",self.driver.find_element_by_xpath("//div[@id='layer-container']/ul[@id='layers-in-project-list']/li/a[@href="+'"'+project_URL+'layer/4"'+"]").text), 'openembedded-core layer should be present')
           self.assertTrue(re.search("meta-poky",self.driver.find_element_by_xpath("//div[@id='layer-container']/ul[@id='layers-in-project-list']/li/a[@href="+'"'+project_URL+'layer/211"'+"]").text), 'meta-poky layer should be present')
           self.assertTrue(re.search("meta-yocto-bsp",self.driver.find_element_by_xpath("//div[@id='layer-container']/ul[@id='layers-in-project-list']/li/a[@href="+'"'+project_URL+'layer/31"'+"]").text), 'meta-yocto-bsp layer should be present')

           self.driver.find_element_by_xpath("//input[@id='layer-add-input']")
           self.driver.find_element_by_xpath("//button[@id='add-layer-btn']")

        except:
           self.fail(msg='No Layer information in project detail page')


        ##############
        #  CASE 1517 #
        ##############
    def test_1517(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self._url)
        self.wait_until_visible('#projectstable')
        self.find_element_by_link_text_in_table('projectstable', 'selenium-project').click()
        try:
            self.assertTrue(self.element_exists('#machine-section'),'Machine section for the project configuration page does not exist')
            self.assertTrue(re.search("qemux86",self.driver.find_element_by_xpath("//span[@id='project-machine-name']").text),'The machine type is not assigned')
            self.driver.find_element_by_xpath("//span[@id='change-machine-toggle']").click()
            self.wait_until_visible('#select-machine-form')
            self.wait_until_visible('#cancel-machine-change')
            self.driver.find_element_by_xpath("//form[@id='select-machine-form']/a[@id='cancel-machine-change']").click()
        except:
            self.fail(msg='The machine information is wrong in the configuration page')



        ##############
        #  CASE 1518 #
        ##############


    def test_1518(self):
        self.case_no = self.get_case_number()
        project_URL=self.get_URL()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self._url)
        self.wait_until_visible('#projectstable')
        self.find_element_by_link_text_in_table('projectstable', 'selenium-project').click()
        try:
            self.assertTrue(re.search("You haven't built any recipes yet",self.driver.find_element_by_xpath("//div[@id='no-most-built']").text),'Default message of no builds is not present')
            self.driver.find_element_by_xpath("//div[@id='no-most-built']/p/a[@href="+'"'+project_URL+'images/"'+"]").click()
            self.assertTrue(re.search("Compatible image recipes",self.driver.find_element_by_xpath("//div[@class='col-md-10']").text),'The Choose a recipe to build link  is not working  properly')            

        except:
            self.fail(msg='No Most built information in project detail page')




        ##############
        #  CASE 1519 #
        ##############


    def test_1519(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self._url)
        self.wait_until_visible('#projectstable')
        self.find_element_by_link_text_in_table('projectstable', 'selenium-project').click()

        try:
            self.assertTrue(re.search("Yocto Project master",self.driver.find_element_by_xpath("//span[@id='project-release-title']").text),'The project release is not defined')
        except:
            self.fail(msg='No project release title information in project detail page')




        ##############
        #  CASE 1520 #
        ##############


    def test_1520(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self._url)
        self.wait_until_visible('#projectstable')
        self.find_element_by_link_text_in_table('projectstable', 'selenium-project').click()
        project_URL=self.get_URL()
        
        try:
            self.driver.find_element_by_xpath("//div[@id='layer-container']")
            self.assertTrue(re.search("3",self.driver.find_element_by_xpath("//span[@id='project-layers-count']").text),'There should be 3 layers listed in the layer count')
            self.assertTrue(re.search("openembedded-core",self.driver.find_element_by_xpath("//div[@id='layer-container']/ul[@id='layers-in-project-list']/li/a[@href="+'"'+project_URL+'layer/4"'+"]").text), 'openembedded-core layer should be present')
            self.assertTrue(re.search("meta-poky",self.driver.find_element_by_xpath("//div[@id='layer-container']/ul[@id='layers-in-project-list']/li/a[@href="+'"'+project_URL+'layer/211"'+"]").text), 'meta-poky layer should be present')
            self.assertTrue(re.search("meta-yocto-bsp",self.driver.find_element_by_xpath("//div[@id='layer-container']/ul[@id='layers-in-project-list']/li/a[@href="+'"'+project_URL+'layer/31"'+"]").text), 'meta-yocto-bsp layer should be present')

            self.driver.find_element_by_xpath("//input[@id='layer-add-input']")
            self.driver.find_element_by_xpath("//button[@id='add-layer-btn']")
            self.driver.find_element_by_xpath("//div[@id='layer-container']/form[@class='form-inline']/p/a[@id='view-compatible-layers']")
            self.driver.find_element_by_xpath("//div[@id='layer-container']/form[@class='form-inline']/p/a[@href="+'"'+project_URL+'importlayer"'+"]")

        except:
            self.fail(msg='No Layer information in project detail page')




        ##############
        #  CASE 1521 #
        ##############


    def test_1521(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self._url)
        self.wait_until_visible('#projectstable')
        self.find_element_by_link_text_in_table('projectstable', 'selenium-project').click()
        project_URL=self.get_URL()


        
        self.driver.find_element_by_xpath("//div[@id='project-topbar']/ul[@class='nav nav-tabs']/li[@id='topbar-configuration-tab']/a[@href="+'"'+project_URL+'"'+"]").click()
        self.assertTrue(re.search("Configuration",self.driver.find_element_by_xpath("//div[@id='project-topbar']/ul[@class='nav nav-tabs']/li[@id='topbar-configuration-tab']/a[@href="+'"'+project_URL+'"'+"]").text), 'Configuration tab in project topbar is misspelled')
        time.sleep(5)

        try:
            self.driver.find_element_by_xpath("//div[@id='project-topbar']/ul[@class='nav nav-tabs']/li/a[@href="+'"'+project_URL+'builds/"'+"]").click()
            self.assertTrue(re.search("Builds",self.driver.find_element_by_xpath("//div[@id='project-topbar']/ul[@class='nav nav-tabs']/li/a[@href="+'"'+project_URL+'builds/"'+"]").text), 'Builds tab in project topbar is misspelled')
            self.driver.find_element_by_xpath("//div[@id='empty-state-projectbuildstable']")
        except:
            self.fail(msg='Builds tab information is not present')



        time.sleep(5)


        try:
            self.driver.find_element_by_xpath("//div[@id='project-topbar']/ul[@class='nav nav-tabs']/li/a[@href="+'"'+project_URL+'importlayer"'+"]").click()
            self.assertTrue(re.search("Import layer",self.driver.find_element_by_xpath("//div[@id='project-topbar']/ul[@class='nav nav-tabs']/li/a[@href="+'"'+project_URL+'importlayer"'+"]").text), 'Import layer tab in project topbar is misspelled')
            
            self.driver.find_element_by_xpath("//fieldset[@id='repo-select']")
            self.driver.find_element_by_xpath("//fieldset[@id='git-repo']")
        except:
            self.fail(msg='Import layer tab not loading properly')


        time.sleep(5)

        try:
            self.driver.find_element_by_xpath("//div[@id='project-topbar']/ul[@class='nav nav-tabs']/li/a[@href="+'"'+project_URL+'newcustomimage/"'+"]").click()
            self.assertTrue(re.search("New custom image",self.driver.find_element_by_xpath("//div[@id='project-topbar']/ul[@class='nav nav-tabs']/li/a[@href="+'"'+project_URL+'newcustomimage/"'+"]").text), 'New custom image tab in project topbar is misspelled')

            self.assertTrue(re.search("Select the image recipe you want to customise",self.driver.find_element_by_xpath("//div[@class='col-md-12']/h2").text),'The new custom image tab is not loading correctly')

        except:
            self.fail(msg='New custom image tab not loading properly')



        time.sleep(5)
