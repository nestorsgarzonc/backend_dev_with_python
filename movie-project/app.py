from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

API_KEY = ADDD

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies.db"


Bootstrap(app)

db = SQLAlchemy(app)


class EditMovieForm(FlaskForm):
    rating = StringField(label='rating', validators=[DataRequired()])
    review = StringField(label='review', validators=[DataRequired()])
    submit = SubmitField(label='submit')


class AddMovieForm(FlaskForm):
    name = StringField(label='name', validators=[DataRequired()])
    submit = SubmitField(label='submit')


class Movie(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Float, nullable=False)
    review = db.Column(db.String(255), nullable=False)
    img_url = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'''
        id: {self.id}
        title: {self.title}
        year: {self.year}
        description: {self.description}
        rating: {self.rating}
        ranking: {self.ranking}
        review: {self.review}
        img_url: {self.img_url}
        '''


try:
    db.create_all()
except Exception as e:
    print(e)


@app.route("/")
def home():
    all_movies = db.session.query(Movie).all()
    return render_template("index.html", movies=all_movies)


@app.route("/edit/<id>", methods=['GET', 'POST'])
def edit(id: str):
    movie = Movie.query.get(id)
    form = EditMovieForm()
    if form.validate_on_submit():
        movie.review = form.review.data
        movie.rating = float(form.rating.data)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)


@app.route("/delete/<id>")
def delete(id: str):
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=['GET', 'POST'])
def add():
    form = AddMovieForm()
    if form.validate_on_submit():
        print(form.name.data)
        res = requests.get(
            'https://api.themoviedb.org/3/search/movie',
            params={
                'api_key': '38a229726f7775bfb2a13412bc203940',
                'language': 'en-US',
                'page': '1',
                'include_adult': 'false',
                'query': 'batman',
            }
        )
        print(res.json())
        return redirect(url_for('select', name=form.name.data))
    return render_template('add.html', form=form)


@app.route("/select/<name>", methods=['GET', 'POST'])
def select(name: str):
    print(name)
    res = requests.get(
        'https://api.themoviedb.org/3/search/movie',
        params={
            'api_key': '38a229726f7775bfb2a13412bc203940',
            'language': 'en-US',
            'page': '1',
            'include_adult': 'false',
            'query': name,
        }
    )
    print(res.json())
    return render_template('select.html', movies=res.json()['results'])


@app.route("/add/<id>", methods=['GET', 'POST'])
def add_id(id: str):
    print(id)
    res = requests.get(
        f'https://api.themoviedb.org/3/movie/{id}',
        params={
            'api_key': '38a229726f7775bfb2a13412bc203940',
            'language': 'en-US',
        }
    )
    res_json = res.json()
    new_movie = Movie(
        title=res_json['title'],
        year=int(res_json['release_date'][:4]),
        description=res_json['overview'],
        rating=0.0,
        ranking=float(res_json['popularity']),
        review="",
        img_url=f"https://image.tmdb.org/t/p/w500{res_json['poster_path']}"
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('edit', id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)
