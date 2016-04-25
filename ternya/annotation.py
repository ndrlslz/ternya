"""
ternya.annotation
=================

This module define the annotation
"""
import functools
import types
import logging
import re

from ternya import AnnotationError
from ternya import Openstack

log = logging.getLogger(__name__)

# customer's nova process which not include wildcard.
nova_customer_process = {}
# customer's nova process which include wildcard.
nova_customer_process_wildcard = {}

# customer's cinder process which not include wildcard.
cinder_customer_process = {}
# customer's cinder process which include wildcard.
cinder_customer_process_wildcard = {}

# customer's neutron process which not include wildcard.
neutron_customer_process = {}
# customer's neutron process which include wildcard.
neutron_customer_process_wildcard = {}

# customer's glance process which not include wildcard.
glance_customer_process = {}
# customer's glance process which include wildcard.
glance_customer_process_wildcard = {}

# customer's swift process which not include wildcard.
swift_customer_process = {}
# customer's swift process which include wildcard.
swift_customer_process_wildcard = {}

# customer's keystone process which not include wildcard.
keystone_customer_process = {}
# customer's swift process which include wildcard.
keystone_customer_process_wildcard = {}

# customer's heat process which not include wildcard.
heat_customer_process = {}
# customer's heat process which include wildcard.
heat_customer_process_wildcard = {}


def nova(*arg):
    """
    Nova annotation for adding function to process nova notification.

    if event_type include wildcard, will put {pattern: function} into process_wildcard dict
    else will put {event_type: function} into process dict

    :param arg: event_type of notification
    """
    check_event_type(Openstack.Nova, *arg)
    event_type = arg[0]

    def decorator(func):
        if event_type.find("*") != -1:
            event_type_pattern = pre_compile(event_type)
            nova_customer_process_wildcard[event_type_pattern] = func
        else:
            nova_customer_process[event_type] = func
        log.info("add function {0} to process event_type:{1}".format(func.__name__, event_type))

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return decorator


def cinder(*arg):
    """
    Cinder annotation for adding function to process cinder notification.

    if event_type include wildcard, will put {pattern: function} into process_wildcard dict
    else will put {event_type: function} into process dict

    :param arg: event_type of notification
    """
    check_event_type(Openstack.Cinder, *arg)
    event_type = arg[0]

    def decorator(func):
        if event_type.find("*") != -1:
            event_type_pattern = pre_compile(event_type)
            cinder_customer_process_wildcard[event_type_pattern] = func
        else:
            cinder_customer_process[event_type] = func
        log.info("add function {0} to process event_type:{1}".format(func.__name__, event_type))

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return decorator


def neutron(*arg):
    """
    Neutron annotation for adding function to process neutron notification.

    if event_type include wildcard, will put {pattern: function} into process_wildcard dict
    else will put {event_type: function} into process dict

    :param arg: event_type of notification
    """
    check_event_type(Openstack.Neutron, *arg)
    event_type = arg[0]

    def decorator(func):
        if event_type.find("*") != -1:
            event_type_pattern = pre_compile(event_type)
            neutron_customer_process_wildcard[event_type_pattern] = func
        else:
            neutron_customer_process[event_type] = func
        log.info("add function {0} to process event_type:{1}".format(func.__name__, event_type))

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return decorator


def glance(*arg):
    """
    Glance annotation for adding function to process glance notification.

    if event_type include wildcard, will put {pattern: function} into process_wildcard dict
    else will put {event_type: function} into process dict

    :param arg: event_type of notification
    """
    check_event_type(Openstack.Glance, *arg)
    event_type = arg[0]

    def decorator(func):
        if event_type.find("*") != -1:
            event_type_pattern = pre_compile(event_type)
            glance_customer_process_wildcard[event_type_pattern] = func
        else:
            glance_customer_process[event_type] = func
        log.info("add function {0} to process event_type:{1}".format(func.__name__, event_type))

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return decorator


def swift(*arg):
    """
    Swift annotation for adding function to process swift notification.

    if event_type include wildcard, will put {pattern: function} into process_wildcard dict
    else will put {event_type: function} into process dict

    :param arg: event_type of notification
    """
    check_event_type(Openstack.Swift, *arg)
    event_type = arg[0]

    def decorator(func):
        if event_type.find("*") != -1:
            event_type_pattern = pre_compile(event_type)
            swift_customer_process_wildcard[event_type_pattern] = func
        else:
            swift_customer_process[event_type] = func
        log.info("add function {0} to process event_type:{1}".format(func.__name__, event_type))

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return decorator


def keystone(*arg):
    """
    Swift annotation for adding function to process keystone notification.

    if event_type include wildcard, will put {pattern: function} into process_wildcard dict
    else will put {event_type: function} into process dict

    :param arg: event_type of notification
    """
    check_event_type(Openstack.Keystone, *arg)
    event_type = arg[0]

    def decorator(func):
        if event_type.find("*") != -1:
            event_type_pattern = pre_compile(event_type)
            keystone_customer_process_wildcard[event_type_pattern] = func
        else:
            keystone_customer_process[event_type] = func
        log.info("add function {0} to process event_type:{1}".format(func.__name__, event_type))

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return decorator


def heat(*arg):
    """
    Heat annotation for adding function to process heat notification.

    if event_type include wildcard, will put {pattern: function} into process_wildcard dict
    else will put {event_type: function} into process dict

    :param arg: event_type of notification
    """
    check_event_type(Openstack.Heat, *arg)
    event_type = arg[0]

    def decorator(func):
        if event_type.find("*") != -1:
            event_type_pattern = pre_compile(event_type)
            heat_customer_process_wildcard[event_type_pattern] = func
        else:
            heat_customer_process[event_type] = func
        log.info("add function {0} to process event_type:{1}".format(func.__name__, event_type))

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return decorator


def check_event_type(openstack_component, *arg):
    if not arg:
        raise AnnotationError("parameter is required for {component} annotation."
                              .format(component=openstack_component.value))
    if isinstance(arg[0], types.FunctionType):
        raise AnnotationError("{component} annotation need to set event_type."
                              .format(component=openstack_component.value))


def pre_compile(event_type):
    event_type_str = event_type.replace(".", "\.").replace("*", "\w*?")
    event_type_pattern = re.compile(event_type_str)
    return event_type_pattern
