from echo_client import client


def test_1():
    assert client('This is a unicode test') == 'This is a unicode test'


def test_2():
    assert client('This string is larger than my current buffer size. It should return all of the characters. This is the last sentence of this test.') == 'This string is larger than my current buffer size. It should return all of the characters. This is the last sentence of this test.'


def test_3():
    assert client('') == ''
