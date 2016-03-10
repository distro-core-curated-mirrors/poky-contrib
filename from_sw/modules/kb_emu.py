import os, sys, usbkm232 
import basic_functionality as bf
from IPython import embed

class KeybEmu(usbkm232.UsbKm232):
    def __init__(self, board='', s_port=''):
        self.keyb_cfg = dict()
        self.brd = board
        serial_port = s_port
        self.keyb_cfg = self.read_config() # read conf file and populates keyb_cfg dict {machine:serial_port}
        #print self.check_for_board()
	if self.brd and self.check_for_board():
	    serial_port = self.keyb_cfg[self.brd]
	elif s_port and not board:
	    serial_port = s_port
	else:
            print "No serial port provided."
	    return
	    
	serial_port = os.path.join("/dev/serial/by-path", serial_port)
        usbkm232.UsbKm232.__init__(self,serial_port) # for whatever reason i couldn't make it work with super()

    @classmethod	    	
    def read_config(self):
        module_path = os.path.abspath(__file__)
        cfg_file_path = os.path.join(os.path.dirname(module_path), "..", "config_files", "keyboard_emu.cfg")
	keyb_cfg = dict()
        cfg_content = bf.read_file(cfg_file_path)
        for line in cfg_content:
            if not (line.startswith('#') or line == ''): # avoid blanks and comments
		#because the port path name contains ":" we cannot just split after ":", so will use an other trick
		pos = line.find(":")
		keyb_cfg[line[:pos]] = line[pos+1:].strip()
	return keyb_cfg
					
    def check_for_board(self):
	if self.brd == '' or self.brd not in self.keyb_cfg.keys():
	    print "No configured serial port found in config_files/keyboard_emu.cfg {}.".\
		format(['',"for %s"%self.brd][self.brd is not ''])	
	    return False
	else:
	    return True
					
    def send_keys_to_machine(self, my_str, ae='Yes'):#ae stands for auto-enter, meaning after each command, send an enter
# i prefered to overwrite the usbkm232 module's key dict, because using  send_list_of_commands([list of chars)
# gives finer control over key emu device.
# only special commands are sent through generate_command_from_input() method
	command = my_str
        #pth = os.path.abspath(__path__)
	#cfg_fl = os.path.join(pth, 'logfile')
	#with open(cfg_fl,'a') as f:
	#    f.write(command)

	print "comande este: %s" % command
	command_non_writable = ['uparrow',
				'downarrow',
				'larrow',
				'rarrow',
				'capslock',
				'enter',
				'lshift',
				'f10']
	#embed()
	if command in command_non_writable:
	    command = '{}{}{}'.format('<',command,'>')
	    print command
	    self.generate_command_from_input(command)
	else:
	    for ch in command:
		if ch.isalpha():
		    if ch.isupper():
			key_no = usbkm232.UsbKm232.KEYS[ch.lower()]
			self.send_list_of_commands([chr(44), chr(key_no)])
				# the above is basically a <shift> + low(ch). e.g. A ---> shift + "a"
		    else:
			key_no = usbkm232.UsbKm232.KEYS[ch]
			self.send_list_of_commands([chr(key_no)])
		elif ch == ":":
		    self.send_list_of_commands([chr(44),chr(40)]) # this is a shift + ":"
		else:
		    self.generate_command_from_input(ch)

	if ae == 'Yes':
	    self.generate_command_from_input("<enter>")
	


if __name__ == "__main__":
    s = \
"""
This is a module and is intended to be used as such. For fast keyboard emulation purposes only
one can pass as arguments the /dev/serial/by-path/ value of the serial port followed by a no 
space separated string. The result is the string being sent to the corresponding keyboard emu.
device.
e.g.:  python kb_emu.py "pci-0000:00:14.0-usb-0:1.4.3:1.0-port0" "Hello_:)"
"""
    def help_menu():
        print s
	
    if len(sys.argv) != 3:
	help_menu()
	sys.exit("ERROR: Wrong no. of parameters sent.")
	
    sp = sys.argv[1]
    str_to_send = sys.argv[2]
    kb = KeybEmu(s_port=sp)
    kb.send_keys_to_machine(str_to_send)
    kb.close()
 		    
		
