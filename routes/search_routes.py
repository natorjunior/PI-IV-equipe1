from flask import Blueprint, request, jsonify
from models import Usuario, Postagem

search_bp = Blueprint('search', __name__)

# Buscar por nome ou palavra
@search_bp.route("/buscar", methods=["GET"])
def buscar():
    termo = request.args.get("q", "")
    usuarios = Usuario.query.filter(Usuario.nome_usuario.contains(termo)).all()
    postagens = Postagem.query.filter(Postagem.conteudo.contains(termo)).all()
    return jsonify({
        "usuarios": [u.nome_usuario for u in usuarios],
        "postagens": [p.conteudo for p in postagens]
    })

# Retornar à tela inicial (menu > home)
@search_bp.route("/home", methods=["GET"])
def home():
    return jsonify({"message": "Você está na tela principal (Home)!"})
