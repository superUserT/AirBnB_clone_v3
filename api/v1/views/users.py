#!/usr/bin/python3
"""Users Routes"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    users = storage.all(User)

    list_users = list(map(lambda x: x.to_dict(), users.values()))

    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id: str):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    user.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    if 'email' not in data.keys():
        abort(400, 'Missing email')

    if 'password' not in data.keys():
        abort(400, 'Missing password')

    user = User(**data)

    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str):
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    for key, value in data.items():
        if key in ['id', 'email', 'created_at', 'updated_at']:
            continue

        user.__setattr__(key, value)

    user.save()

    return jsonify(user.to_dict()), 200
