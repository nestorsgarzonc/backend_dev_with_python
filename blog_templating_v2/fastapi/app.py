from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse('index.html', {
        'request': request,
        'image_path': 'background-image: url(../static/assets/img/home-bg.jpg)',
        'title': 'NW BLOG',
        'subtitle': 'A blog by Sebastian Garzon',
        'posts': posts,
    })


@app.get('/post/{post_id}', response_class=HTMLResponse)
def post(request: Request, post_id: str):
    sel_post = None
    for post in posts:
        print(post)
        if post.id == post_id:
            sel_post: Post = post
    print(sel_post)
    return templates.TemplateResponse('index.html', {
        'request': request,
        'image_path': 'background-image: url(../static/assets/img/home-bg.jpg)',
        'title': sel_post.title,
        'subtitle': f'Id post: {post_id}',
        'post': sel_post.author,
    })


@app.get('/about', response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse('about.html', {
        'request': request,
        'image_path': 'background-image: url(../static/assets/img/about-bg.jpg)',
        'title': 'About me',
        'subtitle': 'That is what I do',
    })


@app.get('/contact', response_class=HTMLResponse)
def contact(request: Request):
    return templates.TemplateResponse('contact.html', {
        'request': request,
        'image_path': 'background-image: url(../static/assets/img/contact-bg.jpg)',
        'title': 'Contact Me',
        'subtitle': 'Have questions? I have answers',
    })


@app.post('/contact_me')
def contact_me(
        name: str = Form(...),
        email: str = Form(...),
        phone: str = Form(...),
        message: str = Form(...),
):
    data = {
        'name': name,
        'email': email,
        'phone': phone,
        'message': message,
    }
    print(data)
    return data
