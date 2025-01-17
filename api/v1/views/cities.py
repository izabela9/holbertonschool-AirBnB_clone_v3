#!/usr/bin/python3
'''
Module for handling all RESTFul
API actions
'''

from flask import Flask, jsonify, abort, request
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'], strict_slashes=False)
def handle_cities(state_id=None):
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if request.method == 'GET':
        return jsonify([city.to_dict() for city in state.cities])

    if request.method == 'POST':
        if not request.get_json():
            abort(400, description="Not a JSON")
        data = request.get_json(silent=True, force=True)
        if 'name' not in data:
            abort(400, description="Missing name")
        city = City(name=data['name'], state_id=state.id)
        storage.new(city)
        storage.save()
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, description="Not a JSON")
        data = request.get_json()
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
