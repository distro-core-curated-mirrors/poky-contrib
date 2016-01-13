import os
from dogtail import tree
import time
from stopHob import StopHob
from startHob import StartHob

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
        iters = 0
        while iters < 25:
            iters += 1
            try:
                #finish = hob.child(name = "Your image is ready", roleName = "label")
		finish = hob.child("Build new image")
            except:
                try:
                    hob.child('File a bug')
                    self.writeInFile("finish_build: found a bug")
                except:
                    try:
                        hob.child('Step 2 of 2: Edit packages')
                    except:
                        pass
                    else:
                        return 10
                else:
                    return 20

                try:
                    win = bitbake.findChildren(predicate.GenericPredicate(roleName="dialog"))
                    self.writeInFile("finish_build: found the dialog")
                except:
                    pass
                else:
                    if len(win)>0:
                        dialog=win[0]
                        try:
                            dialog.child('Close').click()
                        except:
                            pass
                        return 20
            else:
                return 10

        if iters == 25:
            stopH=StopHob()
            stopH.stop()
            self.writeInFile("finish_build: stop hob")

            time.sleep(40)

            startH=StartHob()
            startH.start()
            self.writeInFile("finish_build: start hob")
            return 20
