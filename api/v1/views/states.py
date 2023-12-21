#!/usr/bin/python3
'''
Module for handling all RESTFul
API actions
'''

from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
import os
from api.v1.views import app_views
import json

app = Flask(__name__)


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """Handles GET (all states) and POST
    (create a new state) requests."""
    if request.method == 'GET':
        states = storage.all(State).values()
        return jsonify([state.to_dict() for state in states])

    if request.method == 'POST':
        if not request.get_json():
            abort(400, description="Not a JSON")

        data = request.get_json()

        if 'name' not in data:
            abort(400, description="Missing name")

        new_state = State(**data)
        storage.new(new_state)
        storage.save()

        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def state(state_id):
    """Handles GET, PUT (update),
    and DELETE (delete) requests
    for a specific state."""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(state.to_dict())

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, description="Not a JSON")

        data = request.get_json()

        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)

        storage.save()
        return jsonify(state.to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
