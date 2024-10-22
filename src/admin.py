from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, Users, Planets, Vehicles, Characters, FavoriteCharacter, FavoriteVehicle, FavoritePlanet

def setup_admin(app):
    admin = Admin(app, name='My App Admin', template_mode='bootstrap3')
    admin.add_view(ModelView(Users, db.session))
    admin.add_view(ModelView(Planets, db.session))
    admin.add_view(ModelView(Vehicles, db.session))
    admin.add_view(ModelView(Characters, db.session))
    admin.add_view(ModelView(FavoriteCharacter, db.session))
    admin.add_view(ModelView(FavoriteVehicle, db.session))
    admin.add_view(ModelView(FavoritePlanet, db.session))
