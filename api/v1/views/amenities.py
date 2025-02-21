#!/usr/bin/python3
""" Amenity objects that handles all default RESTFul API actions """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def all_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()

    amenities_list = []
    for amenity in amenities:
        amenities_list.append(amenity.to_dict())

    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>",
                methods=["GET"], strict_slashes=False)
def amenity_by_id(amenity_id):
    """Retrieves a Amenity object linked to <amenity_id>"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    else:
        return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>",
                methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object linked to <amenity_id>"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()

        return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def new_amenity():
    """Creates a new Amenity object"""
    amenity_data = request.get_json()
    if not amenity_data:
        abort(400, "Not a JSON")

    if "name" not in amenity_data:
        abort(400, "Missing name")

    amenity = Amenity(**amenity_data)
    amenity.save()

    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>",
                methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    else:
        json_amenity = request.get_json()
        if not json_amenity:
            abort(400, "Not a JSON")

        ignore_keys = ["id", "created_at", "updated_at"]
        for key, value in json_amenity.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)

        amenity.save()

        return jsonify(amenity), 200


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