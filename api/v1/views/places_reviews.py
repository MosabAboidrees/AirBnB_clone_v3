#!/usr/bin/python3
"""
This file contains the Review module, which provides API endpoints for
managing Review objects, including retrieving, creating, updating, and
deleting reviews.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from flasgger.utils import swag_from


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/reviews/get.yml', methods=['GET'])
def get_all_reviews(place_id):
    """
    Retrieve all Review objects for a given place.

    This function retrieves all Review objects associated with a specific
    place identified by the place_id
    Args:
        place_id (str): The ID of the place for which
        reviews are to be retrieved.
    Returns:
        Response: JSON response containing a list of Review objects for the
                  specified place, or a 404 error if the place is not found.
    """
    # Retrieve the Place object using the place_id
    place = storage.get(Place, place_id)

    # If the Place object does not exist, abort with a 404 error
    if place is None:
        abort(404)

    # Create a list of dictionaries for each Review object in the place
    reviews = [obj.to_dict() for obj in place.reviews]

    # Return the list of Review objects as a JSON response
    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/reviews/get_id.yml', methods=['GET'])
def get_review(review_id):
    """
    Retrieve a Review object by its ID.

    This function retrieves a specific Review object using its unique ID.
    Args:
        review_id (str): The ID of the Review object to retrieve.
    Returns:
        Response: JSON response containing the Review object if found,
                  or a 404 error if not found.
    """
    # Retrieve the Review object using its ID
    review = storage.get(Review, review_id)

    # If the Review object does not exist, abort with a 404 error
    if review is None:
        abort(404)

    # Return the Review object as a JSON response
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/reviews/delete.yml', methods=['DELETE'])
def del_review(review_id):
    """
    Delete a Review object by its ID.

    This function deletes a specific Review object using its unique ID.
    Args:
        review_id (str): The ID of the Review object to delete.
    Returns:
        Response: JSON response with an empty dictionary if the Review
                  object was deleted successfully, or a 404 error if not found.
    """
    # Retrieve the Review object using its ID
    review = storage.get(Review, review_id)
    # If the Review object does not exist, abort with a 404 error
    if review is None:
        abort(404)

    # Delete the Review object from storage
    review.delete()
    # Save the changes to storage
    storage.save()
    # Return an empty JSON response indicating successful deletion
    return jsonify({})


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/reviews/post.yml', methods=['POST'])
def create_obj_review(place_id):
    """
    Create a new Review object.

    This function creates a new Review object associated with a specific
    place identified by the place_id, based on the provided JSON data.
    Args:
        place_id (str): The ID of the place to which the new Review belongs.
    Returns:
        Response: JSON response containing the newly created Review object
                  and a status code of 201, or a 400 error if the input
                  is invalid, or a 404 error if the place or user is not found.
    """
    # Retrieve the Place object using the place_id
    place = storage.get(Place, place_id)

    # If the Place object does not exist, abort with a 404 error
    if place is None:
        abort(404)

    # Check if the request data is valid JSON
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Check if the 'user_id' field is present in the JSON data
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    # Check if the 'text' field is present in the JSON data
    if 'text' not in request.get_json():
        return make_response(jsonify({"error": "Missing text"}), 400)

    # Retrieve the JSON data from the request
    kwargs = request.get_json()
    # Set the place_id for the new Review object
    kwargs['place_id'] = place_id
    # Retrieve the User object using the user_id from the request
    user = storage.get(User, kwargs['user_id'])
    # If the User object does not exist, abort with a 404 error
    if user is None:
        abort(404)

    # Create a new Review object using the JSON data
    obj = Review(**kwargs)
    # Save the new Review object to storage
    obj.save()

    # Return the newly created Review object as a JSON response
    return jsonify(obj.to_dict()), 201


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/reviews/put.yml', methods=['PUT'])
def post_review(review_id):
    """
    Update an existing Review object.

    This function updates a specific Review object based on the provided
    JSON data and its unique ID.
    Args:
        review_id (str): The ID of the Review object to update.
    Returns:
        Response: JSON response containing the updated Review object,
                  or a 400 error if the input is invalid,
                  or a 404 error if the Review object is not found.
    """
    # Check if the request data is valid JSON
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Retrieve the Review object using its ID
    obj = storage.get(Review, review_id)
    # If the Review object does not exist, abort with a 404 error
    if obj is None:
        abort(404)

    # Iterate over the JSON data and update the Review object's attributes
    for key, value in request.get_json().items():
        # Skip updating certain attributes
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated']:
            setattr(obj, key, value)

    # Save the updated Review object to storage
    storage.save()

    # Return the updated Review object as a JSON response
    return jsonify(obj.to_dict())
