import re
import sys
import os
import time
import const
import errno
import logging
import platform
import ConfigParser


def enum(**enums):
    return type('Enum', (), enums)


class ToasterTestsLog(object):
    log_tmp_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), const.LOG_TOP_DIR_NAME,
                               const.LOG_TMP_DIR_NAME)

    def __init__(self, logging_level):
        """
        we use root logger for every testcase.
        The reason why we don't use TOASTERXXX_logger is to avoid setting respective level for
        root logger and TOASTERXXX_logger
        To Be Discussed
        """
        CommonToasterTestsUtils.mkdir_p(ToasterTestsLog.log_tmp_dir)
        log_level_dict = {'CRITICAL': logging.CRITICAL, 'ERROR': logging.ERROR, 'WARNING': logging.WARNING,
                          'INFO': logging.INFO, 'DEBUG': logging.DEBUG, 'NOTSET': logging.NOTSET}
        log = logging.getLogger()
        self.logging_level = logging_level
        key = self.logging_level.upper()
        log.setLevel(log_level_dict[key])
        log_filename = os.path.join(ToasterTestsLog.log_tmp_dir, const.MAIN_LOG_FILENAME)
        fh = logging.FileHandler(filename=log_filename, mode='a')
        ch = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(pathname)s - %(lineno)d - %(levelname)s - %(message)s ')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        log.addHandler(fh)
        log.addHandler(ch)
        self.log = log


class ToasterTestsConfig(object):
    host_os = platform.system().lower()
    case_no = None
    base_url = None
    browser = None
    logging_level = None
    cases_to_run = None
    configs = None
    initialized = False

    @staticmethod
    def initialize():
        parser = ConfigParser.SafeConfigParser()
        configs = parser.read(const.MAIN_CONFIG_FILE_PATH)
        ToasterTestsConfig.configs = configs
        ToasterTestsConfig.base_url = eval(parser.get('toaster_test_' + ToasterTestsConfig.host_os, 'toaster_url'))
        ToasterTestsConfig.browser = eval(parser.get('toaster_test_' + ToasterTestsConfig.host_os, 'test_browser'))
        ToasterTestsConfig.logging_level = eval(parser.get('toaster_test_' + ToasterTestsConfig.host_os, 'logging_level'))
        ToasterTestsConfig.cases_to_run = eval(parser.get('toaster_test_' + ToasterTestsConfig.host_os, 'test_cases'))
        ToasterTestsConfig.initialized = True

    @staticmethod
    def set_case_no(test_method_name):
        """
        This method will be called by the setUp method before starting each test to set the test case number
        :param test_method_name: the test method that represents the test currently executed
        :return: a number representing the test number
        """
        digit_seqence_pattern = '\d+'
        test_nr = int(re.findall(digit_seqence_pattern, test_method_name)[0])
        ToasterTestsConfig.case_no = test_nr
        return test_nr


class ScreenShooter(object):
    def __init__(self, webdriver):
        self.driver = webdriver
        self.screenshot_sequence = 1

    def take_screenshot(self, **log_args):
        """
        This function is used to save screen either by os interface or selenium interface.
        How to use:
        self.save_screenshot(screenshot_type = 'native'/'selenium', log_sub_dir = 'xxx',
                             append_name = 'stepx')
        where native means screenshot func provided by OS,
        selenium means screenshot func provided by selenium webdriver
        """
        types = [log_args.get('screenshot_type')]
        # when no screenshot_type is specified
        if types == [None]:
            types = ['native', 'selenium']
        # normally append_name is used to specify which step..
        add_name = log_args.get('append_name')
        if not add_name:
            add_name = '-'
        # normally there's no need to specify sub_dir
        sub_dir = log_args.get('log_sub_dir')
        if not sub_dir:
            # use casexxx as sub_dir name
            sub_dir = 'case' + str(ToasterTestsConfig.case_no)
        for item in types:
            log_dir = ToasterTestsLog.log_tmp_dir + os.sep + sub_dir
            CommonToasterTestsUtils.mkdir_p(log_dir)
            log_path = log_dir + os.sep + ToasterTestsConfig.browser + '-' + \
                item + '-' + add_name + '-' + str(self.screenshot_sequence) + '.png'
            if item == 'native':
                os.system("scrot " + log_path)
            elif item == 'selenium':
                self.driver.get_screenshot_as_file(log_path)
            self.screenshot_sequence += 1


class CommonToasterTestsUtils(object):
    @staticmethod
    def mkdir_p(dir_name):
        try:
            os.makedirs(dir_name)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(dir_name):
                pass
            else:
                raise


class ToasterValueList(object):
    """
    Set of list attribute. This is used to determine what the list content is.
    Later on we may add more attributes here.
    """
    NULL = "null"
    NUMBERS = "numbers"
    STRINGS = "strings"
    PERCENT = "percentage"
    SIZE = "size"
    UNKNOWN = "unknown"

    @staticmethod
    def get_list_attr(testlist):
        """
        To determine the list content
        """
        if not testlist:
            return ToasterValueList.NULL
        listtest = testlist[:]
        try:
            listtest.remove('')
        except ValueError:
            pass
        pattern_percent = re.compile(r"^([0-9])+(\.)?([0-9])*%$")
        pattern_size = re.compile(r"^([0-9])+(\.)?([0-9])*( )*(K)*(M)*(G)*B$")
        pattern_number = re.compile(r"^([0-9])+(\.)?([0-9])*$")

        def get_patterned_number(pattern, tlist):
            count = 0
            for item in tlist:
                if re.search(pattern, item):
                    count += 1
            return count
        if get_patterned_number(pattern_percent, listtest) == len(listtest):
            return ToasterValueList.PERCENT
        elif get_patterned_number(pattern_size, listtest) == len(listtest):
            return ToasterValueList.SIZE
        elif get_patterned_number(pattern_number, listtest) == len(listtest):
            return ToasterValueList.NUMBERS
        else:
            return ToasterValueList.STRINGS

    @staticmethod
    def is_list_ascending(testlist):
        """
        Function to tell if list is sequenced
        Currently we may have list made up of: Strings ; numbers ; percentage ; time; size
        Each has respective way to determine if it's sequenced.
        """
        test_list = testlist[:]
        try:
            test_list.remove('')
        except ValueError:
            pass

        if ToasterValueList.get_list_attr(testlist) == ToasterValueList.NULL:
            return True

        elif ToasterValueList.get_list_attr(testlist) == ToasterValueList.STRINGS:
            return sorted(test_list) == test_list

        elif ToasterValueList.get_list_attr(testlist) == ToasterValueList.NUMBERS:
            list_number = []
            for item in test_list:
                list_number.append(eval(item))
            return sorted(list_number) == list_number

        elif ToasterValueList.get_list_attr(testlist) == ToasterValueList.PERCENT:
            list_number = []
            for item in test_list:
                list_number.append(eval(item.strip('%')))
            return sorted(list_number) == list_number

        elif ToasterValueList.get_list_attr(testlist) == ToasterValueList.SIZE:
            list_number = []
            # currently SIZE is splitted by space
            for item in test_list:
                if item.split()[1].upper() == "KB":
                    list_number.append(1024 * eval(item.split()[0]))
                elif item.split()[1].upper() == "MB":
                    list_number.append(1024 * 1024 * eval(item.split()[0]))
                elif item.split()[1].upper() == "GB":
                    list_number.append(1024 * 1024 * 1024 * eval(item.split()[0]))
                else:
                    list_number.append(eval(item.split()[0]))
            return sorted(list_number) == list_number

        else:
            print 'Unrecognized list type, please check'
            return False

    @staticmethod
    def is_list_descending(testlist):
        """
        Function to tell if list is inverted
        Currently we may have list made up of: Strings ; numbers ; percentage ; time; size
        Each has respective way to determine if it's inverted.
        """
        test_list = testlist[:]
        try:
            test_list.remove('')
        except ValueError:
            pass

        if ToasterValueList.get_list_attr(testlist) == ToasterValueList.NULL:
            return True

        elif ToasterValueList.get_list_attr(testlist) == ToasterValueList.STRINGS:
            return sorted(test_list, reverse=True) == test_list

        elif ToasterValueList.get_list_attr(testlist) == ToasterValueList.NUMBERS:
            list_number = []
            for item in test_list:
                list_number.append(eval(item))
            return sorted(list_number, reverse=True) == list_number

        elif ToasterValueList.get_list_attr(testlist) == ToasterValueList.PERCENT:
            list_number = []
            for item in test_list:
                list_number.append(eval(item.strip('%')))
            return sorted(list_number, reverse=True) == list_number

        elif ToasterValueList.get_list_attr(testlist) == ToasterValueList.SIZE:
            list_number = []
            # currently SIZE is splitted by space. such as 0 B; 1 KB; 2 MB
            for item in test_list:
                if item.split()[1].upper() == "KB":
                    list_number.append(1024 * eval(item.split()[0]))
                elif item.split()[1].upper() == "MB":
                    list_number.append(1024 * 1024 * eval(item.split()[0]))
                elif item.split()[1].upper() == "GB":
                    list_number.append(1024 * 1024 * 1024 * eval(item.split()[0]))
                else:
                    list_number.append(eval(item.split()[0]))
            return sorted(list_number, reverse=True) == list_number

        else:
            print 'Unrecognized list type, please check'
            return False

    @staticmethod
    def lists_have_oposite_monotonicity(list_a, list_b):
        return ((ToasterValueList.is_list_ascending(list_a) and ToasterValueList.is_list_descending(list_b)) or
               (ToasterValueList.is_list_ascending(list_b) and ToasterValueList.is_list_descending(list_a)))


class Filter(object):
    def __init__(self, name, column_filter, filter_form):
        self.name = name
        self.column_filter = column_filter
        self.filter_form = filter_form


ToasterTestsConfig.initialize()
LOG = ToasterTestsLog(ToasterTestsConfig.logging_level).log
