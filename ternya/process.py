"""
ternya.process
==============

This module define the process to deal with openstack notification.
"""
import logging

from ternya.annotation import nova_customer_process
from ternya import Openstack

log = logging.getLogger(__name__)


class ProcessFactory:
    @staticmethod
    def process(openstack_component):
        if openstack_component == Openstack.Nova:
            return nova_process


def nova_process(body, message):
    event_type = body['event_type']
    process = nova_customer_process.get(event_type)
    if process is not None:
        process(body, message)
    else:
        default_process(body, message)


def default_process(body, message):
    event_type = body['event_type']
    log.debug("event_type:" + event_type)
    log.debug(body)
    message.ack()
