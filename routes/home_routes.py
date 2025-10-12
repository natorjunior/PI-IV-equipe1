from flask import Blueprint, request, jsonify
from database import db
from models import Postagem, Sala

home_bp = Blueprint('home', __name__)

# Criar uma postagem
@home_bp.route("/postagem", methods=["POST"])
def criar_postagem():
    data = request.json
    nova = Postagem(conteudo=data["conteudo"], usuario_id=data["usuario_id"])
    db.session.add(nova)
    db.session.commit()
    return jsonify({"message": "Postagem criada com sucesso"}), 201

# Curtir uma postagem
@home_bp.route("/postagem/<int:id>/curtir", methods=["PUT"])
def curtir_postagem(id):
    post = Postagem.query.get_or_404(id)
    post.curtidas += 1
    db.session.commit()
    return jsonify({"message": "Postagem curtida!"}), 200

# Criar sala (pública ou privada)
@home_bp.route("/sala", methods=["POST"])
def criar_sala():
    data = request.json
    sala = Sala(nome=data["nome"], tipo=data["tipo"], criador_id=data["criador_id"])
    db.session.add(sala)
    db.session.commit()
    return jsonify({"message": "Sala criada com sucesso"}), 201

# Excluir postagem
@home_bp.route("/postagem/<int:id>", methods=["DELETE"])
def excluir_postagem(id):
    post = Postagem.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Postagem excluída com sucesso"}), 200
