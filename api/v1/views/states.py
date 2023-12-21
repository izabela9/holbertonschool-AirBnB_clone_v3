#!/usr/bin/python3
'''
Module for handling all RESTFul
API actions
'''

from flask import Flask, jsonify, abort
from models import storage
import os

app = Flask(__name__)

@app.route('/api/v1/states', methods=['GET'])
def get_states():
    """Retrieves the list of all State objects"""
    states = storage.all('State')
    return jsonify([state.to_dict() for state in states])

@app.route('/api/v1/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieves a state object"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app.route('/api/v1/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Delete a state object"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

if __name__ == "__main__":
    '''
    Starting server
    '''
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
