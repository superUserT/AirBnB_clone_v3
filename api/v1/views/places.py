#!/usr/bin/python3
""" Place objects that handles all default RESTFul API actions """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places",
                methods=["GET"], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)
    else:
        places_list = []
        for city in city.places:
            places_list.append(city.to_dict())

        return jsonify(places_list)

@app_views.route("/places/<place_id>",
                methods=["GET"], strict_slashes=False)
def place_by_id(place_id):
    """Retrieves a Place object linked to <place_id>"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route("/places/<place_id>",
                methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object linked to <place_id>"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    else:
        storage.delete(place)
        storage.save()

        return jsonify({}), 200


@app_views.route("/cities/<city_id>/places",
                methods=["POST"], strict_slashes=False)
def new_place(city_id):
    """Creates a new Place object"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)
    else:
        place_data = request.get_json()
        if not place_data:
            abort(400, "Not a JSON")

        if "user_id" not in place_data:
            abort(400, "Missing user_id")

        if "name" not in place_data:
            abort(400, "Missing name")

        user = storage.get(User, place_data['user_id'])
        if not user:
            abort(404)

        place_data['city_id'] = city_id
        place = Place(**place_data)
        place.save()

        return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>",
                methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    else:
        json_place = request.get_json()
        if not json_place:
            abort(400, "Not a JSON")

        ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
        for key, value in json_place.items():
            if key not in ignore_keys:
                setattr(place, key, value)

        place.save()

        return jsonify(place), 200


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