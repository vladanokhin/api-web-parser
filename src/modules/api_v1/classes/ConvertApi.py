from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from src.convertor import Convertor
from src.helpers import api_result, extract_content_from_html
from src.class_result import BaseResult


class ConvertApi(Resource):

    URL = '/convert'

    def __init__(self):
        super().__init__()
        self.reqparse = RequestParser()
        self.reqparse.add_argument("source", type=str, default='html', choices=['html'])
        self.reqparse.add_argument("text", type=str, required=True)

    @api_result
    def post(self):
        args = self.reqparse.parse_args()
        result = BaseResult()
        convertor = Convertor()

        try:
            result.metadata, result.content = extract_content_from_html(args.text, False)
            result.content = convertor.convert(result.content)
            result.success = True
        except Exception:
            result.error = 'Cannot convert text from xml to md'

        return result
