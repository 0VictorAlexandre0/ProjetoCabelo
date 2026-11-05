from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app import db
from app.entidades.profissionais.model import Profissionais
from app.entidades.servicos.model import Servicos
from app.entidades.agendamentos.model import Agendamentos

profissionais = Blueprint('profissionais', __name__)

@profissionais.route("/profissionais")
@login_required
def listar_profissionais():
    busca = request.args.get("busca", "").strip()

    consulta = Profissionais.query

    if busca:
        consulta = consulta.filter(
            Profissionais.nome.ilike(f"%{busca}%")
        )

    profissionais = consulta.all()

    return render_template(
        'profissionais/index.html',
        profissionais=profissionais,
        busca=busca
    )


@profissionais.route('/profissionais/novo', methods=['GET', 'POST'])
@login_required
def novo_profissional():
    lista_servicos = Servicos.query.order_by(Servicos.nome).all()

    if request.method == "POST":
        ids_servicos = request.form.getlist("servicos")

        if not ids_servicos:
            return render_template(
                "profissionais/novo.html",
                servicos=lista_servicos,
                erro="Selecione pelo menos um serviço."
            )

        profissional = Profissionais(
            nome=request.form.get("nome"),
            especialidade=request.form.get("especialidade"),
            telefone=request.form.get("telefone"),
            servicos=Servicos.query.filter(
                Servicos.id.in_(ids_servicos)
            ).all()
        )

        db.session.add(profissional)
        db.session.commit()

        return redirect(url_for("profissionais.listar_profissionais"))

    return render_template(
        "profissionais/novo.html",
        servicos=lista_servicos
    )


@profissionais.route("/profissionais/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_profissional(id):
    profissional = Profissionais.query.get_or_404(id)
    lista_servicos = Servicos.query.order_by(Servicos.nome).all()

    if request.method == "POST":
        ids_servicos = request.form.getlist("servicos")

        if not ids_servicos:
            return render_template(
                "profissionais/editar.html",
                profissional=profissional,
                servicos=lista_servicos,
                erro="Selecione pelo menos um serviço."
            )

        profissional.nome = request.form.get("nome")
        profissional.especialidade = request.form.get("especialidade")
        profissional.telefone = request.form.get("telefone")
        profissional.servicos = Servicos.query.filter(
            Servicos.id.in_(ids_servicos)
        ).all()

        db.session.commit()

        return redirect(url_for("profissionais.listar_profissionais"))

    return render_template(
        "profissionais/editar.html",
        profissional=profissional,
        servicos=lista_servicos
    )


@profissionais.route("/profissionais/excluir/<int:id>", methods=["POST"])
@login_required
def excluir_profissional(id):
    profissional = Profissionais.query.get_or_404(id)

    agendamentos = Agendamentos.query.filter_by(
        profissionais_id=profissional.id
    ).first()

    if agendamentos:
        return (
            "Não é possível excluir este profissional, "
            "pois ele possui agendamentos vinculados.", 400
        )

    db.session.delete(profissional)
    db.session.commit()

    return redirect(url_for("profissionais.listar_profissionais"))





















