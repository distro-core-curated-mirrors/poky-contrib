import os
from dogtail import tree
import time
from stopHob import StopHob
from startHob import StartHob

#test class. to be deleted

try:
    bitbake = tree.root.application('bitbake')
except:
    print "can not connect to the application"
else:
    try:
        hob = bitbake.child( roleName='frame' )
    except:
        print "can not connect to the application"

class TestFinish:

    def writeInFile(self, error_name):
        f = open('hobResults', 'a')
        f.write('\n' + error_name)
        f.close()

    def analyse(self):
    	try:
    		finish = hob.child("Build new image")
		print "Image is ready"
		return 10
    	except:
		print "Image ready not detected"
		return 20

