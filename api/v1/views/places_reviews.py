#!/usr/bin/python3
""" Review object that handles all default RESTFul API actions """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"], strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Reviews objects of a Place"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)
    else:
        places_list = []
        for place in place.places:
            places_list.append(place.to_dict())

        return jsonify(places_list)


@app_views.route("/reviews/<review_id>",
                 methods=["GET"], strict_slashes=False)
def review_by_id(review_id):
    """Retrieves a Review object linked to <review_id>"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object linked to <review_id>"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    else:
        storage.delete(review)
        storage.save()

        return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def new_review(place_id):
    """Creates a new Review object"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)
    else:
        review_data = request.get_json()
        if not review_data:
            abort(400, "Not a JSON")

        if "user_id" not in review_data:
            abort(400, "Missing user_id")
        
        if "text" not in review_data:
            abort(400, "Missing user_id")

        user = storage.get(User, review_data['user_id'])
        if not user:
            abort(404)

        review_data['place_id'] = place_id
        review = Review(**review_data)
        review.save()

        return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>",
                 methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    else:
        json_review = request.get_json()
        if not json_review:
            abort(400, "Not a JSON")

        ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
        for key, value in json_review.items():
            if key not in ignore_keys:
                setattr(review, key, value)

        review.save()

        return jsonify(review), 200


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