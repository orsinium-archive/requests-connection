from requests_connection import Session, Connection
from requests.adapters import HTTPAdapter


def test_session():
    conn = Connection.https('ya.ru')
    assert conn.host == 'ya.ru'
    assert conn.port == 443

    sess = Session(conn)
    resp = sess.get('https://ya.ru/')
    assert resp.text.startswith('<!DOCTYPE html>')


def test_reuse():
    conn = Connection.https('ya.ru')
    sess = Session(conn)

    resp = sess.get('https://ya.ru/')
    assert resp.text.startswith('<!DOCTYPE html>')

    resp2 = sess.get('https://ya.ru/news/')
    assert resp2.text.startswith('<!DOCTYPE html>')

    assert resp2.text[40:100] != resp.text[40:100]


def test_restore():
    conn = Connection.https('ya.ru')
    sess = Session(conn)

    resp = sess.get('https://ya.ru/')
    assert resp.text.startswith('<!DOCTYPE html>')

    sess.mount('https://', HTTPAdapter())
    sess.mount('http://', HTTPAdapter())

    resp2 = sess.get('https://ya.ru/news/')
    assert resp2.text.startswith('<!DOCTYPE html>')

    assert resp2.text[40:100] != resp.text[40:100]


def test_bypass():
    conn = Connection.https('ya.ru')
    sess = Session(conn)

    resp = sess.get('https://google.com/')
    assert resp.text.startswith('<!doctype html>')
