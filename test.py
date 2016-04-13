from ternya.config import Config


config = Config()
config.read("config.ini")
print(config.nova_mq_user)
