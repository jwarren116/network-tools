from echo_client import client
from http2_server import (
    parse_request, resolve_uri, response_ok, response_error, RequestError
)
import pytest


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
    assert first_line == 'HTTP/1.1 404 Page Not Found'


def test_parse_request():
    assert parse_request('GET sample.txt HTTP/1.1') == 'sample.txt'


def test_parse_request_error():
    with pytest.raises(RequestError):
        parse_request('POST somethingevil HTTP/1.1')


def test_resolve_uri_file_error():
    with pytest.raises(RequestError):
        resolve_uri('imnotreal.txt')


def test_resolve_uri_dir():
    dir_body = resolve_uri('/')
    assert '<!DOCTYPE html><html><body><ul>' in dir_body[1]
    assert '<a href=' in dir_body[1]
    assert 'text/html' == dir_body[0]


def test_response_error():
    error = response_error(405, 'Method Not Allowed')
    assert 'HTTP/1.1 405 Method Not Allowed' in error


def test_response_ok():
    body = response_ok(('text/plain', 'This is plain text'))
    body = body.split('\r\n')
    assert body[0] == 'HTTP/1.1 200 OK'
    assert body[2] == 'Content-Type: text/plain'
    assert body[4] == 'This is plain text'
