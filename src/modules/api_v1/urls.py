from flask_restful import Api

from src.modules.api_v1.classes.ParserApi import ParserApi
from src.modules.api_v1.classes.ConvertApi import ConvertApi


def url_mapping(api: Api) -> None:
    api.add_resource(ParserApi, ParserApi.URL)
    api.add_resource(ConvertApi, ConvertApi.URL)
