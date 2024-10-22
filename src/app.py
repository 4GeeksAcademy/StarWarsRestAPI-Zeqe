"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, Planets, Vehicles, Characters, FavoriteCharacter, FavoriteVehicle, FavoritePlanet

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'Eze030790.') 
app.url_map.strict_slashes = False


db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/users/favorites', methods=['GET'])
def list_favorites():
    current_user_id = request.args.get('user_id')  

    if not current_user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    user = Users.query.get(current_user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(user.serialize_favorites()), 200


@app.route('/favorite/vehicles/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(vehicle_id):
    current_user_id = request.args.get('user_id')  
    if not current_user_id:
        return jsonify({'error': 'User not authenticated'}), 401
    vehicle = Vehicles.query.get(vehicle_id)
    if vehicle is None:
        return jsonify({'error': 'Vehicle not found'}), 404

    new_favorite = FavoriteVehicle(user_id=current_user_id, vehicle_id=vehicle_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({'message': 'Favorite vehicle added successfully!'}), 201

@app.route('/favorite/vehicles/<int:vehicle_id>', methods=['DELETE'])
def remove_favorite_vehicle(vehicle_id):
    current_user_id = request.args.get('user_id')

    if not current_user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    favorite = FavoriteVehicle.query.filter_by(user_id=current_user_id, vehicle_id=vehicle_id).first()

    if favorite is None:
        return jsonify({'error': 'Favorite vehicle not found'}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({'message': 'Favorite vehicle removed successfully!'}), 200


@app.route('/favorite/planets/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    current_user_id = request.args.get('user_id') 

    if not current_user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({'error': 'Planet not found'}), 404

    new_favorite = FavoritePlanet(user_id=current_user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({'message': 'Favorite planet added successfully!'}), 201

@app.route('/favorite/planets/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    current_user_id = request.args.get('user_id')

    if not current_user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    favorite = FavoritePlanet.query.filter_by(user_id=current_user_id, planet_id=planet_id).first()

    if favorite is None:
        return jsonify({'error': 'Favorite planet not found'}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({'message': 'Favorite planet removed successfully!'}), 200


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_character(people_id):
    current_user_id = request.args.get('user_id')  

    if not current_user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    character = Characters.query.get(people_id)
    if character is None:
        return jsonify({'error': 'Character not found'}), 404

    new_favorite = FavoriteCharacter(user_id=current_user_id, character_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({'message': 'Favorite character added successfully!'}), 201

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def remove_favorite_character(people_id):
    current_user_id = request.args.get('user_id')

    if not current_user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    favorite = FavoriteCharacter.query.filter_by(user_id=current_user_id, character_id=people_id).first()

    if favorite is None:
        return jsonify({'error': 'Favorite character not found'}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({'message': 'Favorite character removed successfully!'}), 200


@app.route('/')
def sitemap():
    return generate_sitemap(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
