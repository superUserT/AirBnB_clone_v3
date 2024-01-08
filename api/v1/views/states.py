#!/usr/bin/python3
""" State objects that handles all default RESTFul API actions """


from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def all_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()

    states_list = []
    for state in states:
        states_list.append(state.to_dict())

    return jsonify(states_list)


@app_views.route("/states/<state_id>",
                methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """Retrieves a State object linked to <state_id>"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route("/states/<state_id>",
                methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object linked to <state_id>"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        storage.delete(state)
        storage.save()

        return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def new_state():
    """Creates a new State object"""
    state_data = request.get_json()
    if not state_data:
        abort(400, "Not a JSON")

    if "name" not in state_data:
        abort(400, "Missing name")

    state = State(**state_data)
    state.save()

    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>",
                methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        json_state = request.get_json()
        if not json_state is None:
            abort(400, "Not a JSON")

        ignore_keys = ["id", "created_at", "updated_at"]
        for key, value in json_state.items():
            if key not in ignore_keys:
                setattr(state, key, value)

        state.save()

        return jsonify(state), 200


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