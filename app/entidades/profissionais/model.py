from app import db

class Profissionais(db.Model):

    __tablename__ = "profissionais"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)