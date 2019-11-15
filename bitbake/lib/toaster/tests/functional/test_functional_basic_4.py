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
logging.basicConfig(filename="Toasteruitestsuit2_part4.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.INFO)
class FuntionalTestBasic(SeleniumFunctionalTestCase):

    def test_1110_Layer_details_page_Default_view(self):
        project_name = "1110"
        self.create_new_project(project_name)
        time.sleep(50)
        self.driver.find_element_by_id("view-compatible-layers").click()
        time.sleep(20)
        self.search_element("search-input-layerstable", "search-submit-layerstable", "meta-aarch64")
        if (self.driver.find_element_by_xpath("//div[@class='col-md-10']/h2").text == "Compatible layers (1)"):
            logger.info("Pass: 1110 searched layer found and showing ")
        else:
            self.fail(msg="Fail: 1110 same search not found and not showin  on page")
        self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr/td[1]/a").click()
        time.sleep(10)
        self.assertTrue(self.driver.find_elements_by_xpath("//ul[@class='nav nav-tabs']/li"),
                        "Fail: 1110  Left side tabs are not present ")
        if('About' in self.driver.find_element_by_xpath("//div[@class='well']/h2").text):
             logger.info("Pass: 1110 right one provides information about the layer ")
        else:
             logger.info("Fail: 1110 right one  does not provide information about the layer")
             self.fail(msg="Fail: 1110 right one  does not provide information about the layer")
        time.sleep(20)
        self.driver.find_element_by_xpath("(//div[@class='col-md-12']/ul[@class='breadcrumb']/li/a)[1]").click()
        time.sleep(10)
        self.driver.back()
        time.sleep(30)
        self.driver.find_element_by_xpath("(//div[@class='col-md-12']/ul[@class='breadcrumb']/li/a)[2]").click()
        time.sleep(10)
        self.driver.back()
        time.sleep(10)
        if("meta-aarch64" in self.driver.find_element_by_xpath("//ul[@class='breadcrumb']/li[3]").text ):
            logger.info("Pass: 1110 breadcumb is not showing layer name as expected ")
        else:
            self.fail(msg="Fail: 1110 breadcumb is not showing layer name as expected ")
            logger.info("Fail: 1110 breadcumb is not showing layer name as expected ")
        if("meta-aarch64", "master" in self.driver.find_element_by_xpath("//div[@class='page-header']/h1").text ):
             logger.info("Pass: 1110 page heading includes the layer branch name ")
        else:
             logger.info("Fail: 1110 : page heading  does not include the layer branch name")
             self.fail(msg="Fail: 1110 : page heading  does not include the layer branch name")
        if("Summary" in self.driver.find_element_by_xpath("(//div[@class='well']/dl/dt)[1]").text):
             logger.info("Pass: 1110 Summary is present in about information ")
        else:
             self.fail(msg="Fail: 1110 : Summary is not  present in about information")
             logger.info("Fail: 1110 : Summary is not  present in about information")
        if(self.driver.find_element_by_xpath("(//div[@class='well']/dl/dd/span[@class='current-value'])[1]").text !=' ' ):
             logger.info("Pass: 1110 Summary is present in about information and value is also showing ")
        else:
             logger.info("Fail: 1110 Value is not showing  in about summary")
             self.fail(msg="Fail: 1110 Value is not showing  in about summary")
        if("Description" in self.driver.find_element_by_xpath("(//div[@class='well']/dl/dt)[2]").text ):
            logger.info("Pass: 1110 Description  is present in about information ")
        else:
            logger.info("Fail: 1110 : Description  is not  present in about information")
            self.fail(msg="Fail: 1110 : Description  is not  present in about information")

        if(self.driver.find_element_by_xpath("(//div[@class='well']/dl/dd/span[@class='current-value'])[2]").text !=' ' ):
             logger.info("Pass :1110  Description  is present in about information and value is also showing ")
        else:
             logger.info("Fail: 1110 Value is not showing  in about description")
             self.fail(msg="Fail: 1110 Value is not showing  in about description")
        tab_elements=self.driver.find_elements_by_xpath("//ul[@class='nav nav-tabs']/li")
        tab_element = [element.text for element in tab_elements]
        if(['Layer details', 'Recipes (1)', 'Machines (0)'] ==tab_element ):
            logger.info("Pass: 1110  Tab element are showing correctly ")
        else:
            logger.info("Fail: 1110 Tab element are  not showing correctly")
            self.fail(msg="Fail: 1110 Tab element are  not showing correctly")
        self.assertTrue(self.driver.find_element_by_xpath("//*[@id='add-remove-layer-btn']"),
                        "Fail: 1110  Add or remove layer button is  not present")
        time.sleep(10)
        layer_details_page=self.driver.find_elements_by_xpath("//*[@id='git-repo-info']/dt")
        layer_detail_page_element = [element.text for element in layer_details_page]
        if(layer_detail_page_element== ['Repository URL', 'Repository subdirectory', 'Git revision']):
            logger.info("Pass: 1110 layer_detail_page_element is showing correctly")
        else:
            logger.info("Fail: 1110 layer_detail_page_element is not showing correctly")
            self.fail(msg="Fail: 1110 layer_detail_page_element is not showing correctly")
        if(self.driver.find_element_by_xpath("//*[@id='git-repo-info']/dd[1]/span").text !=' '):
            logger.info("Pass: 1110  git repositroy is not blank ")
            self.driver.find_element_by_xpath("//*[@id='git-repo-info']/dd[1]/a").click()
            time.sleep(10)
        else:
            logger.info("Fail: 1110  git repositroy is  blank")
            self.fail(msg="Fail: 1110  git repositroy is  blank")
        if(self.driver.find_element_by_xpath("//*[@id='git-repo-info']/dd[2]/span[2]").text !=' '):
            logger.info("Pass: 1110  Repository subdirectory is not blank ")
            self.driver.find_element_by_xpath("//*[@id='git-repo-info']/dd[2]/a").click()
            time.sleep(10)
        else:
            logger.info("Fail: 1110 Repository subdirectory is  blank")
            self.fail(msg="Fail: 1110 Repository subdirectory is  blank")
        self.driver.find_element_by_id("targets-tab").click()
        time.sleep(10)
        if('Recipes' in self.driver.find_element_by_id("targets-tab").text):
            logger.info("Pass: 1110 Recipie tab got clicked and showing information as expected")
        else:
            logger.info("Fail: 1110  Recipie tab not clicked and  not showing information as expected")
            self.fail(msg="Fail: 1110  Recipie tab not clicked and  not showing information as expected")
        self.assertTrue(self.driver.find_element_by_xpath("//*[@id='add-remove-layer-btn']"),
                        "Fail: 1110  Add or remove layer button is  not present")
        recipie_column_elements=self.driver.find_elements_by_xpath("//*[@id='recipestable']/thead/tr/th")
        recipie_column_element = [element.text for element in recipie_column_elements]

        if(['Recipe', 'Version', 'Description', 'Build recipe'] ==recipie_column_element):
            logger.info("Pass: 1110  Recipie column is showing as expected")
        else:
            self.fail(msg="Fail: 1110  Recipie column is  not showing as expected")
            logger.info("Fail: 1110  Recipie column is  not showing as expected")
        recipie_table_elements=self.driver.find_elements_by_xpath("//*[@id='recipestable']/tbody/tr/td[1]")
        recipie_table_element= [element.text for element in recipie_table_elements]

        if (recipie_table_element == sorted(recipie_table_element)):
            logger.info("Pass: 1110 Recipie element table column is soreted in ascending order")
        else:
            self.fail(msg="Fail: 1110 Recipie element table column is  not soreted in ascending order")
            logger.info("Fail: 1110 Recipie element table column is  not soreted in ascending order")
        if (self.driver.find_element_by_xpath(
                "//*[@id='recipestable']/tbody/tr/td[4]/a[contains(@class,'disabled')]").text == 'Build recipe'):
            logger.info("Pass: 1110 Build recipie is disabled for not added layer")
        else:
            self.fail(msg="Fail: 1110 Build recipie is not disabled for not added layer")
            logger.info("Fail: 1110 Build recipie is not disabled for not added layer")
        self.driver.find_element_by_id("machines-tab").click()
        time.sleep(20)
        if ('Machines' in self.driver.find_element_by_id("machines-tab").text):
            logger.info("Pass: 1110  Machine tab got clicked and showing information as expected")
        else:
            self.fail(msg="Fail: 1110  Machine tab not clicked and  not showing information as expected")
            logger.info("Fail: 1110  Machine tab not clicked and  not showing information as expected")
        if ("Toaster does not have machine information" in self.driver.find_element_by_xpath("//*[@id='no-machines-yet']/p[1]").text):
            logger.info("Pass: 1110 No machine information is present for this layer")
        else:
            if(self.driver.find_element_by_xpath("//*[@id='machinestable']/tbody/tr/td[3]/a[contains(@class,'disabled')]").text=="Select machine"):
                logger.info("Pass: 1110 Select machine got enabled ")
            else:
                logger.info("Fail: 1110  Select machine is not diabled before adding layer")
                self.fail(msg="Fail: 1110  Select machine is not diabled before adding layer")

            machine_column_elements = self.driver.find_elements_by_xpath("//*[@id='machinestable']/thead/tr/th")
            machine_column_element = [element.text for element in machine_column_elements]
            machine_table_elements = self.driver.find_elements_by_xpath("//*[@id='machinestable']/tbody/tr/td[1]")
            machine_table_element = [element.text for element in machine_table_elements]
            if (machine_table_element == sorted(machine_table_element)):
                logger.info("Pass: 1110 Machine element table column is soreted in ascending order")
            else:
                self.fail(msg="Fail: 1110 Machine element table column is  not soreted in ascending order")
                logger.info("Fail: 1110 Machine element table column is  not soreted in ascending order")
        self.assertTrue(self.driver.find_element_by_xpath("//*[@id='add-remove-layer-btn']"),
                        "Fail: 1110  Add or remove layer button is  not present")
        print("All test steps passed in test case 1110")
        logger.info("All test steps passed in test case 1110")

    def test_1104_Project_builds_Default_view(self):
        project_name = "1104"
        Build_Checkbox_Table=["checkbox-completed_on","checkbox-errors_no",
                        "checkbox-failed_tasks","checkbox-image_files","checkbox-machine",
                        "checkbox-outcome","checkbox-target","checkbox-started_on","checkbox-time","checkbox-warnings_no"]
        Sorting_Table_Column=['outcome','machine','started_on','completed_on','errors_no','warnings_no']
        filter_item=['outcome','started_on','completed_on','failed_tasks']
        self.create_new_project(project_name)
        time.sleep(20)
        self.driver.find_element_by_xpath("//*[@id='project-topbar']/ul/li[2]/a").click()
        time.sleep(10)
        if('This project has no builds. Choose a recipe to build' in self.driver.find_element_by_xpath("//*[@id='empty-state-projectbuildstable']/div").text):
            logger.info("Pass: 1104 no recipie build for this project")
            self.build_recipie('core-image-minimal', project_name)
        else:
            logger.info("Pass: 1104 build recipie is  already present  so no need to build the recipie for this project")
        time.sleep(10)
        if('Builds' in self.driver.find_element_by_xpath("//*[@id='project-topbar']/ul/li[2]/a").text):
             logger.info("Pass: 1104 Project heading includes all build  and number ")
        else:
             self.fail(msg="Fail: 1104 project heading does not include  total porject build")
             logger.info("Fail: 1104 project heading does not include  total porject build")
        if(int(self.driver.find_element_by_xpath("//*[@id='project-topbar']/ul/li[2]/a").text.split(' ')[1].split('(')[1].split(')')[0])==1):
            logger.info("Pass: 1104 toatl number of build project is correct ")
        else:
            logger.info("Fail: 1104 toatl number of build project is not correct")
            self.fail(msg="Fail: 1104 toatl number of build project is not correct")
        # self.build_recipie('core-image-sato-sdk', project_name)
        # time.sleep(300)
        # logger.info(int(self.driver.find_element_by_xpath("//*[@id='project-topbar']/ul/li[2]/a").text.split(' ')[1].split('(')[1].split(')')[0]))
        # if (int(self.driver.find_element_by_xpath("//*[@id='project-topbar']/ul/li[2]/a").text.split(' ')[1].split('(')[1].split(')')[0]) == 2):
        #     logger.info("Pass: 1104 toatl number of build project is correct  after building second time")
        # else:
        #     self.fail(msg="Fail: toatl number of build project is not correct after building second time")

        build_head_elements=(self.driver.find_elements_by_xpath("//*[@id='projectbuildstable']/thead/tr/th"))
        build_head_element = [element.text for element in build_head_elements]
        if(['Outcome', 'Recipe', '', '', 'Completed on', 'Failed tasks', 'Errors', 'Warnings', '', 'Image files']==build_head_element):
            logger.info("Pass: 1104 total number of column is correct as expected ")
        else:
            logger.info("Fail: 1104 total number of columns is not as expected")
            self.fail(msg="Fail: 1104 total number of columns is not as expected")
        self.assertTrue(self.driver.find_element_by_xpath("//*[@id='projectbuildstable']/thead/tr/th[5]/i[@style='display: inline;']"),
                        "Fail: 1104 caret up is not active means completed on is not in ascending order")
        completedon_table_elements = self.driver.find_elements_by_xpath("//*[@id='projectbuildstable']/tbody/tr/td[5]")
        completedon_table_element = [element.text for element in completedon_table_elements]
        if (completedon_table_element == sorted(completedon_table_element,reverse=True)):
             logger.info("Pass: 1104 Completed on table element is in descending order")
        else:
             logger.info("Fail: 1104 Completed on table element is  not in descending order")
             self.fail(msg="Fail: 1104 Completed on table element is  not in descending order")
        #test case 1105
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(2)
        for item1 in Build_Checkbox_Table:
            if (self.driver.find_element_by_id(item1).is_selected()):
                pass
            else:
                self.driver.find_element_by_id(item1).click()
                time.sleep(5)
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(2)
        for item in Sorting_Table_Column:
            self.assertTrue(self.driver.find_element_by_xpath("//a[@data-sort-field='" + item + "']"),
                                msg="Fail: 1105 Sortable table heads are not correct as expected")
            self.driver.find_element_by_xpath("//a[@data-sort-field='" + item + "']").click()
            time.sleep(20)
            column_elements_sortable_first_click=self.driver.find_elements_by_xpath("//*[@id='projectbuildstable']/tbody/tr/td[@class='" + item + "']")
            column_element_sortable_first_click = [element.text for element in column_elements_sortable_first_click]
            if ((column_element_sortable_first_click == sorted(column_element_sortable_first_click, reverse=True)) or (column_element_sortable_first_click == sorted(column_element_sortable_first_click)) ):
                logger.info("Pass: 1105 table element is in descending order or ascending order for %s" %(item))
            else:
                logger.info("Fail: 1105 table element is  not in descending order or ascending order for %s" % (item))
                self.fail(msg="Fail: 1105 table element is  not in descending order or ascending order for %s" %(item))
            self.driver.find_element_by_xpath("//a[@data-sort-field='" + item + "']").click()
            time.sleep(30)

            column_elements_sortable_after_second_click = self.driver.find_elements_by_xpath(
                "//*[@id='projectbuildstable']/tbody/tr/td[@class='" + item + "']")
            column_element_sortable_after_second_click = [element.text for element in column_elements_sortable_after_second_click]
            if ((column_element_sortable_after_second_click == sorted(column_element_sortable_after_second_click, reverse=True)) or (
                    column_element_sortable_after_second_click == sorted(column_element_sortable_after_second_click))):
                logger.info("Pass: 1105 table element is in descending or ascending  order after clicking for %s" %(item))
            else:
                logger.info("Fail: 1105 table element is  not in descending or ascending  order after clicking for %s" %(item))
                self.fail(msg="Fail: 1105 table element is  not in descending or ascending  order after clicking for %s" %(item))
        self.driver.find_element_by_xpath("//a[@data-sort-field='machine']").click()
        time.sleep(10)

        column_elements_machine = self.driver.find_elements_by_xpath("//*[@id='projectbuildstable']/tbody/tr/td[@class='machine']")
        column_element_machine = [element.text for element in column_elements_machine]
        if ((column_element_machine == sorted(column_element_machine))):
            logger.info("Pass: 1105 Machine on table element is in descending order")
        else:
            logger.info("Fail: 1105 Machine on table element is  not in descending order")
            self.fail(msg="Fail: 1105 Machine on table element is  not in descending order")
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(2)
        self.driver.find_element_by_id("checkbox-machine").click()
        time.sleep(10)
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(2)

        completedon_table_elements_hiding = self.driver.find_elements_by_xpath(
            "//*[@id='projectbuildstable']/tbody/tr/td[5]")
        completedon_table_element_hiding = [element.text for element in completedon_table_elements_hiding]
        if (completedon_table_element_hiding == sorted(completedon_table_element_hiding,reverse=True)):
            logger.info("Pass: 1105 Completed on table element is in ascending oredr after hiding element also")
        else:
            self.fail(msg="Fail: 1105 Completed on table element is  not in ascending order after hiding element")
            logger.info("Fail: 1105 Completed on table element is  not in ascending order after hiding element")
        build_head_elements_check = (self.driver.find_elements_by_xpath("//*[@id='projectbuildstable']/thead/tr/th"))
        build_head_element_check = [element.text for element in build_head_elements_check]

        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(2)
        edit_checkbox_selected_elements = self.driver.find_elements_by_xpath("//*[@id='table-chrome-collapse-projectbuildstable']/div/ul/li/div/label/input[@checked='checked']")

        edit_checkbox_selected_element=[]
        for element in edit_checkbox_selected_elements:
            parent_element=element.find_element_by_xpath('..')
            edit_checkbox_selected_element.append(parent_element.text)
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(2)
        if(all(elem in build_head_element_check for elem in edit_checkbox_selected_element) ):
            logger.info("Pass:1106 Selected element in edit column menu is correct as it is showing head elements")
        else:
            self.fail(msg="Fail: 1106 Selected element in edit column menu is  not correct as it is  not showing head elements")
            logger.info("Fail: 1106 Selected element in edit column menu is  not correct as it is  not showing head elements")
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(2)
        non_removed_checkbox_elements = self.driver.find_elements_by_xpath("//label[@class='text-muted']")
        non_removed_checkbox_element = [element.text for element in non_removed_checkbox_elements]
        if(['Completed on', 'Outcome', 'Recipe'] == non_removed_checkbox_element ):
            logger.info("Pass: 1106 correct mute column is showing")
        else:
            self.fail(msg="Fail: 1106 correct mute column is  not showing")
            logger.info("Fail: 1106 correct mute column is  not showing")
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(2)

        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(2)
        for item1 in Build_Checkbox_Table:
            if (self.driver.find_element_by_id(item1).is_selected()):
                self.driver.find_element_by_id(item1).click()
                time.sleep(5)
                build_head_elements_check_after_unselecting = (self.driver.find_elements_by_xpath("//*[@id='projectbuildstable']/thead/tr/th"))
                build_head_element_check_after_unselecting = [element.text for element in build_head_elements_check_after_unselecting]
                if(item not in build_head_element_check_after_unselecting):
                    logger.info("Pass: 1106 As expected item not in head_element after clicking on checkbox")
                else:
                    logger.info("Fail: 1106 item is present after clicking checkbox also")
                    self.fail(msg="Fail: 1106 item is present after clicking checkbox also")
                break

            else:
                pass
        #started test case 1108
        for item in filter_item:
            self.assertTrue(self.driver.find_elements_by_xpath("//th[@class='" + item + "']//i[@class='glyphicon glyphicon-filter filtered']"),
                            "Fail: 1108 filter item is not present as expected")
        self.driver.find_element_by_xpath("//*[@id='outcome_filter']/i").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='outcome_filter:successful_builds']").click()
        time.sleep(20)
        self.driver.find_element_by_xpath("//*[@id='filter-modal-projectbuildstable']/div/div/div[3]/button").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='started_on_filter']/i").click()
        time.sleep(10)
        self.driver.find_element_by_id("started_on_filter:date_range").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='filter-modal-projectbuildstable']/div/div/div[3]/button").click()
        time.sleep(10)

        self.driver.find_element_by_xpath("//*[@id='outcome_filter']/i").click()
        time.sleep(10)
        if(self.driver.find_element_by_id("outcome_filter:all").is_selected()):
            logger.info("Pass: 1108 filters are mutally exclusive")
        else:
            logger.info("Fail: 1108 filters are  not mutally exclusive")
            self.fail(msg="Fail: 1108 filters are  not mutally exclusive")
        self.driver.find_element_by_xpath("//*[@id='filter-modal-projectbuildstable']/div/div/div[1]/button").click()
        time.sleep(10)

        self.driver.find_element_by_xpath("//*[@id='started_on_filter']/i").click()
        time.sleep(10)
        self.driver.find_element_by_id("started_on_filter:date_range").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='filter-modal-projectbuildstable']/div/div/div[3]/button").click()
        time.sleep(10)
        self.search_element("search-input-projectbuildstable", "search-submit-projectbuildstable","core-image-minimal")
        self.driver.find_element_by_xpath("//*[@id='started_on_filter']/i").click()
        time.sleep(10)
        if (self.driver.find_element_by_id("started_on_filter:all").is_selected()):
            logger.info("Pass: 1108  filters are got cleared after search")
        else:
            logger.info("Fail: 1108 filters are not cleared after search")
            self.fail(msg="Fail: 1108 filters are not cleared after search")
        self.driver.find_element_by_xpath("//*[@id='filter-modal-projectbuildstable']/div/div/div[1]/button").click()
        time.sleep(10)

        self.assertTrue(self.driver.find_element_by_xpath("//*[@id='search-input-projectbuildstable'][@placeholder='Search all project builds']"),
                        msg="Fail: 1109 search placeholder string are not present")
        build_head_elements_before_search = (self.driver.find_elements_by_xpath("//*[@id='projectbuildstable']/thead/tr/th"))
        build_head_element_before_search = [element.text for element in build_head_elements_before_search]
        time.sleep(30)
        self.driver.find_element_by_id("search-input-projectbuildstable").clear()
        time.sleep(10)
        self.search_element("search-input-projectbuildstable","search-submit-projectbuildstable","core-image-minimal")
        time.sleep(20)

        self.assertTrue(self.driver.find_element_by_xpath("//span[@style='display: block;']"),msg="Fail: 1109 In search placeholder serached string are not present")
        if('project build found' in self.driver.find_element_by_xpath("//h2[@class='top-air']").text):
            logger.info("Pass: 1109 : build search is showing correclty")
            build_head_elements_after_search = (self.driver.find_elements_by_xpath("//*[@id='projectbuildstable']/thead/tr/th"))
            build_head_element_after_search = [element.text for element in build_head_elements_after_search]
            if(build_head_element_before_search==build_head_element_after_search):
                logger.info("Pass: 1109  search is not affecting on head table element same is showing")
            else:
                logger.info("Fail: 1109 search is affecting on head table element same is  not showing")
                self.fail(msg="Fail: 1109 search is affecting on head table element same is  not showing")
            time.sleep(20)
            self.driver.find_element_by_xpath("(//span[@class='remove-search-btn-projectbuildstable glyphicon glyphicon-remove-circle'])[2]").click()
            time.sleep(20)

        else:
            logger.info("Fail: 1109 build search is not showing correclty")
            self.fail(msg="Fail: 1109 build search is not showing correclty")
        self.search_element("search-input-projectbuildstable", "search-submit-projectbuildstable", "fjdjg")
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='no-results-projectbuildstable']/div/form/button[2]").click()
        time.sleep(20)
        print("All test steps passed in test case  1104,1105,1106,1108,1109")
        logger.info("All test steps passed in test case  1104,1105,1106,1108,1109")


    def test_1102_Configuration_variables_Test_UI_elements(self):
        project_name = "1102"
        # variable_validation_message="Some variables cannot be set from Toaster\
        #
        #                             Toaster cannot set any variables that impact\
        #                                1) the configuration of the build servers, \
        #                              or 2) where artifacts produced by the build are stored. Such variables include:\
        #                         BB_DISKMON_DIRS BB_NUMBER_THREADS CVS_PROXY_HOST CVS_PROXY_PORT PARALLEL_MAKE TMPDIR\
        #                              Plus the following standard shell environment variables:\
        #                                              http_proxy ftp_proxy https_proxy all_proxy"
        self.create_new_project(project_name)
        self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li[10]/a").click()
        time.sleep(10)
        self.assertTrue(self.driver.find_element_by_xpath("//*[@class='glyphicon glyphicon-edit'][@id='change-distro-icon']"),
                        msg="Fail: 1102 Editable icon is not present  for distro in bitbake variable")
        self.driver.find_element_by_id("change-distro-icon").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//input[@type='text'][@id='new-distro']").click()
        time.sleep(10)
        self.driver.find_element_by_id("new-distro").clear()
        time.sleep(20)
        self.assertTrue(self.driver.find_element_by_xpath("//button[@id='apply-change-distro']"),msg="1102 :Save button is not disabled after clearing distro")
        self.driver.find_element_by_id("new-distro").send_keys("poky tiny")
        time.sleep(20)
        if('A valid distro name cannot include spaces'==self.driver.find_element_by_id("distro-error-message").text ):
            logger.info("Pass: 1102 After giving distro name with sapce alert error message is showing")
        else:
            logger.info("Fail: 1102  After giving distro name with sapce alert error message is not showing")
            self.fail(msg="Fail: 1102  After giving distro name with sapce alert error message is not showing")
        self.driver.find_element_by_id("new-distro").clear()
        time.sleep(10)
        self.driver.find_element_by_id("new-distro").send_keys("poky")
        time.sleep(10)
        self.driver.find_element_by_id("apply-change-distro").click()
        time.sleep(10)
        self.assertTrue(self.driver.find_element_by_xpath("//*[@class='glyphicon glyphicon-edit'][@id='change-image_fstypes-icon']"),msg="1102 :Editable icon is not present  for Image_Fstype in bitbake variable")
        self.driver.find_element_by_id("change-image_fstypes-icon").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//input[@type='text'][@id='new-imagefs_types']").click()
        time.sleep(10)
        checked_element=self.driver.find_elements_by_xpath("//div[@class='checkbox']/label/input[@checked='checked']")
        Total_checked_element=len(checked_element)
        checkbox_selected_element = []
        for element in checked_element:
            parent_element = element.find_element_by_xpath('..')
            checkbox_selected_element.append(parent_element.text)
        if (checkbox_selected_element == sorted(checkbox_selected_element)):
             logger.info("Pass: 1102 Checked element for image_fstype is in ascending order")
        else:
             logger.info("Fail: 1102 Checked element for image_fstype is  not in ascending order")
             self.fail(msg="Fail: 1102 Checked element for image_fstype is  not in ascending order")

        Total_checkbox_image_fstype_element=(len(self.driver.find_elements_by_xpath("//*[@id='all-image_fstypes']/div/label/input")))
        Unchecked_element = []
        for i in range(int(Total_checked_element)+1,int(Total_checkbox_image_fstype_element)+1):
            element=self.driver.find_element_by_xpath("//*[@id='all-image_fstypes'][@class='scrolling']/div[%d]/label" %i)
            Unchecked_element.append(element.text)
        if (Unchecked_element == sorted(Unchecked_element)):
            logger.info("Pass: 1102 Unchecked element  fo image fs_types  is also in ascending order")
        else:
            logger.info("Fail: 1102 Unchecked element  fo image_fstypes  is  not in ascending order")
            self.fail(msg="Fail: 1102 Unchecked element  fo image_fstypes  is  not in ascending order")
        self.driver.find_element_by_id("filter-image_fstypes").click()
        time.sleep(10)
        self.driver.find_element_by_id("filter-image_fstypes").send_keys("fgjfk")
        time.sleep(10)
        if("No image types found" ==self.driver.find_element_by_id("no-match-fstypes").text):
            logger.info("Pass: 1102 message notify for  not matching string is showing correclty")
        else:
            self.fail(msg="Fail: 1102  message notify for not matching string is not showing correclty")
            logger.info("Fail: 1102  message notify for not matching string is not showing correclty")
        self.driver.find_element_by_id("filter-image_fstypes").clear()
        time.sleep(10)
        self.driver.find_element_by_id("cancel-change-image_fstypes").click()
        time.sleep(10)
        self.driver.find_element_by_id("change-image_fstypes-icon").click()
        time.sleep(10)
        for  i in range(1,int(Total_checked_element)+1):
            self.driver.find_element_by_xpath("//*[@id='all-image_fstypes']/div[%d]/label/input" %i).click()
            time.sleep(10)
        if("You must select at least one image type"== self.driver.find_element_by_id("fstypes-error-message").text):
            logger.info("Pass: 1102 message notify   is showing after all image_fstypes got unselected")
        else:
            logger.info("Fail: 1102 message notify is not showing after all image_fstypes got unselected")
            self.fail(msg="Fail: 1102 message notify is not showing after all image_fstypes got unselected")
        try:
            self.driver.find_element_by_id("apply-change-image_fstypes").click()
            time.sleep(10)
            logger.info("Fail: 1102  After in checking all element also it got diabled")
            self.fail(msg="Fail: 1102  After in checking all element also it got diabled")
        except:
            logger.info("Pass: 1102 correct save option should be disabled as expected after unchecking all element ")
        clicked_image_fstype=[]
        for i in range(1,4):
            self.driver.find_element_by_xpath("//*[@id='all-image_fstypes']/div[%d]/label/input" %i).click()
            time.sleep(10)
            element = self.driver.find_element_by_xpath("//*[@id='all-image_fstypes'][@class='scrolling']/div[%d]/label" % i)
            clicked_image_fstype.append(element.text)
        self.driver.find_element_by_id("apply-change-image_fstypes").click()
        time.sleep(10)
        if(' '.join(clicked_image_fstype) ==self.driver.find_element_by_id("image_fstypes").text):
             logger.info("Pass: 1102 Image_fstype is showing as expected ")
        else:
             logger.info("Fail: 1102  Image_fstype is  not showing as expected")
             self.fail(msg="Fail: 1102  Image_fstype is  not showing as expected")
        self.assertTrue(self.driver.find_element_by_xpath("//*[@class='glyphicon glyphicon-edit'][@id='change-package_classes-icon']"),msg="1102 :Editable icon is not present  for distro in bitbake variable")
        self.driver.find_element_by_id("change-package_classes-icon").click()
        time.sleep(10)
        dropdown_elements=self.driver.find_elements_by_xpath("//select[@id='package_classes-select']/option")
        dropdown_element = [element.text for element in dropdown_elements]
        if(dropdown_element==['package_deb', 'package_ipk', 'package_rpm']):
            logger.info("Pass: 1102 Dropdownlist for package calss is showing correctly")
        else:
            self.fail(msg="Fail: 1102  Dropdownlist for package calss is not  showing correctly")
            logger.info("Fail: 1102  Dropdownlist for package calss is not  showing correctly")
        self.driver.find_element_by_id("package_classes-select").click()
        time.sleep(10)
        self.driver.find_element_by_id("package_classes-select").send_keys(Keys.UP)
        time.sleep(5)
        self.driver.find_element_by_id("package_classes-select").send_keys(Keys.RETURN)
        time.sleep(5)
        if(self.driver.find_element_by_xpath("//*[@id='change-package_classes-form']/div[2]/div[1]").text=='package_deb'  and self.driver.find_element_by_xpath("//*[@id='change-package_classes-form']/div[2]/div[2]").text=='package_rpm' ):
            logger.info("pass: 1102 checkbox for  package calss is correct")
        else:
            self.fail(msg="Fail: 1102  checkbox for  package class is  not correct")
            logger.info("Fail: 1102  checkbox for  package class is  not correct")
        checked_elemenct_package_class=self.driver.find_element_by_xpath("//*[@id='change-package_classes-form']/div[2]/div[1]").text
        self.driver.find_element_by_xpath("//*[@id='package_class_1']/input[@type='checkbox']").click()
        time.sleep(10)
        self.driver.find_element_by_id("apply-change-package_classes").click()
        time.sleep(10)
        if(checked_elemenct_package_class in self.driver.find_element_by_id("package_classes").text ):
            logger.info("pass: 1102 checkbox element is showing correct after saving for package class")
        else:
            self.fail(msg="Fail: 1102  checkbox element is not showing correct after saving for package class")
            logger.info("Fail: 1102  checkbox element is not showing correct after saving for package class")
        self.driver.find_element_by_id("change-package_classes-icon").click()
        time.sleep(10)
        Unchecked_elemenct_package_class = self.driver.find_element_by_xpath("//*[@id='change-package_classes-form']/div[2]/div[1]").text
        logger.info(Unchecked_elemenct_package_class)
        self.driver.find_element_by_xpath("//*[@id='package_class_1']/input[@type='checkbox']").click()
        time.sleep(10)
        self.driver.find_element_by_id("apply-change-package_classes").click()
        time.sleep(10)
        if (Unchecked_elemenct_package_class not  in self.driver.find_element_by_id("package_classes").text):
            logger.info("pass: 1102 checkbox element is showing correct after doing uncheck for package class")
        else:
            logger.info("Fail: 1102  checkbox element is not showing correct after doing uncheck saving for package class")
            self.fail(msg="Fail: 1102  checkbox element is not showing correct after doing uncheck saving for package class")
        Add_varriable_elements=self.driver.find_elements_by_xpath("//form[@id='variable-form']//fieldset/div/div/div/input[@type='text']")
        Add_variable_element = []
        for element in Add_varriable_elements:
            parent_element=element.find_element_by_xpath("..")
            Add_variable_element.append(parent_element.text)
        if(['Variable', 'Value']==Add_variable_element):
            logger.info("pass: 1102 add variable form has 2 text fields: one for the variable name and a second one for the variable value")
        else:
            logger.info("Fail: 1102  add variable form has  not 2 text fields: one for the variable name and a second one for the variable value")
            self.fail(msg="Fail: 1102  add variable form has  not 2 text fields: one for the variable name and a second one for the variable value")
        try:
            self.driver.find_element_by_id("add-configvar-button").click()
            time.sleep(10)
            logger.info("Fail: 1102  Add  button that is  not disabled until both text fields have some input in them")
            self.fail(msg="Fail: 1102  Add  button that is  not disabled until both text fields have some input in them")
        except:
            logger.info("Pass: 1102 Add button that is disabled until both text fields have some input in them  as expected")
        if ('Some variables cannot be set from Toaster' in self.driver.find_element_by_xpath("//*[@id='variable-form']/fieldset/div/div[2]").text):
            logger.info("Pass:1102 variable validation message is showing")
        else:
            logger.info("Fail: 1102  variable validation message is not showing")
            self.fail(msg="Fail: 1102  variable validation message is not showing")
        self.driver.find_element_by_id("variable").clear()
        self.driver.find_element_by_id("variable").send_keys("poky tiny")
        if("A valid variable name can only include letters, numbers and the special characters _ - /. Variable names cannot include spaces" ==self.driver.find_element_by_id("new-variable-error-message").text):
            logger.info("pass: 1102 variable validation message is showing as expected for giving space ")
        else:
            logger.info("Fail: 1102 variable validation message is not showing as expected for giving space")
            self.fail(msg="Fail: 1102 variable validation message is not showing as expected for giving space")
        self.driver.find_element_by_id("variable").clear()
        self.driver.find_element_by_id("variable").send_keys("BB_DISKMON_DIRS")
        if ("You cannot edit this variable in Toaster because it is set by the build servers" == self.driver.find_element_by_id("new-variable-error-message").text):
            logger.info("pass: 1102 variable validation message  for using restricted variable is showing as expected")
        else:
            logger.info("Fail: 1102 variable validation message  for using restricted variable is not showing as expected")
            self.fail(msg="Fail: 1102 variable validation message  for using restricted variable is not showing as expected")
        self.driver.find_element_by_id("variable").clear()
        self.driver.find_element_by_id("variable").send_keys("test")
        self.driver.find_element_by_id("value").clear()
        self.driver.find_element_by_id("value").send_keys("test")
        self.driver.find_element_by_id("add-configvar-button").click()
        time.sleep(10)
        try:
            self.driver.find_element_by_id("add-configvar-button").click()
            time.sleep(10)
            logger.info("Fail: 1102  Add  button that is  not disabled while both text fields should be clear")
            self.fail(msg="Fail: 1102  Add  button that is  not disabled while both text fields should be clear")
        except:
            logger.info("Pass: 1102 Add button that is disabled  means both text field are  empty")
        if('test' ==self.driver.find_element_by_xpath("//*[@id='configvar-list']/dt/span[@class='js-config-var-name']").text):
            logger.info("Pass: 1102 Added variable is showing correclty")
        else:
            logger.info("Fail: 1102  Added variable is  not showing correclty")
            self.fail(msg="Fail: 1102  Added variable is  not showing correclty")
        if(self.driver.find_element_by_xpath("//*[@id='configvar-list']/dt/span[@class='js-config-var-name']").text=='test'):
            logger.info("Pass: 1102 added variable test got added and showing")
            self.assertTrue(self.driver.find_element_by_xpath("//*[@id='configvar-list']/dt/span[@class='glyphicon glyphicon-trash js-icon-trash-config_var']"),
                            msg="Fail: 1102 delete icon is present next to the variable name")
            self.assertTrue(self.driver.find_element_by_xpath("//*[@id='configvar-list']/dd/span[2]"),
                            msg="Fail: 1102 added variable has a change icon present next to the variable value")
            self.driver.find_element_by_xpath("//*[@id='configvar-list']/dd/span[2]").click()
            self.driver.find_element_by_xpath("//dd[@class='variable-list']//form/div/input[@class='form-control js-new-config_var']").clear()
            time.sleep(10)
            self.driver.find_element_by_xpath("//dd[@class='variable-list']//form/button[@class='btn btn-link js-cancel-change-config_var']").click()
            time.sleep(10)
            try:
                self.driver.find_element_by_xpath("//dd[@class='variable-list']//form/button[@class='btn btn-default js-apply-change-config_var']").click()
                time.sleep(10)
                logger.info("Fail: 1102  Save value is  not disabled  since add variable is empty")
                self.fail(msg="Fail: 1102  Save value is  not disabled  since add variable is empty")
            except:
                logger.info("Pass: 1102 Save value is  disabled as  expected since add variable is empty")
            time.sleep(10)
            self.driver.find_element_by_xpath("//*[@id='configvar-list']/dt/span[@class='glyphicon glyphicon-trash js-icon-trash-config_var']").click()
            time.sleep(10)

            try:
                self.driver.find_element_by_xpath("//*[@id='configvar-list']/dt/span[@class='js-config-var-name']")
                time.sleep(10)
                logger.info("Fail: 1102  add variable is still present after deleting the variable")
                self.fail(msg="Fail: 1102  add variable is still present after deleting the variable")
            except:
                logger.info("Pass:1102 add variable is not present after deleting the variable as expected")
        else:
            self.fail(
                msg="Fail: 1102 added variable test  not got added and not  showing")
            logger.info(
                "Fail: 1102 added variable test  not got added and not  showing")
        print("All test steps passed in test case  1102")
        logger.info("All test steps passed in test case  1102")
    def test_1100_Configuration_variables_default_view(self):
        project_name = "1100"
        self.create_new_project(project_name)
        self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li[10]/a").click()
        time.sleep(10)
        if('poky'==self.driver.find_element_by_id("distro").text):
            logger.info("Pass: 1100 DISTRO default value poky is present")
        else:
            logger.info("Fail: 1100 DISTRO default value poky is not  present")
            self.fail(msg="Fail: 1100 DISTRO default value poky is not  present")
        if('ext3 jffs2 tar.bz2'==self.driver.find_element_by_id("image_fstypes").text):
            logger.info("Pass: 1100 IMAGE_FSTYPES  default value is ext3 jffs2 tar.bz2")
        else:
            logger.info("Fail: 1100 IMAGE_FSTYPES  default value is  not ext3 jffs2 tar.bz2")
            self.fail(msg="Fail: 1100 IMAGE_FSTYPES  default value is  not ext3 jffs2 tar.bz2")
        if('Not set'==self.driver.find_element_by_id("image_install").text):
            logger.info("Pass :1100 IMAGE_INSTALL_append is Not set")
        else:
            logger.info("Fail: 1100 IMAGE_INSTALL_append is not Not set")
            self.fail(msg="Fail: 1100 IMAGE_INSTALL_append is not Not set")
        if('package_rpm'==self.driver.find_element_by_id("package_classes").text):
            logger.info("Pass: 1100 PACKAGE_CLASES is package_rpm")
        else:
            logger.info("Fail: 1100 PACKAGE_CLASES is not package_rpm")
            self.fail(msg="Fail: 1100 PACKAGE_CLASES is not package_rpm")
        if('/poky/sstate-cache'in self.driver.find_element_by_id("sstate_dir").text):
            logger.info("Pass: 1100 SSTATE_DIR is /homeDirectory/poky/sstate-cache")
        else:
            self.fail(msg="Fail: 1100 SSTATE_DIR is not /homeDirectory/poky/sstate-cache")
            logger.info("Fail: 1100 SSTATE_DIR is not /homeDirectory/poky/sstate-cache")
        self.assertTrue( self.driver.find_element_by_xpath("//div[@id='add-configvar-name-div']//input[@placeholder='Type the variable name']"),
                       msg="Fail: 1100 Variable field has the default text Type variable name  not present")
        self.assertTrue(self.driver.find_element_by_xpath(
            "//div[@class='form-group']/input[@placeholder='Type the variable value']"),
                        msg="Fail: 1100 the Value field has the default text Type variable value not  present")
        try:
            self.driver.find_element_by_id("add-configvar-button").click()
            time.sleep(100)
            logger.info("Fail: 1100  Add  button that is  not disabled while both text fields of variable is empty")
            self.fail(msg="Fail: 1100  Add  button that is  not disabled while both text fields of variable is empty")
        except:
            logger.info("Pass:1102 Add  button that is   disabled while both text fields of variable is empty as expected")
        if ('Some variables cannot be set from Toaster' in self.driver.find_element_by_xpath("//*[@id='variable-form']/fieldset/div/div[2]").text):
            logger.info("Pass: 1100  under the Add variable section, there is text present that describes the variables that Toaster cannot modify.")
        else:
            self.fail(msg="Fail: 110 under the Add variable section, there is not text present that describes the variables that Toaster cannot modify.")
            logger.info(
                "Fail: 110 under the Add variable section, there is not text present that describes the variables that Toaster cannot modify.")
        logger.info("All test steps passed in test case 1100")
        print("All test steps passed in test case 1100")

    def test_1079_All_targets_Default_view(self):
        project_name = "1079"
        self.create_new_project(project_name)
        time.sleep(10)
        self.build_recipie('core-image-minimal', project_name)
        self.driver.find_element_by_xpath("//*[@id='topbar-configuration-tab']/a").click()
        time.sleep(20)
        self.driver.find_element_by_xpath("//*[@id='config-nav']/ul/li[4]/a").click()
        time.sleep(10)
        if('Compatible image recipes' in self.driver.find_element_by_xpath("//div[@class='col-md-10']/h2").text ):
            logger.info("Pass: 1079  image recipies got clicked and showing in heading.")
        else:
            logger.info("Fail: 1079  image recipies got  not clicked and  not showing in heading..")
            self.fail(msg="Fail: 1079  image recipies got  not clicked and  not showing in heading..")
        self.assertTrue(self.driver.find_element_by_id("imagerecipestable"),
                        msg="Fail: 1079 : Image recipie table is not showing")
        self.driver.find_element_by_id("imagerecipestable")
        image_recipie_head_elements=self.driver.find_elements_by_xpath("//*[@id='imagerecipestable']/thead/tr/th")
        image_recipie_head_element = [element.text for element in image_recipie_head_elements]
        if(['Image recipe', 'Version', 'Description', '', '', 'Layer', '', '', 'Build']==image_recipie_head_element):
             logger.info("Pass: 1069  image recipies column_heading is as expected.")
        else:
             logger.info("Fail: 1079  image recipies column_heading is  not as expected.")
             self.fail(msg="Fail: 1079  image recipies column_heading is  not as expected.")
        print("All test steps passed in test case 1079")
        logger.info("All test steps passed in test case 1079")

    def test_1078_All_layers_Add_delete_layers(self):
        project_name = "1078"
        self.create_new_project(project_name)
        time.sleep(10)
        self.driver.find_element_by_id("view-compatible-layers").click()
        time.sleep(10)
        if('Add | Remove' in self.driver.find_element_by_xpath("//*[@id='layerstable']/thead/tr/th[7]/span[@class='text-muted']").text):
            logger.info("Pass: 1078 Add/delete column is enabled as expected.")
        else:
            self.fail(msg="Fail: 1078 Add/delete column is  not enabled as expected.")
            logger.info("Fail: 1078 Add/delete column is  not enabled as expected.")
        self.driver.find_element_by_xpath("//*[@id='in_current_project']/i").click()
        time.sleep(10)
        self.driver.find_element_by_id("in_current_project:not_in_project").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='filter-modal-layerstable']/div/div/div[3]/button").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr[1]/td[7]/a[2]").click()
        time.sleep(10)
        try:
            if('dependencies' in self.driver.find_element_by_xpath("//*[@id='dependencies-modal-form']/div[1]/h3").text ):
                logger.info("Pass:1078 a dialog  appears listing the dependencies")
                dependency_list_items=self.driver.find_elements_by_xpath("//*[@id='dependencies-list']/li/div/label")
                dependency_list_item = [element.text for element in dependency_list_items]
                if(dependency_list_item==sorted(dependency_list_item)):
                    logger.info("Pass: 1078 dependencies are in alphabetic order")
                else:
                    logger.info("Fail: 1078 dependencies are not in alphabetic order")
                    self.fail(msg="Fail: 1078 dependencies are not in alphabetic order")
                checked_dependency_element=len(self.driver.find_elements_by_xpath("//*[@id='dependencies-list']/li/div/label/input[@type='checkbox'][@checked='checked']"))
                if(checked_dependency_element==len(dependency_list_items)):
                    logger.info("Pass: 1078  All checkboxes are checked by default.")
                else:
                    logger.info("Fail: 1078  All checkboxes are not checked by default.")
                    self.fail(msg="Fail: 1078  All checkboxes are not checked by default.")
                self.driver.find_element_by_xpath("//*[@id='dependencies-modal-form']/div[3]/button[2]").click()
                time.sleep(10)
                self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr[1]/td[7]/a[2]").click()
                time.sleep(50)
                unchecked_dependency_element=(self.driver.find_element_by_xpath("//*[@id='dependencies-list']/li[1]/div/label").text)
                self.driver.find_element_by_xpath("//*[@id='dependencies-list']/li[1]/div/label/input").click()
                time.sleep(10)
                self.driver.find_element_by_xpath("//*[@id='dependencies-modal-form']/div[3]/button[1]").click()
                time.sleep(10)
                logger.info(self.driver.find_element_by_xpath("//*[@id='change-notification-msg']").text)
                if('You have added' in self.driver.find_element_by_xpath("//*[@id='change-notification-msg']").text ):
                    logger.info("Pass: 1078 confirmation message is displayed at the top of the page ")
                else:
                    logger.info("Fail: 1078 confirmation message is not displayed at the top of the page ")
                    self.fail(msg="Fail: 1078 confirmation message is not displayed at the top of the page ")
                if(unchecked_dependency_element not in self.driver.find_element_by_xpath("//*[@id='change-notification-msg']").text ):
                    logger.info("Pass: 1078  Unchecked depndency layer not added and not showing in message as expected ")
                else:
                    logger.info("Fail: 1078  Unchecked depndency layer got added and  showing in message ")
                    self.fail(msg="Fail: 1078  Unchecked depndency layer got added and  showing in message ")
            else:
                    logger.info("Fail: 1078 a dialog didn't appear listing the dependencies.")
                    self.fail(msg="Fail: 1078 a dialog didn't appear listing the dependencies.")
        except:
            logger.info("Fail: 1078 Added layer has not any dependency")
            self.fail(msg="Fail: 1078 Added layer has not any dependency")
        if (self.driver.find_element_by_xpath( "//*[@id='layerstable']/tbody/tr/td[7]/a[contains(@class,'btn btn-danger btn-block')]").text == "Remove layer"):
            logger.info("Pass : 1078 Remove layer button got enabled after adding layer")
        else:
            self.fail(msg="Fail: 1078  Remove layer button  didn't get enabled after adding layer")
            logger.info("Fail: 1078  Remove layer button  didn't get enabled after adding layer")
        self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr/td[7]/a[contains(@class,'btn btn-danger btn-block')]").click()
        time.sleep(10)
        if ("You have removed" in self.driver.find_element_by_id("change-notification-msg").text):
            logger.info("Pass: 1078 Remove message is getting displayed after clicking remove button")
        else:
            self.fail(msg="Fail: 1078 Remove message is getting displayed after clicking remove button")
            logger.info("Fail: 1078 Remove message is getting displayed after clicking remove button")
        if (self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr/td[7]/a[contains(@class,'btn btn-default btn-block')]").text == 'Add layer'):
            logger.info("Pass: 1078 Add layer button got enabled after clicking remove layer")
        else:
            logger.info("Fail: 1078 Add layer button  didn't got enabled after clicking remove layer")
            self.fail(msg="Fail: 1078 Add layer button  didn't got enabled after clicking remove layer")
        print("All test steps passed in test case 1078")
        logger.info("All test steps passed in test case 1078")

    def test_1069_All_layers_default_view(self):
        logger.info("Pass: Test case 1069 started")
        project_name = "1069"
        self.create_new_project(project_name)
        time.sleep(10)
        self.driver.find_element_by_id("view-compatible-layers").click()
        time.sleep(10)
        self.search_element("search-input-layerstable","search-submit-layerstable", "meta-yocto-bsp")
        self.driver.find_element_by_xpath("//*[@id='table-chrome-collapse-layerstable']/form[1]/div/div/span").click()
        time.sleep(10)
        if(int(((((self.driver.find_element_by_xpath("//div[@class='col-md-10']/h2").text).split(' ')[2]).split('('))[1]).split(')')[0])>0):
            logger.info("Pass: 1069 Table is populated with the default layers meta-yocto-basp")
        else:
            logger.info("Fail: 1069 Table is  not populated with the default layers meta-yocto-basp")
            self.fail(msg="Fail: 1069 Table is  not populated with the default layers meta-yocto-bsp")
        layer_head_elements=self.driver.find_elements_by_xpath("//*[@id='layerstable']/thead/tr[1]/th")
        layer_head_element = [element.text for element in layer_head_elements]
        if(layer_head_element == ['Layer', 'Summary', '', '', 'Git revision', 'Dependencies', 'Add | Remove']):
             logger.info("Pass: 1069 default the following columns are shown: as expected")
        else:
            logger.info("Fail: 1069 default the following columns are not shown: as expected")
            self.fail(msg="Fail: 1069 default the following columns are not shown: as expected")

        revision_elements=self.driver.find_elements_by_xpath("//*[@id='layerstable']/tbody/tr/td[5]")
        revision_element = [element.text for element in revision_elements]
        if(set(revision_element)=={'master'}):
             logger.info("Pass: 1069  Revision entries match the release entry from the main project page")
        else:
             self.fail(msg="Fail: 1069 Revision entries match the release entry from the main project page")
             logger.info("Fail: 1069 Revision entries match the release entry from the main project page")
        self.search_element("search-input-layerstable","search-submit-layerstable", "openembedded-core")
        if(int(self.driver.find_element_by_xpath("//div[@class='col-md-10']/h2").text.split(' ')[2].split('(')[1].split(')')[0]) ==1):
            logger.info("Pass: 1069  only one instance of the core layers openembedded-core")
        else:
            logger.info("Fail: 1069  only one instance of the core layers openembedded-core is not present")
            self.fail(msg="Fail: 1069  only one instance of the core layers openembedded-core is not present")
        if(self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr[1]/td[5]").text=='master'):
             logger.info("Pass: 1069 instance has a branch that matches the selected project release from the main project page.")
        else:
             logger.info(
                "Fail: 1069 instance has a branch that  not matches the selected project release from the main project page.")
             self.fail(msg="Fail: 1069 instance has a branch that  not matches the selected project release from the main project page.")
        self.driver.find_element_by_xpath("//*[@id='table-chrome-collapse-layerstable']/form[1]/div/div/span").click()
        time.sleep(100)
        logger.info(int(self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr[1]/td[6]/a").text))
        if(int(self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr[1]/td[6]/a").text)>0):
            logger.info("Pass 1069: dependencies  column are present so we can click and verify further")
            self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr[1]/td[6]/a").click()
            time.sleep(10)
            if('dependencies'  in self.driver.find_element_by_xpath("//h3[@class='popover-title']").text ):
                logger.info("Pass: 1069 A small popup  appeared containing a list of other layers required for this layer to work")
            else:
                logger.info(
                    "Fail: 1069 A small popup didn't appear containing a list of other layers required for this layer to work")
                self.fail(msg="Fail: 1069 A small popup didn't appear containing a list of other layers required for this layer to work")
            if(len(self.driver.find_elements_by_xpath("//div[@class='popover-content']/ul/li/a"))==int(self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr[1]/td[6]/a").text)):
                logger.info("Pass:1069: All dependencies value are correct")
                time.sleep(20)
                self.driver.find_element_by_xpath("(//div[@class='popover-content']/ul/li/a)[1]").click()
                time.sleep(20)
                self.driver.back()
                time.sleep(20)
                self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr[1]/td[6]/a").click()
                time.sleep(10)
                self.driver.find_element_by_xpath("(//div[@class='popover-content']/ul/li/a)[2]").click()
                time.sleep(10)
                self.driver.back()
                time.sleep(20)
            else:
                logger.info("Fail: 1069  All dependencies value are not matching ")
                self.fail(msg="Fail: 1069  All dependencies value are not matching ")
        else:
             logger.info("Pass: 1069 dependencies  column are  not present so we can't click and verify further")
        time.sleep(20)
        self.edit_specicific_checkbox("checkbox-layer__vcs_url")

        self.edit_specicific_checkbox("checkbox-git_subdir")
        self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr[1]/td[3]/a[1]/code").click()
        time.sleep(10)
        self.driver.back()
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@id='layerstable']/tbody/tr[1]/td[4]/a[1]/code").click()
        time.sleep(10)
        self.driver.back()
        time.sleep(10)
        logger.info("All test steps passed in test case 1069")
        print("All test steps passed in test case 1069")






















