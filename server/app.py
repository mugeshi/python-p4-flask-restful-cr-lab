#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route('/plants', methods=['GET'])
def index():
    # Retrieve all plants from the database and convert to JSON format
    plants = Plant.query.all()
    plant_list = [plant.to_dict() for plant in plants]
    return jsonify(plant_list), 200

@app.route('/plants/<int:id>', methods=['GET'])
def show(id):
    # Retrieve a specific plant by its ID and convert to JSON format
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({"message": "Plant not found"}), 404
    return jsonify(plant.to_dict()), 200

@app.route('/plants', methods=['POST'])
def create():
    # Create a new plant based on the JSON request data
    data = request.get_json()
    new_plant = Plant(**data)
    db.session.add(new_plant)
    db.session.commit()
    return jsonify(new_plant.to_dict()), 201
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
