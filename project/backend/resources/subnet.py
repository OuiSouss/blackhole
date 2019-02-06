from flask_restful import Resource, reqparse, fields, marshal_with

subnets = {
    'subnet1': {
        "id": 1,
        "ip": "203.0.13.0/32",
        "next_hop": "192.0.2.1",
        "communities": [
            "564:65"
        ],
        "created_at": 1456446454,
        "human_created_at" : "Fri, 5 Feb 2019 09:46:56 GMT",
        "modified_at": "null",
        "human_modified_at": "null",
        "last_activation": "Fri, 5 Feb 2019 09:47:00 GMT",
        "activated_since": 4564,
    },
    'subnet2': {
        "id": 2,
        "ip": "3.0.13.0/32",
        "next_hop": "192.0.2.1",
        "communities": [
            "56:655"
        ],
        "created_at": 1456446450,
        "human_created_at" : "Fri, 5 Feb 2019 09:50:00 GMT",
        "modified_at": "null",
        "human_modified_at": "null",
        "last_activation": "Fri, 5 Feb 2019 09:53:00 GMT",
        "activated_since": 4556,
    },
}

subnets_fields = {
    'id': fields.Integer,
    'ip': fields.String,
    'next_hop': fields.String,
    'communities': fields.String,
    'created_at': fields.DateTime,
    'modified_at': fields.DateTime,
    'is_activated': fields.Boolean,
    'last_activation': fields.DateTime,
    'activated_since': fields.Integer,
}

post_parser = reqparse.RequestParser()
post_parser.add_argument(
    "ip", dest="ip", location=["form", "json"], required=True, help="The IP",
)
class Subnet(Resource):
    def get(self):
        return subnets
    
    @marshal_with(subnets_fields)
    def post(self):
        args = post_parser.parse_args()
        subnets = {
            'id': subnets[-1]['id'] + 1,
        }
        return subnets_fields, 201