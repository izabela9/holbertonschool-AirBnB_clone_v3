#!/usr/bin/python3
'''
Module to instatiate an flask app
to deploy our API
'''
from flask import Flask
from models import storage
from api.v1.views import app_views
import os
from flask import jsonify

app = Flask(__name__)

app.register_blueprint(app_views)


@app.errorhandler(404)
def error_404(error):
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def close_db(error):
    """
    Closes the storage on teardown
    """
    storage.close()

if __name__ == "__main__":
    '''
    Starting server
    '''
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
