import unittest

class ToasterOptions(object): 
    pass

class ToasterTestCase(unittest.TestCase):
    def __init__(self, testname, opts, logger):
        super(ToasterTestCase, self).__init__(testname)

        self.opts = opts
        self.logger = logger
