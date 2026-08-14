from werkzeug.security import generate_password_hash, check_password_hash

def gerar_hash_senha(senha):
    return generate_password_hash(senha)

def verificar_hash_senha(senha, senha_hash):
    return check_password_hash(senha_hash, senha)