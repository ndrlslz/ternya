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
            int: self.get_int,
            bool: self.get_bool
        }
        # default
        self.project_abspath = self.get_config_value("default", "project_abspath", str)
        self.packages_scan = self.get_config_value("default", "packages_scan", str)
        self.mq_user = self.get_config_value("default", "mq_user", str)
        self.mq_password = self.get_config_value("default", "mq_password", str)
        self.mq_host = self.get_config_value("default", "mq_host", str)
        # nova
        self.nova_mq_exchange = "nova"
        self.nova_mq_queue = "ternya_nova_queue"
        self.listen_nova_notification = self.get_config_value("nova", "listen_notification", bool)
        self.nova_mq_consumer_count = self.get_config_value("nova", "mq_consumer_count", int)
        # cinder
        self.cinder_mq_exchange = "cinder"
        self.cinder_mq_queue = "ternya_cinder_queue"
        self.listen_cinder_notification = self.get_config_value("cinder", "listen_notification", bool)
        self.cinder_mq_consumer_count = self.get_config_value("cinder", "mq_consumer_count", int)
        # neutron
        self.neutron_mq_exchange = "neutron"
        self.neutron_mq_queue = "ternya_neutron_queue"
        self.listen_neutron_notification = self.get_config_value("neutron", "listen_notification", bool)
        self.neutron_mq_consumer_count = self.get_config_value("neutron", "mq_consumer_count", int)

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

    def get_bool(self, section, key) -> bool:
        return self.config.getboolean(section, key, fallback=False)
