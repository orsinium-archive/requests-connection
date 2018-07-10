from requests.packages import urllib3


class ConnectionPoolMixin(object):
    def __init__(self, *args, connection, **kwargs):
        self.connection = connection
        super(ConnectionPoolMixin, self).__init__(*args, **kwargs)

    def _new_conn(self):
        self.num_connections += 1
        return self.connection


class HTTPConnectionPool(ConnectionPoolMixin, urllib3.HTTPConnectionPool):
    pass


class HTTPSConnectionPool(ConnectionPoolMixin, urllib3.HTTPConnectionPool):
    pass


class PoolManager(urllib3.PoolManager):
    def __init__(self, host, port, **kwargs):
        self.host = host
        self.port = port
        super(PoolManager, self).__init__(**kwargs)

    def _new_pool(self, scheme, host, port):
        # Important!
        if host == self.host and port == self.port:
            if scheme == 'http':
                return HTTPConnectionPool(host, port, **self.connection_pool_kw)
            if scheme == 'https':
                return HTTPSConnectionPool(host, port, **self.connection_pool_kw)
        return super(PoolManager, self)._new_pool(self, scheme, host, port)
