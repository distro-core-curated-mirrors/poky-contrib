import os, time
from dogtail import tree
from dogtail.utils import run
from dogtail.tree import predicate
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

class RecipesStop(Base):

    def stop(self):

        self.selectMachineShort('genericx86')

        try:
            stop = hob.child('Stop')
            stop.click()
        except:
            self.writeInFile("recipe build stop: can not find stop button")
            return 10
        time.sleep(5)

        try:
            comboBox = hob.findChildren(predicate.GenericPredicate(roleName="combo box"))
            if(len(comboBox) > 0):
                self.writeInFile("Recipes stop: passed")
            else:
                self.writeInFile("Recipes stop: failed")
        except:
            pass
	scriptname=os.path.basename(__file__)
	print "Ending "+scriptname
        return 10
