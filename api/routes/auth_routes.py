from flask import Blueprint, request, jsonify, session, current_app
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash 
from models import Usuario
from auth_utils import get_current_user_data

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"message": "Email e senha são obrigatórios"}), 400

    usuario = Usuario.query.filter_by(email=email).first()

    # Compara a senha fornecida com o hash armazenado
    if not usuario or not check_password_hash(usuario.senha, senha):
        return jsonify({"message": "Credenciais inválidas"}), 401

    # Faz login do usuário usando Flask-Login
    login_user(usuario, remember=True)
    
    return jsonify({
        "message": "Login realizado com sucesso!",
        "id": usuario.id,
        "nome_usuario": usuario.nome_usuario,
        "authenticated": True
    }), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():
    """
    Realiza logout do usuário e limpa a sessão
    """
    logout_user()
    session.clear()
    # Remove cookies de sessão e de remember (Flask-Login)
    resp = jsonify({"message": "Logout realizado com sucesso"})
    cookie_name = current_app.config.get('SESSION_COOKIE_NAME', 'session')
    resp.delete_cookie(cookie_name, path='/')
    resp.delete_cookie('remember_token', path='/')
    return resp, 200

@auth_bp.route("/check-auth", methods=["GET"])
def check_auth():
    """
    Verifica se o usuário está autenticado
    """
    return jsonify(get_current_user_data()), 200