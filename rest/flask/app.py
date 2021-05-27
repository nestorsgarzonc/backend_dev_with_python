from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random as rd
app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

API_KEY = '123123'

# Cafe TABLE Configuration


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_json(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def random():
    coffees = db.session.query(Cafe).all()
    coffee_indx = rd.randrange(int(len(coffees)))
    coffee = coffees[coffee_indx]
    return jsonify(coffee.to_json())


@app.route("/all")
def all():
    coffees = db.session.query(Cafe).all()
    coffees_json = [i.to_json() for i in coffees]
    return jsonify(data=coffees_json)


@app.route("/add", methods=["POST"])
def add():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={'success': 'Successfully added the new cafe'})


@app.route("/update_price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id: str):
    coffee = Cafe.query.get(cafe_id)
    if coffee:
        coffee.coffee_price = request.form.get('price')
        db.session.commit()
        return jsonify(response={'success': 'Successfully modified the price of the cafe'}), 200
    return jsonify(response={'Error': 'Cafe dont found :c'}), 400


@app.route("/delete_coffee/<cafe_id>", methods=["DELETE"])
def delete_coffee(cafe_id: str):
    coffee = Cafe.query.get(cafe_id)
    if request.args.get('api-key') != API_KEY:
        return jsonify(response={'Error': 'Dont authorized :c'}), 403
    if coffee:
        db.session.delete(coffee)
        db.session.commit()
        return jsonify(response={'success': 'Successfully deleted the cafe'}), 200
    return jsonify(response={'Error': 'Cafe dont found :c'}), 400


@app.route("/search")
def search():
    loc = request.args.get('loc')
    coffee = db.session.query(Cafe).filter(Cafe.location == loc).first()
    if coffee:
        return jsonify(data=coffee.to_json())
    return jsonify(error='NOT FOUND')


if __name__ == '__main__':
    app.run(debug=True)
