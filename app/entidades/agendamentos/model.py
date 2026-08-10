from app import db
from enum import Enum

class StatusAgendamento(Enum):
    AGENDADO = "Agendado"
    CONCLUIDO = "Concluído"
    CANCELADO = "Cancelado"

class Agendamentos(db.Model):
    
    __tablename__ = "agendamentos"

    id = db.Column(db.Integer, primary_key=True)

    clientes_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)

    profissionais_id = db.Column(db.Integer, db.ForeignKey("profissionais.id"), nullable=False)

    servicos_id = db.Column(db.Integer, db.ForeignKey("servicos.id"), nullable=False)

    data = db.Column(db.Date, nullable=False)

    hora = db.Column(db.Time, nullable=False)

    status = db.Column(db.Enum(StatusAgendamento), nullable=False)
