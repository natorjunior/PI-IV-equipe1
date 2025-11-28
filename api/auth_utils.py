"""
Utilitários de autenticação para proteger rotas da API
"""
from functools import wraps
from flask import jsonify
from flask_login import current_user

def login_required_api(f):
    """
    Decorador personalizado para rotas de API que requer autenticação.
    Retorna JSON em vez de redirecionar para página de login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({
                "message": "Autenticação necessária",
                "authenticated": False
            }), 401
        return f(*args, **kwargs)
    return decorated_function

def get_current_user_data():
    """
    Retorna os dados do usuário atualmente logado
    """
    if current_user.is_authenticated:
        return {
            "id": current_user.id,
            "nome_usuario": current_user.nome_usuario,
            "email": current_user.email,
            "authenticated": True
        }
    return {"authenticated": False}
