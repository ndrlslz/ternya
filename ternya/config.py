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
        self.project_abspath = self.get_config_value("default", "project_abspath")
        self.packages_scan = self.get_config_value("default", "packages_scan")
        self.nova_mq_user = self.get_config_value("nova", "mq_user")
        self.nova_mq_password = self.get_config_value("nova", "mq_password")
        self.nova_mq_host = self.get_config_value("nova", "mq_host")
        self.nova_mq_exchange = "nova"
        self.nova_mq_queue = "ternya_nova_queue"
        self.nova_mq_consumer_count = self.get_config_value("nova", "mq_consumer_count", int)

    def get_config_value(self, section, key, return_type=str):
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

    def get_int(self, section, key):
        return self.config.getint(section, key)

    def get_str(self, section, key):
        return self.config.get(section, key)
