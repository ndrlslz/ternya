# ternya - Openstack notification library for Python
---
| Version    | 0.1.2  |
| --------   | -----  |
| Blog       |        |
| Download   | https://pypi.python.org/pypi/ternya   |
| Source     | https://github.com/ndrlslz/ternya     |
| Keywords   | openstack, notification, python, amqp |

## About
---
ternya is a openstack notification library for python.
The aim of ternya is to receive openstack notification and deal with notification easily.


## Requirements
---
* python 3
* works on Linux, Windows. (not tested on Mac OS)

## Quick overview
---
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
---
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

## Documentation
---

## Chinese Version
---

