"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os, random
import requests
from flask import Flask, jsonify, abort, request
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

@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Datos simulados para usuarios
users = [
    {
        "id": 1,
        "nombre": "Ezequiel",
        "apellido": "Bellino",
        "email": "ezebellino@hotmail.com",
        "fecha_ingreso": "10/10/2024",
        "username": "ezebellino",
        "is_active": True
    }
]

# Endpoint para obtener usuarios
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    username = "ezebellino" 

    # Acá genero 3 elementos aleatorios
    favorite_items = []
    for _ in range(3):
        random_type = random.choice(["people", "vehicles", "planets"])  # Tipo aleatorio
        random_id = random.randint(1, 82)  # ID aleatorio (ajusta el rango según SWAPI)
        swapi_url = f"https://swapi.dev/api/{random_type}/{random_id}"
        response = requests.get(swapi_url)
        
        if response.status_code == 200:
            data = response.json()
            item_type = "character" if random_type == "people" else random_type[:-1]  # Formato de tipo
            favorite_items.append({
                "name": data.get("name"),
                "type": item_type
            })

    # Devuelvo los elementos favoritos en formato JSON
    return jsonify({
        "username": username,
        "favorites": favorite_items
    })


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
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

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
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



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
