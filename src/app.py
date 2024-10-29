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

@app.route('/users', methods=['GET'])
def get_users():
    # Consulta todos los usuarios en la base de datos
    users = Users.query.all()
    
    # Usuarios en un formato JSON
    users_data = [
        {
            "id": user.id,
            "nombre": user.nombre,
            "apellido": user.apellido,
            "email": user.email,
            "fecha_ingreso": user.fecha_ingreso,
            "username": user.username,
            "is_active": user.is_active
        } for user in users
    ]
    
    return jsonify(users_data)

@app.route('/people', methods=['GET'])
def get_all_people():
    characters = Characters.query.all()

    characters_data = [
        {
            'name':character.name,
            'id': character.id,            
            'description': character.description,
            'eye_color': character.eye_color,
            'birth_year': character.birth_year,
            'gender': character.gender,
            'hair_color': character.hair_color
        }
        for character in characters
    ]
    return jsonify(characters_data), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_by_id(people_id):
    character = Characters.query.get(people_id)
    
    if character is None:
        abort(404, description="Character not found")
    
    # Serializar los datos 
    people_data = {
            'name':character.name,            
            'description': character.description,
            'eye_color': character.eye_color,
            'birth_year': character.birth_year,
            'gender': character.gender,
            'hair_color': character.hair_color
    }
    
    # Devolver los datos en formato JSON
    return jsonify(people_data), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    # Consultar todos los planetas en la base de datos
    planets = Planets.query.all()
    #Serializer
    planets_data = [
        {
            'name': planet.name,
            'id': planet.id,
            'description': planet.description,
            'gravity': planet.gravity,
            'population': planet.population,
            'climate': planet.climate
        }
        for planet in planets
    ]
    
    # Devolver los datos en formato JSON
    return jsonify(planets_data), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    planet = Planets.query.get(planet_id)
    
    if planet is None:
        abort(404, description="Planet not found")
    
    # Serializar los datos 
    planet_data = {
            'name': planet.name,
            'gravity': planet.gravity,
            'population': planet.population,
            'climate': planet.climate
    }
    
    # Devolver los datos en formato JSON
    return jsonify(planet_data), 200

# Ruta para obtener todos los vehículos
@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    # Consultar todos los vehículos en la base de datos
    vehicles = Vehicles.query.all()
    
    # Serializar los datos
    vehicles_data = [
        {
            'name': vehicle.name,
            'id': vehicle.id,
            'description': vehicle.description,
            'model': vehicle.model,
            'manufacturer': vehicle.manufacturer
        }
        for vehicle in vehicles
    ]
    
    # Devolver los datos en formato JSON
    return jsonify(vehicles_data), 200

# Ruta para obtener un vehículo por ID
@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle_by_id(vehicle_id):
    # Consultar el vehículo por su ID en la base de datos
    vehicle = Vehicles.query.get(vehicle_id)
    
    # Verificar si el vehículo existe
    if vehicle is None:
        abort(404, description="Vehicle not found")
    
    # Serializar los datos del vehículo encontrado
    vehicle_data = {
        'name': vehicle.name,
        'description': vehicle.description,
        'model': vehicle.model,
        'manufacturer': vehicle.manufacturer
    }
    
    # Devolver los datos en formato JSON
    return jsonify(vehicle_data), 200

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
