from requests_connection import Session, Connection


def test_session():
    conn = Connection.https('ya.ru')
    sess = Session(conn)
    resp = sess.get('https://ya.ru/')
    assert resp.text.startswith('<!DOCTYPE html>')
    assert False


def test_reuse():
    conn = Connection.https('ya.ru')
    sess = Session(conn)

    resp = sess.get('https://ya.ru/')
    assert resp.text.startswith('<!DOCTYPE html>')

    resp2 = sess.get('https://ya.ru/news/')
    assert resp2.text.startswith('<!DOCTYPE html>')

    assert resp2.text[40:100] != resp.text[40:100]


def test_bypass():
    conn = Connection.https('ya.ru')
    sess = Session(conn)

    resp = sess.get('https://google.com/')
    assert resp.text.startswith('<!doctype html>')
