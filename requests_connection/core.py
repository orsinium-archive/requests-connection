import logging
from requests import Session as _Session
from requests.adapters import HTTPAdapter as _HTTPAdapter
from requests.exceptions import ConnectionError

from .pool import PoolManager

logger = logging.getLogger('requests_connection')


class HTTPAdapter(_HTTPAdapter):
    connection = None

    def mount(self, connection):
        if connection is None:
            logger.warning("mounted empty connection")
        else:
            logger.debug("mount connection")
        self.connection = connection
        self.init_poolmanager(
            self._pool_connections,
            self._pool_maxsize,
            block=self._pool_block,
        )
        return self

    def init_poolmanager(self, *args, **kwargs):
        if self.connection is not None:
            logger.debug("get pool manager")
            self.poolmanager = PoolManager(self.connection, *args, **kwargs)
        else:
            logger.info("connection not mounted")
            super(HTTPAdapter, self).init_poolmanager(*args, **kwargs)


class Session(_Session):
    def __init__(self, connection=None):
        super(Session, self).__init__()
        self.connect(connection)

    def connect(self, connection):
        logger.debug("mount connection to session")
        self.connection = connection
        self.mount('https://', HTTPAdapter().mount(connection))
        self.mount('http://', HTTPAdapter().mount(connection))
        return self

    def send(self, *args, **kwargs):
        logger.debug("make request")
        try:
            return super(Session, self).send(*args, **kwargs)
        except ConnectionError:
            logger.warning("connection failed")

        # try to reconnect and repeat request
        self.connect(self.connection)
        return super(Session, self).send(*args, **kwargs)
