# Copyright (C) 2016 Intel Corporation
# Released under the MIT license (see COPYING.MIT)

import os

from oeqa.core.context import OETestContext, OETestContextExecutor
from oeqa.core.target.ssh import OESSHTarget
from oeqa.runtime.loader import OERuntimeTestLoader

class OERuntimeTestContext(OETestContext):
    loaderClass = OERuntimeTestLoader
    runtime_files_dir = os.path.join(
                        os.path.dirname(os.path.abspath(__file__)), "files")

    def __init__(self, td, logger, target, packages_manifest):
        super(OERuntimeTestContext, self).__init__(td, logger)
        self.target = target
        self.image_packages = self.readPackagesManifest(packages_manifest)
        self._set_target_cmds()

    def _set_target_cmds(self):
        self.target_cmds = {}

        self.target_cmds['ps'] = 'ps'
        if 'procps' in self.image_packages:
            self.target_cmds['ps'] = self.target_cmds['ps'] + ' -ef'

    def readPackagesManifest(self, manifest):
        if not os.path.exists(manifest):
            raise OSError("Couldn't find manifest file: %s" % manifest)

        image_packages = set()
        with open(manifest, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    image_packages.add(line.split()[0])

        return image_packages

    def _get_json_file(self, module_path):
        """
        Returns the path of the JSON file for a module, empty if doesn't exitst.
        """

        json_file = '%s.json' % module_path.rsplit('.', 1)[0]
        if os.path.isfile(module_path) and os.path.isfile(json_file):
            return json_file
        else:
            return ''

    def _get_needed_packages(self, json_file, test=None):
        """
        Returns a dict with needed packages based on a JSON file.


        If a test is specified it will return the dict just for that test.
        """

        import json

        needed_packages = {}

        with open(json_file) as f:
            test_packages = json.load(f)
        for key,value in test_packages.items():
            needed_packages[key] = value

        if test:
            if test in needed_packages:
                needed_packages = needed_packages[test]
            else:
                needed_packages = {}

        return needed_packages

    def extract_packages(self, d, ed, needed_packages):
        """
        Extract packages that will be needed during runtime.
        """

        import oe.path

        extracted_path = ed['TEST_EXTRACTED_DIR']

        for key,value in needed_packages.items():
            packages = ()
            if isinstance(value, dict):
                packages = (value, )
            elif isinstance(value, list):
                packages = value
            else:
                bb.fatal('Failed to process needed packages for %s; '
                         'Value must be a dict or list' % key)

            for package in packages:
                pkg = package['pkg']
                rm = package.get('rm', False)
                extract = package.get('extract', True)

                if extract:
                    self.logger.debug(1, 'Extracting %s' % pkg)
                    dst_dir = os.path.join(extracted_path, pkg)
                    # Same package used for more than one test,
                    # don't need to extract again.
                    if os.path.exists(dst_dir):
                        continue

                    # Extract package and copy it to TEST_EXTRACTED_DIR
                    pkg_dir = self._extract_in_tmpdir(d, ed, pkg)
                    oe.path.copytree(pkg_dir, dst_dir)
                    shutil.rmtree(pkg_dir)

                else:
                    self.logger.debug(1, 'Copying %s' % pkg)
                    self._copy_package(d, ed, pkg)

    def _extract_in_tmpdir(self, d, ed, pkg):
        """"
        Returns path to a temp directory where the package was
        extracted without dependencies.
        """

        from oeqa.utils.package_manager import get_package_manager

        pkg_path = os.path.join(ed['TEST_INSTALL_TMP_DIR'], pkg)
        pm = get_package_manager(d, pkg_path)
        extract_dir = pm.extract(pkg)
        shutil.rmtree(pkg_path)

        return extract_dir

    def _copy_package(self, d, ed, pkg):
        """
        Copy the RPM, DEB or IPK package to dst_dir
        """

        from oeqa.utils.package_manager import get_package_manager

        pkg_path = os.path.join(ed['TEST_INSTALL_TMP_DIR'], pkg)
        dst_dir = ed['TEST_PACKAGED_DIR']
        pm = get_package_manager(d, pkg_path)
        pkg_info = pm.package_info(pkg)
        file_path = pkg_info[pkg]['filepath']
        shutil.copy2(file_path, dst_dir)
        shutil.rmtree(pkg_path)

    def install_uninstall_packages(self, test_id, pkg_dir, install):
        """
        Check if the test requires a package and Install/Unistall it in the DUT
        """

        test = test_id.split('.')[4]
        module = self.getModulefromID(test_id)
        json = self._getJsonFile(module)
        if json:
            needed_packages = self._getNeededPackages(json, test)
            if needed_packages:
                self._install_uninstall_packages(needed_packages, pkg_dir, install)

    def _install_uninstall_packages(self, needed_packages, pkg_dir, install=True):
        """
        Install/Unistall packages in the DUT without using a package manager
        """

        if isinstance(needed_packages, dict):
            packages = [needed_packages]
        elif isinstance(needed_packages, list):
            packages = needed_packages

        for package in packages:
            pkg = package['pkg']
            rm = package.get('rm', False)
            extract = package.get('extract', True)
            src_dir = os.path.join(pkg_dir, pkg)

            # Install package
            if install and extract:
                self.target.connection.copy_dir_to(src_dir, '/')

            # Unistall package
            elif not install and rm:
                self.target.connection.delete_dir_structure(src_dir, '/')

class OERuntimeTestContextExecutor(OETestContextExecutor):
    _context_class = OERuntimeTestContext

    name = 'runtime'
    help = 'runtime test component'
    description = 'executes runtime tests over targets'

    default_cases = os.path.join(os.path.abspath(os.path.dirname(__file__)),
            'cases')
    default_data = None

    default_target_type = 'simpleremote'
    default_server_ip = '192.168.7.1'
    default_target_ip = '192.168.7.2'

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

        runtime_group.add_argument('--packages-manifest', action='store',
                help="Package manifest of the image under test")

    def _process_args(self, logger, args):
        if not args.packages_manifest:
            raise TypeError('Manifest file not provided')

        super(OERuntimeTestContextExecutor, self)._process_args(logger, args)
        target = OESSHTarget(args.target_ip)

        self.tc_kwargs['init']['target'] = target

        packages_manifest = os.path.join(os.getcwd(), args.packages_manifest)
        self.tc_kwargs['init']['packages_manifest'] = packages_manifest

_executor_class = OERuntimeTestContextExecutor
