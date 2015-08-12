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
                        self.toaster_driver.get_table_row_nr(tasks_page.otable_id))
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
                tasks_page.select_table_cell_by_class(tasks_page.columns_with_link_items[column_name])
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
            table_header_values = self.toaster_driver.get_table_head_text(perf_page.otable_id)
            self.log.info("table on current page has header: %s" % str(table_header_values))
            for value in perf_page.check_head_list:
                self.failUnless(value in table_header_values)
            time.sleep(2)
            main_column_values = perf_page.get_toaster_table_column_values_by_class(perf_page.column_class)
            self.failUnless(ToasterValueList.is_list_descending(main_column_values))
            for column_id in perf_page.check_column_list:
                perf_page.add_single_column_to_display_by_id(column_id)
            self.screenshooter.take_screenshot(screenshot_type='selenium', append_name='step11_%s' % perf_page.page_type)

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