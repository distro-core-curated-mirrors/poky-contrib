import os
from dogtail import tree
from dogtail import predicate
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

class BroughtIn(Base):

    def broughtInBy(self):
        self.selectMachine('qemux86')
        self.selectImage('core-image-minimal')
        try:
            hob.child('Edit image recipe').click()
        except:
            self.writeInFile("brought in by: can not find edit image recipe button")
            return 10
        includedRecipes = hob.child('Included recipes')
        recipesList = includedRecipes.findChildren(predicate.GenericPredicate(roleName="table cell"))

        i=0
        for i in range(len(recipesList)):
            if (recipesList[i].name == 'base-files'):
		print "Clicking recipe list..."
		try:                
			recipesList[i].click()
		except:
			print "Failed to click"
			return 10
                #win = bitbake.findChildren(predicate.GenericPredicate(roleName="dialog"))
	win = bitbake.child('base-files properties')
        if len(win)== 0:
        	self.writeInFile("brought in by: failed")
                return 10
        else:
        	self.writeInFile("brought in by: passed")
		print "Clicking Close..."
	try:
	    	win.child('Close').click()
	except:
		print "Failed to click Close!"
		return 10
	print "Clicking Cancel..."
        try:
            hob.child('Cancel').click()
        except:
            self.writeInFile("brought in by: can not find cancel button")
	    return 10

        time.sleep(5)

	scriptname=os.path.basename(__file__)
	print "Ending "+scriptname
#        return 10
