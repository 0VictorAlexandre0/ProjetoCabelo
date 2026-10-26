from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app import db
from app.entidades.profissionais.model import Profissionais
from app.entidades.agendamentos.model import Agendamentos

profissionais = Blueprint('profissionais', __name__)

@profissionais.route("/profissionais")
@login_required
def listar_profissionais():
    busca = request.args.get("busca" , "").strip()

    consulta = Profissionais.query

    if busca:
        consulta = consulta.filter(
            Profissionais.nome.ilike(f"%{busca}%")
        )

    profissionais = consulta.all()

    return render_template('profissionais/index.html', profissionais=profissionais, busca=busca)


@profissionais.route('/profissionais/novo', methods=['GET', 'POST'])
@login_required
def novo_profissional():
    if request.method == "POST":
        nome = request.form.get("nome")
        especialidade = request.form.get("especialidade")
        telefone = request.form.get("telefone")

        profissional = Profissionais(
            nome = nome,
            especialidade = especialidade,
            telefone = telefone
        )

        db.session.add(profissional)
        db.session.commit()

        return redirect(url_for("profissionais.listar_profissionais"))
    
    return render_template("profissionais/novo.html")
    

@profissionais.route("/profissionais/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_profissional(id):
    profissional = Profissionais.query.get_or_404(id)

    if request.method == "POST":
        profissional.nome = request.form.get("nome")
        profissional.especialidade = request.form.get("especialidade")
        profissional.telefone = request.form.get("telefone")

        db.session.commit()

        return redirect(url_for("profissionais.listar_profissionais"))

    return render_template("profissionais/editar.html", profissional=profissional)


@profissionais.route("/profissionais/excluir/<int:id>", method=["POST"])
@login_required
def excluir_profissional(id):
    profissional = Profissionais.query.get_or_404(id)
    
    agendamentos = Agendamentos.query.filter_by(profissionais_id=profissional.id).first()

    if agendamentos:
        return(
            "Não é possível excluir este profissional, "
            "pois ele possui agendamentos vínculados.", 400 
        )

    db.session.delete(profissional)
    db.session.commit()

    return redirect(url_for("profissionais.listar_profissionais"))



































