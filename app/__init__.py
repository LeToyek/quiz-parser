from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    # Configure rate limiting
    # limiter = Limiter(
    #     get_remote_address, app=app, default_limits=["200 per day", "50 per hour"]
    # )
    print("Rate limiting configured")
    CORS(
        app,
        resources={
            r"/*": {
                "origins": [
                    "http://localhost:8000",
                    "http://localhost",
                    "https://asn.trialdyk.my.id",
                ]
            }
        },
    )
    # Register blueprints or routes
    from .routes import quiz_bp

    app.register_blueprint(quiz_bp)

    return app
