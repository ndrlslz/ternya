# ternya - Openstack notification library for Python

| Version    | 0.1.2  |
| --------   | -----  |
| Blog       |        |
| Download   | https://pypi.python.org/pypi/ternya   |
| Source     | https://github.com/ndrlslz/ternya     |
| Keywords   | openstack, notification, python, amqp |

## About

ternya is a openstack notification library for python.

The aim of ternya is to receive openstack notification and deal with notification easily.

## Feature

* Flexible to receive openstack notification, it controlled by config file.

* Inject service logic according to use annotation. and annotation support wildcard.

* The ability to auto reconnect openstack mq

## Requirements

* Python 3
* Works on Linux, Windows. (not tested on Mac OS)

## Quick overview

### start ternya

```python
from ternya import Ternya

if __name__ == "__main__":
     ternya = Ternya()
     ternya.read("config.ini")
     ternya.work()
```

### deal with notification
```python
from ternya import neutron

@neutron("network.create.start")
def test2(body, message):
    print("this is neutron process")
    print(body['event_type'])
    print(body)
```

## Installation

You can install Ternya either via the Python Package Index (PyPI) or from source.
To install using pip:
```
$ pip install ternya
```
To install using easy_install:
```
$ easy_install ternya
```
To install using source:
```
python setup.py install
```

## Detail Documentation

[detail doc](https://github.com/ndrlslz/ternya/tree/master/docs)

## Chinese Version

