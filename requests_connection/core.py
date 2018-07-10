from requests import Session as _Session
from requests.adapters import HTTPAdapter as _HTTPAdapter

from .pool import PoolManager


class HTTPAdapter(_HTTPAdapter):
    def mount(self, connection, host, port):
        self.connection = connection
        self.host = host
        self.port = port
        return self

    def init_poolmanager(self, connections, maxsize):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
        )


class Session(_Session):
    def __init__(self, connection=None):
        self.connection = connection
        super(Session, self).__init__()
        self.connect(connection)

    def connect(self, connection):
        self.mount('https://', HTTPAdapter().mount(connection))
        self.mount('http://', HTTPAdapter().mount(connection))
