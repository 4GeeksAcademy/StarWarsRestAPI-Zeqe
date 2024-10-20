from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, User, Planet, Vehicle, Character, FavoriteCharacter, FavoriteVehicle, FavoritePlanet

def setup_admin(app):
    admin = Admin(app, name='My App Admin', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Planet, db.session))
    admin.add_view(ModelView(Vehicle, db.session))
    admin.add_view(ModelView(Character, db.session))
    admin.add_view(ModelView(FavoriteCharacter, db.session))
    admin.add_view(ModelView(FavoriteVehicle, db.session))
    admin.add_view(ModelView(FavoritePlanet, db.session))
