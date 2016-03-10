import argparse, re, time, os, serial, glob, sys
from time import sleep

cfg_dir='/root/USB_SW/config_files/'
base_dir='/root/USB_SW/'
#read m66313 pin mapping

m66313fp_mapping={}
m66313fp_file = open(os.path.join(cfg_dir, "m66313fp_mapping.cfg"))
for line in m66313fp_file:
    m66313fp_mapping[line.split(":")[0]] = int(line.split(":")[1])
m66313fp_file.close()

#assign respective ppins to each machine

machines_mapping={}
machine_assigned_ports={}
machine_names=[]

machines_file = open(os.path.join(cfg_dir + "machine_mapping.cfg"))
for line in machines_file:
    machines_mapping[line.split(":")[0]] = (int(m66313fp_mapping[line.split(":")[1]]), int(m66313fp_mapping[line.split(":")[2]])) # creez o tupla de valori usb/pwr asignate fiecarui BSP
    machine_assigned_ports[line.split(":")[0]] = (line.split(":")[1], line.split(":")[2])
    machine_names.append(line.split(":")[0]) 
machines_file.close()

# here we will prepare the word to send:
 
class USBSW(object):
    def __init__(self):
        port=glob.glob("/dev/serial/by-id/*1a86*")[0]
        self.uart=serial.Serial(port,9600)
        if (self.uart.isOpen()):
          print(port + " serial port successfully initialized.\n")
          sleep(1)
        else:
          print("USB-SW is not connected. Please connect the USB-SW\n")


    def __compose_word_to_send(self,params):

	print "params sent ",params
        f = open(cfg_dir + 'last_word_sent','r')
        word_to_send = int(f.readline())
        f.close()
        usb_bank1_mask = 257024 # masca pentru bancul 1 de pini alocati usb1~7
        usb_bank2_mask = 3690987568 # masca pentru bancul 1 de pini alocati usb8~14
        usb_bank1=('usb1','usb2','usb3','usb4','usb5','usb6','usb7')
        usb_bank2=('usb8','usb9','usb10','usb11','usb12','usb13','usb14')

        pwr_bank1_mask = 66584576
        pwr_bank2_mask = 967
        pwr_bank1=('pwr1','pwr2','pwr3','pwr4','pwr5','pwr6','pwr7')
        pwr_bank2=('pwr8','pwr9','pwr10','pwr11','pwr12','pwr13','pwr14')

        stick_bank1_mask = 266240
        stick_bank2_mask = 536870920
        stick_bank1=('stick1','stick2')
        stick_bank2=('stick3','stick4')

        stick = params['stick']
        board = params['board']
        brd_usb = params['board_usb']
        brd_pwr = params['board_pwr']
        stick_dir = params['stick_to']

        if board:
          m = machines_mapping[board]
          m_usb = m[0]
          m_pwr = m[1]

          if (brd_usb == 'on') and (machine_assigned_ports[board][0] in usb_bank1):
            word_to_send = word_to_send & (~usb_bank1_mask) | m_usb
          elif (brd_usb == 'on') and (machine_assigned_ports[board][0] in usb_bank2):
            word_to_send = word_to_send & (~usb_bank2_mask) | m_usb
          elif (brd_usb == 'off') and (machine_assigned_ports[board][0] in usb_bank1):
            word_to_send = word_to_send & (~usb_bank1_mask)
          elif (brd_usb == 'off') and (machine_assigned_ports[board][0] in usb_bank2):
            word_to_send = word_to_send & (~usb_bank2_mask)
    # de aici incolo se realizeaza controlul de alimentare
          p = m66313fp_mapping[machine_assigned_ports[board][1]]
          if (machine_assigned_ports[board][1] in pwr_bank1) and (brd_pwr == 'off'):
            word_to_send = word_to_send & (~pwr_bank1_mask) | p
          elif (machine_assigned_ports[board][1] in pwr_bank1) and (brd_pwr == 'on'):
            word_to_send = word_to_send & (~pwr_bank1_mask)
          elif (machine_assigned_ports[board][1] in pwr_bank2) and (brd_pwr == 'off'):
            word_to_send = word_to_send & (~pwr_bank2_mask) | p
          elif (machine_assigned_ports[board][1] in pwr_bank2) and (brd_pwr == 'on'):
            word_to_send = word_to_send & (~pwr_bank2_mask)
    # de aici incolo se ia decizia doar pentru stick
        if stick:
          stk = m66313fp_mapping[stick] #obtin numarul corespunzator stick-ului pentru m66313fp
          if (stick in stick_bank1) and (stick_dir == 'board'):
            word_to_send = word_to_send & (~stick_bank1_mask) | stk
          elif (stick in stick_bank1) and (stick_dir == 'pc'):
            word_to_send = word_to_send & (~stick_bank1_mask)
          elif (stick in stick_bank2) and (stick_dir == 'board'):
            word_to_send = word_to_send & (~stick_bank2_mask) | stk
          elif (stick in stick_bank2) and (stick_dir == 'pc'):
            word_to_send = word_to_send & (~stick_bank2_mask)
        else:
          pass
        return word_to_send

    def send_to_SW(self, args):
        wts = self.__compose_word_to_send(args)
        if (wts >= 0):
          f=open(os.path.join(cfg_dir, 'last_word_sent'),'w')
          f.write(str(wts))
          f.close()

        full_bin_no='0'*(32-len(str(bin(int(wts)))[2:])) + str(bin(int(wts)))[2:] # calculul numarului final de trimis
        i=0
        self.uart.write('b')
	sent_word = ''
        while(i < 32):
          each_byte=full_bin_no[i:i+8]
          self.uart.write(str(int(each_byte,2)))
	  sent_word += each_byte
          if (i != 24):
            self.uart.write(',')
          i += 8
        self.uart.write('e')
        self.uart.close()
	print "Sent word to USB-SW: {}".format(sent_word)
	return sent_word


if __name__ == "__main__":
    print "Used as stand alone module. This module is intended to work inside a framework/system."
    usb_cmd_line_choices=['on','off','ON','OFF']
    pwr_cmd_line_choices=['ON','on','OFF','off']
    stick_cmd_line_choices=['pc','board']
    stick_names = ['stick1', 'stick2', 'stick3', 'stick4']   

    parser = argparse.ArgumentParser(description='Program de controlat i/o pentru USB-SW')
    parser.add_argument('-m','--machine',nargs=1 , dest='machines', choices=machine_names)
    parser.add_argument('stick',nargs='?', default=None, choices=stick_names)
    parser.add_argument('-u','--usb', dest='usb',nargs=1, default='off', choices=usb_cmd_line_choices)
    parser.add_argument('-p','--pwr',nargs=1, dest='pwr', default='on', choices=pwr_cmd_line_choices)
    parser.add_argument('-s','--stick',nargs=1, dest='st_option', default='pc', choices=stick_cmd_line_choices)
    args = parser.parse_args()
    
    print args

    params = dict()
    params['stick'] = '' if not args.stick else args.stick
    params['board'] = '' if not args.machines else args.machines[0]
    params['board_usb'] = '' if not args.usb else args.usb[0]
    params['board_pwr'] = '' if not args.pwr else args.pwr[0] 
    params['stick_to'] = '' if not args.st_option else args.st_option[0]

    SW = USBSW()
    SW.send_to_SW(params)
