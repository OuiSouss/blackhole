"""
REST API /api/subnet
"""
from datetime import datetime
from flask import jsonify, abort
from flask_restful import Resource, reqparse, fields, marshal_with
from bson import ObjectId
from backend.database.funct_base import MongoDB

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

class Subnet(Resource):
    """
    Subnet class to provide GET, POST, PUT, DELETE and PATCH methods to
    frontend. This class communicates with ExaBGP and store info in MongoDB
    database.
    """

    def __init__(self):
        self.general_parser = reqparse.RequestParser()
        self.general_parser.add_argument(
            "ip", dest="ip", location=["form", "json"], required=True,
            help="The IP",
        )
        self.general_parser.add_argument(
            "next_hop", dest="next_hop", location=["form", "json"],
            required=True, help="The next hop",
        )
        self.general_parser.add_argument(
            "communities", dest="communities", location=["form", "json"],
            required=True, help="The community", action="append"
        )
        self.simple_parser = reqparse.RequestParser()
        self.simple_parser.add_argument(
            "id", dest="id", location=["form", "json"], required=True,
            help="The ID",
        )
        self.mongo_db = MongoDB("Route")
        super(Subnet, self).__init__()


    def get(self):
        """
        GET request
        :return: List of subnets in json stored
        """
        items = self.mongo_db.get_all_routes()
        for i in items:
            _id = i['_id']
            del i['_id']
            i['id'] = _id
        return jsonify(items)

    @marshal_with(subnets_fields)
    def post(self):
        """
        POST request create a new subnet
        It will announced to ExaBGP and store in database
        :return: The new subnet with 201 status
        """
        args = self.general_parser.parse_args()
        subnet = {
            'ip': args.ip,
            'next_hop': args.next_hop,
            'communities': args.communities,
        }
        self.mongo_db.add_route(subnet)
        return subnet, 201

    @marshal_with(subnets_fields)
    def put(self):
        """
        PUT request need all fields infos except dates
        :return: The subnet modify
        """
        put_parser = self.general_parser.copy()
        put_parser.add_argument(
            "id", dest="id", location=["form", "json"], required=True,
            help="The ID",
        )
        put_parser.add_argument(
            "is_activated", dest="is_activated", location=["form", "json"],
            required=True, help="The activation",
        )
        args = put_parser.parse_args()
        is_activated = True
        if (args.is_activated == "false" or args.is_activated == "False"):
            is_activated = False
        subnet = {
            '_id': ObjectId(args.id),
            'ip': args.ip,
            'next_hop': args.next_hop,
            'communities': args.communities,
            'is_activated': is_activated,
        }
        subnet = self.mongo_db.update_route(subnet)
        return subnet, 200

    @marshal_with(subnets_fields)
    def patch(self):
        """
        PATCH request need ID and is_activated
        :return: The modify subnet
        """
        patch_parser = self.simple_parser.copy()
        patch_parser.add_argument(
            "is_activated", dest="is_activated", location=["form", "json"],
            required=True, help="The activation",
        )
        args = patch_parser.parse_args()
        is_activated = True
        if (args.is_activated == "false" or args.is_activated == "False"):
            is_activated = False
        subnet = {
            '_id': ObjectId(args.id),
            'is_activated': is_activated
        }
        subnet = self.mongo_db.update_route(subnet)
        return subnet, 200


    @marshal_with(subnets_fields)
    def delete(self):
        """
        DELETE request delete a subnet which has a specific ID
        """
        args = self.simple_parser.parse_args()
        self.mongo_db.delete_route({'_id' : ObjectId(args.id)})
