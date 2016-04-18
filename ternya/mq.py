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
    :keyword exchange_name: openstack exchange your queue need to binds.
    :keyword queue_name: openstack queue name you defined.
    :keyword process: process method to deal with notifications.
    :keyword consumer_count: (optional) defined consumer count to receive message from the same queue.
    """

    def __init__(self, mq_user, mq_password, mq_host, exchange_name, queue_name, process, consumer_count=1):
        self.mq_user = mq_user
        self.mq_password = mq_password
        self.mq_host = mq_host
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.process = process
        self.consumer_count = consumer_count

    def __repr__(self):
        return "user={0},password={1},host={2},exchange={3},queue={4},process={5}".format(
                self.mq_user, self.mq_password, self.mq_host, self.exchange_name, self.queue_name, self.process
        )

    __str__ = __repr__

    def create_connection(self):
        host = "amqp://{0}:{1}@{2}//".format(self.mq_user, self.mq_password, self.mq_host)
        log.info("create connection: " + host)
        return Connection(host)

    def create_consumer(self, connection):
        try:
            channel = connection.channel()
            exchange = Exchange(self.exchange_name, type="topic")
            queue = Queue(self.queue_name, exchange, routing_key="notifications.#")
            consumer = Consumer(channel, queue)
            consumer.register_callback(self.process)
            consumer.consume()
            log.info("create consumer: " + repr(consumer))
        except OSError:
            raise MQConnectionError("please check your mq user, password and host configuration.")

        return connection
