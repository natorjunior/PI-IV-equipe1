from flask import Flask
from models import db
from routes import init_routes

def create_app():
    app = Flask(__name__)

    # Configuração do banco (daniel faça as alterações)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa banco
    db.init_app(app)

    with app.app_context():
        db.create_all()  # cria tabelas se não existirem

    # Carrega rotas
    init_routes(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
