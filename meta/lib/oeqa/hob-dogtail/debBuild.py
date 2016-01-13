#!/usr/bin/python

import os
from dogtail import tree
from dogtail.utils import run
import time
#from finishBuild import TestFinish
from dogtail.tree import predicate
from base import Base
from openLog import ViewLog
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

class DebImageBuild(Base):

    def testFinish(self):
	final = None
    	try:
    		final = hob.child("Build new image")
		print "Image is ready"
		if final is not None:
			print final
			return 10
    	except:
		return 25
	else:
		try:
			final = hob.child("File a bug")
			if final is not None:
				return 20
		except:
			return 25
		else:
			try:
				final = hob.child("Step 2 of 2: Edit packages")
				if final is not None:
					return 20
			except:			
				print "Image ready not detected"
				return 25
    def debBuild(self):
        self.selectMachine('qemux86')
	time.sleep(60)

        press = 0
        while press < 20:
            try:
                selectDistro = hob.child(name = 'Advanced configuration\nSelect image types, package formats, etc', roleName='push button')
                selectDistro.click()
                break
            except:
                press += 1
        if press == 20:
            self.writeInFile("deb_build: can not find advanced configuration button")
            return 10

        press = 0
        while press < 20:
            try:
                advConfig=bitbake.dialog('Advanced configuration')
                changeTab=advConfig.child('Output').click()
                break
            except:
                press += 1
        if press == 20:
            self.writeInFile("deb_build: can not find output button")
            return 10

        press = 0
        while press < 20:
            try:
                distroType = advConfig.findChildren(predicate.GenericPredicate(roleName="combo box"))
                distroType[1].click()
                break
            except:
                press += 1

        try:
            selectPackageType = advConfig.child(name='deb')
            selectPackageType.click()
        except:
            self.writeInFile("deb_build: can not find package button")
            return 10
        try:
            advConfig.child('Save').click()
        except:
            self.writeInFile("deb_build: can not find save button")
            return 10
        time.sleep(180)

        self.selectImage('core-image-minimal')
        try:
            hob.child('Build image').click()
        except:
            self.writeInFile("deb_build: can not find build image button")
            return 10

	time.sleep(120)

	#t=TestFinish()
        #finish = t.analyse()
	
	finish = Finish().waitFinish()
	#finish = self.testFinish()

        if finish == 20:
            self.writeInFile("deb build image: failed")
        else:
            self.writeInFile("deb image build: passed")
            #log = ViewLog()
            #log.openLog()
        time.sleep(120)
	finish = 1
        try:
            bnw = hob.child('Build new image')
            bnw.click()
        except:
            self.writeInFile("deb build image: can not find build new image button")
        return 10
