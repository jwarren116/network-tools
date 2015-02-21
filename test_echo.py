from echo_client import client


def test_unicode():
    assert client(u'This is a unicode test'.encode('utf-8')) == \
        u'This is a unicode test'.decode('utf-8')


def test_long():
    assert client('This string is larger than my current buffer size') == \
                 ('This string is larger than my current buffer size')


def test_exact():
    assert client('This string is equal to mybuffer') == \
                 ('This string is equal to mybuffer')


def test_empty():
    assert client('') == ''
