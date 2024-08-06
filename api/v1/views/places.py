#!/usr/bin/python3
"""
This file contains the Place module, which provides API endpoints for
managing Place objects, including retrieving, creating, updating, deleting,
and searching places.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.state import State
from flasgger.utils import swag_from


@app_views.route('/cities/<string:city_id>/places',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/places/get.yml', methods=['GET'])
def get_all_places(city_id):
    """
    Retrieve all Place objects for a given city.

    This function retrieves all Place objects associated with a specific
    city identified by the city_id.

    Args:
        city_id (str): The ID of the city for which places are to be retrieved.

    Returns:
        Response: JSON response containing a list of Place objects for the
                  specified city, or a 404 error if the city is not found.
    """
    # Retrieve the City object using the city_id
    city = storage.get(City, city_id)

    # If the City object does not exist, abort with a 404 error
    if city is None:
        abort(404)

    # Create a list of dictionaries for each Place object in the city
    places = [obj.to_dict() for obj in city.places]

    # Return the list of Place objects as a JSON response
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/places/get_id.yml', methods=['GET'])
def get_place(place_id):
    """
    Retrieve a Place object by its ID.

    This function retrieves a specific Place object using its unique ID.

    Args:
        place_id (str): The ID of the Place object to retrieve.

    Returns:
        Response: JSON response containing the Place object if found,
                  or a 404 error if not found.
    """
    # Retrieve the Place object using its ID
    place = storage.get(Place, place_id)

    # If the Place object does not exist, abort with a 404 error
    if place is None:
        abort(404)

    # Return the Place object as a JSON response
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/places/delete.yml', methods=['DELETE'])
def del_place(place_id):
    """
    Delete a Place object by its ID.

    This function deletes a specific Place object using its unique ID.

    Args:
        place_id (str): The ID of the Place object to delete.

    Returns:
        Response: JSON response with an empty dictionary if the Place
                  object was deleted successfully, or a 404 error if not found.
    """
    # Retrieve the Place object using its ID
    place = storage.get(Place, place_id)

    # If the Place object does not exist, abort with a 404 error
    if place is None:
        abort(404)

    # Delete the Place object from storage
    place.delete()

    # Save the changes to storage
    storage.save()

    # Return an empty JSON response indicating successful deletion
    return jsonify({})


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/places/post.yml', methods=['POST'])
def create_obj_place(city_id):
    """
    Create a new Place object.

    This function creates a new Place object associated with a specific
    city identified by the city_id, based on the provided JSON data.

    Args:
        city_id (str): The ID of the city to which the new Place belongs.

    Returns:
        Response: JSON response containing the newly created Place object
                  and a status code of 201, or a 400 error if the input
                  is invalid, or a 404 error if the city or user is not found.
    """
    # Retrieve the City object using the city_id
    city = storage.get(City, city_id)

    # If the City object does not exist, abort with a 404 error
    if city is None:
        abort(404)

    # Check if the request data is valid JSON
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Check if the 'user_id' field is present in the JSON data
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    # Check if the 'name' field is present in the JSON data
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    # Retrieve the JSON data from the request
    kwargs = request.get_json()

    # Set the city_id for the new Place object
    kwargs['city_id'] = city_id

    # Retrieve the User object using the user_id from the request
    user = storage.get(User, kwargs['user_id'])

    # If the User object does not exist, abort with a 404 error
    if user is None:
        abort(404)

    # Create a new Place object using the JSON data
    obj = Place(**kwargs)

    # Save the new Place object to storage
    obj.save()

    # Return the newly created Place object as a JSON response
    return jsonify(obj.to_dict()), 201


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/places/put.yml', methods=['PUT'])
def post_place(place_id):
    """
    Update an existing Place object.

    This function updates a specific Place object based on the provided
    JSON data and its unique ID.

    Args:
        place_id (str): The ID of the Place object to update.

    Returns:
        Response: JSON response containing the updated Place object,
                  or a 400 error if the input is invalid,
                  or a 404 error if the Place object is not found.
    """
    # Check if the request data is valid JSON
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Retrieve the Place object using its ID
    obj = storage.get(Place, place_id)

    # If the Place object does not exist, abort with a 404 error
    if obj is None:
        abort(404)

    # Iterate over the JSON data and update the Place object's attributes
    for key, value in request.get_json().items():
        # Skip updating certain attributes
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated']:
            setattr(obj, key, value)

    # Save the updated Place object to storage
    storage.save()

    # Return the updated Place object as a JSON response
    return jsonify(obj.to_dict())


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/places/search.yml', methods=['POST'])
def search_places_by_id():
    """
    Search for Place objects based on filters.

    This function searches for Place objects based on specified filters,
    such as state IDs, city IDs, and amenity IDs, provided in the JSON
    request data.

    Returns:
        Response: JSON response containing a list of Place objects that
                  match the search criteria, or a 400 error if the input
                  is not valid JSON.
    """
    # Check if the request data is valid JSON
    if request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Retrieve the JSON data from the request
    data = request.get_json()

    # Initialize lists for state, city, and amenity filters
    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    # If no filters are specified, return all Place objects
    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        # Retrieve all Place objects and convert them to a list of dictionaries
        places = storage.all(Place).values()
        list_places = [place.to_dict() for place in places]
        return jsonify(list_places)

    # Initialize a list to store matching Place objects
    list_places = []

    # Filter places based on state IDs
    if states:
        # Retrieve State objects using state IDs
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    # Filter places based on city IDs
    if cities:
        # Retrieve City objects using city IDs
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    # Filter places based on amenity IDs
    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        # Retrieve Amenity objects using amenity IDs
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    # Create a list of dictionaries for the filtered Place objects
    places = []
    for p in list_places:
        d = p.to_dict()
        # Remove amenities from the dictionary representation
        d.pop('amenities', None)
        places.append(d)

    # Return the filtered list of Place objects as a JSON response
    return jsonify(places)
