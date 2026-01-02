from flask import Blueprint, request, jsonify
from modules.user.service import UserService

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    try:
        user = UserService.create_user(data['email'], data['name'])
        return jsonify(user), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@user_bp.route('/api/users', methods=['GET'])
def get_users():
    users = UserService.get_all_users()
    return jsonify(users)

