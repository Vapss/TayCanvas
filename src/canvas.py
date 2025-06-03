import base64
import os
import requests
import random
from .constants import TOKEN_ENDPOINT, TRACK_URI_PREFIX, API_HOST, CANVAS_ROUTE
from .protos.canvas_pb2 import EntityCanvazRequest, EntityCanvazResponse

def get_access_token():  # sourcery skip: raise-specific-error
    """Retrieve a Spotify access token using the Client Credentials flow."""

    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise EnvironmentError("Missing Spotify client credentials")

    credentials = f"{client_id}:{client_secret}".encode()
    encoded_credentials = base64.b64encode(credentials).decode()

    try:
        response = requests.post(
            TOKEN_ENDPOINT,
            headers={"Authorization": f"Basic {encoded_credentials}"},
            data={"grant_type": "client_credentials"},
        )
        response.raise_for_status()
        data = response.json()
        return data["access_token"], data["expires_in"]
    except Exception as e:
        raise Exception(e) from e


def get_canvas_for_track(access_token, track_id):
    canvas_request = EntityCanvazRequest()
    canvas_request_entities = canvas_request.entities.add()
    canvas_request_entities.entity_uri = TRACK_URI_PREFIX + track_id

    try:
        resp = requests.post(
            API_HOST + CANVAS_ROUTE,
            headers={
                "Content-Type": "application/x-protobuf",
                "Authorization": f"Bearer {access_token}",
            },
            data=canvas_request.SerializeToString(),
        )
    except:
        raise ConnectionError

    canvas_response = EntityCanvazResponse()
    canvas_response.ParseFromString(resp.content)

    if(len(canvas_response.canvases) == 0):
        raise AttributeError

    canvas = random.choice(canvas_response.canvases)
    return canvas.url
