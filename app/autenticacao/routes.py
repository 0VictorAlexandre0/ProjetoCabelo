from flask import Blueprint, request, render_template, redirect, url_for
from app.entidades.clientes.model import Clientes
from app.entidades.administrador.model import Administrador
from app.entidades.profissionais.model import Profissionais
from app.entidades.servicos.model import Servicos
from app.entidades.agendamentos.model import Agendamentos
from app.autenticacao.seguranca import verificar_hash_senha
from flask_login import login_user, login_required, logout_user

autenticacao = Blueprint("autenticacao", __name__)

@autenticacao.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        senha = request.form.get("senha")
        
        administrador = Administrador.query.filter_by(email=email).first()

        if not administrador:
            return "Administrador não encontrado"
        
        if verificar_hash_senha(senha, administrador.senha):
            login_user(administrador)
            return redirect(url_for("autenticacao.dashboard"))
            
        return "Senha incorreta"
    
    return render_template("login.html")

@autenticacao.route("/dashboard")
@login_required
def dashboard():

    total_clientes = Clientes.query.count()
    total_profissionais = Profissionais.query.count()
    total_servicos = Servicos.query.count()
    total_agendamentos = Agendamentos.query.count()

    return render_template("dashboard/index.html", total_clientes=total_clientes, total_profissionais=total_profissionais, total_servicos=total_servicos, total_agendamentos=total_agendamentos)
    

@autenticacao.route("/logout")
@login_required
def logout():
    logout_user() 
    return "Logout realizado com sucesso"