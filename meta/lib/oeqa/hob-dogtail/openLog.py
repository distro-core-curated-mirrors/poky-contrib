import os, time
from dogtail import tree
from dogtail.utils import run
from dogtail.tree import predicate


try:
    bitbake = tree.root.application('bitbake')
except:
    print "can not connect to the application"
else:
    try:
        hob = bitbake.child( roleName='frame' )
    except:
        print "can not connect to the application"

class ViewLog:

    def openLog(self):

        try:
            log = hob.child('Open log')
            log.click()
        except:
            self.writeInFile("open log: can not find open log button")
            return 10
        gedit = tree.root.application('gedit')
        frames = gedit.findChildren(predicate.GenericPredicate(roleName="frame"))
        for i in range(len(frames)):
            if frames[i].name.find(".log") != -1:
                find = 1
                self.writeInFile("open log: passed")
        if find == 0:
            self.writeInFile("open log: failed")

        time.sleep(40)
        try:
            bnw = hob.child('Build new image')
            bnw.click()
        except SearchError:
            self.writeInFile("open log: can not find build new image button")
        return 10
