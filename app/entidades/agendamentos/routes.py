from datetime import date, time, datetime
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

from app import db
from app.entidades.agendamentos.model import Agendamentos, StatusAgendamento
from app.entidades.clientes.model import Clientes
from app.entidades.profissionais.model import Profissionais
from app.entidades.servicos.model import Servicos


agendamentos = Blueprint("agendamentos", __name__)

@agendamentos.route("/agendamentos")
@login_required
def listar_agendamentos():
    lista = (
        db.session.query(
            Agendamentos,
            Clientes.nome,
            Profissionais.nome,
            Servicos.nome
        )
        .join(Clientes, Agendamentos.clientes_id == Clientes.id)
        .join(Profissionais, Agendamentos.profissionais_id == Profissionais.id)
        .join(Servicos, Agendamentos.servicos_id == Servicos.id)
        .order_by(Agendamentos.data, Agendamentos.hora)
        .all()
    )

    return render_template("agendamentos/index.html", agendamentos=lista)


@agendamentos.route("/agendamentos/novo", methods=["GET", "POST"])
@login_required
def novo_agendamento():
    clientes = Clientes.query.order_by(Clientes.nome).all()
    profissionais = Profissionais.query.order_by(Profissionais.nome).all()
    servicos = Servicos.query.order_by(Servicos.nome).all()

    if request.method == "POST":
        cliente_id = request.form.get("clientes_id", type=int)
        profissional_id = request.form.get("profissionais_id", type=int)
        servico_id = request.form.get("servicos_id", type=int)
        data_informada = request.form.get("data")
        hora_informada = request.form.get("hora")
        status_informado = request.form.get("status")

        cliente = db.session.get(Clientes, cliente_id)
        profissional = db.session.get(Profissionais, profissional_id)
        servico = db.session.get(Servicos, servico_id)

        try:
            data_agendamento = date.fromisoformat(data_informada)
        except (ValueError, TypeError):
            data_agendamento = None

        status_agendamento = next((status for status in StatusAgendamento if status.name == status_informado), None)

        if not cliente or not profissional or not servico:
            return(
                "Selecione um cliente, profissional e serviço válidos", 400
            )
        
        if not data_agendamento or not hora_informada or not status_agendamento:
            return(
                "Informe uma data, hora e status válidos", 400
            )
        
        try:
            hora_agendamento = time.fromisoformat(hora_informada)
        except (ValueError, TypeError):
            return "Informe uma hora válida.", 400

        if data_agendamento < date.today():
            return "Não é possível agendar em uma data passada.", 400

        if datetime.combine(data_agendamento, hora_agendamento) <= datetime.now():
            return "Não é possível agendar em um horário que já passou.", 400
        
        novo = Agendamentos(
            clientes_id = cliente.id,
            profissionais_id = profissional.id,
            servicos_id = servico.id,
            data = data_agendamento,
            hora = hora_agendamento,
            status = status_agendamento
        )

        db.session.add(novo)
        db.session.commit()

        return redirect(url_for("agendamentos.listar_agendamentos"))
    
    return render_template(
        "agendamentos/novo.html",
        clientes = clientes,
        profissionais = profissionais,
        servicos = servicos,
        status_agendamentos = StatusAgendamento,
        hoje=date.today().isoformat()
    )


@agendamentos.route("/agendamentos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_agendamento(id):
    agendamento = db.session.get(Agendamentos, id)

    if not agendamento:
        return "Agendamento não encontrado.", 404

    clientes = Clientes.query.order_by(Clientes.nome).all()
    profissionais = Profissionais.query.order_by(Profissionais.nome).all()
    servicos = Servicos.query.order_by(Servicos.nome).all()

    if request.method == "POST":
        status_informado = request.form.get("status")

        status_agendamento = next(
            (status for status in StatusAgendamento if status.name == status_informado),
            None
        )

        if not status_agendamento:
            return "Informe um status válido.", 400

        if agendamento.data < date.today() or (
            agendamento.data == date.today()
            and datetime.combine(agendamento.data, agendamento.hora) <= datetime.now()
        ):
            agendamento.status = status_agendamento
            db.session.commit()

            return redirect(url_for("agendamentos.listar_agendamentos"))

        cliente_id = request.form.get("clientes_id", type=int)
        profissional_id = request.form.get("profissionais_id", type=int)
        servico_id = request.form.get("servicos_id", type=int)
        data_informada = request.form.get("data")
        hora_informada = request.form.get("hora")

        cliente = db.session.get(Clientes, cliente_id)
        profissional = db.session.get(Profissionais, profissional_id)
        servico = db.session.get(Servicos, servico_id)

        try:
            data_agendamento = date.fromisoformat(data_informada)
            hora_agendamento = time.fromisoformat(hora_informada)
        except (ValueError, TypeError):
            return "Informe uma data e hora válidas.", 400

        if not cliente or not profissional or not servico:
            return "Selecione dados válidos para o agendamento.", 400

        if data_agendamento < date.today():
            return render_template(
                "agendamentos/editar.html",
                agendamento=agendamento,
                clientes=clientes,
                profissionais=profissionais,
                servicos=servicos,
                status_agendamentos=StatusAgendamento,
                hoje=date.today(),
                erro_data="Não é possível alterar o agendamento para uma data passada."
            )

        if datetime.combine(data_agendamento, hora_agendamento) <= datetime.now():
            return render_template(
                "agendamentos/editar.html",
                agendamento=agendamento,
                clientes=clientes,
                profissionais=profissionais,
                servicos=servicos,
                status_agendamentos=StatusAgendamento,
                hoje=date.today(),
                erro_hora="Não é possível alterar o agendamento para um horário que já passou."
            )

        agendamento.clientes_id = cliente.id
        agendamento.profissionais_id = profissional.id
        agendamento.servicos_id = servico.id
        agendamento.data = data_agendamento
        agendamento.hora = hora_agendamento
        agendamento.status = status_agendamento

        db.session.commit()

        return redirect(url_for("agendamentos.listar_agendamentos"))

    return render_template(
        "agendamentos/editar.html",
        agendamento=agendamento,
        clientes=clientes,
        profissionais=profissionais,
        servicos=servicos,
        status_agendamentos=StatusAgendamento,
        hoje=date.today()
    )


@agendamentos.route("/agendamentos/excluir/<int:id>", methods=["GET", "POST"])
@login_required
def excluir_agendamento(id):
    agendamento = db.session.get(Agendamentos, id)

    if not agendamento:
        return "Agendamento não encontrado.", 404

    if request.method == "POST":
        db.session.delete(agendamento)
        db.session.commit()

        return redirect(url_for("agendamentos.listar_agendamentos"))

    cliente = db.session.get(Clientes, agendamento.clientes_id)
    profissional = db.session.get(Profissionais, agendamento.profissionais_id)
    servico = db.session.get(Servicos, agendamento.servicos_id)

    return render_template(
        "agendamentos/excluir.html",
        agendamento=agendamento,
        cliente=cliente,
        profissional=profissional,
        servico=servico
    )
