from flask_restful import Resource, reqparse, fields, marshal_with
from datetime import datetime
import json

subnets = {
}

subnets_fields = {
    'id': fields.Integer,
    'ip': fields.String,
    'next_hop': fields.String,
    'communities': fields.List(fields.String),
    'created_at': fields.String,
    'modified_at': fields.String,
    'is_activated': fields.Boolean,
    'last_activation': fields.String,
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
        return subnets
    
    @marshal_with(subnets_fields)
    def post(self):
        args = post_parser.parse_args()
        id = 1
        if (len(subnets.keys()) > 0):
            last_subnet = max(subnets.keys())
            id = subnets[last_subnet]['id'] + 1
        subnet_name = "subnet%i" % id
        subnets[subnet_name] = {
            'id': id,
            'ip': args.ip,
            'next_hop': args.next_hop,
            'communities': [args.communities],
            'created_at': str(datetime.now()),
            'modified_at': str(datetime.now()),
            'is_activated': True,
            'last_activation': str(datetime.now()),
        }
        return subnets[subnet_name], 201