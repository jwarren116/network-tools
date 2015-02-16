from echo_client import client


def test_ok():
    response = client('GET a_web_page.html HTTP/1.1').split('\r\n')
    first_line = response[0]
    assert first_line == 'HTTP/1.1 200 OK'


def test_body():
    response = client('GET sample.txt HTTP/1.1').split('\r\n')
    body = response[4]
    assert 'This is a very simple text file.' in body


def test_directory():
    response = client('GET / HTTP/1.1').split('\r\n')
    body = response[4]
    assert "<a href='make_time.py'>make_time.py</a>" in body


def test_404():
    response = client('GET does/not/exist.html HTTP/1.1').split('\r\n')
    first_line = response[0]
    assert first_line == 'HTTP/1.1 404 Not Found'
