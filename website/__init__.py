# __init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = os.path.join(os.path.dirname(__file__), 'database.db')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'qwertyuiop'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    print("DB URI:", app.config['SQLALCHEMY_DATABASE_URI'])

    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Asset

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    print("Working directory at runtime:", os.getcwd())
    print("Database path:", DB_NAME)
    if not os.path.exists(DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')
