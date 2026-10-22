from flask import Blueprint, render_template
from app.entidades.clientes.model import Clientes
from flask_login import login_required

clientes = Blueprint("clientes", __name__)

@clientes.route("/clientes")
@login_required
def listar_clientes():

    clientes = Clientes.query.all()

    return render_template("clientes/index.html", clientes=clientes)