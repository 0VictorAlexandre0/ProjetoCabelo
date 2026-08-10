from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def criar_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    from app import entidades #ele está aqui para iniciar os models antes de criar as tabelas

    return app