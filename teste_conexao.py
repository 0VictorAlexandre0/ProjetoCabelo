from app import criar_app, db

app = criar_app()

with app.app_context():
    try:
        db.engine.connect()
        print("Conectado ao PostgreSQL com sucesso!")
    except Exception as e:
        print("Erro na conexão:")
        print(e)