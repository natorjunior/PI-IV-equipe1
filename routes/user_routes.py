from flask import Blueprint, request, jsonify
from database import db
from models import Usuario
from werkzeug.security import generate_password_hash

user_bp = Blueprint('user', __name__)

# Editar perfil
@user_bp.route("/usuario/<int:id>", methods=["PUT"])
def editar_usuario(id):
    user = Usuario.query.get_or_404(id)
    data = request.json
    user.nome_usuario = data.get("nome_usuario", user.nome_usuario)
    user.email = data.get("email", user.email)
    if data.get("senha"):
        user.senha = generate_password_hash(data["senha"])
    db.session.commit()
    return jsonify({"message": "Perfil atualizado"}), 200

# Excluir conta
@user_bp.route("/usuario/<int:id>", methods=["DELETE"])
def excluir_usuario(id):
    user = Usuario.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Conta excluída com sucesso"}), 200
