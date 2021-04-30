from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI()


@app.get('/')
def index():
    return 'HW'


@app.get('/bye/{name}', response_class=HTMLResponse)
def bye(name: str):
    data = f'<h1>Bye {name}! :)</h1>'
    return data
