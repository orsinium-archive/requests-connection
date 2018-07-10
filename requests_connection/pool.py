import logging
from requests.packages import urllib3


logger = logging.getLogger('requests_connection')


class ConnectionPoolMixin(object):
    def __init__(self, *args, connection, **kwargs):
        self.connection = connection
        super(ConnectionPoolMixin, self).__init__(*args, **kwargs)

    def _new_conn(self):
        logger.debug('use existing connection for request')
        self.num_connections += 1
        return self.connection


class HTTPConnectionPool(ConnectionPoolMixin, urllib3.HTTPConnectionPool):
    pass


class HTTPSConnectionPool(ConnectionPoolMixin, urllib3.HTTPConnectionPool):
    pass


class PoolManager(urllib3.PoolManager):
    def __init__(self, connection, **kwargs):
        self.connection = connection
        super(PoolManager, self).__init__(**kwargs)

    def _new_pool(self, scheme, host, port, request_context=None):
        if host == self.connection.host and port == self.connection.port:
            if scheme == 'http':
                logger.debug('get http pool')
                return HTTPConnectionPool(host, port, connection=self.connection, **self.connection_pool_kw)
            if scheme == 'https':
                logger.debug('get https pool')
                return HTTPSConnectionPool(host, port, connection=self.connection, **self.connection_pool_kw)
            logger.warning('does not match scheme: {}'.format(scheme))

        if host != self.connection.host:
            logger.warning('does not match host: {} != {}'.format(host, self.connection.host))
        if port != self.connection.port:
            logger.warning('does not match port: {} != {}'.format(port, self.connection.port))
        return super(PoolManager, self)._new_pool(scheme, host, port, request_context=request_context)
