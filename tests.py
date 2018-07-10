from requests_connection import Session, Connection


def test_session():
    conn = Connection.https('ya.ru')
    sess = Session(conn)
    resp = sess.get('https://ya.ru/')
    assert resp.text.startswith('<!DOCTYPE html>')


def test_reuse():
    conn = Connection.https('ya.ru')
    sess = Session(conn)

    resp = sess.get('https://ya.ru/')
    assert resp.text.startswith('<!DOCTYPE html>')

    resp = sess.get('https://ya.ru/news/')
    assert resp.text.startswith('<!DOCTYPE html>')
