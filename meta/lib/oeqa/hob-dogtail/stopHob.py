import os, re, time
import getpass
from dogtail import *

class StopHob:

    def writeInFile(self, error_name):
        f = open('hobResults', 'a')
        f.write('\n' + error_name)
        f.close()

    def lines(self):
        f = open('stopHob.txt', 'r')
        lines=f.readlines()
        num_lines = len([l for l in lines if l.strip(' \n') != ''])
        f.close()
        if num_lines == 2:
            return True
        else:
            return False

    def check_window(self):
        try:
            bitbake = tree.root.application('bitbake')
        except:
            return False
        else:
            try:
                win = bitbake.findChildren(predicate.GenericPredicate(roleName="dialog"))
                dialog=win[0]
            except IndexError:
                self.writeInFile("stop_hob: no dialog window")
                return False
            else:
                try:
                    dialog.child('Close').click()
                except:
                    self.writeInFile("stop_hob: can not find close button")
                else:
                    return True

    def stop(self):
        username = getpass.getuser()
        os.system('echo '' > stopHob.txt')
        os.system('ps aux | grep -i [h]ob >stopHob.txt')
        f = open('stopHob.txt', 'r')
        finished=False
        for line in f:
            #print line
            if line.find('color') == -1 or line.find('stopHob.txt') == -1:
                splitline=re.match(username+'\s+(\d+).*',line)
                pid = splitline.group(1)
                os.system('kill -9 ' +pid)
                if self.lines() == True:
                    break
                if self.check_window() == True:
                    break
                else:
                    os.system('echo '' > stopHob.txt')
                    os.system('ps aux |grep -i hob > stopHob.txt')
                    time.sleep(3)
        f.close()
