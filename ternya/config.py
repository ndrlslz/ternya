"""
ternya.config
=============

This module read customer's config file.
"""
from configparser import ConfigParser, NoSectionError, NoOptionError
from ternya import ConfigError
import logging

log = logging.getLogger(__name__)


class Config:
    """
    This class Read Configuration
    """

    def __init__(self, config_path):
        self.config = ConfigParser()
        self.config.read(config_path)
        self.method_mapping = {
            str: self.get_str,
            int: self.get_int
        }
        # default
        self.project_abspath = self.get_config_value("default", "project_abspath", str)
        self.packages_scan = self.get_config_value("default", "packages_scan", str)
        # nova
        self.nova_mq_user = self.get_config_value("nova", "mq_user", str)
        self.nova_mq_password = self.get_config_value("nova", "mq_password", str)
        self.nova_mq_host = self.get_config_value("nova", "mq_host", str)
        self.nova_mq_exchange = "nova"
        self.nova_mq_queue = "ternya_nova_queue"
        self.nova_mq_consumer_count = self.get_config_value("nova", "mq_consumer_count", int)
        # cinder
        self.cinder_mq_user = self.get_config_value("cinder", "mq_user", str)
        self.cinder_mq_password = self.get_config_value("cinder", "mq_password", str)
        self.cinder_mq_host = self.get_config_value("cinder", "mq_host", str)
        self.cinder_mq_exchange = "cinder"
        self.cinder_mq_queue = "ternya_cinder_queue"
        self.cinder_mq_consumer_count = self.get_config_value("cinder", "mq_consumer_count", int)

    def get_config_value(self, section, key, return_type: type):
        """Read customer's config value by section and key.

        :param section: config file's section. i.e [default]
        :param key: config file's key under section. i.e packages_scan
        :param return_type: (optional) value type, default is str.
        """
        try:
            value = self.method_mapping[return_type](section, key)
        except NoSectionError as e:
            raise ConfigError(e.message)
        except NoOptionError as e:
            raise ConfigError(e.message)
        return value

    def get_int(self, section, key) -> int:
        return self.config.getint(section, key, fallback=1)

    def get_str(self, section, key) -> str:
        return self.config.get(section, key, fallback="")
