import unittest
from toaster_driver import *
import toaster_pages


class BaseToasterTestCase(unittest.TestCase):

    def setUp(self):
        self.verificationErrors = []
        self.log = LOG
        ToasterTestsConfig.set_case_no(self._testMethodName)
        self.log.info(const.LOG_TESTCASE_START_HEADER.replace("$NR", str(ToasterTestsConfig.case_no)))
        self.log.info("setting up test: %s" % str(ToasterTestsConfig.case_no))
        self.toaster_driver = ToasterDriver()
        self.screenshooter = ScreenShooter(self.toaster_driver.driver)

    def tearDown(self):
        self.log.info('ending test: %s' % str(ToasterTestsConfig.case_no))
        self.log_before_tear_down()
        self.toaster_driver.clean_up()
        self.assertEqual([], self.verificationErrors)

    def log_before_tear_down(self):
        result = self._resultForDoCleanups
        if not result.wasSuccessful():
            self.screenshooter.take_screenshot(screenshot_type='selenium', append_name='tearDown')

    def log_test_step_number(self, *step_numbers):
        if len(step_numbers) == 1:
            self.log.info('executing test step: %s' % step_numbers[0])
        elif len(step_numbers) > 1:
            self.log.info('executing test steps: %s' % str(step_numbers).strip('[]()'))


class ToasterTests(BaseToasterTestCase):
        ##############
        #  CASE 901  #
        ##############
    def test_901(self):
        # step 1
        self.log_test_step_number(1)
        self.toaster_driver.go_to_base_url()
        home_page = toaster_pages.HomePage(self.toaster_driver.driver)

        # steps 2-3
        self.log_test_step_number(2, 3)
        home_page = home_page.select_all_builds()

        # steps 4-6
        self.log_test_step_number(4, 5, 6)
        home_page.display_all_build_info_columns()

        for column_name in home_page.column_name_class_map:
            self.log.info("testing sorting on the %s column" % column_name)
            home_page.order_builds_by_column(column_name)
            first_values = home_page.get_build_column_values(column_name)
            home_page.order_builds_by_column(column_name)
            second_values = home_page.get_build_column_values(column_name)
            self.assertTrue("first and second sorts must de ascending or descending",
                            ToasterValueList.lists_have_oposite_monotonicity(first_values, second_values))

        ##############
        #  CASE 902  #
        ##############
    def test_902(self):
        # step 1
        self.log_test_step_number(1)
        self.toaster_driver.go_to_base_url()
        home_page = toaster_pages.HomePage(self.toaster_driver.driver)

        # steps 2
        self.log_test_step_number(2)
        home_page = home_page.select_all_builds()

        # step 3-5
        self.log_test_step_number(3, 4, 5)
        build_keywords = ["minimal", "sato"]
        for search_word in build_keywords:
            reference_recipe_values = home_page.get_build_column_values(home_page.recipe_column_name)
            home_page.search_for_build(search_word)
            recipe_column_values = home_page.get_build_column_values(home_page.recipe_column_name)
            # if nothing found, we still count it as "pass"
            if recipe_column_values:
                for value in recipe_column_values:
                    self.failUnless(value.find(search_word))
            home_page.clear_search_results()
            clear_search_recipe_values = home_page.get_build_column_values(home_page.recipe_column_name)
            self.failUnless(clear_search_recipe_values == reference_recipe_values)

        ##############
        #  CASE 903  #
        ##############
    def test_903(self):
        # step 1
        self.log_test_step_number(1)
        self.toaster_driver.go_to_base_url()
        home_page = toaster_pages.HomePage(self.toaster_driver.driver)

        # steps 2-3
        self.log_test_step_number(2, 3)
        home_page = home_page.select_all_builds()

        # steps 4
        self.log_test_step_number(4)
        home_page.display_started_on_column()
        home_page.check_filters_are_displayed()

        # step 5-7
        self.log_test_step_number(5, 6, 7)
        for filter_index in range(len(home_page.get_filter_filter_form_mapping())):
            build_filter = home_page.get_filter_filter_form_mapping()[filter_index]
            self.log.info("testing filter %s" % build_filter.name)
            home_page.filter_builds(build_filter.column_filter, build_filter.filter_form,
                                    home_page.second_filter_option_xpath)
            time.sleep(2)
            self.screenshooter.take_screenshot(screenshot_type='selenium', append_name='step5_%s' % build_filter.name)
            ToasterDriver.browser_delay()
            home_page.search_for_build("core-image")
            self.screenshooter.take_screenshot(screenshot_type='selenium', append_name='step6_%s' % build_filter.name)
            home_page = home_page.clear_search_results()

        ##############
        #  CASE 904  #
        ##############
    def test_904(self):
        # steps 1-3
        self.log_test_step_number(1, 2, 3)
        self.toaster_driver.go_to_base_url()
        home_page = toaster_pages.HomePage(self.toaster_driver.driver)
        build_page = home_page.select_core_image_minimal_build()
        tasks_page = build_page.select_tasks_option()

        # steps 4-7
        self.log_test_step_number(4, 5, 6, 7)
        self.failUnless(tasks_page.get_nr_of_rows_in_select() ==
                        tasks_page.table.get_table_row_nr(tasks_page.otable_id))
        tasks_page.search_for_task("busybox")
        self.toaster_driver.browser_delay()
        self.screenshooter.take_screenshot(screenshot_type='selenium', append_name='step5')
        tasks_page.clear_search_results()
        # Save screen here
        self.screenshooter.take_screenshot(screenshot_type='selenium', append_name='step5_2')
        tasks_page.display_all_build_info_columns()
        for column_name in tasks_page.column_name_class_map:
            self.log.info("testing sorting on column %s" % column_name)
            tasks_page.order_tasks_by_column(column_name)
            first_values = tasks_page.get_tasks_column_values(column_name)
            tasks_page.order_tasks_by_column(column_name)
            second_values = tasks_page.get_tasks_column_values(column_name)
            self.assertTrue("first and second sorts must de ascending or descending",
                            ToasterValueList.lists_have_oposite_monotonicity(first_values, second_values))

        # steps 8-10
        self.log_test_step_number(8, 9, 10)
        for filter_index in range(len(tasks_page.get_filter_filter_form_mapping())):
            tasks_filter = tasks_page.get_filter_filter_form_mapping()[filter_index]
            self.log.info("testing filter %s" % tasks_filter.name)
            tasks_page.ensure_column_displayed(tasks_filter.name)
            nr_of_filter_options = tasks_page.get_nr_of_filter_options(tasks_filter.column_filter)
            for option_nr in range(nr_of_filter_options):
                # Refresh filter element to avoid StaleElementException
                tasks_filter = tasks_page.get_filter_filter_form_mapping()[filter_index]
                tasks_page.filter_tasks(tasks_filter.column_filter, tasks_filter.filter_form,
                                        tasks_page.get_nth_filter_option_xpath(option_nr + 1))
                self.screenshooter.take_screenshot(screenshot_type='selenium',
                                                   append_name='step8_%s' % tasks_filter.name)
                tasks_page.handle_no_results_page()
                ToasterDriver.browser_delay()

        # step 11
        self.log_test_step_number(11)
        for column_name in tasks_page.columns_with_link_items:
            self.log.info("testing items in table column %s" % column_name)
            tasks_page.ensure_column_displayed(column_name)
            try:
                tasks_page.table.select_table_cell_by_class(tasks_page.columns_with_link_items[column_name])
            except Exception as e:
                self.log.error("could not find item of class %s in column %s"
                               % (tasks_page.columns_with_link_items[column_name], column_name))
            self.screenshooter.take_screenshot(screenshot_type='selenium', append_name='step11')
            time.sleep(2)
            self.toaster_driver.driver.back()

        # steps 12-14
        self.log_test_step_number(12, 13, 14)
        for navigator in tasks_page.get_performance_page_navigators():
            perf_page = navigator()
            self.log.info("testing performance page %s" % perf_page.page_type)
            table_header_values = perf_page.table.get_table_head_text(perf_page.otable_id)
            self.log.info("table on current page has header: %s" % str(table_header_values))
            for value in perf_page.check_head_list:
                self.failUnless(value in table_header_values)
            time.sleep(2)
            main_column_values = perf_page.table.get_toaster_table_column_values_by_class(perf_page.column_class)
            self.failUnless(ToasterValueList.is_list_descending(main_column_values))
            for column_id in perf_page.check_column_list:
                perf_page.add_single_column_to_display_by_id(column_id)
            self.screenshooter.take_screenshot(screenshot_type='selenium', append_name='step11_%s' % perf_page.page_type)

        ##############
        #  CASE 906  #
        ##############
    def test_906(self):
        # steps 1-3
        self.log_test_step_number(1, 2, 3)
        self.toaster_driver.go_to_base_url()
        home_page = toaster_pages.HomePage(self.toaster_driver.driver)
        build_page = home_page.select_core_image_minimal_build()
        packages_page = build_page.select_packages_option()
        packages_page.search_for_package(packages_page.test_package_name)
        package_view_page = packages_page.select_package(packages_page.test_package_name)

        # step 4
        self.log_test_step_number(4)
        self.log.info("there are %s breadcrumbs on the current page" % package_view_page.get_nr_of_breadcrumbs())
        self.failUnless(package_view_page.get_nr_of_breadcrumbs() == 4)
        self.failUnless(package_view_page.check_first_n_crumbs_links(len(package_view_page.breadcrumbs_ref_text),
                                                                 package_view_page.breadcrumbs_ref_text))
        self.failUnless(package_view_page.check_last_breadcrumb_contains_string(packages_page.test_package_name))

        # step 5
        self.log_test_step_number(5)
        self.screenshooter.take_screenshot(screenshot_type='selenium', append_name='step5')
        self.failUnless(package_view_page.is_element_present(By.XPATH, package_view_page.right_info_box_xpath))
        self.failIf(package_view_page.is_element_present(By.ID, package_view_page.left_nav_box_id))

        # step 6
        self.log_test_step_number(6)
        package_view_page.check_mandatory_page_elements()

        # steps 7
        self.log_test_step_number(7)
        package_view_page.open_generated_files_tab()
        header_text = package_view_page.table.get_table_head_text(package_view_page.otable_id)
        for name in package_view_page.generated_files_table_column_names:
            self.failUnless(name in header_text)
        path_values = package_view_page.table.get_toaster_table_column_values_by_class(package_view_page.path_values_class)
        self.failUnless(ToasterValueList.is_list_ascending(path_values))

        #step 8
        self.log_test_step_number(8)
        package_view_page.open_runtime_dependencies_tab()
        header_text = package_view_page.table.get_table_head_text(package_view_page.runtime_dependencies_table_id)
        for name in package_view_page.runtime_dependencies_table_column_names:
            self.failUnless(name in header_text)
        dependency_values = package_view_page.table\
            .get_table_values_in_column_nr(package_view_page.runtime_dependencies_table_id,
                                           package_view_page.dependency_column_nr)
        ToasterValueList.is_list_ascending(dependency_values)

        #step 9
        self.log_test_step_number(9)
        package_view_page.is_text_present(package_view_page.mandatory_package_information_text)

        ##############
        #  CASE 946  #
        ##############
    def test_946(self):
        # steps 1-2
        self.log_test_step_number(1, 2)
        self.toaster_driver.go_to_base_url()
        home_page = toaster_pages.HomePage(self.toaster_driver.driver)
        build_page = home_page.select_core_image_minimal_build()
        config_page = build_page.select_configuration_option()

        # steps 3-4
        self.log_test_step_number(3, 4)
        config_page.check_for_mandatory_elements()
        summary_tab = config_page.open_summary_tab()
        summary_tab.is_text_present(summary_tab.mandatory_summary_tab_text)

        # step 5
        self.log_test_step_number(5)
        bitbake_vars_tab = summary_tab.open_bitbake_variables_tab()
        bitbake_vars_tab.is_text_present(bitbake_vars_tab.mandatory_bitbake_variables_tab_text)
        # This may be unstable because it's page-specific

        # step 6: this is how we find filter beside "Set in file"
        self.log_test_step_number(6)
        bitbake_vars_tab.filter_otable_by_local_config_variables()
        # save screen here
        ToasterDriver.browser_delay()
        self.screenshooter.take_screenshot(screenshot_type='selenium', append_name='step6')
        # save screen here

        # steps 7-8
        self.log_test_step_number(7, 8)
        # we should manually check the step 6-8 result using screenshot
        ToasterDriver.browser_delay()
        bitbake_vars_tab.edit_columns()
        self.screenshooter.take_screenshot(screenshot_type='selenium', append_name='step7-8')
        bitbake_vars_tab.edit_columns()
        time.sleep(4)

        # step 9
        self.log_test_step_number(9)
        # click the 1st item, no matter what it is
        bitbake_vars_tab.click_first_variable()
        self.toaster_driver.check_active_popup_element_for_text(bitbake_vars_tab.mandatory_variable_popup_element_text)

        # step 10 : need to manually check "Yocto Manual" in saved screen
        self.log_test_step_number(10)
        bitbake_vars_tab.click_first_link_to_manual()
        # save screen here
        time.sleep(5)
        self.screenshooter.take_screenshot(screenshot_type='native', append_name='step10')
        
        ###############
        #  CASE 1069  #
        ###############
    def test_1069(self):
        #step 1
        self.log_test_step_number(1)
        self.toaster_driver.go_to_base_url()
        home_page = toaster_pages.HomePage(self.toaster_driver.driver)
        project_page = home_page.select_selenium_project()
        
        #step 2
        self.log_test_step_number(2)
        layer_page  = project_page.select_layers_option()
        
        #step 3-5
        self.log_test_step_number(3)
        layer_page.is_text_present(layer_page.default_layers)
        self.log_test_step_number(4)
        layer_page.is_text_present(layer_page.default_columns)
        self.log_test_step_number(5)
        layer_page.is_text_present(layer_page.default_revision)
        
        #Change project release to "yocto master" to access more options
        layer_page.select_config_option()
        project_page.change_release("Yocto Project master")
        project_page.change_release("Local Yocto Project")
        
        #step 6
        layer_page.display_all_layers_columns()
        self.log_test_step_number(6)
        layer_page.search_for_layer("meta-yocto-bsp")
        layer_page.is_text_present("meta-yocto-bsp")
        layer_page.is_text_present("master")
        
        #step 7
        #step 7 cannot be automated at this time
        self.log_test_step_number(7)
        
        #step 8
        self.log_test_step_number(8)
        layer_page.is_text_present('github')
        
        ###############
        #  CASE 1070  #
        ###############
    def test_1070(self):
        #step 1
        self.log_test_step_number(1)
        self.toaster_driver.go_to_base_url()
        home_page = toaster_pages.HomePage(self.toaster_driver.driver)
        project_page = home_page.select_selenium_project()
        
        #step 2
        self.log_test_step_number(2)
        layer_page  = project_page.select_layers_option()
        
        #step 3
        list = get_table_values_in_column_nr(column_classes['Layer'])
        