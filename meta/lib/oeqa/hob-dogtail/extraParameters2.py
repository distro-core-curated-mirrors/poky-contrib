import os
from dogtail import tree
from dogtail.utils import run
import time
from dogtail.tree import predicate
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

class ExtraParameters(Base):

    def setParams(self):
        #self.selectMachine('qemux86')
        try:
            hob.child(name = 'Settings').click()
        except:
            self.writeInFile("extra_params: can not find settings button")
            return 10

        settings = bitbake.dialog('Settings')

        try:
            settings.child(name = 'Others').click()
        except:
            self.writeInFile("extra_params: can not find others button")
            return 10

        try:
            settings.child(name= 'Add').click()
        except:
            self.writeInFile("extra_params: can not find add button")
            return 10

        settings.child(name = '##KEY##').actions['edit'].do()
        settings.child(name = '##KEY##').typeText("PREFERRED_PROVIDER_virtual/libx11")
        settings.keyCombo("enter")

        settings.child(name = '##VALUE##').actions['edit'].do()
        settings.child(name = '##VALUE##').typeText("libx11-diet")
        settings.keyCombo("enter")

        try:
            settings.child(name = 'Save').click()
        except:
            self.writeInFile("extra_params: can not find save button")
            return 10

        time.sleep(50)
        self.selectImage('core-image-sato')

        try:
            hob.child('Edit image recipe').click()
        except:
            self.writeInFile("extra_params: can not find edit image button")
            return 10
        try:
            hob.button('Build packages').click()
        except:
            self.writeInFile("extra_params: can not find build packages button")
            return 10


ExtraParameters().setParams()
