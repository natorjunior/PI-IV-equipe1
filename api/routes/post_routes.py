from flask import Blueprint, request, jsonify, current_app
from flask_login import current_user
from models import Postagem, Usuario
from database import db
from datetime import datetime
from auth_utils import login_required_api
from werkzeug.utils import secure_filename
import os

post_bp = Blueprint('post_bp', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- ROTA GET: Pega todos os posts ---
@post_bp.route('/', methods=['GET'])
@post_bp.route('', methods=['GET'], strict_slashes=False)
@login_required_api
def get_posts():
    posts_db = Postagem.query.order_by(Postagem.id.desc()).all()
    
    posts_list = []
    for p in posts_db:
        autor_nome = p.autor.nome_usuario if p.autor else "Desconhecido"
        
        # Verifica se o post tem data, senão põe string vazia
        data_formatada = p.criado_em.strftime("%d/%m %H:%M") if p.criado_em else ""

        posts_list.append({
            'id': p.id,
            'username': autor_nome,
            'content': p.conteudo if p.conteudo else "Conteúdo indisponível", 
            'image_url': p.imagem_url,
            'timestamp': data_formatada,
            'avatar': "", 
            'likes': p.curtidas,
            # Só pode deletar se for o dono do post
            'can_delete': (p.usuario_id == current_user.id),
            'liked_by': [u.nome_usuario for u in p.quem_curtiu] 
        })
        
    return jsonify(posts_list)

# --- ROTA POST: Cria novo post ---
@post_bp.route('/', methods=['POST'])
@post_bp.route('', methods=['POST'], strict_slashes=False)
@login_required_api
def create_post():
    content = request.form.get('content')
    image_file = request.files.get('image')

    if not content:
        return jsonify({'error': 'Conteúdo vazio'}), 400

    usuario = current_user
    image_url = None
    
    # Se tem imagem, salva
    if image_file and image_file.filename and allowed_file(image_file.filename):
        filename = secure_filename(f"{usuario.id}_{datetime.now().timestamp()}_{image_file.filename}")
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        image_file.save(filepath)
        image_url = f"/static/uploads/{filename}"
    
    new_post = Postagem(
        conteudo=content,
        usuario_id=usuario.id,
        imagem_url=image_url,
        curtidas=0
    )
    
    db.session.add(new_post)
    db.session.commit()
    
    return jsonify({
        'id': new_post.id,
        'username': usuario.nome_usuario,
        'content': new_post.conteudo,
        'image_url': image_url,
        'timestamp': 'Agora',
        'avatar': '',
        'likes': 0,
        'can_delete': True,
        'liked_by': []
    }), 201

# --- ROTA DELETE ---
@post_bp.route('/<int:post_id>', methods=['DELETE'])
@post_bp.route('/<int:post_id>', methods=['DELETE'], strict_slashes=False)
@login_required_api
def delete_post(post_id):
    post = Postagem.query.get(post_id)
    
    if not post:
        return jsonify({'error': 'Não encontrado'}), 404
    
    # Verifica se o usuário é o dono do post
    if post.usuario_id != current_user.id:
        return jsonify({'error': 'Não autorizado'}), 403
    
    db.session.delete(post)
    db.session.commit()
    
    return '', 204

# --- ROTA CURTIR (CORRIGIDA) ---
@post_bp.route('/<int:post_id>/like', methods=['POST'])
@post_bp.route('/<int:post_id>/like', methods=['POST'], strict_slashes=False)
@login_required_api
def like_post(post_id):
    # Usa o usuário autenticado da sessão
    usuario = current_user

    post = Postagem.query.get(post_id)

    if not post:
        return jsonify({'error': 'Post não encontrado'}), 404
    
    # Atualizar o contador físico E a relação
    if usuario in post.quem_curtiu:
        post.quem_curtiu.remove(usuario)
        post.curtidas = max(0, post.curtidas - 1)
        action = 'unliked'
    else:
        post.quem_curtiu.append(usuario)
        post.curtidas += 1
        action = 'liked'

    db.session.commit()
    
    return jsonify({
        'likes': post.curtidas,
        'action': action
    }), 200