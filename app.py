from flask import request, jsonify
from models import db, User, Post, Room

def init_routes(app):

    # -------------------- REGISTRO --------------------
    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Usuário e senha são obrigatórios"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Usuário já existe"}), 400

        novo = User(username=username, password=password)
        db.session.add(novo)
        db.session.commit()

        return jsonify({"message": "Usuário registrado com sucesso!"}), 201

    # -------------------- LOGIN --------------------
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username, password=password).first()
        if not user:
            return jsonify({"error": "Credenciais inválidas"}), 401

        return jsonify({"message": f"Bem-vindo, {user.username}!"}), 200

    # -------------------- POSTAGENS --------------------
    @app.route('/posts', methods=['POST'])
    def create_post():
        data = request.get_json()
        user_id = data.get('user_id')
        content = data.get('content')

        if not user_id or not content:
            return jsonify({"error": "Campos obrigatórios ausentes"}), 400

        post = Post(user_id=user_id, content=content)
        db.session.add(post)
        db.session.commit()
        return jsonify({"message": "Postagem criada com sucesso!"}), 201

    @app.route('/posts', methods=['GET'])
    def get_posts():
        posts = Post.query.all()
        result = [
            {
                "id": p.id,
                "content": p.content,
                "likes": p.likes,
                "reposts": p.reposts,
                "user": p.user.username
            } for p in posts
        ]
        return jsonify(result), 200

    @app.route('/posts/<int:post_id>/like', methods=['POST'])
    def like_post(post_id):
        post = Post.query.get(post_id)
        if not post:
            return jsonify({"error": "Post não encontrado"}), 404
        post.likes += 1
        db.session.commit()
        return jsonify({"message": "Post curtido!"}), 200

    @app.route('/posts/<int:post_id>/reply', methods=['POST'])
    def reply_post(post_id):
        data = request.get_json()
        user_id = data.get('user_id')
        content = data.get('content')

        if not user_id or not content:
            return jsonify({"error": "Campos obrigatórios ausentes"}), 400

        reply = Post(user_id=user_id, content=content, reply_to=post_id)
        db.session.add(reply)
        db.session.commit()
        return jsonify({"message": "Resposta enviada!"}), 201

    @app.route('/posts/<int:post_id>/repost', methods=['POST'])
    def repost_post(post_id):
        post = Post.query.get(post_id)
        if not post:
            return jsonify({"error": "Post não encontrado"}), 404
        post.reposts += 1
        db.session.commit()
        return jsonify({"message": "Post repostado!"}), 200

    @app.route('/posts/<int:post_id>', methods=['DELETE'])
    def delete_post(post_id):
        data = request.get_json()
        user_id = data.get('user_id')

        post = Post.query.get(post_id)
        if not post:
            return jsonify({"error": "Post não encontrado"}), 404

        if post.user_id != user_id:
            return jsonify({"error": "Você só pode excluir suas próprias postagens"}), 403

        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": "Post excluído com sucesso!"}), 200

    # -------------------- SALAS --------------------
    @app.route('/rooms', methods=['POST'])
    def create_room():
        data = request.get_json()
        name = data.get('name')
        is_private = data.get('is_private', False)
        owner_id = data.get('owner_id')

        if not name or not owner_id:
            return jsonify({"error": "Nome da sala e dono são obrigatórios"}), 400

        room = Room(name=name, is_private=is_private, owner_id=owner_id)
        db.session.add(room)
        db.session.commit()
        return jsonify({"message": "Sala criada com sucesso!"}), 201

    @app.route('/rooms', methods=['GET'])
    def list_rooms():
        rooms = Room.query.all()
        result = [
            {
                "id": r.id,
                "name": r.name,
                "is_private": r.is_private,
                "owner": r.owner.username
            } for r in rooms
        ]
        return jsonify(result), 200
