#!/usr/bin/python3
"""States Routes"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """Returning a list of states"""
    states = storage.all(State)

    states_list = list(map(lambda x: x.to_dict(), states.values()))

    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id: str):
    """Returning a specific state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id: str):
    """Deleteling a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    state.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creating a new state"""
    json_to_state = request.get_json()
    if json_to_state is None:
        abort(400, 'Not a JSON')
    if 'name' not in json_to_state.keys():
        abort(400, 'Missing name')

    state = State(**json_to_state)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def mod_state(state_id: str):
    """Modify a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key in ['id', 'created_at']:
            continue

        state.__setattr__(key, value)

    state.save()
    return jsonify(state.to_dict()), 200
