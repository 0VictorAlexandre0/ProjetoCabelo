from app import db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)