#!/usr/bin/env python3

import os
import sys

# Set up sys.path to let us import tinfoil
scripts_path = os.path.dirname(os.path.realpath(__file__))
lib_path = scripts_path + '/lib'
sys.path.insert(0, lib_path)
import scriptpath
scriptpath.add_bitbake_lib_path()

import bb.tinfoil
import time


config_only = False

def tf(sleep):
    with bb.tinfoil.Tinfoil() as tinfoil:
        tinfoil.prepare(config_only=config_only)
        tmpdir = tinfoil.config_data.getVar('TMPDIR')
        print('TMPDIR is "%s"' % tmpdir)

    time.sleep(sleep)
    with bb.tinfoil.Tinfoil() as tinfoil:
        tinfoil.prepare(config_only=config_only)
        tmpdir = tinfoil.config_data.getVar('TMPDIR')
        print('TMPDIR is "%s"' % tmpdir)


sleep = 0
print('\n\nwith delay %s' % sleep)
tf(sleep)

sleep = 1
print('\n\nwith delay %s' % sleep)
tf(sleep)
