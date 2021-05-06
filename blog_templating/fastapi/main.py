
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            'posts': posts,
        }
    )


@app.get('/post/{id}', response_class=HTMLResponse)
def post(request: Request, id: str):
    sel_post: Post = None
    print(id)
    for i in posts:
        if i.id == id:
            sel_post = i
        break
    return templates.TemplateResponse(
        'post.html',
        {
            'request': request,
            'post': sel_post,
        }
    )
