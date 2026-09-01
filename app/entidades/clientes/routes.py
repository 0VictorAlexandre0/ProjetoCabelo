from flask import Blueprint, render_template
from app.entidades.clientes.model import Clientes

clientes = Blueprint("clientes", __name__)

@clientes.route("/clientes")
def listar_clientes():

    clientes = Clientes.query.all()

    return render_template("clientes/index.html", clientes=clientes)