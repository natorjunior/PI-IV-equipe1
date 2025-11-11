from flask import Blueprint, request, jsonify
from models import Postagem, Usuario
from database import db

post_bp = Blueprint("post", __name__)

@post_bp.route("/postar", methods=["POST"])
def postar():
    data = request.get_json()
    conteudo = data.get("conteudo")
    usuario_id = data.get("usuario_id")
    imagem_url = data.get("imagem_url")  # URL da imagem (opcional)

    if not conteudo or not usuario_id:
        return jsonify({"message": "Conteúdo e usuário são obrigatórios"}), 400

    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({"message": "Usuário não encontrado"}), 404

    nova_postagem = Postagem(
        conteudo=conteudo, 
        usuario_id=usuario_id,
        imagem_url=imagem_url
    )
    db.session.add(nova_postagem)
    db.session.commit()

    return jsonify({"message": "Postagem criada com sucesso!"}), 201

@post_bp.route("/postagens", methods=["GET"])
def listar_postagens():
    """Lista todas as postagens"""
    postagens = Postagem.query.all()
    return jsonify({
        "postagens": [{
            "id": p.id,
            "conteudo": p.conteudo,
            "imagem_url": p.imagem_url,
            "curtidas": p.curtidas,
            "usuario_id": p.usuario_id,
            "autor": p.autor.nome_usuario if p.autor else None
        } for p in postagens]
    }), 200
