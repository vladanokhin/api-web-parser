from flask_restful.reqparse import RequestParser
from flask_restful import Resource

from src.parser import Parser
from configs.app import AppConfig
from src.helpers import api_result


class ParserApi(Resource):

    URL = "/collect"

    def __init__(self):
        super().__init__()
        self.cfg = AppConfig()
        self.reqparse = RequestParser()
        self.reqparse.add_argument("url", required=True, type=str)
        self.reqparse.add_argument("timeout", type=int)
        self.reqparse.add_argument("proxy", type=str)
        self.reqparse.add_argument("method_parse",
                                   type=str,
                                   choices=self.cfg.METHOD_OF_PARSE,
                                   default=self.cfg.METHOD_OF_PARSE[0])

    @api_result
    def post(self):
        args = self.reqparse.parse_args()
        parser = Parser(url=args.url, timeout=args.timeout, proxy=args.proxy, method_parse=args.method_parse)
        result = parser.parse()

        return result
