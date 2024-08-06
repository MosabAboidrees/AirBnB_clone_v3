#!/usr/bin/python3
"""
This file contains the Amenity module, which provides API endpoints for
managing Amenity objects, including retrieving, creating, updating, and
deleting amenities.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity
from flasgger.utils import swag_from


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@swag_from('documentation/amenity/get.yml', methods=['GET'])
def get_all_amenities():
    """
    Retrieve all Amenity objects.

    This function retrieves all Amenity objects stored in the database and
    returns them as a JSON response.

    Returns:
        Response: JSON response containing a list of all Amenity objects.
    """
    # Retrieve all Amenity objects and convert them to a list of dictionaries
    all_list = [obj.to_dict() for obj in storage.all(Amenity).values()]

    # Return the list of Amenity objects as a JSON response
    return jsonify(all_list)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/amenity/get_id.yml', methods=['GET'])
def get_amenity(amenity_id):
    """
    Retrieve an Amenity object by its ID.

    This function retrieves a specific Amenity object using its unique ID.

    Args:
        amenity_id (str): The ID of the Amenity object to retrieve.

    Returns:
        Response: JSON response containing the Amenity object if found,
                  or a 404 error if not found.
    """
    # Retrieve the Amenity object using its ID
    amenity = storage.get(Amenity, amenity_id)

    # If the Amenity object does not exist, abort with a 404 error
    if amenity is None:
        abort(404)

    # Return the Amenity object as a JSON response
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/amenity/delete.yml', methods=['DELETE'])
def del_amenity(amenity_id):
    """
    Delete an Amenity object by its ID.

    This function deletes a specific Amenity object using its unique ID.

    Args:
        amenity_id (str): The ID of the Amenity object to delete.

    Returns:
        Response: JSON response with an empty dictionary if the Amenity
                  object was deleted successfully, or a 404 error if not found.
    """
    # Retrieve the Amenity object using its ID
    amenity = storage.get(Amenity, amenity_id)

    # If the Amenity object does not exist, abort with a 404 error
    if amenity is None:
        abort(404)

    # Delete the Amenity object from storage
    amenity.delete()

    # Save the changes to storage
    storage.save()

    # Return an empty JSON response indicating successful deletion
    return jsonify({})


@app_views.route('/amenities/', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/amenity/post.yml', methods=['POST'])
def create_obj_amenity():
    """
    Create a new Amenity object.

    This function creates a new Amenity object based on the provided JSON data.

    Returns:
        Response: JSON response containing the newly created Amenity object
                  and a status code of 201, or a 400 error if the input
                  is invalid.
    """
    # Check if the request data is valid JSON
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Check if the 'name' field is present in the JSON data
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    # Retrieve the JSON data from the request
    js = request.get_json()

    # Create a new Amenity object using the JSON data
    obj = Amenity(**js)

    # Save the new Amenity object to storage
    obj.save()

    # Return the newly created Amenity object as a JSON response
    return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/amenity/put.yml', methods=['PUT'])
def post_amenity(amenity_id):
    """
    Update an existing Amenity object.

    This function updates a specific Amenity object based on the provided
    JSON data and its unique ID.

    Args:
        amenity_id (str): The ID of the Amenity object to update.

    Returns:
        Response: JSON response containing the updated Amenity object,
                  or a 400 error if the input is invalid,
                  or a 404 error if the Amenity object is not found.
    """
    # Check if the request data is valid JSON
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Retrieve the Amenity object using its ID
    obj = storage.get(Amenity, amenity_id)

    # If the Amenity object does not exist, abort with a 404 error
    if obj is None:
        abort(404)

    # Iterate over the JSON data and update the Amenity object's attributes
    for key, value in request.get_json().items():
        # Skip updating certain attributes
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)

    # Save the updated Amenity object to storage
    storage.save()

    # Return the updated Amenity object as a JSON response
    return jsonify(obj.to_dict())
