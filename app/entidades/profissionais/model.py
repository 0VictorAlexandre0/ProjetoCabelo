from app import db

profissionais_servicos = db.Table(
    "profissionais_servicos",
    db.Column("profissional_id", db.Integer, db.ForeignKey("profissionais.id"), primary_key=True),
    db.Column("servico_id", db.Integer, db.ForeignKey("servicos.id"), primary_key=True)
)


class Profissionais(db.Model):

    __tablename__ = "profissionais"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

    servicos = db.relationship(
        "Servicos",
        secondary=profissionais_servicos,
        back_populates="profissionais"
    )