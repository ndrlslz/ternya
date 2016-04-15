"""
ternya.openstack
================

This module define the enum which include openstack component
"""
from enum import Enum


class Openstack(Enum):
    Nova = "nova"
    Cinder = "cinder"
    Neutron = "neutron"
    Glance = "glance"
    Swift = "swift"
