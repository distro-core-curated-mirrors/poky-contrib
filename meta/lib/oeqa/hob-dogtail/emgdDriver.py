import os
from dogtail import tree
import time
from dogtail.tree import predicate
import getpass
from base import Base
from finish import Finish
from buildDir import BuildDir


currentPath = os.getcwd()

username = getpass.getuser()
#os.chdir('/home/' + username + '/work/m5-rc4/poky/build/conf/')
os.chdir(BuildDir().getPath()+'/poky/build/conf/')
print "Changed location to: "+BuildDir().getPath()+'/poky/build/conf/'

conf = open('local.conf', 'a')
conf.write("\n" +"LICENSE_FLAGS_WHITELIST = \"license_emgd-driver-bin\"")
conf.close()
os.chdir(currentPath)



try:
    bitbake = tree.root.application('bitbake')
except:
    print "can not connect to the application"
else:
    try:
        hob = bitbake.child( roleName='frame' )
    except:
        print "can not connect to the application"

class EmgdDriver(Base):

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

    def selectLayer(self):
        layers = bitbake.dialog("Layers")
        layers.child("Add layer").click()
        newLayer = bitbake.dialog('Add new layer')
        #newLayer.child(username).click()
        newLayer.child('work').doubleClick()
        return newLayer

    def emgd(self):
        iters = 0
        while iters < 100:
            try:
                dialog = hob.child(name = 'Layers\nAdd support for machines, software, etc.', roleName='push button')
                dialog.click()
                break
            except:
                iters += 1

        if iters == 100:
            self.writeInFile("emgd_driver: can not add layer")
            return 10

        newLayer = self.selectLayer()

        try:
            newLayer.child('meta-intel').click()
            newLayer.child('Open').click()
        except:
            self.writeInFile("emgd_driver: can not add layer")

        newLayer = self.selectLayer()
        layers = bitbake.dialog("Layers")
        try:
            newLayer.child('meta-intel').doubleClick()
            newLayer.child('meta-emenlow').click()
            newLayer.child('Open').click()
            layers.child('OK').click()
        except:
            self.writeInFile("emgd_driver: can not add layer")
            return 10
        time.sleep(10)

        self.selectMachine('emenlow')
	time.sleep(120)
        self.selectImage('core-image-sato')
        try:
            hob.child('Build image').click()
        except:
            self.writeInFile("emgd driver: can not find build image button")
            return 10

	time.sleep(180)

	#t=TestFinish()
        #finish = t.analyse()
	
	finish = Finish().waitFinish()
	#finish = self.testFinish()

	time.sleep(240)
        if finish == 20:
            self.writeInFile("emgd driver: failed")
        else:
            self.writeInFile("emgd driver: passed")
        time.sleep(120)
	finish=1
        try:
            bnw = hob.child('Build new image')
            bnw.click()
        except SearchError:
            self.writeInFile("emgd driver: can not find build new image button")
	scriptname=os.path.basename(__file__)
	print "Ending "+scriptname
        return 10
