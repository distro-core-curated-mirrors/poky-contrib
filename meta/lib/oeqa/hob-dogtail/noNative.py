#!/usr/bin/python

import os
from dogtail import *
from finishBuild import TestFinish
from os import environ, path, remove
import subprocess
import time
from base import Base

try:
    bitbake = tree.root.application('bitbake')
except:
    print "can not connect to the application"
else:
    try:
        hob = bitbake.child( roleName='frame' )
    except:
        print "can not connect to the application"

class NoNativeRecipes(Base):

    def searchNativeRecipes(self):	
        self.selectMachine('qemux86')
        self.selectImage('core-image-minimal')
        try:
            hob.child('Edit image recipe').click()
        except:
            self.writeInFile("no_native: can not edit image button")
            return 10

        try:
            includedRecipes = hob.child('Included recipes')
        except:
            self.writeInFile("no_native: can not incude recipes button")

        recipesList = includedRecipes.findChildren(predicate.GenericPredicate(roleName="table cell"))
        error=False
        for i in range(len(recipesList)):
            if recipesList[i].name.find("-native") != -1:
                error=True
                break
        if error:
            self.writeInFile("No native recipe shown in recipe list: failed")
        else:
            self.writeInFile("No native recipe shown in recipe list: passed")
        try:
            hob.child('Cancel').click()
        except:
            self.writeInFile("no_native: can not find cancel button")
            return 10
        time.sleep(10)
	scriptname=os.path.basename(__file__)
	print "Ending "+scriptname
        return 10
