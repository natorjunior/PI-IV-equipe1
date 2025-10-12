from flask import Flask
from flask_cors import CORS
from database import db
from routes.auth_routes import auth_bp
from routes.home_routes import home_bp
from routes.user_routes import user_bp
from routes.chat_routes import chat_bp
from routes.search_routes import search_bp

app = Flask(__name__)
CORS(app)

# Configuração do banco para mecher (nao ta pronto)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Registro das rotas
app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(user_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(search_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
