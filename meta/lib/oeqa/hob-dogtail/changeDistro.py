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

class ChangeDistro(Base):

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


    def distro(self):
        self.selectMachine('qemux86')
        press = 0
        while press < 20:
            try:
                selectDistro = hob.child(name = 'Advanced configuration\nSelect image types, package formats, etc', roleName='push button')
                selectDistro.click()
                break
            except:
                press += 1

        if press == 20:
            self.writeInFile("change_distro: can not find advanced configuration button")
            return 10

        press = 0
        while press < 20:
            try:
                advConfig=bitbake.dialog('Advanced configuration')
                break
            except:
                press += 1

        if press == 20:
            self.writeInFile("change_distro: can not find output button")
            return 10

        try:
            distroType = advConfig.findChildren(predicate.GenericPredicate(roleName="combo box"))
            distroType[0].click()
        except:
            self.writeInFile("change_distro: can not find change distro button")
            return 10
        try:
            selectPackageType = advConfig.child(name='poky-lsb')
            selectPackageType.click()
        except:
            self.writeInFile("change_distro: can not find poky lsb button")
            return 10
        try:
            advConfig.child('Save').click()
        except:
            self.writeInFile("change_distro: can not find save button")
            return 10
        time.sleep(100)

        self.selectImage('core-image-minimal')
        try:
            hob.child('Build image').click()
        except:
            self.writeInFile("change_distro: can not find build image button")
            return 10

 	time.sleep(120)

	#t=TestFinish()
        #finish = t.analyse()
	
	Finish().waitFinish()
	finish = self.testFinish()


        if finish == 20:
            self.writeInFile("change_distro: failed")
        else:
            self.writeInFile("change_distro: passed")
        time.sleep(30)
	finish=1
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

        #deselect option to not mess with next tests
	self.selectMachine('qemux86')
        press = 0
        while press < 20:
            try:
                selectDistro = hob.child(name = 'Advanced configuration\nSelect image types, package formats, etc', roleName='push button')
                selectDistro.click()
                break
            except:
                press += 1

        if press == 20:
            self.writeInFile("change_distro: can not find advanced configuration button")
            return 10

        press = 0
        while press < 20:
            try:
                advConfig=bitbake.dialog('Advanced configuration')
                break
            except:
                press += 1

        if press == 20:
            self.writeInFile("change_distro: can not find output button")
            return 10

        try:
            distroType = advConfig.findChildren(predicate.GenericPredicate(roleName="combo box"))
            distroType[0].click()
        except:
            self.writeInFile("change_distro: can not find change distro button")
            return 10
        try:
            selectPackageType = advConfig.child(name='poky')
            selectPackageType.click()
        except:
            self.writeInFile("change_distro: can not find poky lsb button")
            return 10
        try:
            advConfig.child('Save').click()
        except:
            self.writeInFile("change_distro: can not find save button")
            return 10
	scriptname=os.path.basename(__file__)
	print "Ending "+scriptname
        time.sleep(100)
