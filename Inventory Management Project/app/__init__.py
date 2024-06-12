# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Key' #Used for encrypting sessions
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1001@localhost/NqtProjDB'
    db.init_app(app)

    # Register routes from api.py
    from . import api
    api.init_app(app)

    return app
