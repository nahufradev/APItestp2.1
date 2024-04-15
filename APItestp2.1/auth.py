from flask import Blueprint, request, jsonify
from database.user_repository import UserRepository

auth_bp = Blueprint('auth', __name__)
user_repo = UserRepository()

@auth_bp.route('/registro', methods=['POST'])
def registro():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if user_repo.get_user_by_username(username):
        return jsonify({'message': 'El nombre de usuario ya existe'}), 400

    user_repo.create_user(username, password)
    return jsonify({'message': 'Usuario registrado exitosamente'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = user_repo.get_user_by_username(username)
    if user and user.check_password(password):
        return jsonify({'message': 'Inicio de sesión exitoso'}), 200
    else:
        return jsonify({'message': 'Credenciales incorrectas'}), 401