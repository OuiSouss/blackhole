from flask_restful import Resource

class Subnet(Resource):
    def get(self):
        return {"message": "Hello, World!"}

    def post(self):
        return {"message": "Hello, World!"}