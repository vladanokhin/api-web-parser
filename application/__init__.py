import os
from flask import Flask

from src.helpers import create_dirs
from src.modules.api_v1 import init_api_v1


def create_app() -> Flask:
    """
    Entry point for application.
    Also, initializing submodules
    :return: Flask application
    """
    _app = Flask(__name__)  # initialization Flask app

    # Get settings from Class
    _app.config.from_object(
        os.getenv('FLASK_CONFIG', 'configs.ProductionConfig')
    )

    init_api_v1(_app)  # initialization module Api v.1

    create_dirs(_app.config['TEMP_DIR'])

    return _app


app = create_app()
