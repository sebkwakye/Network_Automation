from flask import Flask

# Import blueprints for API and dashboard views
from .api import api
from .dashboard import dashboard


def create_app():
    """
    Create and configure the Flask application.

    This function initializes a Flask app instance, registers
    all blueprints (modular route collections), and returns the app.

    :return: Configured Flask application
    """
    # Instantiate the Flask application
    app = Flask(__name__)

    # Register the API routes under the '/api' prefix
    app.register_blueprint(api)

    # Register the dashboard routes (serves HTML UI)
    app.register_blueprint(dashboard)


    return app
