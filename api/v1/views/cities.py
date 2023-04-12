#!/usr/bin/python3
"""Routes"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route(
    '/states/<state_id>/cities',
    methods=['GET'],
    strict_slashes=False)
def cities(state_id: str):
    """Listing cities from a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities_list = []

    for city in state.cities:
        cities_list.append(city.to_dict())

    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id: str):
    """Returning a city from an id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id: str):
    """Deleting a city from an id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    city.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route(
    '/states/<state_id>/cities',
    methods=['POST'],
    strict_slashes=False)
def create_city(state_id: str):
    """Creating a new city"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not json')

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if 'name' not in data.keys():
        abort(400, 'Missing name')

    city = City(**data, state_id=state_id)

    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id: str):
    """Modify the specified city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key in ['id', 'created_at', 'updated_at', 'state_id']:
            continue

        city.__setattr__(key, value)

    city.save()

    return jsonify(city.to_dict()), 200
