#!/usr/bin/python
#
# DESCRIPTION
# This is script consist of common utils like sorting, getting attribute and so on.
# These modules are used for running all selected toaster cases
# on selected web browser manifested in toaster_test.cfg
#

import  errno
import  logging
import  os
import  re
import  sys

class Listattr(object):
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

def get_log_root_dir():
    max_depth = 5
    parent_dir = '../'
    for number in range(0, max_depth):
        if os.path.isdir(sys.path[0] + os.sep + (os.pardir + os.sep)*number + 'log'):
            log_root_dir = os.path.abspath(sys.path[0] + os.sep + (os.pardir + os.sep)*number + 'log')
            break

    if number == (max_depth - 1):
        print('No log dir found. Please check')
        raise Exception

    return log_root_dir

def get_list_attr(testlist):
    """
    To determine the list content
    """
    if not testlist:
        return Listattr.NULL
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
        return Listattr.PERCENT
    elif get_patterned_number(pattern_size, listtest) == len(listtest):
        return Listattr.SIZE
    elif get_patterned_number(pattern_number, listtest) == len(listtest):
        return Listattr.NUMBERS
    else:
        return Listattr.STRINGS

def is_list_sequenced(testlist):
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

    if get_list_attr(testlist) == Listattr.NULL :
        return True

    elif get_list_attr(testlist) == Listattr.STRINGS :
        return (sorted(test_list) == test_list)

    elif get_list_attr(testlist) == Listattr.NUMBERS :
        list_number = []
        for item in test_list:
            list_number.append(eval(item))
        return (sorted(list_number) == list_number)

    elif get_list_attr(testlist) == Listattr.PERCENT :
        list_number = []
        for item in test_list:
            list_number.append(eval(item.strip('%')))
        return (sorted(list_number) == list_number)

    elif get_list_attr(testlist) == Listattr.SIZE :
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
        return (sorted(list_number) == list_number)

    else:
        print('Unrecognized list type, please check')
        return False


def is_list_inverted(testlist):
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

    if get_list_attr(testlist) == Listattr.NULL :
        print ("is_list_inverted ---> 1")
        return True

    elif get_list_attr(testlist) == Listattr.STRINGS :
        print ("is_list_inverted ---> 2")
        return (sorted(test_list, reverse = True) == test_list)
        print ("is_list_inverted ---> 3")

    elif get_list_attr(testlist) == Listattr.NUMBERS :
        print ("is_list_inverted ---> 4")
        list_number = []
        for item in test_list:
            list_number.append(eval(item))
        return (sorted(list_number, reverse = True) == list_number)

    elif get_list_attr(testlist) == Listattr.PERCENT :
        print ("is_list_inverted ---> 5")
        list_number = []
        for item in test_list:
            list_number.append(eval(item.strip('%')))
        return (sorted(list_number, reverse = True) == list_number)

    elif get_list_attr(testlist) == Listattr.SIZE :
        print ("is_list_inverted ---> 6")
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
        return (sorted(list_number, reverse = True) == list_number)

    else:
        print ("is_list_inverted ---> 7")
        print('Unrecognized list type, please check')
        return False

def replace_file_content(filename, item, option):
    f = open(filename)
    lines = f.readlines()
    f.close()
    output = open(filename, 'w')
    for line in lines:
        if line.startswith(item):
            output.write(item + " = '" + option + "'\n")
        else:
            output.write(line)
    output.close()

def extract_number_from_string(s):
    """
    extract the numbers in a string. return type is 'list'
    """
    return re.findall(r'([0-9]+)', s)

def mkdir_p(dir):
    try:
        os.makedirs(dir)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dir):
            pass
        else:
            raise

# Below is decorator derived from toaster backend test code
class NoParsingFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == 100

#rewrite the run method of unittest.TestCase to add testcase logging
def LogResults(original_class):
    orig_method = original_class.run

    from time import strftime, gmtime
    caller = 'toaster'
    timestamp = strftime('%Y%m%d%H%M%S', gmtime())
    logfile = os.path.join(os.getcwd(), 'results-' + caller + '.' + timestamp + '.log')
    linkfile = os.path.join(os.getcwd(), 'results-' + caller + '.log')

    # rewrite the run method of unittest.TestCase to add testcase logging
    def run(self, result, *args, **kws):
        orig_method(self, result, *args, **kws)
        passed = True
        testMethod = getattr(self, self._testMethodName)
        # if test case is decorated then use it's number, else use it's name
        try:
            test_case = testMethod.test_case
        except AttributeError:
            test_case = self._testMethodName

        class_name = str(testMethod.im_class).split("'")[1]

        # create custom logging level for filtering.
        custom_log_level = 100
        logging.addLevelName(custom_log_level, 'RESULTS')

        def results(self, message, *args, **kws):
            if self.isEnabledFor(custom_log_level):
                self.log(custom_log_level, message, *args, **kws)

        logging.Logger.results = results

        logging.basicConfig(filename=logfile,
                            filemode='w',
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            datefmt='%H:%M:%S',
                            level=custom_log_level)
        for handler in logging.root.handlers:
            handler.addFilter(NoParsingFilter())
        local_log = logging.getLogger(caller)

        # check status of tests and record it
        for (name, msg) in result.errors:
            if (self._testMethodName == str(name).split(' ')[0]) and (class_name in str(name).split(' ')[1]):
                local_log.results("Testcase " + str(test_case) + ": ERROR")
                local_log.results("Testcase " + str(test_case) + ":\n" + msg)
                passed = False
        for (name, msg) in result.failures:
            if (self._testMethodName == str(name).split(' ')[0]) and (class_name in str(name).split(' ')[1]):
                local_log.results("Testcase " + str(test_case) + ": FAILED")
                local_log.results("Testcase " + str(test_case) + ":\n" + msg)
                passed = False
        for (name, msg) in result.skipped:
            if (self._testMethodName == str(name).split(' ')[0]) and (class_name in str(name).split(' ')[1]):
                local_log.results("Testcase " + str(test_case) + ": SKIPPED")
                passed = False
        if passed:
            local_log.results("Testcase " + str(test_case) + ": PASSED")

        # Create symlink to the current log
        if os.path.exists(linkfile):
            os.remove(linkfile)
        os.symlink(logfile, linkfile)

    original_class.run = run
    return original_class