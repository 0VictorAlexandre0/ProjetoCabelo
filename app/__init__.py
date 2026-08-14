from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def criar_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from app import entidades 

    from app.entidades.administrador.model import Administrador

    @login_manager.user_loader
    def carregar_administrador(id):
        return db.session.get(Administrador, int(id))
        
    from app.autenticacao.routes import autenticacao
    app.register_blueprint(autenticacao)

    return app