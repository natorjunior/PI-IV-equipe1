from flask import Flask, send_from_directory
from flask_cors import CORS
from database import db
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.home_routes import home_bp
from routes.chat_routes import chat_bp
from routes.post_routes import post_bp
from routes.search_routes import search_bp

app = Flask(__name__, static_folder='static')
# Durante desenvolvimento, liberar CORS para facilitar chamadas do frontend.
# Em produção, restrinja para os domínios necessários.
CORS(app)  # permite todas as origens
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mentor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# Registrar blueprints da API normalmente
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(home_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(post_bp)
app.register_blueprint(search_bp)

# Rotas estáticas para servir frontend
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/home')
def serve_home():
    return send_from_directory(app.static_folder, 'home.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=5001, debug=True)