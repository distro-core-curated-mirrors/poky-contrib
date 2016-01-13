from dogtail import tree
from dogtail.utils import run
from time import sleep
from os import environ, path, remove
import sys, string, os
import subprocess
from subprocess import call
import time
from dogtail.tree import predicate
from base import Base

print "===========Entering removeExtraParam==============="

try:
    bitbake = tree.root.application('bitbake')
except:
    print "can not connect to the application"
else:
    try:
        hob = bitbake.child( roleName='frame' )
    except:
        print "can not connect to the application"

class RemoveExtraParameters(Base):

    def removeParams(self):
        self.selectMachine('qemux86')
        try:
            hob.child(name = 'Settings').click()
        except:
            self.writeInFile("remove extra_params: can not find settings button")
            return 10

        settings = bitbake.dialog('Settings')

        try:
            settings.child(name = 'Others').click()
        except:
            self.writeInFile("remove extra_params: can not find others button")
            return 10

        try:
            settings.child(name = 'PREFERRED_PROVIDER_virtual/libx11').actions['activate'].do()
        except:
            self.writeInFile("remove extra_params: can not find the extra param")
            return 10

        try:
            settings.child(name= 'Remove').click()
        except:
            self.writeInFile("remove extra_params: can not find add button")
            return 10


        try:
            settings.child(name = 'Save').click()
        except:
            self.writeInFile("remove extra_params: can not find save button")
            return 10

        time.sleep(50)
        self.selectImage('core-image-sato')

        try:
            hob.child('Edit image recipe').click()
        except:
            self.writeInFile("remove extra_params: can not find edit image button")
            return 10
        try:
            hob.button('Build packages').click()
        except:
            self.writeInFile("remove extra_params: can not find build packages button")
            return 10
