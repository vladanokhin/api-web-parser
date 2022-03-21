import os

from configs.api_v1 import ApiConfigV1
from configs.parser import ParserConfig


class AppConfig(ApiConfigV1, ParserConfig):

    DEBUG = True

    FLASK_ENV = os.getenv('FLASK_ENV', 'development')

    SECRET_KEY = os.getenv('SECRET_KEY')


class ProductionConfig(AppConfig):

    DEBUG = False

    FLASK_ENV = 'production'
