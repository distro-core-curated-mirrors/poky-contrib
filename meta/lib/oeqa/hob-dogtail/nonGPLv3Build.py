from dogtail import *
import sys, string
import os
from finishBuild import TestFinish
import time
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

config.searchCutoffCount=20

class NonGPL(Base):

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


    def nonGPL(self):
        self.selectMachine('qemux86')
	time.sleep(240)
        try:
            selectDistro = hob.child(name = 'Advanced configuration\nSelect image types, package formats, etc', roleName='push button')
            selectDistro.click()
        except:
            self.writeInFile("nonGPLV3_build: can not find adv config button")
            return 10

        try:
            advConfig=bitbake.dialog('Advanced configuration')
        except:
            self.writeInFile("nonGPLV3_build: can not find adv config dialog")
            return 10
        try:
            changeTab=advConfig.child('Output').click()
        except:
            self.writeInFile("nonGPLV3_build: can not find ouput button")
            return 10

        try:
            excludeGPLv3 = advConfig.child(name = 'Exclude GPLv3 packages').click()
        except:
            self.writeInFile("nonGPLV3_build: can not find exclude GPLv3 button")
            return 10

        advConfig.child('Save').click()
        time.sleep(400)

        self.selectImage('core-image-minimal')

        try:
            hob.child('Build image').click()
        except:
            self.writeInFile("nonGPLV3_build: can not find build image button")
            return 10

 	time.sleep(180)

	#t=TestFinish()
        #finish = t.analyse()
	
	finish = Finish().waitFinish()
	#finish = self.testFinish()
	time.sleep(60)

        if finish == 20:
            self.writeInFile("non-GPLv3 build: failed")
        else:
            self.writeInFile("non-GPLv3 build: passed")
        time.sleep(30)
	finish = 1
        try:
            bnw = hob.child('Build new image')
	    print "Clicking Build new image"
	    t=str(bnw)
	    try:
		print t    
		if t.index('Build new image') > 0:
			try:                        
				bnw.click()				
			except:
				print "Found the build new image button but failed to click it!"
		else:
			print "Cannot find build new image button"
	    except:
		print "Not the right element!"        
        except:
            self.writeInFile("nonGPLV3_build: can not find build new image button")


	#deselect option to not mess with next tests
        self.selectMachine('qemux86')
	time.sleep(240)
	print "Clicking advanced configuration..."
        try:
            selectDistro = hob.child(name = 'Advanced configuration\nSelect image types, package formats, etc', roleName='push button')
            selectDistro.click()
        except:
            self.writeInFile("nonGPLV3_build: can not find adv config button")
            return 10
	
        try:
            advConfig=bitbake.dialog('Advanced configuration')
        except:
            self.writeInFile("nonGPLV3_build: can not find adv config dialog")
            return 10
	print "Clicking output tab..."
        try:
            changeTab=advConfig.child('Output').click()
        except:
            self.writeInFile("nonGPLV3_build: can not find ouput button")
            return 10
	print "Unchecking Exclude checkbox..."
        try:
            excludeGPLv3 = advConfig.child(name = 'Exclude GPLv3 packages').click()
        except:
            self.writeInFile("nonGPLV3_build: can not find exclude GPLv3 button")
            return 10

	print "Clicking Save button..."
	try:        
		saveButton=advConfig.child('Save').click()
	except:
		print "Cannot click Save button"
        time.sleep(300)

	scriptname=os.path.basename(__file__)
	print "Ending "+scriptname
	#finish=1
        #return 10
