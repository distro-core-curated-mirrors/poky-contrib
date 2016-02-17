#!/usr/bin/python
# Copyright

# DESCRIPTION
# This is eclipse automation base class and test cases file



import unittest, time, re, sys, getopt, os, logging, string, errno, exceptions
from time import sleep

import shutil, argparse, ConfigParser, platform, json
from iniparser import IniParser
import getpass, subprocess
from dogtail import tree
from dogtail.tree import predicate
from datetime import datetime
from dogtail.rawinput import keyCombo, pressKey, typeText
from dogtail.procedural import FocusApplication
from configVariables import *
import httplib
import urllib2
import pexpect


class NoParsingFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == 100

class testcase(object):

    def __init__(self, test_case):
        self.test_case = test_case

    def __call__(self, func):
        def wrapped_f(*args):
            return func(*args)
        wrapped_f.test_case = self.test_case
        wrapped_f.__name__ = func.__name__
        return wrapped_f


def LogResults(original_class):
    orig_method = original_class.run

    inifile = IniParser()

    param1 = inifile.getValue("settings-eclipse.ini", "Run", "param1")
    param2 = inifile.getValue("settings-eclipse.ini", "Run", "param2")
    eclipse_version= inifile.getValue("settings-eclipse.ini", "Run", "eclipse_version")
    commit = inifile.getValue("settings-eclipse.ini", "Run", "commit")
    dateofrun = inifile.getValue("settings-eclipse.ini", "Run", "date")

    name_of_file = 'results-eclipse-' + eclipse_version +'.log'
    path_of_file = '/home/'+getpass.getuser()+'/eclipse-results/' + param1 + '/' + param2 + "-" + dateofrun + "/"
    logfile=path_of_file+name_of_file

    from time import strftime, gmtime
    caller = os.path.basename(sys.argv[0])
    #timestamp = strftime('%Y%m%d%H%M%S',gmtime())
    #logfile = os.path.join(os.getcwd(),'results-'+caller+'.'+timestamp+'.log')
    linkfile = os.path.join(os.getcwd(),'results-'+caller+'.log')

    #rewrite the run method of unittest.TestCase to add testcase logging
    def run(self, result, *args, **kws):
        orig_method(self, result, *args, **kws)
        passed = True
        testMethod = getattr(self, self._testMethodName)
        #if test case is decorated then use it's number, else use it's name
        try:
            test_case = testMethod.test_case
        except AttributeError:
            test_case = self._testMethodName

        class_name = str(testMethod.im_class).split("'")[1]

        #create custom logging level for filtering.
        custom_log_level = 100
        logging.addLevelName(custom_log_level, 'RESULTS')

        def results(self, message, *args, **kws):
            if self.isEnabledFor(custom_log_level):
                self.log(custom_log_level, message, *args, **kws)
        logging.Logger.results = results

        logging.basicConfig(filename=logfile,
                            filemode='w',
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            datefmt='%H:%M:%S',
                            level=custom_log_level)
        for handler in logging.root.handlers:
            handler.addFilter(NoParsingFilter())
        local_log = logging.getLogger(caller)

        #check status of tests and record it

        for (name, msg) in result.errors:
            if (self._testMethodName == str(name).split(' ')[0]) and (class_name in str(name).split(' ')[1]):
                local_log.results("Testcase "+str(test_case)+": ERROR")
                local_log.results("Testcase "+str(test_case)+":\n"+msg)
                passed = False
        for (name, msg) in result.failures:
            if (self._testMethodName == str(name).split(' ')[0]) and (class_name in str(name).split(' ')[1]):
                local_log.results("Testcase "+str(test_case)+": FAILED")
                local_log.results("Testcase "+str(test_case)+":\n"+msg)
                passed = False
        for (name, msg) in result.skipped:
            if (self._testMethodName == str(name).split(' ')[0]) and (class_name in str(name).split(' ')[1]):
                local_log.results("Testcase "+str(test_case)+": SKIPPED")
                passed = False
        if passed:
            local_log.results("Testcase "+str(test_case)+": PASSED")

        # Create symlink to the current log
        if os.path.exists(linkfile):
            os.remove(linkfile)
        os.symlink(logfile, linkfile)

    original_class.run = run

    return original_class


###########################################
#                                         #
# PART II: base class                     #
#                                         #
###########################################

@LogResults
class eclipse_cases_base(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.log = cls.logger_create()

    def setUp(self):
        #self.parser.read('eclipse_test.cfg')

        pass

    @staticmethod
    def logger_create():
        
 
        inifile = IniParser()

        param1 = inifile.getValue("settings-eclipse.ini", "Run", "param1")
        param2 = inifile.getValue("settings-eclipse.ini", "Run", "param2")
        eclipse_version= inifile.getValue("settings-eclipse.ini", "Run", "eclipse_version")
        dateofrun = inifile.getValue("settings-eclipse.ini", "Run", "date")

        name_of_file = 'eclipse-' + eclipse_version + "-" +param1 + "-" + param2 + "-" + dateofrun +".log"
        path_of_file = '/home/'+getpass.getuser()+'/eclipse-results/' + param1 + '/' + param2 + "-" + dateofrun + "/"
        log_file=path_of_file+name_of_file

        if not os.path.exists(path_of_file):
            os.makedirs(path_of_file)
        #log_file = "eclipse-auto-" + time.strftime("%Y%m%d%H%M%S") + ".log"

        #if os.path.exists("eclipse-auto.log"): os.remove("eclipse-auto.log")
        #os.symlink(log_file, "eclipse-auto.log")

        log = logging.getLogger("eclipse")
        log.setLevel(logging.DEBUG)

        fh = logging.FileHandler(filename=log_file)
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        log.addHandler(fh)
        log.addHandler(ch)

        return log


    def tearDown(self):


        app = tree.root.application('Eclipse')
        frames = app.findChildren(predicate.GenericPredicate(roleName = frame_rolename))
        frames_number = len(frames)
        if (frames_number == 0):
            self.log.info("can not find frames")
        while frames_number > 1:
            keyCombo("<<Alt><F4>")
            print frames_number
            frames_number-= 1



    def create_tree(self, eclipse_version, param1, param2, dateofrun):

        nameofrun = "run-"+ param1 + "-" + param2 + "-" + dateofrun
        self.log.info("# Step  : Name of run: %s"%(nameofrun))

        #create folder for eclipse-run
        eclipse_run = '/home/' + getpass.getuser() + '/eclipse-run/'
        if not os.path.exists(eclipse_run):
            os.makedirs(eclipse_run)
            self.log.info("# Step  : Create directory : %s" %(eclipse_run))

        #create folder run-param1-param2-date of run in eclipse-run
        run_path=eclipse_run + nameofrun
        if not os.path.exists(run_path):
                os.makedirs(run_path)
                self.log.info("# Step  : Create directory : %s" %(run_path))

        #create folder download under eclipse-run/run-param1-param2-dateofrun.
        download_path = run_path + "/download"
        if not os.path.exists(download_path):
                os.makedirs(download_path)
                self.log.info("# Step  : Create directory : %s" %(download_path))

        #create folder installed under eclipse-run/run-param1-param2-dateofrun.
        installed_path = run_path + "/installed"
        if not os.path.exists(installed_path):
                os.makedirs(installed_path)
                self.log.info("# Step  : Create directory : %s" %(installed_path))


        #create folder version of eclipse(luna/kepler/mars) under eclipse-run/run-param1-param2-dateofrun.
        version_path = run_path + "/"+eclipse_version
        if not os.path.exists(version_path):
                os.makedirs(version_path)
                self.log.info("# Step  : Create directory : %s" %(version_path))


        #create folder for eclipse-results
        eclipse_result = '/home/' + getpass.getuser() + '/eclipse-results/'
        if not os.path.exists(eclipse_result):
            os.makedirs(eclipse_result)
            self.log.info("# Step  : Create directory : %s" %(eclipse_result))


        #create folder for release-results
        release_result = eclipse_result + "/releases"
        if not os.path.exists(release_result):
            os.makedirs(release_result)
            self.log.info("# Step  : Create directory : %s" %(release_result))

        #create folder for nightly-results
        nightly_result = eclipse_result + "/nightly"
        if not os.path.exists(nightly_result):
            os.makedirs(nightly_result)
            self.log.info("# Step  : Create directory : %s" %(nightly_result))


    def download_basic_things(self, param1, param2, dateofrun):

        dogtail_scripts_path = subprocess.check_output("pwd", shell=True)
        examples_path = dogtail_scripts_path.strip()

        download_path = '/home/' + getpass.getuser() + '/eclipse-run/' + "run-" + param1 + "-" + param2 + "-" + dateofrun + '/download/'
        os.chdir(download_path)
        adt_archive="adt_installer.tar.bz2"
        adt_archive_path = download_path + adt_archive

        if os.path.exists(adt_archive_path):
            self.log.info("* Check : Found adt-archive on %s-%s"%(param1,param2))
        else:
            self.log.info("# Step  : Download adt-archive for %s-%s"%(param1,param2))
            if not "rc" in param2:
                adt_link = "https://autobuilder.yoctoproject.org/pub/" + param1 + "/" + param2 + "/adt-installer/" + adt_archive
            else:
                adt_link = "https://autobuilder.yoctoproject.org/pub/" + param1 + "/" + param2 + "/adt-installer-QA/" + adt_archive

            #verify adt_link
            try:
                response = urllib2.urlopen(adt_link)
                self.log.info("* Check : Url is : " +  str(adt_link) )
                self.log.info("* Check : Response from url is : " + str(response.code))
                os.system("wget -q " +adt_link)
                self.log.info("# Step  : Wget " + str(adt_link) )
            except urllib2.HTTPError, message:
                self.fail("Message from url is : " + str(message.code))
            except urllib2.URLError, urlerror:
                self.fail("Message from url is : " + str(urlerror.args))



        adt_path = download_path + 'adt-installer'
        if os.path.exists(adt_path):
            self.log.info("* Check : Found folder adt-installer on %s-%s"%(param1,param2))
        else:
            os.system("tar jxf "+adt_archive)
            self.log.info("# Step  : Extract adt-archive")


        poky_path = download_path + "poky/"
        if os.path.exists(poky_path):
            self.log.info("* Check : Found folder poky on %s-%s folder"%(param1,param2))
        else:
            os.system("git clone git://git.yoctoproject.org/poky")
            self.log.info("# Step  : Clone poky")

        # download poky2
        poky2_path = download_path + "poky2/"
        if os.path.exists(poky2_path):
            self.log.info("* Check : Found folder poky2 on %s-%s folder"%(param1,param2))
        else:
            os.system("git clone git://git.yoctoproject.org/poky poky2")
            self.log.info("# Step  : Clone poky2")

        #download toolchain
        os.chdir(download_path)

        toolchain_i586 = subprocess.check_output("curl -s http://autobuilder.yoctoproject.org/pub/" + param1 + "/"+ param2 + "/" + "/toolchain/x86_64/" + "/|grep sato-i586|sed \'s/<[^>]*>//g\'|awk -F\"./.sh\" \'{print $1}'", shell=True)
        toolchain_i586_split = str(toolchain_i586.split(".sh")[0]).strip() + ".sh"
        toolchain_i586_link = "http://autobuilder.yoctoproject.org/pub/" + param1 + "/" + param2 + "/toolchain/x86_64/" + toolchain_i586_split
        toolchain_path=download_path + toolchain_i586_split

        if os.path.exists(toolchain_path):
            self.log.info("* Check : Found toolchain %s in download folder "%(toolchain_i586_split))
        else:
            self.log.info("# Step  : Download toolchain %s"%(toolchain_i586_split))
            try:
                response = urllib2.urlopen(toolchain_i586_link)
                self.log.info("* Check : Url is : " +  str(toolchain_i586_link) )
                self.log.info("* Check : Response from url is : " + str(response.code))
                os.system("wget -q " + toolchain_i586_link)
                self.log.info("# Step  : Wget " + str(toolchain_i586_link))
            except urllib2.HTTPError, message:
                self.fail("Message from url is : " + str(message.code))
            except urllib2.URLError, urlerror:
                self.fail("Message from url is : " + str(urlerror.args))

    
        os.chdir(examples_path)




    def download_plugin_and_eclipse_version(self, eclipse_version, param1, param2, dateofrun):

        dogtail_scripts_path = subprocess.check_output("pwd", shell=True)
        examples_path = dogtail_scripts_path.strip()

        version_path = '/home/' + getpass.getuser() + '/eclipse-run/' + "run-" + param1 + "-" + param2 + "-" + dateofrun + '/' + eclipse_version + '/'
        os.chdir(version_path)

        #download eclipse-plugin
        archive_parent_link = "http://autobuilder.yoctoproject.org/pub/" + str(param1) + "/" + str(param2) + "/"
        archive = subprocess.check_output("curl -s http://autobuilder.yoctoproject.org/pub/" + param1 + "/"+ param2 + "/" + "eclipse-plugin/" + eclipse_version +"/|grep archive|sed \'s/<[^>]*>//g\'|awk -F\".zip\" \'{print $1}'", shell=True)
        archive_link = str(archive_parent_link) + "eclipse-plugin/" + eclipse_version + "/" + archive.strip().split("\n" , 1)[0] + ".zip"


        archive_plugin_path = version_path + archive.strip().split("\n" , 1)[0]+".zip"

        if os.path.exists(archive_plugin_path):
            self.log.info("* Check : Found eclipse-%s plugin archive"%(eclipse_version))
        else:
            self.log.info("# Step  : Download eclipse-%s plugin archive"%(eclipse_version))
            try:
                response = urllib2.urlopen(archive_link)
                self.log.info("* Check : Url is : " +  str(archive_link) )
                self.log.info("* Check : Response from url is : " + str(response.code))
                os.system("wget -q " + archive_link)
                self.log.info("# Step  : Wget " + str(archive_link))
            except urllib2.HTTPError, message:
                self.fail("Message from url is : " + str(message.code))
            except urllib2.URLError, urlerror:
                self.fail("Message from url is : " + str(urlerror.args))

        #download eclipse-poky for eclipse-version(luna/kepler/mars)

        version_poky_parent_link = "http://autobuilder.yoctoproject.org/pub/" + str(param1) + "/" + str(param2) + "/"
        version_poky = subprocess.check_output("curl -s http://autobuilder.yoctoproject.org/pub/" + param1 + "/"+ param2 +"/|grep eclipse-poky-" + eclipse_version +"|sed 's/<[^>]*>//g'|awk -F\".tar.bz2\" \'{print $1}\'", shell=True)

        if not "rc" in param2:
            version_poky_link = version_poky_parent_link + version_poky.strip().split("\n" , 2)[1] + ".tar.bz2"
            archive_eclipse_path = version_path + version_poky.strip().split("\n" , 2)[1] + ".tar.bz2"
        else:
            version_poky_link = version_poky_parent_link + version_poky.strip().split("\n" , 1)[0] + ".tar.bz2"
            archive_eclipse_path = version_path + version_poky.strip().split("\n" , 1)[0] + ".tar.bz2"

        if os.path.exists(archive_eclipse_path):
            self.log.info("* Check : Found eclipse-%s poky archive"%(eclipse_version))
        else:
            self.log.info("# Step  : Download eclipse-%s poky archive"%(eclipse_version))
            try:
                response = urllib2.urlopen(version_poky_link)
                self.log.info("* Check : Url is : " +  str(version_poky_link) )
                self.log.info("* Check : Response from url is : " + str(response.code))
                os.system("wget -q " + version_poky_link)
                self.log.info("# Step  : Wget " + str(archive_link))
            except urllib2.HTTPError, message:
                self.fail("Message from url is : " + str(message.code))
            except urllib2.URLError, urlerror:
                self.fail("Message from url is : " + str(urlerror.args))

        #extract eclipse-poky

        if not "rc" in param2:
            poky_archive = version_poky.strip().split("\n" , 2)[1] + ".tar.bz2"
        else:
            poky_archive = version_poky.strip().split("\n" , 1)[0] + ".tar.bz2"

        os.system("tar jxf " + poky_archive)
        self.log.info("# Step  : Extract : %s"%(poky_archive))

        os.chdir(examples_path)

    def install_basic_things(self, param1, param2, commit, dateofrun):

        dogtail_scripts_path = subprocess.check_output("pwd", shell=True)
        examples_path = dogtail_scripts_path.strip()

        run_path = '/home/' + getpass.getuser() + '/eclipse-run/' + "run-" + param1 + "-" + param2 + "-" + dateofrun
        download_path = run_path + '/download/'

        toolchain_i586 = subprocess.check_output("curl -s http://autobuilder.yoctoproject.org/pub/" + param1 + "/"+ param2 + "/" + "/toolchain/x86_64/" + "/|grep sato-i586|sed \'s/<[^>]*>//g\'|awk -F\"./.sh\" \'{print $1}'", shell=True)
        tch_file = toolchain_i586.split(".sh")[0].strip() + ".sh"

        os.chdir(download_path)
        os.system("chmod +x %s" %tch_file)
        toolchain_installed_path = run_path + "/installed/toolchain"

        if os.path.exists(toolchain_installed_path):
            self.log.info("* Check : Found toolchain %s installed"%(tch_file))
        else:
            self.log.info("# Step  : Install toolchain : %s" %(tch_file))

            tch = pexpect.spawn("sh " + str(tch_file))
            tch.expect("Enter target directory for SDK")
            tch.sendline(toolchain_installed_path)
            tch.expect("Proceed[Y/n]?")
            tch.sendline("Y")
            i = tch.expect(['Each time you wish to use the SDK in a new shell session, you need to source the environment setup script e.g.','SDK has been successfully set up and is ready to be used.'], timeout=600)
            if i==0:
                self.log.warning("Each time you wish to use the SDK in a new shell session, you need to source the environment setup script e.g.")
            elif i==1:
                self.log.info("# Step  : SDK has been successfully set up and is ready to be used.")


        #bitbake meta-ide-support and core-image-sato-sdk
        poky_path = download_path + "poky/"
        os.chdir(poky_path)
        os.system("git checkout " + commit)
        os.chdir(examples_path)
        os.system("bash build_meta_ide.sh %s" %(poky_path))

        self.log.info("# Step  : Build meta-ide-support")
        adt_path = download_path + 'adt-installer'
        adt_archive="adt_installer.tar.bz2"

        if os.path.exists(adt_path):
            self.log.info("* Check : Found adt extracted")
        else:
            os.chdir(download_path)
            #extract adt archive
            os.system("tar jxf "+ adt_archive)
            self.log.info("# Step  : Extract : %s" %(adt_archive))

        #install adt
        adt_path = download_path + 'adt-installer'
        os.chdir(adt_path)
        adt_installed_path = run_path + "/installed/adt"

        if os.path.exists(adt_installed_path):
            self.log.info("* Check : Found adt installed")
        else:
            self.log.info("# Step  : Install adt-installer")

            child = pexpect.spawn("./adt_installer")
            child.expect("Please enter the install location")
            child.sendline(adt_installed_path)
            child.expect("Please enter your selections here:")
            child.sendline("s")
            i = child.expect(['# Yocto ADT has been successfully installed.','# Meet errors', '# Please check'], timeout=15000)
            if i==0:
                self.log.info("# Step  : Yocto ADT has been successfully installed")
            elif i==1:
                self.fail("Meet errors and can not install ADT")
            elif i==2:
                self.fail("Please download another ADT")

        os.chdir(examples_path)

    def install_eclipse_version(self, param1, param2, eclipse_version, dateofrun):

        dogtail_scripts_path = subprocess.check_output("pwd", shell=True)
        examples_path = dogtail_scripts_path.strip()

        run_path = '/home/' + getpass.getuser() + '/eclipse-run/' + "run-" + param1 + "-" + param2 + "-" + dateofrun
        download_path = run_path + '/download/'

        #install eclipse
        version_poky = subprocess.check_output("curl -s http://autobuilder.yoctoproject.org/pub/" + param1 + "/"+ param2 +"/|grep eclipse-poky-" + eclipse_version +"|sed 's/<[^>]*>//g'|awk -F\".tar.bz2\" \'{print $1}\'", shell=True)

        if not "rc" in param2:
            version_poky_directory = version_poky.strip().split("\n" , 2)[1]
        else:
            version_poky_directory = version_poky.strip().split("\n" , 1)[0]

        eclipse_poky_path = run_path + '/' + eclipse_version + "/" + version_poky_directory +"/scripts"
        launch_path = eclipse_poky_path + "/eclipse/eclipse"

        if os.path.exists(launch_path):
            self.log.info("* Check : Found eclipse %s installed " %(eclipse_version))
        else:
            os.chdir(eclipse_poky_path)
            os.system("./setup.sh")
            self.log.info("# Step  : Install eclipse %s " %(eclipse_version))


        ##command_to_build_plugin = "ECLIPSE_HOME=" + eclipse_poky_path + "/eclipse ./build.sh " + eclipse_version + "-master " + "master " + eclipse_version + "-master"
        ##os.system(command_to_build_plugin)
        ###self.log.info("# Step  : Build plugin")

        os.chdir(examples_path)


    def start_eclipse(self, param1, param2, eclipse_version, dateofrun):


        dogtail_scripts_path = subprocess.check_output("pwd", shell=True)
        examples_path = dogtail_scripts_path.strip()



        version_poky = subprocess.check_output("curl -s http://autobuilder.yoctoproject.org/pub/" + param1 + "/"+ param2 +"/|grep eclipse-poky-" + eclipse_version +"|sed 's/<[^>]*>//g'|awk -F\".tar.bz2\" \'{print $1}\'", shell=True)
        version_poky_directory = version_poky.strip().split("\n" , 1)[0]
        eclipse_poky_path = '/home/' + getpass.getuser() + '/eclipse-run/' + "run-" + str(param1) + "-" + str(param2) + "-" + str(dateofrun) +"/" + str(eclipse_version) + "/" + version_poky_directory

        eclipse_path = eclipse_poky_path + "/scripts/eclipse/"
        os.chdir(eclipse_path)
        os.system('./eclipse &')
        self.log.info("# Step  : Starting eclipse from %s \n" %(eclipse_path))

        time.sleep(10)
        self.log.info("# Step  : Waiting to start eclipse %s" %(eclipse_version))

        #os.system("cd -")

        #dogtail_path = "/home/" + getpass.getuser() + "/yocto/dogtail-0.9.0/examples"
        #os.chdir(dogtail_path)
        os.chdir(examples_path)


    def install_eclipse_plugin(self, param1, param2, eclipse_version, dateofrun):

        workspace_path = "/home/" + getpass.getuser() + '/eclipse-run/' + "run-" + str(param1) + "-" + str(param2) + "-"+ str(dateofrun) + "/" + str(eclipse_version)+"/workspace"
        
        app = tree.root.application('Eclipse')

        found = 1
        if os.path.exists(workspace_path):
            pass
        else:
            try:
                workspace = app.child(name = worspacelauncher_frame, roleName = frame_rolename)
                self.log.info("* Check : Workspace Launcher is Open")
            except:
                found = 0
                self.log.info("can not find Workspace Launcher frame")
            
            if found == 1:
                text = workspace.findChildren(predicate.GenericPredicate(roleName = text_rolename))
                nrText = len(text)
                if (nrText == 0):
                    self.log.info("can not find text boxes")
                    
            
                text[0].click()
                self.log.info("# Step  : Click on box <<Workspace>>")
                text[0].text = workspace_path
                self.log.info("* Check : Insert Workspace Location")

                try:
                    checkBox = workspace.findChildren(predicate.GenericPredicate(roleName=checkbox_rolename))
                    self.log.info("* Check : Found check box <<Use this as the default and do no ask again>>")
                except:
                    self.fail("can not find check box <<Use this as the default and do no ask again>")
                   
            
            
                checkBox[0].click()
                self.log.info("# Step  : Click on check box <<Use project specific settings>>")
            
                try:
                    ok = workspace.child(name=ok_button, roleName = button_rolename)
                    self.log.info("* Check : Found OK push button")
                except:
                    self.fail("can not find OK push button")

            
                if (ok.sensitive):
                    ok.click()
                    self.log.info("# Step  : Click <<OK>>")
                else:
                    self.fail("OK push button not sensitive")
                   
            time.sleep(60)
            print "sleep 60"
            
            eclipse =  app.child(roleName=frame_rolename)

            try:
                YPT = eclipse.child(name = yocto_project_tools_menu, roleName = menu_rolename)
                self.log.info("* Check : Found YoctoProjectTools menu")
                self.log.info("* Check : Plugin it's already installed")
            except:
                self.log.info("* Step : Install plugin .........")
                try:
                    helpmenu = eclipse.child(name = help_menu, roleName = menu_rolename)
                    self.log.info("* Check : Found Help menu")
                except:
                    self.fail("can not find Help menu")


                helpmenu.click()
                self.log.info("# Step  : Click on menu <<Help>>")

                try:
                    install_new_software = helpmenu.child(name=installnewsoftware_item, roleName=menuitem_rolename)
                    self.log.info("* Check : Found <<Install New Software...>> menu item")
                except:
                    self.fail("can not find Install New Software... menu item")

                install_new_software.click()
                self.log.info("# Step  : Click on menu item <<Install New Software...>>")

                try:
                    install = app.child(name=install_frame, roleName=frame_rolename)
                    self.log.info("* Check : Found <<Install>> frame")
                except:
                    self.fail("can not find Install frame")

                try:
                    addbutton = install.child(name = add_button, roleName = button_rolename)
                    self.log.info("* Check : Found Add... push button")
                except:
                    self.fail("can not find Add... push button")


                addbutton.click()
                self.log.info("# Step  : Click on box <<Add...>>")

                try:
                    addrepository = app.child(name=addrepository_frame , roleName=frame_rolename)
                    self.log.info("* Check : Found <<Add Repository>> frame")
                except:
                    self.fail("can not find Add Repository frame")

                text = addrepository.findChildren(predicate.GenericPredicate(roleName = text_rolename))
                nrText = len(text)
                if (nrText == 0):
                    self.fail("can not find text boxes")

                archive = subprocess.check_output("curl -s http://autobuilder.yoctoproject.org/pub/" + param1 + "/"+ param2 + "/" + "eclipse-plugin/" + eclipse_version +"/|grep archive|sed \'s/<[^>]*>//g\'|awk -F\".zip\" \'{print $1}'", shell=True)
                plugin = archive.strip().split("\n" , 1)[0] + ".zip"
                plugin_path = '/home/' + getpass.getuser() + '/eclipse-run/' + "run-" + param1 + "-" + param2 + "-" + dateofrun +"/" + eclipse_version

                location = "jar:file:" + plugin_path + "/" + plugin + "!/"

                text[1].click()
                self.log.info("# Step  : Click on box <<Location>>")
                text[1].text = location
                self.log.info("* Check : Insert Location")

                try:
                    ok = addrepository.child(name=ok_button, roleName = button_rolename)
                    self.log.info("* Check : Found OK push button")
                except:
                    self.fail("can not find OK push button")

                if (ok.sensitive):
                    time.sleep(2)
                    ok.click()
                    self.log.info("# Step  : Click <<OK>>")
                else:
                    self.fail("OK push button not sensitive")

                try:
                    selectAll = install.child(name = selectall_button, roleName = button_rolename)
                    self.log.info("* Check : Found Select All push button")
                except:
                    self.fail("can not find Select All push button")


                selectAll.click()
                self.log.info("# Step  : Click on box <<Select All>>")

                try:
                    next = install.child(name = next_button, roleName = button_rolename)
                    self.log.info("* Check : Found Next push button")
                except:
                    self.fail("can not find Next push button")


                time.sleep(4)

                if (next.sensitive):
                    self.log.info("* Check : Found Next push button sensitive")
                    next.click()
                    self.log.info("# Step  : Click <<Next>>")
                else:
                    self.fail("Next push button not sensitive")


                print "sleep 60"
                time.sleep(60)
                print "sleep 60"
                time.sleep(60)
                print "sleep 60"
                time.sleep(60)
                print "sleep 60"
                time.sleep(60)

                if (next.sensitive):
                    self.log.info("* Check : Found Next push button sensitive")
                    next.click()
                    self.log.info("# Step  : Click <<Next>>")
                else:
                    self.fail("Next push button not sensitive")

                try:
                    acceptTerms = install.child(name= acceptterms_button, roleName = radiobutton_rolename)
                    self.log.info("* Check : Found I accept the terms of the license agreement radio button")
                except:
                    self.fail("can not find I accept the terms of the license agreement radio button")


                acceptTerms.click()
                self.log.info("# Step  : Click on radio button <<I accept the terms of the license agreement>>")

                try:
                    finish = install.child(name=finish_button, roleName = button_rolename)
                    self.log.info("* Check : Found Finish push button")
                except:
                    self.fail("can not find Finish push button")



                if (finish.sensitive):
                    self.log.info("* Check : Found Finish push button sensitive")
                    finish.doubleClick()
                    time.sleep(2)
                    self.log.info("# Step  : Click <<Finish>>")
                else:
                    self.fail("Finish push button not sensitive")

                print "sleep 60"
                time.sleep(60)

                print "sleep 40"
                time.sleep(40)
                print "sleep 40"
                time.sleep(40)

                try:
                    securityWarning = app.child(name=securitywarning_frame, roleName=frame_rolename)
                    self.log.info("* Check : Found <<Security Warning>> frame")
                except:
                    self.log.info("can not find Security Warning frame")

                try:
                    ok = securityWarning.child(name=ok_button, roleName = button_rolename)
                    self.log.info("* Check : Found OK push button")
                except:
                    self.fail("can not find OK push button")

                if (ok.sensitive):
                    time.sleep(2)
                    ok.click()
                    self.log.info("# Step  : Click <<OK>>")
                else:
                    self.fail("OK push button not sensitive")

                print "sleep 100"
                time.sleep(100)

                try:
                    softwareUpdates= app.child(name=softwareupdates_frame, roleName=frame_rolename)
                    self.log.info("* Check : Found <<Software Updates>> frame")
                except:
                    self.fail("can not find Software Updates frame")

                try:
                    yes = softwareUpdates.child(name=yes_button, roleName = button_rolename)
                    self.log.info("* Check : Found Yes push button")
                except:
                    self.fail("can not find Yes push button")

                if (yes.sensitive):
                    self.log.info("* Check : Found Yes push button sensitive")
                    yes.click()
                    self.log.info("# Step  : Click on button <<Yes>>")
                else:
                    self.fail("Yes push button not sensitive")

                print "sleep 90"
                time.sleep(90)
                print "sleep 35"
                time.sleep(35)
                print "sleep 45"
                time.sleep(45)
            

    def restart_and_close_welcome(self):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        try:
            helpmenu = eclipse.child(name = help_menu, roleName = menu_rolename)
            self.log.info("* Check : Found Help menu")
        except:
            self.fail("can not find Help menu")

        helpmenu.click()
        self.log.info("# Step  : Click on menu <<Help>>")

        try:
            searchitem = helpmenu.child(name=search_item, roleName=menuitem_rolename)
            self.log.info("* Check : Found <<Search>> menu item")
        except:
            self.fail("can not find Search menu item")
        
        searchitem.click()
        self.log.info("# Step  : Click on menu item <<Search>>")

        time.sleep(3)

        try:
            filemenu = eclipse.child(name = file_menu, roleName = menu_rolename)
            self.log.info("* Check : Found File menu")
        except:
            self.fail("can not find File menu")

        filemenu.click()
        self.log.info("# Step  : Click on menu <<File>>")

        try:
            restartitem = filemenu.child(name = restart_item, roleName = menuitem_rolename)
            self.log.info("* Check : Found Restart menu")
        except:
            self.fail("can not find Restart menu")

        restartitem.click()
        self.log.info("# Step  : Click on menu item <<Search>>")

        self.log.info("# Step  : Waiting to restart ......")
        time.sleep(10)

    def close_eclipse(self):

        app = tree.root.application("Eclipse")
        eclipse =  app.child(roleName=frame_rolename)

        try:
            filemenu = eclipse.child(name = file_menu, roleName = menu_rolename)
            self.log.info("* Check : Found File menu")
        except:
            self.fail("can not find File menu")

        filemenu.click()
        self.log.info("# Step  : Click on menu <<File>>")

        try:
            exititem = filemenu.child(name = exit_item, roleName = menuitem_rolename)
            self.log.info("* Check : Found Exit menu item")
        except:
            self.fail("can not find Exit menu item")

        exititem.click()
        self.log.info("# Step  : Select <<Exit>> menu item")

    def verify_frame(self,name_of_frame):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        try:
            myFrame =  app.child(name = name_of_frame, roleName='frame')
            self.log.info("* Check : Window %s is Open " %name_of_frame)
        except:
            self.fail("FAIL: can not find %s frame " %name_of_frame)
            sys.exit(1)

    def click_menu(self, name_of_menu, parent):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        try:
            menu = parent.child(name = name_of_menu, roleName = menu_rolename)
            self.log.info("* Check : Found %s menu " %name_of_menu)
        except:
            self.fail("FAIL: can not find %s menu " %name_of_menu)
            sys.exit(1)

        menu.click()
        self.log.info("# Step  : Click on menu <<%s>>" %name_of_menu)

    def click_button(self,name_of_button, name_of_frame):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        myFrame =  app.child(name = name_of_frame, roleName='frame')

        try:
            button = myFrame.child(name = name_of_button, roleName = 'push button')
            self.log.info("* Check : Found %s push button " %name_of_button)
        except:
            self.fail("FAIL: can not find %s push button" %name_of_button)
            sys.exit(1)


        if (button.sensitive):
            button.click()
            self.log.info("# Step  : Click on <<%s>>" %name_of_button)
        else:
            self.fail("FAIL: button %s is not clickable" %name_of_button)
            sys.exit(1)


    def doubleClick_button(self,name_of_button, name_of_frame):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)
        myFrame =  app.child(name = name_of_frame, roleName='frame')

        try:
            button = myFrame.child(name = name_of_button, roleName = 'push button')
            self.log.info("* Check : Found %s push button " %name_of_button)
        except:
            self.fail("FAIL: can not find %s push button" %name_of_button)

        try:
            button.doubleClick()
            self.log.info("# Step  : Click on <<%s>>" %name_of_button)
        except:
            self.fail("FAIL: could not double click %s button" %name_of_button)
            sys.exit(1)

    def click_pageTab(self, name_of_pageTab, name_of_frame):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)
        myFrame =  app.child(name = name_of_frame, roleName='frame')

        try:
            pageTab = myFrame.child(name = name_of_pageTab, roleName = 'page tab')
            self.log.info("* Check : Found %s page tab " %name_of_pageTab)
        except:
            self.fail("FAIL: can not find %s page tab" %name_of_pageTab)
            sys.exit(1)

        try:
            pageTab.click()
            self.log.info("# Step  : Click on <<%s>>" %name_of_pageTab)
        except:
            self.fail("FAIL: could not click %s page tab" %name_of_pageTab)
            sys.exit(1)



    def click_tableCell(self, name_of_tableCell, name_of_frame):


        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)
        myFrame =  app.child(name = name_of_frame, roleName='frame')

        try:
            tableCell = myFrame.child(name = name_of_tableCell, roleName = 'table cell')
            self.log.info("* Check : Found %s table cell " %name_of_tableCell)
        except:
            self.fail("FAIL: can not find %s table cell" %name_of_tableCell)

        try:
            tableCell.click()
            self.log.info("# Step  : Click on <<%s>>" %name_of_tableCell)
        except:
            self.fail("FAIL: could not click %s table cell" %name_of_tableCell)
            sys.exit(1)



    def doubleclick_tableCell(self,name_of_tableCell, name_of_frame):

        app = tree.root.application('Eclipse')
        myFrame =  app.child(name = name_of_frame, roleName='frame')

        try:
            tableCell = myFrame.child(name = name_of_tableCell, roleName = 'table cell')
            self.log.info("* Check : Found %s table cell " %name_of_tableCell)
        except:
            self.fail("FAIL: can not find %s table cell" %name_of_tableCell)

        try:
            tableCell.doubleClick()
            self.log.info("# Step  : Double click on <<%s>>" %name_of_tableCell)
        except:
            self.fail("FAIL: could not double click on %s" %name_of_tableCell)
            sys.exit(1)



    def insert_text(self, myText, fieldNumber, name_of_frame):
        """
        :param myText:
        :param fieldNumber:
        :param name_of_frame:
        :return:
        """
        app = tree.root.application('Eclipse')
        myFrame =  app.child(name = name_of_frame, roleName='frame')

        text = myFrame.findChildren(predicate.GenericPredicate(roleName = 'text'))
        if (len(text) < 1):
            self.fail("FAIL: can not find any text boxes")

        try:
            text[fieldNumber].click()
            self.log.info("# Step  : Click on box")
        except:
            self.fail("FAIL: can not find text boxe %s" %fieldNumber)
            sys.exit(1)

        try:
            text[fieldNumber].text = myText
            self.log.info("# Step  : Insert text on box: %s" %myText)
        except:
            self.fail("FAIL: could not insert %s in " %myText)
            sys.exit(1)


    def select_from_dropdown_list(self,myMenuItem, dropDownNumber, name_of_frame):
        """
        :param myMenuItem:
        :param dropDownNumber:
        :param name_of_frame:
        :return:
        """
        app = tree.root.application('Eclipse')
        myFrame =  app.child(name = name_of_frame, roleName='frame')
        comboBox = myFrame.findChildren(predicate.GenericPredicate(roleName='combo box'))

        if (len(comboBox) > 1):
            self.log.info("* Check : Found drop-down lists")
        else:
            self.fail("FAIL: can not find combo boxes")
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = myFrame.child(name='Cancel', roleName = 'push button')
            if (cancel_close.sensitive):
                cancel_close.click()

        comboBox[dropDownNumber].click()
        self.log.info("# Step  : Click on drop-down list = %s" %dropDownNumber)

        try:
            dropDownItem = myFrame.child(name = myMenuItem, roleName='menu item')
            self.log.info("* Check : Found %s menu item" %myMenuItem)
        except:
            self.fail("FAIL: can not find %s menu item" %myMenuItem)

        dropDownItem.click()
        self.log.info("# Step  : Select <<%s>>" %myMenuItem)

    def select_radioButton(self, MyRadioButton, name_of_frame):

        app = tree.root.application('Eclipse')

        myFrame =  app.child(name = name_of_frame, roleName='frame')

        try:
            radioButton = myFrame.child(name = MyRadioButton, roleName = 'radio button')
            self.log.info("* Check : Found %s radio button" %MyRadioButton)
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = myFrame.child(name='Cancel', roleName = 'push button')
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("FAIL: can not find %s radio button" %MyRadioButton)

        radioButton.click()
        self.log.info("# Step  : Click on %s radio button" %MyRadioButton)


    def select_checkBox(self,myCheckBox, name_of_frame):

        app = tree.root.application('Eclipse')

        myFrame =  app.child(name = name_of_frame, roleName='frame')

        try:
            checkBox = myFrame.child(name = myCheckBox, roleName = 'check box')
            self.log.info("* Check : Found %s check box" %myCheckBox)
        except:
            self.fail("FAIL: can not find %s check box" %myCheckBox)
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = myFrame.child(name='Cancel', roleName = 'push button')
            if (cancel_close.sensitive):
                cancel_close.click()

        checkBox.click()
        self.log.info("# Step  : Click on %s check box" %myCheckBox)


    def verifyMessage(self,myMessage):

        app = tree.root.application('Eclipse')

        myFrame =  app.child(name = 'Android Driver Development Kit', roleName='frame')
        text = myFrame.findChildren(predicate.GenericPredicate(roleName = 'text'))
        nrText = len(text)

        if (nrText < 1):
            self.fail("FAIL: can not find text boxes")

        text[nrText-1].click()
        self.log.info("# Step  : Click on text")
        last_lines = text[nrText-1].text.strip().split("\n")[-3:]

        self.log.info("* Check : Text on box: %s" %last_lines)

        if any(myMessage in line for line in last_lines):
            self.log.info("* Check : Found message: %s" %myMessage)
        else:
            self.fail("FAIL: can not find message: %s" %myMessage)


   
    def configure_standard_profile(self, toolchainType, toolchainAdr, sysrootAdr, targetArch, targetType, kernelAdr):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        # try to found window menu
        try:
            window = eclipse.child(name = window_menu, roleName = menu_rolename)
            self.log.info("* Check : Found Window menu")
        except:
            self.fail("can not find Window menu")

        window.click()
        self.log.info("# Step  : Click on menu <<Window>>")

        try:
            windowitem = window.child(name=preferences_item, roleName=menuitem_rolename)
            self.log.info("* Check : Found <<Preferences>> menu item")
        except:
            self.fail("can not find Preferences menu item")
            

        windowitem.click()
        self.log.info("# Step  : Click on menu item <<Preferences>>")

        try:
            preferences = app.child(name = preferences_frame, roleName = frame_rolename)
            self.log.info("* Check : Window Preferences is Open")
        except:
            self.fail("can not find Preferences frame")
            

        text = preferences.findChildren(predicate.GenericPredicate(roleName = text_rolename))
        nrText = len(text)
        if (nrText == 0):
            self.fail("can not find text boxes")

        try:
            yoctoProjectADT = app.child(name = YP_ADT_tablecell, roleName = tablecell_rolename)
            self.log.info("* Check : Found Yocto Project ADT button")
        except:
            self.fail("can not find Yocto Project ADT table cell")

        yoctoProjectADT.click()
        self.log.info("# Step  : Click on <<Yocto Project ADT>>")

        comboBox = preferences.findChildren(predicate.GenericPredicate(roleName=combobox_rolename))

        try:
            crossCompiler = preferences.child(name = toolchainType, roleName = radiobutton_rolename)
            self.log.info("* Check : Found toolchain type radio button")
        except:
            self.fail("can not find toolchain type radio button")

        crossCompiler.click()
        self.log.info("# Step  : Click on radio button <<" + str(toolchainType)+">>")

        text = preferences.findChildren(predicate.GenericPredicate(roleName = text_rolename))
        nrText = len(text)
        if (nrText == 0):
            self.fail("can not find text boxes")
            

        text[3].click()
        self.log.info("# Step  : Click on box <<Toolchain Root Location>>")
        text[3].text = toolchainAdr
        self.log.info("* Check : Insert Toolchain Root Location")

        text[4].click()
        self.log.info("# Step  : Click on box <<Sysroot Location>>")
        text[4].text = sysrootAdr
        self.log.info("* Check : Insert Sysroot Location")

        if (len(comboBox) > 1):
            self.log.info("* Check : Found menu drop-down list Target Arhitecture")
            comboBox[1].click()
            self.log.info("# Step  : Click on menu drop-down list <<Target Arhitecture>>")
        else:
            self.fail("can not find combo boxes")

        try:
            targetArchitecture = preferences.child(name = targetArch, roleName=menuitem_rolename)
            self.log.info("* Check : Found " + str(targetArch) + " menu item")
        except:
            self.fail("can not find " + str(targetArch) + " menu item")
            

        targetArchitecture.click()
        self.log.info("# Step  : Select <<" + str(targetArch) + ">>")

        try:
            targetOptions = preferences.child(name = targetType , roleName = radiobutton_rolename)
            self.log.info("* Check : Found target type radio button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find target type radio button")

                

        targetOptions.click()
        self.log.info("# Step  : Click on radio button <<QEMU>>")

        if (targetType == "QEMU"):
            text[5].click()
            self.log.info("# Step  : Click on box <<Kernel>>")
            text[5].text = kernelAdr
            self.log.info("* Check : Insert location for bzImage")

        try:
            applyPref = preferences.child(name = apply_button, roleName = button_rolename)
            self.log.info("* Check : Found Apply push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()

            self.fail("can not find Apply push button")


        try:
            general = app.child(name = general_tablecell, roleName = tablecell_rolename)
            self.log.info("* Check : Found General button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find General table cell")

                

        general.click()
        self.log.info("# Step  : Click on <<General>>")

        if (applyPref.sensitive):
            applyPref.click()
            #applyPref.doubleClick()
            self.log.info("# Step  : Click <<Apply>> to save Standard Profile")
        else:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("Apply push button not sensitive")

        try:
            ok = preferences.child(name=ok_button, roleName = button_rolename)
            self.log.info("* Check : Found OK push button")
        except:
            self.fail("can not find OK push button")

        if (ok.sensitive):
            ok.click()
            self.log.info("# Step  : Click <<OK>>")
        else:
            self.fail("OK push button not sensitive")

                


    def work_around_preferences_frame(self):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        self.click_menu(window_menu,eclipse)

        try:
            window = eclipse.child(name = window_menu, roleName = menu_rolename)
            self.log.info("* Check : Found Window menu")
        except:
            self.fail("can not find Window menu")
            

        #window.click()
        #self.log.info("# Step  : Click on menu <<Window>>")

        try:
            windowitem = window.child(name = preferences_item, roleName = menuitem_rolename)
            self.log.info("* Check : Found <<Preferences>> menu item")
        except:
            self.fail("can not find Preferences menu item")

        windowitem.click()
        self.log.info("# Step  : Click on menu item <<Preferences>>")

        try:
            preferences = app.child(name = preferences_frame, roleName = frame_rolename)
            self.log.info("* Check : Window Preferences is Open")
        except:
            self.fail("can not find Preferences frame")
            

        text = preferences.findChildren(predicate.GenericPredicate(roleName = text_rolename))
        nrText = len(text)
        if (nrText == 0):
            self.fail("can not find text boxes")

        try:
            yoctoProjectADT = app.child(name = YP_ADT_tablecell, roleName = tablecell_rolename)
            self.log.info("* Check : Found Yocto Project ADT button")
        except:
            self.fail("can not find Yocto Project ADT table cell")

        yoctoProjectADT.click()
        self.log.info("# Step  : Click on <<Yocto Project ADT>>")

        text = preferences.findChildren(predicate.GenericPredicate(roleName = text_rolename))
        nrText = len(text)
        if (nrText == 0):
            self.fail("can not find text boxes")
            

        text[3].click()
        self.log.info("# Step  : Click on box <<Toolchain Root Location>>")
        text[3].text = "Input a long text to modify size of this frame---> workaround"
        self.log.info("* Check : Insert text for work around")

        try:
            general = app.child(name = general_tablecell, roleName = tablecell_rolename)
            self.log.info("* Check : Found General button")
        except:
            self.fail("can not find General table cell")

                

        general.click()
        self.log.info("# Step  : Click on <<General>>")

        try:
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            self.log.info("* Check : Found Cancel push button")
        except:
            self.fail("can not find Cancel push button")

        cancel_close.click()
        self.log.info("# Step  : Click on <<Cancel>>")


    def createProject(self, projectname, typeproject, searchtype, author, copyrightproject):

        app = tree.root.application("Eclipse")
        eclipse =  app.child(roleName=frame_rolename)

        try:
            project = eclipse.child(name = file_menu, roleName = menu_rolename)
            self.log.info("* Check : Found File menu")
        except:
            self.fail("can not find File menu")
            

        project.select()
        self.log.info("# Step  : Click on menu <<File>>")

        try:
            newmenu = project.child(name = new_menu, roleName = menu_rolename)
            self.log.info("* Check : Found New menu")
        except:
            self.fail("can not find New menu")
            

        newmenu.select()
        self.log.info("# Step  : Select <<New>> menu")

        try:
            projectitem = newmenu.child(name = project_item , roleName = menuitem_rolename)
            self.log.info("* Check : Found <<Project...>> menu item")
        except:
            self.fail("can not find Project... menu item")
            

        projectitem.click()
        self.log.info("# Step  : Click on menu item <<Project...>>")

        try:
            new_proj = app.child(name = new_project_frame, roleName = frame_rolename)
            self.log.info("* Check : New Project frame")
        except:
            self.fail("can not find New Project frame")


        text = new_proj.findChildren(predicate.GenericPredicate(roleName = text_rolename))

        text[0].click()
        self.log.info("# Step  : Click on box <<Wizards>>")
        text[0].text = typeproject
        self.log.info("* Check : Insert type of project")

        try:
            next = new_proj.child(name = next_button, roleName = button_rolename)
            self.log.info("* Check : Found Next push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = new_proj.child(name = cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find Next push button")

        time.sleep(4)
        if (next.sensitive):
            self.log.info("* Check : Found Next push button sensitive")
            #next.doubleClick()
            next.click()
            self.log.info("# Step  : Click <<Next>>")
        else:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = new_proj.child(name = cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("Next push button not sensitive")


        try:
            cProject = app.child(name = str(typeproject) + ' ', roleName = frame_rolename)
            self.log.info("* Check : Found " + str(typeproject) + " frame")
        except:
            self.fail("can not find" + str(typeproject) + " frame")
            

        text = cProject.findChildren(predicate.GenericPredicate(roleName = text_rolename))

        time.sleep(5)
        #text[0].click()
        #self.log.info("# Step  : Click on box <<Project Name >>")
        typeText(projectname)
        #text[0].text = projectname
        self.log.info("* Check : Insert name of project")

        if eclipse_version == 'mars':
            try:
                executable = cProject.child(name = executable_tablecell, roleName = tablecell_rolename)
                self.log.info("* Check : Found " + str(typeproject) + " frame  Executable table cell")
            except:
                self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
                cancel_close = cProject.child(name = cancel_button, roleName = button_rolename)
                if (cancel_close.sensitive):
                    cancel_close.click()
                self.fail("can not find Executable table cell")

            executable.actions['expand or contract'].do()
            self.log.info("# Step  : Expand or contract")
            time.sleep(3)

            try:
                yocto = cProject.child(name = YPADT_AutotoolsP_tablecell, roleName = tablecell_rolename)
                self.log.info("* Check : Found %s table cell" %(YPADT_AutotoolsP_tablecell))
            except:
                self.log.warning("# Warning  : Click <<Cancel>> and jump to next step" %(YPADT_AutotoolsP_tablecell))
                cancel_close = cProject.child(name = cancel_button, roleName = button_rolename)
                if (cancel_close.sensitive):
                    time.sleep(2)
                    cancel_close.click()
                self.fail("can not find %s table cell"%(YPADT_AutotoolsP_tablecell))


            yocto.actions['expand or contract'].do()
            self.log.info("# Step  : Expand Yocto Project ADT Autotools Project table cell")

            yocto.click()
            keyCombo("<<Page_Down>")
            time.sleep(2)

            tablecell = cProject.findChildren(predicate.GenericPredicate(name = searchtype, roleName = tablecell_rolename))
            nrTablecell = len(tablecell)
            keyCombo("<<Page_Down>")
            tablecell[nrTablecell-1].click()

        else:
            try:
                tree_table = cProject.child(name = projecttype_treetable, roleName = treetable_rolename)
                self.log.info("* Check : Found Project type tree table")
            except:
                self.fail("can not find Project type tree table")

            try:
                executable = tree_table.child(name = executable_tablecell, roleName = tablecell_rolename)
                self.log.info("* Check : Found " + str(typeproject) + " frame  Executable table cell")
            except:
                self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
                cancel_close = cProject.child(name = cancel_button, roleName = button_rolename)
                if (cancel_close.sensitive):
                    cancel_close.click()
                self.fail("can not find Executable table cell")


            executable.actions['expand or contract'].do()
            self.log.info("# Step  : Expand or contract")

            try:
                yocto = tree_table.child(name = YPADT_AutotoolsP_tablecell, roleName = tablecell_rolename)
                self.log.info("* Check : Found Yocto Project ADT Autotools Project table cell")
            except:
                self.fail("can not find Yocto Project ADT Autotools Project table cell")


            yocto.actions['expand or contract'].do()
            self.log.info("# Step  : Expand Yocto Project ADT Autotools Project table cell")

            yocto.click()

            keyCombo("<<Page_Down>")
            time.sleep(2)

            tablecell = tree_table.findChildren(predicate.GenericPredicate(name = searchtype, roleName = tablecell_rolename))
            nrTablecell = len(tablecell)

            keyCombo("<<Page_Down>")

            tablecell[nrTablecell-1].click()

        try:
            next = cProject.child(name = next_button, roleName = button_rolename)
            self.log.info("* Check : Found Next push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = cProject.child(name = cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find Next push button")

                

        if (next.sensitive):
            self.log.info("* Check : Found Next push button sensitive")
            #next.doubleClick()
            next.click()
            self.log.info("# Step  : Click <<Next>>")
        else:
            self.fail("Next push button not sensitive")
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = cProject.child(name = cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            

        text = cProject.findChildren(predicate.GenericPredicate(roleName = text_rolename))
        if (len(text) < 1):
            self.fail("can not find text boxes")
            
        # am schimbat 3 cu 2 si 4 cu 3
        text[3].click()
        self.log.info("# Step  : Click on box <<Author>>")
        text[3].text = author
        self.log.info("* Check : Insert Author")

        text[4].click()
        self.log.info("# Step  : Click on box <<Copyright notice>>")
        text[4].text = copyrightproject
        self.log.info("* Check : Insert Copyrght notice")

        try:
            finish = cProject.child(name=finish_button, roleName = button_rolename)
            self.log.info("* Check : Found Finish push button")
        except:
            self.fail("can not find Finish push button")
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = cProject.child(name = cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            

        if (finish.sensitive):
            self.log.info("* Check : Found Finish push button sensitive")
            finish.doubleClick()
            time.sleep(2)
            self.log.info("# Step  : Click <<Finish>>")
        else:
            self.fail("Finish push button not sensitive")

            

    def add_new_profile(self, newprofileName):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)
        try:
            window = eclipse.child(name = window_menu, roleName = menu_rolename)
            self.log.info("* Check : Found Window menu")
        except:
            self.fail("can not find Window menu")
            

        window.click()
        self.log.info("# Step  : Click on menu <<Window>>")

        try:
            windowitem = window.child(name=preferences_item, roleName = menuitem_rolename)
            self.log.info("* Check : Found <<Preferences>> menu item")
        except:
            self.fail("can not find Preferences menu item")
            

        windowitem.click()
        self.log.info("# Step  : Click on menu item <<Preferences>>")

        try:
            preferences = app.child(name = preferences_frame, roleName = frame_rolename)
            self.log.info("* Check : Window Preferences is Open")
        except:
            self.fail("can not find Preferences frame")
            

        text = preferences.findChildren(predicate.GenericPredicate(roleName = text_rolename))
        nrText = len(text)
        if (nrText == 0):
            self.fail("can not find text boxes")
            

        try:
            yoctoProjectADT = app.child(name = YP_ADT_tablecell, roleName = tablecell_rolename)
            self.log.info("* Check : Found Yocto Project ADT button")

        except:
            self.fail("can not find Yocto Project ADT table cell")
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
                

        yoctoProjectADT.click()
        self.log.info("# Step  : Click on <<Yocto Project ADT>>")

        try:
            saveAs = preferences.child(name = saveAs_button, roleName = button_rolename)
            self.log.info("* Check : Found Save as push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find Save as push button")

                

        saveAs.click()
        self.log.info("# Step  : Click <<Save as ...>>")

        try:
            saveAsProfile = app.child(name = saveAs_frame, roleName = frame_rolename)
            self.log.info("* Check : Found Save as new cross development profile frame")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find Save as new cross development profile frame")


        try:
            inputProfileName = saveAsProfile.child(roleName = text_rolename)
            self.log.info("* Check : Found box to input Profile Name")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find text")


        inputProfileName.click()
        self.log.info("# Step  : Click on box <<Profile Name>>")

        inputProfileName.text = newprofileName

        self.log.info("* Check : Insert Profile Name")

        found = 1
        try:
            ok = saveAsProfile.child(name=ok_button, roleName = button_rolename)
            self.log.info("* Check : Found OK push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find OK push button")


        if (ok.sensitive):
            ok.click()
            self.log.info("# Step  : Click <<OK>>")
        else:
            self.fail("can not find OK push button sensitive")

                    

        comboBox = preferences.findChildren(predicate.GenericPredicate(roleName=combobox_rolename))

        if (len(comboBox) > 0):
            comboBox[0].click()
        else:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find combo boxes")


        try:
            preferences.child(name=newprofileName, roleName=menuitem_rolename).click()
            self.log.info("* Check : Found profile name menu item")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find profile name menu item")



        try:
            general = app.child(name = general_tablecell, roleName = tablecell_rolename)
            self.log.info("* Check : Found General button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find General table cell")

        general.click()
        self.log.info("# Step  : Click on <<General>>")

        try:
            applyPref = preferences.child(name = apply_button, roleName = button_rolename)
            self.log.info("* Check : Found Apply push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find Apply push button")


        if (applyPref.sensitive):
            applyPref.click()
            self.log.info("# Step  : Click <<Apply>>")
        else:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("Apply push button not sensitive")

        try:
            ok = preferences.child(name=ok_button, roleName = button_rolename)
            self.log.info("* Check : Found OK push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find OK push button")


        if (ok.sensitive):
            ok.click()
            self.log.info("# Step  : Click <<OK>>")
        else:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("OK push button not sensitive")



    def open_perspective(self):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        found = 1
        try:
            openPersp = app.child(name = open_perspective_frame, roleName = frame_rolename)
            self.log.info("* Check : Found Open Associated Perspective")
        except:
            found = 0
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")

        if found == 1:
            try:
                yes = openPersp.child(name=yes_button, roleName = button_rolename)
                self.log.info("* Check : Found Yes push button")
            except:
                self.fail("can not find Yes push button")
                

            if (yes.sensitive):
                self.log.info("* Check : Found Yes push button sensitive")
                yes.click()
                #yes.doubleClick()
                self.log.info("# Step  : Click on button <<Yes>>")
            else:
                self.fail("Yes push button not sensitive")
                


    def reconfigure_project(self,projectname):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        text = eclipse.findChildren(predicate.GenericPredicate(roleName = text_rolename))
        nrText = len(text)
        if (nrText == 0):
            self.fail("can not find text boxes")
            

        text[nrText-1].click()
        self.log.info("# Step  : Click on box <<Quick Access>>")
        text[nrText-1].text='Reconfigure Project'
        self.log.info("# Step  : Insert <<Reconfigure Project>> on box <<Quick Access>>")

        try:
            reconfig = app.child(name = reconfigureproject_tablecell, roleName = tablecell_rolename)
            self.log.info("* Check : Found C Reconfigure Project table cell")
            reconfig.click()
            self.log.info("# Step  : Click on box <<Reconfigure Project >>")
        except:
            keyCombo("<<Esc>")
            self.log.warning("can not find Reconfigure Project table cell on Quick Access")
            try:
                project = eclipse.child(name = projectname, roleName=tablecell_rolename)
                self.log.info("* Check : Found <<" +str(projectname) + ">> table cell")
            except:
                self.fail("can not find " +str(projectname) + " table cell")
                

            project.click()
            self.log.info("* Step : Click on project <<" +str(projectname) + ">>")

            keyCombo("<<Shift><F10>")
            time.sleep(2)
            keyCombo("Down")
            keyCombo("Down")
            keyCombo("Down")
            keyCombo("Down")
            keyCombo("Down")
            keyCombo("Down")
            keyCombo("Down")
            keyCombo("Down")
            keyCombo("Down")
            keyCombo("Down")
            keyCombo("Down")
            keyCombo("Down")
            keyCombo("Down")
            keyCombo("Down")
            keyCombo("Down")
            keyCombo("Down")
            keyCombo("Down")
            keyCombo("Down")
            pressKey("Enter")   # Reconfigure project

        time.sleep(10)



    def verify_console(self):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        text = eclipse.findChildren(predicate.GenericPredicate(roleName = text_rolename))
        nrText = len(text)
        if (nrText == 0):
            self.fail("can not find text boxes")
            

        text[nrText-1].click()
        self.log.info("# Step  : Click on box <<Quick Access>>")
        text[nrText-1].text='Console'
        self.log.info("# Step  : Insert <<Console>> on box <<Quick Access>>")

        try:
            console = app.child(name = console_tablecell, roleName = tablecell_rolename)
            self.log.info("* Check : Found Console")
        except:
            self.fail("can not find Problems table cell")

        console.click()
        self.log.info("# Step  : Click on box <<Close Project>>")

        text[nrText-2].click()
        #self.log.info("# Step  : Click on" + str(projectname) + " Console")
        time.sleep(3)
        if "error" in text[nrText-2].text:
            self.log.info("# Step  : Output from  Console:")
            self.log.info(str(text[nrText-2].text))
        else:
            self.fail("Error found in Console")

        try:
            clearconsole = eclipse.child(description=clear_console_description, roleName = button_rolename)
            self.log.info("* Check : Found Clear Console push button")
        except:
            self.fail("can not find Clear Console push button")
            

        clearconsole.click()
        self.log.info("# Step  : Click on button <<Clear Console>>")

    def verify_profile(self, projectname, toolchainType, toolchainAdr, sysrootAdr, targetArch, targetType, kernelAdr, newprofileName):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)
        try:
            project = eclipse.child(name = project_menu, roleName = menu_rolename)
            self.log.info("* Check : Found Project menu")
        except:
            self.fail("can not find Project menu")

        project.click()
        self.log.info("# Step  : Click on menu <<Project>>")

        try:
            targetProfiles = project.child(name = targetprofiles_menu, roleName = menu_rolename)
            self.log.info("* Check : Found Project Target Profiles menu")
        except:
            self.fail("can not find Target Profiles menu")
            

        targetProfiles.select()
        self.log.info("# Step  : Select <<Target Profiles>> menu")

        # try to avoid a display bug. Need to select Target Profiles twice to see profileitem  with name = newprofileName

        targetProfiles.deselect()
        self.log.info("# Step  : Exit <<Target Profiles>> menu")

        project.deselect()
        self.log.info("# Step  : Exit <<Project>> menu")

        project.click()
        self.log.info("# Step  : Click on menu <<Project>>")

        targetProfiles.select()
        self.log.info("# Step  : Select <<Target Profiles>> menu")

        try:
            profileitem = targetProfiles.child(name = newprofileName , roleName = radio_menu_item_rolename)
            self.log.info("* Check : Found <<"+ str(newprofileName) + ">> menu item")
        except:
            self.fail("can not find" +str(newprofileName) + ">> menu item")
            

        targetProfiles.deselect()
        self.log.info("# Step  : Exit <<Target Profiles>> menu")

        project.deselect()
        self.log.info("# Step  : Exit <<Project>> menu")

        try:
            project = eclipse.child(name = project_menu, roleName = menu_rolename)
            self.log.info("* Check : Found Project menu")
        except:
            self.fail("can not find Project menu")
            

        project.select()
        self.log.info("# Step  : Click on menu <<Project>>")

        try:
            changeYPSettings = project.child(name = changeYPsettings_item, roleName = menuitem_rolename)
            self.log.info("* Check : Found Change Yocto Project Settings menu item")
        except:
            self.fail("can not find Change Yocto Project Settings menu item")
            

        changeYPSettings.click()
        self.log.info("# Step  : Select <<Change Yocto Project Settings menu >> menu item")

        try:
            projectProperties = app.child(name = 'Properties for ' + str(projectname) + " ", roleName = frame_rolename)
            self.log.info("* Check : Window Properties for " + str(projectname) + " is Open")
        except:
            self.fail("can not find Properties for " + str(projectname) + " frame")
            

        comboBox = projectProperties.findChildren(predicate.GenericPredicate(roleName=combobox_rolename))
        if (len(comboBox) > 1):
            self.log.info("* Check : Found menu drop-down list Target Arhitecture")
            if str(newprofileName) in str(comboBox[0]):
                self.log.info("* Check : Profile is saved correctly")
            else:
                self.log.warning("# Warning  : Profile is not saved correctly saved")
        else:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = projectProperties.child(name = cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find combo boxes")


        try:
            checkBox = projectProperties.findChildren(predicate.GenericPredicate(roleName=checkbox_rolename))
            self.log.info("* Check : Found check box <<Use project specific settings>>")
        except:
            self.fail("can not find check box <<Use project specific settings>")

        checkBox[0].click()
        self.log.info("# Step  : Click on check box <<Use project specific settings>>")

        try:
            crosscompiler = projectProperties.child(name = toolchainType, roleName = radiobutton_rolename)
            self.log.info("* Check : Found toolchain type radio button")
        except:
            self.fail("can not find toolchain type radio button")

        crosscompiler.click()
        self.log.info("# Step  : Click on radio button <<" + str(toolchainType) + ">>")

        text = projectProperties.findChildren(predicate.GenericPredicate(roleName = text_rolename))
        nrText = len(text)
        if (nrText == 0):
            self.fail("can not find text boxes")
            

        text[2].click()
        self.log.info("# Step  : Click on box <<Toolchain Root Location>>")
        if text[2].text == toolchainAdr:
            self.log.info("* Check : Toolchain Root Location is saved correctly")
        else:
            self.log.warning("# Warning  : Toolchain Root Location is not saved correctly saved")


        text[3].click()
        self.log.info("# Step  : Click on box <<Sysroot Location>>")
        if text[3].text == sysrootAdr:
            self.log.info("* Check : Sysroot Location is saved correctly")
        else:
            self.log.warning("# Warning  : Sysroot Location is not saved correctly saved")

        if (len(comboBox) > 1):
            self.log.info("* Check : Found menu drop-down list Target Arhitecture")
            if str(targetArch) in str(comboBox[1]):
                self.log.info("* Check : Target Arhitecture is saved correctly")
            else:
                self.log.warning("# Warning  : Target Arhitecture is not saved correctly saved")
                
        else:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = projectProperties.child(name = cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find combo boxes")

        try:
            targetT = projectProperties.child(name = targetType , roleName = radiobutton_rolename)
            self.log.info("* Check : Found target type radio button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = projectProperties.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find target type radio button")


        targetT.click()
        self.log.info("# Step  : Click on radio button <<QEMU>>")

        if (targetType == "QEMU"):
            text[4].click()
            self.log.info("# Step  : Click on box <<Kernel>>")
            if text[4].text == kernelAdr:
                self.log.info("* Check : Kernel Location is saved correctly")
            else:
                self.log.warning("# Warning  : Kernel Locationis not saved correctly saved")

        try:
            applyPref = projectProperties.child(name = apply_button, roleName = button_rolename)
            self.log.info("* Check : Found Apply push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = projectProperties.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find Apply push button")


        if (applyPref.sensitive):
            applyPref.doubleClick()
            self.log.info("# Step  : Click <<Apply>> to save Standard Profile")
        else:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = projectProperties.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("Apply push button not sensitive")


        try:
            ok = projectProperties.child(name=ok_button, roleName = button_rolename)
            self.log.info("* Check : Found OK push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = projectProperties.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find OK push button")


        if (ok.sensitive):
            ok.click()
            self.log.info("# Step  : Click <<OK>>")
        else:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = projectProperties.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("OK push button not sensitive")



    def rename_profile(self, newprofileName, renameprofile):


        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        try:
            window = eclipse.child(name = window_menu, roleName = menu_rolename)
            self.log.info("* Check : Found Window menu")
        except:
            self.fail("can not find Window menu")
            

        window.click()
        self.log.info("# Step  : Click on menu <<Window>>")

        try:
            windowitem = window.child(name=preferences_item, roleName=menuitem_rolename)
            self.log.info("* Check : Found <<Preferences>> menu item")
        except:
            self.fail("can not find Preferences menu item")
            

        windowitem.click()
        self.log.info("# Step  : Click on menu item <<Preferences>>")

        try:
            preferences = app.child(name = preferences_frame, roleName = frame_rolename)
            self.log.info("* Check : Window Preferences is Open")
        except:
            self.fail("can not find Preferences frame")
            

        text = preferences.findChildren(predicate.GenericPredicate(roleName = text_rolename))
        nrText = len(text)
        if (nrText == 0):
            self.fail("can not find text boxes")
            

        try:
            yoctoProjectADT = app.child(name = YP_ADT_tablecell, roleName = tablecell_rolename)
            self.log.info("* Check : Found Yocto Project ADT button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find Yocto Project ADT table cell")



        yoctoProjectADT.click()
        self.log.info("# Step  : Click on <<Yocto Project ADT>>")

        comboBox = preferences.findChildren(predicate.GenericPredicate(roleName=combobox_rolename))

        if (len(comboBox) > 1):
            self.log.info("* Check : Found menu drop-down list Target Arhitecture")
            comboBox[0].click()
            self.log.info("# Step  : Click on menu drop-down list <<Target Arhitecture>>")
        else:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name = cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find combo boxes")

        try:
            preferences.child(name=newprofileName, roleName=menuitem_rolename).click()
            self.log.info("* Check : Found profile name menu item")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find profile name menu item")


        try:
            Rename = preferences.child(name = rename_button, roleName = button_rolename)
            self.log.info("* Check : Found Rename push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find Rename push button")


        Rename.click()
        self.log.info("# Step  : Click <<Rename>>")

        try:
            renameProfile = app.child(name = rename_frame, roleName = frame_rolename)
            self.log.info("* Check : Found Rename cross development profile frame")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find Rename cross development profile frame")


        try:
            inputrenameProfileName = renameProfile.child(roleName = text_rolename)
            self.log.info("* Check : Found box to Rename Profile")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find text")


        inputrenameProfileName.click()
        self.log.info("# Step  : Click on box <<Profile Name>>")

        inputrenameProfileName.text = renameprofile              #RenameProfile"

        self.log.info("* Check : Insert Profile Name")

        found = 1
        try:
            ok = renameProfile.child(name=ok_button, roleName = button_rolename)
            self.log.info("* Check : Found OK push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find OK push button")


        if (ok.sensitive):
            ok.click()
            self.log.info("# Step  : Click <<OK>>")
        else:
            try:
                cancel = renameProfile.child(name=cancel_button, roleName = button_rolename)
                self.log.info("* Check : Found Cancel push button")
            except:
                self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
                if (cancel.sensitive):
                    cancel.click()
                self.fail("can not find Cancel push button")


        if (len(comboBox) > 0):
            comboBox[0].click()
        else:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find combo boxes")


        try:
            preferences.child(name=renameprofile, roleName=menuitem_rolename).click()
            self.log.info("* Check : Found Rename profile menu item")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find profile name menu item")

        try:
            general = app.child(name = general_tablecell, roleName = tablecell_rolename)
            self.log.info("* Check : Found General button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find General table cell")


        general.click()
        self.log.info("# Step  : Click on <<General>>")

        try:
            applyPref = preferences.child(name = apply_button, roleName = button_rolename)
            self.log.info("* Check : Found Apply push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find Apply push button")


        if (applyPref.sensitive):
            applyPref.click()
            self.log.info("# Step  : Click <<Apply>>")
        else:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("Apply push button not sensitive")

        try:
            ok = preferences.child(name=ok_button, roleName = button_rolename)
            self.log.info("* Check : Found OK push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find OK push button")


        if (ok.sensitive):
            ok.click()
            self.log.info("# Step  : Click <<OK>>")
        else:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("OK push button not sensitive")

        try:
            updateProfile = app.child(name = update_frame, roleName = frame_rolename)
            self.log.info("* Check : Found Update cross development profile frame")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find Update cross development profile frame")


        try:
            ok = updateProfile.child(name=ok_button, roleName = button_rolename)
            self.log.info("* Check : Found OK push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find OK push button")


        if (ok.sensitive):
            ok.click()
            self.log.info("# Step  : Click <<OK>>")
        else:
            cancel_close = updateProfile.child(name=cancel_button, roleName = button_rolename)
            self.log.info("* Check : Found Cancel push button")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find OK push button sensitive")


    def remove_yocto_profile(self, renameprofile):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        try:
            window = eclipse.child(name = window_menu, roleName = menu_rolename)
            self.log.info("* Check : Found Window menu")
        except:
            self.fail("can not find Window menu")
            

        window.click()
        self.log.info("# Step  : Click on menu <<Window>>")

        try:
            windowitem = window.child(name=preferences_item, roleName=menuitem_rolename)
            self.log.info("* Check : Found <<Preferences>> menu item")
        except:
            self.fail("can not find Preferences menu item")
            

        windowitem.click()
        self.log.info("# Step  : Click on menu item <<Preferences>>")

        try:
            preferences = app.child(name = preferences_frame, roleName = frame_rolename)
            self.log.info("* Check : Window Preferences is Open")
        except:
            self.fail("can not find Preferences frame")
            


        text = preferences.findChildren(predicate.GenericPredicate(roleName = text_rolename))
        nrText = len(text)
        if (nrText == 0):
            self.fail("can not find text boxes")
            
        cancel_close = preferences.child(name=cancel_button, roleName = button_rolename)

        try:
            yoctoProjectADT = app.child(name = YP_ADT_tablecell, roleName = tablecell_rolename)
            self.log.info("* Check : Found Yocto Project ADT button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find Yocto Project ADT table cell")


        yoctoProjectADT.click()
        self.log.info("# Step  : Click on <<Yocto Project ADT>>")

        comboBox = preferences.findChildren(predicate.GenericPredicate(roleName=combobox_rolename))
        if (len(comboBox) > 1):
            self.log.info("* Check : Found menu drop-down list Target Arhitecture")
            comboBox[0].click()
            self.log.info("# Step  : Click on menu drop-down list <<Target Arhitecture>>")
        else:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find combo boxes")

        try:
            preferences.child(name=renameprofile, roleName=menuitem_rolename).click()
            self.log.info("* Check : Found profile name menu item")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find profile name menu item")


        try:
            Remove = preferences.child(name = remove_button, roleName = button_rolename)
            self.log.info("* Check : Found Remove push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                time.sleep(2)
                cancel_close.click()
            

        Remove.click()
        self.log.info("# Step  : Click <<Remove>>")

        try:
            removeProfile = app.child(name = remove_frame, roleName = frame_rolename)
            self.log.info("* Check : Found Remove cross development profile frame")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find Remove cross development profile frame")


        try:
            ok = removeProfile.child(name=ok_button, roleName = button_rolename)
            self.log.info("* Check : Found OK push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find OK push button")


        ok.click()
        self.log.info("# Step  : Click <<OK>>")

        try:
            general = app.child(name = general_tablecell, roleName = tablecell_rolename)
            self.log.info("* Check : Found General button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find General table cell")


        general.click()
        self.log.info("# Step  : Click on <<General>>")

        try:
            applyPref = preferences.child(name = apply_button, roleName = button_rolename)
            self.log.info("* Check : Found Apply push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find Apply push button")


        if (applyPref.sensitive):
            applyPref.click()
            self.log.info("# Step  : Click <<Apply>>")
        else:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("Apply push button not sensitive")


        try:
            ok = preferences.child(name=ok_button, roleName = button_rolename)
            self.log.info("* Check : Found OK push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find OK push button")


        if (ok.sensitive):
            ok.click()
            self.log.info("# Step  : Click <<OK>>")
        else:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("OK push button not sensitive")



        try:
            updateProfile = app.child(name = update_frame, roleName = frame_rolename)
            self.log.info("* Check : Found Update cross development profile frame")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find Update cross development profile frame")


        try:
            ok = updateProfile.child(name=ok_button, roleName = button_rolename)
            self.log.info("* Check : Found OK push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find OK push button")


        if (ok.sensitive):
            ok.click()
            self.log.info("# Step  : Click <<OK>>")
        else:
            cancel = updateProfile.child(name=cancel_button, roleName = button_rolename)
            self.log.info("* Check : Found Cancel push button")
            if (cancel.sensitive):
                cancel.click()
            self.fail("can not find OK push button sensitive")


    def close_project(self):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        text = eclipse.findChildren(predicate.GenericPredicate(roleName = text_rolename))
        nrText = len(text)
        if (nrText == 0):
                self.fail("can not find text boxes")
                


        #text[nrText-1].click()
        #self.log.info("# Step  : Click on box <<Quick Access>>")
        #text[nrText-1].text='Close Project'
        #self.log.info("# Step  : Insert <<Close Project>> on box <<Quick Access>>")

        try:
            keyCombo("<<Shift><F10>") # Right Click
            pressKey("s")   # Shortcut for close Project
            #reconfig = app.child(name = 'Close Project - Close the selected project', roleName = tablecell_rolename)
            self.log.info("* Check : Found Close Project")
        except:
            self.fail("can not find Close Project table cell")
            

        #reconfig.click()
        #self.log.info("# Step  : Click on box <<Close Project>>")

    def delete_project(self, projectname, typeproject):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        keyCombo("<<Esc>")
        keyCombo("<<Esc>")
        try:
            project = eclipse.child(name = projectname, roleName=tablecell_rolename)
            self.log.info("* Check : Found <<" +str(projectname) + ">> table cell")
        except:
            self.fail("can not find " +str(projectname) + " table cell")
            

        project.click()
        self.log.info("* Step  : Click on project <<" +str(projectname) + ">>")

        keyCombo("<<Esc>")
        keyCombo("<<Esc>")
        keyCombo("<<Shift><F10>")
        time.sleep(2)
        keyCombo("Down")
        keyCombo("Down")
        pressKey("d")
        time.sleep(2)
        pressKey("Enter")   # Delete project

        try:
            deleteresources = app.child(name=delete_frame, roleName=frame_rolename)
            self.log.info("* Check : Found <<Delete Resources>> frame")
        except:
            self.fail("can not find Delete Resources frame")
            

        time.sleep(3)

        if "New Yocto Project" in typeproject:
            pass
        else:
            deletecombobox = deleteresources.findChildren(predicate.GenericPredicate(roleName=checkbox_rolename))
            deletecombobox[0].click()
            self.log.info("# Step  : Click on check box <<Delete project contents on disk>>")

        try:
            ok = deleteresources.child(name=ok_button, roleName = button_rolename)
            self.log.info("* Check : Found OK push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = deleteresources.child(name = cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find OK push button")


        ok.click()
        self.log.info("# Step  : Click on button <<OK>>")

        frames = app.findChildren(predicate.GenericPredicate(roleName = frame_rolename))
        if (len(frames) == 0):
            self.fail("can not find frames")
            

        found = 1
        try:
            deleteresources = frames[2] #app.child(name=delete_frame, roleName=frame_rolename)
            self.log.info("* Check : Found <<Delete Resources>> frame")
        except:
            found = 0

        if found == 1:
            try:
                continuebutton = deleteresources.child(name=continue_button, roleName = button_rolename)
                self.log.info("* Check : Found Continue push button")
            except:
                self.log.info("can not find Continue push button")
                

            if (continuebutton.sensitive):
                self.log.info("* Check : Found Continue push button sensitive")
                time.sleep(2)
                continuebutton.click()
                self.log.info("# Step  : Click on button <<Continue>>")
            else:
                self.fail("Continue push button not sensitive")
                

    def close_perspective(self):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        try:
            window = eclipse.child(name = window_menu, roleName = menu_rolename)
            self.log.info("* Check : Found Window menu")
        except:
            self.fail("can not find Window menu")
            
        time.sleep(2)

        window.click()
        self.log.info("# Step  : Click on menu <<Window>>")

        if eclipse_version == "mars":

            try:
                perspective = window.child(name = perspective_menu, roleName = menu_rolename)
                self.log.info("* Check : Found Perspective menu")
            except:
                self.fail("can not find Window menu")
                

            perspective.select()
            self.log.info("# Step  : Click on menu <<Perspective>>")

            try:
                perspectiveitem = perspective.child(name=closeperspective_item, roleName=menuitem_rolename)
                self.log.info("* Check : Found <<Close Perspective>> menu item")

            except:
                self.fail("can not find Close Perspective menu item")
                
            time.sleep(3)
            perspectiveitem.click()
            self.log.info("# Step  : Click on menu item <<Close Perspective>>")

        else:
            try:
                windowitem = window.child(name=closeperspective_item, roleName=menuitem_rolename)
                self.log.info("* Check : Found <<Close Perspective>> menu item")
            except:
                self.fail("can not find Close Perspective menu item")
                

            windowitem.click()
            self.log.info("# Step  : Click on menu item <<Close Perspective>>")


    def set_network_preferences_to_direct(self):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        try:
            window = eclipse.child(name = window_menu, roleName = menu_rolename)
            self.log.info("* Check : Found Window menu")
        except:
            self.fail("can not find Window menu")
            

        window.click()
        self.log.info("# Step  : Click on menu <<Window>>")

        try:
            windowitem = window.child(name=preferences_item, roleName=menuitem_rolename)
            self.log.info("* Check : Found <<Preferences>> menu item")

        except:
            self.fail("can not find Preferences menu item")
            

        windowitem.click()
        self.log.info("# Step  : Click on menu item <<Preferences>>")

        try:
            preferences = app.child(name = preferences_frame, roleName = frame_rolename)
            self.log.info("* Check : Window Preferences is Open")
        except:
            self.fail("can not find Preferences frame")
            
        cancel_close = preferences.child(name = cancel_button, roleName = button_rolename)

        text = preferences.findChildren(predicate.GenericPredicate(roleName = text_rolename))
        nrText = len(text)
        if (nrText == 0):
            self.fail("can not find text boxes")
            

        time.sleep(3)
        typeText("Network Connections")
        time.sleep(3)
        keyCombo("Down")
        keyCombo("Down")
        self.log.info("# Step  : Select <<Network Connections>>")

        comboBox = preferences.findChildren(predicate.GenericPredicate(roleName=combobox_rolename))
        if (len(comboBox) < 1):
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find combo boxes")

        else:
            self.log.info("* Check : Found drop-down list ")

            comboBox[0].click()
            self.log.info("# Step  : Click on menu drop-down list <<Active Provider>>")

        try:
            directitem = preferences.child(name=direct_item, roleName=menuitem_rolename)
            self.log.info("* Check : Found Direct menu item")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                #cancel_close.click()
                cancel_close.doubleClick()
            self.fail("can not find Direct menu item")


        directitem.click()
        self.log.info("# Step  : Click on <<Direct>> menu item")

        try:
            applyPref = preferences.child(name = apply_button, roleName = button_rolename)
            self.log.info("* Check : Found Apply push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find Apply push button")


        try:
            general = app.child(name = general_tablecell, roleName = tablecell_rolename)
            self.log.info("* Check : Found General button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                time.sleep(2)
                cancel_close.click()
            self.fail("can not find General table cell")


        general.click()
        self.log.info("# Step  : Click on <<General>>")

        if (applyPref.sensitive):
            self.log.info("* Check : Found Apply push button sensitive")

            applyPref.click()
            self.log.info("# Step  : Click <<Apply>>")
        else:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("Apply push button not sensitive")


        try:
            ok = preferences.child(name=ok_button, roleName = button_rolename)
            self.log.info("* Check : Found OK push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find OK push button")


        if (ok.sensitive):
            self.log.info("* Check : Found OK push button sensitive")
            ok.click()
            self.log.info("# Step  : Click <<OK>>")
        else:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("OK push button not sensitive")



    def build_project(self):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        try:
            project = eclipse.child(name = project_menu, roleName = menu_rolename)
            self.log.info("* Check : Found Project menu")
        except:
            self.fail("can not find Project menu")
            

        project.click()
        self.log.info("# Step  : Click on menu <<Project>>")

        try:
            build = project.child(name=buildproject_item, roleName=menuitem_rolename)
            self.log.info("* Check : Found Build Project menu item")
        except:
            self.fail("can not find Build Project menu item")
            

        if (build.sensitive):
            build.click()
            self.log.info("# Step  : Click on menu item <<Build Project>>")
        else:
            self.fail("Build Project menu item not sensitive")
            


    def launch_qemu_from_eclipse(self):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        try:
            run = eclipse.child(name = run_menu, roleName = menu_rolename)
            self.log.info("* Check : Found Run menu")
        except:
            self.fail("can not find Run menu")
            

        run.select()
        self.log.info("# Step  : Select <<Run>> menu")

        try:
            externalTools = run.child(name = externaltools_menu, roleName = menu_rolename)
            self.log.info("* Check : Found Run External Tools menu")
        except:
            self.fail("can not find External Tools menu")
            

        externalTools.select()
        self.log.info("# Step  : Select <<External Tools>> menu")

        externalTools.deselect()
        self.log.info("# Step  : Exit <<External Tools>> menu")

        run.deselect()
        self.log.info("# Step  : Exit <<Run>> menu")

        try:
            run = eclipse.child(name = run_menu, roleName = menu_rolename)
            self.log.info("* Check : Found Run menu")
        except:
            self.fail("can not find Run menu")
            

        run.select()
        self.log.info("# Step  : Select <<Run>> menu")

        try:
            externalTools = run.child(name = externaltools_menu, roleName = menu_rolename)
            self.log.info("* Check : Found Run External Tools menu")
        except:
            self.fail("can not find External Tools menu")
            

        externalTools.select()
        self.log.info("# Step  : Select <<External Tools>> menu")

        try:
            qemu = externalTools.child(name = qemu_item , roleName = menuitem_rolename)

            self.log.info("* Check : Found <<1 qemu_i586-poky-linux>> menu item")
        except:
            try:
                qemu = externalTools.child(name = qemu2_item , roleName = menuitem_rolename)
                self.log.info("* Check : Found <<1 qemu_i586-poky-linux>> menu item")
            except:
                if eclipse_version == 'mars':
                    pass
                else:
                    self.fail("can not find qemu menu item")  ###
                

        #qemu.click()
        #time.sleep(3)


        #self.log.info("# Step  : Click on menu item <<1 qemu_i586-poky-linux>>")
        #time.sleep(2)

        externalTools.deselect()
        self.log.info("# Step  : Exit <<External Tools>> menu")
        time.sleep(3)

        run.deselect()
        self.log.info("# Step  : Exit <<Run>> menu")


    def new_connection_for_run(self,eclipse_version):


        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        runConfig = app.child(name=runconfiguration_frame, roleName=frame_rolename)

        inifile = IniParser()
        ip = inifile.getValue("settings-eclipse.ini", "SSH", "ip")
        conncectionId = datetime.now().strftime("-%d-%m-%Y %H:%M:%S")
        connection = ip +' SSH ' + conncectionId

        try:
            new = runConfig.child(name = new_button, roleName = button_rolename)
            self.log.info("* Check : Found New push button")
        except:
            self.fail("can not find New push button")
            

        new.click()
        self.log.info("# Step  : Click on <<New...>push button")

        newConnection = app.child(name=newconnection_frame, roleName = frame_rolename)
        text = newConnection.findChildren(predicate.GenericPredicate(roleName = text_rolename))

        text[0].click()
        self.log.info("# Step  : Click on box <<System type>>")
        text[0].text = 'SSH Only'
        self.log.info("* Check : Insert <<SSH Only>> as System type")


        try:
            sshOnly = newConnection.child(name = ssh_tablecell, roleName = tablecell_rolename)
            self.log.info("* Check : Found SSH Only table cell")
        except:
            self.fail("can not find SSH Only table cell")
                

        sshOnly.click()
        self.log.info("# Step  : Click on box <<System type>>")

        try:
            next = newConnection.child(name = next_button, roleName = button_rolename)
            self.log.info("* Check : Found Next push button")
        except:
            self.fail("can not find Next push button")
            

        next.click()
        self.log.info("# Step  : Click <<Next>>")

        text = newConnection.findChildren(predicate.GenericPredicate(roleName = text_rolename))
        nrText = len(text)
        if (nrText == 0):
            self.fail("can not find text boxes")

        if eclipse_version == 'kepler' or eclipse_version == 'luna':
            text[0].click()
        else:
            pass

        keyCombo("<<Ctrl><a>")


        self.log.info("# Step  : Click on box <<Host name>>")
        #text[0].text =  ip
        typeText(ip)
        #text[0].text =  ip
        self.log.info("* Check : Insert ip of QEMU as hostname")


        if eclipse_version == 'kepler' or eclipse_version == 'luna':
            text[1].click()
            self.log.info("# Step  : Click on box <<Connection name>>")
            text[1].text = connection
            self.log.info("* Check : Insert Connection name")

        else:
            text[2].click()
            self.log.info("# Step  : Click on box <<Connection name>>")
            text[2].text = connection
            self.log.info("* Check : Insert Connection name")


        #text[0].click()
        #text[0].text =  ip

        try:
            finish = newConnection.child(name = finish_button, roleName = button_rolename)
            self.log.info("* Check : Found Finish push button")
        except:
            self.fail("can not find Finish push button")
            

        finish.click()
        self.log.info("# Step  : Click on box <<Finish>>")


    def run_project(self , projectname, searchtype, eclipse_version):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        text = eclipse.findChildren(predicate.GenericPredicate(roleName = text_rolename))
        nrText = len(text)
        if (nrText == 0):
            self.fail("can not find text boxes")
            

        try:
            run = eclipse.child(name = run_menu, roleName = menu_rolename)
            self.log.info("* Check : Found Run menu")
        except:
            self.fail("can not find Run menu")
            

        run.select()
        self.log.info("# Step  : Click on menu <<Run>>")

        try:
            runitem = run.child(name=runconfiguration_item, roleName=menuitem_rolename)
            self.log.info("* Check : Found <<Run Configurations...>> menu item")
        except:
            self.fail("can not find Run Configurations menu item")
            

        time.sleep(3)
        runitem.click()
        self.log.info("# Step  : Click on menu item <<Run Configurations...>>")

        try:
            runConfig = app.child(name=runconfiguration_frame, roleName=frame_rolename)
            self.log.info("* Check : Found <<Run Configurations>> frame")
        except:
            self.fail("can not find Run Configurations frame")
            

        time.sleep(3)
        typeText(str(projectname))

        time.sleep(10)
        keyCombo("Enter")


        self.new_connection_for_run(eclipse_version)
        self.log.info("# Step  : Create a new Connection")

        text = runConfig.findChildren(predicate.GenericPredicate(roleName = text_rolename))

        if (len(text) < 6):
            self.fail("can not find text boxes")
            
        if eclipse_version=="mars":
            text[4].click()
            self.log.info("# Step  : Click on box <<Remote Absolute File Path for C/C++ App>>")
            text[4].text = '/home/root/' + str(projectname)
            self.log.info("* Check : Insert Remote Absolute File Path for C/C++ App")
        else:
            text[5].click()
            self.log.info("# Step  : Click on box <<Remote Absolute File Path for C/C++ App>>")
            text[5].text = '/home/root/' + str(projectname)
            self.log.info("* Check : Insert Remote Absolute File Path for C/C++ App")

        if "Hello World GTK C" in str(searchtype):
            if eclipse_version=='mars':
                text[5].click()
                text[5].text = 'export DISPLAY=:0.0'
            else:
                text[6].click()
                text[6].text = 'export DISPLAY=:0.0'

        cancel_close = runConfig.child(name = close_button, roleName = button_rolename)

        try:
            run = runConfig.child(name=run_button, roleName = button_rolename)
            self.log.info("* Check : Found Run push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find Run push button")


        if (run.sensitive):
            self.log.info("* Check : Found Run push button sensitive")
            run.click()
            self.log.info("# Step  : Click on button <<Run>>")
        else:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                    cancel_close.click()
            self.fail("Run push button not sensitive")


        found = 1
        try:
            enterPassword =  app.child(name=enterpassword_frame, roleName=frame_rolename)
            self.log.info("* Check : Found <<Enter Password>> frame")
        except:
            found = 0

        if found == 1:
            text = enterPassword.findChildren(predicate.GenericPredicate(roleName = text_rolename))
            if (len(text) == 0):
                self.fail("can not find text boxes")
                
            text[0].click()
            self.log.info("# Step  : Click on box <<User ID>>")
            text[0].text = 'root'
            self.log.info("* Check : Insert <<root>> in <<User ID>> box")

            try:
                ok = enterPassword.child(name=ok_button, roleName = button_rolename)
                self.log.info("* Check : Found OK push button")
            except:
                self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
                cancel_close = enterPassword.child(name = cancel_button, roleName = button_rolename)
                if (cancel_close.sensitive):
                    cancel_close.click()
                self.fail("can not find OK push button")


            if (ok.sensitive):
                self.log.info("* Check : Found OK push button sensitive")
                ok.click()
                self.log.info("# Step  : Click on button <<OK>>")
            else:
                self.fail("OK push button not sensitive")
                

        found = 1
        try:
            warning =  app.child(name=warning_frame, roleName=frame_rolename)
            self.log.info("* Check : Found <<Warning>> frame")
        except:
            found = 0
        if found == 1:
            try:
                yes = warning.child(name=yes_button, roleName = button_rolename)
                self.log.info("* Check : Found Yes push button")
            except:
                self.fail("can not find Yes push button")
                

            if (yes.sensitive):
                self.log.info("* Check : Found Yes push button sensitive")
                yes.click()
                self.log.info("# Step  : Click on button <<Yes>>")
            else:
                self.fail("Yes push button not sensitive")
                

        if "Hello World GTK C" in str(searchtype):

            var = subprocess.check_output("ssh root@192.168.7.2 \"ps -x | grep " + str(projectname) + "\"", shell=True)
            expectedmessage = '/home/root/' + str(projectname)
            if str(expectedmessage) in str(var):
                self.log.info("* Check : Message from QEMU: " + str(expectedmessage) )

                subprocess.check_output("ssh root@192.168.7.2 \"killall " + str(projectname) + "\"", shell=True)
                self.log.info("# Step  : Kill process: " + str(expectedmessage) + "")
        else:
            var = subprocess.check_output("ssh root@192.168.7.2 \"./" + str(projectname) + "\"", shell=True)
            self.log.info("* Check : Message from QEMU: " + str(var))


    def change_profile_on_selected_project(self, projectname, newprofileName):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        try:
            project = eclipse.child(name = project_menu, roleName = menu_rolename)
            self.log.info("* Check : Found Project menu")
        except:
            self.fail("can not find Project menu")
            

        project.click()
        self.log.info("# Step  : Click on menu <<Project>>")

        try:
            changeYPSettings = project.child(name = changeYPsettings_item, roleName = menuitem_rolename)
            self.log.info("* Check : Found Change Yocto Project Settings menu item")
        except:
            keyCombo("<<Esc>")
            self.reconfigure_project(projectname)
            try:
                changeYPSettings = project.child(name = changeYPsettings_item, roleName = menuitem_rolename)
                self.log.info("* Check : Found Change Yocto Project Settings menu item")
            except:
                self.fail("can not find Change Yocto Project Settings menu item")
                

        changeYPSettings.click()
        self.log.info("# Step  : Select <<Change Yocto Project Settings menu >> menu item")

        try:
            projectProperties = app.child(name = projectproperties_frame + projectname + " ", roleName = frame_rolename)
            self.log.info("* Check : Window Properties for " + str(projectname) + " is Open")
        except:
            self.fail("can not find Properties for " + str(projectname) + " frame")
            
        cancel_close = projectProperties.child(name = cancel_button, roleName = button_rolename)
        comboBox = projectProperties.findChildren(predicate.GenericPredicate(roleName=combobox_rolename))

        if (len(comboBox) > 1):
            self.log.info("* Check : Found menu drop-down list Target Arhitecture")
            comboBox[0].click()
            self.log.info("# Step  : Click on menu drop-down list <<Target Arhitecture>>")
        else:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find combo boxes")

        try:
            projectProperties.child(name=newprofileName, roleName=menuitem_rolename).click()
            self.log.info("* Check : Found profile name menu item")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find profile name menu item")


        try:
            applyPref = projectProperties.child(name = apply_button, roleName = button_rolename)
            self.log.info("* Check : Found Apply push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find Apply push button")


        if (applyPref.sensitive):
            applyPref.doubleClick()
            self.log.info("# Step  : Click <<Apply>> to save Standard Profile")
        else:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("Apply push button not sensitive")


        try:
            ok = projectProperties.child(name=ok_button, roleName = button_rolename)
            self.log.info("* Check : Found OK push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find OK push button")


        if (ok.sensitive):
            ok.click()
            self.log.info("# Step  : Click <<OK>>")
        else:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("OK push button not sensitive")


    def debug_project(self, projectname, searchtype):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        text = eclipse.findChildren(predicate.GenericPredicate(roleName = text_rolename))
        nrText = len(text)
        if (nrText == 0):
            self.fail("can not find text boxes")
            
        try:
            run = eclipse.child(name = run_menu, roleName = menu_rolename)
            self.log.info("* Check : Found Run menu")
        except:
            self.fail("can not find Run menu")
            

        run.click()
        self.log.info("# Step  : Click on menu <<Run>>")

        try:
            debugitem = run.child(name=debugconfiguration_item, roleName=menuitem_rolename)
            self.log.info("* Check : Found <<Debug Configurations...>> menu item")
        except:
            self.fail("can not find Debug Configurations menu item")
            

        debugitem.click()
        self.log.info("# Step  : Click on menu item <<Debug Configurations...>>")

        try:
            debugConfig = app.child(name=debugconfiguration_frame, roleName=frame_rolename)
            self.log.info("* Check : Found <<Debug Configurations>> frame")
        except:
            self.fail("can not find Debug Configurations frame")


        text = debugConfig.findChildren(predicate.GenericPredicate(roleName = text_rolename))
        nrText = len(text)

        if (len(text) < 1):
            self.fail("can not find text boxes")
            

        text[0].click()
        #text[0].text = projectname

        typeText(str(projectname))
        #self.log.info("# Step  : Insert <<"+ str(projectname)+">> name of project to debug")

        try:
            debug = debugConfig.child(name=debug_button, roleName = button_rolename)
            self.log.info("* Check : Found Debug push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = debugConfig.child(name = cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                time.sleep(2)
                cancel_close.click()
            self.fail("can not find Debug push button")


        if (debug.sensitive):
            self.log.info("* Check : Found Debug push button sensitive")
            debug.click()
            self.log.info("# Step  : Click on button <<Debug>>")
        else:
            self.log.warning("# Warning  : Click <<Close>> and jump to next step")
            cancel_close = debugConfig.child(name = close_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("Debug push button not sensitive")


        found = 1
        try:
            confirm =  app.child(name=confirmperspectiveswitch_frame, roleName=frame_rolename)
            self.log.info("* Check : Found <<Confirm Perspective Switch >> frame")
        except:
            found = 0

        if found == 1:
            try:
                yes = confirm.child(name=yes_button, roleName = button_rolename)
                self.log.info("* Check : Found Yes push button")
            except:
                self.fail("can not find Yes push button")
                

            if (yes.sensitive):
                self.log.info("* Check : Found Yes push button sensitive")
                yes.doubleClick()
                self.log.info("# Step  : Click on button <<Yes>>")
            else:
                self.fail("Yes push button not sensitive")
                

        time.sleep(20)

        #var = subprocess.check_output("ssh root@192.168.7.2 \"ps -ef | grep gdbserver " + str(projectname) + "\"", shell=True)
        #print var
        if eclipse_version == 'mars':
            var = subprocess.check_output("ssh root@192.168.7.2 \"killall gdbserver\"", shell=True)
            self.log.info("# Step  : Kill gdbserver open by  : " + str(projectname) + "")
        else:
            if "Hello World GTK C" in str(searchtype):
                var = subprocess.check_output("ssh root@192.168.7.2 \"killall gdbserver\"", shell=True)
                self.log.info("# Step  : Kill gdbserver open by  : " + str(projectname) + "")


        self.close_perspective()
        self.log.info("# Step  : Close Debug perspective")

        found = 1
        try:
            dateforgdb = datetime.now().strftime("%m/%d/%y, %I:%M %p")
            gdbserver =  app.child(name= gdbserverdebugger_frame + dateforgdb, roleName=frame_rolename)
            self.log.info("* Check : Found <<"+ gdbserverdebugger_frame+">> frame")
        except:
            found = 0
        if found == 1:
            try:
                details = gdbserver.child(name=details_button, roleName = button_rolename)
                self.log.info("* Check : Found Details push button")
            except:
                self.fail("can not find Details push button")
                

            if (details.sensitive):
                self.log.info("* Check : Found Details push button sensitive")
                details.click()
                self.log.info("# Step  : Click on button <<Details>>")
            else:
                self.fail("Details push button not sensitive")
                

            found = 1
            try:
                errorconnection =  gdbserver.child(name= error_connection_closed, roleName=tablecell_rolename)
            except:
                found = 0
            if found == 1:
                self.log.info("* Warning : Found" + error_connection_closed +"   ?????")
            try:
                ok = gdbserver.child(name=ok_button, roleName = button_rolename)
                self.log.info("* Check : Found OK push button")
            except:
                self.fail("can not find OK push button")
                self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
                cancel_close = gdbserver.child(name = cancel_button, roleName = button_rolename)
                if (cancel_close.sensitive):
                    cancel_close.click()
                

            ok.click()
            self.log.info("# Step  : Click on button <<OK>>")

    def open_other_perspective(self, perspectivename):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        try:
            window = eclipse.child(name = window_menu, roleName = menu_rolename)
            self.log.info("* Check : Found Window menu")
        except:
            self.fail("can not find Window menu")
            

        window.click()
        self.log.info("# Step  : Click on menu <<Window>>")

        try:
            windowitem = window.child(name=openperspective_menu, roleName=menu_rolename)
            self.log.info("* Check : Found <<Open Perspective>> menu")
        except:
            self.fail("can not find Open Perspective menu")
            

        windowitem.select()
        self.log.info("# Step  : Select menu <<Open Perspective>>")

        try:
            otheritem = windowitem.child(name=other_item, roleName=menuitem_rolename)
            self.log.info("* Check : Found <<Other...>> menu item")

        except:
            self.fail("can not find Other... menu item")
            

        otheritem.click()
        self.log.info("# Step  : Click on menu item <<Other...>>")

        try:
            OpenPerspective = app.child(name = openp_other_erspective_frame, roleName = frame_rolename)
            self.log.info("* Check : Open Perspective is Open")
        except:
            self.fail("can not find Open Perspective frame")
            

        try:
            perspectiveitem = OpenPerspective.child(name = perspectivename, roleName=tablecell_rolename)
            self.log.info("* Check : Found <<" +str(perspectivename) + ">> table cell")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = OpenPerspective.child(name = cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find " +str(perspectivename) + " table cell")


        perspectiveitem.click()
        self.log.info("# Step  : Click on perspective <<" + str(perspectivename) +">>")

        try:
            ok = OpenPerspective.child(name=ok_button, roleName = button_rolename)
            self.log.info("* Check : Found OK push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = OpenPerspective.child(name = cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find OK push button")


        ok.click()
        self.log.info("# Step  : Click on button <<OK>>")

        try:
            perspectiveButton = eclipse.child(name = perspectivename, roleName = togglebutton_rolename)
            self.log.info("* Check : Found <<" +str(perspectivename) + ">> toggle button")
        except:
            self.fail("can not find " +str(perspectivename) + ">> toggle button")
            

        perspectiveButton.click()
        self.log.info("# Step  : Click on <<" +str(perspectivename) + ">>")
        self.log.info("# Step  : Perspective <<" +str(perspectivename) + ">> is open")

    def create_yocto_project(self, projectname, projectlocation, typeproject):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)
        try:
            project = eclipse.child(name = file_menu, roleName = menu_rolename)
            self.log.info("* Check : Found File menu")

        except:
            self.fail("can not find File menu")
            

        project.click()
        self.log.info("# Step  : Click on menu <<File>>")

        try:
            newmenu = project.child(name = new_menu, roleName = menu_rolename)
            self.log.info("* Check : Found New menu")
        except:
            self.fail("can not find New menu")
            

        newmenu.select()
        self.log.info("# Step  : Select <<New>> menu")

        try:
            projectitem = newmenu.child(name = project_item , roleName = menuitem_rolename)
            self.log.info("* Check : Found <<Project...>> menu item")
        except:
            self.fail("can not find Project... menu item")
            

        projectitem.click()
        self.log.info("# Step  : Click on menu item <<Project...>>")

        try:
            new_proj = app.child(name = new_project_frame, roleName = frame_rolename)
            self.log.info("* Check : New Project frame")
        except:
            self.fail("can not find New Project frame")



        text = new_proj.findChildren(predicate.GenericPredicate(roleName = text_rolename))
        text[0].click()
        self.log.info("# Step  : Click on box <<Wizards>>")
        text[0].text = typeproject
        self.log.info("* Check : Insert type of project")

        try:
            next = new_proj.child(name = next_button, roleName = button_rolename)
            self.log.info("* Check : Found Next push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = new_proj.child(name = cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("can not find Next push button")


        time.sleep(10)

        if (next.sensitive):
            self.log.info("* Check : Found Next push button sensitive")
            #next.doubleClick()
            next.click()
            self.log.info("# Step  : Click <<Next>>")
        else:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = new_proj.child(name = cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("Next push button not sensitive")


        try:
            BBCProject = app.child(name = yoctoBBcommander_frame, roleName = frame_rolename)
            self.log.info("* Check : Found Yocto Project Bitbake Commander frame")
        except:
            self.fail("can not find Yocto Project Bitbake Commanderframe")
            

        text = BBCProject.findChildren(predicate.GenericPredicate(roleName = text_rolename))

        text[1].click()
        self.log.info("# Step  : Click on box <<Project Name >>")
        text[1].text = projectname
        self.log.info("* Check : Insert name of project")

        text[2].click()
        self.log.info("# Step  : Click on box <<Project Location>>")
        text[2].text = projectlocation
        self.log.info("* Check : Insert location of project")


        try:
            finish = BBCProject.child(name = finish_button, roleName = button_rolename)
            self.log.info("* Check : Found Finish push button")
        except:
            self.fail("can not find Finish push button")
            

        finish.click()
        self.log.info("# Step  : Click on box <<Finish>>")

    def add_bitbake_recipe(self, projectname, srcURI, description, recipelicense, recipename, pressPopulate):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)
        try:
            project = eclipse.child(name = projectname, roleName=tablecell_rolename)
            self.log.info("* Check : Found <<" +str(projectname) + ">> table cell")
        except:
            self.fail("can not find " +str(projectname) + " table cell")
            

        project.click()
        self.log.info("* Step : Click on project <<" +str(projectname) + ">>")

        try:
            file = eclipse.child(name = file_menu, roleName = menu_rolename)
            self.log.info("* Check : Found File menu")
        except:
            self.fail("can not find File menu")
            

        file.click()
        self.log.info("# Step  : Click on menu <<File>>")

        try:
            newmenu = file.child(name = new_menu, roleName = menu_rolename)
            self.log.info("* Check : Found New menu")
        except:
            self.fail("can not find New menu")
            

        newmenu.select()
        self.log.info("# Step  : Select <<New>> menu")

        try:
            projectitem = newmenu.child(name = bitbakerecipe_item , roleName = menuitem_rolename)
            self.log.info("* Check : Found <<BitBake Recipe>> menu item")
        except:
            self.fail("can not find BitBake Recipe menu item")
            

        projectitem.click()
        self.log.info("# Step  : Click on menu item <<Project...>>")

        frames = app.findChildren(predicate.GenericPredicate(roleName = frame_rolename))
        if (len(frames) == 0):
            self.fail("can not find frames")

        bbrecipe = frames[1]
        text = bbrecipe.findChildren(predicate.GenericPredicate(roleName = text_rolename ))

        text[0].click()
        self.log.info("# Step  : Click on box <<Recipe Directory>>")
        recipe_directory = "/" + str(projectname)

        if text[0].text == recipe_directory :
            self.log.info("* Check : Recipe directory is correct")
        else:
            self.fail("Other recipe directory")

        text[1].click()
        self.log.info("# Step  : Click on box <<SRC_URI>>")
        text[1].text = srcURI
        self.log.info("* Check : Insert SRC_URI")


        text[6].click()
        self.log.info("# Step  : Click on box <<Description>>")
        text[6].text = description
        self.log.info("* Check : Insert Description")


        text[7].click()
        self.log.info("# Step  : Click on box <<License>>")
        text[7].text = recipelicense
        self.log.info("* Check : Insert License")


        try:
            finish = bbrecipe.child(name = finish_button, roleName = button_rolename)
            self.log.info("* Check : Found Finish push button")
        except:
            self.fail("can not find Finish push button")
            

        if pressPopulate:
            try:
                populate = bbrecipe.child(name = populate_button, roleName = button_rolename)
                self.log.info("* Check : Found Populate... push button")
            except:
                self.fail("can not find Populate... push button")
                

            populate.click()
            self.log.info("# Step  : Click on box <<Populate...>>")
            time.sleep(20)

            if text[2].text == recipename:
                self.log.info("* Check : Recipe Name is correct")
            else:
                self.fail("Recipe Name is not correct")

            self.log.info("# Step  : Click on box SRC_URI[md5sum]")
            text[3].click()
            self.log.info("# Step  : Text in box SRC_URI[md5sum]: %s" %(text[3].text) )

            self.log.info("# Step  : Click on box SRC_URI[sha255sum]")
            text[4].click()
            self.log.info("# Step  : Text on box SRC_URI[sha255sum]: %s" %(text[4].text) )

            self.log.info("# Step  : Click on Lincense File CheckSum")
            text[5].click()
            self.log.info("# Step  : Text on box SRC_URI[sha255sum]: %s" %(text[5].text) )
        else:
            text[2].click()
            self.log.info("# Step  : Click on box <<Recipe Name>>")
            text[2].text = recipename
            self.log.info("* Check : Insert Recipe Name")

        finish.click()
        self.log.info("# Step  : Click on button <<Finish>>")

        time.sleep(3)
        text = eclipse.findChildren(predicate.GenericPredicate(roleName = text_rolename))
        nrText = len(text)

        if (nrText == 0):
            self.fail("can not find text boxes")
            

        if eclipse_version == 'mars':
            text[nrText-1].click()
            self.log.info("# Step  : Click on " + str(projectname) + " Console")
            time.sleep(3)
            self.log.info("# Step  : Output from " + str(projectname) + " Console: %s" %((text[nrText-1].text)))
        else:
            text[nrText-2].click()
            self.log.info("# Step  : Click on <<" + str(projectname) + ">> Console")
            time.sleep(3)
            self.log.info("# Step  : Output from " + str(projectname) + " Console: %s "%(text[nrText-2].text))

        try:
            clearconsole = eclipse.child(description=clear_console_description, roleName = button_rolename)
            self.log.info("* Check : Found Clear Console push button")
        except:
            self.fail("can not find Clear Console push button")
            

        clearconsole.click()
        self.log.info("# Step  : Click on button <<Clear Console>>")

        project.actions['expand or contract'].do()
        self.log.info("# Step  : Expand or contract")

        project.grabFocus()
        project.typeText(recipename)
        self.log.info("# Step  : Search " + str(recipename) + "")

        try:
            foundrecipe = eclipse.child(name = recipename, roleName = tablecell_rolename)
            self.log.info("* Check : Found recipe: " + str(recipename) + " in BitBake Project <<" + str(projectname) + ">>")
        except:
            self.fail("can not find " + str(recipename) + "in BitBake Project <<" + str(projectname) + ">>")
            

        foundrecipe.click()
        self.log.info("# Step  : Click on recipe file " + str(recipename) + "")

        project.actions['expand or contract'].do()
        self.log.info("# Step  : Expand or contract")

        project.click()
        self.log.info("* Step  : Click on project <<" +str(projectname) + ">>")


    def start_HOB_or_toaster(self,eclipse_version):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        try:
            project = eclipse.child(name = project_menu, roleName = menu_rolename)
            self.log.info("* Check : Found Project menu")
        except:
            self.fail("can not find Project menu")
            

        project.select()
        self.log.info("# Step  : Click on menu <<Project>>")

        if eclipse_version == 'kepler':

            try:
                projectitem = project.child(name=launchHob_item, roleName=menuitem_rolename)
                self.log.info("* Check : Found <<Launch HOB>> menu item")
            except:
                project.deselect()
                time.sleep(10)
                project.select()
                self.log.info("# Step  : Click on menu <<Project>>")

            time.sleep(3)
            projectitem.click()
            self.log.info("# Step  : Click on menu item <<Launch HOB>>")

            try:
                Launch_HOB = app.child(name = launchHob_frame, roleName = frame_rolename)
                self.log.info("* Check : Window Launch HOB is Open")
            except:
                self.fail("can not find Launch HOB frame")
                

            try:
                ok = Launch_HOB.child(name=ok_button, roleName = button_rolename)
                self.log.info("* Check : Found OK push button")
            except:
                self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
                cancel_close = Launch_HOB.child(name = cancel_button, roleName = button_rolename)
                if (cancel_close.sensitive):
                    cancel_close.click()
                self.fail("can not find OK push button")


            if (ok.sensitive):
                self.log.info("* Check : Found OK push button sensitive")
                time.sleep(2)
                ok.click()
                self.log.info("# Step  : Click on button <<OK>>")
            else:
                self.fail("OK push button not sensitive")
                

            time.sleep(10)

            app2 = tree.root.application('bitbake')

            try:
                Hob =  app2.child(name = 'Hob', roleName='frame')
                self.log.info("* Check : Window %s is Open " %Hob)
            except:
                self.fail("FAIL: can not find %s frame " %Hob)

            os.system("killall hob")


        elif eclipse_version == 'luna':

            try:
                projectitem = project.child(name=launchToaster_item, roleName=menuitem_rolename)
                self.log.info("* Check : Found <<Launch Toaster>> menu item")
            except:
                project.deselect()
                time.sleep(10)
                project.select()
                self.log.info("# Step  : Click on menu <<Project>>")

            time.sleep(3)
            projectitem.click()
            self.log.info("# Step  : Click on menu item <<Launch Toaster>>")

            frames = app.findChildren(predicate.GenericPredicate(roleName = frame_rolename))
            if (len(frames) == 0):
                self.fail("can not find frames")

            Launch_Toaster = frames[1]
            text = Launch_Toaster.findChildren(predicate.GenericPredicate(roleName = text_rolename ))

            text[0].click()
            self.log.info("# Step  : Click on box <<Toaster Server URL>")

            link_toaster = 'https://www.yoctoproject.org/toaster/'

            if text[0].text == link_toaster :
                self.log.info("* Check : Toaster Server URL is correct")

            else:
                text[0].click()
                text[0].text = link_toaster
            try:
                ok = Launch_Toaster.child(name=ok_button, roleName = button_rolename)
                self.log.info("* Check : Found OK push button")
            except:
                self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
                cancel_close = Launch_Toaster.child(name = cancel_button, roleName = button_rolename)
                if (cancel_close.sensitive):
                    cancel_close.click()
                self.fail("can not find OK push button")


            if (ok.sensitive):
                self.log.info("* Check : Found OK push button sensitive")
                time.sleep(2)
                ok.click()
                self.log.info("# Step  : Click on button <<OK>>")
            else:
                self.fail("OK push button not sensitive")
                

            time.sleep(10)
            app3 = tree.root.application('Firefox')

            try:
                Toaster =  app3.child(name = 'Toaster - Mozilla Firefox', roleName='frame')
                self.log.info("* Check : Window %s is Open " %Toaster)
            except:
                self.fail("FAIL: can not find %s frame " %Toaster)

            os.system("killall firefox")

        elif eclipse_version == 'mars':

            try:
                projectitem = project.child(name=launchToaster_item, roleName=menuitem_rolename)
                self.log.info("* Check : Found <<Launch Toaster>> menu item")
            except:
                project.deselect()
                time.sleep(10)
                project.select()
                self.log.info("# Step  : Click on menu <<Project>>")

            time.sleep(3)
            projectitem.click()
            self.log.info("# Step  : Click on menu item <<Launch Toaster>>")

            frames = app.findChildren(predicate.GenericPredicate(roleName = frame_rolename))
            if (len(frames) == 0):
                self.fail("can not find frames")

            Launch_Toaster = frames[2]
            text = Launch_Toaster.findChildren(predicate.GenericPredicate(roleName = text_rolename ))


            text[0].click()
            self.log.info("# Step  : Click on box <<Toaster Server URL>")

            link_toaster = 'https://www.yoctoproject.org/toaster/'

            if text[0].text == link_toaster :
                self.log.info("* Check : Toaster Server URL is correct")
            else:
                text[0].click()
                text[0].text = link_toaster

            try:
                ok = Launch_Toaster.child(name=ok_button, roleName = button_rolename)
                self.log.info("* Check : Found OK push button")
            except:
                self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
                cancel_close = Launch_Toaster.child(name = cancel_button, roleName = button_rolename)
                if (cancel_close.sensitive):
                    cancel_close.click()
                self.fail("can not find OK push button")


            if (ok.sensitive):
                self.log.info("* Check : Found OK push button sensitive")
                time.sleep(2)
                ok.click()
                self.log.info("# Step  : Click on button <<OK>>")
            else:
                self.fail("OK push button not sensitive")
                

            try:
                toaster_web = eclipse.child(name='Toaster', roleName='document web')
                self.log.info("* Check : Found <<Toaster>> document web")
            except:
                self.fail("can not find Toaster document web")
                



            time.sleep(10)

            toaster_web.click()
            self.log.info("# Step  : Click on <<Toaster>> document web")


    def new_connection_for_debug(self):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        inifile = IniParser()
        debugConfig = app.child(name=debugconfiguration_frame, roleName=frame_rolename)

        ip = inifile.getValue("test.ini", "SSH", "ip")
        conncectionId = datetime.now().strftime("%d-%m-%Y  %H:%M:%S")
        connection = ip +'SSH_' + conncectionId

        try:
            new = debugConfig.child(name = new_button, roleName = button_rolename)
            self.log.info("* Check : Found New push button")
        except:
            self.fail("can not find New push button")
            

        new.click()
        self.log.info("# Step  : Click on <<New...>push button")

        newConnection = app.child(name=newconnection_frame, roleName = frame_rolename)
        text = newConnection.findChildren(predicate.GenericPredicate(roleName = text_rolename))

        text[0].click()
        self.log.info("# Step  : Click on box <<System type>>")
        text[0].text = 'SSH Only'
        self.log.info("* Check : Insert <<SSH Only>> as System type")


        try:
            sshOnly = newConnection.child(name = ssh_tablecell, roleName = tablecell_rolename)
            self.log.info("* Check : Found SSH Only table cell")
        except:
            self.fail("can not find SSH Only table cell")
            

        sshOnly.click()
        self.log.info("# Step  : Click on box <<System type>>")

        try:
            next = newConnection.child(name = next_button, roleName = button_rolename)
            self.log.info("* Check : Found Next push button")
        except:
            self.fail("can not find Next push button")
            

        next.click()
        self.log.info("# Step  : Click <<Next>>")

        text = newConnection.findChildren(predicate.GenericPredicate(roleName = text_rolename))

        text[1].click()
        self.log.info("# Step  : Click on box <<Host name>>")
        text[1].text =  ip
        self.log.info("* Check : Insert ip of QEMU as hostname")



        text[2].click()
        self.log.info("# Step  : Click on box <<Connection name>>")
        text[2].text = connection
        self.log.info("* Check : Insert Connection name")


        try:
            finish = newConnection.child(name = finish_button, roleName = button_rolename)
            self.log.info("* Check : Found Finish push button")
        except:
            self.fail("can not find Finish push button")
            

        finish.click()
        self.log.info("# Step  : Click on box <<Finish>>")


    def debug_project_to_avoid_5163(self,projectname):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        debugConfig = app.child(name=debugconfiguration_frame, roleName=frame_rolename)

        text = eclipse.findChildren(predicate.GenericPredicate(roleName = text_rolename))
        nrText = len(text)
        if (nrText == 0):
            self.fail("can not find text boxes")
            

        try:
            run = eclipse.child(name = run_menu, roleName = menu_rolename)
            self.log.info("* Check : Found Run menu")
        except:
            self.fail("can not find Run menu")
            

        time.sleep(2)

        run.click()
        self.log.info("# Step  : Click on menu <<Run>>")

        try:
            debugitem = run.child(name=debugconfiguration_item, roleName=menuitem_rolename)
            self.log.info("* Check : Found <<Debug Configurations...>> menu item")
        except:
            self.fail("can not find Debug Configurations menu item")
            

        debugitem.click()
        self.log.info("# Step  : Click on menu item <<Debug Configurations...>>")

        try:
            debugConfig = app.child(name=debugconfiguration_frame, roleName=frame_rolename)
            self.log.info("* Check : Found <<Debug Configurations>> frame")
        except:
            self.fail("can not find Debug Configurations frame")
            

        time.sleep(3)

        typeText(str(projectname))
        self.log.info("# Step  : Insert <<"+ str(projectname)+">> name of project to debug")
        time.sleep(3)
        keyCombo("Down")
        keyCombo("Down")
        keyCombo("Down")
        keyCombo("Enter")


        self.new_connection_for_debug()
        self.log.info("# Step  : Create a new Connection")

        text = debugConfig.findChildren(predicate.GenericPredicate(roleName = text_rolename))

        if (len(text) < 6):
            self.fail("can not find text boxes")
            

        text[5].click()
        self.log.info("# Step  : Click on box <<Remote Absolute File Path for C/C++ App>>")
        text[5].text = '/home/root/'+ str(projectname)

        self.log.info("* Check : Insert Remote Absolute File Path for C/C++ App")

        try:
            debug = debugConfig.child(name=debug_button, roleName = button_rolename)
            self.log.info("* Check : Found Debug push button")
        except:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = debugConfig.child(name = cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                time.sleep(2)
                cancel_close.click()
            self.fail("can not find Debug push button")


        if (debug.sensitive):
            self.log.info("* Check : Found Debug push button sensitive")
            debug.click()
            self.log.info("# Step  : Click on button <<Debug>>")
        else:
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = debugConfig.child(name = cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            self.fail("Debug push button not sensitive")


        found = 1
        try:
            enterPassword =  app.child(name=enterpassword_frame, roleName=frame_rolename)
            self.log.info("* Check : Found <<Enter Password>> frame")
        except:
            found = 0

        if found == 1:
            text = enterPassword.findChildren(predicate.GenericPredicate(roleName = text_rolename))
            if (len(text) == 0):
                self.fail("can not find text boxes")
                

            text[0].click()
            self.log.info("# Step  : Click on box <<User ID>>")
            text[0].text = 'root'
            self.log.info("* Check : Insert <<root>> in <<User ID>> box")

            try:
                ok = enterPassword.child(name=ok_button, roleName = button_rolename)
                self.log.info("* Check : Found OK push button")
            except:
                self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
                cancel_close = enterPassword.child(name = cancel_button, roleName = button_rolename)
                if (cancel_close.sensitive):
                    cancel_close.click()
                self.fail("can not find OK push button")


            if (ok.sensitive):
                self.log.info("* Check : Found OK push button sensitive")
                time.sleep(2)
                ok.click()
                self.log.info("# Step  : Click on button <<OK>>")
            else:
                self.fail("OK push button not sensitive")
                

        time.sleep(60)
        try:
            problem_occurred = app.child(name=problemoccurred_frame, roleName=frame_rolename)
            self.log.info("* Check : Found <<Problem Occurred>> frame")
        except:
            self.fail("can not find Problem Occurred push button")

        try:
            ok = problem_occurred.child(name=ok_button, roleName = button_rolename)
            self.log.info("* Check : Found OK push button")
        except:
            self.fail("can not find OK push button")
            

        if (ok.sensitive):
            self.log.info("* Check : Found OK push button sensitive")
            time.sleep(2)
            ok.click()
            self.log.info("# Step  : Click on button <<OK>>")
        else:
            self.fail("OK push button not sensitive")
            


    def connection_for_linux_tools(self,linuxToolsItem, linuxToolsFrame):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        ip = inifile.getValue("settings-eclipse.ini", "SSH", "ip")


        try:
            YoctoProjectTools = eclipse.child(name = yocto_project_tools_menu, roleName = menu_rolename)
            self.log.info("* Check : Found YoctoProjectTools menu")
        except:
            self.fail("can not find YoctoProjectTools menu")
            

        YoctoProjectTools.click()
        self.log.info("# Step  : Click on menu <<YoctoProjectTools>>")
        time.sleep(2)

        try:
            YPTitem = YoctoProjectTools.child(name=linuxToolsItem, roleName=menuitem_rolename)
            self.log.info("* Check : Found <<"+linuxToolsItem+">> menu item")
        except:
            self.fail("can not find "+linuxToolsItem+" menu item")

        YPTitem.click()
        self.log.info("# Step  : Click on menu item <<"+linuxToolsItem+">>")

        try:
            linuxtoolswindow = app.child(name=linuxToolsFrame, roleName=frame_rolename)
            self.log.info("* Check : Found <<Perf>> frame")
        except:
            self.fail("can not find Debug Configurations frame")
            

        try:
            new = linuxtoolswindow.child(name = new2_button, roleName = button_rolename)
            self.log.info("* Check : Found New push button")
        except:
            self.fail("can not find New push button")
            

        new.click()
        self.log.info("# Step  : Click on <<New>push button")

        newConnection = app.child(name=newconnection_frame, roleName = frame_rolename)
        text = newConnection.findChildren(predicate.GenericPredicate(roleName = text_rolename))

        text[0].click()
        self.log.info("# Step  : Click on box <<System type>>")
        text[0].text = 'SSH Only'
        self.log.info("* Check : Insert <<SSH Only>> as System type")

        try:
            sshOnly = newConnection.child(name = ssh_tablecell, roleName = tablecell_rolename)
            self.log.info("* Check : Found SSH Only table cell")
        except:
            self.fail("can not find SSH Only table cell")
            

        sshOnly.click()
        self.log.info("# Step  : Click on box <<System type>>")

        try:
            next = newConnection.child(name = next_button, roleName = button_rolename)
            self.log.info("* Check : Found Next push button")
        except:
            self.fail("can not find Next push button")
            

        next.click()
        self.log.info("# Step  : Click <<Next>>")

        text = newConnection.findChildren(predicate.GenericPredicate(roleName = text_rolename))
        nrText = len(text)
        if (nrText == 0):
            self.fail("can not find text boxes")
            


        keyCombo("<<Ctrl><a>")
        #text[1].click()
        self.log.info("# Step  : Click on box <<Host name>>")
        #text[1].text =  ip
        typeText(ip)
        self.log.info("* Check : Insert ip of QEMU as hostname")

        conncectionId = datetime.now().strftime("-%d-%m-%Y %H:%M:%S")
        connection = ip + ' ' + linuxToolsItem + conncectionId
        if eclipse_version == 'mars':
            text[2].click()
            self.log.info("# Step  : Click on box <<Connection name>>")
            text[2].text = connection
            self.log.info("* Check : Insert Connection name")
        elif eclipse_version == 'luna':
            text[1].click()
            self.log.info("# Step  : Click on box <<Connection name>>")
            text[1].text = connection
            self.log.info("* Check : Insert Connection name")

        try:
            finish = newConnection.child(name = finish_button, roleName = button_rolename)
            self.log.info("* Check : Found Finish push button")
        except:
            self.fail("can not find Finish push button")

        finish.click()
        self.log.info("# Step  : Click on box <<Finish>>")



        comboBox = linuxtoolswindow.findChildren(predicate.GenericPredicate(roleName=combobox_rolename))
        if (len(comboBox) > 0):
            self.log.info("* Check : Found menu drop-down list Connection")
            comboBox[0].click()
            self.log.info("# Step  : Click on menu drop-down list <<Connection>>")
        else:
            self.fail("can not find combo boxes")
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = linuxtoolswindow.child(name=cancel_button, roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()


        try:
            connectionTools = linuxtoolswindow.child(name = connection, roleName=menuitem_rolename)
            self.log.info("* Check : Found " + str(connection) + " menu item")
        except:
            self.fail("can not find " + str(connection) + " menu item")


        connectionTools.click()
        self.log.info("# Step  : Select <<" + str(connection) + ">>")

        try:
            ok_tools = linuxtoolswindow.child(name = ok_button, roleName = button_rolename)
            self.log.info("* Check : Found OK push button")
        except:
            self.fail("can not find OK push button")


        ok_tools.click()
        self.log.info("# Step  : Click on <<OK>>push button")

        found = 1
        try:
            enterPassword =  app.child(name=enterpassword_frame, roleName=frame_rolename)
            self.log.info("* Check : Found <<Enter Password>> frame")
        except:
            found = 0

        if found == 1:
            text = enterPassword.findChildren(predicate.GenericPredicate(roleName = text_rolename))
            if (len(text) == 0):
                self.fail("can not find text boxes")


            text[0].click()
            self.log.info("# Step  : Click on box <<User ID>>")
            text[0].text = 'root'
            self.log.info("* Check : Insert <<root>> in <<User ID>> box")

            try:
                ok_enter = enterPassword.child(name=ok_button, roleName = button_rolename)
                self.log.info("* Check : Found OK push button")
            except:
                self.fail("can not find OK push button")
                self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
                cancel_close = enterPassword.child(name = cancel_button, roleName = button_rolename)
                if (cancel_close.sensitive):
                    cancel_close.click()


            if (ok_enter.sensitive):
                self.log.info("* Check : Found OK push button sensitive")
                ok_enter.click()
                self.log.info("# Step  : Click on button <<OK>>")
            else:
                self.fail("OK push button not sensitive")




###################################################################
#                                                                 #
# PART III: test cases                                            #
# please refer to                                                 #
# https://bugzilla.yoctoproject.org/tr_show_case.cgi?case_id=xxx  
#                                                                 #
###################################################################

# Note: to comply with the unittest framework, we call these test_xxx functions
# from run_eclipsecases.py to avoid calling setUp() and tearDown() multiple times


class eclipse_cases(eclipse_cases_base):

    
        
    ##############
    #  CASE 24  #
    ##############
    @testcase(24)
    def test_24(self):

        param1 = inifile.getValue("settings-eclipse.ini", "Run", "param1")
        param2 = inifile.getValue("settings-eclipse.ini", "Run", "param2")
        eclipse_version= inifile.getValue("settings-eclipse.ini", "Run", "eclipse_version")
        commit = inifile.getValue("settings-eclipse.ini", "Run", "commit")
        dateofrun = inifile.getValue("settings-eclipse.ini", "Run", "date")

        self.log.info('#############################################################################')
        self.log.info('###         TC 24 - Install Eclipse Using the Headless Build              ###')
        self.log.info('#############################################################################')

        self.create_tree(eclipse_version, param1, param2, dateofrun)
        self.log.info("# Step  : Create tree for run")

        self.download_basic_things(param1, param2, dateofrun)
        self.log.info("# Step  : Download basic things")

        self.download_plugin_and_eclipse_version(eclipse_version, param1, param2, dateofrun)
        self.log.info("# Step  : Download plugin and eclipse version")

        self.install_basic_things(param1, param2, commit, dateofrun)
        self.log.info("# Step  : Install basic things")

        self.install_eclipse_version(param1, param2, eclipse_version, dateofrun)
        self.log.info("# Step  : Install eclipse %s " %(eclipse_version))

        self.start_eclipse(param1, param2, eclipse_version, dateofrun)
        self.log.info("# Step  : Start Eclipse %s" %eclipse_version)

        self.install_eclipse_plugin(param1, param2, eclipse_version, dateofrun)
        self.log.info("# Step  : Install Eclipse %s" %eclipse_version)
        time.sleep(10)
        self.restart_and_close_welcome()
        self.log.info("# Step  : Restart Eclipse %s" %eclipse_version)



    @testcase(739)
    def test_739(self):
        
        param1 = inifile.getValue("settings-eclipse.ini", "Run", "param1")
        param2 = inifile.getValue("settings-eclipse.ini", "Run", "param2")
        dateofrun = inifile.getValue("settings-eclipse.ini", "Run", "date")
        eclipse_version= inifile.getValue("settings-eclipse.ini", "Run", "eclipse_version")

        toolchainType = inifile.getValue("settings-eclipse.ini", "TC739_eclipse-plugin_support_profiles", "Cross_Compiler_Options")
        toolchainAdr = '/home/' + getpass.getuser() + '/eclipse-run/' + "run-" + param1 + "-" + param2 + "-" + dateofrun + "/installed/adt"
        sysrootAdr = '/home/' + getpass.getuser() + '/test-yocto/qemux86'
        targetArch = inifile.getValue("settings-eclipse.ini", "TC739_eclipse-plugin_support_profiles", "Target_Arhitecture")
        targetType = inifile.getValue("settings-eclipse.ini", "TC739_eclipse-plugin_support_profiles", "Target_Options")
        kernelAdr = '/home/' + getpass.getuser() + '/eclipse-run/' + "run-" + param1 + "-" + param2 + "-" + dateofrun + "/download/adt-installer/download_image/bzImage-qemux86.bin"

        newprofileName = inifile.getValue("settings-eclipse.ini", "TC739_eclipse-plugin_support_profiles", "Cross_development_profiles")
        renameprofile = inifile.getValue("settings-eclipse.ini", "TC739_eclipse-plugin_support_profiles", "Cross_development_profiles_rename")
        projectname = inifile.getValue("settings-eclipse.ini", "TC739_eclipse-plugin_support_profiles", "Project_name")
        typeproject = inifile.getValue("settings-eclipse.ini", "TC739_eclipse-plugin_support_profiles", "Wizards")
        searchtype = inifile.getValue("settings-eclipse.ini", "TC739_eclipse-plugin_support_profiles", "Search")
        author = inifile.getValue("settings-eclipse.ini", "TC739_eclipse-plugin_support_profiles", "Author")
        copyrightproject = inifile.getValue("settings-eclipse.ini", "TC739_eclipse-plugin_support_profiles", "Copyright")


        self.log.info("#############################################################################")
        self.log.info("###              TC 739 - eclipse-plugin support profiles                 ###")
        self.log.info("#############################################################################")

        self.work_around_preferences_frame()
        self.log.info("# Step  : Insert a text in one text box to modify size of frame")

        self.configure_standard_profile(toolchainType, toolchainAdr, sysrootAdr, targetArch, targetType, kernelAdr)
        self.log.info("# Step  : Configure Standard Profile")

        self.add_new_profile(newprofileName)
        self.log.info("# Step  : Add Profile " + str(newprofileName) + "")

        self.createProject(projectname, typeproject, searchtype, author, copyrightproject)
        self.log.info("# Step  : Create Project")

        self.open_perspective()
        self.log.info("# Step  : Change Perspective")

        self.reconfigure_project(projectname)
        self.log.info("# Step  : Reconfigure Project")

        if eclipse_version == 'mars':
            self.reconfigure_project(projectname)
            self.log.info("# Step  : Reconfigure Project")

        self.verify_profile(projectname, toolchainType, toolchainAdr, sysrootAdr, targetArch, targetType, kernelAdr, newprofileName)
        self.log.info("# Step  : Verify all the information about profile saved")

        self.rename_profile(newprofileName, renameprofile)
        self.log.info("# Step  : Rename profile")

        self.remove_yocto_profile(renameprofile)
        self.log.info("# Step  : Remove profile")

        self.close_project()
        self.log.info("# Step  : Close Project")

        self.delete_project(projectname, typeproject)
        self.log.info("# Step  : Delete Project")

        self.close_perspective()
        self.log.info("# Step  : Close C/C++ perspective")



    @testcase(25)
    def test_25(self):
        
        projectname = inifile.getValue("settings-eclipse.ini", "TC25_support_SSH_connection_to_Target", "Project_name")
        typeproject = inifile.getValue("settings-eclipse.ini", "TC25_support_SSH_connection_to_Target", "Wizards")
        searchtype = inifile.getValue("settings-eclipse.ini", "TC25_support_SSH_connection_to_Target", "Search")
        author = inifile.getValue("settings-eclipse.ini", "TC25_support_SSH_connection_to_Target", "Author")
        copyrightproject = inifile.getValue("settings-eclipse.ini", "TC25_support_SSH_connection_to_Target", "Copyright")
        
        self.log.info("#############################################################################")
        self.log.info("###              TC 25 - Support SSH connection to Target                 ###")
        self.log.info("#############################################################################")
        
        self.set_network_preferences_to_direct()
        self.log.info("# Step  : Set connection to Direct")
        
        self.createProject(projectname, typeproject, searchtype, author, copyrightproject)
        self.log.info("# Step  : Create Project")
        
        self.open_perspective()
        self.log.info("# Step  : Change Perspective")
        
        self.reconfigure_project(projectname)
        self.log.info("# Step  : Reconfigure Project")
        
        self.build_project()
        self.log.info("# Step  : Build Project")

        self.launch_qemu_from_eclipse()
        self.log.info("# Step  : Verify if QEMU appears in External Tools in Eclipse")
        
        self.delete_project(projectname, typeproject)
        self.log.info("# Step  : Delete Project")
        
        self.close_perspective()
        self.log.info("# Step  : Close C/C++ perspective")
    



    @testcase(26)
    def test_26(self):
    
        param1 = inifile.getValue("settings-eclipse.ini", "Run", "param1")
        param2 = inifile.getValue("settings-eclipse.ini", "Run", "param2")
        dateofrun = inifile.getValue("settings-eclipse.ini", "Run", "date")
        eclipse_version= inifile.getValue("settings-eclipse.ini", "Run", "eclipse_version")
        
        toolchainAdr = '/home/' + getpass.getuser() + '/eclipse-run/' + "run-" + param1 + "-" + param2 + "-" + dateofrun + "/installed/adt"
        kernelAdr = '/home/' + getpass.getuser() + '/eclipse-run/' + "run-" + param1 + "-" + param2 + "-" + dateofrun + "/download/adt-installer/download_image/bzImage-qemux86.bin"
        sysrootAdr = '/home/' + getpass.getuser() + '/test-yocto/qemux86'

        toolchainType = inifile.getValue("settings-eclipse.ini", "TC26_Persistent_Yocto_Project_ADT_Settings", "Cross_Compiler_Options")
        targetArch = inifile.getValue("settings-eclipse.ini", "TC26_Persistent_Yocto_Project_ADT_Settings", "Target_Arhitecture")
        targetType = inifile.getValue("settings-eclipse.ini", "TC26_Persistent_Yocto_Project_ADT_Settings", "Target_Options")
        projectname = inifile.getValue("settings-eclipse.ini", "TC26_Persistent_Yocto_Project_ADT_Settings", "Project_name")
        typeproject = inifile.getValue("settings-eclipse.ini", "TC26_Persistent_Yocto_Project_ADT_Settings", "Wizards")
        searchtype = inifile.getValue("settings-eclipse.ini", "TC26_Persistent_Yocto_Project_ADT_Settings", "Search")
        author = inifile.getValue("settings-eclipse.ini", "TC26_Persistent_Yocto_Project_ADT_Settings", "Author")
        copyrightproject = inifile.getValue("settings-eclipse.ini", "TC26_Persistent_Yocto_Project_ADT_Settings", "Copyright")
        
        self.log.info("#############################################################################")
        self.log.info("###            TC 26 - Persistent Yocto Project ADT settings              ###")
        self.log.info("#############################################################################")
        
        self.configure_standard_profile(toolchainType, toolchainAdr, sysrootAdr, targetArch, targetType, kernelAdr)
        self.log.info("# Step  : Configure Standard Profile")
        
        self.createProject(projectname, typeproject, searchtype, author, copyrightproject)
        self.log.info("# Step  : Create Project")
        
        self.open_perspective()
        self.log.info("# Step  : Change Perspective")
        
        self.reconfigure_project(projectname)
        self.log.info("# Step  : Reconfigure Project")
        
        self.build_project()
        self.log.info("# Step  : Build Project")
        
        self.run_project(projectname, searchtype,eclipse_version)
        self.log.info("# Step  : Run Project")
    
        self.close_project()
        self.log.info("# Step  : Close Project")
        
        self.delete_project( projectname, typeproject)
        self.log.info("# Step  : Delete Project")
        
        self.close_perspective()
        self.log.info("# Step  : Close C/C++ perspective")
            
    @testcase(27)
    def test_27(self):
        
        param1 = inifile.getValue("settings-eclipse.ini", "Run", "param1")
        param2 = inifile.getValue("settings-eclipse.ini", "Run", "param2")
        dateofrun = inifile.getValue("settings-eclipse.ini", "Run", "date")
        
        
        toolchainAdr = '/home/' + getpass.getuser() + '/eclipse-run/' + "run-" + param1 + "-" + param2 + "-" + dateofrun + "/installed/adt"
        kernelAdr = '/home/' + getpass.getuser() + '/eclipse-run/' + "run-" + param1 + "-" + param2 + "-" + dateofrun + "/download/adt-installer/download_image/bzImage-qemux86.bin"
        sysrootAdr = '/home/' + getpass.getuser() + '/test-yocto/qemux86'

        toolchainType = inifile.getValue("settings-eclipse.ini", "TC27_Change_Yocto_Project_ADT_Settings_profile", "Cross_Compiler_Options")
        targetArch = inifile.getValue("settings-eclipse.ini", "TC27_Change_Yocto_Project_ADT_Settings_profile", "Target_Arhitecture")
        targetType = inifile.getValue("settings-eclipse.ini", "TC27_Change_Yocto_Project_ADT_Settings_profile", "Target_Options")
        
        
        projectname = inifile.getValue("settings-eclipse.ini", "TC27_Change_Yocto_Project_ADT_Settings_profile", "Project_name")
        typeproject = inifile.getValue("settings-eclipse.ini", "TC27_Change_Yocto_Project_ADT_Settings_profile", "Wizards")
        searchtype = inifile.getValue("settings-eclipse.ini", "TC27_Change_Yocto_Project_ADT_Settings_profile", "Search")
        author = inifile.getValue("settings-eclipse.ini", "TC27_Change_Yocto_Project_ADT_Settings_profile", "Author")
        copyrightproject = inifile.getValue("settings-eclipse.ini", "TC27_Change_Yocto_Project_ADT_Settings_profile", "Copyright")
        
        newprofileName = inifile.getValue("settings-eclipse.ini", "TC27_Change_Yocto_Project_ADT_Settings_profile", "Cross_development_profiles_2")
        renameprofile = inifile.getValue("settings-eclipse.ini", "TC27_Change_Yocto_Project_ADT_Settings_profile", "Cross_development_profiles_2")
        
        
        self.log.info("#############################################################################")
        self.log.info("###        TC 27 - Change Yocto Project ADT Settings profile              ###")
        self.log.info("#############################################################################")
        
        self.configure_standard_profile(toolchainType, toolchainAdr, sysrootAdr, targetArch, targetType, kernelAdr)
        self.log.info("# Step  : Configure Standard Profile")
        
        self.createProject(projectname, typeproject, searchtype, author, copyrightproject)
        self.log.info("# Step  : Create Project")
        
        self.open_perspective()
        self.log.info("# Step  : Change Perspective")
        
        self.reconfigure_project(projectname)
        self.log.info("# Step  : Reconfigure Project")
        
        self.add_new_profile(newprofileName)
        self.log.info("# Step  : Add Profile " + str(newprofileName) )
        
        self.change_profile_on_selected_project(projectname, newprofileName)
        self.log.info("# Step  : Change Profile")
        
        self.reconfigure_project(projectname)
        self.log.info("# Step  : Reconfigure Project")
        
        self.remove_yocto_profile(renameprofile)
        self.log.info("# Step  : Remove profile")
        
        self.close_project()
        self.log.info("# Step  : Close Project")
        
        self.delete_project(projectname, typeproject)
        self.log.info("# Step  : Delete Project")
        
        self.close_perspective()
        self.log.info("# Step  : Close C/C++ perspective")
    

    @testcase(385)
    def test_385(self):

        param1 = inifile.getValue("settings-eclipse.ini", "Run", "param1")
        param2 = inifile.getValue("settings-eclipse.ini", "Run", "param2")
        dateofrun = inifile.getValue("settings-eclipse.ini", "Run", "date")

        toolchainAdr = '/home/' + getpass.getuser() + '/eclipse-run/' + "run-" + param1 + "-" + param2 + "-" + dateofrun + "/installed/adt"
        kernelAdr = '/home/' + getpass.getuser() + '/eclipse-run/' + "run-" + param1 + "-" + param2 + "-" + dateofrun + "/download/adt-installer/download_image/bzImage-qemux86.bin"
        sysrootAdr = '/home/' + getpass.getuser() + '/test-yocto/qemux86'

        toolchainType = inifile.getValue("settings-eclipse.ini", "TC385_ADT-installer_Configure_Eclipse_plugin_with_the_toolchain_and_sysroot_installed_using_ADT", "Cross_Compiler_Options")
        targetArch = inifile.getValue("settings-eclipse.ini", "TC385_ADT-installer_Configure_Eclipse_plugin_with_the_toolchain_and_sysroot_installed_using_ADT", "Target_Arhitecture")
        targetType = inifile.getValue("settings-eclipse.ini", "TC385_ADT-installer_Configure_Eclipse_plugin_with_the_toolchain_and_sysroot_installed_using_ADT", "Target_Options")


        self.log.info("##########################################################################################################")
        self.log.info("###TC 385 - ADT-installer - Configure Eclipse plugin with the toolchain and sysroot installed using ADT###")
        self.log.info("##########################################################################################################")

        self.configure_standard_profile(toolchainType, toolchainAdr, sysrootAdr, targetArch, targetType, kernelAdr)
        self.log.info("# Step  : Configure standard profile")



    @testcase(38)
    def test_38(self):
        
      
        projectname = inifile.getValue("settings-eclipse.ini", "TC38_ADT-installer_C_Build_Hello_World_ANSI_C_Autotools_Project", "Project_name")
        typeproject = inifile.getValue("settings-eclipse.ini", "TC38_ADT-installer_C_Build_Hello_World_ANSI_C_Autotools_Project", "Wizards")
        searchtype = inifile.getValue("settings-eclipse.ini", "TC38_ADT-installer_C_Build_Hello_World_ANSI_C_Autotools_Project", "Search")
        author = inifile.getValue("settings-eclipse.ini", "TC38_ADT-installer_C_Build_Hello_World_ANSI_C_Autotools_Project", "Author")
        copyrightproject = inifile.getValue("settings-eclipse.ini", "TC38_ADT-installer_C_Build_Hello_World_ANSI_C_Autotools_Project", "Copyright")
        eclipse_version= inifile.getValue("settings-eclipse.ini", "Run", "eclipse_version")
       
        self.log.info("#############################################################################")
        self.log.info("###TC 38 - ADT-installer - C - Build Hello World ANSI C Autotools Project ###")
        self.log.info("#############################################################################")
        
        self.createProject(projectname, typeproject, searchtype, author, copyrightproject)
        self.log.info("# Step  : Create Project")
        
        self.open_perspective()
        self.log.info("# Step  : Change Perspective")
        
        self.reconfigure_project(projectname)
        self.log.info("# Step  : Reconfigure Project")
        
        self.build_project()
        self.log.info("# Step  : Build Project")
        
        self.run_project(projectname, searchtype,eclipse_version)
        self.log.info("# Step  : Run Project")
        
        self.debug_project(projectname, searchtype)
        self.log.info("# Step  : Debug Project")
        
        self.close_project()
        self.log.info("# Step  : Close Project")
        
        self.delete_project(projectname, typeproject)
        self.log.info("# Step  : Delete Project")
        
        self.close_perspective()
        self.log.info("# Step  : Close C/C++ perspective")
        

    @testcase(39)
    def test_39(self):

        projectname = inifile.getValue("settings-eclipse.ini", "TC39_ADT-installer_C++_Build_Hello_World_C++_Autotools project", "Project_name")
        typeproject = inifile.getValue("settings-eclipse.ini", "TC39_ADT-installer_C++_Build_Hello_World_C++_Autotools project", "Wizards")
        searchtype = inifile.getValue("settings-eclipse.ini", "TC39_ADT-installer_C++_Build_Hello_World_C++_Autotools project", "Search")
        author = inifile.getValue("settings-eclipse.ini", "TC39_ADT-installer_C++_Build_Hello_World_C++_Autotools project", "Author")
        copyrightproject = inifile.getValue("settings-eclipse.ini", "TC39_ADT-installer_C++_Build_Hello_World_C++_Autotools project", "Copyright")
        eclipse_version= inifile.getValue("settings-eclipse.ini", "Run", "eclipse_version")
  
        self.log.info("#############################################################################")
        self.log.info("### TC 39 - ADT-installer - C++ - Build Hello World C++ Autotools Project ###")
        self.log.info("#############################################################################")
        
        self.createProject(projectname, typeproject, searchtype, author, copyrightproject)
        self.log.info("# Step  : Create Project")
        
        self.open_perspective()
        self.log.info("# Step  : Change Perspective")
        
        self.reconfigure_project(projectname)
        self.log.info("# Step  : Reconfigure Project")
        
        self.build_project()
        self.log.info("# Step  : Build Project")
        
        self.run_project(projectname, searchtype, eclipse_version)
        self.log.info("# Step  : Run Project")
        
        self.debug_project(projectname, searchtype)
        self.log.info("# Step  : Debug Project")
        
        self.close_project()
        self.log.info("# Step  : Close Project")
        
        self.delete_project(projectname, typeproject)
        self.log.info("# Step  : Delete Project")
        
        self.close_perspective()
        self.log.info("# Step  : Close C/C++ perspective")
        

    @testcase(377)
    def test_377(self):
        
        projectname = inifile.getValue("settings-eclipse.ini", "TC377_ADT-installer_C_Build_Hello_World_GTK_C_Autotools_Project", "Project_name")
        typeproject = inifile.getValue("settings-eclipse.ini", "TC377_ADT-installer_C_Build_Hello_World_GTK_C_Autotools_Project", "Wizards")
        searchtype = inifile.getValue("settings-eclipse.ini", "TC377_ADT-installer_C_Build_Hello_World_GTK_C_Autotools_Project", "Search")
        author = inifile.getValue("settings-eclipse.ini", "TC377_ADT-installer_C_Build_Hello_World_GTK_C_Autotools_Project", "Author")
        copyrightproject = inifile.getValue("settings-eclipse.ini", "TC377_ADT-installer_C_Build_Hello_World_GTK_C_Autotools_Project", "Copyright")
        eclipse_version= inifile.getValue("settings-eclipse.ini", "Run", "eclipse_version")
        
       
        self.log.info("#############################################################################")
        self.log.info("###TC 377 - ADT-installer - C - Build Hello World GTK C  Autotools Project###")
        self.log.info("#############################################################################")
        
        self.createProject(projectname, typeproject, searchtype, author, copyrightproject)
        self.log.info("# Step  : Create Project")
        
        self.open_perspective()
        self.log.info("# Step  : Change Perspective")
        
        self.reconfigure_project(projectname)
        self.log.info("# Step  : Reconfigure Project")
        
        self.build_project()
        self.log.info("# Step  : Build Project")
        
        self.run_project(projectname, searchtype,eclipse_version)
        self.log.info("# Step  : Run Project")
        
        self.debug_project(projectname, searchtype)
        self.log.info("# Step  : Debug Project")
        
        self.close_project()
        self.log.info("# Step  : Close Project")
        
        self.delete_project(projectname, typeproject)
        self.log.info("# Step  : Delete Project")
        
        self.close_perspective()
        self.log.info("# Step  : Close C/C++ perspective")

    @testcase(386)
    def test_386(self):

        param1 = inifile.getValue("settings-eclipse.ini", "Run", "param1")
        param2 = inifile.getValue("settings-eclipse.ini", "Run", "param2")
        dateofrun = inifile.getValue("settings-eclipse.ini", "Run", "date")

        toolchainAdr = '/home/' + getpass.getuser() + '/eclipse-run/' + "run-" + param1 + "-" + param2 + "-" + dateofrun + "/installed/toolchain"
        kernelAdr = '/home/' + getpass.getuser() + '/eclipse-run/' + "run-" + param1 + "-" + param2 + "-" + dateofrun + "/download/adt-installer/download_image/bzImage-qemux86.bin"
        sysrootAdr = '/home/' + getpass.getuser() + '/test-yocto/qemux86'

        toolchainType = inifile.getValue("settings-eclipse.ini", "TC386_Relocatable_SDK_Configure_Eclipse_plugin_with_the_toolchain_and_sysroot_installed_using_Relocatable_SDK", "Cross_Compiler_Options")
        targetArch = inifile.getValue("settings-eclipse.ini", "TC386_Relocatable_SDK_Configure_Eclipse_plugin_with_the_toolchain_and_sysroot_installed_using_Relocatable_SDK", "Target_Arhitecture")
        targetType = inifile.getValue("settings-eclipse.ini", "TC386_Relocatable_SDK_Configure_Eclipse_plugin_with_the_toolchain_and_sysroot_installed_using_Relocatable_SDK", "Target_Options")

        self.log.info("########################################################################################################################")
        self.log.info("###TC 386 - Relocatable SDK - Configure Eclipse plugin with the toolchain and sysroot installed using Relocatable SDK###")
        self.log.info("########################################################################################################################")

        self.work_around_preferences_frame()
        self.log.info("# Step  : Insert a text in one text box to modify size of frame")

        self.configure_standard_profile(toolchainType, toolchainAdr, sysrootAdr, targetArch, targetType, kernelAdr)
        self.log.info("# Step  : Configure standard profile")


    @testcase(373)
    def test_373(self):

        projectname = inifile.getValue("settings-eclipse.ini", "TC373_Relocatable_SDK_C_Build_Hello_World_ANSI_C_Autotools_Project", "Project_name")
        typeproject = inifile.getValue("settings-eclipse.ini", "TC373_Relocatable_SDK_C_Build_Hello_World_ANSI_C_Autotools_Project", "Wizards")
        searchtype = inifile.getValue("settings-eclipse.ini", "TC373_Relocatable_SDK_C_Build_Hello_World_ANSI_C_Autotools_Project", "Search")
        author = inifile.getValue("settings-eclipse.ini", "TC373_Relocatable_SDK_C_Build_Hello_World_ANSI_C_Autotools_Project", "Author")
        copyrightproject = inifile.getValue("settings-eclipse.ini", "TC373_Relocatable_SDK_C_Build_Hello_World_ANSI_C_Autotools_Project", "Copyright")
        eclipse_version= inifile.getValue("settings-eclipse.ini", "Run", "eclipse_version")

        self.log.info("################################################################################")
        self.log.info("###TC 373 - Relocatable SDK - C - Build Hello World ANSI C Autotools Project ###")
        self.log.info("################################################################################")

        self.createProject(projectname, typeproject, searchtype, author, copyrightproject)
        self.log.info("# Step  : Create Project")

        self.open_perspective()
        self.log.info("# Step  : Change Perspective")

        self.reconfigure_project(projectname)
        self.log.info("# Step  : Reconfigure Project")

        self.build_project()
        self.log.info("# Step  : Build Project")

        self.run_project(projectname, searchtype,eclipse_version)
        self.log.info("# Step  : Run Project")

        self.debug_project(projectname, searchtype)
        self.log.info("# Step  : Debug Project")

        self.close_project()
        self.log.info("# Step  : Close Project")

        self.delete_project(projectname, typeproject)
        self.log.info("# Step  : Delete Project")

        self.close_perspective()
        self.log.info("# Step  : Close C/C++ perspective")



    @testcase(379)
    def test_379(self):

        projectname = inifile.getValue("settings-eclipse.ini", "TC379_Relocatable_SDK_C++_Build_Hello_World_C++_Autotools_Project", "Project_name")
        typeproject = inifile.getValue("settings-eclipse.ini", "TC379_Relocatable_SDK_C++_Build_Hello_World_C++_Autotools_Project", "Wizards")
        searchtype = inifile.getValue("settings-eclipse.ini", "TC379_Relocatable_SDK_C++_Build_Hello_World_C++_Autotools_Project", "Search")
        author = inifile.getValue("settings-eclipse.ini", "TC379_Relocatable_SDK_C++_Build_Hello_World_C++_Autotools_Project", "Author")
        copyrightproject = inifile.getValue("settings-eclipse.ini", "TC379_Relocatable_SDK_C++_Build_Hello_World_C++_Autotools_Project", "Copyright")
        eclipse_version= inifile.getValue("settings-eclipse.ini", "Run", "eclipse_version")

 
        self.log.info("##############################################################################")
        self.log.info("###TC 379 - Relocatable SDK - C++ - Build Hello World C++ Autotools Project###")
        self.log.info("##############################################################################")


        self.createProject(projectname, typeproject, searchtype, author, copyrightproject)
        self.log.info("# Step  : Create Project")

        self.open_perspective()
        self.log.info("# Step  : Change Perspective")


        self.reconfigure_project(projectname)
        self.log.info("# Step  : Reconfigure Project")

        self.build_project()
        self.log.info("# Step  : Build Project")

        self.run_project(projectname, searchtype,eclipse_version)
        self.log.info("# Step  : Run Project")

        self.debug_project(projectname, searchtype)
        self.log.info("# Step  : Debug Project")

        self.close_project()
        self.log.info("# Step  : Close Project")

        self.delete_project(projectname, typeproject)
        self.log.info("# Step  : Delete Project")

        self.close_perspective()
        self.log.info("# Step  : Close C/C++ perspective")



    @testcase(378)
    def test_378(self):

        projectname = inifile.getValue("settings-eclipse.ini", "TC378_Relocatable_SDK_C_Build_Hello_World_GTK_C_Autotools_Project", "Project_name")
        typeproject = inifile.getValue("settings-eclipse.ini", "TC378_Relocatable_SDK_C_Build_Hello_World_GTK_C_Autotools_Project", "Wizards")
        searchtype = inifile.getValue("settings-eclipse.ini", "TC378_Relocatable_SDK_C_Build_Hello_World_GTK_C_Autotools_Project", "Search")
        author = inifile.getValue("settings-eclipse.ini", "TC378_Relocatable_SDK_C_Build_Hello_World_GTK_C_Autotools_Project", "Author")
        copyrightproject = inifile.getValue("settings-eclipse.ini", "TC378_Relocatable_SDK_C_Build_Hello_World_GTK_C_Autotools_Project", "Copyright")
        eclipse_version= inifile.getValue("settings-eclipse.ini", "Run", "eclipse_version")

        self.log.info("################################################################################")
        self.log.info("###TC 378 - Relocatable SDK - C - Build Hello World  GTK C  Autotools Project###")
        self.log.info("################################################################################")

        self.createProject(projectname, typeproject, searchtype, author, copyrightproject)
        self.log.info("# Step  : Create Project")

        self.open_perspective()
        self.log.info("# Step  : Change Perspective")

        self.reconfigure_project(projectname)
        self.log.info("# Step  : Reconfigure Project")

        self.build_project()
        self.log.info("# Step  : Build Project")

        self.run_project(projectname, searchtype,eclipse_version)
        self.log.info("# Step  : Run Project")

        self.debug_project(projectname, searchtype)
        self.log.info("# Step  : Debug Project")

        self.close_project()
        self.log.info("# Step  : Close Project")

        self.delete_project(projectname, typeproject)
        self.log.info("# Step  : Delete Project")

        self.close_perspective()
        self.log.info("# Step  : Close C/C++ perspective")



    @testcase(387)
    def test_387(self):

        param1 = inifile.getValue("settings-eclipse.ini", "Run", "param1")
        param2 = inifile.getValue("settings-eclipse.ini", "Run", "param2")
        dateofrun = inifile.getValue("settings-eclipse.ini", "Run", "date")
        
        poky_path =  '/home/' + getpass.getuser() + '/eclipse-run/' + "run-" + param1 + "-" + param2 + "-" + dateofrun + "/download/poky/"
        toolchainAdr = poky_path + "build/"
        kernelAdr = '/home/' + getpass.getuser() + '/eclipse-run/' + "run-" + param1 + "-" + param2 + "-" + dateofrun + "/download/adt-installer/download_image/bzImage-qemux86.bin"

        sysrootAdr = '/home/' + getpass.getuser() + '/test-yocto/qemux86'
        toolchainType = inifile.getValue("settings-eclipse.ini", "TC387_User_Built_SDK-Configure_Eclipse_plugin_with_the_toolchain_and_sysroot_installed_using_User_Built_SDK", "Cross_Compiler_Options")
        targetArch = inifile.getValue("settings-eclipse.ini", "TC387_User_Built_SDK-Configure_Eclipse_plugin_with_the_toolchain_and_sysroot_installed_using_User_Built_SDK", "Target_Arhitecture")
        targetType = inifile.getValue("settings-eclipse.ini", "TC387_User_Built_SDK-Configure_Eclipse_plugin_with_the_toolchain_and_sysroot_installed_using_User_Built_SDK", "Target_Options")

        #kernelAdr = poky_path +"build/tmp/deploy/images/qemux86/bzImage-qemux86.bin"
        #sysrootAdr = poky_path + "build/tmp/sysroots/qemux86"
        #sysrootAdr = inifile.getValue("settings-eclipse.ini", "TC387_User_Built_SDK-Configure_Eclipse_plugin_with_the_toolchain_and_sysroot_installed_using_User_Built_SDK", "Sysroot_Location")

        self.log.info("########################################################################################################################")
        self.log.info("### TC 387 - User Built SDK - Configure Eclipse plugin with the toolchain and sysroot installed using User Built SDK ###")
        self.log.info("########################################################################################################################")
        
        self.work_around_preferences_frame()
        self.log.info("# Step  : Insert a text in one text box to modify size of frame")
        
        self.configure_standard_profile(toolchainType, toolchainAdr, sysrootAdr, targetArch, targetType, kernelAdr)
        
        

    @testcase(374)
    def test_374(self):
        

        projectname = inifile.getValue("settings-eclipse.ini", "TC374_User_Built_SDK_C_Build_Hello_World_ANSI_C_Autotools_Project", "Project_name")
        typeproject = inifile.getValue("settings-eclipse.ini", "TC374_User_Built_SDK_C_Build_Hello_World_ANSI_C_Autotools_Project", "Wizards")
        searchtype = inifile.getValue("settings-eclipse.ini", "TC374_User_Built_SDK_C_Build_Hello_World_ANSI_C_Autotools_Project", "Search")
        author = inifile.getValue("settings-eclipse.ini", "TC374_User_Built_SDK_C_Build_Hello_World_ANSI_C_Autotools_Project", "Author")
        copyrightproject = inifile.getValue("settings-eclipse.ini", "TC374_User_Built_SDK_C_Build_Hello_World_ANSI_C_Autotools_Project", "Copyright")
        eclipse_version= inifile.getValue("settings-eclipse.ini", "Run", "eclipse_version")

        self.log.info("################################################################################")
        self.log.info("### TC 374 - User Built SDK - C - Build Hello World ANSI C Autotools Project ###")
        self.log.info("################################################################################")
        
        
        self.createProject(projectname, typeproject, searchtype, author, copyrightproject)
        self.log.info("# Step  : Create Project")

        self.open_perspective()
        self.log.info("# Step  : Change Perspective")

        self.reconfigure_project(projectname)
        self.log.info("# Step  : Reconfigure Project")
        
        self.build_project()
        self.log.info("# Step  : Build Project")
        
        self.run_project(projectname, searchtype,eclipse_version)
        self.log.info("# Step  : Run Project")

        self.debug_project(projectname, searchtype)
        self.log.info("# Step  : Debug Project")
        
        self.close_project()
        self.log.info("# Step  : Close Project")
        
        self.delete_project(projectname, typeproject)
        self.log.info("# Step  : Delete Project")
        
        self.close_perspective()
        self.log.info("# Step  : Close C/C++ perspective")
        
    


    @testcase(380)
    def test_380(self):

        projectname = inifile.getValue("settings-eclipse.ini", "TC380_User_Built_SDK_C++_Build_Hello_World_C++_Autotools_Project", "Project_name")
        typeproject = inifile.getValue("settings-eclipse.ini", "TC380_User_Built_SDK_C++_Build_Hello_World_C++_Autotools_Project", "Wizards")
        searchtype = inifile.getValue("settings-eclipse.ini", "TC380_User_Built_SDK_C++_Build_Hello_World_C++_Autotools_Project", "Search")
        author = inifile.getValue("settings-eclipse.ini", "TC380_User_Built_SDK_C++_Build_Hello_World_C++_Autotools_Project", "Author")
        copyrightproject = inifile.getValue("settings-eclipse.ini", "TC380_User_Built_SDK_C++_Build_Hello_World_C++_Autotools_Project", "Copyright")
        eclipse_version= inifile.getValue("settings-eclipse.ini", "Run", "eclipse_version")

        self.log.info("################################################################################")
        self.log.info("###  TC 380 - User Built SDk - C++ - Build Hello World C++ Autotools Project ###")
        self.log.info("################################################################################")
        
        self.createProject(projectname, typeproject, searchtype, author, copyrightproject)
        self.log.info("# Step  : Create Project")

        self.open_perspective()
        self.log.info("# Step  : Change Perspective")
        
        self.reconfigure_project(projectname)
        self.log.info("# Step  : Reconfigure Project")
        
        self.build_project()
        self.log.info("# Step  : Build Project")
        
        self.run_project(projectname, searchtype,eclipse_version)
        self.log.info("# Step  : Run Project")

        self.debug_project(projectname, searchtype)
        self.log.info("# Step  : Debug Project")
        
        self.close_project()
        self.log.info("# Step  : Close Project")
        
        self.delete_project(projectname, typeproject)
        self.log.info("# Step  : Delete Project")
        
        self.close_perspective()
        self.log.info("# Step  : Close C/C++ perspective")
    

    @testcase(42)
    def test_42(self):

        projectname = inifile.getValue("settings-eclipse.ini", "TC42_User_Built_SDK_C_Build_Hello_World_GTK_C_Autotools_Project", "Project_name")
        typeproject = inifile.getValue("settings-eclipse.ini", "TC42_User_Built_SDK_C_Build_Hello_World_GTK_C_Autotools_Project", "Wizards")
        searchtype = inifile.getValue("settings-eclipse.ini", "TC42_User_Built_SDK_C_Build_Hello_World_GTK_C_Autotools_Project", "Search")
        author = inifile.getValue("settings-eclipse.ini", "TC42_User_Built_SDK_C_Build_Hello_World_GTK_C_Autotools_Project", "Author")
        copyrightproject = inifile.getValue("settings-eclipse.ini", "TC42_User_Built_SDK_C_Build_Hello_World_GTK_C_Autotools_Project", "Copyright")
        eclipse_version= inifile.getValue("settings-eclipse.ini", "Run", "eclipse_version")

        self.log.info("################################################################################")
        self.log.info("### TC 42 - User Built SDK - C - Build Hello World  GTK C  Autotools Project ###")
        self.log.info("################################################################################")
        
        self.createProject(projectname, typeproject, searchtype, author, copyrightproject)
        self.log.info("# Step  : Create Project")

        self.open_perspective()
        self.log.info("# Step  : Change Perspective")

        self.reconfigure_project(projectname)
        self.log.info("# Step  : Reconfigure Project")
        
        if eclipse_version == 'mars':
            self.reconfigure_project(projectname)
            self.log.info("# Step  : Reconfigure Project")

        self.build_project()
        self.log.info("# Step  : Build Project")

        self.run_project(projectname, searchtype,eclipse_version)
        self.log.info("# Step  : Run Project")

        
        self.debug_project(projectname, searchtype)
        self.log.info("# Step  : Debug Project")
        
        
        #check_passed3ewb = verify_console()
        #ewb
        #self.log.info("# Step  : Verify problems")
        
        self.close_project()
        self.log.info("# Step  : Close Project")

        self.delete_project(projectname, typeproject)
        self.log.info("# Step  : Delete Project")
        
        self.close_perspective()
        self.log.info("# Step  : Close C/C++ perspective")
        

    @testcase(388)
    def test_388(self):

        param1 = inifile.getValue("settings-eclipse.ini", "Run", "param1")
        param2 = inifile.getValue("settings-eclipse.ini", "Run", "param2")
        dateofrun = inifile.getValue("settings-eclipse.ini", "Run", "date")
        projectlocation = '/home/' + getpass.getuser() + '/eclipse-run/' + "run-" + param1 + "-" + param2 + "-" + dateofrun +'/download/'
        
        projectname = inifile.getValue("settings-eclipse.ini", "TC388_BB_Commander-Create_a_User_customized_recipe", "Project_name")
        typeproject = inifile.getValue("settings-eclipse.ini", "TC388_BB_Commander-Create_a_User_customized_recipe", "Wizards")
        perspectivename = inifile.getValue("settings-eclipse.ini", "TC388_BB_Commander-Create_a_User_customized_recipe", "Perspective_name")
        srcURI = inifile.getValue("settings-eclipse.ini", "TC388_BB_Commander-Create_a_User_customized_recipe", "SRC_URI")
        description = inifile.getValue("settings-eclipse.ini", "TC388_BB_Commander-Create_a_User_customized_recipe", "Description")
        recipelicense = inifile.getValue("settings-eclipse.ini", "TC388_BB_Commander-Create_a_User_customized_recipe", "License")
        recipename = inifile.getValue("settings-eclipse.ini", "TC388_BB_Commander-Create_a_User_customized_recipe", "Recipe_name")

        self.log.info("################################################################################")
        self.log.info("###        TC 388 - BB Commander - Create a User customized recipe           ###")
        self.log.info("################################################################################")
        
        self.open_other_perspective(perspectivename)
        self.log.info("# Step  : Create BB Commander Project")
        
        self.create_yocto_project(projectname, projectlocation, typeproject)
        self.log.info("# Step  : Create BB Commander Project")
        
        self.add_bitbake_recipe(projectname, srcURI, description,recipelicense,recipename, pressPopulate=False)
        self.log.info("# Step  : Create BitBake Recipe")
        
        self.close_project()
        self.log.info("# Step  : Close Project")
        
        self.delete_project(projectname, typeproject)
        self.log.info("# Step  : Delete Project")
        
        self.close_perspective()
        self.log.info("# Step  : Close BitBake Commander perspective")
        
    

    @testcase(153)
    def test_153(self):
        
        
        param1 = inifile.getValue("settings-eclipse.ini", "Run", "param1")
        param2 = inifile.getValue("settings-eclipse.ini", "Run", "param2")
        dateofrun = inifile.getValue("settings-eclipse.ini", "Run", "date")
        projectlocation = '/home/' + getpass.getuser() + '/eclipse-run/' + "run-" + param1 + "-" + param2 + "-" + dateofrun  + '/download/'
        
        projectname = inifile.getValue("settings-eclipse.ini", "TC153_BB_Commander-Create_a_customized_recipeu_using_a_source_package", "Project_name")
        typeproject = inifile.getValue("settings-eclipse.ini", "TC153_BB_Commander-Create_a_customized_recipeu_using_a_source_package", "Wizards")
        perspectivename = inifile.getValue("settings-eclipse.ini", "TC153_BB_Commander-Create_a_customized_recipeu_using_a_source_package", "Perspective_name")
        srcURI = inifile.getValue("settings-eclipse.ini", "TC153_BB_Commander-Create_a_customized_recipeu_using_a_source_package", "SRC_URI")
        description = inifile.getValue("settings-eclipse.ini", "TC153_BB_Commander-Create_a_customized_recipeu_using_a_source_package", "Description")
        recipelicense = inifile.getValue("settings-eclipse.ini", "TC153_BB_Commander-Create_a_customized_recipeu_using_a_source_package", "License")
        recipename = inifile.getValue("settings-eclipse.ini", "TC153_BB_Commander-Create_a_customized_recipeu_using_a_source_package", "Recipe_name")

        self.log.info("################################################################################")
        self.log.info("### TC 153 - BB Commander - Create a customized recipe using a source package###")
        self.log.info("################################################################################")
        
        self.open_other_perspective(perspectivename)
        self.log.info("# Step  : Create BB Commander Project")
        
        self.create_yocto_project(projectname, projectlocation, typeproject)
        self.log.info("# Step  : Create BB Commander Project")
        
        self.add_bitbake_recipe(projectname, srcURI, description, recipelicense, recipename, pressPopulate=True)
        self.log.info("# Step  : Create BitBake Recipe")
        
        self.close_project()
        self.log.info("# Step  : Close Project")
        
        self.delete_project(projectname, typeproject)
        self.log.info("# Step  : Delete Project")
        
        self.close_perspective()
        self.log.info("# Step  : Close BitBake Commander perspective")
        

    @testcase(159)
    def test_159(self):
        
        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        param1 = inifile.getValue("settings-eclipse.ini", "Run", "param1")
        param2 = inifile.getValue("settings-eclipse.ini", "Run", "param2")
        dateofrun = inifile.getValue("settings-eclipse.ini", "Run", "date")
        eclipse_version= inifile.getValue("settings-eclipse.ini", "Run", "eclipse_version")
        
        poky = '/home/' + getpass.getuser() + '/eclipse-run/' + "run-" + param1 + "-" + param2 + "-" + dateofrun + '/download/poky'
        workspace = '/home/' + getpass.getuser() + '/eclipse-run/' + "run-" + param1 + "-" + param2 + "-" + dateofrun + "/" + eclipse_version + '/workspace/'
        kernelArch = inifile.getValue("settings-eclipse.ini", "TC159_Yocto-BSP", "Kernel_Arhitecture")
        if (kernelArch == "qemu"):
            qemuArch = inifile.getValue("settings-eclipse.ini", "TC159_Yocto-BSP", "Qemu_Arhitecture")
        else:
            qemuArch = ""
        kernel = inifile.getValue("settings-eclipse.ini", "TC159_Yocto-BSP", "Kernel")
        kernelBranch = inifile.getValue("settings-eclipse.ini", "TC159_Yocto-BSP", "Kernel_branch")
        
        projectNameId = datetime.now().strftime("%d-%m-%Y-%H:%M:%S")
        projectName = 'BSP_' + projectNameId
        
        
        self.log.info("################################################################################")
        self.log.info("###                           TC 159 - Yocto-BSP tool                        ###")
        self.log.info("################################################################################")
        
        
        try:
            YoctoProjectTools = eclipse.child(name = 'YoctoProjectTools', roleName = menu_rolename)
            self.log.info("* Check : Found YoctoProjectTools menu")
            
        except:
            self.fail("can not find YoctoProjectTools menu")
            
        
        YoctoProjectTools.click()
        self.log.info("# Step  : Click on menu <<YoctoProjectTools>>")
        time.sleep(2)
        
        
        try:
            YPTitem = YoctoProjectTools.child(name='yocto-bsp', roleName=menuitem_rolename)
            self.log.info("* Check : Found <<yocto-bsp>> menu item")

        except:
            self.fail("can not find yocto-bsp menu item")
            
        
        YPTitem.click()
        self.log.info("# Step  : Click on menu item <<yocto-bsp>>")
        
        app = tree.root.application('Eclipse')
        frames = app.findChildren(predicate.GenericPredicate(roleName = frame_rolename))
        if (len(frames) == 0):
            self.fail("can not find frames")
            
        
        yoctoBsp = frames[1]
        text = yoctoBsp.findChildren(predicate.GenericPredicate(roleName = text_rolename))
        
        
        text[0].click()
        self.log.info("# Step  : Click on box <<Metadata location>>")
        text[0].text = poky
        self.log.info("* Check : Insert Metadata location")
        
        
        text[1].click()
        self.log.info("# Step  : Click on box <<Build location>>")
        text[1].text = workspace + 'build' + projectName
        self.log.info("* Check : Insert Build location")
        
        
        text[2].click()
        self.log.info("# Step  : Click on box <<BSP Name>>")
        text[2].text = projectName
        self.log.info("* Check : Insert BSP Name")
        
        
        text[3].click()
        self.log.info("# Step  : Click on box <<BSP output location>>")
        text[3].text = workspace + 'output' + projectName
        self.log.info("* Check : Insert BSP output location")
        
        
        comboBox = yoctoBsp.findChildren(predicate.GenericPredicate(roleName=combobox_rolename))
        if (len(comboBox) < 4):
            self.fail("can not find combo boxes")
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = yoctoBsp.child(name = 'Cancel', roleName = button_rolename)
            if (cancel_close.sensitive):
                time.sleep(2)
                cancel_close.click()
            
        else: 
            self.log.info("* Check : Found menu drop-down list Kernel Architecture")
        
        
        comboBox[0].click()
        self.log.info("# Step  : Click on menu drop-down list <<Kernel Architecture>>")
        
        try:
            yoctoBsp.child(name=kernelArch, roleName=menuitem_rolename).click()
            self.log.info("* Check : Found kernel architecture name menu item")

        except:
            self.fail("can not find kernel architecture name menu item")
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = yoctoBsp.child(name = 'Cancel', roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            
        
        comboBox[1].click()
        self.log.info("# Step  : Select <<qemu>>")
        
        print "sleep 4"
        time.sleep(4)
        
        try:
            if eclipse_version =='luna' or eclipse_version=='mars':
                keyCombo("Down")
        
            pressKey("Enter")
            
            #yoctoBsp.child(name="i386", roleName='menu item').click()
            self.log.info("* Check : Found qemu architecture name menu item")
            self.log.info("# Step  : Select Qemu Architecture <<x86_64>>")
        except:
            self.fail("can not find qemu architecture name menu item")
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = yoctoBsp.child(name = 'Cancel', roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            
        
        try:
            next = yoctoBsp.child(name = next_button, roleName = button_rolename)
            self.log.info("* Check : Found Next push button")
        
        except:
            self.fail("can not find Next push button")
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = yoctoBsp.child(name = 'Cancel', roleName = button_rolename)
            if (cancel_close.sensitive):
                time.sleep(2)
                cancel_close.click()
            
        
        if (next.sensitive):
            self.log.info("* Check : Found Next push button sensitive")
            time.sleep(2)
            next.doubleClick()
            self.log.info("# Step  : Click <<Next>>")
        else:	
            self.fail("Next push button not sensitive")
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = yoctoBsp.child(name = 'Cancel', roleName = button_rolename)
            if (cancel_close.sensitive):
                time.sleep(2)
                cancel_close.click()

        comboBox[2].click()
        self.log.info("* Check : Found kernel name menu item")
        try:
            yoctoBsp.child(name = kernel, roleName=menuitem_rolename).click()
            time.sleep(6)
            self.log.info("# Step  : Select kernel<<linux-yocto_3.19>>")
        except:
            self.fail("can not find kernel name menu item")
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = yoctoBsp.child(name = 'Cancel', roleName = button_rolename)
            if (cancel_close.sensitive):
                time.sleep(2)
                cancel_close.click()
            
        
        comboBox[3].click()
        self.log.info("* Check : Found kernel branch menu item")
        
        try:
            yoctoBsp.child(kernelBranch, roleName=menuitem_rolename).click()
            self.log.info("# Step  : Select kernel branch <<standard/base>>")
        except:
            self.fail("can not find kernel name menu item")
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = yoctoBsp.child(name = 'Cancel', roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            
        
        time.sleep(10)
        
        try:
            finish = yoctoBsp.child(name = 'Finish', roleName = button_rolename)
            self.log.info("* Check : Found Finish push button")
        
        except:
            self.fail("can not find Finish push button")
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = yoctoBsp.child(name = 'Cancel', roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            
        
        finish.click()
        self.log.info("# Step  : Click <<Finish>>")
        
        newYoctoBSP =  app.child(name = 'Yocto-BSP ', roleName = frame_rolename)
        try:
            ok = newYoctoBSP.child(name='OK', roleName = button_rolename)
            self.log.info("* Check : Found OK push button")
        
        except:
            self.fail("can not find OK push button")
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = yoctoBsp.child(name = '&Cancel ', roleName = button_rolename)
            if (cancel_close.sensitive):
                time.sleep(2)
                cancel_close.click()
            
        if (ok.sensitive):
            self.log.info("* Check : Found OK push button sensitive")
            ok.click()
            self.log.info("# Step  : Click <<OK>>")
        else:
            self.fail("OK push button not sensitive")
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = yoctoBsp.child(name = 'Cancel', roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()
            
        
        if (os.path.exists(workspace + 'build' + projectName)):
            self.log.info('# Step  : Create  ' + workspace + 'build' + projectName + "")
        else:
            self.log.info("error: " + workspace + 'build' + projectName + " not created")
        
        if (os.path.exists(workspace + 'output' + projectName)):
            self.log.info('# Step  : Create  ' + workspace + 'output' + projectName + "")
        else:
            self.log.info("error: " + workspace + 'output' + projectName + " not created")



    @testcase(157)
    def test_157(self):

        app = tree.root.application('Eclipse')
        eclipse =  app.child(roleName=frame_rolename)

        param1 = inifile.getValue("settings-eclipse.ini", "Run", "param1")
        param2 = inifile.getValue("settings-eclipse.ini", "Run", "param2")
        dateofrun = inifile.getValue("settings-eclipse.ini", "Run", "date")
        eclipse_version= inifile.getValue("settings-eclipse.ini", "Run", "eclipse_version")

        poky = '/home/' + getpass.getuser() + '/eclipse-run/' + "run-" + param1 + "-" + param2 + "-" + dateofrun + '/download/poky'

        workspace = '/home/' + getpass.getuser() + '/eclipse-run/' + "run-" + param1 + "-" + param2 + "-" + dateofrun + "/" + eclipse_version + '/workspace/'
        kernelArch = inifile.getValue("settings-eclipse.ini", "TC157_Yocto-BSP", "Kernel_Arhitecture")
        if (kernelArch == "qemu"):
            qemuArch = inifile.getValue("settings-eclipse.ini", "TC157_Yocto-BSP", "Qemu_Arhitecture")
        else:
            qemuArch = ""
        kernel = inifile.getValue("settings-eclipse.ini", "TC157_Yocto-BSP", "Kernel")
        kernelBranch = inifile.getValue("settings-eclipse.ini", "TC157_Yocto-BSP", "Kernel_branch")

        projectNameId = datetime.now().strftime("%d-%m-%Y-%H:%M:%S")
        projectName = 'BSP_' + projectNameId


        self.log.info("################################################################################")
        self.log.info("###                           TC 157 - Yocto-BSP tool                        ###")
        self.log.info("################################################################################")


        try:
            YoctoProjectTools = eclipse.child(name = 'YoctoProjectTools', roleName = menu_rolename)
            self.log.info("* Check : Found YoctoProjectTools menu")
        except:
            self.fail("can not find YoctoProjectTools menu")

        YoctoProjectTools.click()
        self.log.info("# Step  : Click on menu <<YoctoProjectTools>>")
        time.sleep(2)


        try:
            YPTitem = YoctoProjectTools.child(name='yocto-bsp', roleName=menuitem_rolename)
            self.log.info("* Check : Found <<yocto-bsp>> menu item")

        except:
            self.fail("can not find yocto-bsp menu item")

        YPTitem.click()
        self.log.info("# Step  : Click on menu item <<yocto-bsp>>")


        frames = app.findChildren(predicate.GenericPredicate(roleName = frame_rolename))
        if (len(frames) == 0):
            self.fail("can not find frames")

        yoctoBsp = frames[1]
        text = yoctoBsp.findChildren(predicate.GenericPredicate(roleName = text_rolename))

        message_with_empty_metadata_location = 'Enter the required fields(with *) to create new Yocto Project BSP!'

        text[0].click()
        self.log.info("# Step  : Click on box <<Metadata location>>")
        #text[0].text = wrong_poky_path
        self.log.info("* Check : Insert Metadata location")


        if text[4].text == message_with_empty_metadata_location:
            self.log.info("* Check : Found message: %s" %(message_with_empty_metadata_location))
        else:
            self.fail("can not find %s" %(message_with_empty_metadata_location))


        message_with_invalid_metadata_location = ' Invalid meta data location: Make sure it exists and is a directory!'

        text[0].click()
        self.log.info("# Step  : Click on box <<Metadata location>>")
        text[0].text = "dsadasdasd"
        self.log.info("* Check : Insert Metadata location")


        if text[4].text == message_with_invalid_metadata_location:
            self.log.info("* Check : Found message: %s" %(message_with_invalid_metadata_location))
        else:
            self.fail("can not find %s" %(message_with_invalid_metadata_location))


        wrong_poky_path = '"/home/scripts"'
        message_with_no_poky_in_metadata_location = ' Make sure yocto-bsp exists under %s and is executable!' %(wrong_poky_path)

        text[0].click()
        self.log.info("# Step  : Click on box <<Metadata location>>")
        text[0].text = "/home"
        self.log.info("* Check : Insert Metadata location")

        if text[4].text == message_with_no_poky_in_metadata_location:
            self.log.info("* Check : Found message: %s" %(message_with_no_poky_in_metadata_location))
        else:
            self.fail("can not find %s" %(message_with_no_poky_in_metadata_location))


        text[0].click()
        self.log.info("# Step  : Click on box <<Metadata location>>")
        text[0].text = poky
        self.log.info("* Check : Insert Metadata location")

        text[2].click()
        self.log.info("# Step  : Click on box <<BSP Name>>")
        text[2].text = projectName
        self.log.info("* Check : Insert BSP Name")

        comboBox = yoctoBsp.findChildren(predicate.GenericPredicate(roleName=combobox_rolename))
        if (len(comboBox) < 4):
            self.fail("can not find combo boxes")
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = yoctoBsp.child(name = 'Cancel', roleName = button_rolename)
            if (cancel_close.sensitive):
                time.sleep(2)
                cancel_close.click()
        else:
            self.log.info("* Check : Found menu drop-down list Kernel Architecture")


        comboBox[0].click()
        self.log.info("# Step  : Click on menu drop-down list <<Kernel Architecture>>")

        try:
            yoctoBsp.child(name=kernelArch, roleName=menuitem_rolename).click()
            self.log.info("* Check : Found kernel architecture name menu item")

        except:
            self.fail("can not find kernel architecture name menu item")
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = yoctoBsp.child(name = 'Cancel', roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()

        comboBox[1].click()
        self.log.info("# Step  : Select <<qemu>>")

        print "sleep de 4"
        time.sleep(4)

        try:
            if eclipse_version =='luna' or eclipse_version=='mars':
                keyCombo("Down")

            pressKey("Enter")

            #yoctoBsp.child(name="i386", roleName='menu item').click()
            self.log.info("* Check : Found qemu architecture name menu item")
            self.log.info("# Step  : Select Qemu Architecture <<x86_64>>")
        except:
            self.fail("can not find qemu architecture name menu item")
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = yoctoBsp.child(name = 'Cancel', roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()

        try:
            next = yoctoBsp.child(name = next_button, roleName = button_rolename)
            self.log.info("* Check : Found Next push button")

        except:
            self.fail("can not find Next push button")
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = yoctoBsp.child(name = 'Cancel', roleName = button_rolename)
            if (cancel_close.sensitive):
                time.sleep(2)
                cancel_close.click()

        if (next.sensitive):
            self.log.info("* Check : Found Next push button sensitive")
            time.sleep(2)
            next.doubleClick()
            self.log.info("# Step  : Click <<Next>>")
        else:
            self.fail("Next push button not sensitive")
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = yoctoBsp.child(name = 'Cancel', roleName = button_rolename)
            if (cancel_close.sensitive):
                time.sleep(2)
                cancel_close.click()


        comboBox[2].click()
        self.log.info("* Check : Found kernel name menu item")
        try:
            yoctoBsp.child(name = kernel, roleName=menuitem_rolename).click()
            time.sleep(6)
            self.log.info("# Step  : Select kernel<<linux-yocto_4.1>>")
        except:
            self.fail("can not find kernel name menu item")
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = yoctoBsp.child(name = 'Cancel', roleName = button_rolename)
            if (cancel_close.sensitive):
                time.sleep(2)
                cancel_close.click()

        comboBox[3].click()
        self.log.info("* Check : Found kernel branch menu item")

        try:
            yoctoBsp.child(kernelBranch, roleName=menuitem_rolename).click()
            self.log.info("# Step  : Select kernel branch <<standard/base>>")
        except:
            self.fail("can not find kernel name menu item")
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = yoctoBsp.child(name = 'Cancel', roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()

        time.sleep(10)

        try:
            finish = yoctoBsp.child(name = 'Finish', roleName = button_rolename)
            self.log.info("* Check : Found Finish push button")

        except:
            self.fail("can not find Finish push button")
            self.log.warning("# Warning  : Click <<Cancel>> and jump to next step")
            cancel_close = yoctoBsp.child(name = 'Cancel', roleName = button_rolename)
            if (cancel_close.sensitive):
                cancel_close.click()

        finish.click()
        self.log.info("# Step  : Click <<Finish>>")

        newYoctoBSP =  app.child(name = 'Yocto-BSP ', roleName = frame_rolename)
        try:
            ok = newYoctoBSP.child(name='OK', roleName = button_rolename)
            self.log.info("* Check : Found OK push button")

        except:
            self.fail("can not find OK push button")

        if (ok.sensitive):
            self.log.info("* Check : Found OK push button sensitive")
            ok.click()
            self.log.info("# Step  : Click <<OK>>")
        else:
            self.fail("OK push button not sensitive")

        if (os.path.exists(poky + '/meta-' + projectName)):
            self.log.info('# Step  : Create  ' + poky + '/meta-' + projectName + "")
        else:
            self.fail("error: " + poky + 'meta-' + projectName + " not created")

    @testcase(31)
    def test_31(self):


        self.log.info("#############################################################################")
        self.log.info("###                        TC 31 - Linux tools - Perf                     ###")
        self.log.info("#############################################################################")

        linuxToolsItem = perf_item
        linuxToolsFrame = perf_frame

        self.connection_for_linux_tools(linuxToolsItem, linuxToolsFrame)
        self.log.info("# Step  : New SSH connection for %s" %(linuxToolsItem))

        keyCombo("Enter")
        time.sleep(4)

        typeText("perf top")
        time.sleep(4)
        keyCombo("Enter")

    @testcase(32)
    def test_32(self):

        linuxToolsItem = powertop_item
        linuxToolsFrame = powertop_frame


        self.log.info("#############################################################################")
        self.log.info("###                        TC 32 - Linux tools - PowerTop                 ###")
        self.log.info("#############################################################################")

        self.connection_for_linux_tools(linuxToolsItem, linuxToolsFrame)
        self.log.info("# Step  : New SSH connection for" +linuxToolsItem)





