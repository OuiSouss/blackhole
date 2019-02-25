"""
subnets.py
===================
REST API /api/subnets
"""
from flask import jsonify
from flask_restful import Resource, reqparse, fields, marshal_with
from backend.database.funct_base import MongoDB

subnets_fields = {
    'id': fields.String,
    'ip': fields.String,
    'next_hop': fields.String,
    'communities': fields.List(fields.String),
    'created_at': fields.String,
    'modified_at': fields.String,
    'is_activated': fields.Boolean,
    'last_activation': fields.String,
}

class Subnets(Resource):
    """
    Subnets class to provide GET, POST methods.
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
            action='append'
        )
        self.mongo_db = MongoDB('Route')
        super(Subnets, self).__init__()


    def get(self):
        """
        get GET Method

        GET /api/subnets

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
    def post(self):
        """
        post POST Method

        POST api/subnets

        {
            ip: <ip>
            next_hop: <next_hop>
            communities: <communities>
        }

        :return: The created subnet
        :rtype: dict, HTTP status
        """
        args = self.general_parser.parse_args()
        subnet = {
            'ip': args.ip,
            'next_hop': args.next_hop,
            'communities': args.communities,
        }
        self.mongo_db.add_route(subnet)
        return subnet, 201
