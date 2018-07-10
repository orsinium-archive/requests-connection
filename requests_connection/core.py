from requests import Session as _Session
from requests.adapters import HTTPAdapter as _HTTPAdapter
from requests.exceptions import ConnectionError

from .pool import PoolManager


class HTTPAdapter(_HTTPAdapter):
    def mount(self, connection):
        self.connection = connection
        return self

    def init_poolmanager(self, *args, **kwargs):
        self.poolmanager = PoolManager(*args, **kwargs)


class Session(_Session):
    def __init__(self, connection=None):
        super(Session, self).__init__()
        self.connect(connection)

    def connect(self, connection):
        self.connection = connection
        self.mount('https://', HTTPAdapter().mount(connection))
        self.mount('http://', HTTPAdapter().mount(connection))

    def send(self, *args, **kwargs):
        try:
            return super(Session, self).send(*args, **kwargs)
        except ConnectionError:
            pass

        # try to reconnect and repeat request
        self.connect(self.connection)
        return super(Session, self).send(*args, **kwargs)
