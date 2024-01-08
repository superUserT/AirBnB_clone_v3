#!/usr/bin/python3
""" User object that handles all default RESTFul API actions """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def all_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User).values()

    users_list = []
    for user in users:
        users_list.append(user.to_dict())

    return jsonify(users_list)


@app_views.route("/users/<user_id>",
                smethods=["GET"], strict_slashes=False)
def user_by_id(user_id):
    """Retrieves a User object linked to <user_id>"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route("/users/<user_id>",
                methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object linked to <user_id>"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    else:
        storage.delete(user)
        storage.save()

        return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def new_user():
    """Creates a new User object"""
    user_data = request.get_json()
    if not user_data:
        abort(400, "Not a JSON")

    if "email" not in user_data:
        abort(400, "Missing email")

    if "password" not in user_data:
        abort(400, "Missing password")

    user = User(**user_data)
    user.save()

    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>",
                methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    else:
        json_user = request.get_json()
        if not json_user:
            abort(400, "Not a JSON")

        ignore_keys = ["id", "email", "created_at", "updated_at"]
        for key, value in json_user.items():
            if key not in ignore_keys:
                setattr(user, key, value)

        user.save()

        return jsonify(user), 200


@app_views.errorhandler(404)
def page_not_found(exception):
    """
    A handler for 404 errors that returns
    a JSON-formatted 404 status code response.
    """
    error = {
    "error": "Not found"
    }

    response_error = jsonify(error)

    return response_error, 404


@app_views.errorhandler(400)
def bad_request(exception):
    """
    A handler for 400 errors that returns
    a JSON-formatted 400 status code response.
    """
    error = {
    "error": "Bad Request"
    }

    response_error = jsonify(error)

    return response_error, 400