from flask import request, jsonify
import services

def init_routes(app):

    @app.route("/register", methods=["POST"])
    def register():
        data = request.get_json()
        return services.register_user(data)

    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json()
        return services.login_user(data)

    @app.route("/")
    def home():
        return jsonify({"info": "Use /register para criar conta e /login para logar"})
