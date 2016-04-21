from ternya.config import Config
from ternya.modules import ServiceModules
# #
# # #Config
# # # config = Config("config.ini")
# # # print(config.nova_mq_user, " ", type(config.nova_mq_user))
# #
# #
# # #Modules
# # import os
# modules = ServiceModules(Config("config.ini"))
# # # print(modules.import_modules())
# modules.import_modules()
# # # string = "test.test"
# # # string1 = "E:\\python"
# # # print(os.path.join(string1, string.replace(".", os.path.sep)))
# # # list1 = []
# # # print(os.path.normcase(string1))
# from ternya.process import ProcessFactory
# from ternya.openstack import Openstack
#
# process = ProcessFactory().process(Openstack.Nova)
# process({"event_type": "123"}, "")

# from ternya import Config, MQ
# from ternya.process import nova_process
# from kombu import Connection, Exchange, Queue, Consumer
#
#
# config = Config("config.ini")
# mq = MQ(config.nova_mq_user, config.nova_mq_password, config.nova_mq_host, config.nova_mq_exchange,
#         config.nova_mq_queue, nova_process, consumer_count=1)
# conn = mq.create_connection()
# conn = mq.create_consumer(conn)
# assert isinstance(conn, Connection)
# while True:
#     conn.drain_events()

from ternya.ternya import Ternya
from multiprocessing import Process, freeze_support

#

if __name__ == "__main__":
    freeze_support()
    ternya = Ternya()
    ternya.read("config.ini")
    ternya.work()
    # process = Process(target=ternya.work)
    # process.start()

# from ternya.annotation import nova
#
#
# @nova("compute.metrics.test")
# def test():
#     print("this is not wildcard process")
#
# test()
