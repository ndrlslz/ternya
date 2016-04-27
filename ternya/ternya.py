"""
ternya.ternya
=============

This module do main work.
"""
import time
import logging
from amqp import ConnectionForced

from ternya import Config, ServiceModules, MQ, Openstack
from ternya import ProcessFactory
from ternya import MQConnectionError

log = logging.getLogger(__name__)


class Ternya:
    """
    Ternya main class.

    First, you need to use ternya to read your config file.
    Then invoke work() to start ternya.

    *Example usage*::

        >>> from ternya import Ternya
        >>>
        >>> if __name__ == "__main__":
        >>>     ternya = Ternya()
        >>>     ternya.read("config.ini")
        >>>     ternya.work()

    If you use ternya in your project, you need to start a process to start ternya.
    *Example usage*::
    
        >>> from ternya import Ternya
        >>> from multiprocessing import Process
        >>>
        >>> if __name__ == "__main__":
        >>>     ternya = Ternya()
        >>>     ternya.read("config.ini")
        >>>     process = Process(target=ternya.work)
        >>>     process.start()

    ..note::
        If you start ternya with process. And your os is windows.
        'if __name__ == "__main__"' is necessary.
    """

    def __init__(self):
        self.config = None

    def read(self, path):
        """
        Load customer's config information.

        :param path: customer config path.
        """
        self.config = Config(path)

    def work(self):
        """
        Start ternya work.

        First, import customer's service modules.
        Second, init openstack mq.
        Third, keep a ternya connection that can auto-reconnect.
        """
        self.init_modules()
        connection = self.init_mq()
        TernyaConnection(self, connection).connect()

    def init_mq(self):
        """Init connection and consumer with openstack mq."""
        mq = self.init_connection()
        self.init_consumer(mq)
        return mq.connection

    def init_modules(self):
        """Import customer's service modules."""
        if not self.config:
            raise ValueError("please read your config file.")

        log.debug("begin to import customer's service modules.")
        modules = ServiceModules(self.config)
        modules.import_modules()
        log.debug("end to import customer's service modules.")

    def init_connection(self):
        mq = MQ(self.config.mq_user,
                self.config.mq_password,
                self.config.mq_host)
        mq.create_connection()
        return mq

    def init_consumer(self, mq):
        self.init_nova_consumer(mq)
        self.init_cinder_consumer(mq)
        self.init_neutron_consumer(mq)
        self.init_glance_consumer(mq)
        self.init_swift_consumer(mq)
        self.init_keystone_consumer(mq)
        self.init_heat_consumer(mq)

    def init_nova_consumer(self, mq):
        """
        Init openstack nova mq

        1. Check if enable listening nova notification
        2. Create consumer

        :param mq: class ternya.mq.MQ
        """
        if not enable_component_notification(self.config, Openstack.Nova):
            log.debug("disable listening nova notification")
            return

        for i in range(self.config.nova_mq_consumer_count):
            mq.create_consumer(self.config.nova_mq_exchange,
                               self.config.nova_mq_queue,
                               ProcessFactory.process(Openstack.Nova))
        log.debug("enable listening openstack nova notification.")

    def init_cinder_consumer(self, mq):
        """
        Init openstack cinder mq

        1. Check if enable listening cinder notification
        2. Create consumer

        :param mq: class ternya.mq.MQ
        """
        if not enable_component_notification(self.config, Openstack.Cinder):
            log.debug("disable listening cinder notification")
            return

        for i in range(self.config.cinder_mq_consumer_count):
            mq.create_consumer(self.config.cinder_mq_exchange,
                               self.config.cinder_mq_queue,
                               ProcessFactory.process(Openstack.Cinder))

        log.debug("enable listening openstack cinder notification.")

    def init_neutron_consumer(self, mq):
        """
        Init openstack neutron mq

        1. Check if enable listening neutron notification
        2. Create consumer

        :param mq: class ternya.mq.MQ
        """
        if not enable_component_notification(self.config, Openstack.Neutron):
            log.debug("disable listening neutron notification")
            return

        for i in range(self.config.neutron_mq_consumer_count):
            mq.create_consumer(self.config.neutron_mq_exchange,
                               self.config.neutron_mq_queue,
                               ProcessFactory.process(Openstack.Neutron))

        log.debug("enable listening openstack neutron notification.")

    def init_glance_consumer(self, mq):
        """
        Init openstack glance mq

        1. Check if enable listening glance notification
        2. Create consumer

        :param mq: class ternya.mq.MQ
        """
        if not enable_component_notification(self.config, Openstack.Glance):
            log.debug("disable listening glance notification")
            return

        for i in range(self.config.glance_mq_consumer_count):
            mq.create_consumer(self.config.glance_mq_exchange,
                               self.config.glance_mq_queue,
                               ProcessFactory.process(Openstack.Glance))

        log.debug("enable listening openstack glance notification.")

    def init_swift_consumer(self, mq):
        """
        Init openstack swift mq

        1. Check if enable listening swift notification
        2. Create consumer

        :param mq: class ternya.mq.MQ
        """
        if not enable_component_notification(self.config, Openstack.Swift):
            log.debug("disable listening swift notification")
            return

        for i in range(self.config.swift_mq_consumer_count):
            mq.create_consumer(self.config.swift_mq_exchange,
                               self.config.swift_mq_queue,
                               ProcessFactory.process(Openstack.Swift))

        log.debug("enable listening openstack swift notification.")

    def init_keystone_consumer(self, mq):
        """
        Init openstack swift mq

        1. Check if enable listening keystone notification
        2. Create consumer

        :param mq: class ternya.mq.MQ
        """
        if not enable_component_notification(self.config, Openstack.Keystone):
            log.debug("disable listening keystone notification")
            return

        for i in range(self.config.keystone_mq_consumer_count):
            mq.create_consumer(self.config.keystone_mq_exchange,
                               self.config.keystone_mq_queue,
                               ProcessFactory.process(Openstack.Keystone))

        log.debug("enable listening openstack keystone notification.")

    def init_heat_consumer(self, mq):
        """
        Init openstack heat mq

        1. Check if enable listening heat notification
        2. Create consumer

        :param mq: class ternya.mq.MQ
        """
        if not enable_component_notification(self.config, Openstack.Heat):
            log.debug("disable listening heat notification")
            return

        for i in range(self.config.heat_mq_consumer_count):
            mq.create_consumer(self.config.heat_mq_exchange,
                               self.config.heat_mq_queue,
                               ProcessFactory.process(Openstack.Heat))

        log.debug("enable listening openstack heat notification.")


class TernyaConnection:
    """
    This class keep the connection with openstack mq.

    If connection interrupt, try to reconnect openstack mq
    """

    def __init__(self, ternya, connection):
        self.connection = connection
        self.ternya = ternya

    def connect(self):
        while True:
            try:
                self.connection.drain_events()
            except (ConnectionResetError, ConnectionForced):
                log.error("Connection interrupt error")
                re_conn = None
                while True:
                    try:
                        log.debug("try to reconnect openstack mq")
                        re_conn = self.ternya.init_mq()
                        log.debug("reconnect successfully")
                        break
                    except MQConnectionError:
                        log.error("connect failed, ternya will try it after 10 seconds")
                        time.sleep(10)
                self.connection = re_conn


def enable_component_notification(config, openstack_component):
    """
    Check if customer enable openstack component notification.

    :param config: customer config information.
    :param openstack_component: Openstack component type.
    """
    if openstack_component == Openstack.Nova:
        return True if config.listen_nova_notification else False
    elif openstack_component == Openstack.Cinder:
        return True if config.listen_cinder_notification else False
    elif openstack_component == Openstack.Neutron:
        return True if config.listen_neutron_notification else False
    elif openstack_component == Openstack.Glance:
        return True if config.listen_glance_notification else False
    elif openstack_component == Openstack.Swift:
        return True if config.listen_swift_notification else False
    elif openstack_component == Openstack.Keystone:
        return True if config.listen_keystone_notification else False
    elif openstack_component == Openstack.Heat:
        return True if config.listen_heat_notification else False
