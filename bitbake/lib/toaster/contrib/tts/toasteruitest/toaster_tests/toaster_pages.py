# The goal of this Page Objects design pattern is to have exactly 1 PageElement
# for each HTML element we need to interact with. This greatly improves the
# maintainability of the code, if something changes, we'll need to modify just
# one PageElement of PageObject

# Also, it is considered best practice for the PageObjects to only expose their
# functionality to other calling modules, and never the PageElements, in order to
# ensure that future changes will only impact the Page Object model

# If there are common HTML elements on several pages, one can use inheritance to
# define Page Elements only once in a base class and the pages having common
# elements should inherit the base class

from toaster_driver import *
from page_objects import PageObject, PageElement


class ToasterTable(PageObject):
    table_item_of_class_xpath = "//td[@class='%s']/a"
    table_cell_text_xpath = "//a[contains(.,'%s')]"
    table_column_class_xpath = "//td[@class='%s']"

    def __init__(self, webdriver):
        super(ToasterTable, self).__init__(webdriver)
        self.log = LOG

    def order_toaster_table_by_column(self, column_name, columns):
        if column_name not in columns:
            self.log.error("invalid column name %s" % column_name)
        else:
            self.w.find_element_by_link_text(column_name).click()

    def get_toaster_table_column_values(self, column_name, columns):
        values = None
        if column_name not in columns:
            self.log.error("invalid column name %s" % column_name)
        else:
            elements = self.w.find_elements_by_xpath(self.table_column_class_xpath % columns[column_name])
            values = [element.text for element in elements]
        return values

    def get_table_row_nr(self, table_id):
        table = self.w.find_element_by_id(table_id)
        rows = table.find_elements_by_tag_name("tr")
        return len(rows) - 1  # first row represents the table header

    def get_table_head_text(self, table_id):
        table = self.w.find_element_by_id(table_id)
        first_row = table.find_element_by_tag_name("tr")
        head_cells = first_row.find_elements_by_tag_name("th")
        return [str(cell.text) for cell in head_cells if len(cell.text) > 0]

    def get_table_values_in_column_nr(self, table_id, column_nr):
        column_index = column_nr - 1
        table = self.w.find_element_by_id(table_id)
        rows = table.find_elements_by_tag_name("tr")
        values = []
        for row in rows:
            columns = row.find_elements_by_tag_name("td")
            if len(columns) > column_index:
                values.append(str(columns[column_index].text))
        return values

    def get_toaster_table_column_values_by_class(self, column_class):
        elements = self.w.find_elements_by_xpath("//td[@class='%s']" % column_class)
        values = [element.text for element in elements if len(element.text) > 0]
        return values

    def select_table_cell_by_class(self, class_name):
        self.otable_table.find_element_by_xpath(self.table_item_of_class_xpath % class_name).click()


class ToasterPage(PageObject):
    # elements that appear on all Toaster pages
    all_builds_tab = PageElement(xpath="//a[@href='/toastergui/builds/']")
    edit_columns_button = PageElement(xpath="//button[contains(.,'Edit columns')]")
    apply_filter_button = PageElement(xpath="//button[@type='submit' and text()='Apply'"
                                      " and not(ancestor::form[@aria-hidden='true'])]")
    otable_id = "otable"
    otable_table = PageElement(id_=otable_id)
    search_text_field = PageElement(id_="search")
    search_submit_button = PageElement(xpath="//button[@value='Search']")
    clear_search_results_button = PageElement(xpath="//i[@class='icon-remove']")
    column_text_xpath = "//label[contains(.,'%s')]"
    visible_column_text_xpath = "//a[contains(.,'%s') and not(ancestor::th[@style='display: none;'])] | " \
                                "//span[contains(.,'%s') and not(ancestor::th[@style='display: none;'])]"
    filter_option_xpath = "//label[@class='radio' and not(ancestor::form[@aria-hidden='true'])]"
    nth_filter_option_xpath = "(//label[@class='radio' and not(ancestor::form[@aria-hidden='true'])])[%s]"

    def __init__(self, webdriver):
        super(ToasterPage, self).__init__(webdriver)
        self.table = ToasterTable(webdriver)
        self.log = LOG

    def is_text_present(self, patterns):
        not_found = []
        for pattern in patterns:
            if str(pattern) not in self.w.page_source:
                not_found.append(str(pattern))
                self.log.error("didn't find text pattern '%s'" % str(pattern))
        if len(not_found) == 0:
            return True, not_found
        else:
            return False, not_found

    def check_presence_of_page_elements(self, *elements):
        for element in elements:
            if element is None:
                self.log.error("page element is not displayed")

    def select_all_builds(self):
        self.all_builds_tab.click()
        return HomePage(self.w)

    def basic_search(self, search_string):
        self.search_text_field.clear()
        self.search_text_field.send_keys(search_string)
        self.search_submit_button.click()

    def basic_clear_search_results(self):
        self.clear_search_results_button.click()

    def add_single_column_to_display(self, column_name):
        self.edit_columns_button.click()
        ToasterDriver.browser_delay()
        self.w.find_element_by_xpath(self.column_text_xpath % column_name).click()
        self.edit_columns_button.click()

    def add_single_column_to_display_by_id(self, column_id):
        self.edit_columns_button.click()
        ToasterDriver.browser_delay()
        self.w.find_element_by_id(column_id).click()
        self.edit_columns_button.click()

    def ensure_column_displayed(self, column_name):
        try:
            WebDriverWait(self.w, 5).until(EC.presence_of_element_located((By.XPATH,
                                           self.visible_column_text_xpath % (column_name, column_name))))
        except Exception as e:
            self.log.error("could not find column name %s" % column_name)
            self.add_single_column_to_display(column_name)

    def add_columns_to_display(self, column_names):
        self.edit_columns_button.click()
        ToasterDriver.browser_delay()
        for name in column_names:
            self.w.find_element_by_xpath(self.column_text_xpath % name).click()
            ToasterDriver.browser_delay()
        self.edit_columns_button.click()

    def basic_filter(self, filter_element, filter_form, filter_option_xpath):
        filter_element.click()
        ToasterDriver.browser_delay()
        option = filter_form.find_element_by_xpath(filter_option_xpath)
        option.click()
        ToasterDriver.browser_delay()
        self.apply_filter_button.click()

    def get_nth_filter_option_xpath(self, n):
        return self.nth_filter_option_xpath % int(n)

    def get_nr_of_filter_options(self, filter_element):
        filter_element.click()
        ToasterDriver.browser_delay()
        nr_of_options = len(self.w.find_elements_by_xpath(self.filter_option_xpath))
        self.log.info("there are %s options for the current filter" % nr_of_options)
        self.apply_filter_button.click()
        return nr_of_options

    def is_element_present(self, selector_type, select_string):
        return len(self.w.find_elements(selector_type, select_string)) > 0


class HomePage(ToasterPage):
    core_image_minimal_build = PageElement(link_text="core-image-minimal")
    selenium_project = PageElement(link_text="selenium-project")
    add_column_log_option = PageElement(id_="log")
    add_column_started_on_option = PageElement(id_="started_on")
    add_column_time_option = PageElement(id_="time")
    recipe_column_name = "Recipe"
    started_on_column_name = 'Started on'
    column_name_class_map = {'Outcome': 'outcome', recipe_column_name: 'target', 'Machine': 'machine',
                             started_on_column_name: 'started_on', 'Completed on': 'completed_on',
                             'Errors': 'errors.count', 'Warnings': 'warnings.count', 'Time': 'time', 'Log': 'log'}
    outcome_filter = PageElement(xpath="//a[@href='#filter_outcome']")
    completed_on_filter = PageElement(xpath="//a[@href='#filter_completed_on']")
    started_on_filter = PageElement(xpath="//a[@href='#filter_started_on']")
    failed_tasks_filter = PageElement(xpath="//a[@href='#filter_failed_tasks']")
    errors_filter = PageElement(xpath="//a[@href='#filter_errors_no']")
    warnings_filter = PageElement(xpath="//a[@href='#filter_warnings_no']")

    outcome_filter_form = PageElement(xpath="//form[@id='filter_outcome']")
    completed_on_filter_form = PageElement(xpath="//form[@id='filter_completed_on']")
    started_on_filter_form = PageElement(xpath="//form[@id='filter_started_on']")
    failed_tasks_filter_form = PageElement(xpath="//form[@id='filter_failed_tasks']")
    errors_filter_form = PageElement(xpath="//form[@id='filter_errors_no']")
    warnings_filter_form = PageElement(xpath="//form[@id='filter_warnings_no']")

    second_filter_option_xpath = "(//label[@class='radio' and not(ancestor::form[@aria-hidden='true'])])[2]"

    def get_filter_filter_form_mapping(self):
        return [Filter("Outcome", self.outcome_filter, self.outcome_filter_form),
                Filter("Completed_on", self.completed_on_filter, self.completed_on_filter_form),
                Filter("Started_on", self.started_on_filter, self.started_on_filter_form),
                Filter("Failed tasks", self.failed_tasks_filter, self.failed_tasks_filter_form),
                Filter("Errors", self.errors_filter, self.errors_filter_form),
                Filter("Warnings", self.warnings_filter, self.warnings_filter_form)]

    def filter_builds(self, build_filter, filter_form, filter_option_xpath):
        self.basic_filter(build_filter, filter_form, filter_option_xpath)

    def check_filters_are_displayed(self):
        self.outcome_filter.is_displayed()
        self.completed_on_filter.is_displayed()
        self.started_on_filter.is_displayed()
        self.failed_tasks_filter.is_displayed()
        self.errors_filter.is_displayed()
        self.warnings_filter.is_displayed()

    def select_core_image_minimal_build(self):
        self.core_image_minimal_build.click()
        return BuildPage(self.w)

    def select_selenium_project(self):
        self.selenium_project.click()
        return ProjectPage(self.w)
        
    def display_started_on_column(self):
        self.add_single_column_to_display("Started on")

    def display_all_build_info_columns(self):
        self.add_columns_to_display(["Started on", "Log", "Time"])

    def order_builds_by_column(self, column_name):
        self.table.order_toaster_table_by_column(column_name, self.column_name_class_map)

    def get_build_column_values(self, column_name):
        return self.table.get_toaster_table_column_values(column_name, self.column_name_class_map)

    def search_for_build(self, search_string):
        self.basic_search(search_string)
        return HomePage(self.w)

    def clear_search_results(self):
        self.basic_clear_search_results()
        return HomePage(self.w)


class BuildPage(ToasterPage):
    breadcrumbs = PageElement(id_="breadcrumb")
    build_configuration_option = PageElement(link_text="Configuration")
    tasks_option = PageElement(link_text="Tasks")
    time_option = PageElement(link_text="Time")
    cpu_usage_option = PageElement(link_text="CPU usage")
    disk_io_option = PageElement(link_text="Disk I/O")
    packages_option = PageElement(link_text="Packages")
    left_nav_box_id = "nav"

    def get_nr_of_breadcrumbs(self):
        return len(self.breadcrumbs.find_elements_by_tag_name('li'))

    def get_breadcrumb_as_text_list(self):
        crumbs = self.breadcrumbs.find_elements_by_tag_name('li')
        return [crumb.get_attribute('innerHTML') for crumb in crumbs]

    def check_first_n_crumbs_links(self, n, link_substrings):
        crumbs = self.breadcrumbs.find_elements_by_tag_name('li')
        check = True
        for i in range(n):
            href = crumbs[i].find_element_by_tag_name('a').get_attribute('href')
            if link_substrings[i] not in href:
                check = False
        return check

    def check_last_breadcrumb_contains_string(self, string):
        return string in self. get_breadcrumb_as_text_list()[-1]

    def select_configuration_option(self):
        self.build_configuration_option.click()
        return ConfigurationPage(self.w)

    def select_tasks_option(self):
        self.tasks_option.click()
        return TasksPage(self.w)

    def select_time_option(self):
        self.time_option.click()
        return TimePage(self.w)

    def select_cpu_usage_option(self):
        self.cpu_usage_option.click()
        return CpuUsagePage(self.w)

    def select_disk_io_option(self):
        self.disk_io_option.click()
        return DiskIoPage(self.w)

    def select_packages_option(self):
        self.packages_option.click()
        return PackagesPage(self.w)

    def get_performance_page_navigators(self):
        return [self.select_time_option, self.select_cpu_usage_option, self.select_disk_io_option]


class PackagesPage(BuildPage):
    test_package_name = "bash"
    package_class = "package_name"
    breadcrumbs_ref_text = ['project', 'build', 'packages']

    def search_for_package(self, package_name):
        self.basic_search(package_name)

    def select_package(self, package_name):
        self.w.find_element_by_xpath(self.table_cell_text_xpath % package_name).click()
        return PackageViewPage(self.w)


class PackageViewPage(BuildPage):
    breadcrumbs_ref_text = PackagesPage.breadcrumbs_ref_text
    right_info_box_xpath = "//dl[@class='item-info']"
    path_values_class = "path"
    generated_files_tab = PageElement(xpath="//a[contains(.,'Generated files')]")
    runtime_dependencies_tab = PageElement(xpath="//a[contains(.,'Runtime dependencies')]")
    runtime_dependencies_table_id = "dependencies"
    dependency_column_nr = 1
    generated_files_table_column_names = ['File', 'Size']
    runtime_dependencies_table_column_names = ['Package', 'Version', 'Size']
    mandatory_package_information_text = ['Size', 'License', 'Recipe', 'Recipe version',
                                          'Layer', 'Layer branch', 'Layer commit']

    def check_mandatory_page_elements(self):
        self.generated_files_tab.is_displayed()
        self.runtime_dependencies_tab.is_displayed()

    def open_generated_files_tab(self):
        self.generated_files_tab.click()

    def open_runtime_dependencies_tab(self):
        self.runtime_dependencies_tab.click()


class TasksPage(BuildPage):
    page_size_select_xpath = "//select[@class='pagesize']"
    add_cpu_used_column_option = PageElement(id_="cpu_used")
    add_disk_io_column_option = PageElement(id_="disk_io")
    add_recipe_version_column_option = PageElement(id_="recipe_version")
    add_time_taken_column_option = PageElement(id_="time_taken")
    show_all_tasks_button = PageElement(xpath="//button[contains(.,'Show all tasks')]")
    column_name_class_map = {'Order': 'order', 'Recipe': 'recipe_name', 'Task': 'task_name', 'Executed': 'executed',
                             'Outcome': 'outcome', 'Cache attempt': 'cache_attempt', 'Time (secs)': 'time_taken',
                             'CPU usage': "cpu_used", 'Disk I/O (ms)': 'disk_io'}
    columns_with_link_items = {'Order': 'order', 'Task': 'task_name', 'Executed': 'executed', 'Outcome': 'outcome',
                               'Recipe': 'recipe_name', 'Recipe version': 'recipe_version'}
    executed_filter = PageElement(xpath="//a[@href='#filter_executed']")
    outcome_filter = PageElement(xpath="//a[@href='#filter_outcome']")
    cache_attempt_filter = PageElement(xpath="//a[@href='#filter_cache_attempt']")

    executed_filter_form = PageElement(xpath="//form[@id='filter_executed']")
    outcome_filter_form = PageElement(xpath="//form[@id='filter_outcome']")
    cache_attempt_filter_form = PageElement(xpath="//form[@id='filter_cache_attempt']")

    def get_filter_filter_form_mapping(self):
        return [Filter("Executed", self.executed_filter, self.executed_filter_form),
                Filter("Outcome", self.outcome_filter, self.outcome_filter_form),
                Filter("Cache attempt", self.cache_attempt_filter, self.cache_attempt_filter_form)]

    def get_nr_of_rows_in_select(self):
        select = Select(self.w.find_element_by_xpath(self.page_size_select_xpath))
        return int(select.first_selected_option.text)

    def display_all_build_info_columns(self):
        self.add_columns_to_display(["CPU usage", "Disk I/O (ms)", "Recipe version", "Time (secs)"])

    def search_for_task(self, search_string):
        self.basic_search(search_string)
        return TasksPage(self.w)

    def clear_search_results(self):
        self.basic_clear_search_results()
        return TasksPage(self.w)

    def order_tasks_by_column(self, column_name):
        try:
            WebDriverWait(self.w, 5).until(EC.presence_of_element_located((By.LINK_TEXT, column_name)))
        except Exception as e:
            self.log.error("could not find column %s" % column_name)
            self.add_single_column_to_display(column_name)
        self.table.order_toaster_table_by_column(column_name, self.column_name_class_map)

    def get_tasks_column_values(self, column_name):
        return self.table.get_toaster_table_column_values(column_name, self.column_name_class_map)

    def filter_tasks(self, task_filter, filter_form, filter_option_xpath):
        self.basic_filter(task_filter, filter_form, filter_option_xpath)

    def handle_no_results_page(self):
        try:
            WebDriverWait(self.w, 5).until(EC.presence_of_element_located((By.ID, self.otable_id)))
        except Exception as e:
            self.log.info("empty results page detected for the current filter")
            self.show_all_tasks_button.click()


class TimePage(TasksPage):
    page_type = "Time"
    column_class = "time_taken"
    check_head_list = ['Recipe', 'Task', 'Executed', 'Outcome', 'Time (secs)']
    check_column_list = ['cpu_used', 'cache_attempt', 'disk_io', 'order', 'recipe_version']


class CpuUsagePage(TasksPage):
    page_type = "CPU usage"
    column_class = "cpu_used"
    check_head_list = ['Recipe', 'Task', 'Executed', 'Outcome', 'CPU usage']
    check_column_list = ['cache_attempt', 'disk_io', 'order', 'recipe_version', 'time_taken']


class DiskIoPage(TasksPage):
    page_type = "Disk I/O"
    column_class = "disk_io"
    check_head_list = ['Recipe', 'Task', 'Executed', 'Outcome', 'Disk I/O (ms)']
    check_column_list = ['cpu_used', 'cache_attempt', 'order', 'recipe_version', 'time_taken']


class ConfigurationPage(BuildPage):
    summary_tab = PageElement(link_text="Summary")
    bitbake_variables_tab = PageElement(link_text="BitBake variables")

    def check_for_mandatory_elements(self):
        self.summary_tab.is_displayed()
        self.bitbake_variables_tab.is_displayed()

    def open_bitbake_variables_tab(self):
        self.bitbake_variables_tab.click()
        return BitBakeVariablesTab(self.w)

    def open_summary_tab(self):
        self.summary_tab.click()
        return SummaryTab(self.w)


class BitBakeVariablesTab(ConfigurationPage):
    mandatory_bitbake_variables_tab_text = ['Variable', 'Value', 'Set in file', 'Description']
    mandatory_variable_popup_element_text = ['Order', 'Configuration file', 'Operation', 'Line number']
    otable = PageElement(id_="otable")
    history_filename_filter_button = PageElement(xpath="//a[@href='#filter_vhistory__file_name']")
    local_config_vars_radio_button = PageElement(xpath="//input[contains(@value,'/conf/')]")
    first_variable_item = PageElement(xpath="//a[contains(@href,'#variable-')]")
    variable_to_manual_link = PageElement(css="i.icon-share.get-info")

    def filter_otable_on_set_in_file(self, filter_element):
        self.history_filename_filter_button.click()
        filter_element.click()
        self.apply_filter_button.click()

    def filter_otable_by_local_config_variables(self):
        self.filter_otable_on_set_in_file(self.local_config_vars_radio_button)

    def edit_columns(self):
        self.edit_columns_button.click()

    def click_first_variable(self):
        self.first_variable_item.click()

    def click_first_link_to_manual(self):
        self.variable_to_manual_link.click()


class SummaryTab(ConfigurationPage):
    mandatory_summary_tab_text = ['Layers', 'Layer', 'Layer branch', 'Layer commit', 'Layer directory']
    
class ProjectPage(ToasterPage):
    configuration_option=PageElement(link_text="Configuration")
    image_recipes_option=PageElement(link_text="Image recipes")
    software_recipes_option=PageElement(link_text="Software recipes")
    machines_option=PageElement(link_text="Machines")
    layers_option=PageElement(link_text="Layers")
    bb_variables_option=PageElement(link_text="Bitbake variables")
    project_builds_option=PageElement(class_name="total-builds")
    import_layer_option=PageElement(link_text="Import layer")
    import_layer_box=PageElement(id="import-layer-name")
    import_git_repo_box=PageElement(id="layer-git-repo-url")
    import_subdir_box=PageElement(id="layer-subdir")
    import_revision_box=PageElement(id="layer-git-ref")
    import_add_button=PageElement(id="import-and-add-btn")
    build_input_box=PageElement(id="build-input")
    build_button_option=PageElement(id="build-button")
    release_change_option=PageElement(id="release-change-toggle")
    release_change_form=PageElement(id="change-release-form")
    release_change_button=PageElement(id="change-release-btn")
    machine_change_option=PageElement(id="change-machine-toggle")
    machine_change_box=PageElement(id="machine-change-input")
    machine_change_button=PageElement(id="machine-change-btn")
    
    def select_layers_option(self):
        self.layers_option.click()
        return LayersPage(self.w)
        
    def select_image_recipes_option(self):
        self.image_recipes_option.click()
        return RecipesPage(self.w)
        
    def select_machines_option(self):
        self.machines_option.click()
        return MachinesPage(self.w)
        
    def select_bb_variables_option(self):
        self.bb_variables_option.click()
        return VariablesPage(self.w)
    
    def select_config_option(self):
        self.configuration_option.click()
        return ProjectPage(self.w)
    
    def change_release(self, release):
        self.relese_change_option.click()
        self.release_change_form.send_keys(release)
        self.release_change_button.click()
    
    def change_machine(self, machine):
        self.machine_change_option.click()
        self.machine_change_box.send_keys(machine)
        self.machine_change_button.click()
        
    def add_layer(self, layer, git_repo, subdir, revision):
        self.import_layer_option.click()
        self.import_layer_box.send_keys(layer)
        self.import_git_repo_box.send_keys(git_repo)
        self.import_subdir_box.send_keys(subdir)
        self.import_revision_box.send_keys(revision)
        self.import_add_button.click()
        
    
class LayersPage(ProjectPage):
    default_columns = ['Layer', 'Summary', 'Revision', 'Dependencies', 'Add/Delete']
    default_layers = ['meta-yocto-bsp', 'meta-yocto', 'openembedded-core']
    default_revision = 'HEAD'
    search_text_field = PageElement(id="search-input-layerstable")
    search_submit_button = PageElement(id="search-submit-layerstable")
    column_classes = {'Layer':'layer__name'}
    
    def display_all_layers_columns(self):
        self.add_columns_to_display(["Git repository URL", "Subdirectory"])
    
    def search_for_layer(self, search_string):
        self.search_text_field.clear()
        self.search_text_field.sendkeys(search_string)
        self.search_submit_button.click()
    