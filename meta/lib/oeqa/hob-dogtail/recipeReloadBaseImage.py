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

class BaseImageChange(Base):

    def imageChange(self):
        self.selectMachine('qemux86')
        self.selectImage("core-image-sato")

        try:
            hob.child('Edit image recipe').click()
        except:
            self.writeInFile("Recipe list re-load for base image change: can not find recipe reload button")
            return 10

        x = hob.child('Included recipes')
        listaImensa = x.findChildren(predicate.GenericPredicate(roleName="table cell"))
        try:
            hob.child('Cancel').click()
        except:
            self.writeInFile("Recipe list re-load for base image change: can not find cancel button")
            return 10
        time.sleep(18)

        sato = len(listaImensa)
        self.selectImage('core-image-minimal')
        time.sleep(20)

        try:
            hob.child('Edit image recipe').click()
        except:
            self.writeInFile("Recipe list re-load for base image change: can not find recipe reload button")
            return 10
        x = hob.child('Included recipes')
        minim = x.findChildren(predicate.GenericPredicate(roleName="table cell"))
        try:
            hob.child('Cancel').click()
        except:
            self.writeInFile("Recipe list re-load for base image change: can not find cancel button")
            return 10
        time.sleep(5)

        minimal = len(minim)
        if(sato == minimal):
            self.writeInFile("Recipe list re-load for base image change: failed")
        else:
            self.writeInFile("Recipe list re-load for base image change: passed")

	scriptname=os.path.basename(__file__)
	print "Ending "+scriptname
        return 10
