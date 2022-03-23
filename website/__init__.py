from os import path
from urllib.request import pathname2url
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#variables para trabajar con la base de datos en todo el proyecto
db = SQLAlchemy()
DB_NAME = "database.db"

#funcion para crear la aplicacion en flask
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'I am the secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

#funcion para crear la base de datos si aun no existe ninguna
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database')


