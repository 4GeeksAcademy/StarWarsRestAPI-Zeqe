from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250))
    gravity = db.Column(db.String(250))
    population = db.Column(db.String(250))
    climate = db.Column(db.String(250))
    favorite_planets = db.relationship('FavoritePlanet', back_populates='planet')

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate
        }

class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250))
    model = db.Column(db.String(250))
    manufacturer = db.Column(db.String(250))
    favorite_vehicles = db.relationship('FavoriteVehicle', back_populates='vehicle')

    def __repr__(self):
        return '<Vehicle %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "model": self.model,
            "manufacturer": self.manufacturer
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    birth_year = db.Column(db.String(250))
    gender = db.Column(db.String(6))
    hair_color = db.Column(db.String(250))
    favorite_characters = db.relationship('FavoriteCharacter', back_populates='character')

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "hair_color": self.hair_color
        }

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250))
    apellido = db.Column(db.String(250))
    email = db.Column(db.String(250), unique=True)
    username = db.Column(db.String(50), unique=True)  # Campo de username único
    password = db.Column(db.String(50))
    fecha_ingreso = db.Column(db.String(250))
    is_active = db.Column(db.Boolean(), default=True, unique=False, nullable=False)
    
    favorite_characters = db.relationship('FavoriteCharacter', back_populates='user')
    favorite_vehicles = db.relationship('FavoriteVehicle', back_populates='user')
    favorite_planets = db.relationship('FavoritePlanet', back_populates='user')

    def __repr__(self):
        return f'<User {self.username}>'

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha_ingreso": self.fecha_ingreso,
            "is_active": self.is_active
        }

    def serialize_favorites(self):
        result = {
            "user": self.serialize(),
            "favorites": {
                "characters": [fav.character.serialize() for fav in self.favorite_characters],
                "vehicles": [fav.vehicle.serialize() for fav in self.favorite_vehicles],
                "planets": [fav.planet.serialize() for fav in self.favorite_planets],
            }
        }
        return result


class FavoriteCharacter(db.Model):
    __tablename__ = 'favorite_characters'
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    character = db.relationship(Characters)
    user = db.relationship(Users)

    def __repr__(self):
        return '<FavoriteCharacter %r>' % self.id

class FavoriteVehicle(db.Model):
    __tablename__ = 'favorite_vehicles'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    vehicle = db.relationship(Vehicles)
    user = db.relationship(Users)

    def __repr__(self):
        return '<FavoriteVehicle %r>' % self.id

class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planets'
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    planet = db.relationship(Planets)
    user = db.relationship(Users)

    def __repr__(self):
        return '<FavoritePlanet %r>' % self.id
