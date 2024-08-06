#!/usr/bin/python3
"""API Status Module"""

from flask import Flask, make_response, jsonify
from models import storage
from os import environ, getenv
from api.v1.views import app_views
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_db(obj):
    """
    Close the storage connection.

    This function is called when the app context is torn down,
    ensuring that the storage connection is properly closed.
    """
    # Call the close() method to close the storage connection
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """
    Handle 404 errors with a custom response.

    This function returns a custom JSON response with a 404 status
    code when a resource is not found.
    """
    # Return a JSON response indicating that the requested
    # resource was not found
    return make_response(jsonify({"error": "Not found"}), 404)


# Configure Swagger for API documentation
app.config['SWAGGER'] = {
    'title': 'AirBnB clone - RESTful API',
    'description': 'This is the API that was created'
                   'for the hbnb restful API project, '
                   'all the documentation will be shown below.',
    'uiversion': 3  # Set the UI version for Swagger
}

# Initialize Swagger for the app to provide interactive API documentation
Swagger(app)

# Entry point for the application
if __name__ == "__main__":

    # Get the host and port configuration from
    # environment variables or set defaults
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)

    # Run the Flask application with the specified
    # host, port, and threading enabled
    app.run(host, int(port), threaded=True)
