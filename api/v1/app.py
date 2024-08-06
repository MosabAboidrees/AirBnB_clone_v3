#!/usr/bin/python3
"""API Status Module"""

from flask import Flask, make_response, jsonify
from models import storage
from os import environ
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_database(error):
    """Close the storage database"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Not found """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == '__main__':
    """ Main Function """
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = environ.get('HBNB_API_PORT', '5000')

    app.run(host=host, port=port, threaded=True)
