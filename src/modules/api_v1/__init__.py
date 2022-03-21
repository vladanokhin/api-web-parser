from flask import Flask
from flask import Blueprint
from flask_restful import Api

from src.modules.api_v1.urls import url_mapping


errors = {
    "BadRequest": {
        "status": "error"
    }
}


def init_api_v1(app: Flask) -> None:
    """
    Initializing submodule Api
    :param app: Flask application
    :return: None
    """
    blueprint = Blueprint('api', __name__)
    api = Api(blueprint, errors=errors, prefix=app.config.get('API_URL_PREFIX'))
    url_mapping(api)
    app.register_blueprint(blueprint)

