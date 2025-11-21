from flask import Blueprint, request, jsonify

# Define o Blueprint. No app.py, ele deve ser registrado com url_prefix='/api/posts'
post_bp = Blueprint('post_bp', __name__)

# --- SIMULAÇÃO DE BANCO DE DADOS (Lista em memória) ---
# Nota: Futuramente, você vai substituir isso pelas chamadas ao 'models.py' e 'database.py'
POSTS = [
    {
        'id': 1,
        'username': 'Amigo_Tech',
        'content': 'Adorei o novo design! Estrutura modular é outro nível.',
        'timestamp': 'há 2 horas',
        'avatar': 'https://iplaceholder.com/40x40/FF00FF/FFFFFF?text=A',
        'likes': 12,
        'can_delete': False,
        'liked': False
    },
    {
        'id': 2,
        'username': 'Usuário Exemplo',
        'content': 'Olá, mundo! Testando a API na estrutura real.',
        'timestamp': 'há 5 minutos',
        'avatar': 'https://iplaceholder.com/40x40/FF00FF/FFFFFF?text=U',
        'likes': 0,
        'can_delete': True,
        'liked': False
    }
]
next_post_id = 3

# ROTA GET: Pega todos os posts
@post_bp.route('/', methods=['GET'])
def get_posts():
    return jsonify(POSTS)

# ROTA POST: Cria novo post
@post_bp.route('/', methods=['POST'])
def create_post():
    global next_post_id
    global POSTS
    
    data = request.get_json()
    
    if data is None:
        return jsonify({'error': 'JSON inválido'}), 415 

    content = data.get('content')
    if not content or content.strip() == "":
        return jsonify({'error': 'Conteúdo vazio'}), 400

    new_post = {
        'id': next_post_id,
        'username': 'Usuário Logado', 
        'content': content,
        'timestamp': 'agora',
        'avatar': 'https://iplaceholder.com/40x40/FF00FF/FFFFFF?text=L',
        'likes': 0,
        'can_delete': True,
        'liked': False
    }
    
    POSTS.insert(0, new_post)
    next_post_id += 1
    
    return jsonify(new_post), 201

# ROTA DELETE: Apaga post por ID
@post_bp.route('/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global POSTS
    
    post_index = next((i for i, post in enumerate(POSTS) if post['id'] == post_id), None)
    
    if post_index is None:
        return jsonify({'error': 'Não encontrado'}), 404
    
    del POSTS[post_index]
    

    return '', 204
