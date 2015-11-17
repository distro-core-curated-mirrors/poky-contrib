#!/usr/bin/env python

# import cProfile

# to generate random numbers
import random
# useful operating system functions
import os
# useful system functions
import sys
# for searching
import re
import copy
# so it is not sooo slow that Randy gives up
import Queue
'''
This parses the output of the container based tester.
It generates some useful(?) statistics

'''
# Verbosity level. raised by passing in -v or -v -v
gVerbose=0
gDoTimes=False
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
           1 -v -> more data info  like directories
           2 -v or more -> debugging
     -c --cores=#                                - num threads to use defaults to #cores
     -t                                          - also does times, takes longer
     -h --help                                   - prints this

    I analyze the container testing results in a given directory.

    """
    sys.exit(0)


# This allows me to extract the kernel boot time. on reflection
# I think the total time is fine to start with. We can use this
# as a guide if I want to break it up later.
# unused!
def getKernelBootTime(rootDir,dir):
    testDir=rootDir+"/"+dir+"/"+"testimage"
    patternKernel=re.compile(".*Startup finished in (\d+)\.(\d+)s \(kernel\).*")
    for dirName,subdirList,fileList in os.walk(testDir):
        for f in fileList:
            if "ssh_target_log." in f:
                filename=testDir+"/"+f
                f=open(filename,'r')
                txt = f.read()
                f.close()
                mKernel = patternKernel.search(txt)
                if mKernel:
                    if len(mKernel.groups()) == 2:
                        kernelBooTime = (float)(mKernel.group(1)) + (float)(mKernel.group(2))/1000.0
    try:
        return kernelBootTime
    except NameError:
        return 0.0




# returns the sum of kernel and user boot time
def getTotalBootTime(rootDir,dir):
    testDir=rootDir+"/"+dir+"/"+"testimage"
    totalBootTime=0.0
    if gVerbose >=3:
        print "getTotalBoot:testDir=%s"%testDir

    patternBootMin=re.compile(".*Startup finished in.*\(kernel\).*\= (\d+)min (\d+)\.(\d+)s.*")
    patternBootSec=re.compile(".*Startup finished in.*\(kernel\).*\= (\d+)\.(\d+)s.*")
    #patternKernel=re.compile(".*Startup finished in (\d+)\.(\d+)s \(kernel\).*")

    for dirName,subdirList,fileList in os.walk(testDir):
        for f in fileList:
            if "ssh_target_log." in f:
                #print "getStartupTimes: f=%s"%f
                filename=testDir+"/"+f
                f=open(filename,'r')
                txt = f.read()
                f.close()
                mBootMin = patternBootMin.search(txt)
                if mBootMin:
                    if gVerbose >=3:
                        print "mBootMin num groups=%d"%len(mBootMin.groups())
                        print "group0 = ",mBootMin.group(0)
                    if len(mBootMin.groups()) == 3:
                        totalBootTime = (float)(mBootMin.group(1))*60.0+(float)(mBootMin.group(2)) + (float)(mBootMin.group(3))/1000.0
                        if gVerbose >=3:
                            print "total time as float = %f" % totalBootTime
                else:
                    # bootmin failed. either we booted in < 1 min or didn't boot at all
                    mBootSec = patternBootSec.search(txt)
                    if mBootSec:
                        if gVerbose >=3:
                            print "mBootSec num groups=%d"%len(mBootSec.groups())
                            print "group0 = ",mBootSec.group(0)
                        if len(mBootSec.groups()) == 2:
                            totalBootTime = (float)(mBootSec.group(1)) + (float)(mBootSec.group(2))/1000.0
                            if gVerbose >=3:
                                print "total time as float = %f" % totalBootTime

    #try:
    return totalBootTime
    #except NameError:
    #    return 0.0



def getStartupTime(rootDir,dir):
    #    bootTime = getTotalBootTime(rootDir,dir)
    bootTime = getTotalBootTime(rootDir,dir)
    return bootTime


def isTestDir(rootDir,dir):

    if "testrun" in dir or "container-" in dir:
        return True
    else:
        print "dir NOT testrun = ",dir
        False

def isFailDir(rootDir,dir):
    return True if "-failure" in dir else False

def isSuccessDir(rootDir,dir):
    return False if "-failure" in dir else True




def isSimpleRegex(rootDir,dir,regex=".*"):
    pattern =re.compile(regex,re.MULTILINE)

    if "-failure" in dir:
        filename = rootDir+"/"+dir+"/stdout"
        if gVerbose>=3:
            print "isSimpleRegex:%s"%filename
        f=open(filename,'r')
        txt = f.read()
        f.close()
        m = pattern.search(txt)
        if m:
            if gVerbose>=3:
                print "Group0 = [%s]"%m.group(0)
                print "m=",m.group(0)
            return True
        else:
            return False
    else:
        return False



# generic avahi failure handler. grabs the sad systemd guys and then
# uses the passed in regex to determine why avahi failed
def isServicesFailAvahi(rootDir,dir,whichAvahis,data={}):

    patternGeneric=re.compile('^\|\W+(\w+)\.service.*loaded failed failed .*',re.MULTILINE)
    pattern1 =re.compile('^\|.*bluetooth.*loaded failed failed Bluetooth service$',re.MULTILINE)
    pattern2 =re.compile('^\|.*wpa_supplicant.*loaded failed failed WPA supplicant$',re.MULTILINE)
    patternAvahi=[]
    for reg in whichAvahis:
        patternAvahi.append(re.compile(reg,re.MULTILINE))
    #patternAvahi2 =re.compile('.*systemd.*avahi-daemon\.service\: Failed with result.*timeout.*',re.MULTILINE)

    if "-failure" in dir:
        filename = rootDir+"/"+dir+"/stdout"
        if gVerbose>=3:
            print "isServicesFailAvahiTimeout:%s"%filename
        f=open(filename,'r')
        txt = f.read()
        f.close()

        iter = patternGeneric.finditer(txt)
        l=[]
        for q in iter:
            l.append(q.group(1))


        #if len(l)>0 and (mAvahi or mAvahi2):
        found=False
        if len(l)>0:
            # you can pass in a set of regexs for the avahi part,
            # return false if none of them match
            for p in patternAvahi:
                if p.search(txt):
                    found=True
            if not found:
                return False
            data[dir]=l
            if gVerbose>=3:
                print "the following systemd services failed: ",l
            return True
        else:
            return False
    else:
        return False

# avahi fails for a timeout
def isServicesFailAvahiTimeout(rootDir,dir,data={}):
    return isServicesFailAvahi(rootDir,dir,['^\|.*Job for avahi-daemon.*failed because a timeout was exceeded.*for details\.$',
                                            '.*systemd.*avahi-daemon\.service\: Failed with result.*timeout.*'],data)
# avahi fails for an exit
def isServicesFailAvahiExit(rootDir,dir,data={}):
    return isServicesFailAvahi(rootDir,dir,['.*systemd.*avahi-daemon\.service\: Failed with result.*exit-code.*'],data)

def HandleTests(tests,rootDir):
    for dirName,subdirList,fileList in os.walk(rootDir):
        dirCount=0
        for sub in subdirList:
            if not ("testrun" in sub or "container-" in sub):
                continue
            percentDone=100*dirCount/len(subdirList)
            sys.stdout.write("Processing progress: %d%%   \r" % percentDone)
            sys.stdout.flush()
            dirCount+=1
            for t in tests:
                # generic simple regex to match failure
                if t.has_key('regex'):
                    if t['test'](rootDir,sub,regex=t['regex']):
                        t['count']+=1
                        t['dirlist'].append(sub)
                # pass back data since a list of things may have failed!
                elif t.has_key('dataByDir'):
                    if t['test'](rootDir,sub,data=t['dataByDir']):
                        t['count']+=1
                        t['dirlist'].append(sub)
                else:
                    if t['test'](rootDir,sub):
                        t['count']+=1
                        t['dirlist'].append(sub)
                        if t.has_key('startupTime') and gDoTimes:
                            t['startupTime'][sub]=getStartupTime(rootDir,sub)
        break
    return


def PrintStats(tests):
    print ""
    for t in tests:
        if "Total" in t['name']:
            totalRuns=t['count']
            fullTimeList = t['startupTime']
        if "Failures" in t['name']:
            totalFailures=t['count']
            uncharacterizedDirs=t['dirlist']
    print "########"
    print "Total Failure Count =%d for a %02.2f%% failure rate out of %d Total Tests"%(totalFailures,100.0*totalFailures/totalRuns,totalRuns)
    print "########"

    for t in tests:
        per = t['count']*100.0/totalRuns
        if "Total" in t['name']:
            continue
        if "Failures" in t['name']:
            continue
        print "test %s has a count of %d for a percentage of %02.2f%%" % (t['name'],t['count'],per)

        # handle additional data if any
        if t.has_key('dataByDir') and not "Success" in t['name'] and gVerbose>0:
            for k in t['dataByDir'].keys():
                print "\t dir=%s  data matches:[%s]" %(k,t['dataByDir'][k])
        elif not "Success" in t['name'] and gVerbose>0:
            for k in t['dirlist']:
                print "\t dir=%s"%(k)
        # get some time info
        timeList = []
        if len(fullTimeList)>0:
            for d in t['dirlist']:
                timeList.append(fullTimeList[d])
        # 0.0 means we don't know anything so don't mix it into the stats
        timeListStat=[x for x in timeList if x > 0]
        try:
            timeListStat.remove(0.0)
        except ValueError:
            pass
        if len(timeListStat):
            print ("\tStartup Time Information (Number of  0.0 sec entries removed = %d):\n" % (len(timeList) - len(timeListStat)))
            print("\t\t Min Startup Time: %f" % min(timeListStat))
            print("\t\t Max Startup Time: %f" % max(timeListStat))
            print("\t\t Avg Startup Time: %f" % (sum(timeListStat)/float(len(timeListStat))))
            if gVerbose:
                print("\t In case you want to dive deeper,here are the dir:times -- ")
                for time,dir in zip(timeList,t['dirlist']):
                    print "\t\tdir:%s took %f sec"%(dir,time)
        else:
            print "\tNo Time information for this test :("


        # figure out how many failures do not have matching tests yet
        if "Success" not in t['name']:
            totalFailures-=t['count']
        u=[x for x in uncharacterizedDirs if x not in t['dirlist']]
        uncharacterizedDirs=u

    print "Had %d uncharacterized Failures!"%len(uncharacterizedDirs)
    print "uncharacterizedDirs=%s!"%(uncharacterizedDirs)
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
                                        'hvtd:c:', ["help", "verbose", "dir=","cores="])
    except Exception, e:
        print e
        usage()

    # default values
    rootDir="."
    import multiprocessing
    maxQSize = multiprocessing.cpu_count()

    for (k,v) in options:
        if k in ('-h', '--help'):
            usage()
        elif k in ('-v', '--verbose'):
            gVerbose += 1
        elif k in ('-t'):
            gDoTimes = True
        elif k in ('-d', '--dir'):
            rootDir = v
        elif k in ('-c', '--cores'):
            maxQSize = v
        else:
            print "I didn't understand that"
            usage()

    # test definitions
    tests = [{"name":"kernelPanic",
             "test":isSimpleRegex,
#              "regex":'^\[?\s*\d*\]\s?Kernel panic.*Attempted.*$',
              # deals with new timecodes.
              "regex":'.*Kernel panic.*Attempted.*kill.*idle task\!.*$',
              "dirlist":[],
              "count":0
          },
             {"name":"XServerFail",
             "test":isSimpleRegex,
              "regex":'^\|.*xserver-nodm.*loaded failed failed Xserver.*display manager$',
              "dirlist":[],
              "count":0
          },
             {"name":"Qemu PID didn't appear, complete fail to start qemu",
             "test":isSimpleRegex,
              "regex":'^\|.* NOTE: Qemu pid didn\'t appeared in 60 seconds$',
              "dirlist":[],
              "count":0
          },

             {"name":"SystemdListUnitTimeout",
             "test":isSimpleRegex,
              "regex":'^\|.*Failed to list unit files: Connection timed out$',
              "dirlist":[],
              "count":0
          },
             {"name":"ServicesFail-AvahiTimeout",
             "test":isServicesFailAvahiTimeout,
              "dirlist":[],
              "dataByDir":{},
              "count":0
          },

             {"name":"ServicesFail-AvahiExits",
             "test":isServicesFailAvahiExit,
              "dirlist":[],
              "dataByDir":{},
              "count":0
          },

             {"name":"SshFails",
             "test":isSimpleRegex,
              "regex":'^\| FAIL\: test_ssh \(oeqa\.runtime\.ssh\.SshTest\)$',
              "dirlist":[],
              "dataByDir":{},
              "count":0
          },

             {"name":"SystemdFailsBasic",
             "test":isSimpleRegex,
              "regex":'^\| FAIL\: test_systemd_status \(oeqa\.runtime\.systemd\.SystemdServiceTests\)$',
              "dirlist":[],
              "dataByDir":{},
              "count":0
          },


             # summation tests
             {"name":"Failures",
             "test":isFailDir,
              "dirlist":[],
              "count":0
          },
             {"name":"Successes",
             "test":isSuccessDir,
              "dirlist":[],
              "count":0
          },
             {"name":"Total",
             "test":isTestDir,
              "dirlist":[],
              # this is a dict of startuptimes by testdir so that we can look it up
              # it's too expensive to run this more than once.
              "startupTime":{},
              "count":0
          }
         ]



    HandleTests(tests,rootDir)
    PrintStats(tests)




else:
    # being imported as a module
    print "Module time!"
