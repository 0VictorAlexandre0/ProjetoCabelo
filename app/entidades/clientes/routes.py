from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.entidades.clientes.model import Clientes
from flask_login import login_required
from app.entidades.agendamentos.model import Agendamentos


clientes = Blueprint("clientes", __name__)

@clientes.route("/clientes")
@login_required
def listar_clientes():
    busca = request.args.get("busca", "").strip()

    consulta = Clientes.query

    if busca:
        consulta = consulta.filter(
            Clientes.nome.ilike(f"%{busca}%")
        )
    
    clientes = consulta.all()
    
    return render_template(
        "clientes/index.html",
        clientes = clientes,
        busca=busca
    )

@clientes.route("/clientes/novo", methods=["GET", "POST"])
@login_required
def novo_cliente():
    if request.method == "POST":
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        email = request.form.get("email")

        cliente = Clientes(
            nome = nome,
            telefone = telefone,
            email = email
        )

        db.session.add(cliente)
        db.session.commit()

        return redirect(url_for("clientes.listar_clientes"))
    
    return render_template("clientes/novo.html")


@clientes.route("/clientes/editar/<int:id>", methods= ["GET", "POST"])
@login_required
def editar_cliente(id):
    cliente = Clientes.query.get_or_404(id)

    if request.method == "POST":
        cliente.nome = request.form.get("nome")
        cliente.telefone = request.form.get("telefone")
        cliente.email = request.form.get("email")

        db.session.commit()

        return redirect(url_for("clientes.listar_clientes"))
    
    return render_template("clientes/editar.html", cliente=cliente)


@clientes.route("/clientes/excluir/<int:id>", methods=["POST"])
@login_required
def excluir_cliente(id):
    cliente = Clientes.query.get_or_404(id)

    agendamentos = Agendamentos.query.filter_by(
        clientes_id=cliente.id
    ).first()

    if agendamentos:
        return(
            "Não é possível excluir este cliente, pois ele possui "
            "agendamentos vinculados.", 400
        )

    db.session.delete(cliente)
    db.session.commit()

    return redirect(url_for("clientes.listar_clientes"))