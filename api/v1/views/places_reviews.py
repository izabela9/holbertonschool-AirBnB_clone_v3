#!/usr/bin/python3
'''
Module for handling all RESTFul
API actions
'''

from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'], strict_slashes=False)
def handle_place_reviews(place_id):
    """Handles GET and POST requests"""
    place = storage.get(Place, place_id)

    if place is None:
        return abort(404)

    if request.method == 'GET':
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)

    if request.method == 'POST':
        data = request.get_json(silent=True, force=True)

        if data is None:
            return abort(400, description="Not a JSON")
        
        user_id = data.get("user_id", None)
        text = data.get("text", None)

        if user_id not in data:
            return abort(400, description="Missing user_id")

        if text not in data:
            return abort(400, description="Missing text")

        user = storage.get(User, user_id)

        if user is None:
            abort(404)

        new_review = Review(place_id=place_id, **data)
        storage.new(new_review)
        storage.save()

        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def handle_review(review_id):
    """Handles GET, PUT, and DELETE requests for a specific review"""
    review = storage.get(Review, review_id)

    if review is None:
        return abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict()), 200

    if request.method == 'PUT':
        data = request.get_json(silent=True, force=True)

        if data is None:
            return abort(400, description="Not a JSON")

        ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(review, key, value)

        storage.save()
        return jsonify(review.to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
