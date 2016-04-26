## Catalog

* [How to Configure file](#config)
* [Start ternya](#start)
* [Deal with notification](#notification)



<h2 id="config">How to Configure file</h2>

### There is a example config file:
[example config file](https://github.com/ndrlslz/ternya/blob/master/config.ini)

### Detail information

* **project_abspath** point the absolute path of your project root directory.

* **packages_scan** python packages where you put the method that deal with openstack notification.
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


