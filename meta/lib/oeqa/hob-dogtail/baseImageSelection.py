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

class BaseImage(Base):

    def imageSelection(self):
        self.selectMachine('qemumips')
        self.selectImage('core-image-minimal')

        try:
            hob.child('Edit image recipe').click()
        except:
            self.writeInFile("base image selection: can not find Edit image recipe button")
            return 10

        try:
            recipes = hob.child('Included recipes')
        except:
            self.writeInFile("base image selection: can not find included recipes page")
            return 10

        recipesList = recipes.findChildren(predicate.GenericPredicate(roleName="table cell"))
        if len(recipesList) < 0:
            self.writeInFile("base image selection: failed")
        else:
            self.writeInFile("base image selection: passed")
        try:
            hob.child('Cancel').click()
        except:
            self.writeInFile("base image selection: can not find cancel button")
            return 10
        time.sleep(5)
	scriptname=os.path.basename(__file__)
	print "Ending "+scriptname
        return 10
