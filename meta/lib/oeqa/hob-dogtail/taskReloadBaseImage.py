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

class TaskListReload(Base):

    def getTask(self):
        try:
            includedRecipes = hob.child('Package Groups')
            includedRecipes.click()
        except:
            self.writeInFile("task_list_reload: can not find package group button")
            return 10
        List = includedRecipes.findChildren(predicate.GenericPredicate(roleName="table cell"))
        try:
            elem = List[2].name
        except:
            self.writeInFile("task_list_reload: can not find elemnt in list")
            return 10
        return elem

    def verifyListReload(self):
        self.selectMachine('qemux86')
        self.selectImage('core-image-sato')

        try:
            hob.child('Edit image recipe').click()
        except:
            self.writeInFile("task_list_reload: can not find edit image button")
            return 10

        sato = self.getTask()

        try:
            hob.child('Cancel').click()
        except:
            self.writeInFile("task_list_reload: can not find cancel button")
            return 10

        time.sleep(15)

        self.selectImage('core-image-minimal')
        time.sleep(20)

        try:
            hob.child('Edit image recipe').click()
        except:
            self.writeInFile("task_list_reload: can not find edit image button")
            return 10

        minimal = self.getTask()

        try:
            hob.child('Cancel').click()
        except:
            self.writeInFile("task_list_reload: can not find cancel button")
            return 10

        time.sleep(10)
        if sato==minimal:
            self.writeInFile("Task list re-load when base image change: failed")
        else:
            self.writeInFile("Task list re-load when base image change: passed")
        return 10
