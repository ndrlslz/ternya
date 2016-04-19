"""
ternya.modules
==============

This module import customer's service module.
"""
import glob
import os
import logging

from ternya import ImportModulesError

log = logging.getLogger(__name__)


class Modules(object):
    def __init__(self, config):
        self.config = config
        self._modules = []

    def import_modules(self):
        pass


class ServiceModules(Modules):
    """
    This class deal with customer's service modules.
    Service module means the module include methods for process notification.
    """

    def __init__(self, config):
        super().__init__(config)
        self.project_abspath = self.config.project_abspath
        self.packages_scan = self.config.packages_scan

    def get_modules(self):
        """Get modules by project_abspath and packages_scan.

        Traverse all files under folder packages_scan which set by customer.
        And get all modules name.
        """
        if not self.project_abspath:
            raise TypeError("project_abspath can not be empty.")
        packages_abspath = self.get_package_abspath()
        for package_abspath in packages_abspath:
            self.get_module_name(package_abspath)

        return self._modules

    def import_modules(self):
        """Import customer's service module."""
        modules = self.get_modules()
        log.info("import service modules: " + str(modules))
        try:
            for module in modules:
                __import__(module)
        except ImportError as error:
            raise ImportModulesError(error.msg)

    def get_package_abspath(self):
        packages_scan_list = self.packages_scan.split(";")
        packages_abspath = list(map(lambda x: os.path.join(self.project_abspath, x.replace(".", os.path.sep)),
                                    packages_scan_list))
        return packages_abspath

    def get_module_name(self, path):
        for sub_path in glob.glob(os.path.join(path, '*')):
            if os.path.isdir(sub_path):
                self.get_module_name(sub_path)
            else:
                if sub_path.endswith(".py") and not sub_path.endswith("__init__.py"):
                    module_name = sub_path[len(self.project_abspath) + 1:-3]
                    self._modules.append(module_name.replace(os.path.sep, "."))
