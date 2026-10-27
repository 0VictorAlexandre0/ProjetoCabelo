from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app import db
from app.entidades.servicos.model import Servicos
from app.entidades.agendamentos.model import Agendamentos

servicos = Blueprint("servicos", __name__)

@servicos.route("/servicos")
@login_required
def listar_servicos():
    busca = request.args.get("busca", "").strip()

    consulta = Servicos.query

    if busca:
        consulta = consulta.filter(
            Servicos.nome.ilike(f"%{busca}%")
        )

    servicos = consulta.all()

    return render_template("servicos/index.html", servicos=servicos, busca=busca)


@servicos.route("/servicos/novo", methods=["GET", "POST"])
@login_required
def novo_servico():
    if request.method == "POST":
        nome = request.form.get("nome")
        duracao = request.form.get("duracao")
        preco = request.form.get("preco")

        servico = Servicos(nome=nome, duracao=duracao, preco=preco)
        
        db.session.add(servico)
        db.session.commit()

        return redirect(url_for("servicos.listar_servicos"))
    
    return render_template("servicos/novo.html")


@servicos.route("/servicos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_servico(id):
    servico = Servicos.query.get_or_404(id)

    if request.method == "POST":
        servico.nome = request.form.get("nome")
        servico.duracao = request.form.get("duracao")
        servico.preco = request.form.get("preco")

        db.session.commit()

        return redirect(url_for("servicos.listar_servicos"))
    
    return render_template("servicos/editar.html", servico=servico)


@servicos.route("/servicos/excluir/<int:id>", methods=["POST"])
@login_required
def excluir_servico(id):
    servico = Servicos.query.get_or_404(id)

    agendamentos = Agendamentos.query.filter_by(servicos_id=servico.id).first()

    if agendamentos:
        return(
            "Não é possível excluir este serviço, "
            "pois ele possui agendamentos vinculados.",
            400
        )
    
    db.session.delete(servico)
    db.session.commit()

    return redirect(url_for("servicos.listar_servicos"))
