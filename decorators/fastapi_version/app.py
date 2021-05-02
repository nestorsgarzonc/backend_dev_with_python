from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from decorators.font_styles import make_bold, make_emphasis, make_underlined

app = FastAPI()


@app.get('/')
def index():
    return 'HW'


@app.get('/bye/{name}', response_class=HTMLResponse)
def bye(name: str):
    data = f'<h1>Bye {name}! :)</h1>'
    return data


@app.get('/bye', response_class=HTMLResponse)
@make_bold
@make_emphasis
@make_underlined
def bye_with_decorators():
    return 'Bye'
