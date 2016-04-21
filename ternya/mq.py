"""
ternya.mq
=========

This module define the connection to openstack mq.
"""
from kombu import Connection, Exchange, Queue, Consumer
import logging

from ternya import MQConnectionError

log = logging.getLogger(__name__)


class MQ:
    """
    This class connect to openstack mq to get notifications.

    :keyword mq_user: openstack mq's username.
    :keyword mq_password: openstack mq's password.
    :keyword mq_host: openstack mq's host ip.
    """

    def __init__(self, mq_user, mq_password, mq_host):
        self.mq_user = mq_user
        self.mq_password = mq_password
        self.mq_host = mq_host
        self.connection = None

    def __repr__(self):
        return "user={0},password={1},host={2}".format(
                self.mq_user, self.mq_password, self.mq_host)

    __str__ = __repr__

    def create_connection(self):
        host = "amqp://{0}:{1}@{2}//".format(self.mq_user, self.mq_password, self.mq_host)
        log.info("create connection: " + host)
        self.connection = Connection(host)
        return self.connection

    def create_consumer(self, exchange_name, queue_name, process):
        try:
            channel = self.connection.channel()
            exchange = Exchange(exchange_name, type="topic")
            queue = Queue(queue_name, exchange, routing_key="notifications.#")
            consumer = Consumer(channel, queue)
            consumer.register_callback(process)
            consumer.consume()
            log.info("create consumer: " + repr(consumer))
        except OSError:
            raise MQConnectionError("please check your mq user, password and host configuration.")

        return self.connection
