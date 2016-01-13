#!/usr/bin/python

import os
from sys import exit

if "DISPLAY" not in os.environ:
	print "Error! DISPLAY environment variable is not set! (ex: export DISPLAY=:0)"
	exit(1)

from startHob import StartHob
import time

StartHob().cleanBuild()

try:
	print "Starting Hob..."	
	StartHob().start()
	time.sleep(60)
except:
	print "Fatal! Failed to start Hob!"
	exit(1)

#from buildStopBuild import BuildStop 
#from ipkBuild import IpkImageBuild  
#from debBuild import DebImageBuild  
#rom rpmBuild import RpmImageBuild
#from multiplePackageBuild import MultiplePackage
#from extraParameters import ExtraParameters 
from changeDistro import ChangeDistro 
from nonGPLv3Build import NonGPL 
#from buildToolchain import BuildToolchain
from emgdDriver import EmgdDriver
#from stopHob import StopHob

print "Starting BuildStop"
BuildStop().buildStopBuild()
print "Starting IPK"
IpkImageBuild().ipkSelect()
print "Starting DEB"
DebImageBuild().debBuild()
print "Starting RPM"
RpmImageBuild().rpmSelect()
print "Starting MultiplePackage"
MultiplePackage().multiplePackages()
print "Starting ChangeDistro"
ChangeDistro().distro() 
print "Starting Toolchain"
BuildToolchain().toolchain()
print "Starting NonGPL"
NonGPL().nonGPL()
print "Starting ExtraParameters"
ExtraParameters().setParams()
print "Starting EmgdDriver (partial)"
EmgdDriver().emgd()
print "All tests completed"
StopHob().stop()
