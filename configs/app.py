import os

from pathlib import Path

from configs.api_v1 import ApiConfigV1
from configs.parser import ParserConfig


class AppConfig(ApiConfigV1, ParserConfig):

    BASE_PATH = Path(__file__).resolve().parent.parent

    DEBUG = True

    FLASK_ENV = os.getenv('FLASK_ENV', 'development')

    SECRET_KEY = os.getenv('SECRET_KEY')

    TEMP_DIR = Path(BASE_PATH, 'temp/')  # folder for temporary files


class ProductionConfig(AppConfig):

    DEBUG = False

    FLASK_ENV = 'production'
