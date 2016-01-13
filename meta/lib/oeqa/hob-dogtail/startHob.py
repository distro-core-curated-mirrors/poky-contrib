import os
import getpass
from buildDir import BuildDir

class StartHob:

    def start(self):
	curdir=os.path.dirname(os.path.abspath(__file__))
	hobdir=BuildDir().getPath()+'/poky'
	print "Starting hob from "+hobdir+"\n"
        username = getpass.getuser()
        os.chdir(hobdir)
        os.system('. ./oe-init-build-env; hob &')
	print "Hob restared. \nGoing back to "+curdir+"\n"
	os.chdir(curdir)

    def cleanBuild(self):
	curdir=os.path.dirname(os.path.abspath(__file__))
	hobdir=BuildDir().getPath()+'/poky'
	print "Deleting build folder...\n"
        os.chdir(hobdir)
        os.system('rm -rf build')
	print "Build folder deleted. \nGoing back to "+curdir+"\n"
	os.chdir(curdir)
