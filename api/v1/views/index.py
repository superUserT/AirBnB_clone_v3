#!/usr/bin/python3
""" A route to the status checks """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def get_status():
    """Return the status of your API"""
    status = {
    "status": "OK"
    }

    response = jsonify(status)

    return response


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def stats():
    """Retrieves the number of each objects by type"""
    count = {
    "amenities": storage.count("Amenity"),
    "cities": storage.count("City"),
    "places": storage.count("Place"),
    "reviews": storage.count("Review"),
    "states": storage.count("State"),
    "users": storage.count("User"),
    }

    return jsonify(count)