from decorators.font_styles import make_bold, make_emphasis, make_underlined
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'HW'


@app.route('/bye')
@make_bold
@make_emphasis
@make_underlined
def bye_with_decorators():
    return 'Bye'


@app.route('/bye/<name>')
def bye(name):
    return f'<h1 style="text-align:center;">Bye {name}</h1>'


if __name__ == '__main__':
    app.run(debug=True)
