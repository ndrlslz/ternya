import logging

log = logging.getLogger(__name__)


class Error(Exception):
    def __init__(self, msg):
        self.message = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.message

    __str__ = __repr__


class ConfigError(Error):
    def __init__(self, msg):
        message = ["config file error.", msg]
        Error.__init__(self, " ".join(message))
