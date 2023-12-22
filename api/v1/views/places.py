#!/usr/bin/python3
'''
Module for handling all RESTFul
API actions
'''

from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def handle_city_places(city_id):
    """Handles GET and POST requests"""
    city = storage.get(City, city_id)

    if city is None:
        return abort(404)

    if request.method == 'GET':
        places = storage.all(Place).values()
        city_places = [place.to_dict() for place in places
                       if place.city_id == city.id]
        return jsonify(city_places)

    if request.method == 'POST':
        data = request.get_json(silent=True, force=True)

        if data is None:
            abort(400, description="Not a JSON")

        if 'user_id' not in data:
            abort(400, description="Missing user_id")

        if 'name' not in data:
            abort(400, description="Missing name")

        user_id = data['user_id']
        user = storage.get(User, user_id)

        if user is None:
            abort(404)

        new_place = Place(city_id=city.id, **data)
        storage.new(new_place)
        storage.save()

        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def handle_place(place_id):
    """Handles GET, PUT, and DELETE requests for a specific place"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'PUT':
        data = request.get_json(silent=True, force=True)

        if data is None:
            abort(400, description="Not a JSON")

        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(place, key, value)

        storage.save()
        return jsonify(place.to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
