#!/usr/bin/python3
"""Amenities Routes"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """List all the amenities"""
    amenities = storage.all(Amenity)

    amenities_list = list(map(lambda x: x.to_dict(), amenities.values()))

    return jsonify(amenities_list)


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['GET'],
    strict_slashes=False)
def get_amenity(amenity_id: str):
    """Getting an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_amenity(amenity_id: str):
    """Delete aamenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create amenity"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    if 'name' not in data.keys():
        abort(400, 'Missing name')

    amenity = Amenity(**data)

    return jsonify(amenity.to_dict()), 201


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['PUT'],
    strict_slashes=False)
def update_amenity(amenity_id: str):
    """Update aamenity"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    for key, value in data.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue

        amenity.__setattr__(key, value)

    amenity.save()

    return jsonify(amenity.to_dict()), 200
