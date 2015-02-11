from echo_client import client


def test_1():
    assert client('This is a unicode test') == 'This is a unicode test'


def test_2():
    assert client(u'This is an é unicode test') == u'This is an é unicode test'
