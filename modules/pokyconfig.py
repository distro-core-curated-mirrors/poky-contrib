__author__ = 'cosscat'
"""
this module will be responsible for various config adds on local.conf
or whatever config file is needed for poky
"""
import os, re
from IPython import embed
from ConfigParser import SafeConfigParser
from base import basic_functionality, TestParams


class Config(basic_functionality):

    cfg_pth = os.path.join(os.path.dirname(__file__), 'config_adds') # path to config files
    lclcfg = os.path.join(cfg_pth, 'localconf_adds.cfg')
    bspcfg = os.path.join(cfg_pth, 'BSP.cfg')
    brdcfg = os.path.join(cfg_pth, 'Boards.cfg')


    def __init__(self):
        pass

    def read_config_block(self,file, section):
        file_content = self.read_file(file)
        read_cfg = list()
        for (index, value) in enumerate(file_content):
            if value.strip() == "[{}]".format(section):
                ind = index + 1
                while ind < file_content.__len__() and \
                        not re.match('\[.*\]$', file_content[ind].strip()):
                    read_cfg.append(file_content[ind].strip())
                    ind += 1
                break
        return read_cfg

    def lcl_cfg_append(self):
        read_cfg = list()
        read_cfg = self.read_config_block(Config.lclcfg, self.board)
        read_cfg.extend(self.read_config_block(Config.lclcfg,"RUN_TEST"))

        #embed()

        # append config to local.conf
        for (index, value) in enumerate(read_cfg):
            if re.match("^BBLAYERS", value):
                layer_name = value.split("=")[1].strip()
                if '"' in layer_name:
                    layer_name = layer_name.split('"')[1]

                layer_full_path = os.path.join(self.get_cfg_param("poky_base_dir", "GENERAL"), "poky", layer_name)
                read_cfg[index] = 'BBLAYERS += "{}"'.format(layer_full_path)


        pth_to_lclconf = os.path.join(
            self.get_cfg_param("poky_base_dir", "GENERAL"),
            "poky",
            self.get_cfg_param("build_dir", self.board),
            "conf"
        )
        lclcfg_file = os.path.join(pth_to_lclconf, "local.conf")
        inc_file = os.path.join(pth_to_lclconf, "extra_conf.inc")

        incl_string = "include extra_conf.inc"
        if not incl_string in self.read_file(lclcfg_file):
            self.append_to_file(lclcfg_file, incl_string)

        self.write_file(inc_file, read_cfg)


        """
        ramas de facut:
        de adaugat o functie pentru manipularea oricarui parametru, nu numai BBLAYERS,
        adica sa decida daca este necesara sau nu adaugarea ghilimelelor
        """

        return read_cfg

    @classmethod
    def get_cfg_param(self, param, section='', cfg_file=''):
        fl = [cfg_file, Config.bspcfg][cfg_file is '']
        cfg_parser = SafeConfigParser()
        cfg_parser.read(fl)
        return cfg_parser.get(section, param)

    @classmethod
    def get_section_params(self, section, file_name ):
        cfg_parser = SafeConfigParser()
        cfg_parser.read(file_name)
        params=dict()
        for name,value in cfg_parser.items(section):
            params[name] = value
        return params


