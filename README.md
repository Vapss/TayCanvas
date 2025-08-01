# TayCanvas
 Proyecto con FastAPI, HTML, CSS y JavaScript.
 
 Integra funciones para extraer Canvas(MP4) desde spotify con Canvastify(https://github.com/Delitefully/spotify-canvas-downloader). Además obtiene albums, artistas y canciones con el API de Spotify.
 
conda create -n taylor python=3.9
conda activate taylor
conda install pip
pip install -r requirements.txt

Frontend basico HTML,CSS Y JS.

## Configuración de Spotify

Para que las funciones que utilizan la API de Spotify funcionen correctamente es
necesario definir las siguientes variables de entorno:

```
SPOTIPY_CLIENT_ID
SPOTIPY_CLIENT_SECRET
SPOTIPY_REDIRECT_URL
```

Puedes crearlas en un archivo `.env` o exportarlas directamente en tu consola
antes de ejecutar la aplicación. También es necesario definir `HOST_ORIGIN` con
la URL desde la que se servirá la API.

Puedes tomar como referencia el archivo `.env.example` incluido en el
repositorio.

## Ejecutar la aplicación

Si trabajas localmente puedes iniciar el servidor con **uvicorn**:

```bash
uvicorn src.main:app --reload
```

Para levantar todo con Docker puedes usar:

```bash
docker-compose up --build
```

## Pruebas

Las pruebas unitarias se ejecutan con **pytest**:

```bash
pytest
```
