"""
ternya.process
==============

This module define the process to deal with openstack notification.
"""
import logging

from ternya.annotation import (nova_customer_process, nova_customer_process_wildcard,
                               cinder_customer_process, cinder_customer_process_wildcard)
from ternya import Openstack

log = logging.getLogger(__name__)


class ProcessFactory:
    @staticmethod
    def process(openstack_component):
        if openstack_component == Openstack.Nova:
            return nova_process
        elif openstack_component == Openstack.Cinder:
            return cinder_process


def nova_process(body, message):
    """
    This function deal with the nova notification.

    First, find process from customer_process that not include wildcard.
    if not find from customer_process, then find process from customer_process_wildcard.
    if not find from customer_process_wildcard, then use ternya default process.
    :param body: dict of openstack notification.
    :param message: kombu Message class
    :return:
    """
    event_type = body['event_type']
    process = nova_customer_process.get(event_type)
    if process is not None:
        process(body, message)
    else:
        matched = False
        process_wildcard = None
        for pattern in nova_customer_process_wildcard.keys():
            if pattern.match(event_type):
                process_wildcard = nova_customer_process_wildcard.get(pattern)
                matched = True
                break
        if matched:
            process_wildcard(body, message)
        else:
            default_process(body, message)
    message.ack()


def cinder_process(body, message):
    """
    This function deal with the cinder notification.

    First, find process from customer_process that not include wildcard.
    if not find from customer_process, then find process from customer_process_wildcard.
    if not find from customer_process_wildcard, then use ternya default process.
    :param body: dict of openstack notification.
    :param message: kombu Message class
    :return:
    """
    event_type = body['event_type']
    process = cinder_customer_process.get(event_type)
    if process is not None:
        process(body, message)
    else:
        matched = False
        process_wildcard = None
        for pattern in cinder_customer_process_wildcard:
            if pattern.match(event_type):
                process_wildcard = cinder_customer_process_wildcard.get(pattern)
                matched = True
                break
        if matched:
            process_wildcard(body, message)
        else:
            default_process(body, message)
    message.ack()


def default_process(body, message):
    event_type = body['event_type']
    log.debug("event_type:" + event_type)
    log.debug(body)
