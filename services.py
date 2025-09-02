from flask import jsonify

# Mock em memória
usuarios = {}

def register_user(data):
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"erro": "Usuário e senha são obrigatórios"}), 400

    if username in usuarios:
        return jsonify({"erro": "Usuário já existe"}), 400

    usuarios[username] = password
    return jsonify({"mensagem": "Conta criada com sucesso!"}), 201


def login_user(data):
    username = data.get("username")
    password = data.get("password")

    if username not in usuarios or usuarios[username] != password:
        return jsonify({"erro": "Usuário ou senha inválidos"}), 401

    return jsonify({"mensagem": f"Bem-vindo, {username}!"}), 200
