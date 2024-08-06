#!/usr/bin/python3
"""
This file contains the routes for managing the association between
Place and Amenity objects, providing endpoints to retrieve, delete,
and add amenities to a place.
"""

import os
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity
from models.place import Place
from flasgger.utils import swag_from


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/place_amenity/get_id.yml', methods=['GET'])
def get_amenities(place_id):
    """
    Retrieve all Amenity objects for a given Place.

    This function retrieves all Amenity objects associated with a specific
    place identified by the place_id.
    Args:
        place_id (str): The ID of the place for which
        amenities are to be retrieved.
    Returns:
        Response: JSON response containing a list of Amenity objects for the
                  specified place, or a 404 error if the place is not found.
    """
    # Retrieve the Place object using the place_id
    place = storage.get(Place, place_id)
    # If the Place object does not exist, abort with a 404 error
    if place is None:
        abort(404)

    # Create a list of dictionaries for each Amenity object in the place
    amenities = [obj.to_dict() for obj in place.amenities]

    # Return the list of Amenity objects as a JSON response
    return jsonify(amenities)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/place_amenity/delete.yml', methods=['DELETE'])
def delete_amenity(place_id, amenity_id):
    """
    Delete an Amenity object from a Place.

    This function deletes a specific Amenity object associated with a
    specific place identified by the place_id and amenity_id.
    Args:
        place_id (str): The ID of the place from which the amenity
        will be removed.
        amenity_id (str): The ID of the Amenity object to be removed.
    Returns:
        Response: JSON response with an empty dictionary if the Amenity
                  object was deleted successfully, or a 404 error if not found.
    """
    # Retrieve the Place object using the place_id
    place = storage.get(Place, place_id)
    # If the Place object does not exist, abort with a 404 error
    if place is None:
        abort(404)

    # Retrieve the Amenity object using the amenity_id
    amenity = storage.get(Amenity, amenity_id)
    # If the Amenity object does not exist, abort with a 404 error
    if amenity is None:
        abort(404)

    # If the Amenity object is not associated
    # with the Place, abort with a 404 error
    if amenity not in place.amenities:
        abort(404)

    # Remove the Amenity object from the Place
    place.amenities.remove(amenity)
    # Save the changes to storage
    storage.save()

    # Return an empty JSON response indicating successful deletion
    return jsonify({})


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
@swag_from('documentation/place_amenity/post.yml', methods=['POST'])
def post_amenity2(place_id, amenity_id):
    """
    Add an Amenity object to a Place.

    This function adds a specific Amenity object to a place identified by
    the place_id and amenity_id.
    Args:
        place_id (str): The ID of the place to which the amenity will be added.
        amenity_id (str): The ID of the Amenity object to be added.
    Returns:
        Response: JSON response containing the Amenity object if added
                  successfully, or a 404 error if the place or amenity is not
                  found, or a 200 response if the amenity already exists.
    """
    # Retrieve the Place object using the place_id
    place = storage.get(Place, place_id)
    # If the Place object does not exist, abort with a 404 error
    if place is None:
        abort(404)

    # Retrieve the Amenity object using the amenity_id
    amenity = storage.get(Amenity, amenity_id)
    # If the Amenity object does not exist, abort with a 404 error
    if amenity is None:
        abort(404)

    # If the Amenity object is already associated with the Place
    if amenity in place.amenities:
        # Return the existing Amenity object
        # as a JSON response with a 200 status code
        return jsonify(amenity.to_dict()), 200

    # Append the Amenity object to the Place's amenities
    place.amenities.append(amenity)
    # Save the changes to storage
    storage.save()

    # Return the newly added Amenity object
    # as a JSON response with a 201 status code
    return jsonify(amenity.to_dict()), 201
