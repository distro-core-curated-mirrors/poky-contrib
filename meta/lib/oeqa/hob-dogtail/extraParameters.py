import os
from dogtail import tree
from dogtail.utils import run
import time
from dogtail.tree import predicate
from base import Base
import pyperclip
import time
from finish import Finish

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
	bitbake = tree.root.application('bitbake')
	hob = bitbake.child( roleName='frame' )
	time.sleep(120)
        self.selectMachine('qemux86')
	time.sleep(120)
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
		
	key=settings.child(name = '##KEY##')
        settings.child(name = '##KEY##').doubleClick()
	time.sleep(1)
	settings.child(name = '##KEY##').click()
	time.sleep(1)	
        #settings.child(name = '##KEY##').typeText('PREFERRED_PROVIDER_virtual/libx11')
	pyperclip.copy('PREFERRED_PROVIDER_virtual/libx11')	
	settings.keyCombo("<Control>V")

        settings.child(name = '##VALUE##').doubleClick()
	time.sleep(1)
	settings.child(name = '##VALUE##').click()
	time.sleep(1)
        #settings.child(name = '##VALUE##').typeText("libx11-diet")
	pyperclip.copy('libx11-diet')
	settings.keyCombo("<Control>V")
	time.sleep(1)
	settings.keyCombo("enter")         
	time.sleep(10)

        try:
            settings.child(name = 'Save').click()
        except:
            self.writeInFile("extra_params: can not find save button")
            return 10

        time.sleep(300)
        self.selectImage('core-image-sato')
        try:
	    print "Clicking Build Image"
	    t=str(hob.child('Build image'))
	    try:    
		if t.index('Build') > 0:
                        hob.child('Build image').click()
			print "Clicked Build image button"
		else:
			print "Don't know if clicked the right button"
	    except:
		print "Not the right element!"            
        except:
            self.writeInFile("extra_params: can not find build image button")
            return 10
	

	time.sleep(280)
	
	finish = Finish().waitFinish()

        if finish == 20:
            self.writeInFile("extra parameters: failed")
        else:
            self.writeInFile("extra parameters: passed")
        time.sleep(200)

	finish = 1
        try:
            bnw = hob.child('Build new image')
            bnw.click()
	    time.sleep(10)	
            print "Reverting ExtraParams changes"
	    bitbake = tree.root.application('bitbake')
	    hob = bitbake.child( roleName='frame' )
	    hob.child(name = 'Settings').click()
            settings = bitbake.dialog('Settings')
            settings.child(name = 'Others').click()
            settings.child(name = 'libx11-diet').click()
	    time.sleep(1)
            settings.child(name= 'Remove').click()
	    time.sleep(1)
            settings.child(name = 'Save').click()
	    time.sleep(180)
        except:
            self.writeInFile("extra parameters: can not find build new image button")	
	time.sleep(180)
	scriptname=os.path.basename(__file__)
	print "Ending "+scriptname
        return 10
