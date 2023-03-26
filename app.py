import os
import secrets

from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from resources.item import items_blueprint as ItemBlueprint
from resources.store import store_blueprint as StoreBlueprint
from resources.tags import blue_print as TagBlueprint
from resources.user import blp as UserBlueprint
import models
from db import db


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["CORS_HEADERS"] = 'Content-Type'
    app.config["JWT_SECRET_KEY"] = "142405499885472134789487076269841353067"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
    
    api = Api(app)

    jwt = JWTManager(app)

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app

if __name__ == "__main__":
    create_app()