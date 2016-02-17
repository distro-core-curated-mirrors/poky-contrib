#!/usr/bin/python
import os
import sys
import time

class IniParser():

    def getValue(self, inifile, section, var):
        if os.path.isfile(inifile):
            with open(inifile, "r") as cfgfile:
                content = cfgfile.read()
            content = content.split("\n")
            for i in xrange (len(content)-1):
                if "["+section+"]" in content[i]:
                    j = i+1
                    while not "[" in content[j]:
                        if var == content[j].split("=")[0]:
                            return content[j].split("=")[1].replace('"','').strip()
                        else:
                            j += 1
            cfgfile.close()

    def setValue(self, inifile, section, var, value):
        if os.path.isfile(inifile):
            with open(inifile, "r") as cfgfile:
                content = cfgfile.read()
            content = content.split("\n")
            for i in xrange (len(content)-1):
                if "["+section+"]" in content[i]:
                    j = i+1
                    while not "[" in content[j]:
                        if var == content[j].split("=")[0]:
                            content[j] = var + '="' + value +'"'
                            break
                        else:
                            j += 1
            cfgfile.close()
            with open(inifile, "w") as cfgfile:
                cfgfile.write("\n".join(content))

#inifile = IniParser()

#print inifile.getValue("test.ini", "section3", "var3")
                