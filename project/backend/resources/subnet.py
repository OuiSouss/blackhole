"""
subnet.py
===================
REST API /api/subnet
"""
from flask import jsonify
from flask_restful import Resource, reqparse, fields, marshal_with
from bson import ObjectId
from backend.database.funct_base import MongoDB

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
            'ip', dest='ip', location=['form', 'json'], required=True,
            help='The IP',
        )
        self.general_parser.add_argument(
            'next_hop', dest='next_hop', location=['form', 'json'],
            required=True, help='The next hop',
        )
        self.general_parser.add_argument(
            'communities', dest='communities', location=['form', 'json'],
            required=True, help='The community', action='append'
        )
        self.simple_parser = reqparse.RequestParser()
        self.simple_parser.add_argument(
            'id', dest='id', location=['form', 'json'], required=True,
            help='The ID',
        )
        self.mongo_db = MongoDB('Route')
        super(Subnet, self).__init__()

    def get(self):
        """
        get GET Method

        GET /api/subnet

        :return: List of subnets stored on database
        :rtype: list
        """
        items = self.mongo_db.get_all_routes()
        for i in items:
            _id = i['_id']
            del i['_id']
            i['id'] = _id
        return jsonify(items)

    @marshal_with(subnets_fields)
    def put(self):
        """
        put PUT Method

        PUT api/subnet?id=<id>&ip=<ip>&next_hop=<next_hop>&\
            communities=<communities>&is_activated=<is_activated>

        :return: The updated subnet
        :rtype: dict, HTTP status
        """
        put_parser = self.general_parser.copy()
        put_parser.add_argument(
            'id', dest='id', location=['form', 'json'], required=True,
            help='The ID',
        )
        put_parser.add_argument(
            'is_activated', dest='is_activated', location=['form', 'json'],
            required=True, help='The activation',
        )
        args = put_parser.parse_args()
        is_activated = True
        if (args.is_activated == 'false' or args.is_activated == 'False'):
            is_activated = False
        subnet = {
            '_id': ObjectId(args.id),
            'ip': args.ip,
            'next_hop': args.next_hop,
            'communities': args.communities,
            'is_activated': is_activated,
        }
        subnet = self.mongo_db.put_route(subnet)
        return subnet, 200

    @marshal_with(subnets_fields)
    def patch(self):
        """
        patch PATCH Method

        PATCH api/subnet?id=<id>&is_activated=<is_activated>

        :return: The updated subnet
        :rtype: dict, HTTP status
        """
        patch_parser = self.simple_parser.copy()
        patch_parser.add_argument(
            'is_activated', dest='is_activated', location=['form', 'json'],
            required=True, help='The activation',
        )
        args = patch_parser.parse_args()
        is_activated = True
        if (args.is_activated == 'false' or args.is_activated == 'False'):
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
        delete DELETE Method

        DELETE api/subnet?id=<id>
        """
        args = self.simple_parser.parse_args()
        self.mongo_db.delete_route({'_id' : ObjectId(args.id)})
