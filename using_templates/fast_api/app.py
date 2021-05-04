from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from random import randint
from datetime import datetime
import requests

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            'title': 'NW by FastApi',
            'number': randint(0, 100),
            'year': datetime.now().year,
        }
    )


@app.get('/guess/{name}')
async def guess(request: Request, name: str):
    res_y = requests.get('https://api.agify.io', params={'name': name})
    res_g = requests.get('https://api.genderize.io', params={'name': name})
    gender = res_g.json()['gender']
    years = res_y.json()['age']
    return templates.TemplateResponse(
        'guess.html',
        {
            'request': request,
            'title': name,
            'gender': gender,
            'year': years,
        }
    )
