from configparser import ConfigParser, NoSectionError, NoOptionError
from ternya import ConfigError
import logging

log = logging.getLogger(__name__)


class Config:
    def __init__(self):
        self.config = ConfigParser()
        self.project_abspath = None
        self.component_scan = None
        self.nova_mq_password = None
        self.nova_mq_user = None
        self.openstack_host = None

    def read(self, config_path):
        self.config.read(config_path)
        self.project_abspath = self.get_config_value("default", "project_abspath")
        self.component_scan = self.get_config_value("default", "component_scan")
        self.openstack_host = self.get_config_value("default", "openstack_host")
        self.nova_mq_user = self.get_config_value("nova", "mq_user")
        self.nova_mq_password = self.get_config_value("nova", "mq_password")

    def get_config_value(self, section, key):
        try:
            value = self.config.get(section, key)
        except NoSectionError as e:
            raise ConfigError(e.message)
        except NoOptionError as e:
            raise ConfigError(e.message)
        return value
