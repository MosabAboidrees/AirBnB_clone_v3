#!/usr/bin/python3
"""Index views"""
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def count():
    """An endpoint that retrieves the number of each objects by type"""
    names = ["amenities", "cities", "places", "reviews", "states", "users"]
    classes = [Amenity, City, Place, Review, State, User]

    object_count = {}
    for i in range(len(classes)):
        object_count[names[i]] = storage.count(classes[i])
    return jsonify(object_count)
