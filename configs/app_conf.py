import os

from pathlib import Path

from .api_v1_conf import ApiConfigV1
from .parser_conf import ParserConfig


class AppConfig(ApiConfigV1, ParserConfig):

    BASE_PATH = Path(__file__).resolve().parent.parent

    DEBUG = True

    FLASK_ENV = os.getenv('FLASK_ENV', 'development')

    SECRET_KEY = os.getenv('SECRET_KEY')


class ProductionConfig(AppConfig):

    DEBUG = False

    FLASK_ENV = 'production'
