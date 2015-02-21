from echo_client import client


def test_ok():
    response = client('GET /index.html HTTP/1.1').split('\r\n')
    first_line = response[0]
    assert first_line == 'HTTP/1.1 200 OK'


def test_405():
    response = client('POST /index.html HTTP/1.1').split('\r\n')
    first_line = response[0]
    assert first_line == 'HTTP/1.1 405 Method Not Allowed'


def test_505():
    response = client('GET /index.html HTTP/1.0').split('\r\n')
    first_line = response[0]
    assert first_line == 'HTTP/1.1 505 HTTP Version Not Supported'
