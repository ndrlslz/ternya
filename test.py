from ternya.config import Config
from ternya.modules import ServiceModules
#
# #Config
# # config = Config("config.ini")
# # print(config.nova_mq_user, " ", type(config.nova_mq_user))
#
#
# #Modules
# import os
modules = ServiceModules(Config("config.ini"))
# # print(modules.import_modules())
modules.import_modules()
# # string = "test.test"
# # string1 = "E:\\python"
# # print(os.path.join(string1, string.replace(".", os.path.sep)))
# # list1 = []
# # print(os.path.normcase(string1))
from ternya.process import ProcessFactory
from ternya.openstack import Openstack

process = ProcessFactory().process(Openstack.Nova)
process({"event_type": "123"}, "")
