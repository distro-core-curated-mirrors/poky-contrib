__author__ = 'cosscat'

import os
import sys
from time import time, sleep
from subprocess import PIPE, Popen
from IPython import embed


class Result():
    pass

class TestParams(object):
    stick = ''
    retest = ''
    pass
    

class basic_functionality(TestParams):

    def __init__(self):
        self.poky_dir = ['', TestParams.poky_dir][TestParams.poky_dir is not '']
        self.build_dir = ['', TestParams.build_dir][TestParams.build_dir is not '']
        self.dwl_dir = ['', TestParams.dwl_dir][TestParams.dwl_dir is not '']
        self.img_file = ['', TestParams.img_file][TestParams.img_file is not '']
        self.retest = ['No', 'Yes'][TestParams.retest == 'Yes']

        self.board = TestParams.board
        self.bsp= TestParams.bsp
        self.core_name = TestParams.core_name
        self.test_type = TestParams.test_type
        self.release = TestParams.release
        self.SW_ip = "192.168.99.50" # hard coded, never changes in our setup
        self.stick = TestParams.stick # will retain the stick no. chosen to be written on

    def run_comamd_locally(self, command):
        exit_code = os.system(command)
        return exit_code

    def run_command_remotelly(self,remote_ip, command, user='root'):
        """
        This func. will run a command on a remote machine. It is supposed that the network is set up to
        accept ssh communication without credentials, via ssh keys
        """
        cmd = 'rsh -o StrictHostKeyChecking=no {}@{} "{}"'.format(user, remote_ip, command)
        proc = Popen(args=cmd, stdout=PIPE, shell=True, executable='/bin/bash')
        retval = proc.communicate()[0]                  # so using this small trick
        exit_code = proc.returncode
        Result.exit_code = exit_code
        Result.retval = retval
        return Result

    def rezerve_stick(self):
        """
        On the USB_SW machine there is a script, rezerve_stick.sh that randomly choses a stick to write
        the image on. This script gets the board name as parameter like so identifying the USB rail on
        which it is connected.
        """
        command = "/root/USB_SW/rezerve_stick.py {}".format(self.board)
        res = self.run_command_remotelly(self.SW_ip, command)
        TestParams.stick =  res.retval
        return res.retval # this is the value of the stick name


    def get_board_ip(self):
        """
        This function uses dhcpd.conf file from dhcp server to get the assigned board IP
        in our case the dhcp server's ip is hard coded, never changes
        """
        found = ''
        #lines = list()
        command = 'ssh cornel@10.237.112.97 \"cat /etc/dhcp/dhcpd.conf\" > dhcpd.conf'
        status = os.system(command)
        if status != 0:
            found = False
            return found
        with open('dhcpd.conf', 'r') as f:
            lines = f.readlines()
        os.remove('dhcpd.conf')
        for (index,value) in enumerate(lines):
            if str(value).find(self.board) != -1:
                ind = index
                while True:
                    if str(lines[ind]).find('fixed-address') != -1:
                        self.board_ip = str(lines[ind]).replace(';','').split()[1]
                        break
                    elif str(lines[ind]).find('}') != -1:
                        self.board_ip = ''
                        break
                    ind += 1
                break
        return

    def wait_for_ping(self, timeout=120):
        """
        Wait for the board to come on-line for 120 seconds
        """
        start_time = time()
        on_line = ''
        command = "ping -c 1 {} >/dev/null 2>&1".format(self.board_ip)
        while True:
            res = self.run_command_remotelly(self.SW_ip, command)
            if res.exit_code == 0:
                on_line = True
                break
            sleep(1)
            if (int(start_time) + int(timeout)) > time():
                on_line = False
                break
        return on_line

    def read_file(self,file):
        with open(file, 'r') as f:
            lines = f.read().split(os.linesep)
        return lines


    def write_file(self, file, text):
        with open(file, 'w') as f:
            if type(text) is list:
                for line in text:
                    f.write(line + os.linesep)
            else:
                f.write(text)

    def append_to_file(self, file, text):
        with open(file, 'a') as f:
            if type(text) is list:
                for line in text:
                    f.write(line)
            else:
                f.write(text)

    def erase_from_file(self, file, text):
        file_lines = self.read_file(file)
        if type(text) is list:
            for item in text:
                if item in file_lines:
                    file_lines.remove(item)
                else:
                    print "{} not in {}".format(item, file)
        else:
            if text in file_lines:
                file_lines.remove(text)
            else:
                print "{} not in {}".format(text, file)
        self.write_file(file, file_lines)
