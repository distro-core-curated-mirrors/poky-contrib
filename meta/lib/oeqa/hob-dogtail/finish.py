import time
import commands
from dogtail import tree

try:
    bitbake = tree.root.application('bitbake')
except:
    print "can not connect to the application"
else:
    try:
        hob = bitbake.child( roleName='frame' )
    except:
        print "can not connect to the application"

class Finish():

	def waitFinish(self):		
		print "Waiting for build to complete"
		nrprocs=10
		aux=50		
		while (aux > 0):		
			nrprocs = commands.getoutput("ps aux | grep bitbake | wc -l")
			if (int(nrprocs) < 6):
				aux = aux-1
			else:
				aux = 30
			time.sleep(10)
		
                try:
			hob.child('Build new image')
			print "Image build complete"		
		except:
	                hob.child('File a bug')
			print "Image build failed"
        	        self.writeInFile("finish_build: found a bug")
		time.sleep(60)
		return 10		










''' Old version
		print "Waiting for build to complete"
		nrprocs=10
		aux=50		
		while (aux > 0):		
			while (int(nrprocs) > 5):
				nrprocs = commands.getoutput("ps aux | grep bitbake | wc -l")
				#print nrprocs
				time.sleep(10)
			time.sleep(10)
			aux = aux-1
		print "Image build complete"
		time.sleep(60)
		return 10		
'''
				
