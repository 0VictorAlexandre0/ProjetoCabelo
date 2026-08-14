from flask import Blueprint, request, render_template
from app.entidades.administrador.model import Administrador
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
            return f"Login realizado com sucesso! Bem-vindo, {administrador.nome}"
            
        return "Senha incorreta"
    
    return render_template("login.html")

@autenticacao.route("/dashboard")
@login_required
def dashboard():
    return "Dashboard - acesso permitido"

@autenticacao.route("/logout")
@login_required
def logout():
    logout_user()
    return "Logout realizado com sucesso"