#!/usr/bin/python

import os
from dogtail import tree
from time import sleep
import time, getpass
from dogtail.tree import predicate


try:
    bitbake = tree.root.application('bitbake')
except:
    print "can not connect to the application"
else:
    try:
        hob = bitbake.child( roleName='frame' )
    except:
        print "can not connect to the application"
username = getpass.getuser()

class AddLayer:

    def writeInFile(self, error_name):
        f = open('hobResults', 'a')
        f.write('\n' + error_name)
        f.close()

    def selectLayer(self, layers):
        iters = 0
        while iters < 20:
            try:
                layers.child("Add layer").click()
                newLayer = bitbake.dialog('Add new layer')
                break
            except:
                iters += 1
        if iters == 20:
            self.writeInFile("add layer: can not load layer")
            return 10

        try:
            newLayer.child(username).click()
        except:
            self.writeInFile("add layer: can not load layer in home directory - the meta-intel directory has to be in /home/your_user/work/")
            return 10

        iters = 0
        while iters < 20:
            try:
                newLayer.child('work').doubleClick()
                break
            except:
                iters += 1
        if iters == 20:
            self.writeInFile("add layer: can not load layer - can not find work/ directory")
            return 10
        return newLayer

    def layer(self):
        press = 0
        while press < 20:
            try:
                hob.child(name = 'Layers\nAdd support for machines, software, etc.', roleName='push button').click()
                break
            except:
                press += 1

        if press == 20:
            self.writeInFile("add layer: can not find advanced configuration button")
            return 10

        try:
            layers=bitbake.dialog('Layers')
        except:
            self.writeInFile("add layer: can not find layers dialog")
            return 10

        newLayer = self.selectLayer(layers)

        press = 0
        while press < 20:
            try:
                newLayer.child('meta-intel').click()
                break
            except:
                press += 1
        if press == 20:
           self.writeInFile("add layer: can not find meta-intel folder")
           return 10

        try:
            newLayer.child('Open').click()
        except:
            self.writeInFile("add layer: can not find open button")
            return 10

        self.selectLayer(layers)

        try:
            newLayer = bitbake.dialog('Add new layer')
        except:
            self.writeInFile("add layer: can not find add new layer dialog")
            return 10

        try:
            newLayer.child('meta-intel').doubleClick()
        except:
            self.writeInFile("add layer: can not find meta-intel button")
            return 10

        try:
            newLayer.child('meta-sugarbay').click()
        except:
            self.writeInFile("add layer: can not add layer - no sugarbay machine")
            return 10

        try:
            newLayer.child('Open').click()
        except:
            self.writeInFile("add layer: can not add layer - can not find open button")
            return 10

        try:
            layers.child('OK').click()
        except:
            self.writeInFile("add layer: can not add layer - can not find OK button")
            return 10

        time.sleep(20)
        comboBox = hob.findChildren(predicate.GenericPredicate(roleName="combo box"))
        if(len(comboBox) > 1):
            comboBox[1].click()
        else:
            comboBox[0].click()
        try:
            hob.child( name= 'sugarbay', roleName='menu item' ).click()
        except:
            self.writeInFile("addLayer: failed")
        else:
            self.writeInFile("addLayer: passed")
	scriptname=os.path.basename(__file__)
	print "Ending "+scriptname
        return 10
