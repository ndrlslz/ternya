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

    TODO
    Need doc here.
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
        pass

    def init_mq(self):
        """Init connection with openstack mq."""
        self.init_nova_mq()

    def init_modules(self):
        """Import customer's service modules."""
        if not self.config:
            raise ValueError("please read your config file.")

        modules = ServiceModules(self.config)
        modules.import_modules()

    def init_nova_mq(self):
        if not enable_component_notification(self.config, Openstack.Nova):
            log.debug("disable listening nova notification")
            return
        log.debug("enable listening nova notification")
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
