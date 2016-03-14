__author__ = 'cosscat'

import os
import sys
from time import time, sleep
from subprocess import PIPE, Popen, STDOUT
import re
from IPython import embed


class TestParams(object):
    stick = ''
    retest = ''
    pass
    

class basic_functionality(TestParams):

    def __init__(self):

        self.poky_dir = TestParams.poky_dir if TestParams.poky_dir else ''
        self.build_dir = TestParams.build_dir if TestParams.build_dir else ''
        self.dwl_dir = TestParams.dwl_dir if TestParams.dwl_dir else ''
        self.img_file = TestParams.img_file if TestParams.img_file else ''
        self.retest = TestParams.retest if TestParams.retest else 'No'

        self.board = TestParams.board
        self.board_ip = ''
        self.bsp = TestParams.bsp
        self.core_name = TestParams.core_name
        self.test_type = TestParams.test_type
        self.release = TestParams.release
        self.SW_ip = "192.168.99.50"  #FIXME: not ok: hard coded, never changes in our setup
        self.stick = TestParams.stick  # will retain the stick no. chosen to be written on

    @staticmethod
    def run_command_locally(cmd):
        """
        Run a command locally and return it's exit code and value
        :param cmd: Command to run locally
        :return: Result with exit_code and output
        """
        # TODO: redirect strerr to stdout
        proc = Popen(args=cmd, stdout=PIPE, stderr=STDOUT, shell=True, executable='/bin/bash')
        retval = proc.communicate()[0]
        retcode = proc.returncode

        return retcode, retval

    def run_command_remotely(self, remote_ip, command, user='root'):
        """
        This func. will run a command on a remote machine.
        WARNING: It is supposed that the network is set up to
        accept ssh communication without credentials, via ssh keys
        """
        cmd = 'rsh -o StrictHostKeyChecking=no {}@{} "{}"'.format(user, remote_ip, command)
        retcode, retval = self.run_command_locally(cmd)

        return retcode, retval

    def rezerve_stick(self):
        """
        On the USB_SW machine there is a script, rezerve_stick.sh that randomly chooses a stick to write
        the image on. This script gets the board name as parameter like so identifying the USB rail on
        which it is connected.
        """
        # FIXME: THIS IS NOT VERY PORTABLE
        command = "/root/USB_SW/rezerve_stick.py {}".format(self.board)
        retcode, retval = self.run_command_remotely(self.SW_ip, command)
        if retcode:
            raise ValueError('Command failed. Exit code (%s) is not zero.' % retcode)
        TestParams.stick = retval

        return retval  # this is the value of the stick name

    def get_board_ip(self):
        """
        This function uses dhcpd.conf file from dhcp server to get the assigned board IP
        in our case the dhcp server's ip is hard coded, never changes
        """
        # FIXME: THIS IS NOT VERY PORTABLE

        dhcp_serv_user = 'cornel'
        dhcp_serv_ip = '10.237.112.97'
        command = 'ssh %s@%s \"cat /etc/dhcp/dhcpd.conf\"' % (dhcp_serv_user, dhcp_serv_ip)

        retcode, retval = self.run_command_locally(command)
        if retcode:
            raise ValueError('Command failed. Exit code (%s) is not zero.' % retcode)

        # Look for something like this
        # host NUC_1{
        #   hardware ethernet c0:3f:d5:67:02:ae;
        # 	fixed-address 192.168.99.52;
        #   option host-name "NUC_1";
        # }

        patt = '\s+host\s+%s\s*\{.*?fixed-address\s+(\S+)\s*;' % self.board
        found_ip = re.findall(patt, retval, re.DOTALL)
        if not found_ip:
            raise Exception('Failed to get the ip address for %s' % self.board)

        self.board_ip = found_ip[0]

        return self.board_ip

    def wait_for_ping(self, timeout=120):
        """
        Wait for the board to come on-line for 120 seconds
        """
        start_time = time()
        command = "ping -c 1 {} >/dev/null 2>&1".format(self.board_ip)
        while True:
            retcode, retval = self.run_command_remotely(self.SW_ip, command)
            if not retcode:
                return True
            sleep(1)
            if (int(start_time) + int(timeout)) > time():
                return False

    def read_file(self, filename):
        with open(filename, 'r') as f:
            lines = f.read().splitlines()
        return lines

    def write_file(self, filename, text):
        with open(filename, 'w') as f:
            if type(text) is list:
                for line in text:
                    f.write(line + os.linesep)
            else:
                f.write(text)

    def append_to_file(self, filename, text):
        with open(filename, 'a') as f:
            if type(text) is list:
                for line in text:
                    f.write(line)
            else:
                f.write(text)

    def erase_from_file(self, filename, text):
        file_lines = self.read_file(filename)
        if type(text) is list:
            for item in text:
                if item in file_lines:
                    file_lines.remove(item)
                else:
                    print "{} not in {}".format(item, filename)
        else:
            if text in file_lines:
                file_lines.remove(text)
            else:
                print "{} not in {}".format(text, filename)
        self.write_file(filename, file_lines)
