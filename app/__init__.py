from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def criar_app():
    app = Flask(__name__)

    @app.route("/")
    def inicio():
        return redirect(url_for("autenticacao.login"))

    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from app import entidades 

    from app.entidades.administrador.model import Administrador

    @login_manager.user_loader
    def carregar_administrador(id):
        return db.session.get(Administrador, int(id))
        
    from app.autenticacao.routes import autenticacao
    from app.entidades.clientes.routes import clientes
    from app.entidades.profissionais.routes import profissionais
    from app.entidades.servicos.routes import servicos
    from app.entidades.agendamentos.routes import agendamentos
    
    app.register_blueprint(autenticacao)
    app.register_blueprint(clientes)
    app.register_blueprint(profissionais)
    app.register_blueprint(servicos)
    app.register_blueprint(agendamentos)

    return app