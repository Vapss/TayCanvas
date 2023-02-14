# Obtener lista de todas las canciones de Taylor swift con el API de Spotify

# Importamos librerias
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import json
import requests
import datetime

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

    album_ids = [album['id'] for album in albums]
    # Obtener todas las canciones de cada album con columna nombre y album y url y track_id
    songs = []

    for album_id in album_ids:
        album = spotify.album(album_id)
        songs.extend(
            [
                track['name'],
                album['name'],
                track['external_urls']['spotify'],
                track['id'],
            ]
            for track in album['tracks']['items']
        )
    # Convertir a dataframe
    songs_df = pd.DataFrame(songs, columns=['song_name', 'album_name', 'url', 'track_id'])


    # Obtener canvas de cada cancion desde http://localhost:8000/api/canvas/{track_id}. Agregar el nombre de la cancion a la respuesta desde songs_df y agregar a un array
    # Agregar fecha de obtencion de canvas al nombre del archivo
    canvas = []


    for track_id in songs_df['track_id']:
        # Realizar llamada interna a la API
        response = requests.get(f'http://localhost:8000/api/canvas/{track_id}').json()
        print(response)


        # Agregar nombre de la cancion y album al que pertenece
        song_name = songs_df[songs_df['track_id'] == track_id]['song_name'].values[0]
        album_name = songs_df[songs_df['track_id'] == track_id]['album_name'].values[0]

        response['album_name'] = album_name
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
    # Agregar fecha de obtencion de canvas al nombre del archivo
    
    canvas_df.to_csv(f'./data/canvas_{datetime.now().strftime("%Y-%m-%d")}.csv', index=False)
    # Ahora en html
    canvas_df.to_html(f'./data/canvas_{datetime.now().strftime("%Y-%m-%d")}.html', index=False)
    
    # Comparar con canvas anterior y resaltar los cambios
    
    # Guardamos la fecha de la ultima actualizacion
    with open('./data/last_update.txt', 'w') as f:
        f.write(datetime.now().strftime("%Y-%m-%d"))
    
    # Leer canvas anterior desde la fecha de la ultima actualización
    with open('./data/last_update.txt', 'r') as f:
        last_update = f.read()
    
    # Leer canvas anterior
    canvas_old = pd.read_csv(f'./data/canvas_{last_update}.csv')
    
    # Comparar con canvas actual
    canvas_new = canvas_df

    # Comparar columnas
    canvas_new['new'] = True
    canvas_old['new'] = False

    # Unir dataframes
    canvas_all = pd.concat([canvas_new, canvas_old])
    
    # Remover duplicados
    canvas_all = canvas_all.drop_duplicates(subset=['canvas_url'], keep=False)

    # Mostrar cambios en html
    canvas_all.to_html(f'./data/canvas_changes_{datetime.now().strftime("%Y-%m-%d")}.html', index=False)
