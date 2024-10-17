'''from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
'''
'''class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
'''
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.String(120), nullable=False)
    occupation = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean()), nullable=False)
    

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    galaxy = db.Column(db.String(100), unique=False, nullable=False)
    type_of_inhabitant = db.Column(db.String(80), unique=False, nullable=False)
    inhabitant_height = db.Column(db.String(80), unique=False, nullable=False)


class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    people = db.relationship('People', backref='favorites', lazy=True)
    planet = db.relationship('Planet', backref='favorites', lazy=True)

def __repr__(self):
    return `<User %r>` % self.username
