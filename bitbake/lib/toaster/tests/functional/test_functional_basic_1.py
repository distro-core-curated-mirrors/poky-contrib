#! /usr/bin/env python3
#
# BitBake Toaster functional tests implementation
#
# Copyright (C) 2019 HCL Corporation
#
# SPDX-License-Identifier: GPL-2.0-only
#

import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.functional.functional_helpers import SeleniumFunctionalTestCase
from orm.models import Project
import logging
#import os
#import pexpect
#from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
logging.basicConfig(filename="Toasteruitestsuit2_part1.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.INFO)
class FuntionalTestBasic(SeleniumFunctionalTestCase):
#   testcase (1514)
    def test_1514_create_slenium_project(self):
        project_name = '1514'
        self.create_new_project(project_name)
        element = self.wait_until_visible('#project-created-notification')
        self.assertTrue(self.element_exists('#project-created-notification'),'Fail: 1514 Project creation notification not shown')
        self.assertTrue(project_name in element.text,
                        "Fail: 1514 New project name not in new project notification")
        self.assertTrue(Project.objects.filter(name=project_name).count(),
                        "Fail: 1514 New project not found in database")
        print("All test steps passed in test case 1514")
        logger.info("All test steps passed in test case 1514")
 #  testcase (1515)
    def test_1515_verify_left_bar_menu(self):
        project_name = '1515'
        self.create_new_project(project_name)
        self.assertTrue(self.element_exists('#config-nav'),'Configuration Tab does not exist')
        project_URL=self.get_URL()
        self.driver.find_element_by_xpath('//a[@href="'+project_URL+'"]').click()
        try:
            self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li/a[@href="+'"'+project_URL+'customimages/"'+"]").click()
            time.sleep(5)
            self.assertTrue(re.search("Custom images",self.driver.find_element_by_xpath("//div[@class='col-md-10']").text),' Fail: 1515 Custom images information is not loading properly')
        except:
            self.fail(msg='Fail: 1515 No Custom images tab available')
            logger.info('Fail: 1515 No Custom images tab available')
        try:
            self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li/a[@href="+'"'+project_URL+'images/"'+"]").click()
            self.assertTrue(re.search("Compatible image recipes",self.driver.find_element_by_xpath("//div[@class='col-md-10']").text),'Fail:1515 The Compatible image recipes information is not loading properly')
        except:
            self.fail(msg='Fail:1515 No Compatible image tab available')
            logger.info('Fail: 1515 No Compatible image tab available')
        try:
            self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li/a[@href="+'"'+project_URL+'softwarerecipes/"'+"]").click()
            self.assertTrue(re.search("Compatible software recipes",self.driver.find_element_by_xpath("//div[@class='col-md-10']").text),'Fail: 1515 The Compatible software recipe information is not loading properly')
        except:
            self.fail(msg='Fail: 1515 No Compatible software recipe tab available')
            logger.info('Fail: 1515 No Compatible software recipe tab available')
        try:
            self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li/a[@href="+'"'+project_URL+'machines/"'+"]").click()
            self.assertTrue(re.search("Compatible machines",self.driver.find_element_by_xpath("//div[@class='col-md-10']").text),'Fail: 1515 The Compatible machine information is not loading properly')
        except:
            self.fail(msg='Fail: 1515 No Compatible machines tab available')
            logger.info('Fail: 1515  No Compatible machines tab available')
        try:
            self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li/a[@href="+'"'+project_URL+'layers/"'+"]").click()
            self.assertTrue(re.search("Compatible layers",self.driver.find_element_by_xpath("//div[@class='col-md-10']").text),'Fail: 1515 The Compatible layer information is not loading properly')
        except:
            self.fail(msg='Fail: 1515 No Compatible layers tab available')
            logger.info('Fail: 1515 No Compatible layers tab available')
        try:
            self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li/a[@href="+'"'+project_URL+'configuration"'+"]").click()
            self.assertTrue(re.search("Bitbake variables",self.driver.find_element_by_xpath("//div[@class='col-md-10']").text),'Fail: 1515 The Bitbake variables information is not loading properly')
        except:
            self.fail(msg='Fail: 1515 No Bitbake variables tab available')
            logger.info('Fail: 1515 No Bitbake variables tab available')
        logger.info("All test steps passed in test case 1515")
        print("All test steps passed in test case 1515")

#   testcase (1516)
    def test_1516_review_configuration_information(self):
        project_name = '1516'
        self.create_new_project(project_name)
        try:
           self.assertTrue(self.element_exists('#machine-section'),'Fail: 1516 Machine section for the project configuration page does not exist')
           self.assertTrue(re.search("qemux86",self.driver.find_element_by_xpath("//span[@id='project-machine-name']").text),'Fail: 1516 The machine type is not assigned')
           self.driver.find_element_by_xpath("//span[@id='change-machine-toggle']").click()
           self.wait_until_visible('#select-machine-form')
           self.wait_until_visible('#cancel-machine-change')
           self.driver.find_element_by_xpath("//form[@id='select-machine-form']/a[@id='cancel-machine-change']").click()
        except:
           self.fail(msg='Fail: 1516 The machine information is wrong in the configuration page')
           logger.info('Fail: 1516 The machine information is wrong in the configuration page')
        try:
           self.driver.find_element_by_id('no-most-built')
        except:
           self.fail(msg='Fail: 1516 No Most built information in project detail page')
           logger.info('Fail: 1516 No Most built information in project detail page')
        try:
           self.assertTrue(re.search("Yocto Project master",self.driver.find_element_by_xpath("//span[@id='project-release-title']").text),'Fail:1516The project release is not defined')
        except:
           self.fail(msg=' Fail: 1516 No project release title information in project detail page')
           logger.info(' Fail: 1516 No project release title information in project detail page')
        try:
           self.driver.find_element_by_xpath("//div[@id='layer-container']")
           self.assertTrue(re.search("3",self.driver.find_element_by_id("project-layers-count").text),'Fail: 1516 There should be 3 layers listed in the layer count')
           layer_list = self.driver.find_element_by_id("layers-in-project-list")
           layers = layer_list.find_elements_by_tag_name("li")
           for layer in layers:
               if re.match ("openembedded-core",layer.text):
                  logger.info ("Pass: 1516 openembedded-core layer is a default layer in the project configuration")
               elif re.match ("meta-poky",layer.text):
                  logger.info (" Pass: 1516 meta-poky layer is a default layer in the project configuration")
               elif re.match ("meta-yocto-bsp",layer.text):
                  logger.info ("Pass: 1516 meta-yocto-bsp is a default layer in the project configuratoin")
               else:
                  self.fail(msg='Fail: 1516 default layers are missing from the project configuration')
                  logger.info('Fail: 1516 default layers are missing from the project configuration')
        except:
           self.fail(msg='Fail: 1516 No Layer information in project detail page')
           logger.info('Fail: 1516 No Layer information in project detail page')
        logger.info("All test steps passed in test case 1516")
        print("All test steps passed in test case 1516")

#   testcase (1517)
    def test_1517_verify_machine_information(self):
        project_name = '1517'
        self.create_new_project(project_name)
        try:
            self.assertTrue(self.element_exists('#machine-section'),'Fail: 1517 Machine section for the project configuration page does not exist')
            self.assertTrue(re.search("qemux86",self.driver.find_element_by_id("project-machine-name").text),'Fail: 1517 The machine type is not assigned')
            self.driver.find_element_by_id("change-machine-toggle").click()
            self.wait_until_visible('#select-machine-form')
            self.wait_until_visible('#cancel-machine-change')
            self.driver.find_element_by_id("cancel-machine-change").click()
            time.sleep(10)
        except:
            self.fail(msg='Fail: 1517 The machine information is wrong in the configuration page')
            logger.info('Fail: 1517 The machine information is wrong in the configuration page')
        print("All test steps passed in test case 1517")
        logger.info("All test steps passed in test case 1517")

#   testcase (1518)
    def test_1518_verify_most_built_recipes_information(self):
        project_name = '1518'
        self.create_new_project(project_name)
        project_URL=self.get_URL()

        try:
            self.assertTrue(re.search("You haven't built any recipes yet",self.driver.find_element_by_id("no-most-built").text),'Fail: 1518 Default message of no builds is not present')
            self.driver.find_element_by_xpath("//div[@id='no-most-built']/p/a[@href="+'"'+project_URL+'images/"'+"]").click()
            self.assertTrue(re.search("Compatible image recipes",self.driver.find_element_by_xpath("//div[@class='col-md-10']").text),'Fail: 1518 The Choose a recipe to build link  is not working  properly')
        except:
            self.fail(msg='Fail: 1518 No Most built information in project detail page')
            logger.info('Fail: 1518 No Most built information in project detail page')
        print("All test steps passed in test case 1518")
        logger.info("All test steps passed in test case 1518")

#   testcase (1519)
    def test_1519_verify_project_release_information(self):
        project_name = '1519'
        self.create_new_project(project_name)
        try:
            self.assertTrue(re.search("Yocto Project master",self.driver.find_element_by_id("project-release-title").text),'Fail: 1519 The project release is not defined')
        except:
            self.fail(msg='Fail: 1519 No project release title information in project detail page')
            logger.info('Fail: 1519 No project release title information in project detail page')
        print("All test steps passed in test case 1519")
        logger.info("All test steps passed in test case 1519")

#   testcase (1520)
    def test_1520_verify_layer_information(self):
        project_name = '1520'
        self.create_new_project(project_name)
        project_URL=self.get_URL()

        try:
           self.driver.find_element_by_xpath("//div[@id='layer-container']")
           self.assertTrue(re.search("3",self.driver.find_element_by_id("project-layers-count").text),'Fail: 1520 There should be 3 layers listed in the layer count')
           layer_list = self.driver.find_element_by_id("layers-in-project-list")
           layers = layer_list.find_elements_by_tag_name("li")

           for layer in layers:
               if re.match ("openembedded-core",layer.text):
                  logger.info ("Pass: 1520 openembedded-core layer is a default layer in the project configuration")
               elif re.match ("meta-poky",layer.text):
                  logger.info ("Pass: 1520 meta-poky layer is a default layer in the project configuration")
               elif re.match ("meta-yocto-bsp",layer.text):
                  logger.info ("Pass: 1520 meta-yocto-bsp is a default layer in the project configuratoin")
               else:
                  self.fail(msg='Fail: 1520 default layers are missing from the project configuration')
                  logger.info('Fail: 1520 default layers are missing from the project configuration')

           self.driver.find_element_by_xpath("//input[@id='layer-add-input']")
           self.driver.find_element_by_xpath("//button[@id='add-layer-btn']")
           self.driver.find_element_by_xpath("//div[@id='layer-container']/form[@class='form-inline']/p/a[@id='view-compatible-layers']")
           self.driver.find_element_by_xpath("//div[@id='layer-container']/form[@class='form-inline']/p/a[@href="+'"'+project_URL+'importlayer"'+"]")
        except:
            self.fail(msg='Fail: 1520 No Layer information in project detail page')
            logger.info('Fail: 1520 No Layer information in project detail page')
        print("All test steps passed in test case 1520")
        logger.info("All test steps passed in test case 1520")

#   testcase (1521)
    def test_1521_verify_project_detail_links(self):
        project_name = '1521'
        self.create_new_project(project_name)
        project_URL = self.get_URL()
        self.driver.find_element_by_xpath("//div[@id='project-topbar']/ul[@class='nav nav-tabs']/li[@id='topbar-configuration-tab']/a[@href="+'"'+project_URL+'"'+"]").click()
        self.assertTrue(re.search("Configuration",self.driver.find_element_by_xpath("//div[@id='project-topbar']/ul[@class='nav nav-tabs']/li[@id='topbar-configuration-tab']/a[@href="+'"'+project_URL+'"'+"]").text), 'Fail:1521 Configuration tab in project topbar is misspelled')

        try:
            self.driver.find_element_by_xpath("//div[@id='project-topbar']/ul[@class='nav nav-tabs']/li/a[@href="+'"'+project_URL+'builds/"'+"]").click()
            self.assertTrue(re.search("Builds",self.driver.find_element_by_xpath("//div[@id='project-topbar']/ul[@class='nav nav-tabs']/li/a[@href="+'"'+project_URL+'builds/"'+"]").text), 'Fail: 1521 Builds tab in project topbar is misspelled')
            self.driver.find_element_by_xpath("//div[@id='empty-state-projectbuildstable']")
        except:
            self.fail(msg='Fail: 1521 Builds tab information is not present')
            logger.info('Fail: 1521 Builds tab information is not present')

        try:
            self.driver.find_element_by_xpath("//div[@id='project-topbar']/ul[@class='nav nav-tabs']/li/a[@href="+'"'+project_URL+'importlayer"'+"]").click()
            self.assertTrue(re.search("Import layer",self.driver.find_element_by_xpath("//div[@id='project-topbar']/ul[@class='nav nav-tabs']/li/a[@href="+'"'+project_URL+'importlayer"'+"]").text), 'Fail: 1521 Import layer tab in project topbar is misspelled')
            self.driver.find_element_by_xpath("//fieldset[@id='repo-select']")
            self.driver.find_element_by_xpath("//fieldset[@id='git-repo']")
        except:
            logger.info('Fail: 1521 Import layer tab not loading properly')
            self.fail(msg='Fail: 1521 Import layer tab not loading properly')
        try:
            self.driver.find_element_by_xpath("//div[@id='project-topbar']/ul[@class='nav nav-tabs']/li/a[@href="+'"'+project_URL+'newcustomimage/"'+"]").click()
            self.assertTrue(re.search("New custom image",self.driver.find_element_by_xpath("//div[@id='project-topbar']/ul[@class='nav nav-tabs']/li/a[@href="+'"'+project_URL+'newcustomimage/"'+"]").text), 'Fail: 1521 New custom image tab in project topbar is misspelled')
            self.assertTrue(re.search("Select the image recipe you want to customise",self.driver.find_element_by_xpath("//div[@class='col-md-12']/h2").text),'Fail: 1521 The new custom image tab is not loading correctly')
        except:
            self.fail(msg='Fail 1521 :New custom image tab not loading properly')
            logger.info('Fail 1521 :New custom image tab not loading properly')
        print("All test steps passed in test case 1521")
        logger.info("All test steps passed in test case 1521")

    # # testcase (1523) only tested build link information for empty project
    def test_1523_Veryfing_the_builds_link_show_proper_information(self):
        Emty_project_msg="This project has no builds. Choose a recipe to build"
        project_name = '1523'
        self.create_new_project(project_name)
        self.driver.find_element_by_xpath("//*[@id='project-topbar']/ul/li[2]").click()
        time.sleep(10)
        logger.info(self.driver.find_element_by_xpath("//*[@id='empty-state-projectbuildstable']/div").text)
        if (self.driver.find_element_by_xpath("//*[@id='empty-state-projectbuildstable']/div").text==Emty_project_msg):
            logger.info("Pass: 1523 Empty project msg displayed correctly")
        else:
            self.fail(msg='Fail: 1523 :Empty project msg not displayed correctly')
            logger.info('Fail: 1523 Empty project msg not displayed correctly')
        print("All test steps passed in test case 1523")
        logger.info("All test steps passed in test case 1523")

# #   testcase (1522) combined half steps of test case 1523 which after building a recipie  since in this test case we are building one recipie
    def test_1522_verify_textbox_build_exists_and_works(self):
        project_name="1522"
        lable_list = [u'Latest project builds', u'All project builds']
        self.create_new_project(project_name)
        self.assertTrue(self.driver.find_element_by_xpath("//*[@placeholder='Type the recipe you want to build']"),
                        "Fail: 1522 Text with Type the recipe you want to build is not present")
        self.assertTrue(self.driver.find_element_by_id("build-button"),
                        "Fail: 1522 build button is not present near search button")
        self.build_recipie("core-image-minimal",project_name)
        #test case 1523
        element = self.driver.find_elements_by_xpath("//h2")
        label_list_test = list()
        for label in element:
            label_list_test.append(label.text)
        if (label_list_test == lable_list):
            logger.info("Pass: 1523 Both label that says Latest project builds then a label with All project builds are present")
        else:
            self.fail(msg='Fail: 1523 Both label that says Latest project builds then a label with All project builds are not present')
            logger.info('Fail: 1523 Both label that says Latest project builds then a label with All project builds are not present')
        try:
            self.driver.find_element_by_xpath("//div[@id='latest-builds']//following::div[@class='progress']")
            logger.info("Pass: 1523 A progressing build is alos going on in table")
            try:
                self.driver.find_elements_by_xpath(
                    "//div[@id='latest-builds']//following::div[@data-build-state='Succeeded']")
            except:
                logger.info("Pass: 1523 Only one build is in progress no build is in scuceeded state")
        except:
            self.wait_until_visible('#latest-builds')
            self.wait_until_visible("#table-container-projectbuildstable")
            logger.info("Pass: 1523  A table with the already done builds in the project are  present and no progressing build is there")
        try:
            self.driver.find_element_by_xpath(
                "//*[@id='table-container-projectbuildstable']//input[@id='search-input-projectbuildstable']")
            self.driver.find_element_by_id("search-submit-projectbuildstable")
        except:
            self.fail(msg='Fail: 1523 search textbox with a button is not present')
            logger.info('Fail: 1523 search textbox with a button is not present')
        print("All test steps passed in test case 1522 and 1523")
        logger.info("All test steps got passed in test case 1522 and 1523")
    #    testcase (1524)
    def test_1524_verify_that_the_Import_layer_link_shows_the_form(self):
        Import_text_msg="The layer you are importing must be compatible with Yocto Project master, which is the release you are using in this project."
        Layer_msg="Layer dependencies (optional)"
        project_name = "1524"
        self.create_new_project(project_name)
        self.driver.find_element_by_link_text("Import layer").click()
        time.sleep(30)
        if(self.driver.find_element_by_xpath("(//span[@class='help-block'])[1]").text==Import_text_msg):
            logger.info("Pass: 1524 Msg Correctly diplayed after clicking import")
        else:
            self.fail(msg='Fail: 1524 Msg  not Correctly diplayed after clicking import')
            logger.info('Fail: 1524 Msg  not Correctly diplayed after clicking import')
        self.assertTrue(self.driver.find_element_by_xpath("//*[@id='import-layer-name'][@type='text']"),msg="Fail: 1524 Layer name : textbox not present")
        self.assertTrue(self.driver.find_element_by_xpath("//input[@type='text'][@id='layer-git-repo-url']"),msg='Fail: 1524 Git repository URL : textbox not present')
        self.assertTrue(self.driver.find_element_by_xpath("//input[@type='text'][@id='layer-subdir']"),msg="Fail: 1524 Repository subdirectory (optional) : textbox not present")
        self.assertTrue(self.driver.find_element_by_xpath("//input[@type='text'][@id='layer-git-ref']"),msg="Fail: 1524 Git revision : textbox not present")
        if(self.driver.find_element_by_xpath("(//*[@class='fields-apart-from-layer-name']//legend)[4]").text==Layer_msg):
            logger.info("Pass: 1524 Msg Correctly diplayed  for Layer dependencies")
        else:
            self.fail(msg='Fail: 1524 Msg not Correctly diplayed  for Layer dependencies')
            logger.info('Fail: 1524 Msg not Correctly diplayed  for Layer dependencies')
        self.assertTrue(self.driver.find_element_by_link_text("openembedded-core"),msg="Fail: 1524 openembedded-core link not present")
        self.assertTrue(self.driver.find_element_by_xpath("//span[@class='glyphicon glyphicon-trash']"),msg="Fail: 1524 (trash icon) not present")
        self.assertTrue(self.driver.find_element_by_xpath("//input[@type='text'][@id='layer-dependency']"),msg="Fail: 1524 textbox  for add layer not present")
        self.assertTrue(self.driver.find_element_by_id("add-layer-dependency-btn"),msg="Fail: 1524 Add layer button not present")
        self.assertTrue(self.driver.find_element_by_id("import-and-add-btn"),msg="Fail: 1524 Import and add to project : button not present")
        print("All test steps passed in test case 1524")
        logger.info("All test steps passed in test case 1524")

#    testcase (1525)
    def test_1525_verify_that_New_Custom_Image_link_works_and_shows_information(self):
       new_custom_msg='Select the image recipe you want to customise '
       project_name = "1525"
       self.create_new_project(project_name)
       self.driver.find_element_by_link_text("New custom image").click()
       time.sleep(10)
       Actual_String=self.driver.find_element_by_xpath("//div[@class='col-md-12'][2]/h2").text
       if new_custom_msg in Actual_String:
            logger.info("Pass: 1525 Msg Correctly diplayed after clicking new custom image link")
       else:
            self.fail(msg='Fail: 1525 Msg not Correctly diplayed after clicking new custom image link')
            logger.info('Fail: 1525 Msg not Correctly diplayed after clicking new custom image link')
       self.assertTrue(self.driver.find_element_by_xpath("//input[@id='search-input-newcustomimagestable'][@type='text'][@placeholder='Search select the image recipe you want to customise']"),msg="Fail: 1525 search textbox with the label of: Search and select the image recipe you want to customise")
       self.assertTrue(self.driver.find_element_by_id("search-submit-newcustomimagestable"),msg="Fail: 1525 Search button is not present")
       self.assertTrue(self.driver.find_element_by_id("edit-columns-button"),msg="Fail: 1525 Edit columns butoon not present")
       self.assertTrue(self.driver.find_element_by_id("newcustomimagestable"),msg="Fail: 1525 A table that displays the customise images available")
       print("All test steps passed in test case 1525")
       logger.info("All test steps passed in test case 1525")

 #    combined testcase 1529 and 1530 and 1531 testcase (1529)
    def test_1529_1530_1531_verify_most_built_recipe_shows_maximum_5_recipes(self):
        project_name="1529"
        Build_Qeue_msg="Build queued"
        Total_Num_Recipe = 5
        Total_Recipe_list=["core-image-base","core-image-clutter", "core-image-minimal", "core-image-sato","meta-ide-support" ,"meta-toolchain"]
        Most_Built_Recipe = "core-image-base core-image-clutter core-image-minimal core-image-sato meta-ide-support meta-toolchain"
        self.create_new_project(project_name)
        self.build_recipie(Most_Built_Recipe, project_name)
        self.driver.find_element_by_id("topbar-configuration-tab").click()
        time.sleep(10)
        elements = self.driver.find_elements_by_xpath("//*[@id='freq-build-list']/li/div/label/span")
        No_of_built_recipies = len(elements)
        if (int(No_of_built_recipies) <= Total_Num_Recipe):
            logger.info("Pass: 1529 5 of the 6 recipes has been built")
        else:
            self.fail(msg='Fail: 1529 5 of the 6 recipes has not built')
            logger.info('Fail: 1529 5 of the 6 recipes has not built')
        Actual_Most_Built_Recipe = list()
        for element in elements:
            Actual_Most_Built_Recipe.append(element.text)
        not_made_list=list(set(Total_Recipe_list) - set(Actual_Most_Built_Recipe))
        if (all(x in Most_Built_Recipe for x in Actual_Most_Built_Recipe)):
            logger.info("Pass: 1529 The first 5 built recipe made the list")
        else:
            self.fail(msg='Fail: 1529 The first 5 built recipe has not made the list')
            logger.info('Fail: 1529 The first 5 built recipe has not made the list')
        #test case 1530
        self.driver.find_element_by_id("build-input").click()
        self.driver.find_element_by_id('build-input').send_keys(" ".join(not_made_list))
        self.driver.find_element_by_id('build-button').click()
        time.sleep(10)
        try:
            WebDriverWait(self.driver, 1000).until(EC.element_to_be_clickable((By.XPATH, '(//*[@id="latest-builds"]//span[@class="rebuild-btn alert-link info pull-right"])[1]')))
            time.sleep(100)
        except:
            self.fail(msg='Fail: 1529 second build for the send recipie went wrong')
            logger.info('Fail: 1529 second build for the send recipie went wrong')
        self.driver.find_element_by_id("topbar-configuration-tab").click()
        elements = self.driver.find_elements_by_xpath("//*[@id='freq-build-list']/li/div/label/span")
        Rebuild_Actual_Most_Built_Recipe = list()
        print(set(not_made_list))
        for element in elements:
            Rebuild_Actual_Most_Built_Recipe.append(element.text)
        print(set(not_made_list))
        print(set(Rebuild_Actual_Most_Built_Recipe))
        if (set(not_made_list) & set(Rebuild_Actual_Most_Built_Recipe)):
            logger.info("Pass: 1530 Rebuild list  has made the list ")
        else:
            self.fail("Fail: 1530 Rebuild list has not made the list")
            logger.info("Fail: 1530 Rebuild list has not made the list")
        #test case 1531
        self.driver.find_element_by_xpath("//*[@id='freq-build-list']/li[1]/div/label/input").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='freq-build-list']/li[2]/div/label/input").click()
        time.sleep(20)
        self.driver.find_element_by_xpath("//*[@id='freq-build-btn']").click()
        time.sleep(50)
        self.driver.find_element_by_xpath("//*[@id='topbar-configuration-tab']/a").click()
        time.sleep(20)
        self.driver.find_element_by_xpath("//*[@id='freq-build-list']/li[2]/div/label/input").click()
        time.sleep(20)
        self.driver.find_element_by_xpath("//*[@id='freq-build-btn']").click()
        time.sleep(20)
        #print(self.driver.find_element_by_xpath("//*[@id='latest-builds']/div[1]/div/div[2]/div[1]").text)
        if (self.driver.find_element_by_xpath("//*[@id='latest-builds']/div[1]/div/div[2]/div[1]").text==Build_Qeue_msg):
            logger.info("Pass: 1531 Build is in queue as expected")
        else:
            self.fail(msg='Fail: 1531 Build is not in queue as expected')
            logger.info('Pass: 1531 Build is not in queue as expected')
        try:
            WebDriverWait(self.driver, 1000).until(EC.element_to_be_clickable((By.XPATH, '(//*[@id="latest-builds"]//span[@class="rebuild-btn alert-link info pull-right"])[1]')))
            time.sleep(100)
        except:
            logger.info('Pass: 1531 looks like build is still in queue')
        logger.info("All test steps passed in test case  1529 1530 and 1531")
        print("All test steps passed in test case  1529 1530 and 1531")

    def test_1535_Verify_layer_addition_functionality(self):
        project_name = "1535"
        Layer_name = "meta"
        Import_Layer_name="1535_import_layer"
        Repository_subdirectory="meta-acer"
        Git_revision='1'
        Layer_dependencies_name="meta"
        Git_repository_URL="git://github.com/shr-distribution/meta-smartphone.git"
        Adding_layer_msg_Typing="You have added 1 layer to your project:"
        Adding_layer_msg_Compatible="You have added"
        self.create_new_project(project_name)
        self.driver.find_element_by_id("layer-add-input").click()
        time.sleep(5)
        self.driver.find_element_by_id("layer-add-input").send_keys(Layer_name)
        time.sleep(5)
        self.driver.find_element_by_id("layer-add-input").click()
        time.sleep(5)
        if (len(self.driver.find_elements_by_xpath("//div[@class='tt-suggestion tt-selectable']"))>0):
            logger.info("Pass: 1535 Suggestion after typing the layer name is coming")
        else:
            self.fail(msg='Fail: 1535 Suggestion after typing the layer name is not coming')
            logger.info('Fail: 1535 Suggestion after typing the layer name is not coming')
        self.driver.find_element_by_id("layer-add-input").send_keys(Keys.DOWN)
        time.sleep(5)
        self.driver.find_element_by_id("layer-add-input").send_keys(Keys.RETURN)
        time.sleep(5)
        self.driver.find_element_by_id("add-layer-btn").click()
        time.sleep(5)
        if (Adding_layer_msg_Typing in (self.driver.find_element_by_id("change-notification-msg").text)):
            logger.info("Pass: 1535 Layer got added after typing the name")
        else:
            self.fail(msg='Fail: 1535 Layer got added after typing the name')
            logger.info('Fail: 1535 Layer got added after typing the name')
        self.driver.find_element_by_id("hide-alert").click()
        self.driver.find_element_by_id("view-compatible-layers").click()
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='in_current_project']/i").click()
        time.sleep(5)
        self.driver.find_element_by_id("in_current_project:not_in_project").click()
        time.sleep(5)
        self.driver.find_element_by_xpath('//*[@id="filter-modal-layerstable"]/div/div/div[3]/button').click()
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr[1]/td[7]/a[2]").click()
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='dependencies-modal-form']/div[3]/button[1]").click()
        time.sleep(5)
        if (Adding_layer_msg_Compatible in self.driver.find_element_by_id("change-notification-msg").text ):
            logger.info("Pass: 1535 Layer got added after adding from compatible layer")
        else:
            logger.info('Fail: 1535 Layer not added after adding from compatible layer')
            self.fail(msg='Fail: 1535 Layer not added after adding from compatible layer')
        self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li[1]/a").click()
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='layer-container']/form/p/a[2]").click()
        time.sleep(5)
        self.driver.find_element_by_id("import-layer-name").click()
        time.sleep(5)
        self.driver.find_element_by_id("import-layer-name").send_keys(Import_Layer_name)
        time.sleep(5)
        self.driver.find_element_by_id("layer-git-repo-url").click()
        time.sleep(5)
        self.driver.find_element_by_id("layer-git-repo-url").send_keys(Git_repository_URL)
        time.sleep(5)
        self.driver.find_element_by_id("layer-subdir").click()
        time.sleep(5)
        self.driver.find_element_by_id("layer-subdir").send_keys(Repository_subdirectory)
        time.sleep(5)
        self.driver.find_element_by_id("layer-git-ref").click()
        time.sleep(5)
        self.driver.find_element_by_id("layer-git-ref").send_keys(Git_revision)
        time.sleep(5)
        self.driver.find_element_by_id("layer-git-ref").click()
        time.sleep(5)
        self.driver.find_element_by_id("layer-git-ref").send_keys(Keys.DOWN)
        time.sleep(10)
        self.driver.find_element_by_id("layer-git-ref").send_keys(Keys.RETURN)
        time.sleep(10)
        self.driver.find_element_by_id("layer-dependency").click()
        time.sleep(5)
        self.driver.find_element_by_id("layer-dependency").send_keys(Layer_dependencies_name)
        time.sleep(5)
        self.driver.find_element_by_id("layer-dependency").click()
        time.sleep(5)
        self.driver.find_element_by_id("layer-dependency").send_keys(Keys.DOWN)
        time.sleep(10)
        self.driver.find_element_by_id("layer-dependency").send_keys(Keys.RETURN)
        time.sleep(5)
        self.driver.find_element_by_id("add-layer-dependency-btn").click()
        time.sleep(5)
        self.driver.find_element_by_id("import-and-add-btn").click()
        time.sleep(5)
        logger.info(self.driver.find_element_by_id("change-notification-msg").text)
        logger.info("All test steps passed in test case  1535")
        print("All test steps passed in test case  1535")

    #1536
    def test_1536_verify_delete_layer_functionality(self):
        project_name = '1536'
        delete_msg="You have removed 1 layer from your project"
        msg1="This project has no layers"
        msg2="Choose from the layers compatible with this project"
        msg3="Import a layer"
        msg4="Read about layers in the documentation"
        msg5="Or type a layer name below"
        self.create_new_project(project_name)
        org_count_layer=int(self.driver.find_element_by_id("project-layers-count").text)
        Delete_elements=self.driver.find_elements_by_xpath("//span[@class='glyphicon glyphicon-trash']")
        for Delete_element in Delete_elements:
            time.sleep(10)
            self.driver.find_element_by_xpath("(//span[@class='glyphicon glyphicon-trash'])[1]").click()
            time.sleep(5)
            if (delete_msg in self.driver.find_element_by_id("change-notification-msg").text):
                logger.info("Pass: 1536 Correct delete message has been displayed")
                self.driver.find_element_by_xpath("//a[@id='layer-affected-name'] [contains(@href,'/toastergui/')]")
                count_layer_after_deletion=self.driver.find_element_by_id("project-layers-count").text
                logger.info(count_layer_after_deletion)
                time.sleep(10)
                if(int(count_layer_after_deletion)<int(org_count_layer)):
                    logger.info("Pass: 1536 Count got decreased after deleting the layer")
                    org_count_layer=org_count_layer-1
                else:
                    logger.info("Fail: 1536 Count didn't decrease after deleting the layer")
                    self.fail(msg="Fail: 1536  Count didn't decrease after deleting the layer")
            else:
                self.fail(msg='Fail: 1536 Flase delete message has been displayed')
                logger.info('Fail: 1536 Flase delete message has been displayed')
            self.driver.find_element_by_id("hide-alert").click()
            time.sleep(30)
        if (self.driver.find_element_by_xpath("//*[@id='no-layers-in-project']//h4").text==msg1):
            pass
        else:
            self.fail(msg="Fail: 1536 :%s is not diaplyed" %msg1)
            logger.info("Fail: 1536 :%s is not diaplyed" % msg1)
        if(self.driver.find_element_by_xpath("//*[@id='no-layers-in-project']/ul/li[1]/a").text==msg2):
            self.driver.find_element_by_xpath("//*[@id='no-layers-in-project']/ul/li[1]/a").click()
            self.driver.back()
            time.sleep(10)
        else:
            self.fail(msg="Fail: 1536 %s is not diaplyed" %msg2)
            logger.info("Fail: 1536 %s is not diaplyed" % msg2)
        if (self.driver.find_element_by_xpath("//*[@id='no-layers-in-project']/ul/li[2]/a").text==msg3):
            self.driver.find_element_by_xpath("//*[@id='no-layers-in-project']/ul/li[2]/a").click()
            self.driver.back()
            time.sleep(30)
        else:
            self.fail(msg=("Fail: 1536 %s is not diaplyed" %msg3))
            logger.info("Fail: 1536 %s is not diaplyed" % msg3)
        if (self.driver.find_element_by_xpath("//*[@id='no-layers-in-project']/ul/li[3]/a").text==msg4):
            self.driver.find_element_by_xpath("//*[@id='no-layers-in-project']/ul/li[3]/a").click()
            time.sleep(30)
        else:
            self.fail(msg="Fail :1536 %s is not diaplyed" %msg4)
            logger.info("Fail: 1536 %s is not diaplyed" % msg4)
        if (self.driver.find_element_by_xpath("//*[@id='no-layers-in-project']/ul/li[4]").text==msg5):
            pass
        else:
            logger.info("Fail: 1536 %s not  dislayed" % msg5)
            self.fail(msg="Fail: 1536 %s not  dislayed" %msg5)
        logger.info("All test steps passed in test case 1536")
        print("All test steps passed in test case 1536")

    #  Test case 1412 it can be skipped since wr are doing same thing in test case 1529
    def test_1412_Build_multiple_recipes(self):
        project_name = "1412"
        Most_Built_Recipe = "core-image-minimal core-image-sato"
        self.create_new_project(project_name)
        self.build_recipie(Most_Built_Recipe, project_name)
        logger.info("All test steps passed in test case 1412")
        print("All test steps passed in test case 1412")

    def test_1413_Build_a_recipe_with_different_distro(self):
        project_name = "1413"
        Built_Recipe = "core-image-minimal"
        Add_Variable_name="test"
        Add_Variable_value = "meta-qt3, meta-qt4"
        Distro_input_change="poky-lsb"
        self.create_new_project(project_name)
        self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li[10]/a").click()
        time.sleep(5)
        self.driver.find_element_by_id("change-distro-icon").click()
        time.sleep(5)
        self.driver.find_element_by_id("new-distro").click()
        time.sleep(5)
        self.driver.find_element_by_id("new-distro").clear()
        time.sleep(4)
        self.driver.find_element_by_id("new-distro").send_keys(Distro_input_change)
        time.sleep(5)
        self.driver.find_element_by_id("apply-change-distro").click()
        time.sleep(5)
        self.driver.find_element_by_id("variable").click()
        time.sleep(5)
        self.driver.find_element_by_id("variable").send_keys(Add_Variable_name)
        time.sleep(5)
        self.driver.find_element_by_id("value").click()
        time.sleep(5)
        self.driver.find_element_by_id("value").send_keys(Add_Variable_value)
        time.sleep(5)
        self.driver.find_element_by_id("add-configvar-button").click()
        time.sleep(10)
        self.build_recipie(Built_Recipe, project_name)
        self.driver.find_element_by_xpath("//*[@id='topbar-configuration-tab']/a").click()
        time.sleep(10)
        if (self.driver.find_element_by_id("project-distro-name").text==Distro_input_change):
            logger.info("Pass: 1413 Distro name showed correctly after change")
        else:
            self.fail(msg="Fail: 1413 Distro name didn't show correctly after change")
            logger.info("Fail: 1413 Distro name didn't show correctly after change")
        logger.info("Pass: 1413 :All steps got passed in test case 1413")
        print("All test steps passed in test case 1413")
        #  Test case 1412 it can be skipped since wr are doing same thing in test case 1529

    def test_1414_package_format_ipk_rpm_deb(self):
        project_name = "1414"
        Built_Recipe = "core-image-minimal"
        Package_class_selected='package_rpm package_deb package_ipk'
        self.create_new_project(project_name)
        self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li[10]/a").click()
        time.sleep(5)
        self.driver.find_element_by_id("change-package_classes-icon").click()
        time.sleep(5)
        self.driver.find_element_by_id("package_class_1_input").click()
        time.sleep(5)
        self.driver.find_element_by_id("package_class_2_input").click()
        time.sleep(5)
        self.driver.find_element_by_id("apply-change-package_classes").click()
        time.sleep(5)
        if (self.driver.find_element_by_id("package_classes").text==Package_class_selected):
            logger.info("Pass: 1414 Package classes selected")
        else:
            logger.info('Fail: 1414 Package classes not selected')
            self.fail(msg='Fail: 1414 Package classes not selected')
        self.build_recipie(Built_Recipe, project_name)
        print("All test steps passed in test case 1414")
        logger.info("All test steps passed in test case 1414")

    #test_case1415
    def test_1415_IMAGE_INSTALL_append_variable(self):
        project_name = "1415"
        Built_Recipe = "core-image-minimal"
        IMAGE_INSTALL_append_variable_name = 'acpid'
        Search_msg="Packages built"
        self.create_new_project(project_name)
        self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li[10]/a").click()
        time.sleep(5)
        self.driver.find_element_by_id("change-image_install-icon").click()
        time.sleep(5)
        self.driver.find_element_by_id("new-image_install").click()
        time.sleep(5)
        self.driver.find_element_by_id("new-image_install").send_keys(IMAGE_INSTALL_append_variable_name)
        time.sleep(5)
        self.driver.find_element_by_id("apply-change-image_install").click()
        time.sleep(5)
        if (self.driver.find_element_by_id("image_install").text ==IMAGE_INSTALL_append_variable_name):
            logger.info("Pass: 1415 IMAGE_INSTALL_append_variable_name got changed successfully")
        else:
            self.fail(msg='Fail: 1415 IMAGE_INSTALL_append_variable_name not changed successfully')
            logger.info('Fail: 1415 IMAGE_INSTALL_append_variable_name not changed successfully')
        self.build_recipie(Built_Recipe, project_name)
        self.driver.find_element_by_xpath("//*[@id='latest-builds']/div/div/div[1]/a/span").click()
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='menu-packages']/a").click()
        time.sleep(100)
        self.search_element("search-input-builtpackagestable","search-submit-builtpackagestable", IMAGE_INSTALL_append_variable_name)
        if (Search_msg in self.driver.find_element_by_xpath("//div[@class='page-header build-data']/h1").text):
            logger.info("Pass: 1415 Search for packages after adding in image_install_append")
        else:
            logger.info('Fail: 1415 Packages not found after adding in image_install_append ')
            self.fail(msg='Fail: 1415 Packages not found after adding in image_install_append ')
        print("All test steps passed in test case 1415")
        logger.info("All test steps passed in test case 1415")






















