from app import db

class Servicos(db.Model):

    __tablename__ = "servicos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    duracao = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Numeric(10,2), nullable=False)