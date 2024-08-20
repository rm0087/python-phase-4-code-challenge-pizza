#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
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
    restaurant_dicts = [{
        'id': restaurant.id,
        'name': restaurant.name,
        'address': restaurant.address
    } for restaurant in restaurant_list]

    return restaurant_dicts, 200

@app.get("/restaurants/<int:id>")
def get_restaurant(id):
    try:
        restaurant = Restaurant.query.filter(Restaurant.id == id).first()
        restaurant_dict = restaurant.to_dict()
        response = make_response(restaurant_dict,200)
        return response
    except:
        return {'error':'Restaurant not found.'},404
    
@app.delete("/restaurants/<int:id>")
def delete_restaurant(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        response = make_response({},204)
        return response
    else:
        return {'error':'Restaurant not found.'},404
    
## PIZZAS ##########################################################################################    
@app.get("/pizzas")
def get_all_pizzas():
    pizza_list = Pizza.query.all()
    pizza_dicts = [pizza.to_dict() for pizza in pizza_list]

    return pizza_dicts, 200
 
if __name__ == "__main__":
    app.run(port=5555, debug=True)
