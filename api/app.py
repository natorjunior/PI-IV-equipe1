import os
from flask import Flask, render_template
from flask_cors import CORS
from flask_login import LoginManager
from flask_session import Session
from database import db
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.home_routes import home_bp
from routes.chat_routes import chat_bp
from routes.post_routes import post_bp
from routes.search_routes import search_bp

app = Flask(__name__, static_folder='static', template_folder='templates')

# Configuração de segurança
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuração de uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Configuração de sessão
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = True  # exige HTTPS para enviar cookie
app.config['PREFERRED_URL_SCHEME'] = 'https'

Session(app)

# CORS configurado para aceitar credenciais
CORS(app, supports_credentials=True, origins=[
    'http://localhost:5001',
    'http://127.0.0.1:5001',
    'https://mentor.acilab.com.br',
    'http://mentor.acilab.com.br'
])


# Configuração do banco de dados MySQL
env_db_url = os.environ.get('DATABASE_URL')
env_db_host = os.environ.get('DATABASE_HOST') or os.environ.get('DB_HOST')

if env_db_url:
    db_uri = env_db_url
elif env_db_host:
    user = os.environ.get('DATABASE_USER') or os.environ.get('DB_USER', 'root')
    password = os.environ.get('DATABASE_PASSWORD') or os.environ.get('DB_PASS', 'password')
    port = os.environ.get('DATABASE_PORT') or os.environ.get('DB_PORT', '3306')
    name = os.environ.get('DATABASE_NAME') or os.environ.get('DB_NAME', 'mentor')
    
    db_uri = f'mysql+pymysql://{user}:{password}@{env_db_host}:{port}/{name}'
    print(f"Usando MySQL em: {env_db_host}:{port}/{name}")
else:
    # Fallback para desenvolvimento local com MySQL
    db_uri = 'mysql+pymysql://root:root123@localhost:3306/mentor'
    print("Usando MySQL local (localhost:3306/mentor)")

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'

try:
    from models import Usuario, Postagem, Mensagem
except Exception as e:
    print(f"Aviso ao importar modelos: {e}")

# User loader para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from models import Usuario
    return Usuario.query.get(int(user_id))

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(home_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(post_bp, url_prefix='/api/posts')
app.register_blueprint(search_bp)

@app.route('/')
def serve_index():
    return render_template('index.html')

@app.route('/home')
def serve_home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(port=5001, debug=True)