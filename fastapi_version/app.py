from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return 'HW'


@app.get('/bye/{name}')
def bye(name: str):
    return f'Bye {name}! :)'
