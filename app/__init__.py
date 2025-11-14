from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .models import db
from app.controllers.users import users_bp  
from app.controllers.preferences import preferences_bp
from app.controllers.topics import topics_bp    
from app.controllers.availability import availability_bp

api_prefix = "/api/v1/"


def create_app(config):
    app = Flask(__name__)
    app.config.update(config)
    db.init_app(app)

    app.register_blueprint(users_bp, url_prefix=f"{api_prefix}/users")
    app.register_blueprint(preferences_bp, url_prefix=f"{api_prefix}/prefs")
    app.register_blueprint(topics_bp, url_prefix=f"{api_prefix}/topics")
    app.register_blueprint(availability_bp, url_prefix=f"{api_prefix}/availability")

    with app.app_context():
        db.create_all()

    CORS(app, supports_credentials=True)
    return app