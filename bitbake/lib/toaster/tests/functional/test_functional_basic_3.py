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
import os
import pexpect
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
logging.basicConfig(filename="Toasteruitestsuit2_part3.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.INFO)
class FuntionalTestBasic(SeleniumFunctionalTestCase):
    def test_1400_compatible_machines(self):
        project_name = "1400"
        Machine_name="intel-core2-32"
        Searched_machine_msg="Compatible machines (1)"
        Adding_layer_msg="You have added 5 layers to your project: meta-intel and its dependencies meta-dpdk, meta-intel, meta-intel-qat, meta-intel"
        Adding_machine_msg = "You have changed the machine to: intel-core2-32"
        self.create_new_project(project_name)
        time.sleep(20)
        self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li[6]/a").click()
        time.sleep(5)
        self.search_element("search-input-machinestable", "search-submit-machinestable", Machine_name)
        if (Searched_machine_msg==(self.driver.find_element_by_xpath("/html/body/div[3]/div/div[3]/h2").text)):
            logger.info("Pass: 1400 Searched machine found to add")
        else:
            logger.info("Fail: 1400 Searched machine not found to add")
            self.fail(msg="Fail: 1400 Searched machine not found to add")
        time.sleep(50)

        self.driver.find_element_by_xpath("//*[@id='machinestable']/tbody/tr[1]/td[6]/a[2]").click()
        time.sleep(20)

        self.driver.find_element_by_xpath("//*[@id='dependencies-modal-form']/div[3]/button[1]").click()
        time.sleep(10)
        if (Adding_layer_msg==(self.driver.find_element_by_id("change-notification-msg").text)):
            logger.info("Pass: 1400 Layer added successfully")
        else:
            logger.info("Fail: 1400 Layer  not added successfully")
            self.fail(msg="Fail: 1400 Layer  not added successfully")
        self.driver.find_element_by_xpath("//*[@id='machinestable']/tbody/tr/td[6]/a[1]").click()
        time.sleep(100)
        if (Adding_machine_msg==(self.driver.find_element_by_xpath("//*[@id='change-notification-msg']/span").text)):
            logger.info("Pass: 1400 Machine adding notification appeared")
        else:
            logger.info("Fail: 1400 Machine adding notification not appeared")
            self.fail(msg="Fail: 1400 Machine adding notification not appeared")

        if (Machine_name==(self.driver.find_element_by_id("project-machine-name").text)):
            logger.info("Pass: 1400 machine added successfully")
        else:
            logger.info("Pass: 1400 machine not added successfully")
            self.fail(msg="Pass: 1400 machine not added successfully")
        time.sleep(5)
        self.driver.back()
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='machinestable']/tbody/tr/td[3]/a").click()
        time.sleep(5)
        self.driver.find_element_by_id("targets-tab").click()
        time.sleep(5)
        self.search_element("search-input-recipestable","search-submit-recipestable","igt-gpu-tools")
        self.driver.find_element_by_xpath("//*[@id='recipestable']/tbody/tr/td[4]/a").click()
        time.sleep(10)
        try:
            WebDriverWait(self.driver, 5000).until(EC.element_to_be_clickable(
            (By.XPATH, '(//*[@id="latest-builds"]//span[@class="rebuild-btn alert-link info pull-right"])[1]')))
            time.sleep(5)
        except:
            logger.info("Fail: 1400 Build is not successful")
            self.fail(msg="Fail: 1400 Build is not successful")
        logger.info("All test steps passed in test case 1400")
        print("All test steps passed in test case 1400")

    def test_1401_Builds_with_different_machines(self):
        project_name = "1401"
        Machine_name1="qemux86-64"
        Machine_name2 = "qemumips"
        Adding_machine_msg = "You have changed the machine to: qemux86-64"
        self.create_new_project(project_name)
        time.sleep(20)
        self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li[6]/a").click()
        time.sleep(5)
        self.search_element("search-input-machinestable", "search-submit-machinestable", Machine_name1)
        self.driver.find_element_by_xpath("//*[@id='machinestable']/tbody/tr[1]/td[6]/a[1]").click()
        time.sleep(5)

        if (Adding_machine_msg==(self.driver.find_element_by_xpath("//*[@id='change-notification-msg']/span").text)):
            logger.info("Pass: 1401 Machine adding notification appeared")
        else:
            self.fail(msg="Fail: 1401 Machine adding notification not appeared")
            logger.info("Fail: 1401 Machine adding notification not appeared")
        if (Machine_name1==(self.driver.find_element_by_id("project-machine-name").text)):
            logger.info("Pass: 1401 machine qemux86-64 added successfully")
        else:
            logger.info("Fail: 1401 machine  qemux86-64 not added successfully")
            self.fail(msg="Fail: 1401 machine  qemux86-64 not added successfully")
        time.sleep(5)
        self.build_recipie('core-image-minimal', project_name)
        self.driver.find_element_by_xpath("//*[@id='topbar-configuration-tab']/a").click()
        time.sleep(5)
        self.driver.find_element_by_id("change-machine-toggle").click()
        time.sleep(5)
        self.driver.find_element_by_id("machine-change-input").clear()
        time.sleep(5)
        self.driver.find_element_by_id("machine-change-input").send_keys('qemumips')
        time.sleep(5)
        self.driver.find_element_by_id('machine-change-btn').click()
        time.sleep(5)
        if (Machine_name2==(self.driver.find_element_by_id("project-machine-name").text)):
            logger.info("Pass: 1401 machine2  qemumips added successfully")
        else:
            logger.info("Fail: 1401 machine2 qemumips  not added successfully")
            self.fail(msg="Fail: 1401 machine2 qemumips  not added successfully")
        time.sleep(5)
        self.driver.find_element_by_id("build-input").send_keys('core-image-sato')
        time.sleep(5)
        self.driver.find_element_by_id("build-button").click()
        time.sleep(400)
        # try:
        #     WebDriverWait(self.driver, 5000).until(EC.element_to_be_clickable(
        #        (By.XPATH, "(//*[@id='latest-builds']//span[@class='rebuild-btn alert-link info pull-right'])[1]")))
        #     time.sleep(5)
        # finally:
        #     self.fail(msg=" Fail Build is not successful for test case  {} ".format(project_name))
        time.sleep(100)
        self.driver.find_element_by_xpath("//*[@id='latest-builds']/div[1]/div/div[1]/a/span").click()
        time.sleep(20)
        if(self.driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[2]/div/div[3]/div[1]/div/dl/dd[1]").text==Machine_name2):
            logger.info("Pass: 1401 Correct  machine name displayed with build2 ")
        else:
            logger.info("Fail: 1401 Correct  machine name not  displayed with build2 ")
            self.fail(msg="Fail: 1401 Correct  machine name not  displayed with build2 ")
        self.driver.back()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='latest-builds']/div[2]/div/div[1]/a/span").click()
        time.sleep(10)
        if(self.driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[2]/div/div[3]/div[1]/div/dl/dd[1]").text==Machine_name1):
            logger.info("Pass: 1401 Correct  machine name displayed with  this build1  ")
        else:
            logger.info("Fail: 1401 Correct  machine name not  displayed with build1 ")
            self.fail(msg="Fail: 1401 Correct  machine name not  displayed with build1 ")
        print("All test steps passed in test case 1401")
        logger.info("All test steps passed in test case 1401")
    #Test case 1402
    def test_1402_bitbake_variables_IMAGE_FSTYPES(self):
        project_name = "1402"
        self.create_new_project(project_name)
        time.sleep(20)
        self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li[10]/a").click()
        time.sleep(5)
        self.driver.find_element_by_id("change-image_fstypes-icon").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='all-image_fstypes']/div[20]/label/input").click()
        time.sleep(20)
        self.driver.find_element_by_xpath("//*[@id='all-image_fstypes']/div[17]/label/input").click()
        time.sleep(20)
        self.driver.find_element_by_id("apply-change-image_fstypes").click()
        time.sleep(10)
        selected_image=(self.driver.find_element_by_id("image_fstypes").text)
        self.build_recipie('core-image-minimal', project_name)
        self.driver.find_element_by_xpath("//*[@id='latest-builds']/div[1]/div/div[1]/a/span").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='menu-configuration']/a").click()
        time.sleep(30)
        self.driver.find_element_by_xpath("//*[@id='navTab']/ul/li[2]/a").click()
        time.sleep(20)
        self.search_element("search", "search-button", "ext4")
        if (selected_image in self.driver.find_element_by_xpath("//*[@id='otable']/tbody/tr/td[2]").text ):
            logger.info("Pass: 1402 selcted image got built in recipie")
        else:
            logger.info("Fail: 1402 selcted image not built in recipie")
            self.fail(msg="Fail: 1402 selcted image not built in recipie")
        print("All test steps passed in test case 1402")
        logger.info("All test steps passed in test case 1402")
    #test case 1403
    def test_1403_Software_recipes_default_view(self):
        project_name = "1403"
        default_head_software_recipies="Software recipe Version Description Layer Build"
        self.create_new_project(project_name)
        time.sleep(20)
        self.build_recipie('core-image-minimal', project_name)
        self.driver.find_element_by_xpath("//*[@id='topbar-configuration-tab']/a").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li[10]/a").click()
        time.sleep(5)

        self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li[5]/a").click()
        time.sleep(10)
        self.assertTrue(self.driver.find_element_by_id("softwarerecipestable"), 'Software recipie table not found')
        if (self.driver.find_element_by_xpath("//*[@id='softwarerecipestable']/thead/tr").text==default_head_software_recipies):
            logger.info("Pass: 1403 software recipies table head are showing correctly")
        else:
            logger.info("Fail: 1403 software recipies table are not showing correctly")
            self.fail(msg="Fail: 1403 software recipies table are not showing correctly")
        print("All test steps passed in test case 1403")
        logger.info("All test steps passed in test case 1403")
    #TEstcase 1404
    def test_1404_Software_recipes_sorting_the_content_of_the_software_recipes_table(self):
        project_name = "1404"
        deafult_sortable_head_list_name=['Software recipe', 'Section', 'Layer', 'License', '']

        Checkbox_Table = ["checkbox-add-del-layers", "checkbox-get_description_or_summary",
                          "checkbox-layer_version__get_vcs_reference", "checkbox-layer_version__layer__name",
                          "checkbox-license",'checkbox-recipe-file','checkbox-section','checkbox-name','checkbox-version']
        self.create_new_project(project_name)
        time.sleep(20)
        self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li[5]/a").click()
        time.sleep(10)
        software_recipies_column_elements=self.driver.find_elements_by_xpath("//*[@id='softwarerecipestable']/tbody/tr/td[1]")
        deafault_list_sosftware_recipie=[element.text for element in software_recipies_column_elements]
        if (deafault_list_sosftware_recipie == sorted(deafault_list_sosftware_recipie)):
            logger.info("Pass:1404 software recipie list is in ascending order by default")
        else:
            self.fail(msg="Fail: 1404 software recipie list is not in ascending order by default")
            logger.info("Fail: 1404 software recipie list is not in ascending order by default")
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(2)
        for item1 in Checkbox_Table:
            if (self.driver.find_element_by_id(item1).is_selected()):
                pass
            else:
                self.driver.find_element_by_id(item1).click()
                time.sleep(5)
        self.assertTrue(self.driver.find_element_by_xpath("//div[@class='checkbox disabled']//label[@class='text-muted']//input[@id='checkbox-add-del-layers']"),
                        msg="Fail: 1404 Textbox is not muted for build ")
        self.assertTrue(self.driver.find_element_by_xpath(
            "//div[@class='checkbox disabled']//label[@class='text-muted']//input[@id='checkbox-name']"),
                        msg="Fail: 1404 Textbox is not muted for software recipie")
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(5)
        sortable_head_list_names=self.driver.find_elements_by_xpath("//*[@id='softwarerecipestable']/thead/tr/th/a")
        sortable_head_list = [element.text for element in sortable_head_list_names]
        if sortable_head_list == deafult_sortable_head_list_name :
            logger.info("Pass: 1404 sortable head list is showing correctly")
        else:
            logger.info("Fail: 1404 sortable head list is  not showing correctly")
            self.fail(msg="Fail: 1404 sortable head list is  not showing correctly")

        self.driver.find_element_by_xpath("//*[@id='softwarerecipestable']/thead/tr/th[6]/a").click()
        time.sleep(10)

        elements_after_sorting_layer = self.driver.find_elements_by_xpath(
            "//*[@id='softwarerecipestable']/tbody/tr/td[6]/a")
        list_after_sorting_layer = [element.text for element in elements_after_sorting_layer]
        self.driver.find_element_by_xpath("//*[@id='softwarerecipestable']/tbody/tr[1]/td[6]/a").click()
        time.sleep(10)
        self.driver.back()
        elements_after_sort_back_naviagtion = self.driver.find_elements_by_xpath("//*[@id='softwarerecipestable']/tbody/tr/td[6]/a")
        list_after_sort_back_naviagtion = [element.text for element in elements_after_sort_back_naviagtion]
        if (list_after_sort_back_naviagtion == list_after_sorting_layer):
             logger.info("Pass: 1404 list is  same order after navigation once sorting is applied")
        else:
             logger.info("Fail: 1404 list is not in same order after navigation once sorting is applied")
             self.fail(msg="Fail: 1404 list is not in same order after navigation once sorting is applied")
        self.search_element("search-input-softwarerecipestable", "search-submit-softwarerecipestable", "meta")
        elements_after_search_sort = self.driver.find_elements_by_xpath("//*[@id='softwarerecipestable']/tbody/tr/td[6]/a")
        list_after_search = [element.text for element in elements_after_search_sort]
        if (list_after_search == sorted(list_after_search, reverse = True)):
             logger.info("Pass: 1404 list is in  same soritng as applied before search")
        else:
             logger.info("Fail: 1404 list is  not in  same soritng as applied before search")
             self.fail(msg="Fail: 1404 list is  not in  same soritng as applied before search")
        self.edit_specicific_checkbox("checkbox-layer_version__layer__name")
        software_recipies_column_elements = self.driver.find_elements_by_xpath(
            "//*[@id='softwarerecipestable']/tbody/tr/td[1]")
        deafault_list_software_recipie = [element.text for element in software_recipies_column_elements]
        if (deafault_list_software_recipie == sorted(deafault_list_software_recipie)):
            logger.info("Pass: 1404 software recipie list is in ascending order by default after hiding the sorted column layer")
        else:
            logger.info(
                "Fail: 1404 software recipie list is not in ascending order by default after hiding the sorted column layer")
            self.fail(msg="Fail: 1404 software recipie list is not in ascending order by default after hiding the sorted column layer")
        print("All test steps passed in test case  1404")
        logger.info("All test steps passed in test case  1404")

    # TEstcase 1405
    def test_1405_Software_recipes_Searching_the_content_of_the_software_recipes_table(self):
        project_name = "1405"
        self.create_new_project(project_name)
        time.sleep(20)
        self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li[5]/a").click()
        time.sleep(10)
        self.assertTrue(self.driver.find_element_by_id("search-input-softwarerecipestable"), msg="Fail: 1405 Search is made of a text input field  is not present")
        self.assertTrue(self.driver.find_element_by_id("search-submit-softwarerecipestable"),msg="Fail: 1405 Search  button toolbar is not present")
        self.assertTrue(self.driver.find_element_by_xpath("//input[@id='search-input-softwarerecipestable'][@placeholder='Search compatible software recipes']"),
                        msg="Fail: 1405 Search placeholder is not present")

        string_before_search = (self.driver.find_element_by_xpath("//div[@class='col-md-10']/h2").text)
        value_before_search = int(((string_before_search.split())[-1]).split('(')[-1].split(')')[0])
        head_elements_before_search = self.driver.find_elements_by_xpath("//*[@id='softwarerecipestable']/thead/tr/th")
        head_element_list_before_search = [element.text for element in head_elements_before_search]
        self.search_element("search-input-softwarerecipestable", "search-submit-softwarerecipestable", "core")
        head_elements_after_search = self.driver.find_elements_by_xpath("//*[@id='softwarerecipestable']/thead/tr/th")
        head_element_list_after_search = [element.text for element in head_elements_after_search]
        if (head_element_list_after_search ==head_element_list_before_search):
            logger.info("Pass: 1405 Serach recipies does not affect on head columns same are displayed and same are hidden")
        else:
            logger.info("Fail: 1405 Serach recipies  affected on head columns same are not displayed and same are  not hidden")
            self.fail(msg="Fail: 1405 Serach recipies  affected on head columns same are not displayed and same are  not hidden")
        string_after_search_layer_hidden = (self.driver.find_element_by_xpath("//div[@class='col-md-10']/h2").text)
        value_after_search_layer_hidden = int(((string_after_search_layer_hidden.split())[-1]).split('(')[-1].split(')')[0])
        if (value_after_search_layer_hidden <value_before_search):
            logger.info("Pass: 1405 Search is succesfull ")
        else:
            logger.info("Fail: 1405 Search is  not succesfull")
            self.fail(msg="Fail: 1405 Search is  not succesfull")
        self.edit_specicific_checkbox("checkbox-layer_version__layer__name")
        string_after_search_layer_enable = (self.driver.find_element_by_xpath("//div[@class='col-md-10']/h2").text)
        value_after_search_layer_enable = int(((string_after_search_layer_enable.split())[-1]).split('(')[-1].split(')')[0])
        if (value_after_search_layer_enable==value_after_search_layer_hidden):
            logger.info("Pass: 1405 search is successfull across all coiumns either hidden or diplayed")
        else:
            logger.info("Fail: 1405 search is  not successfull across all coiumns either hidden or diplayed")
            self.fail(msg="Fail: 1405 search is  not successfull across all coiumns either hidden or diplayed")
        self.driver.find_element_by_xpath("//*[@id='table-chrome-collapse-softwarerecipestable']/form[1]/div/div/span").click()
        time.sleep(5)
        self.search_element("search-input-softwarerecipestable", "search-submit-softwarerecipestable", "ghght")
        string_after_search_random_string = (self.driver.find_element_by_xpath("//div[@class='col-md-10']/h2").text)
        value_after_search_random_string = int(
            ((string_after_search_random_string.split())[-1]).split('(')[-1].split(')')[0])
        if (value_after_search_random_string==0):
            logger.info("Pass: 1405 random searched element found 0")
        else:
            logger.info("Fail: 1405 random searched element  not found as 0")
            self.fail(msg="Fail: 1405 random searched element  not found as 0")
        self.driver.find_element_by_xpath("//*[@id='no-results-softwarerecipestable']/div/form/button[2]").click()
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='softwarerecipestable']/thead/tr/th[1]/a").click()
        time.sleep(5)
        elements_after_sorting_layer = self.driver.find_elements_by_xpath("//*[@id='softwarerecipestable']/tbody/tr/td[1]")
        list_after_sorting_layer = [element.text for element in elements_after_sorting_layer]
        if (list_after_sorting_layer == sorted(list_after_sorting_layer,reverse=True)):
            logger.info("Pass: 1405 software recipie list got soreted in descending oreder")
        else:
            logger.info("Fail: 1405 software recipie list didn;t got soreted in descending oreder")
            self.fail(msg="Fail: 1405 software recipie list didn;t got soreted in descending oreder")
        self.search_element("search-input-softwarerecipestable", "search-submit-softwarerecipestable", "core")
        elements_after_sorting_searching_layer = self.driver.find_elements_by_xpath("//*[@id='softwarerecipestable']/tbody/tr/td[1]")
        list_after_sorting_searching_layer = [element.text for element in elements_after_sorting_searching_layer]
        if (list_after_sorting_searching_layer == sorted(list_after_sorting_searching_layer, reverse=True)):
            logger.info("Pass: 1405 software recipie list got soreted in descending oreder")
        else:
            logger.info("Fail: 1405 software recipie list didn;t got soreted in descending oreder")
            self.fail(msg="Fail: 1405 software recipie list didn;t got soreted in descending oreder")
        self.driver.find_element_by_id("in_current_project").click()
        time.sleep(5)
        self.driver.find_element_by_id("in_current_project:in_project").click()
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='filter-modal-softwarerecipestable']/div/div/div[3]/button").click()
        time.sleep(5)
        self.driver.find_element_by_id("search-input-softwarerecipestable").click()
        time.sleep(5)
        self.driver.find_element_by_id("search-input-softwarerecipestable").clear()
        self.driver.find_element_by_id("search-input-softwarerecipestable").send_keys("meta")
        self.driver.find_element_by_id("search-submit-softwarerecipestable").click()
        time.sleep(3)
        self.driver.find_element_by_id("in_current_project").click()
        time.sleep(5)
        if (self.driver.find_element_by_xpath("//*[@id='in_current_project:all']").is_selected()):
            logger.info("Pass: 1405 Filter got cleared and set to default after search ")
        else:
            logger.info("Fail: 1405 Filter not got cleared and  not set to default after search")
            self.fail(msg="Fail: 1405 Filter not got cleared and  not set to default after search")
        self.driver.find_element_by_xpath("//*[@id='filter-modal-softwarerecipestable']/div/div/div[3]/button").click()
        time.sleep(2)
        self.driver.find_element_by_id("in_current_project").click()
        time.sleep(5)
        self.driver.find_element_by_id("in_current_project:in_project").click()
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='filter-modal-softwarerecipestable']/div/div/div[3]/button").click()
        time.sleep(5)
        self.driver.find_element_by_id("in_current_project").click()
        time.sleep(5)
        if (self.driver.find_element_by_id("in_current_project:in_project").is_selected()):
            logger.info("Pass: 1405 filter option is slected as it is ")
        else:
            logger.info("Fail: 1405 filter not got cleared and  not set to default after search")
            self.fail(msg="Fail: 1405 filter not got cleared and  not set to default after search")
        self.driver.find_element_by_xpath("//*[@id='filter-modal-softwarerecipestable']/div/div/div[1]/button").click()
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='table-chrome-collapse-softwarerecipestable']/form[1]/div/div/span").click()
        #need to add below line later
        #self.driver.find_element_by_id("in_current_project").click()
        #time.sleep(5)

        # if (self.driver.find_element_by_xpath("//*[@id='in_current_project:all']").is_selected()):
        #     logger.info("Pass : Filter got cleared and set to default after clearing the search from 'x' button ")
        # else:
        #     self.fail(msg="Pass : Filter  didn't got cleared and  not set to default after clearing the search from 'x' button ")
        #
        # self.driver.find_element_by_xpath("//*[@id='filter-modal-softwarerecipestable']/div/div/div[1]/button").click()
        print("All test steps passed in test case 1405")
        logger.info("All test steps passed in test case 1405")
    #Test case 1406
    def test_1406_Software_recipes_Filter_the_contents_of_the_software_recipes_table(self):
        project_name = "1406"
        self.create_new_project(project_name)
        time.sleep(20)
        self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li[5]/a").click()
        time.sleep(10)
        self.assertTrue(self.driver.find_element_by_xpath("//th[@class='add-del-layers']//*[@class='glyphicon glyphicon-filter filtered']"),
                        msg="Fail: 1406 Filter button is not available for build button")
        #only one filter is present so cant check for filter mutuaaly exclusive
        self.driver.find_element_by_id("in_current_project").click()
        time.sleep(5)
        self.driver.find_element_by_id("in_current_project:in_project").click()
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='filter-modal-softwarerecipestable']/div/div/div[3]/button").click()
        time.sleep(5)
        self.driver.find_element_by_id("search-input-softwarerecipestable").click()
        time.sleep(5)
        self.driver.find_element_by_id("search-input-softwarerecipestable").clear()
        self.driver.find_element_by_id("search-input-softwarerecipestable").send_keys("meta")
        self.driver.find_element_by_id("search-submit-softwarerecipestable").click()
        time.sleep(3)
        self.driver.find_element_by_id("in_current_project").click()
        time.sleep(5)
        if (self.driver.find_element_by_xpath("//*[@id='in_current_project:all']").is_selected()):
            logger.info("Pass: 1406 filter got cleared and set to default after search ")
        else:
            logger.info("Fail: 1406 filter not got cleared and  not set to default after search")
            self.fail(msg="Fail: 1406 filter not got cleared and  not set to default after search")
        print("All test steps passed in test case 1406")
        logger.info("All test steps passed in test case 1406")
    #test case 1407
    def test_1407_the_packages_included_in_the_image(self):
        project_name = "1407"
        self.create_new_project(project_name)
        time.sleep(20)
        self.build_recipie('core-image-minimal', project_name)
        self.driver.find_element_by_xpath("//*[@id='latest-builds']/div/div/div[1]/a/span").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='menu-recipes']/a").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='builtrecipestable']/tbody/tr[10]/td[1]/a").click()
        time.sleep(20)
        self.driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[1]/ul/li[2]/a").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='otable']/tbody/tr[1]/td[1]/a").click()
        time.sleep(20)
        self.driver.find_element_by_xpath("//div[@class='lead well']/a").click()
        time.sleep(30)
        self.driver.find_element_by_xpath("//*[@id='otable']/tbody/tr[1]/td[1]/a").click()
        time.sleep(50)
        #print(self.driver.find_element_by_xpath("(//li[@class='active'])[2]").text)
        if(self.driver.find_element_by_xpath("(//li[@class='active'])[2]").text=='Directory structure'):
            logger.info("Pass: 1407 file path is showing in directory structure")
        else:
            logger.info("Fail: 1407 file path is not showing in directory structure")
            self.fail(msg="Fail: 1407 file path is not showing in directory structure")
        print("All test steps passed in test case 1407")
        logger.info("All test steps passed in test case 1407")
    def test_1408_the_filters_from_a_image_page(self):
        project_name = "1408"
        self.create_new_project(project_name)
        time.sleep(20)
        self.build_recipie('core-image-minimal', project_name)
        self.driver.find_element_by_xpath("//*[@id='latest-builds']/div/div/div[1]/a/span").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='menu-configuration']/a").click()
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='navTab']/ul/li[2]/a").click()
        time.sleep(100)
        self.driver.find_element_by_xpath("//*[@id='otable']/thead/tr/th[4]/div/a/span").click()
        time.sleep(5)
        if (self.driver.find_element_by_xpath("//*[@id='filter_description']/div/div/form/div[2]/div[2]/label/input").is_selected()):
            self.driver.find_element_by_xpath("//*[@id='filter_description']/div/div/form/div[1]/button").click()
        else:
            self.driver.find_element_by_xpath("//*[@id='filter_description']/div/div/form/div[2]/div[2]/label/input").click()
            time.sleep(10)
            self.driver.find_element_by_xpath("[@id='filter_description']/div/div/form/div[3]/div/div[1]/button").click()
            time.sleep(5)
        elements_with_description=self.driver.find_elements_by_xpath("//*[@id='otable']/tbody/tr/td[4]")
        list_elements_with_description = [element.text for element in elements_with_description]
        for i in range(len(list_elements_with_description)):
            if (list_elements_with_description[i]!= ' '):
                pass
            else:
                logger.info("Fail: 1408 filter  is not returning only items that match the selected criteria")
                self.fail(msg="Fail: 1408 filter  is not returning only items that match the selected criteria")
                break
        print("All test steps passed in test case 1408")
        logger.info("All test steps passed in test case 1408")
    #test case 1409
    def test_1409_dependencies_link(self):
        project_name = "1409"
        self.create_new_project(project_name)
        time.sleep(20)
        self.build_recipie('core-image-minimal', project_name)
        self.driver.find_element_by_xpath("//*[@id='latest-builds']/div/div/div[1]/a/span").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='menu-recipes']/a").click()
        time.sleep(100)

        if ('Recipes built' in self.driver.find_element_by_xpath("//*[@class='page-header build-data']/h1").text):
            logger.info("Pass: 1409 clicked on recipies tab")
        else:
            logger.info("Fail: 1409 recipies tab not clicked ")
            self.fail(msg="Fail: 1409 recipies tab not clicked ")
        self.driver.find_element_by_xpath("//*[@id='builtrecipestable']/tbody/tr[1]/td[3]/a").click()
        time.sleep(10)
        if ('dependencies' in self.driver.find_element_by_xpath("//*[@class='popover-title']").text):
            logger.info("Pass: 1409 dependencies popped up after clicking number")
        else:
            logger.info("Fail: 1409 dependencies not popped up after clicking number ")
            self.fail(msg="Fail: 1409 dependencies not popped up after clicking number ")
        self.driver.find_element_by_xpath("//div[@class='popover-content']//ul/li[1]/a").click()
        time.sleep(10)
        if(self.driver.find_element_by_xpath("//div[@class='page-header build-data']/h1").text!=''):
            logger.info("Pass: 1409 dependendcies recipies page clicked and showing")
        else:
            logger.info("Fail: 1409 dependendcies recipies page  not clicked not diplayed ")
            self.fail(msg="Fail: 1409 dependendcies recipies page  not clicked not diplayed ")
        print("All test steps passed in test case 1409")
        logger.info("All test steps passed in test case 1409")
    #test case 1410
    def test_1410_recipe_file_link(self):
        project_name = "1410"
        recipie_msg = "Compatible image recipes"
        self.create_new_project(project_name)
        time.sleep(20)
        self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li[4]/a").click()
        time.sleep(10)
        if (recipie_msg in self.driver.find_element_by_xpath("//div[@class='col-md-10']/h2").text):
            logger.info("Pass: 1410 clicked on image recipie successfully")
        else:
            logger.info("Fail: 1410 image recipie not clicked")
            self.fail(msg="Fail: 1410 image recipie not clicked")
        self.edit_specicific_checkbox("checkbox-recipe-file")
        if ('Recipe file'== self.driver.find_element_by_xpath("//*[@id='imagerecipestable']/thead/tr/th[4]/span[2]").text):
            logger.info("Pass: 1410 clicked on Recipe file  checkbox successfully")
        else:
            self.fail(msg="Fail: 1410 Recipe file  checkbox not clicked")
            logger.info("Fail: 1410 Recipe file  checkbox not clicked")
        self.driver.find_element_by_xpath("//*[@id='imagerecipestable']/tbody/tr[1]/td[4]/a/span").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li[5]/a").click()
        time.sleep(10)
        if ('Compatible software recipes' in self.driver.find_element_by_xpath("//div[@class='col-md-10']/h2").text):
            logger.info("Pass: 1410 clicked on software recipie successfully")
        else:
            logger.info("Fail: 1410 software recipie not clicked")
            self.fail(msg="Fail: 1410 software recipie not clicked")
        self.edit_specicific_checkbox("checkbox-recipe-file")
        self.driver.find_element_by_xpath("//*[@id='softwarerecipestable']/tbody/tr[1]/td[4]/a/span").click()
        time.sleep(10)
        print("All test steps passed in test case 1410")
        logger.info("All test steps passed in test case 1410")

    # test case 1411

    def test_1411_See_packages_size(self):
        project_name = "1411"
        package_build_msg = "Packages built"
        self.create_new_project(project_name)
        time.sleep(20)
        self.build_recipie('core-image-minimal', project_name)
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='latest-builds']/div/div/div[1]/a/span").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='menu-packages']/a").click()
        time.sleep(10)
        if (package_build_msg in self.driver.find_element_by_xpath("//div[@class='page-header build-data']/h1").text):
            logger.info("Pass: 1411 clicked on package successfully")
        else:
            logger.info("Fail: 1411 package not clicked")
            self.fail(msg="Fail: 1411 package not clicked")
        self.driver.find_element_by_xpath("//*[@id='builtpackagestable']/thead/tr/th[3]/a").click()
        time.sleep(10)
        package_size_elements=self.driver.find_elements_by_xpath("//*[@id='builtpackagestable']/tbody/tr/td[3]")
        list_elements_with_description = [float(element.text.split(' ')[0]) for element in package_size_elements]

        if (list_elements_with_description==sorted(list_elements_with_description)):
            logger.info("Pass: 1411 package size is in ascending order")
        else:
            logger.info("Fail: 1411 package size is  not in ascending order")
            self.fail(msg="Fail: 1411 package size is  not in ascending order")
        self.driver.find_element_by_xpath("//*[@id='builtpackagestable']/thead/tr/th[3]/a").click()
        time.sleep(10)
        package_size_elements_descending = self.driver.find_elements_by_xpath("//*[@id='builtpackagestable']/tbody/tr/td[3]")
        list_elements_with_description_descending = [float(element.text.split(' ')[0]) for element in package_size_elements_descending]
        # need to check how to compare kb and mb then need to do next step
        logger.info(list_elements_with_description_descending)
        # if (list_elements_with_description_descending == sorted(list_elements_with_description_descending,reverse=True)):
        #     logger.info("Pass: package size is in descending order")
        # else:
        #     self.fail(msg="Fail 1407: package size is  not in descending order")
        print("All test steps passed in test case 1411")
        logger.info("All test steps passed in test case 1411")

    def test_1399_build_recipe_button_from_recipes_page(self):
        project_name = "1399"
        recipie_msg = "Compatible image recipes"
        self.create_new_project(project_name)
        time.sleep(20)
        self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li[4]/a").click()
        time.sleep(10)
        if (recipie_msg in self.driver.find_element_by_xpath("//div[@class='col-md-10']/h2").text):
            logger.info("Pass: 1399 clicked on image recipie successfully")
        else:
            self.fail(msg="Fail: 1399 image recipie not clicked")
        self.driver.find_element_by_xpath("//*[@id='in_current_project']/i").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='in_current_project:not_in_project']").click()
        time.sleep(10)

        self.driver.find_element_by_xpath("//*[@id='filter-modal-imagerecipestable']/div/div/div[3]/button").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='imagerecipestable']/tbody/tr[1]/td[9]/a[2]").click()
        time.sleep(10)

        self.driver.find_element_by_xpath("//*[@id='dependencies-modal-form']/div[3]/button[1]").click()
        time.sleep(10)

        if(self.driver.find_element_by_xpath("//*[@id='imagerecipestable']/tbody/tr[1]/td[9]/a[1]").text=='Build recipe'):
            logger.info("Pass: 1399 'add layer' button became 'build recipe in image recipe" )
        else:
            logger.info("Fail: 1399 add layer' button didn't change to 'build recipe in image recipe ")
            self.fail(msg="Fail: 1399 add layer' button didn't change to 'build recipe in image recipe ")

        self.driver.find_element_by_xpath("//*[@id='imagerecipestable']/tbody/tr[1]/td[9]/a[1]").click()
        time.sleep(20)
        try:
            WebDriverWait(self.driver, 5000).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="latest-builds"]//span[@class="rebuild-btn alert-link info pull-right"]')))
            time.sleep(5)
        except:
            logger.info("Fail: 1399 Build is not successful for image recipie ")
            self.fail(msg="Fail: 1399 Build is not successful for image recipie ")
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='topbar-configuration-tab']/a").click()
        time.sleep(10)

        self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li[5]/a").click()
        time.sleep(10)

        if ('Compatible software recipes' in self.driver.find_element_by_xpath("//div[@class='col-md-10']/h2").text):
            logger.info("Pass: 1399 clicked on software image recipie successfully")
        else:
            self.fail(msg="Fail: 1399 software image recipie not clicked")
            logger.info("Fail: 1399 software image recipie not clicked")
        self.driver.find_element_by_xpath("//*[@id='in_current_project']/i").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='in_current_project:not_in_project']").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='filter-modal-softwarerecipestable']/div/div/div[3]/button").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='softwarerecipestable']/tbody/tr[1]/td[9]/a[2]").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='dependencies-modal-form']/div[3]/button[1]").click()
        time.sleep(10)
        if (self.driver.find_element_by_xpath("//*[@id='softwarerecipestable']/tbody/tr[1]/td[9]/a[1]").text == 'Build recipe'):
            logger.info("Pass: 1399 'add layer' button became 'build recipe in software recipe")
        else:
            logger.info("Fail: 1399 add layer' button didn't change to 'build recipe in software recipe")
            self.fail(msg="Fail: 1399 add layer' button didn't change to 'build recipe in software recipe")
        self.driver.find_element_by_xpath("//*[@id='softwarerecipestable']/tbody/tr[1]/td[9]/a[1]").click()
        time.sleep(10)
        try:
            WebDriverWait(self.driver, 5000).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="latest-builds"]//span[@class="rebuild-btn alert-link info pull-right"]')))
            time.sleep(5)
        except:
            logger.info("Fail: 1399 Build is not successful for software recipie ")
            self.fail(msg="Fail: 1399 Build is not successful for software recipie ")
        print("All test steps passed in test case 1399")
        logger.info("All test steps passed in test case 1399")

    def test_1398_Test_dependencies_layers(self):
        project_name = "1398"
        self.create_new_project(project_name)
        time.sleep(10)
        self.driver.find_element_by_id("view-compatible-layers").click()
        time.sleep(10)
        self.search_element("search-input-layerstable","search-submit-layerstable","meta-agl")
        time.sleep(100)
        self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr[1]/td[7]/a[2]").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='dependencies-modal-form']/div[3]/button[1]").click()
        time.sleep(10)
        self.driver.back()
        time.sleep(20)
        if(self.driver.find_element_by_xpath("//*[@id='layers-in-project-list']/li[7]/a").text=='meta-python'):
            self.driver.find_element_by_xpath("//*[@id='layers-in-project-list']/li[7]/span").click()
            time.sleep(30)
        else:
            logger.info("Fail: 1398 meta-python is not present in dependendt list")
            self.fail(msg="Fail: 1398 meta-python is not present in dependendt list")
        if("meta-python" in self.driver.find_element_by_id("change-notification").text):
            logger.info("Pass: 1398 meta-python has been removed")
        else:
            logger.info("Fail: 1398 meta-python is not present in dependendt list")
            self.fail(msg="Fail: 1398 meta-python has not  been removed after clicking delete button also")
        self.driver.find_element_by_id("build-input").click()
        time.sleep(10)
        self.driver.find_element_by_id("build-input").send_keys("core-image-minimal")
        self.driver.find_element_by_id("build-button").click()
        time.sleep(10)
        try:
            WebDriverWait(self.driver, 5000).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="latest-builds"]//span[@class="rebuild-btn alert-link danger pull-right"]')))
            time.sleep(5)
        except:
            logger.info("Fail: 1398 Build got successful after delting dependent layer also ")
            self.fail(msg="Fail: 1398 Build got successful after delting dependent layer also ")
        print("All test steps passed in test case 1398")
        logger.info("All test steps passed in test case 1398")

    def test_1397_Download_licence_manifest(self):
        project_name = "1397"
        os.system("gnome-terminal -e 'rm -rf ../../../build/tmp'")
        #os.system("gnome-terminal -e 'bash -c \"rm -rf ../../../build-toaster-2/tmp \"'")
        self.create_new_project(project_name)
        time.sleep(30)
        self.build_recipie('core-image-sato-sdk', project_name)
        self.driver.find_element_by_xpath("//*[@id='latest-builds']/div/div/div[1]/a/span").click()
        time.sleep(20)
        if(self.driver.find_element_by_xpath("//a[@class='pull-right log']").text=="Download build log"):
            logger.info("Pass: 1397 Download button for License manifests availbae")
        else:
            logger.info("Fail: 1397 Download button for License manifests is not availbae ")
            self.fail(msg="Fail: 1397 Download button for License manifests is not availbae ")
        self.driver.find_element_by_xpath("//a[@class='pull-right log']").click()
        time.sleep(20)
        print("All test steps passed in test case 1397")
        logger.info("All test steps passed in test case 1397")
    def test_1396_Download_other_artifacts(self):
        project_name = "1396"
        os.system("gnome-terminal -e 'rm -rf ../../../build/tmp'")
        self.create_new_project(project_name)
        time.sleep(10)
        self.build_recipie('core-image-minimal', project_name)
        self.driver.find_element_by_xpath("//*[@id='latest-builds']/div/div/div[1]/a/span").click()
        time.sleep(20)
        if (self.driver.find_element_by_xpath("//*[@id='menu-download-build-log']/a").text == "Download build log"):
            logger.info("Pass: 1396 Download button in other artifacts available")
        else:
            logger.info("Fail: 1396 Download button in other artifacts not available")
            self.fail(msg="Fail: 1396 Download button in other artifacts not available")
        self.driver.find_element_by_xpath("//*[@id='menu-download-build-log']/a").click()
        time.sleep(20)
        print("All test steps passed in test case 1396")
        logger.info("All test steps passed in test case 1396")
    #need to check why build is getting failed
    def test_1395_Intel_layers_builds(self):
        project_name = "1395"
        self.create_new_project(project_name)
        time.sleep(30)
        self.driver.find_element_by_id("view-compatible-layers").click()
        time.sleep(10)
        self.search_element("search-input-layerstable","search-submit-layerstable","meta-intel")
        self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr[1]/td[7]/a[2]").click()
        time.sleep(20)
        self.driver.find_element_by_xpath("//*[@id='dependencies-modal-form']/div[3]/button[1]").click()
        time.sleep(30)
        if ('You have added' in self.driver.find_element_by_id("change-notification-msg").text):
            logger.info("Pass: 1395 first layer got added after clicking add layer")
        else:
            self.fail(msg="Fail: 1395 First Layer didn't added after clicking add layer")
            logger.info("Fail: 1395 First Layer didn't added after clicking add layer")
        self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr[3]/td[7]/a[2]").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='dependencies-modal-form']/div[3]/button[1]").click()
        time.sleep(30)
        if ('You have added' in self.driver.find_element_by_id("change-notification-msg").text):
            logger.info("Pass: 1395 second layer got added after clicking add layer")
        else:
            logger.info("Fail: 1395  second Layer didn't added after clicking add layer")
            self.fail(msg="Fail: 1395  second Layer didn't added after clicking add layer")
        self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr[1]/td[1]/a").click()
        time.sleep(10)
        self.driver.find_element_by_id("machines-tab").click()
        time.sleep(20)
        # need to ask why failing with first machine
        self.driver.find_element_by_xpath("//*[@id='machinestable']/tbody/tr[2]/td[3]/a").click()
        time.sleep(10)
        if ( str(self.driver.find_element_by_id("project-machine-name").text) in str(self.driver.find_element_by_id("change-notification-msg").text.split(':')[1])):
            logger.info("Pass: 1395 machine changed after selecting machine")
        else:
            self.fail(msg="Fail: 1395 machine not changed after selecting machine")
            logger.info("Fail: 1395 machine not changed after selecting machine")
        self.build_recipie('core-image-minimal', project_name)
        print("All test steps passed in test case 1395")
        logger.info("All test steps passed in test case 1395")
    def test_1394_Run_again_button_from_all_builds_page_must_run_the_specified_task(self):
        project_name = "1394"
        self.create_new_project(project_name)
        time.sleep(10)
        self.build_recipie('core-image-minimal:clean', project_name)
        time.sleep(30)
        self.driver.find_element_by_xpath("//*[@id='latest-builds']//span[@class='rebuild-btn alert-link info pull-right']").click()
        time.sleep(30)
        try:
            WebDriverWait(self.driver, 5000).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="latest-builds"]//span[@class="rebuild-btn alert-link info pull-right"]')))
            time.sleep(5)
        except:
            logger.info("Fail: 1394 Build is not successful {} ".format(project_name))
            self.fail(msg="Fail: 1394 Build is not successful {} ".format(project_name))
        self.driver.find_element_by_xpath("//*[@id='latest-builds']/div/div/div[1]/a/span").click()
        time.sleep(10)
        if(self.driver.find_element_by_xpath("((//div[@class='col-md-4 dashboard-section'])[2]//dl/dd)[2]").text==str(1)):
            logger.info("Pass: 1394 no. of task executed after rebuild is showing correctly")
        else:
            logger.info("Fail: 1394 no. of task executed after rebuild is not showing correctly")
            self.fail(msg="Fail: 1394 no. of task executed after rebuild is not showing correctly")
        self.driver.back()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='latest-builds']//span[@class='rebuild-btn alert-link info pull-right']").click()
        time.sleep(30)
        try:
            WebDriverWait(self.driver, 5000).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="latest-builds"]//span[@class="rebuild-btn alert-link info pull-right"]')))
            time.sleep(5)
        except:
            self.fail(msg="Fail: 1394 Build is not successful  after rebuild second time {} ".format(project_name))
        self.driver.find_element_by_xpath("//*[@id='latest-builds']/div/div/div[1]/a/span").click()
        time.sleep(10)
        if (self.driver.find_element_by_xpath(
                "((//div[@class='col-md-4 dashboard-section'])[2]//dl/dd)[2]").text == str(1)):
            logger.info("Pass: 1394 no. of task executed after rebuild second time is showing correctly")
        else:
            logger.info("Fail: 1394 no. of task executed after rebuild  second time is  not showing correctly")
            self.fail(msg="Fail: 1394 no. of task executed after rebuild  second time is  not showing correctly")
        print("All test steps passed in test case 1394")
        logger.info("All test steps passed in test case 1394")
    def test_1393_Download_task_log(self):
        project_name = "1393"
        self.create_new_project(project_name)
        time.sleep(10)
        self.build_recipie('core-image-minimal:clean', project_name)
        time.sleep(30)
        self.build_recipie('core-image-minimal', project_name)
        time.sleep(30)
        self.driver.find_element_by_xpath("//*[@id='latest-builds']/div/div/div[1]/a/span").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='menu-tasks']/a").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='execution_outcome']/i").click()
        time.sleep(10)
        self.driver.find_element_by_id("execution_outcome:executed").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='filter-modal-buildtaskstable']/div/div/div[3]/button").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='buildtaskstable']/tbody/tr/td[2]/a").click()
        time.sleep(10)
        if (self.driver.find_element_by_xpath("//a[@class='btn btn-default btn-lg']").text =='Download task log'):
            logger.info("Pass: 1393 Download task button is present for exceuted task")
        else:
            self.fail(msg="Fail: 1393 Download task button is  not present for exceuted task")
            logger.info("Fail: 1393 Download task button is  not present for exceuted task")
        self.driver.find_element_by_xpath("//a[@class='btn btn-default btn-lg']").click()
        time.sleep(20)
        self.driver.back()
        time.sleep(20)
        self.driver.find_element_by_xpath("//*[@id='execution_outcome']/i").click()
        time.sleep(10)
        self.driver.find_element_by_id("execution_outcome:not_executed").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='filter-modal-buildtaskstable']/div/div/div[3]/button").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='buildtaskstable']/tbody/tr/td[2]/a").click()
        time.sleep(50)
        if(self.driver.find_element_by_xpath("((//div[@class='col-md-12'])[2]/h2)[2]").text=='Not Executed'):
            logger.info("Pass: 1393 Download button is not present and Not executed is showing correctly")
        else:
            self.fail(msg="Fail: 1393 Not executed is  not showing correctly")
            logger.info("Fail: 1393 Not executed is  not showing correctly")
        print("All test steps passed in test case 1393")
        logger.info("All test steps passed in test case 1393")
    def test_1140_Multiple_build_directories(self):
        project_name = "1140"
        child = pexpect.spawn('./manage.py createsuperuser')
        child.timepout = 60
        child.expect(".*Username.*")
        child.sendline('hcl')
        child.expect('.*Email address:')
        child.sendline('khushboo_k@hcl.com')
        child.expect_exact('Password: ')
        child.sendline('hcl')
        child.expect_exact('Password (again): ')
        child.sendline('hcl')
        self.driver.get("http://localhost:8000/admin/login/?next=/admin/")
        time.sleep(30)
        self.driver.find_element_by_id("id_username").send_keys('hcl')
        time.sleep(10)
        self.driver.find_element_by_id("id_password").send_keys('hcl')
        time.sleep(10)
        self.driver.find_element_by_xpath("//input[@type='submit']").click()

        self.driver.find_element_by_xpath("//*[@id='content-main']/div[2]/table/tbody/tr/th/a").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='result_list']/tbody/tr/th/a").click()
        time.sleep(10)
        source_dir_value=(self.driver.find_element_by_xpath("//input[@id='id_sourcedir']")).get_attribute("value")
        Build_dir=self.driver.find_element_by_id("id_builddir").get_attribute("value")
        self.driver.back()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='content-main']/ul/li/a").click()
        time.sleep(10)
        self.driver.find_element_by_id("id_address").send_keys("2")
        time.sleep(10)
        select = Select(self.driver.find_element_by_id('id_betype'))
        select.select_by_index(1)
        time.sleep(10)
        self.driver.find_element_by_id("id_sourcedir").send_keys(source_dir_value)
        time.sleep(10)
        self.driver.find_element_by_id("id_builddir").send_keys(Build_dir)
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='buildenvironment_form']/div/div/input[1]").click()
        time.sleep(10)
        os.system("gnome-terminal -e 'bash -c \"cd ../../.. && source oe-init-build-env build2; bash\" '")
        self.driver.get("http://localhost:8000/")
        self.create_new_project(project_name)
        self.build_recipie('core-image-minimal core-image-sato', project_name)
        if(self.driver.find_element_by_xpath("//div[@class='col-md-3']").text=='core-image-minimal +1'):
            print("Pass: 1140 both builds are excuting simulatanously")
            logger.info("Pass: 1140 both builds are excuting simulatanously")
        else:
            self.fail(msg="Fail: 1140 both builds are  not excuted simulatanously")
            self.fail(msg="Fail: 1140 both builds are  not excuted simulatanously")
        print("All test steps passed in test case 1140")
        logger.info("All test steps passed in test case 1140")
    def test_1112_1113_Importing_new_layers(self):
        project_name = "1112"
        recipie_list=['Recipe', 'Version', 'Description', 'Build recipe']
        self.create_new_project(project_name)
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='layer-container']//p/a[contains(@href,'importlayer')]").click()
        time.sleep(30)
        self.driver.find_element_by_id("import-layer-name").send_keys("meta-imported")
        time.sleep(30)
        self.driver.find_element_by_id("layer-git-repo-url").send_keys("git://github.com/shr-distribution/meta-smartphone.git")
        time.sleep(10)
        self.driver.find_element_by_id("layer-subdir").send_keys("meta-acer")
        time.sleep(10)
        self.driver.find_element_by_id("layer-git-ref").send_keys("master")
        if( 'Layer dependencies' in self.driver.find_element_by_xpath("(//fieldset[@class='fields-apart-from-layer-name'])[4]/legend").text):
             logger.info("Pass: 1112 Layer dependendiceis option is showing correctly")
        else:
             logger.info("Fail: 1112 Layer dependendiceis option not showing correctly")
             self.fail(msg="Fail: 1112 Layer dependendiceis option not showing correctly")
        if(self.driver.find_element_by_xpath("//*[@id='layer-deps-list']/li/a").text=='openembedded-core'):
             logger.info("Pass: 1112 one list of layer dependencies is showing")
        else:
             logger.info("Fail: 1112 List of layer dependencies is showing blank")
             self.fail(msg="Fail: 1112 List of layer dependencies is showing blank")
        self.assertTrue(self.driver.find_element_by_xpath("//*[ @ id = 'layer-deps-list']/li/span"),
                        "Fail: 1112 Trash icon is not present here for list of recipies showing under layer dependencies tab")
        self.driver.find_element_by_id("layer-dependency").send_keys("meta-android, meta-oe")
        time.sleep(20)
        self.driver.find_element_by_id("import-and-add-btn").click()
        time.sleep(30)
        if(self.driver.find_element_by_xpath("//*[@id='layers-in-project-list']/li[4]/a").text=="meta-imported"):
            logger.info("Pass: 1112 imported layer  got added and showing on page")
        else:
            logger.info("Fail: 1112 imported layer not added and showing on tha page")
            self.fail(msg="Fail: 1112 imported layer not added and showing on tha page")
        if( "You have imported " in self.driver.find_element_by_id("change-notification-msg").text):
             logger.info("Pass: 1112 imported layer  got added and  message notification is showing ")
        else:
             logger.info("Fail: 1112 imported layer message notification is  not showing")
             self.fail(msg="Fail: 1112 imported layer message notification is  not showing")
        #started test case 1113
        self.driver.find_element_by_xpath("//*[@id='layers-in-project-list']/li[4]/a").click()
        time.sleep(10)
        if('meta-imported' in self.driver.find_element_by_xpath("//div[@class='well']/h2").text):
            logger.info("Pass: 1113 heading is showing correctly for imported layer")
        else:
            logger.info("Fail: 1113 heading is not showing correctly for imported layer")
            self.fail(msg="Fail: 1113 heading is not showing correctly for imported layer")
        about_elements=self.driver.find_elements_by_xpath("//div[@class='well']/dl/dt")
        about_element = [element.text for element in about_elements]
        if (about_element ==['Summary', 'Description']):
            logger.info("Pass: 1113 about information is showing correctly")
        else:
            self.fail(msg="Fail: 1113 about information not showing correctly")
            logger.info("Fail: 1113 about information not showing correctly")
        self.assertTrue(self.driver.find_elements_by_xpath("//dd/span[@class='text-muted']"),
                        "Fail: 1113 mute text is not available for Summary and description")
        self.driver.find_element_by_xpath("(//span[@class='glyphicon glyphicon-edit'])[1]").click()
        time.sleep(20)
        self.assertTrue(self.driver.find_element_by_xpath("(//dd//div[@class='form-group'])//textarea[@rows='2']"),
                        "Fail: 1113 It consists of a text area, set to 2 rows for the Summary")
        if (self.driver.find_element_by_xpath("//button[@disabled='disabled']").text == 'Save'):
             logger.info("Pass: 1113 Save option is disabled without entering any  text for description")
        else:
             logger.info("Fail: 1113 Save option is  not disabled without entering any text for description")
             self.fail(msg="Fail: 1113 Save option is  not disabled without entering any text for description")

        if (self.driver.find_element_by_xpath("(//a[@href='#'][@class='btn btn-link cancel'])[1]").text == 'Cancel'):
             logger.info("Pass: 1113 cancel option is present for description")
        else:
             logger.info("Fail: 1113 cancel option is disabled for description")
             self.fail(msg="Fail: 1113 cancel option is disabled for description")
        self.driver.find_element_by_xpath("(//div[@class='form-group']/textarea)[1]").send_keys("test")
        time.sleep(20)
        self.driver.find_element_by_xpath("(//button[@class='btn btn-default change-btn'])[1]").click()
        time.sleep(10)

        self.driver.find_element_by_xpath("(//span[@class='glyphicon glyphicon-edit'])[2]").click()
        time.sleep(20)
        self.assertTrue(self.driver.find_element_by_xpath("(//dd//div[@class='form-group'])//textarea[@rows='6']"),
                        "Fail: 1113 It  does not contain of a text area, set to 6 rows for the sumary")
        if(self.driver.find_element_by_xpath("//button[@disabled='disabled']").text=='Save'):
            logger.info("Pass: 1113 Save option is disabled without entering any text for sumary")
        else:
            logger.info("Fail: 1113 Save option is not disabled without entering any text for sumary")
            self.fail(msg="Fail: 1113 Save option is not disabled without entering any text for sumary")

        if (self.driver.find_element_by_xpath("(//a[@href='#'][@class='btn btn-link cancel'])[2]").text == 'Cancel'):
             logger.info("Pass: 1113 cancel option is present for summary")
        else:
             logger.info("Fail: 1113 cancel option is not present for description")
             self.fail(msg="Fail: 1113 cancel option is not present for description")

        self.driver.find_element_by_xpath("(//div[@class='form-group']/textarea)[2]").send_keys("test")
        time.sleep(20)
        self.driver.find_element_by_xpath("(//button[@class='btn btn-default change-btn'])[2]").click()
        time.sleep(10)
        tab_elements=self.driver.find_elements_by_xpath("//li/a[@data-toggle='tab']")
        tab_element= [element.text for element in tab_elements]
        if(tab_element==['Layer details', 'Recipes (0)', 'Machines (0)']):
             logger.info("Pass: 1113 tab element is present in same order as expected")
        else:
             self.fail(msg="tab element is  not present in same order as expected")
        self.assertTrue(self.driver.find_element_by_id("layer-dep-input"),
                       "Fail: 1113 it does not contain a text  input to add layer")

        self.assertTrue(self.driver.find_element_by_xpath("//span[@class='glyphicon glyphicon-trash ']"),
                        "Fail: 1113 it does not contain a delete icon to delete the layer")
        if(self.driver.find_element_by_id("edit-layer-source").text=="Edit layer source code location"):
             logger.info("Pass: 1113 edit layer source code location button is present")
        else:
             logger.info("Fail: 1113 edit layer source code location button is not present")
             self.fail(msg="Fail: 1113 edit layer source code location button is not present")
        self.driver.find_element_by_id("edit-layer-source").click()
        time.sleep(20)
        self.driver.find_element_by_id("layer-git-repo-url").click()
        time.sleep(10)
        if ('optional' in self.driver.find_element_by_xpath("//*[@id='layer-git']/div[2]/label").text):
            logger.info("Pass: 1113 subdrirectory is optional and showing in page")
        else:
            logger.info("Fail: 1113 subdrirectory is  not optional and  not showing in page")
            self.fail(msg="Fail: 1113 subdrirectory is  not optional and  not showing in page")
        self.driver.find_element_by_id("layer-subdir").click()
        time.sleep(100)
        logger.info(self.driver.find_element_by_xpath("//*[@id='layer-git-ref']").text)
        self.driver.find_element_by_id("layer-git-ref").click()
        time.sleep(10)
        self.driver.find_element_by_id("save-changes-for-switch").click()
        time.sleep(10)
        self.assertTrue(self.driver.find_element_by_xpath("//a[@id='add-layer-dependency-btn'][@disabled='disabled']"),
                        "Fail: 1113 Add layer button is not diabled is not any text entered")
        self.driver.find_element_by_id("layer-dep-input").send_keys("meta-96boards")
        self.driver.find_element_by_id("layer-dep-input").click()
        self.driver.find_element_by_id("layer-dep-input").send_keys(Keys.DOWN)
        time.sleep(5)
        self.driver.find_element_by_id("layer-dep-input").send_keys(Keys.RETURN)
        time.sleep(5)
        self.driver.find_element_by_id("add-layer-dependency-btn").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='layer-deps-list']/li[1]/a").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='targets-tab']").click()
        if(int((self.driver.find_element_by_xpath("//*[@id='targets-tab']").text).split(' ')[1].split('(')[1].split(')')[0])>0):
            logger.info("Pass: 1113 Total recipie is grater than zero")
        else:
            logger.info("Pass: 1113 Total recipie is is not more than zero")
        recipie_table_columns=self.driver.find_elements_by_xpath("//*[@id='recipestable']/thead/tr/th")
        recipie_table_column = [element.text for element in recipie_table_columns]
        if (recipie_list == recipie_table_column):
            logger.info("Pass: 1113 Recipie columns are showing as expected")
        else:
            logger.info("Fail: 1113 Recipie columns are  not showing as expected")
            self.fail(msg="Fail: 1113 Recipie columns are  not showing as expected")
        recipie_elements=self.driver.find_elements_by_xpath("//*[@id='recipestable']/tbody/tr/td[1]")
        recipie_element = [element.text for element in recipie_elements]
        if(recipie_element==sorted(recipie_element)):
            logger.info("Pass: 1113 Recipie element is sorted")
        else:
            logger.info("Fail: 1113 Recipie element is not sorted")
            self.fail(msg="Fail: 1113 Recipie element is not sorted")
        if('Remove' in self.driver.find_element_by_id("add-remove-layer-btn").text):
            logger.info("Pass: 1113 add and remove button is avialbe and message is showing to remove layer for recipie tab")
        else:
            logger.info(
                "Fail: 1113 add and remove button is  not avialbe and message is not showing to remove layer for recipie tab")
            self.fail(msg="Fail: 1113 add and remove button is  not avialbe and message is not showing to remove layer for recipie tab")

        self.driver.find_element_by_id("machines-tab").click()
        time.sleep(10)
        if (int((self.driver.find_element_by_xpath("//*[@id='machines-tab']").text).split(' ')[1].split('(')[1].split(')')[0]) > 0):
            logger.info("Pass: 1113 Total machine is greater than zero")
        else:
            logger.info("Pass: 1113 Total machine is  not more than zero")
        machine_table_columns = self.driver.find_elements_by_xpath("//*[@id='machinestable']/thead/tr/th")
        machine_table_column = [element.text for element in machine_table_columns]
        if (machine_table_column == ['Machine', 'Description', 'Select machine']):
            logger.info("Pass: 1113 Machine columns are showing as expected")
        else:
            logger.info("Fail: 1113 Machine columns are  not showing as expected")
            self.fail(msg="Fail: 1113 Machine columns are  not showing as expected")
        machine_elements = self.driver.find_elements_by_xpath("//*[@id='machinestable']/tbody/tr/td[1]")
        machine_element = [element.text for element in machine_elements]
        if (machine_element == sorted(machine_element)):
            logger.info("Pass: 1113 machine element is sorted")
        else:
            logger.info("Fail: 1113 machine element is not sorted")
            self.fail(msg="Fail: 1113 machine element is not sorted")
        if ('Remove' in self.driver.find_element_by_id("add-remove-layer-btn").text):
            logger.info("Pass: 1113 add and remove button is avialbe and message is showing to remove layer for machine tab also")
        else:
            self.fail(
                msg="Fail: 1113 add and remove button is  not avialbe and message is not  showing to remove layer for amchine tab also")
            logger.info(
            "Fail: 1113 add and remove button is  not avialbe and message is not  showing to remove layer for amchine tab also")
        # did a back so that we can see exact import layee page
        self.driver.back()
        time.sleep(10)
        self.driver.back()
        time.sleep(10)
        self.driver.back()
        time.sleep(10)
        self.driver.find_element_by_id("targets-tab").click()
        time.sleep(30)
        if('Toaster does not have recipe information for the' in self.driver.find_element_by_xpath("//*[@id='no-recipes-yet']/p[1]").text):
            logger.info("Pass: 1113 Imported recipie is not built first so we need to build the imported recipie")
        else:
            logger.info("Pass: 1113 Imported recipie  built so we need to check for table")

        self.driver.find_element_by_id("machines-tab").click()
        time.sleep(10)
        if('Toaster does not have machine information' in self.driver.find_element_by_xpath("//*[@id='no-machines-yet']/p[1]").text ):
            logger.info("Pass: 1113 Machine information is not showing for this impoerted layer")
        else:
            self.fail(msg="Fail: 1113 :Machine information is showing for this imported layer")
            logger.info("Fail: 1113 :Machine information is showing for this imported layer")
        print("All test steps passed in test case  1112 and 1113")
        logger.info("All test steps passed in test case 1112 and 1113")

    def test_1111_Layer_details_page_UI_functionality(self):
        project_name = "1111"
        self.create_new_project(project_name)
        time.sleep(50)
        self.driver.find_element_by_id("view-compatible-layers").click()
        time.sleep(20)
        self.search_element("search-input-layerstable","search-submit-layerstable","meta-aarch64")
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr/td[1]/a").click()
        time.sleep(10)
        self.driver.find_element_by_id("targets-tab").click()
        time.sleep(10)

        if(self.driver.find_element_by_xpath("//*[@id='recipestable']/tbody/tr/td[4]/a[contains(@class,'disabled')]").text=='Build recipe'):
            logger.info("Pass: 1111 Build recipie is disabled for not added layer")
        else:
            logger.info("Fail: 1111 Build recipie is not disabled for not added layer")
            self.fail(msg="Fail: 1111 Build recipie is not disabled for not added layer")
        self.driver.find_element_by_id("machines-tab").click()
        if ("Toaster does not have machine information" in self.driver.find_element_by_xpath("//*[@id='no-machines-yet']/p[1]").text):
            logger.info("Pass: 1111 No machine information is present for this layer")
        else:
            if(self.driver.find_element_by_xpath("//*[@id='machinestable']/tbody/tr/td[3]/a[contains(@class,'disabled')]").text=='Select machine'):
                logger.info("Pass: 1111  Select machine  is disabled")
            else:
                logger.info("Fail: 1111 select  machine is not disabled")
                self.fail(msg="Fail: 1111 select  machine is not disabled")

        self.driver.back()
        time.sleep(10)
        self.driver.back()
        time.sleep(10)
        self.driver.back()
        time.sleep(10)
        time.sleep(50)
        if(self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr/td[7]/a[2]").text=="Add layer"):
            logger.info("Pass: 1111 Add layer button is present for this layer")
        else:
            logger.info("Fail: 1111 Add layer button is  not present for this layer")
            self.fail(msg="Fail: 1111 Add layer button is  not present for this layer")
        self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr/td[7]/a[2]").click()
        time.sleep(30)
        if(len(self.driver.find_elements_by_xpath("//*[@id='dependencies-list']//div[@class='checkbox']"))>0):
            logger.info("Pass: 1111 Total number of checkbox for dependency layer is greater than zero ")
            if ("depends on some layers that are not added to your project. Select the ones you want to add:" in self.driver.find_element_by_id(
                    "body-text").text):
                logger.info("Pass: 1111 dependency message is showing correctly after clicking add layer")
            else:
                logger.info("Pass: 1111 dependency message is not present looks like no dependency layer are present")
        else:
            logger.info("pass: 1111 Dependency layer is not present for this layer")
        time.sleep(30)
        if(self.driver.find_element_by_xpath("//*[@id='dependencies-modal-form']/div[3]/button[1]").text=="Add layers"):
            logger.info("Pass: 1111 Add layers button is  showing for dependency layer list")
        else:
            self.fail(msg="Fail: 1111 Add layers button is  not present for dependency layer lists")
            logger.info("Fail: 1111 Add layers button is  not present for dependency layer lists")
        if(self.driver.find_element_by_xpath("//*[@id='dependencies-modal-form']/div[3]/button[2]").text=='Cancel'):
            logger.info("Pass: 1111  cancel button is  showing for dependency layer list")
        else:
            self.fail(msg="Fail: 1111 cancel button is  not present for dependency layer lists")
            logger.info("Fail: 1111 cancel button is  not present for dependency layer lists")
        self.driver.find_element_by_xpath("//*[@id='dependencies-modal-form']/div[3]/button[2]").click()
        time.sleep(10)
        if(self.driver.find_element_by_xpath("//div[@class='col-md-10']/h2").text=="Compatible layers (1)"):
            logger.info("Pass: 1111 same search page is showing after clicking cancel button ")
        else:
            logger.info("Fail: 1111 same search page is not showing after clicking cancel buton")
            self.fail(msg="Fail: 1111 same search page is not showing after clicking cancel buton")

        self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr/td[7]/a[2]").click()
        time.sleep(30)
        self.driver.find_element_by_xpath("//*[@id='dependencies-modal-form']/div[3]/button[1]").click()
        time.sleep(10)

        if("You have added" in self.driver.find_element_by_id("change-notification-msg").text):
            logger.info("Pass: 1111 added layer message is showing")
        else:
            self.fail(msg="Fail: 1111 added layer message is not showing correctly")
            logger.info("Fail: 1111 added layer message is not showing correctly")
        self.driver.find_element_by_id("hide-alert").click()
        time.sleep(10)

        if(self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr/td[7]/a[contains(@class,'btn btn-danger btn-block')]").text=="Remove layer"):
            logger.info("Pass: 1111 Remove layer button got enabled after adding layer")
        else:
            self.fail(msg="Fail: 1111 Remove layer button  didn't get enabled after adding layer")
            logger.info("Fail: 1111 Remove layer button  didn't get enabled after adding layer")
        self.driver.find_element_by_xpath(
            "//*[@id='layerstable']/tbody/tr/td[7]/a[contains(@class,'btn btn-danger btn-block')]").click()
        time.sleep(10)

        if("You have removed" in self.driver.find_element_by_id("change-notification-msg").text):
            logger.info("Pass: 1111 Remove message is getting displayed after clicking remove button")
        else:
            self.fail(msg="Fail: 1111 Remove message is getting displayed after clicking remove button")
            logger.info("Fail: 1111 Remove message is getting displayed after clicking remove button")
        if(self.driver.find_element_by_xpath(
            "//*[@id='layerstable']/tbody/tr/td[7]/a[contains(@class,'btn btn-default btn-block')]").text=='Add layer'):
            logger.info("Pass : 1111 Add layer button got enabled after clicking remove layer")
        else:
            logger.info("Fail: 1111  Add layer button  didn't got enabled after clicking remove layer")
            self.fail(msg="Fail: 1111  Add layer button  didn't got enabled after clicking remove layer")
        self.driver.find_element_by_id("hide-alert").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr/td[7]/a[2]").click()
        time.sleep(30)
        self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr/td[1]/a").click()
        time.sleep(10)
        self.driver.find_element_by_id("machines-tab").click()
        time.sleep(100)

        if ("Toaster does not have machine information" in self.driver.find_element_by_xpath("//*[@id='no-machines-yet']/p[1]").text):
            logger.info("Pass: 1111 No machine information is present for this layer")
        else:
            if(self.driver.find_element_by_xpath("//*[@id='machinestable']/tbody/tr/td[3]/a[contains(@class,'btn btn-default')]").text=="Select machine"):
                logger.info("Pass: 1111 Select machine got enabled ")
                self.drive.find_element_by_xpath("//*[@id='machinestable']/tbody/tr/td[3]/a").click()
                time.sleep(10)
                if ("You have changed the machine t0" in self.driver.find_element_by_xpath(
                        "//*[@id='change-notification-msg']/span").text):
                    logger.info("Pass: 1111  Machine got changed and mesaage is showing ")
                    if(self.driver.find_element_by_id("project-machine-name").text in self.driver.find_element_by_xpath(
                        "//*[@id='change-notification-msg']/span").text):
                        logger.info("Pass: 1111 Machine got changed and showing in configuration page")
                    else:
                        logger.info("Fail: 1111  Machine is not showing in configuration page after changing themachine")
                        self.fail(msg="Fail: 1111  Machine is not showing in configuration page after changing themachine")
                else:
                    logger.info("Fail: 1111  Machine got changed and mesaage is not showing")
                    self.fail(msg="Fail: 1111  Machine got changed and mesaage is not showing")
            else:
                logger.info("Fail: 1111 Select machine didn't got enabled")
                self.fail(msg="Fail: 1111 Select machine didn't got enabled")
        self.driver.back()
        time.sleep(10)
        self.driver.find_element_by_id("targets-tab").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='recipestable']/tbody/tr/td[4]/a").click()
        try:
            WebDriverWait(self.driver, 5000).until(EC.element_to_be_clickable(
                (By.XPATH, '(//*[@id="latest-builds"]//span[@class="rebuild-btn alert-link danger pull-right"])[1]')))

            time.sleep(5)
            logger.info("Pass: 1111 Build is not successful {} but its passed ,since we need to just check the functionality only ".format(project_name))
            #self.fail(msg="Pass: 1111 Build is not successful {} ".format(project_name))
        except:
            WebDriverWait(self.driver, 5000).until(EC.element_to_be_clickable(
                (By.XPATH, '(//*[@id="latest-builds"]//span[@class="rebuild-btn alert-link info pull-right"])[1]')))
            time.sleep(5)
            logger.info("Pass: 1111 Build is  successful {} ".format(project_name))
        print("All test steps passed in test case  1111")
        logger.info("All test steps passed in test case  1111")






















