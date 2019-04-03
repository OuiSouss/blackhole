"""
subnets.py
===================
REST API /api/subnets
"""
from flask import jsonify
from flask_restful import Resource, reqparse, fields, marshal_with, inputs
from backend.database.funct_base import MongoDB
from backend.funct_exabgp import ExaBGP
from backend.resources.settings import URL_EXABGP

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
        NETWORK_REGEX = '^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(/(3[0-2]|[1-2][0-9]|[0-9]))$'
        IP_REGEX = '^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        COMMUNITIES_REGEX = '^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])\:([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$'
        self.general_parser = reqparse.RequestParser()
        self.general_parser.add_argument(
            'ip', dest='ip', location=['form', 'json'], required=True,
            help='The IP with d.d.d.d/m form 0 < d < 255 and 0 < m < 32',
            type=inputs.regex(NETWORK_REGEX),
        )
        self.general_parser.add_argument(
            'next_hop', dest='next_hop', location=['form', 'json'],
            required=True, help='The next hop with d.d.d.d form 0 < d < 255',
            type=inputs.regex(IP_REGEX),
        )
        self.general_parser.add_argument(
            'communities', dest='communities', location=['form', 'json'],
            help="The communities with a:b form, a and b between 0 and 65535",
            action='append', type=inputs.regex(COMMUNITIES_REGEX),
        )
        self.mongo_db = MongoDB('Route')
        self.exabgp = ExaBGP(URL_EXABGP)
        super(Subnets, self).__init__()

    def get(self):
        """
        get GET Method

        GET /api/subnets

        :return: List of subnets stored on database
        :rtype: list
        """
        items = self.mongo_db.get_all_routes()
        self.exabgp.announces_routes(items)
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
        communities = None
        if (args.communities is not None):
            communities = list(args.communities.split(','))
        subnet = {
            'ip': args.ip,
            'next_hop': args.next_hop,
            'communities': communities,
        }
        response = self.exabgp.announce_one_route(subnet)
        if response != 200:
            return subnet, 404
        subnet_id = self.mongo_db.add_route(subnet)
        subnet['id'] = subnet_id
        return subnet, 201
