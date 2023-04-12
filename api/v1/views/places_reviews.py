#!/usr/bin/python3
"""Routes"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route(
    '/places/<place_id>/reviews',
    methods=['GET'],
    strict_slashes=False)
def Reviews(place_id: str):
    """List all reviews"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews_list = list(map(lambda x: x.to_dict(), place.reviews))

    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id: str):
    """Getting a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route(
    '/reviews/<review_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_review(review_id: str):
    """Deleting a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    review.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route(
    '/places/<place_id>/reviews',
    methods=['POST'],
    strict_slashes=False)
def create_review(place_id: str):
    """Creating a new review"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if 'user_id' not in data.keys():
        abort(400, 'Missing user_id')

    user = storage.get(User, data.get('user_id'))
    if user is None:
        abort(404)

    if 'text' not in data.keys():
        abort(400, 'Missing text')

    review = Review(**data, place_id=place.id)

    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id: str):
    """Update a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            continue

        review.__setattr__(key, value)

    review.save()

    return jsonify(review.to_dict())
