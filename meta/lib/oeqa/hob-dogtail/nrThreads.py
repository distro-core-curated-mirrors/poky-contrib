#!/usr/bin/python

import os
import time
from dogtail import tree
from dogtail.tree import predicate
import subprocess
from finishBuild import TestFinish
from base import Base
from buildDir import BuildDir

try:
    bitbake = tree.root.application('bitbake')
except:
    print "can not connect to the application"
else:
    try:
        hob = bitbake.child( roleName='frame' )
    except:
        print "can not connect to the application"

class Threads(Base):

    def nrOfChanges(self, a, val):
        spin = a.findChildren(predicate.GenericPredicate(roleName="spin button"))
        if(val == 1):
            spin[0].doubleClick()
            spin[0].typeText("1")

            spin[1].doubleClick()
            spin[1].typeText("1")
        else:
            spin[0].doubleClick()
            spin[0].typeText("8")

            spin[1].doubleClick()
            spin[1].typeText("8")

        try:
            a.child('Save').click()
        except:
            self.writeInFile("nrThreads: can not find save dialog")

    def threads(self):

        try:
            x=hob.child(name = 'Settings')
            x.click()
        except:
            self.writeInFile("nrThreads: can not find settings button")
            return 10

        try:
            y=bitbake.child(name = 'Settings', roleName = 'dialog')
        except:
            self.writeInFile("nrThreads: can not find settings dialog")
            return 10

        self.nrOfChanges(y, 1)
        self.selectMachine('qemuarm')
        self.selectImage('core-image-minimal')

        try:
            hob.child('Build image').click()
        except:
            self.writeInFile("nrThreads: can not find build image button")
            return 10

        time.sleep(60)

	filesh=BuildDir().getPath()+'/file.sh'
	print "Checking thread check script file in current folder"
	if os.path.isfile("file.sh"):
		subprocess.call(['./file.sh'])
	elif os.path.isfile(filesh):
		print "Checking thread check script file in "+filesh
		subprocess.call(['.'+filesh])
	else:
		print "Cannot find thread check script file!"

	hob.child('Stop').click()
        iters = 0
        while iters < 10:
            try:
                stopDialog=bitbake.child(name = "Warning")	
            except:
                hob.child('Stop').click()
                iters += 1
            else:
                break

        if iters == 10:
            self.writeInFile("build_stop_build: can not find stop dialog")
            return 10

        try:
            stop = stopDialog.child('Force stop')
            stop.click()
        except:
            self.writeInFile("nrThreads: can not find force stop button")
            return 10

        time.sleep(20)

        try:
            hob.child('Build new image').click()
        except:
            self.writeInFile("nrThreads: can not find build new image button")
            return 10

        f = open('hobResults', 'a')
        f.write("User could customize threads: ")
        f.close()

        time.sleep(10)
        try:
            x=hob.child(name = 'Settings')
            x.click()
        except:
            self.writeInFile("nrThreads: can not find settings button")
            return 10

        try:
            y=bitbake.child(name = 'Settings', roleName = 'dialog')
        except:
            self.writeInFile("nrThreads: can not find settings dialog")
            return 10

        self.nrOfChanges(y, 8)
        self.selectMachine('qemuarm')
        self.selectImage('core-image-minimal')

        try:
            hob.child('Build image').click()
        except:
            self.writeInFile("nrThreads: can not find build image button")
            return 10

        time.sleep(60)

	filesh=BuildDir().getPath()+'/file.sh'
	print "Checking thread check script file in current folder"
	if os.path.isfile("file.sh"):
		subprocess.call(['./file.sh'])
	elif os.path.isfile(filesh):
		print "Checking thread check script file in "+filesh
		subprocess.call(['.'+filesh])
	else:
		print "Cannot find thread check script file!"

        try:
            stop = hob.child('Stop')
            stop.click()
        except:
            self.writeInFile("nrThreads: can not find stop button")
            return 10

        try:
            stopDialog=bitbake.child(name = "Warning")
        except:
            self.writeInFile("nrThreads: can not find stop dialog")
            return 10

        try:
            stop = stopDialog.child('Force stop')
            stop.click()
        except:
            self.writeInFile("nrThreads: can not find force stop button")
            return 10

        time.sleep(10)
        try:
            bnw = hob.child('Build new image')
            bnw.click()
        except:
            self.writeInFile("nrThreads: can not find build new image button")
            return 10
        time.sleep(15)

Threads().threads()
scriptname=os.path.basename(__file__)
print "Ending "+scriptname
