import requests
from models import db, Character, Planet, Vehicle
from app import app

# URL de la API de SWAPI
SWAPI_PEOPLE_URL = 'https://swapi.dev/api/people/'
SWAPI_PLANETS_URL = 'https://swapi.dev/api/planets/'
SWAPI_VEHICLES_URL = 'https://swapi.dev/api/vehicles/'

# Esta función obtiene los datos de personajes desde la API de SWAPI
def fetch_characters():
    response = requests.get(SWAPI_PEOPLE_URL)
    data = response.json()

    # Recorrer la lista de resultados y guardar en la base de datos
    for person in data['results']:
        new_character = Character(
            name=person['name'],
            description="Unknown",  # Puedes mapearlo o dejarlo así
            eye_color=person.get('eye_color', "Unknown"),
            birth_year=person.get('birth_year', "Unknown"),
            gender=person.get('gender', "Unknown"),
            hair_color=person.get('hair_color', "Unknown"),
        )
        db.session.add(new_character)
    
    db.session.commit()
    print("Characters added to the database.")

# Esta función obtiene los datos de planetas desde la API de SWAPI
def fetch_planets():
    response = requests.get(SWAPI_PLANETS_URL)
    data = response.json()

    # Recorrer la lista de resultados y guardar en la base de datos
    for planet in data['results']:
        new_planet = Planet(
            name=planet['name'],
            description=planet.get('description', "Unknown"),
            gravity=planet.get('gravity', "Unknown"),
            population=planet.get('population', "Unknown"),
            climate=planet.get('climate', "Unknown"),
        )
        db.session.add(new_planet)
    
    db.session.commit()
    print("Planets added to the database.")

# Esta función obtiene los datos de vehículos desde la API de SWAPI
def fetch_vehicles():
    response = requests.get(SWAPI_VEHICLES_URL)
    data = response.json()

    # Recorrer la lista de resultados y guardar en la base de datos
    for vehicle in data['results']:
        new_vehicle = Vehicle(
            name=vehicle['name'],
            description=vehicle.get('description', "Unknown"),
            model=vehicle.get('model', "Unknown"),
            manufacturer=vehicle.get('manufacturer', "Unknown"),
        )
        db.session.add(new_vehicle)
    
    db.session.commit()
    print("Vehicles added to the database.")

if __name__ == "__main__":
    # Hacer fetch de datos dentro del contexto de la app
    with app.app_context():
        fetch_characters()  # Cargar personajes en la base de datos
        fetch_planets()     # Cargar planetas en la base de datos
        fetch_vehicles()    # Cargar vehículos en la base de datos
