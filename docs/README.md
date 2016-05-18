## Catalog

* [How to Configure file](#config)
* [How to Start ternya](#start_ternya)
* [How to deal with notification](#notification)



<h2 id="config">How to Configure file</h2>

### There is an example config file:
[example config file](https://github.com/ndrlslz/ternya/blob/master/config.ini)

### Detail information

* **project_abspath:** point the absolute path of your project root directory

* **packages_scan:** python packages where you put the method that deal with openstack notification.

  ternya will scan all python files under the package you point. multiple package can join with ';'

  so where is your process method, then set packages_scan to that.
for example. assume your project struct like below:
  ```
  E:\ternya
  |-- my_process_one.py
  `-- process
     |-- my_process_two.py
     `-- sub_process
         |-- my_process_three.py
  `-- process1
     |-- my_process_four.py
  ```
  1. packages_scan =

   in this way, ternya will scan all python files under project root directory. this is not recommended
  2. packages_scan = process

   in this way, ternya will scan my_process_two.py and my_process_threee.py
  3. packages_scan = process.sub_process

   in this way, ternya will scan my_process_three.py
  4. packages_scan = process.sub_process;process1

   in this way, ternya will scan my_process_three.py and my_process_four.py

  you need to set this to include all your process method that deal with openstack notification
but scan less packages is better.

* **mq_use:r** openstack mq server username

* **mq_password:** openstack mq server password

* **mq_host:** openstack mq server host

* **listen_notification:** whether to receive notification for each openstack component

* **mq_consumer_count:** how much consumer to connect one queue.

  if count >=2 queue will use round-roubin policy to send message to consumers.


<h2 id="start_ternya">How to start ternya</h2>

1. Firstly, load your config file by invoking read(path)
2. start ternya by invoking work()

you should start a process to start ternya like below:

```python
from ternya import Ternya
from multiprocessing import Process

if __name__ == "__main__":
    ternya = Ternya()
    ternya.read("config.ini")
    process = Process(target=ternya.work)
    process.start()
 ```

 if you use windows os, 'if __name__ == "__main__":' is necessary.


<h2 id="notification">How to deal with notification</h2>

Ternya provide annotation to deal with openstack notification.

So you can easily deal with notification using ternya annotation like this:

for example about dealing with nova notification
```
from ternya import nova

@nova("compute.instance.create.start")
def create_instance_start(body, message):
    """
    Service method of dealing with notification.
    body and message parameter is necessary.

    :param body: notification dict
    :param message: kombu Message class
    """
    print("start to create instance notification.")
    print(body['event_type'])
    print(body)
```

According to annotation, ternya add mapper between event_type and service function.
In this example, tenrya use create_instance_start function to deal with "compute.instance.create.start" event_type.

About writing your service function, parameter body and message is necessary.

**body:** dict of notification.

**message**: kombu Message class. (subclass of kombu.transport.base.Message)

---

And also ternya annotation support wildcard:

```
from ternya import nova

@nova("compute.instance.delete.*"):
def instance_delete(body, message):
	print("delete instance notification")
	print(body['event_type'])
	print(body)
```

In this example, instance_delete function can handle two event_type: "compute.instance.delete.start" and "compute.instance.delete.end".


for now, ternya support seven type annotation:

>* nova
>* cinder
>* neutron
>* glance
>* swift
>* keystone
>* heat




