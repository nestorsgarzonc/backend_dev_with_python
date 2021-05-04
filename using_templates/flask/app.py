from flask import Flask, render_template
from random import randint
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def home():
    return render_template(
        'index.html',
        title='NW by Flask',
        number=randint(0, 100),
        year=datetime.today().year
    )


if __name__ == '__main__':
    app.run()
