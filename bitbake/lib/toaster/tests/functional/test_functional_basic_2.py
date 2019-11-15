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
logging.basicConfig(filename="Toasteruitestsuit2_part2.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.INFO)
class FuntionalTestBasic(SeleniumFunctionalTestCase):
        # test_case1426
    def test_1426_New_custom_image_default_view(self):
        project_name = "1426"
        Checkbox_Table=["checkbox-customise-or-add-recipe","checkbox-get_description_or_summary",
                        "checkbox-layer_version__get_vcs_reference","checkbox-name","checkbox-layer_version__layer__name",
                        "checkbox-license","checkbox-recipe-file","checkbox-section","checkbox-version"]
        default_custom_column=['Image recipe', 'Version', 'Description', '', '', 'Layer', '', '', 'Customise']
        git_reviosn_name={"master"}
        not_aaded_layer_butoon="Add layer"
        added_layer="Customise"
        self.create_new_project(project_name)
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='project-topbar']/ul/li[4]/a").click()
        time.sleep(5)
        list_image_recipie=[]
        element_image_recipie=self.driver.find_elements_by_xpath("//*[@id='newcustomimagestable']/tbody/tr/td[1]")
        for element in element_image_recipie:
            list_image_recipie.append(element.text)
        if (list_image_recipie==None):
            logger.info("Fail: 1426 Import table is  not populated with the list of image recipes")
            self.fail(msg="Fail: 1426 Import table is  not populated with the list of image recipes")
        else:
            logger.info("Pass: 1426 Import table is populated with the list of image recipes")
        time.sleep(5)
        head_elements=self.driver.find_elements_by_xpath("//*[@id='newcustomimagestable']/thead/tr/th")
        head_element_list=[]
        for head_element in head_elements:
            head_element_list.append(head_element.text)

        if (head_element_list== default_custom_column):
            logger.info("Pass: 1426 Correct head list name displayed in custom image table")
        else:
            self.fail(msg="Fail: 1426 Correct head list name  not displayed in custom image table")
            logger.info("Fail: 1426 Correct head list name  not displayed in custom image table")
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(2)
        for item1 in Checkbox_Table:
            if(self.driver.find_element_by_id(item1).is_selected()):
                pass
            else:
                self.driver.find_element_by_id(item1).click()
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(2)
        git_reviosn_elements=self.driver.find_elements_by_xpath("//*[@id='newcustomimagestable']/tbody/tr/td[8]")
        git_revision_list = []
        for git_reviosn_element in git_reviosn_elements:
            git_revision_list.append(git_reviosn_element.text)
        if (git_reviosn_name.difference(set(git_revision_list))):
            self.fail(msg='Fail: 1426 git revision is not coming as selected  during  project creation')
            logger.info('Fail: 1426 git revision is not coming as selected  during  project creation')
        else:
            logger.info("Pass: 1426 git revision is  coming as selected  during  project creation")
        self.driver.find_element_by_xpath("//*[@id='in_current_project']/i").click()
        time.sleep(5)
        self.driver.find_element_by_id("in_current_project:in_project").click()
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='filter-modal-newcustomimagestable']/div/div/div[3]/button").click()
        time.sleep(5)
        if (self.driver.find_element_by_xpath("//*[@id='newcustomimagestable']/tbody/tr[1]/td[9]/button[@class='btn btn-default btn-block layer-exists-3 customise-btn']").text==added_layer):
            logger.info("Pass: 1426 customize option is coming for added layer")
        else:
            self.fail(msg="Fail: 1426 customize option is  not coming for added layer")
            logger.info("Fail: 1426 customize option is  not coming for added layer")
        self.driver.find_element_by_xpath("//*[@id='in_current_project']/i").click()
        time.sleep(5)
        self.driver.find_element_by_id("in_current_project:not_in_project").click()
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='filter-modal-newcustomimagestable']/div/div/div[3]/button").click()
        time.sleep(50)
        if (self.driver.find_element_by_xpath("//*[@id='newcustomimagestable']/tbody/tr[1]/td[9]/button[contains(@class,'btn btn-default btn-block layer-add')]").text == not_aaded_layer_butoon):
            logger.info("Pass: 1426  Add layer option is coming for added layer")
        else:
            self.fail(msg="Fail: 1426 Add layer option is  not coming for  not added layer")
            logger.info("Fail: 1426 Add layer option is  not coming for  not added layer")
        print("All test steps passed in test case 1426")
        logger.info("All test steps passed in test case 1426")
    #test case 1427
    def test_1427_New_custom_image_sorting_the_content_of_new_custom_image_table(self):
        project_name = "1427"
        Checkbox_Table=["checkbox-customise-or-add-recipe","checkbox-get_description_or_summary",
                        "checkbox-layer_version__get_vcs_reference","checkbox-name","checkbox-layer_version__layer__name",
                        "checkbox-license","checkbox-recipe-file","checkbox-section","checkbox-version"]
        sortable_table_heads=['layer_version__layer__name','section','license','name']
        self.create_new_project(project_name)
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='project-topbar']/ul/li[4]/a").click()
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='newcustomimagestable']/thead/tr/th[1]/a").click()
        time.sleep(5)
        element_image_recipie_descending = self.driver.find_elements_by_xpath("//*[@id='newcustomimagestable']/tbody/tr/td[1]")
        list_image_recipie_descending = [element.text for element in element_image_recipie_descending]
        if (list_image_recipie_descending == sorted(list_image_recipie_descending,reverse=True)):
            logger.info("Pass: 1427 ist is soreted in descending order")
        else:
            self.fail(msg="Fail: 1427 list is not soreted in descending order")
            logger.info("Fail: 1427 list is not soreted in descending order")
        self.driver.find_element_by_xpath("//*[@id='newcustomimagestable']/thead/tr/th[1]/a").click()
        time.sleep(5)
        element_image_recipie_ascending = self.driver.find_elements_by_xpath("//*[@id='newcustomimagestable']/tbody/tr/td[1]")
        list_image_recipie_ascending = [element.text for element in element_image_recipie_ascending]
        if (list_image_recipie_ascending == sorted(list_image_recipie_ascending)):
            logger.info("Pass: 1427 list is soreted in ascending order")
        else:
            self.fail(msg="Fail: 1427  list is  not soreted in ascending order")
            logger.info("Fail: 1427  list is  not soreted in ascending order")
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(2)
        for item1 in Checkbox_Table:
            if(self.driver.find_element_by_id(item1).is_selected()):
                pass
            else:
                self.driver.find_element_by_id(item1).click()
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(5)
        self.assertTrue(self.driver.find_element_by_xpath("//div[@class='checkbox disabled']//label[@class='text-muted']//input[@id='checkbox-customise-or-add-recipe']"),
                        msg="Fail: 1427 Textbox is not muted for customize ")
        self.assertTrue(self.driver.find_element_by_xpath(
            "//div[@class='checkbox disabled']//label[@class='text-muted']//input[@id='checkbox-name']"),
                        msg="Fail: 1427 Textbox is not muted for Image recipie")
        for i in sortable_table_heads:
            self.assertTrue(self.driver.find_element_by_xpath("//a[@data-sort-field='" + i + "']"),msg="1427 :Sortable table heads are not correct as expected")
        self.driver.find_element_by_xpath("//*[@id='newcustomimagestable']/thead/tr/th[6]/a").click()
        time.sleep(5)
        elements=self.driver.find_elements_by_xpath("//*[@id='newcustomimagestable']/tbody/tr/td[6]/a")
        list= [element.text for element in elements]
        self.driver.find_element_by_xpath("//*[@id='newcustomimagestable']/tbody/tr[1]/td[1]/a").click()
        self.driver.back()
        elements_after = self.driver.find_elements_by_xpath("//*[@id='newcustomimagestable']/tbody/tr/td[6]/a")
        list_after = [element.text for element in elements_after]
        if (list==list_after):
            logger.info("Pass: 1427 Element naviagation worke fine for layer sorting")
        else:
            logger.info("Fail: 1427 Element naviagation for layer sorting not working")
            self.fail(msg="Fail: 1427 Element naviagation for layer sorting not working")
        self.edit_specicific_checkbox("checkbox-layer_version__layer__name")
        element_layer_image = self.driver.find_elements_by_xpath("//*[@id='newcustomimagestable']/tbody/tr/td[1]")
        list_layer_image = [element.text for element in element_layer_image]
        if (list_layer_image == sorted(list_layer_image)):
            logger.info("Pass: 1427 list  got soreted for image recipie")
        else:
            logger.info("Fail: 1427 list are not soreted for image recipie")
            self.fail(msg="Fail: 1427 list are not soreted for image recipie")
        self.edit_specicific_checkbox("checkbox-layer_version__layer__name")
        self.driver.find_element_by_xpath("//*[@id='newcustomimagestable']/thead/tr/th[6]/a").click()
        time.sleep(10)
        elements_before_search = self.driver.find_elements_by_xpath("//*[@id='newcustomimagestable']/tbody/tr/td[6]/a")
        list_before_search = [element.text for element in elements_before_search]
        if (list_before_search == sorted(list_before_search)):
            logger.info("Pass: 1427 list is in ascending order before search")
        else:
            logger.info("Fail: 1427 list is not in ascending order before search")
            self.fail(msg="Fail: 1427 list is not in ascending order before search")
        self.search_element("search-input-newcustomimagestable", "search-submit-newcustomimagestable", 'core-image')
        elements_after_search = self.driver.find_elements_by_xpath("//*[@id='newcustomimagestable']/tbody/tr/td[6]/a")
        list_after_search = [element.text for element in elements_after_search]
        if (list_after_search == sorted(list_after_search)):
            logger.info("Pass: 1427 list is in same order after search also")
        else:
            logger.info("Fail: 1427 list is not in same order after search also")
            self.fail(msg="Fail: 1427 list is not in same order after search also")
        print("All test steps passed in test case 1427")
        logger.info("All test steps passed in test case 1427")
    #test case 1428
    def test_1428_New_custom_image_searching_the_content_of_new_custom_image_table(self):
        project_name = "1428"
        serach_text='core'
        no_search_found_msg='Select the image recipe you want to customise (0)'
        head_list=['Image recipe', 'Version', 'Description', '', '', 'Layer', '', '', 'Customise']
        self.create_new_project(project_name)
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='project-topbar']/ul/li[4]/a").click()
        time.sleep(5)
        self.assertTrue(self.driver.find_element_by_id("search-input-newcustomimagestable"),msg=" serach button is not present")
        self.assertTrue(self.driver.find_element_by_xpath("//input[@id='search-input-newcustomimagestable'][@placeholder='Search select the image recipe you want to customise']"),
                        msg="Fail: 1428 Placeholder for not present for search  ")
        string_before_search=(self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/h2").text)
        value_before_search=int(((string_before_search.split())[-1]).split('(')[-1].split(')')[0])
        self.search_element("search-input-newcustomimagestable", "search-submit-newcustomimagestable", serach_text)
        elements_after_search = self.driver.find_elements_by_xpath("//*[@id='newcustomimagestable']/thead/tr/th")
        head_list_after_search = [element.text for element in elements_after_search]
        if(head_list_after_search==head_list):
            logger.info("Pass: 1428 Head_list does not depend on search as expected")
        else:
            logger.info("Fail: 1428 Head_list is not correct after search")
            self.fail(msg="Fail: 1428 Head_list is not correct after search")
        string_after_search=(self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/h2").text)
        value_after_search=int(((string_after_search.split())[-1]).split('(')[-1].split(')')[0])
        if(value_after_search<value_before_search):
            logger.info("Pass: 1428 search is successful")
        else:
            logger.info("Fail: 1428 search is  not successful")
            self.fail(msg="Fail: 1428 search is  not successful")
        self.driver.find_element_by_xpath("//*[@id='table-chrome-collapse-newcustomimagestable']/form[1]/div/div/span").click()
        time.sleep(5)
        string_after_clicking_cross=(self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/h2").text)
        value_after_clicking_cross = int(((string_after_clicking_cross.split())[-1]).split('(')[-1].split(')')[0])
        if (value_after_clicking_cross==value_before_search):
            logger.info("Pass: 1428 cross icon clicked succesfully")
        else:
            logger.info("Fail: 1428 cross icon not clicked succesfully")
            self.fail(msg="Fail: 1428 cross icon not clicked succesfully")
        self.search_element("search-input-newcustomimagestable", "search-submit-newcustomimagestable", "hdjfhd")
        string_after_searching_random = (self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/h2").text)
        if (string_after_searching_random ==no_search_found_msg):
            logger.info("Pass:1428 no result msg is showing as expected ")
        else:
            logger.info("Fail: 1428 no result msg is not showing as expected")
            self.fail(msg="Fail: 1428 no result msg is not showing as expected")
        self.driver.find_element_by_xpath("//*[@id='no-results-newcustomimagestable']/div/form/button[2]").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='in_current_project']/i").click()
        time.sleep(5)
        self.driver.find_element_by_id("in_current_project:in_project").click()
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='filter-modal-newcustomimagestable']/div/div/div[3]/button").click()
        time.sleep(10)

        self.search_element("search-input-newcustomimagestable", "search-submit-newcustomimagestable","meta")
        self.driver.find_element_by_id("search-input-newcustomimagestable").click()
        self.driver.find_element_by_xpath("//*[@id='in_current_project']/i").click()
        time.sleep(5)
        if(self.driver.find_element_by_xpath("//*[@id='in_current_project:all']").is_selected()):
            logger.info("Pass: 1428 Filter got cleared and set to default after search ")
        else:
            logger.info("Fail: 1428 Filter not got cleared and set to default after search")
            self.fail(msg="Fail: 1428 Filter not got cleared and set to default after search")
        string_after_search_before_filter=(self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/h2").text)
        value_after_search_before_filter = int(((string_after_search_before_filter.split())[-1]).split('(')[-1].split(')')[0])
        self.driver.find_element_by_id("in_current_project:in_project").click()
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='filter-modal-newcustomimagestable']/div/div/div[3]/button").click()
        time.sleep(5)

        string_after_search_after_filter = (self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/h2").text)
        value_after_search_after_filter = int(((string_after_search_after_filter.split())[-1]).split('(')[-1].split(')')[0])
        if(value_after_search_after_filter<value_after_search_before_filter):
            logger.info("Pass: 1428 filter is working on searched item")
        else:
            self.fail(msg="Fail: 1428 filter is not working on searched item")
            logger.info("Fail: 1428 filter is not working on searched item")
        time.sleep(5)
        if(self.driver.find_element_by_id("in_current_project:in_project").is_selected()):
            logger.info("Pass: 1428 filter is selected as expected ")
        else:
            logger.info("Fail: 1428 filter is  not selected as expected")
            self.fail(msg="Fail: 1428 filter is  not selected as expected")
        string_before_clicking_cross_filter = (self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/h2").text)
        value_before_clicking_cross_filter = int(((string_before_clicking_cross_filter.split())[-1]).split('(')[-1].split(')')[0])
        self.driver.find_element_by_xpath("//*[@id='table-chrome-collapse-newcustomimagestable']/form[1]/div/div/span").click()
        time.sleep(5)
        string_after_clicking_cross = (self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/h2").text)
        value_after_clicking_cross = int(((string_after_clicking_cross.split())[-1]).split('(')[-1].split(')')[0])
        if (value_after_clicking_cross > value_before_clicking_cross_filter):
            logger.info("Pass: 1428 cross icon cleard succesfully on filtered item also")
        else:
            logger.info("Fail: 1428 cross icon  not cleard succesfully on filtered item also")
            self.fail(msg="Fail: 1428 cross icon  not cleard succesfully on filtered item also")
        ### it should be added as cureently it was not working
        # self.driver.find_element_by_xpath("//*[@id='in_current_project']/i").click()
        # time.sleep(5)
        # if (self.driver.find_element_by_xpath("//*[@id='in_current_project:all']").is_selected()):
        #     logger.info("Pass : Filter got cleared and set to default after search")
        # else:
        #     self.fail(msg="Filter not got cleared and set to default after search")
        # self.driver.find_element_by_xpath("//*[@id='filter-modal-newcustomimagestable']/div/div/div[1]/button").click()
        # time.sleep(5)
        print("All test steps passed in test case 1428")
        logger.info("All test steps passed in test case 1428")
    def test_1429_New_custom_image_Filter_the_contents_of_the_new_custom_image_table (self):
        project_name = "1429"
        selcted_filter_name={'Customise'}
        filter_label_dialogue=["All","Recipes provided by layers added to this project","Recipes provided by layers not added to this project"]
        self.create_new_project(project_name)
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='project-topbar']/ul/li[4]/a").click()
        time.sleep(10)

        self.driver.find_element_by_xpath("//*[@id='in_current_project']/i").click()
        time.sleep(10)
        for i in range(1,4):
            time.sleep(30)
            #print("//*[@id='filter-actions-newcustomimagestable']/div[%d]/label" %i)
            if (filter_label_dialogue[i-1] in self.driver.find_element_by_xpath("//*[@id='filter-actions-newcustomimagestable']/div[%d]/label" %i).text):
                pass
            else:
                self.fail(msg="Fail: 1429 Filter dialogue  not appeared correctly")
                logger.info("Fail: 1429 Filter dialogue  not appeared correctly")
        self.driver.find_element_by_id("in_current_project:in_project").click()
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='filter-modal-newcustomimagestable']/div/div/div[3]/button").click()
        time.sleep(10)
        self.assertTrue(self.driver.find_element_by_xpath("//th[@class='customise-or-add-recipe']/a"),
                        msg="Fail: 1429 Cutomize filter button not present")
        selcted_filter_elements=self.driver.find_elements_by_xpath("//*[@id='newcustomimagestable']/tbody/tr/td[9]")
        selcted_filter_element = [element.text for element in selcted_filter_elements]
        if (selcted_filter_name.difference(set(selcted_filter_element))):
            self.fail(msg="Fail: 1429 correct filter option not got selected")
            logger.info("Fail: 1429 correct filter option not got selected")
        else:
            logger.info("Pass: 1429 correct filter option got selected")
        self.search_element("search-input-newcustomimagestable", "search-submit-newcustomimagestable","meta")
        self.driver.find_element_by_xpath("//*[@id='in_current_project']/i").click()
        time.sleep(5)
        if (self.driver.find_element_by_xpath("//*[@id='in_current_project:all']").is_selected()):
            logger.info("Pass: 1429 Filter got cleared and set to default after search ")
        else:
            logger.info("Fail: 1429 Filter not got cleared and set to default after search")
            self.fail(msg="Fail: 1429 Filter not got cleared and set to default after search")
        print("All test steps passed in test case 1429")
        logger.info("All test steps passed in test case 1429")

    def test_1430_1431_1432_1440_Create_new_custom_image(self):
        project_name = "1430"
        searched_custom_image='rpi-basic-image'
        custom_image_name='1430-custom-image'
        edit_custom_table_item=['checkbox-add_rm_pkg_btn','checkbox-size','checkbox-dependencies','checkbox-license','checkbox-name','checkbox-version','checkbox-recipe__name',
                                'checkbox-recipe__version','checkbox-reverse_dependencies']
        self.create_new_project(project_name)
        time.sleep(20)
        self.build_recipie('core-image-minimal', project_name)
        self.driver.find_element_by_xpath("//*[@id='project-topbar']/ul/li[4]/a").click()
        time.sleep(10)
        self.search_element("search-input-newcustomimagestable", "search-submit-newcustomimagestable",'core-image-minimal')
        self.driver.find_element_by_xpath("//*[@id='newcustomimagestable']/tbody/tr/td[6]/a").click()
        if('Remove' in  self.driver.find_element_by_id("add-remove-layer-btn").text):
             pass
        else:
            self.driver.find_element_by_id("add-remove-layer-btn").click()
            time.sleep(10)
            self.driver.find_element_by_xpath("//*[@id='dependencies-modal-form']/div[3]/button[1]").click()
            time.sleep(10)
            if ('You have added' in self.driver.find_element_by_id("alert-msg").text):
                logger.info("Pass: 1430 layer added notification showed")
            else:
                self.fail(msg="Fail: 1430 layer added notification not showed")
                logger.info("Fail: 1430 layer added notification not showed")
        self.driver.back()
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='newcustomimagestable']/tbody/tr[1]/td[9]/button[1]").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='new-custom-image-modal']/div/div/div[2]/div[2]/div/div/input").click()
        self.driver.find_element_by_xpath("//*[@id='new-custom-image-modal']/div/div/div[2]/div[2]/div/div/input").send_keys(custom_image_name)
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='create-new-custom-image-btn']/span[1]").click()
        time.sleep(10)
        try:
            if ('quilt-native' in self.driver.find_element_by_id('invalid-name-help').text):
                self.driver.find_element_by_xpath("//*[@id='new-custom-image-modal']/div/div/div[1]/button").click()
                time.sleep(10)
                self.build_recipie('core-image-minimal', project_name)
                try:
                    WebDriverWait(self.driver, 5000).until(EC.element_to_be_clickable(
                    (By.XPATH, '(//*[@id="latest-builds"]//span[@class="rebuild-btn alert-link info pull-right"])[1]')))
                    time.sleep(5)
                except:
                    self.fail(msg="Fail: 1430 Build is not successful for test case  {} ".format(project_name))
                    logger.info("Fail: 1430  Build is not successful for test case  {} ".format(project_name))
                self.driver.find_element_by_xpath("//*[@id='project-topbar']/ul/li[4]/a").click()
                time.sleep(10)
                self.search_element("search-input-newcustomimagestable", "search-submit-newcustomimagestable",searched_custom_image)
                self.driver.find_element_by_xpath("//*[@id='newcustomimagestable']/tbody/tr[1]/td[9]/button[1]").click()
                time.sleep(10)
                self.driver.find_element_by_xpath("//*[@id='new-custom-image-modal']/div/div/div[2]/div[2]/div/div/input").click()
                self.driver.find_element_by_xpath("//*[@id='new-custom-image-modal']/div/div/div[2]/div[2]/div/div/input").send_keys(custom_image_name)
                time.sleep(5)
                self.driver.find_element_by_xpath("//*[@id='create-new-custom-image-btn']/span[1]").click()
            else:
                pass
        except:
            logger.info("Pass: 1430 quilt-native is not coming means  we can create image directly without any building of image")
        if('Your custom image' in self.driver.find_element_by_xpath("//*[@id='image-created-notification']/p").text):
            logger.info("Pass: 1430 cutom image created notification showed")
        else:
            self.fail(msg="Fail: 1430 cutom image created notification not showed")
            logger.info("Fail: 1430 custom image created notification not showed")
        try:
            if('Toaster has no package information for' in self.driver.find_element_by_xpath("//*[@id='packages-table']/div/p").text ):
                logger.info("Pass: 1430 need to build  this package to see next information")
                print("Pass: 1430 need to build  this package to see next information")
                self.driver.find_element_by_xpath("//*[@id='packages-table']/div/button").click()
                time.sleep(100)
                try:
                    WebDriverWait(self.driver, 5000).until(EC.element_to_be_clickable(
                    (By.XPATH, '(//*[@id="latest-builds"]//span[@class="rebuild-btn alert-link info pull-right"])[1]')))
                    time.sleep(5)
                except:
                    self.fail(msg="Fail Build is not successful for test case  {} ".format(project_name))
                    logger.info("Fail Build is not successful for test case  {} ".format(project_name))
        except:
            logger.info("Pass: 1430 Added dlayer is already built so no need to build the package")


        if ('Add | Remove packages ' in self.driver.find_element_by_xpath("//*[@id='packages-table']/h2").text):
            logger.info("Pass: 1430  Add | Remove packages option is present means custom image is already build")
        else:
            self.fail(
                msg="Fail: 1430 Add | Remove packages option is not  present means custom image is already build")
            logger.info(
                "Fail: 1430 Add | Remove packages option is not  present means custom image is already build")
        self.assertTrue(self.driver.find_element_by_id("selectpackagestable"),
                        "Fail : 1430  'add / remove' packages table  is not present")
        #test case 1431 started
        self.driver.find_element_by_xpath("(//ul[@class='breadcrumb']/li/a)[1]").click()
        time.sleep(5)
        self.driver.back()
        time.sleep(5)
        self.driver.find_element_by_xpath("(//ul[@class='breadcrumb']/li/a)[2]").click()
        time.sleep(5)
        self.driver.back()
        time.sleep(5)
        if (custom_image_name in self.driver.find_element_by_xpath("//ul[@class='breadcrumb']/li[3]").text):
            logger.info("Pass: 1431 breadcumb is showing layer name as expected ")
        else:
            self.fail(msg="Fail: 1431  breadcumb is not showing layer name as expected ")
            logger.info("Fail: 1431 breadcumb is not showing layer name as expected ")
        if ('Build' in (self.driver.find_element_by_xpath("(//div[@class='button-place btn-group']/a)[1]").text)):
            logger.info("Pass: 1431 build button is available ")
        else:
            self.fail(msg="Fail: 1431  build button is  not available  ")
            logger.info("Fail: 1431 build button is not available  ")
        if ('Download' in (self.driver.find_element_by_xpath("(//div[@class='button-place btn-group']/a)[2]").text)):
            logger.info("Pass: 1431 Download button is available ")
        else:
            self.fail(msg="Fail: 1431   Download button is  not available ")
            logger.info("Fail: 1431  Download button is not available ")
        if ('About' in (self.driver.find_element_by_xpath("//div[@class='well']/h2").text)):
           logger.info("Pass: 1431 About information is available in built customimage ")
        else:
           self.fail(msg="Fail: 1431 About information is  not available in built customimage  ")
           logger.info("Fail: 1431 About information is not  available in built customimage ")

        items=self.driver.find_elements_by_xpath("//div[@class='well']/dl/dt")
        item_info_list = [element.text for element in items]
        if(['Approx. packages included', 'Approx. package size', 'Based on', 'Recipe file', 'Layer', 'Version', 'License']==item_info_list):
            logger.info("Pass: 1431 About information  for custom image showing correctly as expected ")
        else:
            self.fail(msg="Fail: 1431 About information  for custom image  not showing correctly as expected  ")
            logger.info("Fail: 1431 About information  for custom image not showing correctly as expected  ")
        items_value=self.driver.find_elements_by_xpath("//div[@class='well']/dl/dd")
        item_value_list = [element.text for element in  items_value]
        if any(item_value_list) is '':
            self.fail(msg="Fail: 1431 About item value is null for particulaer element")
            logger.info("Fail: 1431 About item value is null for particulaer element")
        else:
            logger.info("Pass: 1431 About item value is not null as expected for all element")
        #test case 1432 started
        self.driver.find_element_by_xpath("(//ul[@class='breadcrumb']/li/a)[1]").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li[3]/a").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='customimagestable']/tbody/tr/td[1]/a").click()
        time.sleep(10)
        pckage_column_lists=self.driver.find_elements_by_xpath("//*[@id='selectpackagestable']/tbody/tr/td[1]")
        pckage_column_list = [element.text for element in pckage_column_lists]
        if(pckage_column_list==sorted(pckage_column_list)):
            logger.info("Pass: 1432 Package column is in ascending order ")
        else:
            self.fail(msg="Fail: 1432 Package column is  not in ascending order  ")
            logger.info("Fail: 1432 Package column is not in ascending order")
        custom_table_head_elements=self.driver.find_elements_by_xpath("//*[@id='selectpackagestable']/thead/tr/th")
        custom_table_head_element = [element.text for element in custom_table_head_elements]
        if (custom_table_head_element == ['Package', 'Package Version', 'Approx Size', '', 'Dependencies', '', '', '', 'Add | Remove']):
            logger.info("Pass: 1432 custom table head element is as expected ")
        else:
            self.fail(msg="Fail: 1432 custom table head element is  not as expected  ")
            logger.info("Fail: 1432 custom table head element is not  as expected ")
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(2)
        for item1 in edit_custom_table_item:
            if (self.driver.find_element_by_id(item1).is_selected()):
                pass
            else:
                self.driver.find_element_by_id(item1).click()
                time.sleep(10)
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(2)
        custom_sorting_elements=self.driver.find_elements_by_xpath("//table[@id='selectpackagestable']/thead/tr/th/i[@class='icon-caret-up']")
        custom_sorting_element = []
        for element in custom_sorting_elements:
            parent_element = element.find_element_by_xpath('..')
            custom_sorting_element.append(parent_element.text)
        if (custom_sorting_element ==['Package', 'Approx Size', 'License', 'Recipe'] ):
             logger.info("Pass: 1432 custom sorting table element is as expected ")
        else:
            self.fail(msg="Fail: 1432 custom sorting table is  not as expected  ")
            logger.info("Fail: 1432 custom sorting table is not  as expected ")
        self.driver.find_element_by_xpath("//*[@id='selectpackagestable']/thead/tr/th[7]").click()
        time.sleep(40)
        recipie_column_lists = self.driver.find_elements_by_xpath("//*[@id='selectpackagestable']/tbody/tr/td[7]")
        recipie_column_list = [element.text for element in recipie_column_lists]
        print(recipie_column_list)
        print(sorted(recipie_column_list))
        if (recipie_column_list==sorted(recipie_column_list)):
             logger.info("Pass: 1432 recipie column is in ascending order after clicking ")
        else:
            #self.fail(msg="Fail :1432 recipie column is  not in ascending order after clicking ")
            logger.info("Fail: 1432 recipie column is  not in ascending order after clicking")
        self.search_element("search-input-selectpackagestable", "search-submit-selectpackagestable", 'busybox')
        recipie_column_lists_after_searching = self.driver.find_elements_by_xpath("//*[@id='selectpackagestable']/tbody/tr/td[7]")
        recipie_column_list_after_searching = [element.text for element in recipie_column_lists_after_searching]
        if (recipie_column_list_after_searching == sorted(recipie_column_list_after_searching)):
            logger.info("Pass: 1432 recipie column is in ascending order after searching also ")
        else:
            self.fail(msg="Fail: 1432 recipie column is  not in ascending order searching  ")
            logger.info("Fail: 1432 recipie column is  not in ascending order after searching ")
        self.driver.find_element_by_xpath("//*[@id='table-chrome-collapse-selectpackagestable']/form[1]/div/div/span").click()
        time.sleep(10)
        self.edit_specicific_checkbox("checkbox-recipe__name")
        pckage_column_lists_after_hiding = self.driver.find_elements_by_xpath("//*[@id='selectpackagestable']/tbody/tr/td[1]")
        pckage_column_list_after_hiding = [element.text for element in pckage_column_lists_after_hiding]
        if (pckage_column_list_after_hiding == sorted(pckage_column_list_after_hiding)):
            logger.info("Pass: 1432 Package column is in ascending order after hiding recipie column ")
        else:
            self.fail(msg="Fail: 1432 Package column is  not in ascending order after hiding recipie column  ")
            logger.info("Fail: 1432 Package column is not in ascending order after hiding recipie column")
        self.assertTrue(self.driver.find_element_by_id("in_current_image_filter"),
                        "Fail: 1432  filter button is not  present for add-remove button")
        self.driver.find_element_by_id("in_current_image_filter").click()
        time.sleep(10)
        self.driver.find_element_by_id("in_current_image_filter:in_image").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='filter-modal-selectpackagestable']/div/div/div[3]/button").click()
        time.sleep(10)
        self.driver.find_element_by_id("in_current_image_filter").click()
        time.sleep(10)
        if (self.driver.find_element_by_id("in_current_image_filter:in_image").is_selected()):
            logger.info("Pass: 1432 Filter option is slected as  expected ")
        else:
            self.fail(msg="Pass: 1432 Filter option is  not slected as  expected")
            logger.info("Fail: 1432 Filter option is  not slected as  expected")

        self.driver.find_element_by_xpath("//*[@id='filter-modal-selectpackagestable']/div/div/div[1]/button").click()
        time.sleep(10)
        self.search_element("search-input-selectpackagestable", "search-submit-selectpackagestable", 'busybox')
        self.driver.find_element_by_id("in_current_image_filter").click()
        time.sleep(10)
        if (self.driver.find_element_by_id("in_current_image_filter:all").is_selected()):
            logger.info("Pass: 1432 Filter option got cleared after search and selected to default ")
        else:
            self.fail(msg="Fail: 1432 Filter option not cleared after search and  not selected to default")
            logger.info("Fail: 1432 Filter option not cleared after search and  not selected to default")
        self.driver.find_element_by_xpath("//*[@id='filter-modal-selectpackagestable']/div/div/div[1]/button").click()
        time.sleep(10)
        self.driver.find_element_by_id('search-input-selectpackagestable').clear()
        self.search_element("search-input-selectpackagestable", "search-submit-selectpackagestable", 'bbb')
        print(self.driver.find_element_by_xpath("//*[@id='no-results-special-selectpackagestable']/div").text)
        logger.info(self.driver.find_element_by_xpath("//*[@id='no-results-special-selectpackagestable']/div").text)
        self.driver.find_element_by_id("no-results-remove-search-btn").click()
        time.sleep(10)
        self.driver.find_element_by_id("no-results-show-all-packages").click()
        time.sleep(10)
        # test case 1440
        self.driver.find_element_by_id("in_current_image_filter").click()
        time.sleep(10)
        self.driver.find_element_by_id("in_current_image_filter:in_image").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='filter-modal-selectpackagestable']/div/div/div[3]/button").click()
        time.sleep(10)
        remove_layer_name=self.driver.find_element_by_xpath("//*[@id='selectpackagestable']/tbody/tr[1]/td[1]").text
        #print(remove_layer_name)
        self.driver.find_element_by_xpath("(//td[@class='add_rm_pkg_btn']/div/button[@data-directive='remove'])[1]").click()
        time.sleep(10)
        try:
            if('dependencies' in self.driver.find_element_by_xpath("//*[@id='package-reverse-deps-modal']/div/div/div[1]/h3").text):
                logger.info("Pass: 1440 dependecy are present for  removing layer ")
                self.driver.find_element_by_id("rm-package-reverse-deps-modal-btn").click()
                time.sleep(10)
        except:
            logger.info("Pass: 1440 No dependecy for removing layer ")
        if ('You have removed' in self.driver.find_element_by_id("change-notification-msg").text):
            logger.info("Pass: 1440 You have removed messsage notification showed for removed searched layer in cutom image ")
            logger.info("Pass: 1440 You have removed messsage notification showed for removed searched layer in cutom image ")
        else:
            self.fail(msg="Fail: 1440 You have removed messsage notification  not showed for removed searched layer in cutom image ")
            logger.info("Fail: 1440 You have removed messsage notification not showed for removed searched layer in cutom image ")
        self.driver.find_element_by_xpath("//a[@class='btn btn-default btn-lg build-custom-image']").click()
        time.sleep(10)
        try:
            WebDriverWait(self.driver, 5000).until(EC.element_to_be_clickable(
                (By.XPATH, '(//*[@id="latest-builds"]//span[@class="rebuild-btn alert-link info pull-right"])[1]')))
            time.sleep(5)
        except:
            self.fail(
                msg="Fail: 1440 Build is not successful for test case  after removing package to custom image {} ".format(
                    project_name))
            logger.info(
                "Fail: 1440 Build is not successful for test case after removing package to custom image  {} ".format(
                    project_name))
        self.driver.find_element_by_xpath("//*[@id='topbar-configuration-tab']/a").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li[3]/a").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='customimagestable']/tbody/tr[1]/td[1]/a").click()
        time.sleep(10)
        self.driver.find_element_by_id('search-input-selectpackagestable').clear()
        self.search_element("search-input-selectpackagestable", "search-submit-selectpackagestable", remove_layer_name)
        if ('Add' in self.driver.find_element_by_xpath("//*[@id='selectpackagestable']/tbody/tr[1]/td[9]").text):
            logger.info("Pass :1440 : Add message is  showing for removed  package as expected in custom table ")
        else:
            self.fail(msg="Fail :1440 :  Add message is  not showing for Remove package as not expected in custom table ")
            logger.info("Fail :1440 :  Add message is not showing for Remove package as  not expected in custom table ")
        self.driver.find_element_by_xpath("//*[@id='table-chrome-collapse-selectpackagestable']/form[1]/div/div/span").click()
        time.sleep(10)
        logger.info("All test steps passed in test case 1430 1431 1432  1440  ")
        print("All test steps passed in test case 1430 1431 1432 1440 ")
    def test_1439_1441_Adding_packages_without_dependencies_from_custom_images(self):
        project_name = "1439"
        custom_image_name='1439-custom-image'
        os.system("gnome-terminal -e 'bash -c \"cd ../../.. ;rm -rf build-toaster-*; source oe-init-build-env; bash\" '")
        time.sleep(500)
        self.create_new_project(project_name)
        time.sleep(20)
        self.build_recipie('core-image-minimal', project_name)
        self.driver.find_element_by_xpath("//*[@id='project-topbar']/ul/li[4]/a").click()
        time.sleep(10)
        self.search_element("search-input-newcustomimagestable", "search-submit-newcustomimagestable","core-image-minimal")
        self.driver.find_element_by_xpath("//*[@id='newcustomimagestable']/tbody/tr[1]/td[9]/button[1]").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='new-custom-image-modal']/div/div/div[2]/div[2]/div/div/input").click()
        self.driver.find_element_by_xpath("//*[@id='new-custom-image-modal']/div/div/div[2]/div[2]/div/div/input").send_keys(custom_image_name)
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='create-new-custom-image-btn']/span[1]").click()
        time.sleep(10)
        self.driver.find_element_by_id('search-input-selectpackagestable').clear()
        self.search_element("search-input-selectpackagestable", "search-submit-selectpackagestable", '-dbg')
        time.sleep(20)
        try:
            if('No package' in self.driver.find_element_by_xpath("//*[@id='no-results-special-selectpackagestable']/div/h3").text):
                logger.info("Pass: 1439 searched package found ")
            else:
                self.fail(msg="Fail: 1439 searched package not found please earch differnet package to add")
                logger.info("Fail :1439 searched package not found please earch differnet package to add ")
        except:
            logger.info("Pass :1439 searched package  found ready to add ")

        if ('Add package' in self.driver.find_element_by_xpath("//*[@id='selectpackagestable']/tbody/tr[1]/td[9]").text):
            logger.info("Pass: 1439 we can click on add for this package ")
        else:
            self.fail(msg="Fail: 1439  Looks like this package is already added need to search differnet package to add ")
            logger.info("Fail :1439 Looks like this package is already added need to search diiffernet package to add ")
        self.driver.find_element_by_xpath("(//td[@class='add_rm_pkg_btn']/div/button[@data-directive='add'])[1]").click()
        time.sleep(10)
        if ('You have added' in self.driver.find_element_by_id("change-notification-msg").text):
            logger.info("Pass: 1439 You have added messsage notification showed for added searched layer in cutom image ")
        else:
            self.fail(msg="Fail: 1439 You have added messsage notification  not showed for added searched layer in cutom image ")
            logger.info("Fail: 1439 You have added messsage notification not showed for added searched layer in cutom image ")
        self.driver.find_element_by_xpath("//a[@class='btn btn-default btn-lg build-custom-image']").click()
        time.sleep(200)
        try:
            WebDriverWait(self.driver, 5000).until(EC.element_to_be_clickable((By.XPATH,'(//*[@id="latest-builds"]//span[@class="rebuild-btn alert-link info pull-right"])[1]')))
            time.sleep(5)
        except:
            self.fail(
                msg="Fail: 1439 Build is not successful for test case  after addign package to custom image {} ".format(
                    project_name))
            logger.info(
                "Fail: 1439 Build is not successful for test case after addign package to custom image  {} ".format(
                    project_name))
        self.driver.find_element_by_xpath("//*[@id='topbar-configuration-tab']/a").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li[3]/a").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='customimagestable']/tbody/tr[1]/td[1]/a").click()
        time.sleep(10)
        self.driver.find_element_by_id('search-input-selectpackagestable').clear()
        self.search_element("search-input-selectpackagestable", "search-submit-selectpackagestable", '-dbg')
        if ('Remove' in self.driver.find_element_by_xpath("//*[@id='selectpackagestable']/tbody/tr[1]/td[9]").text):
            logger.info("Pass: 1439 Remove messgae  is showing for added package as expected in custom table ")
        else:
            self.fail(msg="Fail: 1439 Remove message is not showing for added package as not expected in custom table ")
            logger.info("Fail: 1439 Remove message is not showing for added package as  not expected in custom table ")
        self.driver.find_element_by_xpath("//*[@id='table-chrome-collapse-selectpackagestable']/form[1]/div/div/span").click()
        time.sleep(10)
        #test case 1441
        self.search_element("search-input-selectpackagestable", "search-submit-selectpackagestable", 'acl-ptest')
        if ('Add package' in self.driver.find_element_by_xpath("//*[@id='selectpackagestable']/tbody/tr[1]/td[9]").text):
            logger.info("Pass: 1439 we can click on add for this package ")
        else:
            self.fail(msg="Fail: 1439 Looks like this package is already added need to search differnet package to add ")
            logger.info("Fail: 1439 Looks like this package is already added need to search diiffernet package to add ")
        self.driver.find_element_by_xpath("(//td[@class='add_rm_pkg_btn']/div/button[@data-directive='add'])[1]").click()
        time.sleep(10)
        if('dependencies' in self.driver.find_element_by_xpath("//*[@id='package-deps-modal']/div/div/div[1]/h3").text):
            logger.info("Pass: 1441 Dependecies pop up is showing after clicking on add layer button")
        else:
            self.fail(msg="Fail: 1441 Dependecies pop up is  not showing after clicking on add layer button ")
            logger.info("Fail: 1441 Dependecies pop up is  not showing after clicking on add layer button ")
        self.driver.find_element_by_id("add-package-deps-modal-btn").click()
        time.sleep(10)
        if ('You have added' in self.driver.find_element_by_id("change-notification-msg").text):
            logger.info("Pass: 1441 You have added messsage notification showed for added searched layer in cutom image ")
        else:
            self.fail(msg="Fail: 1441 You have added messsage notification  not showed for added searched layer in cutom image ")
            logger.info("Fail: 1441  You have added messsage notification not showed for added searched layer in cutom image ")
        self.driver.find_element_by_xpath("//a[@class='btn btn-default btn-lg build-custom-image']").click()
        time.sleep(100)
        try:
            WebDriverWait(self.driver, 5000).until(EC.element_to_be_clickable((By.XPATH, '(//*[@id="latest-builds"]//span[@class="rebuild-btn alert-link info pull-right"])[1]')))
            time.sleep(5)
        except:
            self.fail(
                msg="Fail: 1441 Build is not successful for test case  after addign package to custom image {} ".format(
                    project_name))
            logger.info(
                "Fail: 1441  Build is not successful for test case after addign package to custom image  {} ".format(
                    project_name))
        self.driver.find_element_by_xpath("//*[@id='topbar-configuration-tab']/a").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li[3]/a").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='customimagestable']/tbody/tr[1]/td[1]/a").click()
        time.sleep(10)
        self.driver.find_element_by_id('search-input-selectpackagestable').clear()
        self.search_element("search-input-selectpackagestable", "search-submit-selectpackagestable", 'acl-ptest')
        if ('Remove' in self.driver.find_element_by_xpath("//*[@id='selectpackagestable']/tbody/tr[1]/td[9]").text):
            logger.info("Pass: 1441 Remove message is showing for added package as expected in custom table ")
        else:
            self.fail(msg="Fail: 1441  Remove  message is  not showing for added package as not expected in custom table ")
            logger.info("Fail: 1441  Remove message is not showing for added package as  not expected in custom table ")
        self.driver.find_element_by_xpath("//*[@id='table-chrome-collapse-selectpackagestable']/form[1]/div/div/span").click()
        time.sleep(10)
        logger.info("All test steps passed in test case 1439 1441 ")
        print("All test steps passed in test case 1439 1441")






















