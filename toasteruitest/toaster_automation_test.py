#!/usr/bin/python
#
# DESCRIPTION
# This script has toaster_cases class which includes all test cases.
#
import Base_Utility
#from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
import Utility

class toaster_cases(Base_Utility.toaster_cases_base):

    def test_901(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_partial_link_text('builds').click()
        option_ids = ['checkbox-started_on', 'checkbox-failed_tasks', \
                      'checkbox-errors_no', 'checkbox-warnings_no', 'checkbox-time', 'checkbox-image_files', \
                      'checkbox-project']
        self.driver.find_element_by_id("edit-columns-button").click()
        for item in option_ids:
            if not self.driver.find_element_by_id(item).is_selected():
                self.driver.find_element_by_id(item).click()
                time.sleep(3)
        self.driver.find_element_by_id("edit-columns-button").click()
        sorted_column = {'outcome': 1, 'machine': 3, 'completed_on': 4, 'errors_no': 6, 'warnings_no': 8,'project':11}
        for key in sorted_column:
            self.driver.find_element_by_xpath("//a[@data-sort-field='" + key + "']").click()
            time.sleep(3)
            column_list = self.get_table_column_text_by_column_number('allbuildstable',int(sorted_column[key]))
            time.sleep(3)
            if (int(sorted_column[key])!=1):
                self.assertTrue(Utility.is_list_inverted(column_list) or Utility.is_list_sequenced(column_list),
                            msg=("list not in sequence order or  not inverted for %d columns" %int(sorted_column[key])))
            self.driver.find_element_by_xpath("//a[@data-sort-field='" + key + "']").click()
            time.sleep(3)
            column_list = self.get_table_column_text_by_column_number('allbuildstable', int(sorted_column[key]))
            if (int(sorted_column[key]) != 1):
                self.assertTrue(Utility.is_list_inverted(column_list) or Utility.is_list_sequenced(column_list),
                            msg=("list not in sequence order or  not inverted for %d columns" % int(sorted_column[key])))
            time.sleep(2)
        self.log.info("case passed")

    def test_902(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        patterns = ["minimal"]
        self.driver.find_element_by_partial_link_text('builds').click()
        for pattern in patterns:
            self.driver.find_element_by_id("search-input-allbuildstable").clear()
            self.driver.find_element_by_id("search-input-allbuildstable").send_keys(pattern)
            self.driver.find_element_by_id("search-submit-allbuildstable").click()
            time.sleep(3)
            new_target_column_texts = self.get_table_column_text('class', 'target')
            time.sleep(3)
            if new_target_column_texts:
                for text in new_target_column_texts:
                    self.assertTrue(text.find(pattern), msg=("%s item doesn't exist " % pattern))
            self.driver.find_element_by_xpath("(//span[@class='remove-search-btn-allbuildstable glyphicon glyphicon-remove-circle'])[2]").click()
            time.sleep(2)
            self.assertTrue(self.driver.find_element_by_xpath("//h1[@class='top-air']").text == 'All builds',msg=("All builds not found after clear search" ))
        self.log.info("case passed")
    def test_903(self):
        self.case_no = self.get_case_number()
        image_type1 = "core-image-minimal"
        image_type2 = "core-image-sato"
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_partial_link_text('builds').click()
        if (self.driver.find_element_by_xpath("//h1[@class='top-air']").text == 'All builds'):
            self.driver.find_element_by_id("edit-columns-button").click()
            self.driver.find_element_by_id("checkbox-started_on").click()
            self.driver.find_element_by_id("edit-columns-button").click()
            items = ["Outcome", "Completed on", "Started on", 'Failed tasks']
            for item in items:
                try:
                    temp_element = self.find_element_by_text_in_table('allbuildstable', item)
                    time.sleep(3)
                    self.assertTrue(temp_element.find_element_by_xpath(
                        "//a[@data-filter-on='outcome_filter']/i[@class='glyphicon glyphicon-filter filtered']"))
                except Exception as e:
                    self.assertFalse(True, msg=(" %s cannot be found! %s" % (item, e)))
                    raise
            filter_list = ['outcome_filter', 'started_on_filter', 'completed_on_filter','failed_tasks_filter']
            for key in filter_list:
                self.driver.find_element_by_xpath("//*[@id='" + key + "']/i").click()
                time.sleep(2)
                self.driver.find_element_by_xpath("(//label[contains(@for,'" + key + "')] // input[ @ type = 'radio'])[3]").click()
                time.sleep(2)
                self.driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
                time.sleep(2)
                self.driver.find_element_by_id("search-input-allbuildstable").clear()
                self.driver.find_element_by_id("search-input-allbuildstable").send_keys(image_type1)
                time.sleep(2)
                self.driver.find_element_by_id("search-submit-allbuildstable").click()
                self.driver.find_element_by_xpath("//*[@id='" + key + "']/i").click()
                time.sleep(2)
                avail_options = self.driver.find_elements_by_xpath("//label[@class='filter-title']")
                radio_button = self.driver.find_element_by_xpath("//*[@id='" + key + ":all']")
                self.driver.find_element_by_xpath(
                    "//*[@id='filter-modal-allbuildstable']/div/div/div[1]/button").click()
                time.sleep(2)
                if (radio_button.is_selected()):
                    pass
                else:
                    self.assertFalse(True, msg=("Error: All option is not selected after search"))
        self.log.info("case passed")
    def test_904(self):
        Expected_BreadCrumb_Number = 4
        BreadCrumb_String = ["Builds", "core-image-minimal"]
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        Table_id = ['buildtaskstable', 'buildtimetable', 'buildcputimetable', 'buildiotable']
        self.driver.find_element_by_partial_link_text("core-image-minimal").click()
        Checkbox_Table = ["checkbox-order", "checkbox-recipe__name", "checkbox-task_name",
                          'checkbox-recipe__version',
                          "checkbox-task_executed", "checkbox-outcome", "checkbox-sstate_result",
                          'checkbox-elapsed_time',
                          'checkbox-cpu_time_system', 'checkbox-cpu_time_user', 'checkbox-disk_io']
        Shows_Rows_Id = ['table-chrome-collapse-buildtaskstable', 'table-chrome-collapse-buildtimetable',
                         'table-chrome-collapse-buildcputimetable', 'table-chrome-collapse-buildiotable']
        Ui_List = ["Tasks", "Time", "CPU usage", "Disk I/O"]
        SeacrhTaskTable = ['search-input-buildtaskstable', 'search-input-buildtimetable',
                           'search-input-buildcputimetable', 'search-input-buildiotable']
        Expected_Edit_List = {'Tasks': ['Order', 'Recipe', 'Task', 'Executed', 'Outcome', 'Cache attempt'],
                              'Time': ['Recipe', 'Task', 'Executed', 'Outcome', 'Time (secs)'],
                              "CPU usage": ['Recipe', 'Task', 'Executed', 'Outcome', 'System CPU time (secs)',
                                            'User CPU time (secs)'],
                              'Disk I/O': ['Recipe', 'Task', 'Executed', 'Outcome', 'Disk I/O (ms)']}
        count = 0
        for item in Ui_List:
            self.driver.find_element_by_link_text(item).click()
            Total_BreadCrumb_Link = len(self.driver.find_elements_by_xpath("//*[@id='breadcrumb']/li"))
            if (Total_BreadCrumb_Link == Expected_BreadCrumb_Number):
                for i in range(1, Total_BreadCrumb_Link):
                    BreadCrumb_Name = self.driver.find_element_by_xpath("//*[@id='breadcrumb']/li[%d]/a" % i).text
                    self.driver.find_element_by_xpath("//*[@id='breadcrumb']/li[%d]/a" % i).click()
                    self.driver.back()
                Active_BreadCrumb_Link = self.driver.find_element_by_xpath("(//*[@id='breadcrumb']/li)[4]").text
                if (Active_BreadCrumb_Link == "Tasks"):
                    pass
                else:
                    self.assertTrue(Active_BreadCrumb_Link, msg=("Active breadcrumb is not correct"))
            else:
                self.assertTrue(Total_BreadCrumb_Link, msg=("Total Breadcrumb link is not as expected"))
            Total_Number_SideLink = len(self.driver.find_elements_by_xpath("//*[@id='nav']//li/a"))
            for i in range(1, (Total_Number_SideLink - 2)):
                time.sleep(5)
                self.driver.find_element_by_xpath("(//*[@id='nav']//li/a)[%d]" % i).click()
                time.sleep(2)
                self.driver.back()
            Active_Class_Name = self.driver.find_element_by_xpath("//*[@id='build-menu']/li[@class='active']/a").text
            if (Active_Class_Name == item):
                pass
            else:
                self.assertFalse(Active_Class_Name, msg=("Active class not correctly diaplyed"))
            self.assertTrue(self.driver.find_element_by_xpath("//*[@id='" + SeacrhTaskTable[count] + "']"),
                            msg=("search tab not found on page"))
            self.assertTrue(self.driver.find_element_by_xpath(
                "//*[@id='" + SeacrhTaskTable[count] + "'][@placeholder='Search tasks']"),
                            msg=("search Placeholder is search tasks"))
            self.driver.find_element_by_xpath("//*[@id='" + SeacrhTaskTable[count] + "']").click()
            self.driver.find_element_by_xpath("//*[@id='" + SeacrhTaskTable[count] + "']").send_keys("busybox")
            time.sleep(2)
            self.driver.find_element_by_xpath("//button[@class='btn btn-default']").click()
            time.sleep(2)
            column_list_busybox = self.driver.find_elements_by_xpath("//a[text()='busybox']")
            if (len(column_list_busybox) >= 1):
                pass
            else:
                self.assertFalse(len(column_list_busybox),msg=("Error: Seacrh is not successful"))
            self.driver.find_element_by_xpath("//*[@id='" + SeacrhTaskTable[count] + "']").click()
            self.driver.find_element_by_xpath("(//span[contains(@class,'remove-search-btn')])[2]").click()
            edit_Show_Rows = Select(
                self.driver.find_element_by_xpath("//*[@id='" + Shows_Rows_Id[count] + "']/form[2]/div/select"))
            selected_number_rows = "25"
            edit_Show_Rows.select_by_value(selected_number_rows)
            time.sleep(5)
            Total_Row_Num = len(
                self.driver.find_elements_by_xpath("//table[@class='table table-bordered table-hover']/tbody/tr"))
            if selected_number_rows != Total_Row_Num:
                self.assertTrue(Total_Row_Num, msg=("Total number of rows slected are  not correct"))
            else:
                pass
            self.assertTrue(self.driver.find_elements_by_xpath("//ul[@class='pagination']/li"),
                            msg=("Pagination Link not available"))
            self.assertTrue(self.driver.find_element_by_xpath("(//form[@class='navbar-form navbar-right'])[2]"),
                            msg=("Shows Rows option not available at bottom of page"))
            self.driver.find_element_by_id("edit-columns-button").click()
            time.sleep(2)
            Edit_Element = self.driver.find_elements_by_xpath("//*[@class='dropdown-menu editcol']//li//div")
            Edit_Check_List = []
            for element in Edit_Element:
                Edit_Check_List.append(element.text)
            self.driver.find_element_by_id("edit-columns-button").click()
            time.sleep(2)
            self.driver.find_element_by_id("edit-columns-button").click()
            time.sleep(2)
            Actual_Checked_List = []
            for item1 in Checkbox_Table:
                value = self.driver.find_element_by_id(item1).is_selected()
                if value:
                    Actual_Checked_List.append(self.driver.find_element_by_id(item1).find_element_by_xpath('..').text)
            result = all(elem in Actual_Checked_List for elem in Expected_Edit_List[item])
            if result:
                pass
            else:
                self.assertTrue(result, msg=("Error:Edit column list not found as expected"))
            self.driver.find_element_by_id("edit-columns-button").click()
            time.sleep(3)
            self.driver.find_element_by_id("edit-columns-button").click()
            time.sleep(2)
            Edit_Element = self.driver.find_elements_by_xpath("//*[@class='dropdown-menu editcol']//li//div")
            Edit_Check_List = []
            edit_number = 1
            for element in Edit_Element:
                Edit_Check_List.append(element.text)
                Displayed_coulmn_number = len(
                    self.driver.find_elements_by_xpath("//th[contains(@style,'display: none;')]"))
                self.driver.find_element_by_xpath("(//input[@type='checkbox'])[%d]" % edit_number).click()
                time.sleep(10)
                Displayed_coulmn_number_after_click = len(
                    self.driver.find_elements_by_xpath("//th[contains(@style,'display: none;')]"))
                if (Displayed_coulmn_number == Displayed_coulmn_number_after_click):
                    pass
                else:
                    self.driver.find_element_by_xpath("(//input[@type='checkbox'])[%d]" % edit_number).click()
                edit_number = edit_number + 1
            self.driver.find_element_by_id("edit-columns-button").click()
            time.sleep(2)
            self.driver.find_element_by_id("edit-columns-button").click()
            time.sleep(2)
            for item1 in Checkbox_Table:
                if not self.driver.find_element_by_id(item1).is_selected():
                    self.driver.find_element_by_id(item1).click()
                    time.sleep(2)
            self.driver.find_element_by_id("edit-columns-button").click()
            if (item == 'Tasks'):
                if self.driver.find_element_by_xpath("//*[@id='buildtaskstable']/thead/tr/th[1]/a").text == 'Order':
                    pass
                else:
                    self.assertFalse(True, msg=("Error: Order is not bold"))
                self.assertTrue(self.driver.find_element_by_xpath("//*[@id='buildtaskstable']/thead/tr/th[1]/i[1]"),
                                msg=' down-arrow icon are not present ')
                default_column_list = self.get_table_column_text_by_column_number('buildtaskstable', 1)
                self.assertTrue(Utility.is_list_sequenced(default_column_list),
                                msg=("list not in sequence for corresponding column"))
            Column_Head_Len = len(
                self.driver.find_elements_by_xpath("//*[@id='" + Table_id[count] + "']/thead/tr/th"))
            for i in range(2, Column_Head_Len):
                if (i >= 4):
                    i = i + 1
                self.driver.find_element_by_xpath("//*[@id='" + Table_id[count] + "']/thead/tr/th[%d]/a" % i).click()
                time.sleep(10)
                column_list = self.get_table_column_text_by_column_number(Table_id[count], i)
                self.assertTrue(Utility.is_list_sequenced(column_list) or Utility.is_list_inverted(column_list),
                                msg=("list not in sequence  not inverted for corresponding order"))

            filter_list = ['execution_outcome', 'task_outcome', 'sstate_outcome']
            filter_column_number = 5
            for key in filter_list:
                self.driver.find_element_by_xpath("//*[@id='" + key + "']/i").click()
                time.sleep(2)
                avail_options = self.driver.find_elements_by_xpath("//label[@class='filter-title']")
                radio_button = self.driver.find_element_by_xpath("//*[@id='" + key + ":all']")
                self.driver.find_element_by_xpath(
                    "/html/body/div[3]/div[3]/div[2]/div/div[2]/div/div/div[1]/button").click()
                time.sleep(2)
                if (radio_button.is_selected()):
                    pass
                else:
                    self.assertFalse(True, msg=("Error: All option is not selected before channging"))
                for number in range(2, (len(avail_options)) + 1):
                    self.driver.find_element_by_xpath("//*[@id='" + key + "']/i").click()
                    time.sleep(2)
                    if ((number == 4 or number == 5 or number == 6) and key == 'task_outcome'):
                        number = 7
                    if ((number == 4 or number == 5) and key == 'sstate_outcome'):
                        break
                    self.driver.find_element_by_xpath("(//input[@type='radio'])[%d]" % number).click()
                    time.sleep(2)
                    if (number == 7 and key == 'task_outcome'):
                        number = 4
                    match = self.driver.find_element_by_xpath("(//label[@class='filter-title'])[%d]" % number)
                    self.driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
                    time.sleep(2)
                    column_list = self.get_table_column_text_by_column_number(Table_id[count], filter_column_number)
                    column_list_set = set(column_list)
                    column_list_converted = list(column_list_set)
                    if (str(column_list_converted[0]) != ''):
                        if (str(match.text)).find(str(column_list_converted[0])):
                            pass
                        else:
                            self.assertFalse(True, msg=("Error: All option is not selected before channging"))
                    if (number == 4 and key == 'task_outcome'):
                        break
                self.driver.find_element_by_xpath("//*[@id='" + key + "']/i").click()
                time.sleep(2)
                self.driver.find_element_by_xpath("(//input[@type='radio'])[1]").click()
                time.sleep(2)
                self.driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
                time.sleep(2)
                self.driver.find_element_by_xpath("//*[@id='" + key + "']/i").click()
                time.sleep(2)
                radio_button_selected = self.driver.find_element_by_xpath("//*[@id='" + key + ":all']")
                if (radio_button_selected.is_selected()):
                    pass
                else:
                    self.assertFalse(True, msg=("Error:All option is not selected  after chnages"))
                self.driver.find_element_by_xpath(
                    "/html/body/div[3]/div[3]/div[2]/div/div[2]/div/div/div[1]/button").click()
                time.sleep(2)
                filter_column_number = filter_column_number + 1
            Row_Len = len(self.driver.find_elements_by_xpath("//*[@id='" + Table_id[count] + "']/tbody/tr"))
            time.sleep(2)
            for row_number in range(1, Row_Len + 1):
                self.driver.find_element_by_xpath(
                    "//*[@id='" + Table_id[count] + "']/tbody/tr[%d]/td[2]/a" % row_number).click()
                time.sleep(2)
                self.driver.back()
                time.sleep(2)
                self.driver.find_element_by_xpath(
                    "//*[@id='" + Table_id[count] + "']/tbody/tr[%d]/td[3]/a" % row_number).click()
                time.sleep(2)
                self.driver.back()
                time.sleep(2)
            count = count + 1
        self.log.info("case passed")

    def test_906(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        Expected_BreadCrumb_Number = 5
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.find_element_by_link_text_in_table('nav', 'Packages').click()
        self.driver.find_element_by_xpath("//*[@id='builtpackagestable']/tbody/tr[1]/td[1]/a").click()
        Total_BreadCrumb_Link = len(self.driver.find_elements_by_xpath("//*[@id='breadcrumb']/li"))
        if (Total_BreadCrumb_Link == Expected_BreadCrumb_Number):
            for i in range(1, Total_BreadCrumb_Link):
                BreadCrumb_Name = self.driver.find_element_by_xpath("//*[@id='breadcrumb']/li[%d]/a" % i).text
                self.assertTrue(BreadCrumb_Name != '', msg="Breaccrum name not available")
                self.driver.find_element_by_xpath("//*[@id='breadcrumb']/li[%d]/a" % i).click()
                self.driver.back()
                time.sleep(2)
        else:
            self.assertFalse(True, msg=("Error:Total Breadcrumb link is  not as expected"))
        self.driver.find_element_by_xpath("(//ul[@class='breadcrumb']//li)[4]").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@id='builtpackagestable']/tbody/tr[1]/td[1]/a").click()
        time.sleep(1)
        name_package=self.driver.find_element_by_xpath("//div[@class='tab-content']//div[@class='tab-pane active']//div").text
        if 'Package included in' in name_package:
            self.driver.find_element_by_xpath("//div[@class='well']")
            self.driver.find_element_by_xpath("//div[@class='page-header build-data']")
        else:
            if ('Generated files' in self.driver.find_element_by_xpath("(//div[@class='col-md-8 tabbable']/ul/li/a)[1]").text):
                pass
            else:
                self.assertFalse(True, msg=("Error correct active string not diaplyed"))
            if ('Runtime dependencies' in self.driver.find_element_by_xpath("(//div[@class='col-md-8 tabbable']/ul/li/a)[2]").text):
                pass
            else:
                self.assertFalse(True, msg=("Error correct  string not diaplyed in 2nd tab"))
            self.driver.find_element_by_partial_link_text("Generated files").click()
            string_generated_file = self.driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[1]/ul/li[1]/a").text
            generate_files_row_number = len(self.driver.find_elements_by_xpath(
                "//table[@class='table table-bordered table-hover tablesorter']/tbody/tr"))
            expected_value_generated_files = (((string_generated_file.split()[2]).split('(')[1]).split(')'))[0]
            if (int(expected_value_generated_files)>0):
                if (generate_files_row_number == int(expected_value_generated_files) ):
                    head_list = self.get_table_head_text('otable')
                    for item in ['File', 'Size']:
                        self.assertTrue(item in head_list, msg=("%s not in head row" % item))
                    c_list = self.get_table_column_text('class', 'path')
                    self.assertTrue(Utility.is_list_sequenced(c_list), msg=("column not in order"))
                else:
                    self.assertFalse(True, msg=("Error: row number is not correct for generated files"))
            self.driver.find_element_by_partial_link_text("Runtime dependencies").click()
            string_runtime_dependencies = self.driver.find_element_by_xpath(
                "/html/body/div[3]/div[3]/div[1]/ul/li[2]/a").text
            runtime_dependencies_row_number = len(
                self.driver.find_elements_by_xpath("//table[@class='table table-bordered table-hover']/tbody/tr"))
            expected_value_runtime_dependencies = (((string_runtime_dependencies.split()[2]).split('(')[1]).split(')'))[
                0]
            if (int(expected_value_runtime_dependencies) > 0):
                if (runtime_dependencies_row_number == int(expected_value_runtime_dependencies)):
                    head_list = self.get_table_head_text('dependencies')
                    for item in ['Package', 'Version', 'Size']:
                        self.assertTrue(item in head_list, msg=("%s not in head row" % item))
                    c_list = self.get_table_column_text_by_column_number('dependencies', 1)
                    self.assertTrue(Utility.is_list_sequenced(c_list), msg=("list not in order"))
                else:
                    self.assertFalse(True, msg=("Error: row number is not correct for runtime dependencies"))
            texts = ['Size', 'License', 'Recipe', 'Recipe version', 'Layer', 'Layer'' commit']
            if (len(self.driver.find_elements_by_xpath(
                    "//dl//span[@class='glyphicon glyphicon-question-sign get-help']")) == 7):
                pass
            else:
                self.assertFalse(True, msg=("Error: total number of help option is  not correct"))
            self.failUnless(self.is_text_present(texts))
            time.sleep(3)
            self.driver.find_element_by_xpath("//*[@id='breadcrumb']/li[4]/a").click()
            time.sleep(3)
            self.driver.find_element_by_id("search-input-builtpackagestable").click()
            self.driver.find_element_by_id("search-input-builtpackagestable").send_keys("busybox")
            self.driver.find_element_by_id("search-submit-builtpackagestable").click()
            time.sleep(2)
            self.driver.find_element_by_xpath("//*[@id='builtpackagestable']/tbody/tr[1]/td[1]/a").click()
            if (self.driver.find_element_by_xpath("//div[@class='lead well']").text != ''):
                self.driver.find_element_by_xpath("//div[@class='lead well']").click()
        self.log.info("case passed")
    def test_910(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        image_type = "core-image-minimal"
        test_package1 = "busybox"
        test_package2 = "lib"
        section_column_number = 6
        self.driver.find_element_by_link_text(image_type).click()
        self.driver.find_element_by_link_text("Recipes").click()
        default_column_list = self.get_table_column_text_by_column_number('builtrecipestable', 1)
        self.assertTrue(Utility.is_list_sequenced(default_column_list),
                        msg=("list not in sequence order deafault column Recipes"))
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(2)
        self.driver.find_element_by_id("checkbox-section").click()
        time.sleep(2)
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//th[@class='section']/a").click()
        time.sleep(2)
        column_list_after_section = self.get_table_column_text_by_column_number('builtrecipestable',
                                                                                section_column_number)
        self.assertTrue(Utility.is_list_sequenced(column_list_after_section))
        self.driver.find_element_by_id("search-input-builtrecipestable").click()
        self.driver.find_element_by_id("search-input-builtrecipestable").send_keys(test_package1)
        self.driver.find_element_by_xpath("//button[@class='btn btn-default']").click()
        time.sleep(2)
        self.driver.find_element_by_id("search-input-builtrecipestable").click()
        time.sleep(2)
        self.driver.find_element_by_xpath(
            "//*[@id='table-chrome-collapse-builtrecipestable']/form[1]/div/div/span").click()
        time.sleep(2)
        column_list_Section_after_search = self.get_table_column_text_by_column_number('builtrecipestable',
                                                                                       section_column_number)
        self.assertTrue(Utility.is_list_sequenced(column_list_Section_after_search))
        option_ids = ['checkbox-name', 'checkbox-version', \
                      'checkbox-dependencies', 'checkbox-revdeps', 'checkbox-file_path', 'checkbox-section', \
                      'checkbox-license', 'checkbox-layer_version__layer__name', 'checkbox-layer_version__branch',
                      'checkbox-commit']
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(2)
        for item1 in option_ids:
            if not self.driver.find_element_by_id(item1).is_selected():
                self.driver.find_element_by_id(item1).click()
                time.sleep(2)

        self.driver.find_element_by_id("edit-columns-button").click()
        column_head = ['Recipe', 'Section', 'License', 'Layer', 'Layer branch']
        column_number = 1
        for item in column_head:
            time.sleep(2)
            self.find_element_by_link_text_in_table('builtrecipestable', item).click()
            time.sleep(2)
            if column_number == 2:
                column_number = section_column_number
            column_list_packages = self.get_table_column_text_by_column_number('builtrecipestable', column_number)
            self.assertTrue(Utility.is_list_sequenced(column_list_packages) or Utility.is_list_inverted(column_list_packages),
                            msg=("list not in sequence order or  not inverted for %s columns" % item))
            column_number = column_number + 1
        self.find_element_by_link_text_in_table('builtrecipestable', 'Recipe').click()
        time.sleep(2)
        column_number = 1
        for item in column_head:
            self.find_element_by_link_text_in_table('builtrecipestable', item).click()
            time.sleep(2)
            if column_number == 2:
                column_number = section_column_number
            column_list_packages = self.get_table_column_text_by_column_number('builtrecipestable', column_number)
            self.assertTrue(Utility.is_list_sequenced(column_list_packages) or Utility.is_list_inverted(column_list_packages),
                            msg=("list not in sequence order or  not inverted for %s columns before serach" % item))
            self.driver.find_element_by_id("search-input-builtrecipestable").click()
            self.driver.find_element_by_id("search-input-builtrecipestable").send_keys(test_package2)
            self.driver.find_element_by_xpath("//button[@class='btn btn-default']").click()
            time.sleep(2)
            column_list_packages_after_search = self.get_table_column_text_by_column_number('builtrecipestable',column_number)
            self.assertTrue(
                Utility.is_list_sequenced(column_list_packages_after_search) or Utility.is_list_inverted(column_list_packages),
                msg=("list not in sequence order or  not inverted for %s columns after serach" % item))
            self.driver.find_element_by_id("search-input-builtrecipestable").click()
            time.sleep(2)
            self.driver.find_element_by_xpath(
                "//*[@id='table-chrome-collapse-builtrecipestable']/form[1]/div/div/span").click()
            column_number = column_number + 1
        table_head_dict = {'Section': 'checkbox-section', 'License': 'checkbox-license',
                           'Layer': 'checkbox-layer_version__layer__name',
                           'Layer branch': 'checkbox-layer_version__branch'}
        for key in table_head_dict:
            self.find_element_by_link_text_in_table('builtrecipestable', key).click()
            time.sleep(2)
            self.driver.find_element_by_id("edit-columns-button").click()
            self.driver.find_element_by_id(table_head_dict[key]).click()
            self.driver.find_element_by_id("edit-columns-button").click()
            default_column_list = self.get_table_column_text_by_column_number('builtrecipestable', 1)
            self.assertTrue(Utility.is_list_sequenced(default_column_list),
                            msg=("list not in sequence order deafault column Recipes"))
        time.sleep(2)
        self.driver.find_element_by_id("edit-columns-button").click()
        self.driver.find_element_by_id('checkbox-license').click()
        time.sleep(2)
        self.driver.find_element_by_id('checkbox-layer_version__layer__name').click()
        time.sleep(2)
        self.driver.find_element_by_id("edit-columns-button").click()
        self.log.info("case passed")
    def test_911(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        searched_recipies = 'hfidf'
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.find_element_by_link_text_in_table('nav', 'Recipes').click()
        self.driver.find_element_by_xpath("//*[@placeholder='Search recipes built']")
        self.driver.find_element_by_id("search-input-builtrecipestable")
        time.sleep(5)
        self.driver.find_element_by_id("search-input-builtrecipestable").clear()
        self.driver.find_element_by_id("search-input-builtrecipestable").send_keys("lib")
        time.sleep(5)
        self.driver.find_element_by_id("search-submit-builtrecipestable").click()
        time.sleep(3)
        seacrhed_string = self.driver.find_element_by_xpath("//div[@class='page-header build-data']").text
        seacrhed_string_value = int(((seacrhed_string.split()[2].split('(')[1].split(')'))[0]))
        if (seacrhed_string_value == 0):
            self.driver.find_element_by_id("new-search-input-builtrecipestable")
            self.driver.find_element_by_xpath("//*[@id='no-results-builtrecipestable']/div/form/button[2]").click()
            time.sleep(5)
        elif (seacrhed_string_value > 0):
            self.driver.find_element_by_id("search-submit-builtrecipestable").click()
            time.sleep(5)
            self.driver.find_element_by_xpath(
                "//*[@id='table-chrome-collapse-builtrecipestable']/form[1]/div/div/span").click()
        else:
            self.assertFalse(True, msg=("Error: Searched text not found in expected output"))
        head_list = self.get_table_head_text('builtrecipestable')
        self.assertTrue(head_list == ['Recipe', 'Version', 'Dependencies', 'Reverse dependencies', 'License', 'Layer'], \
                        msg=("head row contents wrong"))
        head_list_sort = self.get_table_head_text('builtrecipestable')
        self.find_element_by_link_text_in_table('builtrecipestable', 'Recipe').click()
        time.sleep(7)
        sort_list = self.get_table_column_text_by_column_number('builtrecipestable', 1)
        self.assertTrue(Utility.is_list_inverted(sort_list), msg=("list not inverted"))

        self.driver.find_element_by_id("search-input-builtrecipestable").clear()
        self.driver.find_element_by_id("search-input-builtrecipestable").send_keys("bash")
        time.sleep(2)
        self.driver.find_element_by_id("search-submit-builtrecipestable").click()
        time.sleep(2)
        head_list = self.get_table_head_text('builtrecipestable')
        self.assertTrue(head_list == ['Recipe', 'Version', 'Dependencies', 'Reverse dependencies', 'License', 'Layer'], \
                        msg=("head row contents wrong"))
        head_list = self.get_table_head_text('builtrecipestable')
        self.assertTrue(head_list == ['Recipe', 'Version', 'Dependencies', 'Reverse dependencies', 'License', 'Layer'], \
                        msg=("head row contents wrong"))
        sort_list = self.get_table_column_text_by_column_number('builtrecipestable', 1)
        self.assertTrue(Utility.is_list_inverted(sort_list), msg=("list not in order"))
        time.sleep(2)
        self.driver.find_element_by_id("search-input-builtrecipestable").clear()
        self.driver.find_element_by_xpath(
            "//*[@id='table-chrome-collapse-builtrecipestable']/form[1]/div/div/span").click()
        self.driver.find_element_by_id("search-input-builtrecipestable").clear()
        self.driver.find_element_by_id("search-input-builtrecipestable").send_keys("no such input")
        self.driver.find_element_by_id("search-submit-builtrecipestable").click()
        time.sleep(3)
        self.log.info("case passed")
    def test_912(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.find_element_by_link_text_in_table('nav', 'Recipes').click()
        head_list = self.get_table_head_text('builtrecipestable')
        head = ['Recipe', 'Version', 'Dependencies', 'Reverse dependencies', 'License', 'Layer']
        time.sleep(3)
        for item in head:
            self.assertTrue(item in head_list, msg=("item %s not in head row" % item))
            time.sleep(3)
        self.driver.find_element_by_id("edit-columns-button").click()
        self.driver.find_element_by_xpath("//*[@id='checkbox-file_path']").click()
        self.driver.find_element_by_xpath("//*[@id='checkbox-section']").click()

        self.driver.find_element_by_xpath("//*[@id='checkbox-layer_version__branch']").click()
        self.driver.find_element_by_xpath("//*[@id='checkbox-commit']").click()
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(3)
        check_list = ['Dependencies', 'License', 'Recipe file', 'Section', 'Layer', 'Layer branch', 'Layer commit',
                      'Reverse dependencies']
        head_list = self.get_table_head_text('builtrecipestable')
        time.sleep(2)
        for item in check_list:
            self.assertTrue(item in head_list, msg=("item %s not in head row" % item))
        self.driver.find_element_by_id("edit-columns-button").click()
        self.driver.find_element_by_xpath("//*[@id='checkbox-dependencies']").click()
        self.driver.find_element_by_xpath("//*[@id='checkbox-revdeps']").click()
        self.driver.find_element_by_xpath("//*[@id='checkbox-file_path']").click()
        self.driver.find_element_by_xpath("//*[@id='checkbox-section']").click()
        self.driver.find_element_by_xpath("//*[@id='checkbox-license']").click()
        self.driver.find_element_by_xpath("//*[@id='checkbox-layer_version__layer__name']").click()
        self.driver.find_element_by_xpath("//*[@id='checkbox-layer_version__branch']").click()
        self.driver.find_element_by_xpath("//*[@id='checkbox-commit']").click()
        self.driver.find_element_by_id("edit-columns-button").click()
        head_list = self.get_table_head_text('builtrecipestable')
        for item in check_list:
            self.assertFalse(item in head_list, msg=("item %s should not be in head row" % item))
        self.log.info("case passed")
    def test_913(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.find_element_by_link_text_in_table('nav', 'Recipes').click()
        head_list = self.get_table_head_text('builtrecipestable')
        for item in ['Recipe', 'Version', 'Dependencies', 'Reverse dependencies', 'License', 'Layer']:
            self.assertTrue(item in head_list, msg=("item %s not in head row" % item))
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(10)
        if (len(self.driver.find_elements_by_xpath("//label[@class='text-muted']")) == 2):
            pass
        else:
            self.assertFalse(True, msg=("Fail: Muted element is not correct"))
        time.sleep(1)
        self.driver.find_element_by_id("edit-columns-button").click()
        self.log.info("case passed")
    def test_914(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        image_type = "core-image-minimal"
        test_package2 = "gdbm"
        No_dependecies_msg = "has no build dependencies."
        No_dependecies_Pkg_msg = "does not build any packages."
        No_Reverse_dependecies_msg = "has no reverse build dependencies."
        Search_Build_List = ["gettext-native", "libtool-cross"]
        self.driver.find_element_by_link_text(image_type).click()
        self.driver.find_element_by_link_text("Recipes").click()
        default_column_list = self.get_table_column_text_by_column_number('builtrecipestable', 1)
        for row_number in range(1, len(default_column_list) + 1):
            self.driver.find_element_by_xpath(
                "// *[ @ id = 'builtrecipestable'] // tbody // tr[%d] // td // a[contains( @ href, 'recipe')]" % row_number).click()
            time.sleep(2)
            build_dependecies = self.driver.find_element_by_xpath("//a[@href='#dependencies']")
            string_dependcies = str(build_dependecies.text)
            build_dependecies_num = (int(((string_dependcies.split('('))[1].split(')'))[0]))
            build_dependecies.click()
            time.sleep(2)
            if (build_dependecies_num > 0):
                dependencies_length = len(self.driver.find_elements_by_xpath(
                    "(//table[@class='table table-bordered table-hover'])[2]//tbody//tr"))
                if (dependencies_length == build_dependecies_num):
                    pass
                else:
                    self.assertFalse(True, msg=("Error: Total number of dependencies are correct"))
            else:
                output_string1 = (self.driver.find_element_by_xpath("//div[@class='alert alert-info']").text)
                if (No_dependecies_msg in output_string1):
                    pass
                else:
                    self.assertFalse(True, msg=("Error: Not correct output string"))
            time.sleep(2)
            Reverse_build_dependecies = self.driver.find_element_by_xpath("//a[@href='#brought-in-by']")
            Reverse_string_dependcies = str(Reverse_build_dependecies.text)
            Reverse_build_dependecies_num = (int(((Reverse_string_dependcies.split('('))[1].split(')'))[0]))
            Reverse_build_dependecies.click()
            time.sleep(2)
            if (Reverse_build_dependecies_num > 0):
                Reverse_dependencies_length = len(
                    self.driver.find_elements_by_xpath("//*[@id='brought-in-by']/table/tbody/tr"))
                if (Reverse_dependencies_length == Reverse_build_dependecies_num):
                    Column_number = len(
                        self.driver.find_elements_by_xpath("// *[@id ='brought-in-by']/table/thead/tr/th"))
                    for i in range(1, Reverse_dependencies_length + 1):
                        for j in range(1, Column_number + 1):
                            Reverse_Recipie_name = self.driver.find_element_by_xpath(
                                "//*[@id='brought-in-by']/table/tbody/tr[%d]/td[%d]" % (i, j))
                            if (Reverse_Recipie_name.text != ''):
                                if (j == 1):
                                    Reverse_Recipie_name_link = self.driver.find_element_by_xpath(
                                        "//*[@id='brought-in-by']/table/tbody/tr[%d]/td[%d]/a" % (i, j))
                                    action = ActionChains(self.driver)
                                    action.move_to_element(Reverse_Recipie_name_link).perform()
                                    url = Reverse_Recipie_name_link.get_attribute("href")
                                    self.assertTrue(url,
                                                    msg=("url not found for corresponding reverse dependencies"))
                            else:
                                self.assertFalse(True, msg=("Error! Corresponding name and size are not avaialbale for reverse build dependencies"))
                else:
                    self.assertFalse(True, msg=("Error:Total number of Reverse dependencies are not  correct"))
            else:
                output_string1 = (self.driver.find_element_by_xpath("//div[@class='alert alert-info']").text)
                if (No_Reverse_dependecies_msg in output_string1):
                    pass
                else:
                    self.assertFalse(True, msg=("Error: Correct output string has not been displayed"))
            time.sleep(2)
            if (row_number != (len(default_column_list))):
                self.driver.back()
            time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='breadcrumb']/li[4]/a").click()
        time.sleep(4)
        self.driver.find_element_by_id("search-input-builtrecipestable").click()
        self.driver.find_element_by_id("search-input-builtrecipestable").send_keys(test_package2)
        self.driver.find_element_by_xpath("//button[@class='btn btn-default']").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='builtrecipestable']/tbody/tr/td[1]/a").click()
        Package_dependencies = self.driver.find_element_by_xpath("//a[contains(@href,'recipe_packages')]")
        string_Package_dependencies = str(Package_dependencies.text)
        Package_dependecies_num = (int(((string_Package_dependencies.split('('))[1].split(')'))[0]))
        Package_dependencies.click()
        time.sleep(2)
        if (Package_dependecies_num > 0):
            Package_edit_Show_Rows = Select(
                self.driver.find_element_by_xpath("//*[@id='packages-built']/form[2]/div/select"))
            selected_number_rows = "150"
            Package_edit_Show_Rows.select_by_value(selected_number_rows)
            time.sleep(5)
            Package_dependendencies_length = len(self.driver.find_elements_by_xpath(
                "//table[@class='table table-bordered table-hover tablesorter']/tbody/tr"))
            if (Package_dependendencies_length == Package_dependecies_num):
                pass
            else:
                self.assertFalse(True, msg=("Error: Total number of packages in searched recipie are  not correct"))
        else:
            Package_output_string = (self.driver.find_element_by_xpath("//div[@class='alert alert-info']").text)
            if (No_dependecies_Pkg_msg in Package_output_string):
                pass
            else:
                self.assertFalse(True, msg=("Error : Correct output string not diaplyed for searched recipie"))
        time.sleep(2)
        Search_build_dependencies = self.driver.find_element_by_xpath("//a[contains(@href,'active_tab/3')]")
        string_Search_dependencies = str(Search_build_dependencies.text)
        Search_build_dependencies_num = (int(((string_Search_dependencies.split('('))[1].split(')'))[0]))
        Search_build_dependencies.click()
        time.sleep(5)
        if (Search_build_dependencies_num > 0):
            Searc_dependencies_length = len(self.driver.find_elements_by_xpath(
                "(//table[@class='table table-bordered table-hover'])[2]//tbody//tr"))
            if (Searc_dependencies_length == Search_build_dependencies_num):
                pass
                Search_Column_number_Dependencies = len(
                    self.driver.find_elements_by_xpath("// *[@id ='dependencies']/table/thead/tr/th"))
                Search_Build_Recipies_List = []
                for i in range(1, Searc_dependencies_length + 1):
                    for j in range(1, Search_Column_number_Dependencies + 1):
                        Search_Recipie_name = self.driver.find_element_by_xpath(
                            "//*[@id='dependencies']/table/tbody/tr[%d]/td[%d]" % (i, j))
                        if (Search_Recipie_name.text != ''):
                            if (j == 1):
                                Search_Recipie_name_link = self.driver.find_element_by_xpath(
                                    "//*[@id='dependencies']/table/tbody/tr[%d]/td[%d]/a" % (i, j))
                                Search_Build_Recipies_List.append(Search_Recipie_name_link.text)
                                action = ActionChains(self.driver)
                                action.move_to_element(Search_Recipie_name_link).perform()
                                time.sleep(2)
                                url = Search_Recipie_name_link.get_attribute("href")
                                self.assertTrue(url, msg=("url not found for search build dependencies"))
                        else:
                            self.assertFalse(True, msg=("Error! Corresponding name and size are not avaialbale for searched  recipie build dependencies"))
                result = all(elem in Search_Build_Recipies_List for elem in Search_Build_List)
                if result:
                    pass
                else:
                    self.assertFalse(True, msg=("Error:Serached list not found"))
            else:
                self.assertFalse(True, msg=("Error: Total number of dependencies in searched recipie are correct"))
        time.sleep(2)

        Search_Reverse_build_dependencies = self.driver.find_element_by_xpath("//a[@href='#brought-in-by']")
        Search_Reverse_string_dependencies = str(Search_Reverse_build_dependencies.text)
        Search_Reverse_build_dependencies_num = (
            int(((Search_Reverse_string_dependencies.split('('))[1].split(')'))[0]))
        Search_Reverse_build_dependencies.click()
        time.sleep(2)
        if (Search_Reverse_build_dependencies_num > 0):
            Search_Reverse_dependencies_length = len(
                self.driver.find_elements_by_xpath("//*[@id='brought-in-by']/table/tbody/tr"))
            if (Search_Reverse_dependencies_length == Search_Reverse_build_dependencies_num):
                Search_Reverse_Column_number = len(
                    self.driver.find_elements_by_xpath("// *[@id ='brought-in-by']/table/thead/tr/th"))
                for i in range(1, Search_Reverse_dependencies_length + 1):
                    for j in range(1, Search_Reverse_Column_number + 1):
                        Search_Reverse_build_Recipie_name = self.driver.find_element_by_xpath(
                            "//*[@id='brought-in-by']/table/tbody/tr[%d]/td[%d]" % (i, j))
                        if (j == 1):
                            Search_Reverse_Recipie_name_link = self.driver.find_element_by_xpath(
                                "//*[@id='brought-in-by']/table/tbody/tr[%d]/td[%d]/a" % (i, j))
                            action = ActionChains(self.driver)
                            action.move_to_element(Search_Reverse_Recipie_name_link).perform()
                            time.sleep(2)
                            url = Search_Reverse_Recipie_name_link.get_attribute("href")
                            self.assertTrue(url, msg=("url not found for search  reverse build dependencies"))
            else:
                self.assertFalse(True, msg=("Error: Total number of Reverse dependencies are  not correct in serached recipies"))
        if (Search_Reverse_build_dependencies_num == 0):
            output_string1 = (self.driver.find_element_by_xpath("//div[@class='alert alert-info']").text)
            if (No_Reverse_dependecies_msg in output_string1):
                pass
            else:
                self.assertFalse(True, msg=("Error:Correct output string has been displayed for serached string"))
        self.driver.find_element_by_xpath("//*[@id='breadcrumb']/li[3]/a").click()
        self.driver.find_element_by_link_text("Packages").click()
        time.sleep(2)
        packages_num = self.driver.find_element_by_class_name("table-count-builtpackagestable").text
        edit_Show_Rows = Select(
            self.driver.find_element_by_xpath("(//select[@class='form-control pagesize-builtpackagestable'])[1]"))
        selected_number_rows = "150"
        edit_Show_Rows.select_by_value(selected_number_rows)
        time.sleep(2)
        Total_page_number=int(packages_num)/ int(selected_number_rows)
        #Total_page_number = 4
        packages_row_count = 0
        page_navigation_link = 1
        for i in range(1, (Total_page_number + 1)):
            if (page_navigation_link > 4):
                page_navigation_link = 4
            time.sleep(2)
            self.driver.find_element_by_xpath("(//*[@id='pagination-builtpackagestable']/ul//li//a[contains(@href,page)])[%d]" % page_navigation_link).click()
            time.sleep(2)
            packages_row_count = packages_row_count + len(
                self.driver.find_elements_by_xpath("//*[@id='builtpackagestable']/tbody/tr"))
            page_navigation_link = page_navigation_link + 1
        if int(packages_num) >= int(packages_row_count):
            pass
        else:
            self.assertFalse(True, msg=("Error! The packages number is not correct"))
        edit_Show_Rows = Select(
            self.driver.find_element_by_xpath("(//select[@class='form-control pagesize-builtpackagestable'])[1]"))
        selected_number_rows = "25"
        edit_Show_Rows.select_by_value(selected_number_rows)
        time.sleep(5)
        row_count = len(self.driver.find_elements_by_xpath("//*[@id='builtpackagestable']/tbody/tr"))
        for count in range(1, row_count + 1):
            if ((self.driver.find_element_by_xpath(
                    "//*[@id='builtpackagestable']//tbody//tr[%d]//td[2]" % count).text) == ''):
                self.assertFalse(True, msg=("Error! Version is not present for corresponding package"))
            else:
                pass

            if ((self.driver.find_element_by_xpath(
                    "//*[@id='builtpackagestable']//tbody//tr[%d]//td[3]" % count).text) == ''):
                self.assertFalse(True, msg=("Error! Size is not present for corresponding package"))
            else:
                pass

            package_link = self.driver.find_element_by_xpath(
                "//*[@id='builtpackagestable']/tbody/tr[%d]/td[1]/a" % count)
            action = ActionChains(self.driver)
            action.move_to_element(package_link).perform()
            url = package_link.get_attribute("href")
            self.assertTrue(url, msg=("url not found for corresponding packages"))

    def test_915(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        searched_key = 'hfidf'
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.find_element_by_link_text_in_table('nav', 'Configuration').click()
        self.driver.find_element_by_link_text("BitBake variables").click()
        self.driver.find_element_by_xpath("//*[@placeholder='Search BitBake variables']")
        self.driver.find_element_by_id("search").clear()
        self.driver.find_element_by_id("search").send_keys(searched_key)
        self.driver.find_element_by_id("search-button").click()
        if (
        self.driver.find_element_by_xpath("//div[@class='page-header build-data']").text.find(" No variables found")):
            self.driver.find_element_by_xpath("//*[@value='" + searched_key + "']")
            self.driver.find_element_by_xpath("//*[@id='searchform']/button[2]").click()
            time.sleep(5)
        elif (self.driver.find_element_by_xpath("//div[@class='page-header build-data']").text.find("variables found")):
            self.driver.find_element_by_id("search").click()
            self.driver.find_element_by_xpath("//*[@id='searchform']/div/div/a/span").click()
        else:
            self.assertFalse(True, msg=("Error:Searched text not found in ex[ected output"))
        head_list = self.get_table_head_text('otable')
        self.assertTrue(head_list == ['Variable', 'Value', 'Set in file', 'Description'], \
                        msg=("head row contents wrong"))
        head_list_sort = self.get_table_head_text('otable')
        self.find_element_by_link_text_in_table('otable', 'Variable').click()
        sort_list = self.get_table_column_text_by_column_number('otable', 1)
        self.assertTrue(Utility.is_list_inverted(sort_list), msg=("list not inverted"))

        self.driver.find_element_by_id("search").clear()
        self.driver.find_element_by_id("search").send_keys("poky")
        self.driver.find_element_by_id("search-button").click()
        head_list = self.get_table_head_text('otable')
        self.assertTrue(head_list == ['Variable', 'Value', 'Set in file', 'Description'], \
                        msg=("head row contents wrong"))
        head_list = self.get_table_head_text('otable')
        self.assertTrue(head_list == ['Variable', 'Value', 'Set in file', 'Description'], \
                        msg=("head row contents wrong"))
        sort_list = self.get_table_column_text_by_column_number('otable', 1)
        self.assertTrue(Utility.is_list_inverted(sort_list), msg=("list not in order"))
        time.sleep(2)
        self.driver.find_element_by_id("search").clear()
        self.driver.find_element_by_xpath("//*[@id='searchform']/div/div/a/span").click()
        self.driver.find_element_by_xpath("(//span[@class='glyphicon glyphicon-filter filtered'])[1]").click()
        time.sleep(10)
        self.driver.find_element_by_xpath("(//input[@type='radio'])[2]").click()
        self.driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
        self.driver.find_element_by_id("search").clear()
        self.driver.find_element_by_id("search").send_keys("poky")
        self.driver.find_element_by_id("search-button").click()
        self.driver.find_element_by_xpath("(//span[@class='glyphicon glyphicon-filter filtered'])[1]").click()
        radio_button = self.driver.find_element_by_xpath(
            "//*[@id='filter_vhistory__file_name']/div/div/form/div[2]/div[1]/label/input")
        time.sleep(3)
        if (radio_button.is_selected()):
            pass
        else:
            self.assertFalse(True, msg=("Error: Filter  not got cleared after search"))

    def test_916(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.driver.find_element_by_link_text('Configuration').click()
        self.driver.find_element_by_link_text("BitBake variables").click()
        variable_list = self.get_table_column_text('class', 'variable_name')
        self.assertTrue(Utility.is_list_sequenced(variable_list), msg=("list not in order"))
        self.find_element_by_link_text_in_table('otable', 'Variable').click()
        variable_list = self.get_table_column_text('class', 'variable_name')
        self.assertTrue(Utility.is_list_inverted(variable_list), msg=("list not inverted"))
        self.find_element_by_link_text_in_table('otable', 'Variable').click()
        self.driver.find_element_by_id("search").clear()
        self.driver.find_element_by_id("search").send_keys("lib")
        self.driver.find_element_by_id("search-button").click()
        variable_list = self.get_table_column_text('class', 'variable_name')
        self.assertTrue(Utility.is_list_sequenced(variable_list), msg=("list not in order"))

    def test_923(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_xpath("//*[@id='global-nav']/ul/li[1]/a").click()
        page_header = self.driver.find_elements_by_xpath("//div[@class='page-header']")
        if (len(page_header) == 2):
            if (self.driver.find_element_by_xpath("(//div[@class='page-header'])[1]").text == 'Latest builds'):
                print("Latest builds string is present ")
            elif (self.driver.find_element_by_xpath("(//div[@class='page-header'])[2]").text == 'All builds'):
                print("All builds string is present")
        else:
            if (self.driver.find_element_by_xpath("(//div[@class='page-header'])[1]").text == 'All builds'):
                print("All builds string is only present")
        time.sleep(3)
        c_list = self.get_table_column_text('class', 'completed_on')
        self.assertTrue(Utility.is_list_inverted(c_list), msg=("list not inverted"))
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(3)
        self.driver.find_element_by_id("checkbox-started_on").click()
        time.sleep(3)
        self.driver.find_element_by_id("checkbox-time").click()
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(3)
        self.log.info(
            "Checking column headings : outcome, recipe, machine, started on, completed on, failed tasks, errors, warnings, time, image files, project from Table")
        head_list = self.get_table_head_text('table-container-allbuildstable')
        for item in ['Outcome', 'Recipe', 'Machine', 'Started on', 'Completed on', 'Failed tasks', 'Errors', 'Warnings',
                     'Time', "Image files", "Project"]:
            self.failUnless(item in head_list, msg=item + ' is missing from table head.')
        self.log.info("All column heading are there")

    def test_924(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(
            "http://localhost:8000/toastergui/builds/?limit=25&page=1&orderby=-completed_on&default_orderby=-completed_on&")
        c_list = self.get_table_column_text('class', 'completed_on')
        self.assertTrue(Utility.is_list_inverted(c_list), msg=("list not inverted"))
        self.driver.find_element_by_id("edit-columns-button").click()
        self.driver.find_element_by_id("checkbox-errors_no").click()
        head_list1 = self.get_table_head_text('allbuildstable')
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(1)
        self.driver.find_element_by_id("edit-columns-button").click()
        self.driver.find_element_by_id("checkbox-errors_no").click()
        head_list2 = self.get_table_head_text('allbuildstable')
        self.driver.find_element_by_id("edit-columns-button").click()
        self.assertTrue(len(head_list2) != len(head_list1), msg=("Error: head order is  not correct"))

    def test_940(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.find_element_by_link_text_in_table('nav', 'Packages').click()
        check_head_list = [u'Package', u'Package Version', u'Approx Size', ]
        head_list = self.get_table_head_text('builtpackagestable')
        self.assertTrue(head_list == check_head_list, msg=("head row not as expected"))
        time.sleep(3)
        option_ids = ['checkbox-recipe__layer_version__layer__name', 'checkbox-recipe__layer_version__branch', \
                      'checkbox-vcs_ref', 'checkbox-license', 'checkbox-recipe__name', 'checkbox-recipe__version']
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(3)
        for item in option_ids:
            if not self.driver.find_element_by_id(item).is_selected():
                self.driver.find_element_by_id(item).click()
                time.sleep(3)
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(2)
        Minimum_Table_len = len(self.driver.find_elements_by_xpath("//label[@class='text-muted']"))
        elements = self.driver.find_elements_by_xpath("//label[@class='text-muted']")
        Minimum_Table_len = len(elements)
        if (int(Minimum_Table_len) == 2):
            for item in elements:
                self.driver.find_element_by_id("edit-columns-button").click()
                if (item.text == 'Package' or item.text == 'Package Version'):
                    pass
                else:
                    self.assertTrue(item.text, msg=("Fail :Incorrect muted column"))

                self.driver.find_element_by_id("edit-columns-button").click()

    def test_941(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.find_element_by_link_text_in_table('nav', 'Packages').click()
        column_list = self.get_table_column_text_by_column_number('builtpackagestable', 1)
        self.assertTrue(Utility.is_list_sequenced(column_list), msg=("list not in order"))
        self.find_element_by_link_text_in_table('builtpackagestable', 'Approx Size').click()
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="builtpackagestable"]/tbody/tr[1]/td[1]/a').click()
        time.sleep(3)
        self.driver.back()
        time.sleep(3)
        self.assertTrue(Utility.is_list_sequenced(column_list), msg=("list not in order"))

        option_ids = ['checkbox-recipe__layer_version__layer__name', 'checkbox-recipe__layer_version__branch', \
                      'checkbox-vcs_ref', 'checkbox-license', 'checkbox-recipe__name', 'checkbox-recipe__version']
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(3)
        for item in option_ids:
            if not self.driver.find_element_by_id(item).is_selected():
                self.driver.find_element_by_id(item).click()
                time.sleep(3)
        self.driver.find_element_by_id("edit-columns-button").click()
        column_head = ['Package', 'Approx Size', 'License', 'Recipe', 'Layer', 'Layer branch']
        column_number = 1
        for item in column_head:
            self.find_element_by_link_text_in_table('builtpackagestable', item).click()
            time.sleep(3)
            self.find_elements_by_link_text_in_table('builtpackagestable', item)
            if (column_number == 2 or column_number == 6):
                column_number = column_number + 1
            column_list_packages = self.get_table_column_text_by_column_number('builtpackagestable', column_number)
            self.assertTrue(Utility.is_list_sequenced(column_list_packages) or Utility.is_list_inverted(column_list_packages),
                            msg=("list not in order"))
            column_number = column_number + 1

        self.driver.find_element_by_id("edit-columns-button").click()
        for item in option_ids:
            if self.driver.find_element_by_id(item).is_selected():
                self.driver.find_element_by_id(item).click()
                time.sleep(3)
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(3)
        column_list = self.get_table_column_text_by_column_number('builtpackagestable', 1)
        self.assertTrue(Utility.is_list_sequenced(column_list) or Utility.is_list_inverted(column_list), msg=("list not in order"))

        self.find_element_by_link_text_in_table('builtpackagestable', 'Approx Size').click()
        self.driver.find_element_by_id("search-input-builtpackagestable").clear()
        time.sleep(3)
        self.driver.find_element_by_id("search-input-builtpackagestable").send_keys('lib')
        time.sleep(3)
        self.driver.find_element_by_id("search-submit-builtpackagestable").click()
        time.sleep(3)
        column_list = self.get_table_column_text_by_column_number('builtpackagestable', 3)
        self.assertTrue(Utility.is_list_sequenced(column_list), msg=("list not in order"))
        self.driver.find_element_by_id("search-input-builtpackagestable").clear()
        time.sleep(3)
        self.find_element_by_link_text_in_table('nav', 'core-image-minimal').click()
        column_list = self.get_table_column_text_by_column_number('installedpackagestable', 1)
        self.assertTrue(Utility.is_list_sequenced(column_list), msg=("list not in order"))
        self.find_element_by_link_text_in_table('installedpackagestable', 'Approx Size').click()
        time.sleep(3)
        self.driver.find_element_by_xpath("//*[@id='installedpackagestable']/tbody/tr[1]/td[1]/a").click()
        time.sleep(3)
        self.driver.back()
        column_list = self.get_table_column_text_by_column_number('installedpackagestable', 3)
        self.assertTrue(Utility.is_list_sequenced(column_list), msg=("list not in order"))

        option_ids1 = ['checkbox-size', 'checkbox-license', 'checkbox-dependencies', 'checkbox-reverse_dependencies',
                       'checkbox-recipe__name', \
                       'checkbox-recipe__version', 'checkbox-recipe__layer_version__layer__name',
                       'checkbox-recipe__layer_version__branch', 'checkbox-vcs_ref', 'checkbox-installed_size']
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(3)
        for item in option_ids1:
            if not self.driver.find_element_by_id(item).is_selected():
                self.driver.find_element_by_id(item).click()
                time.sleep(3)
        self.driver.find_element_by_id("edit-columns-button").click()
        column_head = ['Package', 'Approx Size', 'License', 'Recipe', 'Layer', 'Layer branch', 'Installed size']
        column_number = 1
        for item in column_head:
            if (
                    column_number == 2 or column_number == 5 or column_number == 6 or column_number == 8 or column_number == 11):
                column_number = column_number + 1
            self.find_element_by_link_text_in_table('installedpackagestable', item).click()
            time.sleep(3)
            self.find_elements_by_link_text_in_table('installedpackagestable', item)
            if (
                    column_number == 2 or column_number == 5 or column_number == 6 or column_number == 8 or column_number == 11):
                column_list_packages = self.get_table_column_text_by_column_number('installedpackagestable',
                                                                                   column_number)
                self.assertTrue(Utility.is_list_sequenced(column_list_packages) or Utility.is_list_inverted(column_list_packages),
                                msg=("list not in order"))
                column_number = column_number + 1

        self.driver.find_element_by_id("edit-columns-button").click()
        for item in option_ids1:
            if self.driver.find_element_by_id(item).is_selected():
                self.driver.find_element_by_id(item).click()
                time.sleep(3)
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(3)
        column_list = self.get_table_column_text_by_column_number('installedpackagestable', 1)
        self.assertTrue(Utility.is_list_sequenced(column_list) or Utility.is_list_inverted(column_list), msg=("list not in order"))

        self.find_element_by_link_text_in_table('installedpackagestable', 'Package').click()
        self.driver.find_element_by_id("search-input-installedpackagestable").clear()
        time.sleep(3)
        self.driver.find_element_by_id("search-input-installedpackagestable").send_keys('lib')
        time.sleep(3)
        self.driver.find_element_by_id("search-submit-installedpackagestable").click()
        time.sleep(3)
        column_list = self.get_table_column_text_by_column_number('installedpackagestable', 1)
        self.assertTrue(Utility.is_list_sequenced(column_list) or Utility.is_list_inverted(column_list), msg=("list not in order"))
        self.driver.find_element_by_id("search-input-installedpackagestable").clear()
        time.sleep(3)

    def test_942(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.driver.find_element_by_link_text("Packages").click()
        default_column_list = self.get_table_column_text_by_column_number('builtpackagestable', 1)
        self.assertTrue(Utility.is_list_sequenced(default_column_list), msg=("list not in sequence for default pacakge column"))
        head_list = self.get_table_head_text('builtpackagestable')
        self.driver.find_element_by_id("edit-columns-button").click()
        self.driver.find_element_by_id("checkbox-recipe__name").click()
        self.driver.find_element_by_id("edit-columns-button").click()
        new_head = self.get_table_head_text('builtpackagestable')
        self.assertTrue(new_head > head_list)
        self.driver.find_element_by_id("edit-columns-button").click()
        self.driver.find_element_by_id("checkbox-recipe__name").click()
        self.driver.find_element_by_id("edit-columns-button").click()
        new_head1 = self.get_table_head_text('builtpackagestable')
        self.assertTrue(new_head1 < new_head)

    def test_943(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        times = 2
        for i in range(0, times):
            self.driver.find_element_by_link_text("core-image-minimal").click()
            self.find_element_by_link_text_in_table('nav', 'Packages').click()
            column_list = self.get_table_column_text_by_column_number('builtpackagestable', 1)
            self.assertTrue(Utility.is_list_sequenced(column_list), msg=("list not in order"))
            head_list_before_seearch = self.get_table_head_text('builtpackagestable')
            self.assertTrue(self.driver.find_element_by_xpath(
                "//input[@id='search-input-builtpackagestable' and @placeholder='Search packages built']"),
                            msg=("plceholder string not present"))
            self.driver.find_element_by_id("search-input-builtpackagestable").clear()
            self.driver.find_element_by_id("search-input-builtpackagestable").click()
            self.driver.find_element_by_id("search-input-builtpackagestable").send_keys("bash")
            self.driver.find_element_by_id("search-submit-builtpackagestable").click()
            if (int(self.driver.find_element_by_xpath(
                    "//div[@class='page-header build-data']/h1/span[@class='table-count-builtpackagestable']").text )== 0):
                print("Pass:No packages found")
                time.sleep(5)
                self.driver.find_element_by_xpath("(//span[contains(@class,'remove-search-btn')])[1]").click()
                time.sleep(2)
            else:
                print("Pass:packages found")
                self.assertTrue(self.is_text_present("packages found"), msg=("no packages found text"))
                column_list = self.get_table_column_text_by_column_number('builtpackagestable', 1)
                self.assertTrue(Utility.is_list_sequenced(column_list), msg=("list not in order"))
                new_head_after_search = self.get_table_head_text('builtpackagestable')
                self.assertTrue(new_head_after_search == head_list_before_seearch)
                self.driver.find_element_by_id("search-input-builtpackagestable").click()
                self.driver.find_element_by_xpath("(//span[contains(@class,'remove-search-btn')])[2]").click()
            time.sleep(5)
            self.driver.find_element_by_id("edit-columns-button").click()
            time.sleep(2)
            self.driver.find_element_by_id("checkbox-size").click()
            self.driver.find_element_by_id("edit-columns-button").click()
            self.driver.find_element_by_id("search-input-builtpackagestable").clear()
            self.driver.find_element_by_id("search-input-builtpackagestable").send_keys("GPL")
            self.driver.find_element_by_id("search-submit-builtpackagestable").click()
            self.assertTrue(self.is_text_present("packages found"), msg=("no packages found text"))

            self.find_element_by_link_text_in_table('nav', 'core-image-minimal').click()
            column_list = self.get_table_column_text_by_column_number('installedpackagestable', 1)
            self.assertTrue(Utility.is_list_sequenced(column_list), msg=("list not in order"))
            self.assertTrue(self.driver.find_element_by_xpath(
                "//input[@id='search-input-installedpackagestable' and @placeholder='Search packages included']"),
                            msg=("plceholder string not present"))
            self.driver.find_element_by_id("search-input-installedpackagestable").clear()
            self.driver.find_element_by_id("search-input-installedpackagestable").send_keys("lib")
            self.driver.find_element_by_id("search-submit-installedpackagestable").click()
            self.assertTrue(self.is_text_present("packages found"), msg=("no packages found text"))
            self.driver.find_element_by_id("search-input-installedpackagestable").clear()
            self.driver.find_element_by_id("search-input-installedpackagestable").send_keys("GPL")
            self.driver.find_element_by_id("search-submit-installedpackagestable").click()
            self.assertTrue(self.is_text_present("packages found"), msg=("no packages found text"))

    def test_944(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.find_element_by_link_text_in_table('nav', 'Recipes').click()
        time.sleep(3)
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(3)
        self.driver.find_element_by_id("checkbox-layer_version__branch").click()
        self.driver.find_element_by_id("checkbox-commit").click()
        time.sleep(3)
        self.driver.find_element_by_id("edit-columns-button").click()
        otable_head_text = self.get_table_head_text('builtrecipestable')
        for item in ["Layer", "Layer branch", "Layer commit"]:
            self.failIf(item not in otable_head_text, msg=item + ' not in table head.')
        self.get_table_element("builtrecipestable", 1, 1).click()
        self.assertTrue(self.is_text_present(["Layer", "Layer branch", "Layer commit", "Recipe file"]), \
                        msg=("text not in web page"))
        if(self.get_table_column_text_by_column_number('builtrecipestable',9) == ''):
            print("Pass:Layer branch can be empty in recipie")
        self.driver.back()
        time.sleep(1)
        self.find_element_by_link_text_in_table('nav', 'Packages').click()
        time.sleep(3)
        self.driver.find_element_by_id("edit-columns-button").click()
        self.driver.find_element_by_id("checkbox-recipe__layer_version__layer__name").click()
        self.driver.find_element_by_id("checkbox-recipe__layer_version__branch").click()
        self.driver.find_element_by_id("checkbox-vcs_ref").click()
        time.sleep(3)
        self.driver.find_element_by_id("edit-columns-button").click()
        otable_head_text = self.get_table_head_text("builtpackagestable")
        for item in ["Layer", "Layer branch", "Layer commit"]:
            self.assertFalse(item not in otable_head_text, msg=("item %s should be in head row" % item))
        self.get_table_element("builtpackagestable", 1, 1).click()
        self.assertTrue(self.is_text_present(["Layer", "Layer branch", "Layer commit"]), \
                        msg=("text not in web page"))
        if (self.get_table_column_text_by_column_number('builtpackagestable', 8) == ''):
            print("Pass:Layer branch can be empty in recipie")
        self.driver.back()
        time.sleep(3)
        self.find_element_by_link_text_in_table('nav', 'core-image-minimal').click()
        time.sleep(2)
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(2)
        self.driver.find_element_by_id("checkbox-recipe__layer_version__layer__name").click()
        self.driver.find_element_by_id("checkbox-recipe__layer_version__branch").click()
        self.driver.find_element_by_id("checkbox-vcs_ref").click()
        self.driver.find_element_by_id("edit-columns-button").click()
        otable_head_text = self.get_table_head_text("installedpackagestable")
        for item in ["Layer", "Layer branch", "Layer commit"]:
            self.assertFalse(item not in otable_head_text, msg=("item %s should be in head row" % item))
        time.sleep(3)
        self.get_table_element("installedpackagestable", 1, 1).click()
        time.sleep(3)
        self.assertTrue(self.is_text_present(["Layer", "Layer branch", "Layer commit"]), \
                        msg=("text not in web page"))
        self.driver.back()
        self.driver.find_element_by_link_text("Configuration").click()
        otable_head_text = self.get_table_head_text()
        self.assertTrue(self.is_text_present(["Layer", "Layer branch", "Layer commit"]), \
                        msg=("text not in web page"))
        time.sleep(3)
        self.driver.back()
        time.sleep(3)
        self.assertTrue(self.is_text_present("Layers"), msg=("text not in web page"))

    def test_945(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        time.sleep(3)
        for item in ["Packages", "Recipes", "Tasks"]:
            self.driver.get(self.base_url)
            self.driver.find_element_by_link_text("core-image-minimal").click()
            self.driver.find_element_by_link_text(item).click()
            if (item == "Packages"):
                item_id = 'builtpackagestable'
                self.driver.find_element_by_xpath("//*[@id='" + item_id + "']/tbody/tr[1]/td[1]/a").click()
            elif (item == "Recipes"):
                item_id = 'builtrecipestable'
                self.driver.find_element_by_xpath("//*[@id='" + item_id + "']/tbody/tr[1]/td[1]/a").click()
            elif (item == "Tasks"):
                item_id = 'buildtaskstable'
                self.driver.find_element_by_xpath("//*[@id='" + item_id + "']/tbody/tr[1]/td[2]/a").click()
            time.sleep(3)
            self.driver.find_element_by_xpath("//*[@id='breadcrumb']/li[4]/a").click()
            time.sleep(3)
            edit_Show_Rows = Select(self.driver.find_element_by_xpath(
                "//*[@id='table-chrome-collapse-" + item_id + "']/form[2]/div/select "))
            selected_number_rows = ['10', '25', '50', '100', '150']
            for item in selected_number_rows:
                edit_Show_Rows.select_by_value(item)
                self.assertTrue(edit_Show_Rows, msg="rows displayed is not as per selection")
                time.sleep(3)

            maxium_page_number = len(self.driver.find_elements_by_xpath("//*[@class='pagination']/li"))
            if (maxium_page_number < 5 or maxium_page_number == 5):
                pass
            else:
                print("Error: Maximum number of pages navigation button is  not correct")
            for i in range(2, maxium_page_number + 1):
                self.driver.find_element_by_xpath("(//*[@class='pagination']/li/a[@href='#'])[%d]" % i).click()
                self.driver.find_element_by_xpath("(//*[@class='pagination']/li/a[@href='#'])[%d]" % (i - 1)).click()
                time.sleep(5)

    def test_946(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.driver.find_element_by_link_text("Configuration").click()
        check_list = ["Summary", "BitBake variables"]
        for item in check_list:
            if not self.is_element_present(how=By.LINK_TEXT, what=item):
                self.log.error("%s not found" % item)
        if not self.is_text_present(['Layers', 'Layer', 'Layer branch', 'Layer commit']):
            self.log.error("text not found")
        self.driver.find_element_by_link_text("BitBake variables").click()
        if not self.is_text_present(['Variable', 'Value', 'Set in file', 'Description']):
            self.log.error("text not found")
        temp_element = self.find_element_by_text_in_table('otable', "Set in file")
        temp_element.find_element_by_xpath(
            r"//div[@class='btn-group pull-right']/a[@class='btn btn-xs  ']/span[@class='glyphicon glyphicon-filter filtered']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("(//input[@name='filter'])[2]").click()
        btns = self.driver.find_elements_by_css_selector("button.btn.btn-primary")
        for btn in btns:
            try:
                btn.click()
                break
            except:
                pass
        time.sleep(1)
        self.save_screenshot(screenshot_type='selenium', append_name='step6')
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(1)
        self.save_screenshot(screenshot_type='selenium', append_name='step7')
        self.driver.find_element_by_id("edit-columns-button").click()
        elements = self.driver.find_elements_by_xpath("//*[@id='editcol']/li/div/label[@class='muted']")
        if (len(elements) == 2):
            pass
        else:
            print("Error ! Total default muted column is not correct")
        self.driver.find_element_by_xpath("//*[@id='otable']/tbody/tr[1]/td[1]/a").click()
        time.sleep(1)
        element = self.driver.switch_to.active_element
        check_list = ['Order', 'Configuration file', 'Operation']
        for item in check_list:
            if item not in element.text:
                self.log.error("%s not found" % item)
        element.find_element_by_class_name("close").click()
        time.sleep(3)
        self.driver.find_element_by_xpath("//a[contains(@href,'yoctoproject.org')]").click()
        time.sleep(3)
        self.save_screenshot(screenshot_type='native', append_name='step10')

    def test_947(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.find_element_by_link_text_in_table('nav', 'Configuration').click()
        self.driver.find_element_by_link_text("BitBake variables").click()

        def xpath_option(column_name):
            return self.shortest_xpath('id', 'navTab') + self.shortest_xpath('id', 'editcol') \
                   + self.shortest_xpath('id', column_name)

        self.driver.find_element_by_id('edit-columns-button').click()
        self.driver.find_element_by_xpath(xpath_option('description')).click()
        self.driver.find_element_by_xpath(xpath_option('file')).click()
        self.driver.find_element_by_id('edit-columns-button').click()
        check_list = ['Description', 'Set in file']
        head_list = self.get_table_head_text('otable')
        for item in check_list:
            self.assertFalse(item in head_list, msg=("item %s should not be in head row" % item))
        self.driver.find_element_by_id('edit-columns-button').click()
        self.driver.find_element_by_xpath(xpath_option('description')).click()
        self.driver.find_element_by_xpath(xpath_option('file')).click()
        self.driver.find_element_by_id('edit-columns-button').click()
        head_list = self.get_table_head_text('otable')
        for item in check_list:
            self.assertTrue(item in head_list, msg=("item %s not in head row" % item))

    def test_948(self):
        Comparable_string = "You can only apply one filter to the table. This filter will override the current filter."
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.find_element_by_link_text_in_table('nav', 'Configuration').click()
        self.driver.find_element_by_link_text("BitBake variables").click()
        self.driver.find_element_by_xpath(
            "//th[@class='span4 description']//span[@class='glyphicon glyphicon-filter filtered']")
        self.driver.find_element_by_xpath("//th[@class=' file']//span[@class='glyphicon glyphicon-filter filtered']")
        self.driver.find_element_by_xpath(
            "//th[@class=' file']//span[@class='glyphicon glyphicon-filter filtered']").click()
        time.sleep(5)
        self.driver.find_element_by_xpath(
            "//*[@id='filter_vhistory__file_name']/div/div/form/div[2]/div[3]/label/input").click()
        time.sleep(3)
        self.driver.find_element_by_xpath(
            "//*[@id='filter_vhistory__file_name']/div/div/form/div[3]/div/div[1]/button").click()
        time.sleep(5)
        self.driver.find_element_by_xpath(
            "//th[@class='span4 description']//span[@class='glyphicon glyphicon-filter filtered']").click()
        time.sleep(3)
        if (Comparable_string == self.driver.find_element_by_xpath(
                "//*[@id='filter_description']/div/div/form/div[3]/div/div[2]/p").text):
            pass
        else:
            print("Error: string not found")
        self.driver.find_element_by_xpath("//*[@id='filter_description']/div/div/form/div[1]/button").click()
        time.sleep(5)

        self.driver.find_element_by_xpath(
            "//th[@class=' file']//span[@class='glyphicon glyphicon-filter filtered']").click()
        time.sleep(5)
        self.driver.find_element_by_xpath(
            "//*[@id='filter_vhistory__file_name']/div/div/form/div[2]/div[3]/label/input").click()
        time.sleep(3)
        self.driver.find_element_by_xpath(
            "//*[@id='filter_vhistory__file_name']/div/div/form/div[3]/div/div[1]/button").click()
        time.sleep(5)
        self.driver.find_element_by_id("search").clear()
        time.sleep(5)
        self.driver.find_element_by_id("search").send_keys("BB")
        time.sleep(5)
        self.driver.find_element_by_id("search-button").click()
        time.sleep(5)
        self.driver.find_element_by_xpath(
            "//th[@class=' file']//span[@class='glyphicon glyphicon-filter filtered']").click()
        time.sleep(5)
        radio_button_selected = self.driver.find_element_by_xpath(
            "//*[@id='filter_vhistory__file_name']/div/div/form/div[2]/div[1]/label/input")
        if (radio_button_selected.is_selected()):
            pass
        else:
            print("Fail:Filter not cleared after search")
        self.driver.find_element_by_xpath("//*[@id='filter_vhistory__file_name']/div/div/form/div[1]/button").click()
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id='searchform']/div/div/a/span").click()
        time.sleep(5)
        self.driver.find_element_by_id("search").clear()
        time.sleep(20)
        self.driver.find_element_by_id("search").send_keys("busybox")
        time.sleep(20)
        self.driver.find_element_by_id("search-button").click()
        time.sleep(30)
        self.driver.find_element_by_xpath(
            "//th[@class=' file']//span[@class='glyphicon glyphicon-filter filtered']").click()
        time.sleep(5)
        self.driver.find_element_by_xpath(
            "//*[@id='filter_vhistory__file_name']/div/div/form/div[2]/div[5]/label/input").click()
        time.sleep(3)
        self.driver.find_element_by_xpath(
            "//*[@id='filter_vhistory__file_name']/div/div/form/div[3]/div/div[1]/button").click()
        time.sleep(10)
        self.driver.find_element_by_xpath(
            "//th[@class=' file']//span[@class='glyphicon glyphicon-filter filtered']").click()
        time.sleep(5)
        radio_button_selected = self.driver.find_element_by_xpath(
            "//*[@id='filter_vhistory__file_name']/div/div/form/div[2]/div[5]/label/input")
        if (radio_button_selected.is_selected()):
            pass
        else:
            print("Fail:Filter not cleared")
        self.driver.find_element_by_xpath("//*[@id='filter_vhistory__file_name']/div/div/form/div[1]/button")

    def test_949(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.find_element_by_link_text_in_table('nav', 'core-image-minimal').click()
        try:
            self.driver.find_element_by_partial_link_text("Packages included")
            self.driver.find_element_by_partial_link_text("Directory structure")
        except Exception as e:
            self.log.error(e)
            self.assertFalse(True)

        package_included = (self.driver.find_element_by_xpath("//*[@id='navTab']/ul/li[1]/a").text)
        self.assertTrue(self.is_text_present(package_included),
                        msg=("total number of packages and total size not found in Package included"))
        head_list = self.get_table_head_text('installedpackagestable')
        for item in ['Package', 'Package Version']:
            self.assertTrue(item in head_list, msg=("item %s not in head row" % item))
        self.driver.find_element_by_id("edit-columns-button").click()
        default_list = self.driver.find_elements_by_xpath("// *[@checked ='checked']")
        if (len(default_list) == 4):
            pass
        else:
            print("Fail: Deafault column numbernot correct")
        self.driver.find_element_by_id("edit-columns-button").click()
        self.driver.find_element_by_partial_link_text("Packages included").click()
        option_ids = ['checkbox-size', 'checkbox-license', 'checkbox-dependencies', 'checkbox-reverse_dependencies',
                      'checkbox-recipe__name', 'checkbox-recipe__version', \
                      'checkbox-recipe__layer_version__layer__name', 'checkbox-recipe__layer_version__branch',
                      'checkbox-vcs_ref', 'checkbox-vcs_ref']
        self.driver.find_element_by_id("edit-columns-button").click()
        time.sleep(3)
        for item in option_ids:
            if not self.driver.find_element_by_id(item).is_selected():
                self.driver.find_element_by_id(item).click()
                time.sleep(3)
        self.driver.find_element_by_id("edit-columns-button").click()

        self.driver.find_element_by_partial_link_text("Directory structure").click()
        head_list = self.get_table_head_text('dirtable')
        for item in ['Directory / File', 'Symbolic link to', 'Source package', 'Size', 'Permissions', 'Owner', 'Group']:
            self.assertTrue(item in head_list, msg=("%s not found in Directory structure table head" % item))
        self.get_table_element("dirtable", 1, 1).click()
        self.assertTrue(self.is_text_present(
            ["Directory / File", "Symbolic link to", "Source package", "Size", "Permissions", "Owner", "Group"]), \
                        msg=("text not in web page"))

    def test_950(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        check_list = ['Configuration', 'Tasks', 'Recipes', 'Packages', 'Time', 'CPU usage', 'Disk I/O']
        has_successful_build = 1
        has_failed_build = 1
        try:
            pass_icon = self.driver.find_element_by_xpath("//*[@class='icon-ok-sign success']")
        except Exception:
            self.log.info("checking for successful build")
            has_successful_build = 0
            pass
        if has_successful_build:
            pass_icon.click()
            time.sleep(1)
            self.save_screenshot(screenshot_type='selenium', append_name='step3_1')
            for item in check_list:
                try:
                    self.find_element_by_link_text_in_table('nav', item)
                except Exception:
                    self.assertFalse(True, msg=("link  %s cannot be found in the page" % item))
            check_list_2 = ['Packages included', 'Total package size', \
                            'License manifest', 'Image files']
            self.assertTrue(self.is_text_present(check_list_2), msg=("text not in web page"))
            self.driver.back()
        try:
            fail_icon = self.driver.find_element_by_xpath("//*[@class='icon-minus-sign error']")
        except Exception:
            has_failed_build = 0
            self.log.info("checking if build exists")
            pass
        if has_failed_build:
            fail_icon.click()
            time.sleep(1)
            self.save_screenshot(screenshot_type='selenium', append_name='step3_2')
            for item in check_list:
                try:
                    self.find_element_by_link_text_in_table('nav', item)
                except Exception:
                    self.assertFalse(True, msg=("link  %s cannot be found in the page" % item))
            check_list_3 = ['Machine', 'Distro', 'Layers', 'Total number of tasks', 'Tasks executed', \
                            'Tasks not executed', 'Reuse', 'Recipes built', 'Packages built']
            self.assertTrue(self.is_text_present(check_list_3), msg=("text not in web page"))
            self.driver.back()

    def test_951(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        element_latest = self.driver.find_element_by_xpath("//*[@id='latest-builds']/div/div[2]/div[2]/div[3]/a")
        str_warning_latest = element_latest.text
        if (str_warning_latest.find("warnings") and str_warning_latest.split()[1] != ''):
            pass
        else:
            print("Error :warnings are not present in latest build")
        element_latest.click()
        self.driver.back()
        element_all_build = self.driver.find_element_by_xpath("//*[@id='allbuildstable']/tbody/tr/td[8]/a")
        str_warning_all = element_all_build.text
        if (str_warning_all.find("warnings") and str_warning_all.split()[1] != ''):
            pass
        else:
            print("Error :warnings are not present in All build")
        element_all_build.click()
        self.driver.back()
        has_successful_build = 1
        has_failed_build = 1
        try:
            fail_icon = self.driver.find_element_by_xpath("//*[@class='icon-minus-sign error']")
        except Exception:
            has_failed_build = 0
            self.log.info("no failed build exists")
            pass
        if has_failed_build:
            self.driver.find_element_by_partial_link_text("error").click()
            self.driver.back()
        time.sleep(1)
        self.save_screenshot(screenshot_type='selenium', append_name='step4')

    def test_955(self):
        self.case_no = self.get_case_number()
        self.log.info(' CASE %s log: ' % str(self.case_no))
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.find_element_by_link_text("core-image-minimal").click()
        self.driver.find_elements_by_xpath("//*[@id='breadcrumb']/li")
        self.driver.find_elements_by_xpath("//*[@id='build-menu']/li")
        self.assertFalse(self.driver.find_element_by_xpath(
            "//div[@class='page-header build-data']").text != 'core-image-minimal qemux86',
                         msg="Build Image is not present")

        self.driver.find_element_by_xpath("//h2[@data-heading='build-artifacts']")
        self.driver.find_element_by_xpath("//h2[@data-role='build-summary-heading']")
        self.assertFalse(self.driver.find_element_by_xpath("(//span/strong)[3]").text != 'Completed',
                         msg="Completed is not present")
        packages_link = self.driver.find_element_by_xpath(
            "//div[@class='well well-transparent dashboard-section']/h3/a")
        self.assertFalse(packages_link.get_attribute("href") == '', msg="Link not assocaited with pacakge")
        self.assertFalse(
            self.driver.find_element_by_xpath("((//dl[@class='dl-horizontal'])/dt)[1]").text != 'Packages included')
        package_included_link = self.driver.find_element_by_xpath("((//dl[@class='dl-horizontal'])/dd)[1]/a")
        self.assertFalse(package_included_link.get_attribute("href") == '', msg="Link not assocaited with pacakge")
        self.assertFalse(
            int(self.driver.find_element_by_xpath("((//dl[@class='dl-horizontal'])/dd)[1]/a/span").text) == 0,
            msg='Packages included number is zero')
        self.assertFalse(
            self.driver.find_element_by_xpath("((//dl[@class='dl-horizontal'])/dt)[2]").text != 'Total package size',
            msg='Total package size string not present')
        self.assertFalse((self.driver.find_element_by_xpath("((//dl[@class='dl-horizontal'])/dd)[2]").text) == '',
                         msg='Total package size is zero')
        self.assertFalse(self.driver.find_element_by_xpath("(//dl[@class='dl-horizontal'])[2]/dt").text != 'Manifests',
                         msg='Manifests string not present')
        license_manifest_link = self.driver.find_element_by_xpath("((//dl[@class='dl-horizontal'])[2]//dd)[1]/a")
        self.assertFalse(license_manifest_link.get_attribute("href") == '',
                         msg="Link not assocaited with license_manifest")
        package_manifest_link = self.driver.find_element_by_xpath("((//dl[@class='dl-horizontal'])[2]//dd)[2]/a")
        self.assertFalse(package_manifest_link.get_attribute("href") == '',
                         msg="Link not assocaited with package_manifest")
        self.assertFalse(
            self.driver.find_element_by_xpath("((//dl[@class='dl-horizontal'])[3]/dt)[1]").text != 'Image files',
            msg='Image file text not present')
        length = len(self.driver.find_elements_by_xpath("((//dl[@class='dl-horizontal'])[3]/dd)[1]//ul/li"))
        for i in range(1, length + 1):
            self.assertFalse(self.driver.find_element_by_xpath(
                "(((//dl[@class='dl-horizontal'])[3]/dd)[1]//ul/li)[%d]" % i).text == '')

        Configuration_link = self.driver.find_element_by_xpath("(//div[@class='well well-transparent']/h3)[1]/a")
        self.assertFalse(Configuration_link.text != 'Configuration', msg='Configuration text not present')
        self.assertFalse(Configuration_link.get_attribute("href") == '', msg='Link not assocaites with configuration')

        self.driver.find_element_by_xpath(
            "//div[@class='col-md-4 dashboard-section']/div[@class='well well-transparent']/dl/dt")

        self.assertFalse(self.driver.find_element_by_xpath(
            "(//div[@class='col-md-4 dashboard-section']/div[@class='well well-transparent']/dl/dt)[1]").text != 'Machine',
                         msg='machine text not found')
        self.assertFalse(self.driver.find_element_by_xpath(
            "(//div[@class='col-md-4 dashboard-section']/div[@class='well well-transparent']/dl/dt)[2]").text != 'Distro',
                         msg='distro text not found')
        self.assertFalse(self.driver.find_element_by_xpath(
            "(//div[@class='col-md-4 dashboard-section']/div[@class='well well-transparent']/dl/dt)[3]").text != 'Layers',
                         msg='Layers text not found')
        self.assertFalse(self.driver.find_element_by_xpath(
            "(//div[@class='col-md-4 dashboard-section']/div[@class='well well-transparent']/dl/dd)[1]").text != 'qemux86',
                         msg='qemux86 text not found')
        self.assertFalse(self.driver.find_element_by_xpath(
            "(//div[@class='col-md-4 dashboard-section']/div[@class='well well-transparent']/dl/dd)[2]").text != 'poky',
                         msg='poky text not found')
        self.assertFalse(self.driver.find_element_by_xpath(
            "((//div[@class='col-md-4 dashboard-section']/div[@class='well well-transparent']/dl/dd)[3]/ul/li)[1]").text != 'meta-poky',
                         msg='meta-poky text not found')
        self.assertFalse(self.driver.find_element_by_xpath(
            "((//div[@class='col-md-4 dashboard-section']/div[@class='well well-transparent']/dl/dd)[3]/ul/li)[2]").text != 'meta-yocto-bsp',
                         msg='meta-yocto-bsp string not found')
        self.assertFalse(self.driver.find_element_by_xpath(
            "((//div[@class='col-md-4 dashboard-section']/div[@class='well well-transparent']/dl/dd)[3]/ul/li)[3]").text != 'openembedded-core',
                         msg='openembedded-core string not found')

        tasks_link = self.driver.find_element_by_xpath("(//div[@class='well well-transparent']/h3)[2]/a")
        self.assertFalse(tasks_link.text != 'Tasks', msg="Task text not found")
        self.assertFalse(tasks_link.get_attribute("href") == '', msg='Link not assocaites with tasks')
        self.assertFalse(self.driver.find_element_by_xpath(
            "((//div[@class='well well-transparent'])[2]/dl/dt)[1]").text != 'Total number of tasks',
                         msg='Text not available for tasks')

        No_tasks_link = self.driver.find_element_by_xpath("((//div[@class='well well-transparent'])[2]/dl/dd)[1]/a")
        self.assertFalse(int(No_tasks_link.text) == 0, msg='No of toatl task is 0')
        self.assertFalse(No_tasks_link.get_attribute("href") == '',
                         msg='Link not assocaited with total number of tasks')

        self.assertFalse(self.driver.find_element_by_xpath(
            "((//div[@class='well well-transparent'])[2]/dl/dt)[2]").text != 'Tasks executed',
                         msg='Tasks executed text not found')

        Executed_tasks_link = self.driver.find_element_by_xpath(
            "((//div[@class='well well-transparent'])[2]/dl/dd)[2]/a")
        self.assertFalse(int(Executed_tasks_link.text) == 0, msg='Total number of Tasks executed is zero')
        self.assertFalse(Executed_tasks_link.get_attribute("href") == '', msg='Link not assocaited with Executed tasks')
        self.assertFalse(self.driver.find_element_by_xpath(
            "((//div[@class='well well-transparent'])[2]/dl/dt)[3]").text != 'Tasks not executed')

        Not_Executed_tasks_link = self.driver.find_element_by_xpath(
            "((//div[@class='well well-transparent'])[2]/dl/dd)[3]/a")
        self.assertFalse(int(Not_Executed_tasks_link.text) == 0, msg='Total number of  not executed tasks is zero')
        self.assertFalse(Not_Executed_tasks_link.get_attribute("href") == '',
                         msg='Link not assocaited with not Executed tasks')
        self.assertFalse(
            self.driver.find_element_by_xpath("((//div[@class='well well-transparent'])[2]/dl/dt)[4]").text != 'Reuse',
            msg='Reuse ttext not present')

        Reuse_tasks_link = self.driver.find_element_by_xpath("((//div[@class='well well-transparent'])[2]/dl/dd)[3]/a")
        self.assertFalse(int(Reuse_tasks_link.text) == 0, msg='Resue tasks are showing zero')

        self.assertFalse(
            (int(No_tasks_link.text) != (int(Executed_tasks_link.text) + int(Not_Executed_tasks_link.text))),
            msg='Total Task calucaltion not correct')
        Recipies_link = self.driver.find_element_by_xpath("((//div[@class='well well-transparent']/h3)[3]/a)[1]")
        self.assertFalse(Recipies_link.text != 'Recipes', msg='Recipes text not found')
        self.assertFalse(Recipies_link.get_attribute("href") == '', msg='Link not associated with Recipes section')
        Packages_link = self.driver.find_element_by_xpath("((//div[@class='well well-transparent']/h3)[3]/a)[2]")
        self.assertFalse(Packages_link.text != 'Packages', msg='Packages text not found')
        self.assertFalse(Packages_link.get_attribute("href") == '', msg='Link not associated with packages section')
        self.assertFalse(self.driver.find_element_by_xpath(
            "((//div[@class='well well-transparent']/dl)[3]/dt)[1]").text != 'Recipes built',
                         msg='Recipie built text not found')
        Recipie_built_link = self.driver.find_element_by_xpath(
            "((//div[@class='well well-transparent']/dl)[3]/dd)[1]/a")
        self.assertFalse(int(Recipie_built_link.text) == 0, msg="Total packages number is showing zero")
        self.assertFalse(Recipie_built_link.get_attribute("href") == '',
                         msg='Link not associated with built recipie section')
        url_Recipie_built_link = Recipie_built_link.get_attribute("href")
        self.assertFalse(self.driver.find_element_by_xpath(
            "((//div[@class='well well-transparent']/dl)[3]/dt)[2]").text != 'Packages built',
                         msg='Packages built text not found')
        Package_built_link = self.driver.find_element_by_xpath(
            "((//div[@class='well well-transparent']/dl)[3]/dd)[2]/a")
        self.assertFalse(int(Package_built_link.text) == 0, msg="Total packages number is showing zero")
        self.assertFalse(Package_built_link.get_attribute("href") == '',
                         msg='Link not associated with built packages section')
