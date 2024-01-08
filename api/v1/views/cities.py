#!/usr/bin/python3
""" City objects that handles all default RESTFul API actions """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def all_cities(state_id):
    """Retrieves the list of all City objects"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)
    else:
        cities_list = []
        for city in state.cities:
            cities_list.append(city.to_dict())

        return jsonify(cities_list)


@app_views.route("/cities/<city_id>",
                methods=["GET"], strict_slashes=False)
def city_by_id(city_id):
    """Retrieves a City object linked to <city_id>"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>",
                methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object linked to <city_id>"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        storage.delete(city)
        storage.save()

        return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def new_city(state_id):
    """Creates a new City object"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)
    else:
        city_data = request.get_json()
        if not city_data:
            abort(400, "Not a JSON")

        if "name" not in city_data:
            abort(400, "Missing name")

        city_data['state_id'] = state_id
        city = City(**city_data)
        city.save()

        return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>",
                methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        json_city = request.get_json()
        if json_city is None:
            abort(400, "Not a JSON")

        ignore_keys = ["id", "state_id", "created_at", "updated_at"]
        for key, value in json_city.items():
            if key not in ignore_keys:
                setattr(city, key, value)

        city.save()

        return jsonify(city), 200


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