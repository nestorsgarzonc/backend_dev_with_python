from flask import Flask

app = Flask()


@app.route('/')
def index():
    return 'HW'
