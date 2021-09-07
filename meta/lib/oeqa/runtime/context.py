#
# Copyright (C) 2016 Intel Corporation
#
# SPDX-License-Identifier: MIT
#

import os
import sys

from oeqa.core.context import OETestContext, OETestContextExecutor
import oeqa.core.target
from oeqa.utils.dump import HostDumper

from oeqa.runtime.loader import OERuntimeTestLoader

class OERuntimeTestContext(OETestContext):
    loaderClass = OERuntimeTestLoader
    runtime_files_dir = os.path.join(
                        os.path.dirname(os.path.abspath(__file__)), "files")

    def __init__(self, td, logger, target,
                 host_dumper, image_packages, extract_dir):
        super(OERuntimeTestContext, self).__init__(td, logger)

        self.target = target
        self.image_packages = image_packages
        self.host_dumper = host_dumper
        self.extract_dir = extract_dir
        self._set_target_cmds()

    def _set_target_cmds(self):
        self.target_cmds = {}

        self.target_cmds['ps'] = 'ps'
        if 'procps' in self.image_packages:
            self.target_cmds['ps'] = self.target_cmds['ps'] + ' -ef'

class OERuntimeTestContextExecutor(OETestContextExecutor):
    _context_class = OERuntimeTestContext

    name = 'runtime'
    help = 'runtime test component'
    description = 'executes runtime tests over targets'

    default_cases = os.path.join(os.path.abspath(os.path.dirname(__file__)),
            'cases')
    default_data = None
    default_test_data = 'data/testdata.json'
    default_tests = ''
    default_json_result_dir = '%s-results' % name

    default_target_type = 'simpleremote'
    default_manifest = 'data/manifest'
    default_server_ip = '192.168.7.1'
    default_target_ip = '192.168.7.2'
    default_extract_dir = 'packages/extracted'

    def register_commands(self, logger, subparsers):
        super(OERuntimeTestContextExecutor, self).register_commands(logger, subparsers)

        runtime_group = self.parser.add_argument_group('runtime options')

        runtime_group.add_argument('--target-type', action='store',
                default=self.default_target_type, choices=['simpleremote', 'qemu'],
                help="Target type of device under test, default: %s" \
                % self.default_target_type)
        runtime_group.add_argument('--target-ip', action='store',
                default=self.default_target_ip,
                help="IP address of device under test, default: %s" \
                % self.default_target_ip)
        runtime_group.add_argument('--server-ip', action='store',
                default=self.default_target_ip,
                help="IP address of device under test, default: %s" \
                % self.default_server_ip)

        runtime_group.add_argument('--host-dumper-dir', action='store',
                help="Directory where host status is dumped, if tests fails")

        runtime_group.add_argument('--packages-manifest', action='store',
                default=self.default_manifest,
                help="Package manifest of the image under test, default: %s" \
                % self.default_manifest)

        runtime_group.add_argument('--extract-dir', action='store',
                default=self.default_extract_dir,
                help='Directory where extracted packages reside, default: %s' \
                % self.default_extract_dir)

        runtime_group.add_argument('--qemu-boot', action='store',
                help="Qemu boot configuration, only needed when target_type is QEMU.")

    @staticmethod
    def getTarget(target_type, logger, target_ip, server_ip, **kwargs):
        target = None

        if target_ip:
            target_ip_port = target_ip.split(':')
            if len(target_ip_port) == 2:
                target_ip = target_ip_port[0]
                kwargs['port'] = target_ip_port[1]

        if target_type == 'simpleremote':
            logger.info("Using obsolete simpleremote target, use oeqa.core.target.ssh.OESSHTarget")
            return oeqa.core.target.ssh.OESSHTarget(logger, target_ip, server_ip, **kwargs)
        elif target_type == 'qemu':
            logger.info("Using obsolete qemu target, use oeqa.core.target.qemu.OEQemuTarget")
            return oeqa.core.target.qemu.OEQemuTarget(logger, None, server_ip, **kwargs)
        else:
            import importlib
            packagename, classname = target_type.rsplit(".", 1)
            module = importlib.import_module(packagename)
            target_class = getattr(module, classname)
            if not issubclass(target_class, oeqa.core.target.OETarget):
                raise TypeError(f"Class {target_type} is not an instance of oeqa.target.OETarget")
            return target_class(logger, target_ip, server_ip, **kwargs)

    @staticmethod
    def readPackagesManifest(manifest):
        if not manifest or not os.path.exists(manifest):
            raise OSError("Manifest file not exists: %s" % manifest)

        image_packages = set()
        with open(manifest, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    image_packages.add(line.split()[0])

        return image_packages

    @staticmethod
    def getHostDumper(cmds, directory):
        return HostDumper(cmds, directory)

    def _process_args(self, logger, args):
        if not args.packages_manifest:
            raise TypeError('Manifest file not provided')

        super(OERuntimeTestContextExecutor, self)._process_args(logger, args)

        target_kwargs = {}
        target_kwargs['qemuboot'] = args.qemu_boot

        self.tc_kwargs['init']['target'] = \
                OERuntimeTestContextExecutor.getTarget(args.target_type,
                        None, args.target_ip, args.server_ip, **target_kwargs)
        self.tc_kwargs['init']['host_dumper'] = \
                OERuntimeTestContextExecutor.getHostDumper(None,
                        args.host_dumper_dir)
        self.tc_kwargs['init']['image_packages'] = \
                OERuntimeTestContextExecutor.readPackagesManifest(
                        args.packages_manifest)
        self.tc_kwargs['init']['extract_dir'] = args.extract_dir

_executor_class = OERuntimeTestContextExecutor
