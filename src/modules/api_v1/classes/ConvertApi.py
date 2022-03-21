from flask_restful import Resource, reqparse


class ConvertApi(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()


    def get(self):
        return {'class': 'ConvertApi'}
