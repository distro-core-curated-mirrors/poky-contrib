#!/usr/bin/env python

import sys, os, re
import random as r 


cfg_dir='/root/USB_SW/config_files/'

sticks_names=['stick1', 'stick2', 'stick3', 'stick4']
machin_bank1=['usb1', 'usb2', 'usb3', 'usb4', 'usb5', 'usb6', 'usb7']
machin_bank2=['usb8', 'usb9', 'usb10', 'usb11', 'usb12', 'usb13', 'usb14']   

sticks_mapping={}
m66313fp_file = open(cfg_dir + "m66313fp_mapping.cfg")
for line in m66313fp_file:
  for st_name in sticks_names: 
    if (st_name == line.split(":")[0]): 
      sticks_mapping[st_name] = int(line.split(":")[1])
   
#print sticks_mapping

bsp=sys.argv[1]

f = open(cfg_dir + 'last_word_sent','r')
last_word = int(f.readline())
f.close()

machine_assigned_ports={}
machines_file = open(cfg_dir + "machine_mapping.cfg")
for line in machines_file:
    machine_assigned_ports[line.split(":")[0]] = (line.split(":")[1], line.split(":")[2])    
machines_file.close()



def determine_availability(bsp_name):

  free_stick=[]
  if machine_assigned_ports[bsp_name][0] in machin_bank1:
     if not (sticks_mapping['stick1'] & last_word):
       free_stick.append('stick1')   
     if not (sticks_mapping['stick2'] & last_word):
       free_stick.append('stick2')    
  if machine_assigned_ports[bsp_name][0] in machin_bank2:
     if not (sticks_mapping['stick3'] & last_word):
       free_stick.append('stick3')
     if not (sticks_mapping['stick4'] & last_word):
       free_stick.append('stick4')
  print free_stick[r.randrange(0,len(free_stick))]

if __name__ == '__main__':  
  determine_availability(bsp)   
