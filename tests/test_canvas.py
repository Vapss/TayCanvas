import os
import sys
import requests
import random



import pytest

from src import canvas
from protos.canvas_pb2 import EntityCanvazResponse


def test_get_access_token(monkeypatch):
    class Resp:
        def json(self):
            return {"accessToken": "abc123"}
    monkeypatch.setattr(requests, "get", lambda url: Resp())
    token = canvas.get_access_token()
    assert token == "abc123"

def test_get_access_token_requests_exception(monkeypatch):
    def raise_exc(url):
        raise requests.exceptions.RequestException("Network error")
    monkeypatch.setattr(requests, "get", raise_exc)
    with pytest.raises(Exception):
        canvas.get_access_token()

def test_get_access_token_no_json(monkeypatch):
    class Resp:
        pass
    monkeypatch.setattr(requests, "get", lambda url: Resp())
    with pytest.raises(Exception):
        canvas.get_access_token()

def test_get_access_token_invalid_json(monkeypatch):
    class Resp:
        def json(self):
            raise ValueError("Invalid JSON")
    monkeypatch.setattr(requests, "get", lambda url: Resp())
    with pytest.raises(Exception):
        canvas.get_access_token()

def test_get_access_token_missing_key(monkeypatch):
    class Resp:
        def json(self):
            return {"notAccessToken": "nope"}
    monkeypatch.setattr(requests, "get", lambda url: Resp())
    with pytest.raises(Exception):
        canvas.get_access_token()


def test_get_canvas_for_track(monkeypatch):
    response = EntityCanvazResponse()
    c1 = response.canvases.add()
    c1.url = "http://c1"
    c2 = response.canvases.add()
    c2.url = "http://c2"
    serialized = response.SerializeToString()

    class Resp:
        def __init__(self, content):
            self.content = content
    
    def fake_post(url, headers=None, data=None):
        return Resp(serialized)

    monkeypatch.setattr(requests, "post", fake_post)
    monkeypatch.setattr(random, "choice", lambda seq: seq[1] if len(seq) > 1 else ValueError("Sequence must contain at least two elements"))

    url = canvas.get_canvas_for_track("token", "trackid")
    assert url == "http://c2"


def test_get_canvas_for_track_request_failure(monkeypatch):
    def raise_post(*args, **kwargs):
        raise requests.exceptions.RequestException("boom")

    monkeypatch.setattr(requests, "post", raise_post)

    with pytest.raises(ConnectionError):
        canvas.get_canvas_for_track("token", "trackid")


def test_get_canvas_for_track_no_canvases(monkeypatch):
    response = EntityCanvazResponse()
    serialized = response.SerializeToString()

    class Resp:
        def __init__(self, content):
            self.content = content

    monkeypatch.setattr(requests, "post", lambda *a, **k: Resp(serialized))

    with pytest.raises(AttributeError):
        canvas.get_canvas_for_track("token", "trackid")
