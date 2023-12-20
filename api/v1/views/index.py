#!/usr/bin/python3
'''
Module to create the routes
for our api
'''
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns a JSON response with status OK."""
    return jsonify({"status": "OK"})
