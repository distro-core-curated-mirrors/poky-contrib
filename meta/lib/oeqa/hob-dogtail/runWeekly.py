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
#	os.system('export DISPLAY=:0')
	StartHob().start()
	time.sleep(60)
except:
	print "Fatal! Failed to start Hob!"
	exit(1)

from recipesStop import RecipesStop
from addLayer import AddLayer
from baseImageSelection import BaseImage
from recipeReloadBaseImage import BaseImageChange
from recipeReloadMachine import MachineChange 
## from taskReloadBaseImage import TaskListReload #not working
from noNative import NoNativeRecipes
from broughtInBy import BroughtIn
from nrThreads import Threads
from stopHob import StopHob

try:
	print "Starting NoNatives"
	NoNativeRecipes().searchNativeRecipes()
except:
	print "No Natives failed"
	StopHob().stop()
	time.sleep(20)
	StartHob().start()
	time.sleep(60)
try:
	print "Starting BaseImageChange"
	BaseImageChange().imageChange()
except:
	print "Base Image Change failed"
	StopHob().stop()
	time.sleep(20)
	StartHob().start()
	time.sleep(60)
try:
	print "Starting BroughtInBy"
	BroughtIn().broughtInBy()
except:
	print "Brought In By failed"
	StopHob().stop()
	time.sleep(20)
	StartHob().start()
	time.sleep(60)

try:
	print "Starting MachineChange"
	MachineChange().machineChange()
except:
	print "Machine Change failed"
	StopHob().stop()
	time.sleep(20)
	StartHob().start()
	time.sleep(60)
try:
	print "Starting BaseImage"
	BaseImage().imageSelection()
except:
	print "Image Selection failed"
	StopHob().stop()
	time.sleep(20)
	StartHob().start()
	time.sleep(60)
try:
	print "Starting AddLayer"
	AddLayer().layer()
except:
	print "Add Layer failed"
	StopHob().stop()
	time.sleep(20)
	StartHob().start()
	time.sleep(60) 
try:
	print "Starting RecipesStop"
	RecipesStop().stop()
except:
	print "Recipes Stop failed"
	StopHob().stop()
	time.sleep(20)
	StartHob().start()
	time.sleep(60)
#TaskListReload().verifyListReload()
try:
	print "Starting ThreadCount"
	Threads().threads() 
except:
	print "Count Threads failed" 
	StopHob().stop()
	time.sleep(20)
	StartHob().start()
	time.sleep(60)

print "All tests completed"

