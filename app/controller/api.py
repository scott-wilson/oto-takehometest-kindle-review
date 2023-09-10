from flask import Flask
from app.routes import routes


def start():
    # Initialize the Flask app
    app = Flask(__name__)

    # Register routes
    routes.register_routes(app)

    app.run()
