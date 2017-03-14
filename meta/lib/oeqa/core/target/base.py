# Copyright (C) 2016 Intel Corporation
# Released under the MIT license (see COPYING.MIT)
import os
import sys
import importlib

from abc import abstractmethod

# Used to keep record of registered targets, it
# uses class' targetName as the key to the class.
targetClasses = {}

def registerTarget(obj):
    """ Use as decorator to register targets for runtime testing """

    if (obj.targetName in targetClasses and
        obj.__name__ != targetClasses[obj.targetName].__name__):

        msg = ('Tried to register %s as "%s" that is used by %s' %
               (obj, obj.targetName, targetClasses[obj.targetName]))
        raise ImportError(msg)

    if not issubclass(obj, OETarget):
        raise TypeError('%s must inherit from OETarget' % obj)

    targetClasses[obj.targetName] = obj
    return obj

class OETarget(object):

    def __init__(self, logger, *args, **kwargs):
        self.logger = logger

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def run(self, cmd, timeout=None):
        pass

    @abstractmethod
    def copyTo(self, localSrc, remoteDst):
        pass

    @abstractmethod
    def copyFrom(self, remoteSrc, localDst):
        pass

    @abstractmethod
    def copyDirTo(self, localSrc, remoteDst):
        pass
