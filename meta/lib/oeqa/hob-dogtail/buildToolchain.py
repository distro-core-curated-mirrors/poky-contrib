#!/usr/bin/python

import os
from dogtail import tree
from dogtail.utils import run
import sys, string, time
import subprocess
from subprocess import call
#from finishBuild import TestFinish
from dogtail.tree import predicate
from base import Base
from finish import Finish

try:
    bitbake = tree.root.application('bitbake')
except:
    print "can not connect to the application"
else:
    try:
        hob = bitbake.child( roleName='frame' )
    except:
        print "can not connect to the application"

class BuildToolchain(Base):

    def testFinish(self):
    	try:
    		finish = hob.child("Build new image")
		print "Image is ready"
		return 10
    	except:
		return 25
	else:
		try:
			finish = hob.child("File a bug")
			return 20
		except:
			return 25
		else:
			try:
				finish = hob.child("Step 2 of 2: Edit packages")
				return 20
			except:			
				print "Image ready not detected"
				return 25

    def toolchain(self):
        self.selectMachine('qemux86')
	time.sleep(240)
        try:
            selectToolchain = hob.child(name = 'Advanced configuration\nSelect image types, package formats, etc', roleName='push button')
            selectToolchain.click()
        except:
            self.writeInFile("build toolchain: can not find adv config button")
            return 10
        try:
            advConfig=bitbake.dialog('Advanced configuration')
        except:
            self.writeInFile("build toolchain: can not find adv config dialog")
            return 10
        try:
            changeTab=advConfig.child('Output').click()
        except:
            self.writeInFile("build toolchain: can not find output button")
            return 10

        try:
            excludeGPLv3 = advConfig.child(name = 'Populate SDK').click()
        except:
            self.writeInFile("build toolchain: can not find build toolchain button")
            return 10

        try:
            otherPackage = advConfig.findChildren(predicate.GenericPredicate(roleName="combo box"))
            otherPackage[2].click()
        except:
            self.writeInFile("build toolchain: can not select toolchain")
            return 10
        try:
            advConfig.child('i586').click()
        except:
            self.writeInFile("build toolchain: can not select i586")
            return 10
        try:
            advConfig.child('Save').click()
        except:
            self.writeInFile("build toolchain: can not find save button")
            return 10
	
	time.sleep(180)
        self.selectImage('core-image-sato')
        time.sleep(5)
        try:
            hob.child('Build image').click()
        except:
            self.writeInFile("build toolchain: can not find build image button")
            return 10

	time.sleep(120)

	#t=TestFinish()
        #finish = t.analyse()
	
	finish = Finish().waitFinish()
	#finish = self.testFinish()

	time.sleep(240)
        if finish == 20:
            self.writeInFile("build tolchain: failed")
        else:
            self.writeInFile("build tolchain: passed")

        time.sleep(180)
	finish=1
        try:
            hob.child('Build new image').click()
        except:
            pass
	scriptname=os.path.basename(__file__)
	print "Ending "+scriptname
        return 10
