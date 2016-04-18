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
    def __init__(self):
        self.config = None

    def read(self, path):
        self.config = Config(path)

    def work(self):
        pass

    def init_mq(self):
        self.init_nova_mq()

    def init_modules(self):
        if not self.config:
            raise ValueError("please read your config file.")

        modules = ServiceModules(self.config)
        modules.import_modules()

    def init_nova_mq(self):
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
