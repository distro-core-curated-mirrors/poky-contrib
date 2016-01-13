import os
from dogtail import tree
from dogtail.utils import run
import time
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

class Base():

    def writeInFile(self, error_name):
        f = open('hobResults', 'a')
        f.write('\n' + error_name)
        f.close()

    def selectMachine(self, machine):
        iters = 0

        bitbake = tree.root.application('bitbake')
        hob = bitbake.child( roleName='frame' )
        while iters < 30:
            try:
                comboBox = hob.findChildren(predicate.GenericPredicate(roleName="combo box"))
                if(len(comboBox) > 1):
                    comboBox[1].click()
                else:
                    comboBox[0].click()
                break
            except IndexError:
                iters += 1

        press = 0
        while press < 20:
            try:
                hob.child( name= machine, roleName='menu item' ).click()
                break
            except:
                press += 1

        if iters == 20 or press == 20:
            self.writeInFile("select_machine: can not find machine button")
            return 10

        time.sleep(240)

    def selectMachineShort(self, machine):
        iters = 0
	try:
	    bitbake = tree.root.application('bitbake')
	except:
	    print "can not connect to the application"
	else:
	    try:
		hob = bitbake.child( roleName='frame' )
	    except:
		print "can not connect to the application"	
        while iters < 20:
            try:
                comboBox = hob.findChildren(predicate.GenericPredicate(roleName="combo box"))
                if(len(comboBox) > 1):
                    comboBox[1].click()
                else:
                    comboBox[0].click()
                break
            except IndexError:
                iters += 1

        press = 0
        while press < 20:
            try:
                hob.child( name= machine, roleName='menu item' ).click()
                break
            except:
                press += 1

        if iters == 20 or press == 20:
            self.writeInFile("select_machine: can not find machine button")
            return 10

        time.sleep(10)


    def selectImage(self, image):
        iters = 0
	try:
	    bitbake = tree.root.application('bitbake')
	except:
	    print "can not connect to the application"
	else:
	    try:
		hob = bitbake.child( roleName='frame' )
	    except:
		print "can not connect to the application"	
        while iters < 20:
            try:
                comboBox = hob.findChildren(predicate.GenericPredicate(roleName="combo box"))
                comboBox[0].click()
                break
            except IndexError:
                iters += 1

        press = 0
        while press < 20:
            try:
                image = hob.child( name= image, roleName='menu item' )
                image.click()
                break
            except:
                press += 1

        if iters == 20 or press == 20:
            self.writeInFile("select_image: can not find image button")
            return 10

        time.sleep(15)

