from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

POSTS = [
    {
        'id': 1,
        'username': 'Amigo_Tech',
        'content': 'Adorei o novo design! As salas parecem ser uma ótima maneira de organizar grupos de estudo.',
        'timestamp': 'há 2 horas',
        'avatar': 'https://via.placeholder.com/40/28a745/ffffff?text=A',
        'likes': 12,
        'can_delete': False,
        'liked': False
    },
    {
        'id': 2,
        'username': 'Usuário Exemplo',
        'content': 'Olá, mundo! Base para o nosso projeto de rede social!',
        'timestamp': 'há 5 minutos',
        'avatar': 'https://via.placeholder.com/40/007bff/ffffff?text=U',
        'likes': 0,
        'can_delete': True,
        'liked': False
    }
]
next_post_id = 3

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)

@app.route('/api/posts', methods=['POST'])
def create_post():
    global next_post_id
    global POSTS 
    
    data = request.get_json()
    
    if data is None:
        return jsonify({'error': 'JSON malformado ou ausente no corpo da requisição.'}), 415 

    content = data.get('content')
    if not content or content.strip() == "":
        return jsonify({'error': 'O campo "content" da postagem está vazio ou ausente.'}), 400

    new_post = {
        'id': next_post_id,
        'username': 'Usuário Logado', 
        'content': content,
        'timestamp': 'agora',
        'avatar': 'https://via.placeholder.com/40/FF00FF/ffffff?text=L',
        'likes': 0,
        'can_delete': True,
        'liked': False
    }
    
    POSTS.insert(0, new_post)
    next_post_id += 1
    
    return jsonify(new_post), 201

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global POSTS
    
    post_index = next((i for i, post in enumerate(POSTS) if post['id'] == post_id), None)
    
    if post_index is None:
        return jsonify({'error': 'Postagem não encontrada.'}), 404
    
    del POSTS[post_index]
    
    return '', 204 

if __name__ == '__main__':
    print("Iniciando o servidor Flask. Acesse http://127.0.0.1:5000/")
    app.run(debug=True)