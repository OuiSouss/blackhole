from flask_restful import Resource, reqparse, fields, marshal_with
from datetime import datetime
from flask import jsonify

subnets = []

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
    required=True, help="The community", action="append"
)

class Subnet(Resource):
    def get(self):
        return jsonify(subnets)
    
    @marshal_with(subnets_fields)
    def post(self):
        args = post_parser.parse_args()
        id = 1
        if (len(subnets) > 0):
            id = subnets[-1]['id'] + 1
        subnet = {
            'id': id,
            'ip': args.ip,
            'next_hop': args.next_hop,
            'communities': args.communities,
            'created_at': str(datetime.now()),
            'modified_at': str(datetime.now()),
            'is_activated': True,
            'last_activation': str(datetime.now()),
        }
        subnets.append(subnet)
        return subnet, 201