from flask import Flask, render_template, request
import requests

import requests


class Post:
    def __init__(self, post_id, date, title, author):
        self.id = post_id
        self.date = date
        self.title = title
        self.author = author


res = requests.get('https://api.npoint.io/0ad676fe3ff093ac9c24')
posts = [
    Post(post_id=i['id'], date=i['date'], title=i['title'], author=i['author']) for i in res.json()
]

app = Flask(__name__)


@app.route('/')
def home():
    return render_template(
        'index.html',
        image_path='background-image: url(../static/assets/img/home-bg.jpg)',
        title='NW BLOG',
        subtitle='A blog by Sebastian Garzon',
        posts=posts,
    )


@app.route('/post/<post_id>')
def post(post_id: str):
    sel_post = None
    for post in posts:
        print(post)
        if post.id == post_id:
            sel_post: Post = post
    print(sel_post)
    return render_template(
        'index.html',
        image_path='background-image: url(../static/assets/img/home-bg.jpg)',
        title=sel_post.title,
        subtitle=f'Id post: {post_id}',
        post=sel_post.author,
    )


@app.route('/about')
def about():
    return render_template('about.html',
                           image_path='background-image: url(../static/assets/img/about-bg.jpg)',
                           title='About me',
                           subtitle='That is what I do',
                           )


@app.route('/contact')
def contact():
    return render_template('contact.html',
                           image_path='background-image: url(../static/assets/img/contact-bg.jpg)',
                           title='Contact Me',
                           subtitle='Have questions? I have answers',
                           )


@ app.post('/contact_me')
def contact_me():
    data = {
        'name': request.form['name'],
        'email': request.form['email'],
        'phone': request.form['phone'],
        'message': request.form['message'],
    }
    print(data)
    return data
