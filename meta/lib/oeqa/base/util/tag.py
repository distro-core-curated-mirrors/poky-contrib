#!/usr/bin/env python
# Copyright (C) 2013 Intel Corporation
#
# Released under the MIT license (see COPYING.MIT)

# Tag filter module used by testrunner
# This provides tag based filtering function for test case set.

"""Tag Filter Module"""
import unittest

TAG_PREFIX = "tag__"
def tag(*args, **kwargs):
    """tag decorator that adds attributes to classes or functions"""
    def wrap_obj(obj):
        """wrap function"""
        for name in args:
            setattr(obj, TAG_PREFIX + name, True)
        for name, value in kwargs.iteritems():
            setattr(obj, TAG_PREFIX + name, value)
        return obj
    return wrap_obj

def gettag(obj, key, default=None):
    """get a tag value from obj"""
    key = TAG_PREFIX + key
    if not isinstance(obj, unittest.TestCase):
        return getattr(obj, key, default)
    tc_method = getattr(obj, obj._testMethodName)
    ret = getattr(tc_method, key, getattr(obj, key, default))
    return ret

def getvar(obj):
    """if a variable not exist, find it in testcase"""
    class VarDict(dict):
        """wrapper of var dict"""
        def __getitem__(self, key):
            return gettag(obj, key)
    return VarDict()

def checktags(testcase, tagexp):
    """eval tag expression and return the result"""
    return eval(tagexp, None, getvar(testcase))

def filter_tagexp(testsuite, tagexp):
    """filter according to true or flase of tag expression"""
    if not tagexp:
        return testsuite
    caselist = []
    for each in testsuite:
        if not isinstance(each, unittest.BaseTestSuite):
            if checktags(each, tagexp):
                caselist.append(each)
        else:
            caselist.append(filter_tagexp(each, tagexp))
    return testsuite.__class__(caselist)
