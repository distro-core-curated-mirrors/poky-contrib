__author__ = 'cosscat'

import os
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
import modules.SW_ctrl as sw
import modules.kb_emu as kb_emu


def sw_control(params):
    cmd = sw.USBSW()
    sent_word = cmd.send_to_SW(params)
    print params
    return sent_word

def keyboard_emu(board, my_str):
    print board
    print my_str
    kb = kb_emu.KeybEmu(board) 
    kb.send_keys_to_machine(my_str,ae="No")
    kb.close()
    return "good"

server_ip = "192.168.99.50"

server = SimpleXMLRPCServer((server_ip, 8000))
print "Listening on port 8000..."
server.register_function(sw_control, "sw_control")
server.register_function(keyboard_emu, "keyboard_emu")
server.serve_forever()
