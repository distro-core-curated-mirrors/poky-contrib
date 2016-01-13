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

try:
    bitbake = tree.root.application('bitbake')
except:
    print "can not connect to the application"
else:
    try:
        hob = bitbake.child( roleName='frame' )
    except:
        print "can not connect to the application"

class MachineChange(Base):

    def machineChange(self):
        self.selectMachine('qemumips')
        self.selectImage('core-image-minimal')

        try:
            hob.child('Edit image recipe').click()
        except:
            self.writeInFile("Recipe list re-load for machine change: can not find recipe reload button")
            return 10

        x = hob.child('Included recipes')
        listaImensa = x.findChildren(predicate.GenericPredicate(roleName="table cell"))

        qemumips = len(listaImensa)
        try:
            hob.child('Cancel').click()
        except:
            self.writeInFile("Recipe list re-load for machine change: can not find cancel button")
            return 10
        time.sleep(10)

        self.selectMachine('qemux86')
        time.sleep(20)
	self.selectImage('core-image-minimal')
	time.sleep(5)
        try:
            hob.child('Edit image recipe').click()
        except:
            self.writeInFile("Recipe list re-load for machine change: can not find recipe reload button")
            return 10

        x = hob.child('Included recipes')
        listaImensa = x.findChildren(predicate.GenericPredicate(roleName="table cell"))

        qemux = len(listaImensa)
        try:
            hob.child('Cancel').click()
        except:
            self.writeInFile("Recipe list re-load for machine change: can not find cancel button")
            return 10
        time.sleep(5)

        if(qemux== qemumips):
            self.writeInFile("Recipe list re-load for machine change: failed")
        else:
            self.writeInFile("Recipe list re-load for machine change: passed")
	scriptname=os.path.basename(__file__)
	print "Ending "+scriptname
        return 10
