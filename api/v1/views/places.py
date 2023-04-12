#!/usr/bin/python3
"""
This is the place module
contains all the routes
for manage the places class
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.place import User


@app_views.route(
    '/cities/<city_id>/places',
    methods=['GET'],
    strict_slashes=False)
def places(city_id: str):
    """Getting places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places_list = list(map(lambda x: x.to_dict(), city.places))

    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id: str):
    """Getting a place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route(
    '/places/<place_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_place(place_id: str):
    """Delete a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route(
    '/cities/<city_id>/places',
    methods=['POST'],
    strict_slashes=False)
def create_place(city_id: str):
    """Crearing a place"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if 'user_id' not in data.keys():
        abort(400, 'Missing user_id')

    user = storage.get(User, data.get('user_id'))
    if user is None:
        abort(404)

    if 'name' not in data.keys():
        abort(400, 'Missing name')

    place = Place(**data, city_id=city.id)

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id: str):
    """Modify the place"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    for key, value in data.items():
        if key in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            continue

        place.__setattr__(key, value)

    place.save()

    return jsonify(place.to_dict()), 200
