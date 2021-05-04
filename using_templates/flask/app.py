from flask import Flask, render_template
from random import randint
from datetime import datetime
import requests

app = Flask(__name__)


@app.route('/')
def home():
    return render_template(
        'index.html',
        title='NW by Flask',
        number=randint(0, 100),
        year=datetime.today().year
    )


@app.route('/guess/<name>')
def guess(name: str):
    res_y = requests.get('https://api.agify.io', params={'name': name})
    res_g = requests.get('https://api.genderize.io', params={'name': name})
    gender = res_g.json()['gender']
    years = res_y.json()['age']
    return render_template(
        'guess.html',
        title=name,
        gender=gender,
        year=years,
    )


if __name__ == '__main__':
    app.run()
