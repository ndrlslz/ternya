"""
ternya.process
==============

This module define the process to deal with openstack notification.
"""
import logging

from ternya.annotation import (nova_customer_process, nova_customer_process_wildcard,
                               cinder_customer_process, cinder_customer_process_wildcard,
                               neutron_customer_process, neutron_customer_process_wildcard,
                               glance_customer_process, glance_customer_process_wildcard,
                               swift_customer_process, swift_customer_process_wildcard,
                               keystone_customer_process, keystone_customer_process_wildcard,
                               heat_customer_process, heat_customer_process_wildcard)
from ternya import Openstack

log = logging.getLogger(__name__)


class ProcessFactory:
    @staticmethod
    def process(openstack_component):
        return process_mapping[openstack_component]


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
        for pattern in cinder_customer_process_wildcard.keys():
            if pattern.match(event_type):
                process_wildcard = cinder_customer_process_wildcard.get(pattern)
                matched = True
                break
        if matched:
            process_wildcard(body, message)
        else:
            default_process(body, message)
    message.ack()


def neutron_process(body, message):
    """
    This function deal with the neutron notification.

    First, find process from customer_process that not include wildcard.
    if not find from customer_process, then find process from customer_process_wildcard.
    if not find from customer_process_wildcard, then use ternya default process.
    :param body: dict of openstack notification.
    :param message: kombu Message class
    :return:
    """
    event_type = body['event_type']
    process = neutron_customer_process.get(event_type)
    if process is not None:
        process(body, message)
    else:
        matched = False
        process_wildcard = None
        for pattern in neutron_customer_process_wildcard.keys():
            if pattern.match(event_type):
                process_wildcard = neutron_customer_process_wildcard.get(pattern)
                matched = True
                break
        if matched:
            process_wildcard(body, message)
        else:
            default_process(body, message)
    message.ack()


def glance_process(body, message):
    """
    This function deal with the glance notification.

    First, find process from customer_process that not include wildcard.
    if not find from customer_process, then find process from customer_process_wildcard.
    if not find from customer_process_wildcard, then use ternya default process.
    :param body: dict of openstack notification.
    :param message: kombu Message class
    :return:
    """
    event_type = body['event_type']
    process = glance_customer_process.get(event_type)
    if process is not None:
        process(body, message)
    else:
        matched = False
        process_wildcard = None
        for pattern in glance_customer_process_wildcard.keys():
            if pattern.match(event_type):
                process_wildcard = glance_customer_process_wildcard.get(pattern)
                matched = True
                break
        if matched:
            process_wildcard(body, message)
        else:
            default_process(body, message)
    message.ack()


def swift_process(body, message):
    """
    This function deal with the swift notification.

    First, find process from customer_process that not include wildcard.
    if not find from customer_process, then find process from customer_process_wildcard.
    if not find from customer_process_wildcard, then use ternya default process.
    :param body: dict of openstack notification.
    :param message: kombu Message class
    :return:
    """
    event_type = body['event_type']
    process = swift_customer_process.get(event_type)
    if process is not None:
        process(body, message)
    else:
        matched = False
        process_wildcard = None
        for pattern in swift_customer_process_wildcard.keys():
            if pattern.match(event_type):
                process_wildcard = swift_customer_process_wildcard.get(pattern)
                matched = True
                break
        if matched:
            process_wildcard(body, message)
        else:
            default_process(body, message)
    message.ack()


def keystone_process(body, message):
    """
    This function deal with the keystone notification.

    First, find process from customer_process that not include wildcard.
    if not find from customer_process, then find process from customer_process_wildcard.
    if not find from customer_process_wildcard, then use ternya default process.
    :param body: dict of openstack notification.
    :param message: kombu Message class
    :return:
    """
    event_type = body['event_type']
    process = keystone_customer_process.get(event_type)
    if process is not None:
        process(body, message)
    else:
        matched = False
        process_wildcard = None
        for pattern in keystone_customer_process_wildcard.keys():
            if pattern.match(event_type):
                process_wildcard = keystone_customer_process_wildcard.get(pattern)
                matched = True
                break
        if matched:
            process_wildcard(body, message)
        else:
            default_process(body, message)
    message.ack()


def heat_process(body, message):
    """
    This function deal with the heat notification.

    First, find process from customer_process that not include wildcard.
    if not find from customer_process, then find process from customer_process_wildcard.
    if not find from customer_process_wildcard, then use ternya default process.
    :param body: dict of openstack notification.
    :param message: kombu Message class
    :return:
    """
    event_type = body['event_type']
    process = heat_customer_process.get(event_type)
    if process is not None:
        process(body, message)
    else:
        matched = False
        process_wildcard = None
        for pattern in heat_customer_process_wildcard.keys():
            if pattern.match(event_type):
                process_wildcard = heat_customer_process_wildcard.get(pattern)
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


process_mapping = {
    Openstack.Nova: nova_process,
    Openstack.Cinder: cinder_process,
    Openstack.Neutron: neutron_process,
    Openstack.Glance: glance_process,
    Openstack.Swift: swift_process,
    Openstack.Keystone: keystone_process,
    Openstack.Heat: heat_process,
}

# define default method to deal with event_type that appear a lot of times.
# customer can override it if need.
nova_customer_process['compute.metrics.update'] = default_process
nova_customer_process['compute.instance.exists'] = default_process
