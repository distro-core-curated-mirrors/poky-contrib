#!/usr/bin/python

from ipkBuild import IpkImageBuild
from stopHob import StopHob
from startHob import StartHob
import time


print "Starting Hob..."
StartHob().start()
print "Waiting 60 seconds..."
time.sleep(60)
print "Stopping Hob..."
StopHob().stop()
print "Waiting 20 seconds..."
time.sleep(20)
print "Starting Hob..."
StartHob().start()
print "Waiting 60 seconds..."
time.sleep(120)
print "Starting IPK..."
IpkImageBuild().ipkSelect()
