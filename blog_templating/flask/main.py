from flask import Flask, render_template
import requests


class Post:
    def __init__(self, id, date, title, author):
        self.id = id
        self.date = date
        self.title = title
        self.author = author

    def __str__(self):
        return f"""
        id: {self.id}
        date: {self.date}
        title: {self.title}
        author: {self.author}
        """


res = requests.get('https://api.npoint.io/0ad676fe3ff093ac9c24')
posts = [
    Post(id=i['id'], date=i['date'], title=i['title'], author=i['author']) for i in res.json()
]

app = Flask(__name__)


@app.route('/')
def home():
    return render_template(
        'index.html',
        posts=posts,
    )


@app.route('/post/<id>')
def post(id: str):
    sel_post: Post = None
    print(id)
    for i in posts:
        if i.id == id:
            sel_post = i
        break
    return render_template(
        'post.html',
        post=sel_post,
    )
