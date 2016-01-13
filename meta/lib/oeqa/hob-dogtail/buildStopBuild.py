import os
from dogtail import tree
from dogtail.utils import run
import time
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

class BuildStop(Base):

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
				return 20


    def buildStopBuild(self):
        self.selectMachine('qemux86')
	time.sleep(140)
        self.selectImage('core-image-minimal')

        try:
            hob.child('Build image').click()
        except:
            self.writeInFile("build_stop_build: can not find build image button")
            return 10

        time.sleep(120)
        stop = hob.child('Stop')
        stop.click()

        iters = 0
        while iters < 10:
            try:
                stopDialog=bitbake.child('Warning')
            except:
                stop = hob.child('Stop')
                stop.click()
                iters += 1
            else:
                break
        if iters == 10:
            self.writeInFile("build_stop_build: can not find stop dialog")
            return 10

        try:
            stopDialog.child('Force stop').click()
        except:
            self.writeInFile("build_stop_build: can not find force stop button")
            return 10

        time.sleep(10)

        try:
            bnw = hob.child('Build new image')
            bnw.click()
        except:
            self.writeInFile("stop build during image building: can not find build new image button")
        else:
            self.writeInFile("stop build during image building: passed first build")
            self.selectMachine('qemumips')
            self.selectImage('core-image-minimal')
            try:
                hob.child('Build image').click()
            except:
                self.writeInFile("build_stop_build: can not find build image button")
                return 10

	    #t=TestFinish()
            #finish = t.analyse()
	
	    Finish().waitFinish()
	    finish = self.testFinish()


            if finish == 20:
                self.writeInFile("stop build during image building: failed build")
            else:
                time.sleep(30)
                self.writeInFile("stop build during image building: passed second build")
                try:
                    bnw = hob.child('Build new image')
                    bnw.click()
                except:
                    self.writeInFile("build_stop_build: can not find build image button")
                    return 10
        return 10
