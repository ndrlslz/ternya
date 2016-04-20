"""
ternya.ternya
=============

This module do main work.
"""
import time
import logging
from amqp import ConnectionForced
from multiprocessing import Pool, Process

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

        >>> from ternya.ternya import Ternya
        >>>
        >>> if __name__ == "__main__":
        >>>     ternya = Ternya()
        >>>     ternya.read("config.ini")
        >>>     ternya.work()
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
        Second, init openstack mq connection.
        """
        self.init_modules()
        self.init_mq()

    def init_mq(self):
        """Init connection with openstack mq."""
        # pool = Pool(5)
        # pool.apply_async(self.init_nova_mq)
        # pool.close()
        # process = Process(target=self.init_nova_mq)
        # process.start()
        self.init_nova_mq()
        # self.init_cinder_mq()

    def init_modules(self):
        """Import customer's service modules."""
        if not self.config:
            raise ValueError("please read your config file.")

        log.debug("begin to import customer's service modules.")
        modules = ServiceModules(self.config)
        modules.import_modules()
        log.debug("end to import customer's service modules.")

    def init_nova_mq(self):
        """
        Init openstack nova mq

        1. Check if enable listening nova notification
        2. Create mq connection
        3. Create consumer
        4. keep a auto-reconnect connection
        """
        if not enable_component_notification(self.config, Openstack.Nova):
            log.debug("disable listening nova notification")
            return

        log.debug("enable listening openstack nova notification.")
        nova_mq = MQ(self.config.nova_mq_user,
                     self.config.nova_mq_password,
                     self.config.nova_mq_host,
                     self.config.nova_mq_exchange,
                     self.config.nova_mq_queue,
                     ProcessFactory.process(Openstack.Nova))

        nova_conn = nova_mq.create_connection()
        for i in range(self.config.nova_mq_consumer_count):
            nova_mq.create_consumer(nova_conn)

        TernyaConnection(self, nova_conn, Openstack.Nova).connect()

    def init_cinder_mq(self):
        """
        Init openstack cinder mq

        1. Check if enable listening nova notification
        2. Create mq connection
        3. Create consumer
        4. keep a auto-reconnect connection
        """
        if not enable_component_notification(self.config, Openstack.Cinder):
            log.debug("disable listening cinder notification")
            return

        log.debug("enable listening openstack cinder notification.")
        cinder_mq = MQ(self.config.cinder_mq_user,
                       self.config.cinder_mq_password,
                       self.config.cinder_mq_host,
                       self.config.cinder_mq_exchange,
                       self.config.cinder_mq_queue,
                       ProcessFactory.process(Openstack.Cinder))

        cinder_conn = cinder_mq.create_connection()
        for i in range(self.config.cinder_mq_consumer_count):
            cinder_mq.create_consumer(cinder_conn)

        TernyaConnection(self, cinder_conn, Openstack.Cinder).connect()


class TernyaConnection:
    """
    This class keep the connection with openstack mq.

    If connection interrupt, try to reconnect openstack mq
    """

    def __init__(self, ternya, connection, openstack_component):
        self.connection = connection
        self.ternya = ternya
        self.component = openstack_component
        self.method_mapping = {
            Openstack.Nova: self.ternya.init_nova_mq,
        }

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
                        re_conn = self.method_mapping[self.component]()
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
        return True if config.nova_mq_host else False
    elif openstack_component == Openstack.Cinder:
        return True if config.cinder_mq_host else False
