from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

login_manager = LoginManager()
app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager.init_app(app)
# CREATE TABLE IN DB


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
# Line below only required once, when creating DB.
# db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template('index.html', is_logged_in=current_user.is_authenticated)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(
            email=request.form['email'],
            password=generate_password_hash(
                request.form['password'],
                salt_length=8
            ),
            name=request.form['name'],
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Logged in successfully.')
        return redirect(url_for('secrets'))
    return render_template('register.html', is_logged_in=current_user.is_authenticated)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(
            email=request.form['email'],
        ).first()
        if user:
            password = request.form['password']
            if check_password_hash(user.password, password=password):
                login_user(user)
                flash('Logged in successfully.')
                return redirect(url_for('secrets'))
            else:
                flash('Invalid credentials')
                return render_template('login.html', error=True)
        else:
            flash('Opps occured an error')
            return render_template('login.html', error=True)
    return render_template('login.html', is_logged_in=current_user.is_authenticated)


@app.route('/secrets')
@login_required
def secrets():
    return render_template('secrets.html', user=current_user, is_logged_in=current_user.is_authenticated)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    return send_from_directory('static', filename='files/cheat_sheet.pdf')


if __name__ == '__main__':
    app.run(debug=True)
