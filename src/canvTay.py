import datetime
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .database import insert_canvas


def credenciales():
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    artist_uri = 'spotify:artist:06HL4z0CvFAxyc27GXpf02'
    results = spotify.artist_albums(artist_uri, album_type='album')

    albums = results['items']
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])

    album_ids = [album['id'] for album in albums]

    for album_id in album_ids:
        album = spotify.album(album_id)
        for track in album['tracks']['items']:
            track_id = track['id']
            song_name = track['name']
            album_name = album['name']
            response = requests.get(f'http://localhost:8000/api/canvas/{track_id}').json()
            if response.get('success') == 'true':
                canvas_url = response.get('canvas_url')
                insert_canvas(
                    track_id=track_id,
                    song_name=song_name,
                    album_name=album_name,
                    canvas_url=canvas_url,
                    retrieved_at=datetime.datetime.now(
                        datetime.timezone.utc
                    ).isoformat(),
                )
