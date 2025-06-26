import os
from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# SQLAlchemy database instance (used globally)
db = SQLAlchemy()
# define the path to the SQLite database file
DB_NAME = os.path.join(os.path.dirname(__file__), 'database.db')

# create and configure the Flask app
def create_app():
    app = Flask(__name__)
    # secret key used for session management 
    app.config['SECRET_KEY'] = 'qwertyuiop'
    # set database URI if not already configured
    if 'SQLALCHEMY_DATABASE_URI' not in app.config:
        DB_NAME = os.path.join(os.path.dirname(__file__), 'database.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'


    db.init_app(app)

    # import and register Blueprints (routes)
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

# create the database file and tables if it doesn't already exist
def create_database(app):
    print("Working directory at runtime:", os.getcwd())
    print("Database path:", DB_NAME)
    if not os.path.exists(DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')
