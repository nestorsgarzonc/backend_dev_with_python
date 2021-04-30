from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'HW'


@app.route('/bye/<name>')
def bye(name):
    return f'<h1 style="text-align:center;">Bye {name}</h1>'


if __name__ == '__main__':
    app.run(debug=True)
