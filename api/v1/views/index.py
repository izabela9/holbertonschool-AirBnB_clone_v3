from flask import jsonify
from . import app_views

@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns a JSON response with status OK."""
    return jsonify({"status": "OK"})
