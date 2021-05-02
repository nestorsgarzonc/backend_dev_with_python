from fastapi import FastAPI
from functools import wraps
from fastapi.responses import HTMLResponse
import random

app = FastAPI()
winner_number = random.randrange(10)


def random_decorator(function):
    @wraps(function)
    def wrapper(**kwargs):
        print(f'WINNER NUMBER: {winner_number}')
        print(kwargs)
        number = kwargs['number']
        if number == winner_number:
            return function(number)
        elif number > winner_number:
            return f'<h1 style="text-align:center;">TOO HIGH {number}</h1> <img src="https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif"/>'
        else:
            return f'<h1 style="text-align:center;">TOO LOW {number}</h1> <img src="https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif"/>'
    return wrapper


@app.get('/', response_class=HTMLResponse)
def index():
    return '<h1>Guess a number between 0 and 9<h1>'


@app.get('/{number}', response_class=HTMLResponse)
@random_decorator
def bye(number: int):
    return f'<h1 style="text-align:center;">CONGRATULATIONS {number}</h1> <img src="https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif"/>'
