#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

## RESTAURANTS ##########################################################################################
@app.get("/restaurants")
def get_all_restaurants():
    restaurant_list = Restaurant.query.all()
    restaurant_dicts = [restaurant.to_dict() for restaurant in restaurant_list]

    return restaurant_dicts, 200

@app.get("/restaurants/<int:id>")
def get_restaurant(id):
    found_restaurant = Restaurant.query.where(Restaurant.id == id).first()
    if found_restaurant:
        return found_restaurant.to_dict(), 200
    else:
        return {'error': 'Not found'}, 404



if __name__ == "__main__":
    app.run(port=5555, debug=True)
