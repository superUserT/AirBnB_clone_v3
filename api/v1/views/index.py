#!/usr/bin/python3
"""General Routes"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returning the api status"""
    return jsonify(status='OK')


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Returning the classes with their number of instances"""
    classes = {
        "amenities": Amenity, "cities": City,
        "places": Place, "reviews": Review,
        "states": State, "users": User
    }
    count_dict = dict()

    for plural, cls in classes.items():
        count_dict[plural] = storage.count(cls)

    return jsonify(count_dict)
