from flask import Blueprint, request, jsonify, render_template
from flask_login import current_user
from models import Mensagem, Sala, Usuario
from database import db
from auth_utils import login_required_api

chat_bp = Blueprint('chat_bp', __name__)

# --- ROTAS DE TELA (HTML) ---

# Tela de Visualizar Salas (Acessada pelo menu "Salas")
@chat_bp.route('/salas')
def list_rooms_page():
    return render_template('salas.html')

# Tela de Criar Sala (Acessada pelos botões da Home)
@chat_bp.route('/salas/criar')
def create_room_page():
    return render_template('criar_sala.html')


@chat_bp.route('/api/rooms', methods=['GET'])
@login_required_api
def get_rooms():
    """Lista todas as salas do banco de dados"""
    salas = Sala.query.order_by(Sala.created_at.desc()).all()
    return jsonify([sala.to_dict() for sala in salas])

# Cria uma nova sala
@chat_bp.route('/api/rooms', methods=['POST'])
@login_required_api
def create_room():
    data = request.get_json()
    
    name = data.get('name')
    room_type = data.get('type') # 'public' ou 'private'
    password = data.get('password', '')
    objective = data.get('objective')

    if not name or not objective:
        return jsonify({'error': 'Nome e Objetivo são obrigatórios'}), 400

    # Se for privada, exige senha
    if room_type == 'private' and not password:
        return jsonify({'error': 'Salas privadas precisam de senha'}), 400

    try:
        nova_sala = Sala(
            name=name,
            type=room_type,
            password=password if room_type == 'private' else None,
            objective=objective,
            created_by=current_user.id
        )
        
        db.session.add(nova_sala)
        db.session.commit()
        
        return jsonify(nova_sala.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao criar sala: {str(e)}'}), 500


@chat_bp.route('/api/rooms/join', methods=['POST'])
def join_room():
    data = request.get_json()
    room_id = int(data.get('room_id'))
    password_attempt = data.get('password', '')

    # Procura a sala no banco de dados
    sala = Sala.query.get(room_id)
    
    if not sala:
        return jsonify({'error': 'Sala não encontrada'}), 404

    if sala.type == 'private':
        if sala.password != password_attempt:
            return jsonify({'success': False, 'error': 'Senha incorreta!'}), 401
    
    return jsonify({'success': True, 'message': 'Entrou na sala!'}), 200

@chat_bp.route('/chat/<int:room_id>')
def chat_page(room_id):
    # Busca as informações da sala do banco de dados
    sala = Sala.query.get(room_id)
    
    if not sala:
        return "Sala não encontrada", 404
        
    return render_template('chat.html', room=sala.to_dict())

# --- SISTEMA DE MENSAGENS ---


@chat_bp.route('/api/chat/<int:room_id>/messages', methods=['POST'])
@login_required_api
def send_message(room_id):
    # Verifica se a sala existe
    sala = Sala.query.get(room_id)
    if not sala:
        return jsonify({'error': 'Sala não encontrada'}), 404
    
    data = request.get_json()
    text = data.get('text')
    # Usa o nome do usuário autenticado da sessão
    username = current_user.nome_usuario
    
    if not text:
        return jsonify({'error': 'Mensagem vazia'}), 400

    new_msg = Mensagem(
        room_id=room_id,
        user=username,
        text=text
    )
    
    db.session.add(new_msg)
    db.session.commit()
    
    return jsonify(new_msg.to_dict()), 201

# Ler mensagens da sala
@chat_bp.route('/api/chat/<int:room_id>/messages', methods=['GET'])
@login_required_api
def get_messages(room_id):
    # Busca no Banco de Dados filtrando pela sala
    messages_db = Mensagem.query.filter_by(room_id=room_id).order_by(Mensagem.timestamp).all()
    

    messages_list = [msg.to_dict() for msg in messages_db]
    
    return jsonify(messages_list)

# --- EXCLUIR SALA ---

@chat_bp.route('/api/rooms/<int:room_id>', methods=['DELETE'])
@login_required_api
def delete_room(room_id):
    """Exclui uma sala e todas as mensagens associadas a ela"""
    
    sala = Sala.query.get(room_id)
    
    if not sala:
        return jsonify({'error': 'Sala não encontrada'}), 404
    
    # Verifica se o usuário é o criador da sala
    if sala.created_by != current_user.id:
        return jsonify({'error': 'Você não tem permissão para excluir esta sala'}), 403
    
    try:
        # Deleta a sala (mensagens são deletadas automaticamente por cascade)
        db.session.delete(sala)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Sala excluída com sucesso!'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao excluir sala: {str(e)}'}), 500