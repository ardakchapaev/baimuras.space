"""Module docstring."""

from flask import Blueprint, jsonify, request

from src.models.user import User, db

user_bp = Blueprint("user", __name__)


@user_bp.route("/users", methods=["GET"])
def get_users():
    """Function docstring."""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@user_bp.route("/users", methods=["POST"])
def create_user():
    """Create a new user with hashed password."""
    data = request.json
    user = User(username=data["username"], email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Function docstring."""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@user_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """Function docstring."""
    user = User.query.get_or_404(user_id)
    data = request.json
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    if "password" in data:
        user.set_password(data["password"])
    db.session.commit()
    return jsonify(user.to_dict())


@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Function docstring."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return "", 204
