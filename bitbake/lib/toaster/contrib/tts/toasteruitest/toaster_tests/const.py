import os

### Configuration related constants
MAIN_CONFIG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "toaster_test.cfg")

### Logging related constants
LOG_TOP_DIR_NAME = "log"
LOG_TMP_DIR_NAME = "tmp"
MAIN_LOG_FILENAME = "case_all.log"
LOG_DIR_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), LOG_TOP_DIR_NAME)
TMP_LOG_DIR_PATH = os.path.join(LOG_DIR_PATH, LOG_TMP_DIR_NAME)
LOG_TESTCASE_START_HEADER = """


        ##############
        #  CASE $NR  #
        ##############

"""
LOG_AGGREGATE_RESULTS = """
==========================================================================================
Total tests ran: $TOTAL_TESTS
Failed: $FAILED_TESTS
Passed: $PASSED_TESTS
"""