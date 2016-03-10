import re, xmlrpclib
from time import sleep

from base import basic_functionality
from pokyconfig import Config

class USB_SW(basic_functionality):
    """
    This class is the main interface with the physical USB-SW device.
    """
    def __init__(self):
        """
        self.param_list is the dict. containing possible params for SW_interface.py script
        """
        super(USB_SW, self).__init__()
        self.get_board_ip() # returns the board IP from dhcp server config file
        self.USB_SW_img_dir = "/root/BSP_images/"
        self.param_dict = {
            "board" : "-m {}".format(self.board),
            "stick_to" : "-s pc",
            "board_pwr" : "-p on",
            "board_usb" : "-u off"
        } # this is the default
        self.param_xmlrpc = {
            "stick" : self.stick,
            "board" : "{}".format(self.board),
            "stick_to" : "pc",
            "board_pwr" : "on",
            "board_usb" : "off"
        } # this is the default for xmlrpc transmission



    def board_pwr(self, pwr, inverted = False):
        """
        There are cases when a board behaves oposed to the intuitive way for a boot
        """
        if inverted and pwr == "on":
            self.param_dict['board_pwr'] = "-p off"
            self.param_xmlrpc["board_pwr"] = "off"
        elif inverted and pwr == "off":
            self.param_dict['board_pwr'] = "-p on"
            self.param_xmlrpc["board_pwr"] = "on"
        elif pwr == "off":
            self.param_dict['board_pwr'] = "-p off"
            self.param_xmlrpc["board_pwr"] = "off"
        else:
            self.param_dict['board_pwr'] = "-p on"
            self.param_xmlrpc["board_pwr"] = "on"

    def board_usb(self, usb):
        """
        This function sets the usb status for a board. It is eigther connected to the USB rail or not
        """
        if usb == "on":
            self.param_dict['board_usb'] = "-u on"
            self.param_xmlrpc['board_usb'] = "on"
        else:
            self.param_dict['board_usb'] = "-u off"
            self.param_xmlrpc['board_usb'] = "off"

    def stick_to(self, hw):
        """
        :param hw: tells where the stick should be coupled to: either PC or board
        """
        if hw == "board":
            self.param_dict['stick_to'] = "-s board"
            self.param_xmlrpc['stick_to'] = "board"
        else:
            self.param_dict['stick_to'] = "-s pc"
            self.param_xmlrpc['stick_to'] = "pc"

    def execute_command(self):
        """
        This is the old style method, via rsh to the switch
        we use xmlrpc now
        :return:
        """
        command = '/root/USB_SW/SW_interface.py {} {} {} {} {}'.format(self.stick,
                                                                      self.param_dict["board"],
                                                                      self.param_dict["stick_to"],
                                                                      self.param_dict["board_usb"],
                                                                      self.param_dict["board_pwr"]
                                                                       )
        #print command
        #res = self.run_command_remotelly(self.SW_ip, command)
        #return res


class BoardsManipulation(USB_SW):
    def __init__(self):
        super(BoardsManipulation,self).__init__()
        self.proxy = xmlrpclib.ServerProxy("http://{}:8000/".format(self.SW_ip))

    def boardComand(self):
        print self.param_xmlrpc
        sent_word = self.proxy.sw_control(self.param_xmlrpc)
        print sent_word

    def keyboard(self, cmd):
        print cmd
        self.proxy.keyboard_emu(self.board, cmd)

    def installImage(self):
        cfg_file = Config.brdcfg
        install_steps = Config.get_section_params(self.board, cfg_file)
        command_definition = Config.get_section_params("DEFINITIONS", cfg_file)
        for step in range(1, len(install_steps)+1):
            command = install_steps["cmd{}".format(step)]
            if command in command_definition.keys():
                pwr, st, usb = command_definition[command].strip().split(',')
                self.board_pwr(pwr)
                self.stick_to(st)
                self.board_usb(usb)
                self.boardComand()

            elif re.match("wait.*", command):
                sec = float(command.split()[1])
                print "wait: {}s".format(sec)
                sleep(sec)

            elif re.match("write.*", command):
                cmd = command.split("write")[1].strip()
                self.keyboard(cmd)
