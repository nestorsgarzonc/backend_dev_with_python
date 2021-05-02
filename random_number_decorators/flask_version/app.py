from flask import Flask
import random

app = Flask(__name__)
winner_number = random.randrange(10)


def random_decorator(function):
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


@app.route('/')
def index():
    return 'Guess a number between 0 and 9'


@app.route('/a/<int:number>')
@random_decorator
def bye(number):
    return f'<h1 style="text-align:center;">CONGRATULATIONS {number}</h1> <img src="https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif"/>'


if __name__ == '__main__':
    app.run(debug=True)
