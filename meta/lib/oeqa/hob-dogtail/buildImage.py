import os
from dogtail import tree
from dogtail.utils import run
import time
from dogtail.tree import predicate
from finishBuild import TestFinish
from packageSizeShown import PackageSize
from base import Base

print "===========Entering buildImage==============="
try:
    bitbake = tree.root.application('bitbake')
except:
    print "can not connect to the application"
else:
    try:
        hob = bitbake.child( roleName='frame' )
    except:
        print "can not connect to the application"

class BuildImage(Base):

    def build(self):
        self.selectMachine()
        self.selectImage()

        try:
            hob.child('Build image').click()
        except:
            self.writeInFile("image_build: can not find build image button")
            return 10

        self.writeInFile('\n' + "image build: ")

        t=TestFinish()
        finish = t.analyse()
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
