from flask import request, jsonify
from models import db, User

def init_routes(app):

    # Registrar usuário
    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Usuário já existe"}), 400

        novo = User(username=username, password=password)
        db.session.add(novo)
        db.session.commit()

        return jsonify({"message": "Usuário registrado com sucesso!"}), 201

    # Login
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username, password=password).first()

        if not user:
            return jsonify({"error": "Credenciais inválidas"}), 401

        return jsonify({"message": f"Bem-vindo, {user.username}!"}), 200
