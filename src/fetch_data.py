import requests
from models import db, People, Planet
from app import app

# URL de la API de SWAPI
SWAPI_PEOPLE_URL = 'https://swapi.dev/api/people/'
SWAPI_PLANETS_URL = 'https://swapi.dev/api/planets/'

# Esta función obtiene los datos de personajes desde la API de SWAPI
def fetch_people():
    response = requests.get(SWAPI_PEOPLE_URL)
    data = response.json()

    # Recorrer la lista de resultados y guardar en la base de datos
    for person in data['results']:
        new_person = People(
            name=person['name'],
            age="Unknown",  # SWAPI no da la edad exacta
            occupation="Unknown",  # Puedes mapearlo o dejarlo así
            address="Unknown",  # Datos ficticios si no hay
            is_active=True  # Esto lo defines tú
        )
        db.session.add(new_person)
    
    db.session.commit()
    print("People added to the database.")

# Esta función obtiene los datos de planetas desde la API de SWAPI
def fetch_planets():
    response = requests.get(SWAPI_PLANETS_URL)
    data = response.json()

    # Recorrer la lista de resultados y guardar en la base de datos
    for planet in data['results']:
        new_planet = Planet(
            name=planet['name'],
            galaxy="Unknown",  # SWAPI no tiene esta información
            type_of_inhabitant="Unknown",  # Puedes mapearlo o dejarlo así
            inhabitant_height="Unknown",  # Datos ficticios si no hay
        )
        db.session.add(new_planet)
    
    db.session.commit()
    print("Planets added to the database.")

if __name__ == "__main__":
    # Hacer fetch de datos dentro del contexto de la app
    with app.app_context():
        fetch_people()  # Cargar personajes en la base de datos
        fetch_planets()  # Cargar planetas en la base de datos
