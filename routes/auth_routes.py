from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models import Usuario

auth_bp = Blueprint('auth', __name__)

# Login de usuario
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = Usuario.query.filter_by(email=data.get("email")).first()
    if user and check_password_hash(user.senha, data.get("senha")):
        return jsonify({"message": "Login realizado com sucesso", "id": user.id}), 200
    return jsonify({"message": "Credenciais inválidas"}), 401

# Cadastro de usuario
@auth_bp.route("/cadastro", methods=["POST"])
def cadastro():
    data = request.json
    senha_hash = generate_password_hash(data.get("senha"))
    novo_user = Usuario(
        nome_usuario=data.get("nome_usuario"),
        email=data.get("email"),
        senha=senha_hash
    )
    db.session.add(novo_user)
    db.session.commit()
    return jsonify({"message": "Usuário cadastrado com sucesso"}), 201