from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import asyncio
import canvas
import canvTay
from constants import TOKEN_RENEW_TIME

app = FastAPI()

templates = Jinja2Templates(directory="templates")

ORIGIN = os.getenv('HOST_ORIGIN')
origins = [
    ORIGIN,
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

access_token = ""

@app.get('/api/canvas/{track_id}')
def get_track_canvas(track_id):
    try:
        canvas_url = canvas.get_canvas_for_track(access_token, track_id)
        return {'success': 'true', 'canvas_url': canvas_url}
    except AttributeError:
        return {'success': 'false', 'message': 'No canvas found for this track'}
    except ConnectionError:
        return {'success': 'false', 'message': 'failed to connect to Spotify'}
    
@app.get('/api/taylorSwift')
def get_taylor_swift():
    canvTay.credenciales()

@app.get('/api/health')
def health():
    return "up"

async def refresh_token():
    global access_token
    while True:
        print('INFO:     Getting a fresh Spotify access token')

        try:
            access_token = canvas.get_access_token()
        except Exception as e:
            print(f'ERROR:   Failed to get a new access token: {e}')

        await asyncio.sleep(TOKEN_RENEW_TIME)

@app.on_event("startup")
async def startup_event():
    asyncio.get_event_loop().create_task(refresh_token())
    
# Monstrar el index.html
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("canvas.html", {"request": request})

