#!/usr/bin/env python

# to generate random numbers
import random
# useful operating system functions
import os
# useful system functions
import sys
# for searching
import re
'''
This parses the output of the container based tester. 
It generates some useful(?) statistics

'''
# Verbosity level. raised by passing in -v or -v -v 
gVerbose=0
# usually need random numbers for simulation
random.seed(os.urandom(24))

# usage lets you run python AlexExample.py -h so it can tell you what the
# possible arguments are and what it does.
def usage():
    print """
    Usage: ParseContainers.py  <Options>
    Options:
     -d --dir=<directory>                        - defaults to .
     -v --verbose                                - verbose, can specify multiple -v -v -v 
     -h --help                                   - prints this

    I analyze the container testing results in a given directory.

    """
    sys.exit(0)

# naa just do a series of functions.
class ErrorType(object):
    def __init__(self,rootDir="."):
        self.errorPresent=False
        self.rootDir=rootDir
        self.patterns=[]
        self.count=0
    def AddErrorPair(self,errorStr,filename='stdout'):
        p=re.compile(errorStr)
        self.patterns.append({'pattern':p,'filename':filename})
    def RecursiveWalk(self,folder):
        for folderName, subfolders, filenames in os.walk(folder):
            if subfolders:
                for subfolder in subfolders:
                    self.RecursiveWalk(subfolder)
                print('\nFolder: ' + folderName + '\n')
                for filename in filenames:
                    for p in self.patterns:
                        if p['filename'] in filename:
                            print (" I care about this file=%s\n" % (filename))
                        else:
                            print (" I DO NOT care about this file=%s\n" % (filename))
                    


def getStartupTimes(rootDir,dir):
    testDir=rootDir+"/"+dir+"/"+"testimage"
    print "getStartupTimes:testDir=%s"%testDir
    patternKernel=re.compile(".*Startup finished in (\d+)\.(\d+)s \(kernel\).*")
    #patternKernel=re.compile(".*Startup finished in.*")
    for dirName,subdirList,fileList in os.walk(testDir):
        for f in fileList:
            if "ssh_target_log." in f:
                print "getStartupTimes: f=%s"%f
                filename=testDir+"/"+f
                f=open(filename,'r')
                txt = f.read()
                f.close()
                mKernel = patternKernel.search(txt)
                if mKernel:
                    print "mKernel num groups=%d"%len(mKernel.groups())
                    print "group0 = ",mKernel.group(0)
                    for g in mKernel.groups():
                        print "mKernalall = ",g

def isTestDir(rootDir,dir):
    return True if "testrun" in dir else False

def isFailDir(rootDir,dir):
    return True if "-failure" in dir else False



def isSimpleRegex(rootDir,dir,regex=".*"):
    pattern =re.compile(regex,re.MULTILINE)

    if "-failure" in dir:
        filename = rootDir+"/"+dir+"/stdout"
        if gVerbose:
            print "isSimpleRegex:%s"%filename
        f=open(filename,'r')
        txt = f.read()
        f.close()
        m = pattern.search(txt)
        if m:
            if gVerbose:
                print "Group0 = [%s]"%m.group(0)
                print "m=",m.group(0)
            return True
        else:
            return False
    else:
        return False


# This needs 3 separate patterns to appear to be true
def isBlutoothWpaAvahiTimeout(rootDir,dir):
            

    pattern1 =re.compile('^\|.*bluetooth.*loaded failed failed Bluetooth service$',re.MULTILINE)
    pattern2 =re.compile('^\|.*wpa_supplicant.*loaded failed failed WPA supplicant$',re.MULTILINE)
    pattern3 =re.compile('^\|.*Job for avahi-daemon.*failed because a timeout was exceeded.*for details\.$',re.MULTILINE)

    if "-failure" in dir:
        filename = rootDir+"/"+dir+"/stdout"
        if gVerbose:
            print "isBlutoothWpaAvahiTimeout:%s"%filename
        f=open(filename,'r')
        txt = f.read()
        f.close()
        m1 = pattern1.search(txt)
        m2 = pattern2.search(txt)
        m3 = pattern3.search(txt)
        if m1 and m2 and m3:
            if gVerbose:
                print "M1Group0 = [%s]"%m1.group(0)
                print "M2Group0 = [%s]"%m2.group(0)
                print "M3Group0 = [%s]"%m3.group(0)

            getStartupTimes(rootDir,dir)
            return True
        else:
            return False
    else:
        return False


def HandleTests(tests,rootDir):
    for dirName,subdirList,fileList in os.walk(rootDir):
        print "dirname=",dirName
        for sub in subdirList:
            for t in tests:
                if t.has_key('regex'):
                    if t['test'](rootDir,sub,regex=t['regex']):
                        t['count']+=1
                        t['dirlist'].append(sub)
                else:
                    if t['test'](rootDir,sub):
                        t['count']+=1
                        t['dirlist'].append(sub)
        break
    return 


def PrintStats(tests):


    for t in tests:
        if "Total" in t['name']:
            totalRuns=t['count']
        if "Failures" in t['name']:
            totalFailures=t['count']
            uncharacterizedDirs=t['dirlist']
    for t in tests:
        per = t['count']*100.0/totalRuns
        if "Total" in t['name']:
            continue
        if "Failures" in t['name']:
            continue
        print "test %s has a count of %d for a percentage of %02.2f%%" % (t['name'],t['count'],per)
        totalFailures-=t['count']
        u=[x for x in uncharacterizedDirs if x not in t['dirlist']]
        uncharacterizedDirs=u

    print "Had %d uncharacterized Failures!"%totalFailures
    print "len=%d for uncharacterizedDirs=%s!"%(len(uncharacterizedDirs),uncharacterizedDirs)
    return




##### Main start of program #####

if __name__ == "__main__":
    # a python module that helps you parse arguments passed in to the script.
    # the odd looking line:
    #                       (options, argv) = getopt.getopt(sys.argv[1:],
    #                       'hvb:r:', ["help", "verbose", "base=","range="])
    # says we have 4 options.
    # -h or --help -- NO arguments
    # -v or --verbose -- NO arguments
    # -b or --base    -- ONE argument
    # -r or --range   -- ONE argument
    import getopt
    try:
        (options, argv) = getopt.getopt(sys.argv[1:],
                                        'hvd:', ["help", "verbose", "dir="])
    except Exception, e:
        print e
        usage()
    
    # default values
    rootDir="."

    for (k,v) in options:
        if k in ('-h', '--help'):
            usage()
        elif k in ('-v', '--verbose'):
            gVerbose += 1
        elif k in ('-d', '--dir'):
            rootDir = v
        else:
            print "I didn't understand that"
            usage()

    # test definitions
    tests = [{"name":"kernelPanic",
             "test":isSimpleRegex,
              "regex":'^Kernel panic.*Attempted.*$',
              "dirlist":[],
              "count":0
          },
             {"name":"XServerFail",
             "test":isSimpleRegex,
              "regex":'^\|.*xserver-nodm.*loaded failed failed Xserver.*display manager$',
              "dirlist":[],
              "count":0
          },             
             {"name":"SystemdListUnitTimeout",
             "test":isSimpleRegex,
              "regex":'^\|.*Failed to list unit files: Connection timed out$',
              "dirlist":[],
              "count":0
          },             
             {"name":"BluetoothWpaFail-AvahiTimeout",
             "test":isBlutoothWpaAvahiTimeout,
              "dirlist":[],
              "count":0
          },             



             {"name":"Failures",
             "test":isFailDir,
              "dirlist":[],
              "count":0
          },
             {"name":"Total",
             "test":isTestDir,
              "dirlist":[],
              "count":0
          }
         ]

             

    HandleTests(tests,rootDir)
    PrintStats(tests)




else:
    # being imported as a module
    print "Module time!"
