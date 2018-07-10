# requests-connection


## Usage

### Make requests

```python
from requests_connection import Session, Connection

# connect (establish TCP and TLS connections)
connection = Connection.https('ya.ru')

# make requests session
session = Session(connection)

# make http request
response = session.get('https://ya.ru/')
```

You can make only one request via one connection. Reconnect before new request:

```python
connection = Connection.https('ya.ru')
session.connect(connection)
response = session.get('https://ya.ru/')
```

If connection has been closed, new connection will be created on request automatically:

```python
response = session.get('https://ya.ru/')
response = session.get('https://ya.ru/news/')
```

Requests to other host or port bypass created connection:

```python
response = session.get('http://ya.ru/')
response = session.get('https://google.com/')
```

### Make connection

`Connection` class help you to create connection. It supports 3 constructors:

* `Connection.http` -- returns [http.client.HTTPConnection](https://docs.python.org/3/library/http.client.html#http.client.HTTPConnection).
* `Connection.https` -- returns [http.client.HTTPSConnection](https://docs.python.org/3/library/http.client.html#http.client.HTTPSConnection)
* `Connection.socket` -- also returns [http.client.HTTPConnection](https://docs.python.org/3/library/http.client.html#http.client.HTTPConnection), but you can setup socket params.
