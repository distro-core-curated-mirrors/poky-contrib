import os
from dogtail import tree
from dogtail.tree import predicate
from time import sleep
import time
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

class AddRecipe(Base):

    def recipe(self):
        self.selectMachine('qemux86')
        self.selectImage('core-image-sato')

        press = 0
        while press < 20:
            try:
                hob.child('Edit image recipe').click()
                x = hob.child('Included recipes')
                break
            except:
                press += 1

        if press == 20:
            self.writeInFile("add recipe: can not find edit image button")
            return 10

        listaImensa = x.findChildren(predicate.GenericPredicate(roleName="table cell"))

        i=0
        for i in range(len(listaImensa)):
            if listaImensa[i].name == 'acl':
                try:
                    listaImensa[i+3].actions['toggle'].do()
                    break
                except:
                    pass
        press = 0
        while press < 20:
            try:
                hob.child('All recipes').click()
                break
            except:
                press += 1

        if press == 20:
            self.writeInFile("add recipe: can not find all recipes button")
            return 10

        y = hob.child('All recipes')
        listR = y.findChildren(predicate.GenericPredicate(roleName="table cell"))
        i=0
        for i in range(len(listR)):
            if listR[i].name == 'libevent':
                try:
                    listR[i+3].actions['toggle'].do()
                    break
                except:
                    pass
        time.sleep(20)
        press = 0
        while press < 20:
            try:
                hob.child('Build packages').click()
                break
            except:
                press += 1

        if press == 20:
            self.writeInFile("add recipe: can not find build packages button")
            return 10

