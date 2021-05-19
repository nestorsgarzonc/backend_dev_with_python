from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, Length
from wtforms.validators import DataRequired

app = Flask(__name__)
Bootstrap(app)

app.secret_key = "some secret string"


class LoginForm(FlaskForm):
    email = StringField(label='email', validators=[DataRequired(), Email()])
    password = PasswordField(label='password', validators=[
                             DataRequired(),
                             Length(min=8),
                             ])
    submit = SubmitField(label='submit')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/sucess')
def sucess():
    return render_template('success.html')


@app.route('/denied')
def denied():
    return render_template('denied.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.email.data)
        print(form.password.data)
        if form.email.data == 'admin@gmail.com' and form.password.data == '123456':
            return redirect('/sucess')
        return redirect('/denied')
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
