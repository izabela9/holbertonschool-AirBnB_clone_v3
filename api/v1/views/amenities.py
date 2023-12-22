#!/usr/bin/python3
'''
Module for handling all RESTFul
API actions
'''

from flask import Flask, jsonify, abort, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def handle_amenities():
    """Handles GET and POST requests."""
    if request.method == 'GET':
        amenities = storage.all(Amenity).values()
        return jsonify([amenity.to_dict() for amenity in amenities])

    if request.method == 'POST':
        data = request.get_json(silent=True, force=True)

        if data is None:
            abort(400, description="Not a JSON")

        if 'name' not in data:
            abort(400, description="Missing name")

        new_amenity = Amenity(**data)
        storage.new(new_amenity)
        storage.save()

        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def handle_specific_amenity(amenity_id):
    """Handles GET, PUT, and DELETE requests for a specific amenity."""
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    if request.method == 'PUT':
        data = request.get_json(silent=True, force=True)

        if data is None:
            abort(400, description="Not a JSON")

        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)

        storage.save()
        return jsonify(amenity.to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
