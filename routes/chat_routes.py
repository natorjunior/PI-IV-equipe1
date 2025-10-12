from flask import Blueprint, request, jsonify
from database import db
from models import Mensagem

chat_bp = Blueprint('chat', __name__)

# Enviar mensagem no chat
@chat_bp.route("/mensagem", methods=["POST"])
def enviar_mensagem():
    data = request.json
    msg = Mensagem(conteudo=data["conteudo"], sala_id=data["sala_id"], usuario_id=data["usuario_id"])
    db.session.add(msg)
    db.session.commit()
    return jsonify({"message": "Mensagem enviada"}), 201

# Enviar convite (simulação simples provavelmente nao funcionando)
@chat_bp.route("/convite", methods=["POST"])
def enviar_convite():
    data = request.json
    return jsonify({"message": f"Convite enviado para {data['email_destinatario']}!"}), 200
