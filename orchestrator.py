#!/usr/bin/python

__author__ = 'cosscat'

import sys, os, argparse
import modules.pokyconfig as cfg
import modules.control_SW as SW
import modules.imgdwl as imgdwl
from modules.base import TestParams


from IPython import embed

description="Automation harness for runtime tests. Designed to interface with any device that " \
            "would auto deploy images on boards"
parser = argparse.ArgumentParser(description)


class Orchestrator(object):
    """
    This class resembles steps performed in the chronological order when testing a board
    1) get .manifest .direct or .hddimg from a remote link
    2) prepare the env by writing config files: bblayers.conf or local.conf
    """
    def __init__(self):
        self.work_dir = cfg.Config.get_cfg_param("poky_base_dir", "GENERAL")
        self.prepare_env()

    def prepare_env(self):
        TestParams.poky_dir = os.path.join(cfg.Config.get_cfg_param("poky_base_dir","GENERAL"), 'poky')
        TestParams.build_dir = os.path.join(TestParams.poky_dir, cfg.Config.get_cfg_param("build_dir", TestParams.board))
        TestParams.dwl_dir = os.path.join(TestParams.build_dir, "tmp/deploy/images", TestParams.bsp)


    def get_artifacts(self, artifact_type, retest="No"):
        #maybe it would be fine to add a step to get poky too ...
        if retest == "No":
            TestParams.retest = "No"
            dwl = imgdwl.OnlineDwl()
            dwl.dwl_artifacts(artifact_type)
            #need to change imgdwl in order to prevent the case when retest is yes but there is no image.
        else:
            TestParams.retest = "Yes"
            return


    def prepare_cfg(self):
        conf = cfg.Config()
        conf.lcl_cfg_append()
        remote = imgdwl.UseImage()
        if remote.send_img_to_USB_SW() != 0:
            sys.exit("An error occured during image trasnsfer to USB-SW machine."
                     "Please check your settings and retry.")

        if remote.write_image_on_stick() != 0:
            print "An error occured during writing image on: ".format(TestParams.stick)

    def install_image(self):
        print "inside SW control"
        ctrl_SW = SW.BoardsManipulation()
        print "writing image on usb stick: {}".format(TestParams.stick)
        ctrl_SW.installImage()


if __name__ == "__main__":
    initial_cfg_file = os.path.join(os.getcwd(), "params.cfg") # aici sunt parametri pe care ii trimite LAVA sau
    # ce env de lansare a testelor au ei

    tp = TestParams
    tp.board = cfg.Config.get_cfg_param('board', 'SENT_PARAMS', initial_cfg_file)
    tp.release = cfg.Config.get_cfg_param('release', 'SENT_PARAMS',initial_cfg_file)
    tp.bsp = cfg.Config.get_cfg_param('bsp', 'SENT_PARAMS', initial_cfg_file)
    tp.core_name = cfg.Config.get_cfg_param('core_name', 'SENT_PARAMS', initial_cfg_file)
    tp.test_type = cfg.Config.get_cfg_param('test_type', 'SENT_PARAMS', initial_cfg_file)
    tp.img_file = ''


    t = Orchestrator()
    #embed()
    t.get_artifacts("manifest",retest="Yes")
    t.get_artifacts("hddimg",retest="Yes")
    t.prepare_cfg()
    t.install_image()

"""
#this was for testing purposes only
    tp.board = 'NUC_2'
    tp.release = 'yocto-2.1_M2.rc1'
    #tp.release = 'yocto-2.0.1.rc7'
    tp.bsp = 'intel-corei7-64'
    #tp.bsp = 'genericx86'
    #tp.bsp = 'genericx86-64'
    tp.core_name = 'core-image-sato'
    #tp.test_type = 'generic'
    tp.test_type = 'meta-intel'
    #tp.test_type = 'wic_AB'
    tp.img_file = ''
"""



