# Obtener lista de todas las canciones de Taylor swift con el API de Spotify

# Importamos librerias
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import requests

def credenciales():
    from spotipy.oauth2 import SpotifyClientCredentials
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    artist_uri = 'spotify:artist:06HL4z0CvFAxyc27GXpf02'
    artist = spotify.artist(artist_uri)
    results = spotify.artist_albums(artist_uri, album_type='album')

    albums = results['items']
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])

    album_ids = []
    for album in albums:
        print(album['id'])
        album_ids.append(album['id'])

    # Obtener todas las canciones de cada album con columna nombre y album y url y track_id
    songs = []

    for album_id in album_ids:
        album = spotify.album(album_id)
        for track in album['tracks']['items']:
            songs.append([track['name'], album['name'], track['external_urls']['spotify'], track['id']])

    # Convertir a dataframe
    songs_df = pd.DataFrame(songs, columns=['song_name', 'album_name', 'url', 'track_id'])

    # Obtener canvas de cada cancion desde http://localhost:8000/api/canvas/{track_id}. Agregar el nombre de la cancion a la respuesta desde songs_df y agregar a un array

    canvas = []

    for track_id in songs_df['track_id']:
        
        # Obtener canvas
        url = 'http://localhost:8000/api/canvas/' + track_id
        response = requests.get(url)
        response = response.json()
        
        # Agregar nombre de la cancion
        song_name = songs_df[songs_df['track_id'] == track_id]['song_name'].values[0]
        response['song_name'] = song_name
        
        # Agregar a array
        canvas.append(response)
        
        # Crear dataframe con canvas

    canvas_df = pd.DataFrame(canvas)

    # Remover success false

    canvas_df = canvas_df[canvas_df['success'] == 'true']

    # Remover canvas_url duplicados

    canvas_df = canvas_df.drop_duplicates(subset=['canvas_url'])
    
    # Remover columna success y message
    
    canvas_df = canvas_df.drop(['success', 'message'], axis=1)
    
    # Guardar dataframe en csv

    canvas_df.to_csv('canvas.csv', index=False)
    canvas_df.to_html('./templates/canvas.html', index=False)