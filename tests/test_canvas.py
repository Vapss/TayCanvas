import os
import sys
import requests
import random

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import canvas
from protos.canvas_pb2 import EntityCanvazResponse


def test_get_access_token(monkeypatch):
    class Resp:
        def json(self):
            return {"accessToken": "abc123"}
    monkeypatch.setattr(requests, "get", lambda url: Resp())
    token = canvas.get_access_token()
    assert token == "abc123"


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
    monkeypatch.setattr(random, "choice", lambda seq: seq[1])

    url = canvas.get_canvas_for_track("token", "trackid")
    assert url == "http://c2"
