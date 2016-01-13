from dogtail import tree
from dogtail.utils import run
import os
import sys, string, time
import subprocess
from subprocess import call
from finishBuild import TestFinish
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

class IpkImageBuild(Base):

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

    def ipkSelect(self):
        self.selectMachine('qemux86')
	time.sleep(180)

        press = 0
        while press < 20:
            try:
                selectDistro = hob.child(name = 'Advanced configuration\nSelect image types, package formats, etc', roleName='push button')
                selectDistro.click()
                break
            except:
                press += 1
        if press == 20:
            self.writeInFile("ipk_build: can not find advanced configuration button")
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
            self.writeInFile("ipk_build: can not find output button")
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
            selectPackageType = advConfig.child(name='ipk')
            selectPackageType.click()
        except:
            self.writeInFile("ipk_build: can not find package button")
            return 10
        try:
            advConfig.child('Save').click()
        except:
            self.writeInFile("ipk_build: can not find save button")
            return 10
        time.sleep(180)

        self.selectImage('core-image-minimal')
        try:
            hob.child('Build image').click()
        except:
            self.writeInFile("ipk_build: can not find build image button")
            return 10
	
	time.sleep(120)
	
	finish = Finish().waitFinish()

        if finish == 20:
            self.writeInFile("ipk image build: failed")
        else:
            self.writeInFile("ipk image build: passed")
        time.sleep(120)
	finish = 1

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
	scriptname=os.path.basename(__file__)
	print "Ending "+scriptname
        #return 10
