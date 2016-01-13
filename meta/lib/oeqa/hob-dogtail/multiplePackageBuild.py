import os, time
from dogtail import tree
from dogtail.utils import run
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

class MultiplePackage(Base):

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

    def multiplePackages(self):
        self.selectMachine('qemux86')
        self.selectImage('core-image-minimal')
        press = 0
        while press < 20:
            try:
                selectDistro = hob.child(name = 'Advanced configuration\nSelect image types, package formats, etc', roleName='push button')
		print "Selecting distro"
		print selectDistro
                selectDistro.click()
                break
            except:
                press += 1
        if press == 20:
            self.writeInFile("multiple_package_build: can not find advanced configuration button")
            return 10

        press = 0
        while press < 20:
            try:
                advConfig=bitbake.dialog('Advanced configuration')
		print "Clicking Output in advanced configuration"
		print advConfig.child('Output')
                changeTab=advConfig.child('Output').click()
                break
            except:
                press += 1
        if press == 20:
            self.writeInFile("multiple_package_build: can not find output button")
            return 10

        otherPackage = advConfig.findChildren(predicate.GenericPredicate(roleName="check box"))
#	for x in range(0,30):
#		print otherPackage[x]
        try:
	    print "Ckecking deb"
	    t=str(otherPackage[28])
#	    t = t[13:-1]
	    try:    
		if t.index('deb') > 0:
		        otherPackage[28].click()
			print "Clicked deb checkbox"
		else:
			print "Don't know if checked the right checkbox"
	    except:
		print "Not the right element!"
        except:
            self.writeInFile("multiple_package_build: can not find package button")
            return 10

        try:
	    print "Checking ipk"
	    t=str(otherPackage[29])
	    try:    
		if t.index('ipk') > 0:
                        otherPackage[29].click()
			print "Clicked ipk checkbox"
		else:
			print "Don't know if checked the right checkbox"
	    except:
		print "Not the right element!"
        except:
            self.writeInFile("multiple_package_build: can not find package button")
            return 10

        try:
	    print "Clicking Save"
	    print advConfig.child('Save')
	    t=str(advConfig.child('Save'))
	    try:    
		if t.index('Save') > 0:
                        advConfig.child('Save').click()
			print "Clicked Save button"
		else:
			print "Don't know if clicked the right button"
	    except:
		print "Not the right element!"            
        except:
            self.writeInFile("multiple_package_build: can not find save button")
            return 10

        time.sleep(50)

        try:
	    print "Clicking Build Image"
	    t=str(hob.child('Build image'))
	    try:    
		if t.index('Build') > 0:
                        hob.child('Build image').click()
			print "Clicked Build image button"
		else:
			print "Don't know if clicked the right button"
	    except:
		print "Not the right element!"            
        except:
            self.writeInFile("multiple_package_build: can not find build image button")
            return 10

	time.sleep(120)

	#t=TestFinish()
        #finish = t.analyse()
	
	finish = Finish().waitFinish()
	#finish = self.testFinish()

        if finish == 20:
            self.writeInFile("multiple package build: failed")
        else:
            self.writeInFile("multiple package build: passed")
        time.sleep(30)
	finish=1
        try:
            bnw = hob.child('Build new image')
	    print "Clicking Build new image"
	    t=str(bnw)
	    try:    
		if t.index('Build') > 0:
                        bnw.click()
			print "Clicked Build new image button"
		else:
			print "Don't know if clicked the right button"
	    except:
		print "Not the right element!"        
        except SearchError:
            self.writeInFile("multiple package : can not find build new image button")
	scriptname=os.path.basename(__file__)
	print "Ending "+scriptname
        return 10
