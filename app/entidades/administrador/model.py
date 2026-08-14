from app import db
from flask_login import UserMixin

class Administrador(db.Model, UserMixin):

    __tablename__ = "administrador"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
