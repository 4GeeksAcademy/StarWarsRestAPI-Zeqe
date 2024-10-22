from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, Users, Planets, Vehicles, Characters

class SecureUserView(ModelView):

    column_exclude_list = ['password']


    form_excluded_columns = ['password']


    def _password_formatter(view, context, model, name):
        return '*****'  

    column_formatters = {
        'password': _password_formatter
    }

def setup_admin(app):
    admin = Admin(app, name='API Admin', template_mode='bootstrap3')

    admin.add_view(SecureUserView(Users, db.session))  
    admin.add_view(ModelView(Planets, db.session))
    admin.add_view(ModelView(Vehicles, db.session))
    admin.add_view(ModelView(Characters, db.session))
