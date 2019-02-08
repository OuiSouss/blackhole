from flask_restful import Resource, reqparse, fields, marshal_with
from datetime import datetime
import json

subnets = {
    'subnet1': {
        "id": 1,
        "ip": "203.0.13.0/32",
        "next_hop": "192.0.2.1",
        "communities": [
            "564:65"
        ],
        "created_at" : "Fri, 5 Feb 2019 09:46:56 GMT",
        "modified_at": "null",
        "is_activated": False,
        "last_activation": "Fri, 5 Feb 2019 09:47:00 GMT",
    },
    'subnet2': {
        "id": 2,
        "ip": "3.0.13.0/32",
        "next_hop": "192.0.2.1",
        "communities": [
            "56:655"
        ],
        "created_at": "Fri, 5 Feb 2019 09:50:00 GMT",
        "modified_at": "null",
        "is_activated" : True,
        "last_activation": "Fri, 5 Feb 2019 09:53:00 GMT",
    },
}

subnets_fields = {
    'id': fields.Integer,
    'ip': fields.String,
    'next_hop': fields.String,
    'communities': fields.List(fields.String),
    'created_at': fields.DateTime,
    'modified_at': fields.DateTime,
    'is_activated': fields.Boolean,
    'last_activation': fields.DateTime,
}

post_parser = reqparse.RequestParser()
post_parser.add_argument(
    "ip", dest="ip", location=["form", "json"], required=True, help="The IP",
)
post_parser.add_argument(
    "next_hop", dest="next_hop", location=["form", "json"], required=True, 
    help="The next hop",
)

post_parser.add_argument(
    "communities", dest="communities", location=["form", "json"], 
    required=True, help="The community",
)
class Subnet(Resource):
    def get(self):
        return json.dumps(subnets)
    
    @marshal_with(subnets_fields)
    def post(self):
        args = post_parser.parse_args()
        last_subnet = max(subnets.keys())
        id = subnets[last_subnet]['id'] + 1
        subnet_name = "subnet%i" % id
        subnets[subnet_name] = {
            'id': id,
            'ip': args.ip,
            'next_hop': args.next_hop,
            'communities': [args.communities],
            'created_at': datetime.now(),
            'modified_at': datetime.now(),
            'is_activated': True,
            'last_activation': datetime.now(),
        }
        return subnets[subnet_name], 201