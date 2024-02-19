#
# Copyright (C) 2023-2024 Siemens AG
#
# SPDX-License-Identifier: GPL-2.0-only
#
"""Devtool ide-sdk IDE plugin interface definition and helper functions"""

import errno
import json
import logging
import os
import stat
from enum import Enum, auto
from devtool import DevtoolError
from bb.utils import mkdirhier

logger = logging.getLogger('devtool')


class BuildTool(Enum):
    UNDEFINED = auto()
    CMAKE = auto()
    MESON = auto()
    AUTOTOOLS = auto()

    @property
    def is_c_ccp(self):
        if self is BuildTool.CMAKE:
            return True
        if self is BuildTool.MESON:
            return True
        if self is BuildTool.AUTOTOOLS:
            return True
        return False


class GdbCrossConfig:
    """Base class defining the GDB configuration generator interface

    Generate a GDB configuration for a binary on the target device.
    Only one instance per binary is allowed. This allows to assign unique port
    numbers for all gdbserver instances.
    """
    _gdbserver_port_next = 1234
    _binaries = []

    def __init__(self, image_recipe, modified_recipe, binary, gdbserver_multi=True):
        self.image_recipe = image_recipe
        self.modified_recipe = modified_recipe
        self.gdb_cross = modified_recipe.gdb_cross
        self.binary = binary
        if binary in GdbCrossConfig._binaries:
            raise DevtoolError(
                "gdbserver config for binary %s is already generated" % binary)
        GdbCrossConfig._binaries.append(binary)
        self.script_dir = modified_recipe.ide_sdk_scripts_dir
        self.gdbinit_dir = os.path.join(self.script_dir, 'gdbinit')
        self.gdbserver_multi = gdbserver_multi
        self.binary_pretty = self.binary.replace(os.sep, '-').lstrip('-')
        self.gdbserver_port = GdbCrossConfig._gdbserver_port_next
        GdbCrossConfig._gdbserver_port_next += 1
        self.id_pretty = "%d_%s" % (self.gdbserver_port, self.binary_pretty)
        # gdbserver start script
        gdbserver_script_file = 'gdbserver_' + self.id_pretty
        if self.gdbserver_multi:
            gdbserver_script_file += "_m"
        self.gdbserver_script = os.path.join(
            self.script_dir, gdbserver_script_file)
        # gdbinit file
        self.gdbinit = os.path.join(
            self.gdbinit_dir, 'gdbinit_' + self.id_pretty)
        # gdb start script
        self.gdb_script = os.path.join(
            self.script_dir, 'gdb_' + self.id_pretty)

    def _gen_gdbserver_start_script(self):
        """Generate a shell command starting the gdbserver on the remote device via ssh

        GDB supports two modes:
        multi: gdbserver remains running over several debug sessions
        once: gdbserver terminates after the debugged process terminates
        """
        cmd_lines = ['#!/bin/sh']
        if self.gdbserver_multi:
            temp_dir = "TEMP_DIR=/tmp/gdbserver_%s; " % self.id_pretty
            gdbserver_cmd_start = temp_dir
            gdbserver_cmd_start += "test -f \\$TEMP_DIR/pid && exit 0; "
            gdbserver_cmd_start += "mkdir -p \\$TEMP_DIR; "
            gdbserver_cmd_start += "%s --multi :%s > \\$TEMP_DIR/log 2>&1 & " % (
                self.gdb_cross.gdbserver_path, self.gdbserver_port)
            gdbserver_cmd_start += "echo \\$! > \\$TEMP_DIR/pid;"

            gdbserver_cmd_stop = temp_dir
            gdbserver_cmd_stop += "test -f \\$TEMP_DIR/pid && kill \\$(cat \\$TEMP_DIR/pid); "
            gdbserver_cmd_stop += "rm -rf \\$TEMP_DIR; "

            gdbserver_cmd_l = []
            gdbserver_cmd_l.append('if [ "$1" = "stop" ]; then')
            gdbserver_cmd_l.append('  shift')
            gdbserver_cmd_l.append("  %s %s %s %s 'sh -c \"%s\"'" % (
                self.gdb_cross.target_device.ssh_sshexec, self.gdb_cross.target_device.ssh_port, self.gdb_cross.target_device.extraoptions, self.gdb_cross.target_device.target, gdbserver_cmd_stop))
            gdbserver_cmd_l.append('else')
            gdbserver_cmd_l.append("  %s %s %s %s 'sh -c \"%s\"'" % (
                self.gdb_cross.target_device.ssh_sshexec, self.gdb_cross.target_device.ssh_port, self.gdb_cross.target_device.extraoptions, self.gdb_cross.target_device.target, gdbserver_cmd_start))
            gdbserver_cmd_l.append('fi')
            gdbserver_cmd = os.linesep.join(gdbserver_cmd_l)
        else:
            gdbserver_cmd_start = "%s --once :%s %s" % (
                self.gdb_cross.gdbserver_path, self.gdbserver_port, self.binary)
            gdbserver_cmd = "%s %s %s %s 'sh -c \"%s\"'" % (
                self.gdb_cross.target_device.ssh_sshexec, self.gdb_cross.target_device.ssh_port, self.gdb_cross.target_device.extraoptions, self.gdb_cross.target_device.target, gdbserver_cmd_start)
        cmd_lines.append(gdbserver_cmd)
        GdbCrossConfig.write_file(self.gdbserver_script, cmd_lines, True)

    def _gen_gdbinit_config(self):
        """Generate a gdbinit file for this binary and the corresponding gdbserver configuration"""
        gdbinit_lines = ['# This file is generated by devtool ide-sdk']
        if self.gdbserver_multi:
            target_help = '#   gdbserver --multi :%d' % self.gdbserver_port
            remote_cmd = 'target extended-remote'
        else:
            target_help = '#   gdbserver :%d %s' % (
                self.gdbserver_port, self.binary)
            remote_cmd = 'target remote'
        gdbinit_lines.append('# On the remote target:')
        gdbinit_lines.append(target_help)
        gdbinit_lines.append('# On the build machine:')
        gdbinit_lines.append('#   cd ' + self.modified_recipe.real_srctree)
        gdbinit_lines.append(
            '#   ' + self.gdb_cross.gdb + ' -ix ' + self.gdbinit)

        gdbinit_lines.append('set sysroot ' + self.modified_recipe.d)
        gdbinit_lines.append('set substitute-path "/usr/include" "' +
                             os.path.join(self.modified_recipe.recipe_sysroot, 'usr', 'include') + '"')
        # Disable debuginfod for now, the IDE configuration uses rootfs-dbg from the image workdir.
        gdbinit_lines.append('set debuginfod enabled off')
        if self.image_recipe.rootfs_dbg:
            gdbinit_lines.append(
                'set solib-search-path "' + self.modified_recipe.solib_search_path_str(self.image_recipe) + '"')
            # First: Search for sources of this recipe in the workspace folder
            if self.modified_recipe.pn in self.modified_recipe.target_dbgsrc_dir:
                gdbinit_lines.append('set substitute-path "%s" "%s"' %
                                     (self.modified_recipe.target_dbgsrc_dir, self.modified_recipe.real_srctree))
            else:
                logger.error(
                    "TARGET_DBGSRC_DIR must contain the recipe name PN.")
            # Second: Search for sources of other recipes in the rootfs-dbg
            if self.modified_recipe.target_dbgsrc_dir.startswith("/usr/src/debug"):
                gdbinit_lines.append('set substitute-path "/usr/src/debug" "%s"' % os.path.join(
                    self.image_recipe.rootfs_dbg, "usr", "src", "debug"))
            else:
                logger.error(
                    "TARGET_DBGSRC_DIR must start with /usr/src/debug.")
        else:
            logger.warning(
                "Cannot setup debug symbols configuration for GDB. IMAGE_GEN_DEBUGFS is not enabled.")
        gdbinit_lines.append(
            '%s %s:%d' % (remote_cmd, self.gdb_cross.host, self.gdbserver_port))
        gdbinit_lines.append('set remote exec-file ' + self.binary)
        gdbinit_lines.append(
            'run ' + os.path.join(self.modified_recipe.d, self.binary))

        GdbCrossConfig.write_file(self.gdbinit, gdbinit_lines)

    def _gen_gdb_start_script(self):
        """Generate a script starting GDB with the corresponding gdbinit configuration."""
        cmd_lines = ['#!/bin/sh']
        cmd_lines.append('cd ' + self.modified_recipe.real_srctree)
        cmd_lines.append(self.gdb_cross.gdb + ' -ix ' +
                         self.gdbinit + ' "$@"')
        GdbCrossConfig.write_file(self.gdb_script, cmd_lines, True)

    def initialize(self):
        self._gen_gdbserver_start_script()
        self._gen_gdbinit_config()
        self._gen_gdb_start_script()

    @staticmethod
    def write_file(script_file, cmd_lines, executable=False):
        script_dir = os.path.dirname(script_file)
        mkdirhier(script_dir)
        with open(script_file, 'w') as script_f:
            script_f.write(os.linesep.join(cmd_lines))
            script_f.write(os.linesep)
        if executable:
            st = os.stat(script_file)
            os.chmod(script_file, st.st_mode | stat.S_IEXEC)
        logger.info("Created: %s" % script_file)


class IdeBase:
    """Base class defining the interface for IDE plugins"""

    def __init__(self):
        self.ide_name = 'undefined'
        self.gdb_cross_configs = []

    @classmethod
    def ide_plugin_priority(cls):
        """Used to find the default ide handler if --ide is not passed"""
        return 10

    def setup_shared_sysroots(self, shared_env):
        logger.warn("Shared sysroot mode is not supported for IDE %s" %
                    self.ide_name)

    def setup_modified_recipe(self, args, image_recipe, modified_recipe):
        logger.warn("Modified recipe mode is not supported for IDE %s" %
                    self.ide_name)

    def initialize_gdb_cross_configs(self, image_recipe, modified_recipe, gdb_cross_config_class=GdbCrossConfig):
        binaries = modified_recipe.find_installed_binaries()
        for binary in binaries:
            gdb_cross_config = gdb_cross_config_class(
                image_recipe, modified_recipe, binary)
            gdb_cross_config.initialize()
            self.gdb_cross_configs.append(gdb_cross_config)

    @staticmethod
    def gen_oe_scrtips_sym_link(modified_recipe):
        # create a sym-link from sources to the scripts directory
        if os.path.isdir(modified_recipe.ide_sdk_scripts_dir):
            IdeBase.symlink_force(modified_recipe.ide_sdk_scripts_dir,
                                  os.path.join(modified_recipe.real_srctree, 'oe-scripts'))

    @staticmethod
    def update_json_file(json_dir, json_file, update_dict):
        """Update a json file

        By default it uses the dict.update function. If this is not sutiable
        the update function might be passed via update_func parameter.
        """
        json_path = os.path.join(json_dir, json_file)
        logger.info("Updating IDE config file: %s (%s)" %
                    (json_file, json_path))
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)
        try:
            with open(json_path) as f:
                orig_dict = json.load(f)
        except json.decoder.JSONDecodeError:
            logger.info(
                "Decoding %s failed. Probably because of comments in the json file" % json_path)
            orig_dict = {}
        except FileNotFoundError:
            orig_dict = {}
        orig_dict.update(update_dict)
        with open(json_path, 'w') as f:
            json.dump(orig_dict, f, indent=4)

    @staticmethod
    def symlink_force(tgt, dst):
        try:
            os.symlink(tgt, dst)
        except OSError as err:
            if err.errno == errno.EEXIST:
                if os.readlink(dst) != tgt:
                    os.remove(dst)
                    os.symlink(tgt, dst)
            else:
                raise err


def get_devtool_deploy_opts(args):
    """Filter args for devtool deploy-target args"""
    if not args.target:
        return None
    devtool_deploy_opts = [args.target]
    if args.no_host_check:
        devtool_deploy_opts += ["-c"]
    if args.show_status:
        devtool_deploy_opts += ["-s"]
    if args.no_preserve:
        devtool_deploy_opts += ["-p"]
    if args.no_check_space:
        devtool_deploy_opts += ["--no-check-space"]
    if args.ssh_exec:
        devtool_deploy_opts += ["-e", args.ssh.exec]
    if args.port:
        devtool_deploy_opts += ["-P", args.port]
    if args.key:
        devtool_deploy_opts += ["-I", args.key]
    if args.strip is False:
        devtool_deploy_opts += ["--no-strip"]
    return devtool_deploy_opts
