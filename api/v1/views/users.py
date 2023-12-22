#!/usr/bin/python3
'''
Module for handling all RESTFul
API actions
'''

from flask import Flask, jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def handle_users():
    """Handles GET and POST requests"""
    if request.method == 'GET':
        users = storage.all(User).values()
        return jsonify([user.to_dict() for user in users])

    elif request.method == 'POST':
        data = request.get_json(silent=True, force=True)

        if data is None:
            abort(400, description="Not a JSON")

        if 'email' not in data:
            abort(400, description="Missing email")

        if 'password' not in data:
            abort(400, description="Missing password")

        new_user = User(**data)
        storage.new(new_user)
        storage.save()

        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def handle_user(user_id):
    """Handles GET, PUT, and DELETE requests for a specific user"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())

    if request.method == 'PUT':
        data = request.get_json(silent=True, force=True)

        if data is None:
            abort(400, description="Not a JSON")

        ignore_keys = ['id', 'email', 'created_at', 'updated_at', 'password']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(user, key, value)

        storage.save()
        return jsonify(user.to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
