from functools import wraps

from flask import abort,jsonify
from flask_jwt_extended import get_jwt_identity

from models.users import UserModel


def admin_required(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        try:
            user_id = get_jwt_identity()
            if not is_admin(user_id):
                return jsonify({"message": "Admin role is required"}), 403

        except Exception as e:
            return jsonify({"message": "Invalid token"}), 401
        return func(*args, **kwargs)

    return wrapper_func


def is_admin(user_id):
    return UserModel.query.get(user_id).is_admin
