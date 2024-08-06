#!/usr/bin/python3
"""
This file contains the User module, which provides API endpoints for
managing User objects, including retrieving, creating, updating, and
deleting users.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User
from flasgger.utils import swag_from


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get.yml', methods=['GET'])
def get_all_users():
    """
    Retrieve all User objects.

    This function retrieves all User objects stored in the database and
    returns them as a JSON response.

    Returns:
        Response: JSON response containing a list of all User objects.
    """
    # Retrieve all User objects and convert them to a list of dictionaries
    all_list = [obj.to_dict() for obj in storage.all(User).values()]

    # Return the list of User objects as a JSON response
    return jsonify(all_list)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/user/get_id.yml', methods=['GET'])
def get_user(user_id):
    """
    Retrieve a User object by its ID.

    This function retrieves a specific User object using its unique ID.

    Args:
        user_id (str): The ID of the User object to retrieve.

    Returns:
        Response: JSON response containing the User object if found,
                  or a 404 error if not found.
    """
    # Retrieve the User object using its ID
    user = storage.get(User, user_id)

    # If the User object does not exist, abort with a 404 error
    if user is None:
        abort(404)

    # Return the User object as a JSON response
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/user/delete.yml', methods=['DELETE'])
def del_user(user_id):
    """
    Delete a User object by its ID.

    This function deletes a specific User object using its unique ID.

    Args:
        user_id (str): The ID of the User object to delete.

    Returns:
        Response: JSON response with an empty dictionary if the User
                  object was deleted successfully, or a 404 error if not found.
    """
    # Retrieve the User object using its ID
    user = storage.get(User, user_id)

    # If the User object does not exist, abort with a 404 error
    if user is None:
        abort(404)

    # Delete the User object from storage
    user.delete()

    # Save the changes to storage
    storage.save()

    # Return an empty JSON response indicating successful deletion
    return jsonify({})


@app_views.route('/users/', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/user/post.yml', methods=['POST'])
def create_obj_user():
    """
    Create a new User object.

    This function creates a new User object based on the provided JSON data.

    Returns:
        Response: JSON response containing the newly created User object
                  and a status code of 201, or a 400 error if the input
                  is invalid.
    """
    # Check if the request data is valid JSON
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Check if the 'email' field is present in the JSON data
    if 'email' not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)

    # Check if the 'password' field is present in the JSON data
    if 'password' not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)

    # Retrieve the JSON data from the request
    js = request.get_json()

    # Create a new User object using the JSON data
    obj = User(**js)

    # Save the new User object to storage
    obj.save()

    # Return the newly created User object as a JSON response
    return jsonify(obj.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/user/put.yml', methods=['PUT'])
def post_user(user_id):
    """
    Update an existing User object.

    This function updates a specific User object based on the provided
    JSON data and its unique ID.

    Args:
        user_id (str): The ID of the User object to update.

    Returns:
        Response: JSON response containing the updated User object,
                  or a 400 error if the input is invalid,
                  or a 404 error if the User object is not found.
    """
    # Check if the request data is valid JSON
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Retrieve the User object using its ID
    obj = storage.get(User, user_id)

    # If the User object does not exist, abort with a 404 error
    if obj is None:
        abort(404)

    # Iterate over the JSON data and update the User object's attributes
    for key, value in request.get_json().items():
        # Skip updating certain attributes
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(obj, key, value)

    # Save the updated User object to storage
    storage.save()

    # Return the updated User object as a JSON response
    return jsonify(obj.to_dict())
