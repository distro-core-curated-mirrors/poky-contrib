import os
from dogtail import tree
from dogtail.utils import run
import time
from dogtail.tree import predicate
from finishBuild import TestFinish
from packageSizeShown import PackageSize
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

class BuildImage(Build):

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

    def build(self):
        self.selectMachine('qemux86')
        self.selectImage('core-image-minimal')

        try:
            hob.child('Build image').click()
        except:
            self.writeInFile("image_build: can not find build image button")
            return 10

        self.writeInFile('\n' + "image build: ")

	time.sleep(120)
	#t=TestFinish()
        #finish = t.analyse()
	
	finish = 1
	while (finish % 10 != 0):	
		finish = self.testFinish()

        if finish == 20:
            self.writeInFile("failed")
        else:
            self.writeInFile("passed")
            instance = PackageSize()
            instance.showPackageSize()

        time.sleep(30)
        try:
            bnw = hob.child('Build new image')
            bnw.click()
        except:
            self.writeInFile("image_build: can not find build new image button")
        return 10
