"""
subnet.py
===================
REST API /api/subnet
"""
from flask import jsonify, abort
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

class Subnet(Resource):
    """
    Subnet class to provide GET, PUT, DELETE and PATCH methods to
    frontend. This class communicates with ExaBGP and store info in MongoDB
    database.
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
            help='The communities with a:b form, a and b between 0 and 65535',
            type=inputs.regex(COMMUNITIES_REGEX),
        )
        self.simple_parser = reqparse.RequestParser()
        self.simple_parser.add_argument(
            'is_activated', dest='is_activated', location=['form', 'json'],
            required=True, help='The boolean activation',
        )
        self.exabgp = ExaBGP(URL_EXABGP)
        self.mongo_db = MongoDB('Route')
        super(Subnet, self).__init__()

    def get(self, subnet_id):
        """
        get GET Method

        GET /api/subnet/<subnet_id>
        Abort with 404 if the subnet is not in database

        :param subnet_id: id of a subnet in str format
        :type subnet_id: str
        :return: The subnet with subnet_id
        :rtype: dict
        """
        subnet = self.mongo_db.get_route_by_id({'_id' : subnet_id})
        if subnet is None:
            abort(404,
                  message='Cannot find a route with id : {}'.format(subnet_id))
        _id = subnet['_id']
        del subnet['_id']
        subnet['id'] = _id
        return jsonify(subnet)

    @marshal_with(subnets_fields)
    def put(self, subnet_id):
        """
        put PUT Method

        PUT api/subnet/<object_id:subnet_id>

        {
            ip: <ip>
            next_hop: <next_hop>
            communities: <communities>
            is_activated: <is_activated>
        }

        :param subnet_id: id of a subnet in str format
        :type subnet_id: str
        :return: The updated subnet
        :rtype: dict, HTTP status
        """
        subnet = self.mongo_db.get_route_by_id({'_id' : subnet_id})
        if subnet is None:
            abort(404,
                  message='Cannot find a route with id : {}'.format(subnet_id))
        put_parser = self.general_parser.copy()
        put_parser.add_argument(
            'is_activated', dest='is_activated', location=['form', 'json'],
            required=True, help='The activation',
        )
        args = put_parser.parse_args()
        is_activated = True
        if (args.is_activated == 'false' or args.is_activated == 'False'):
            is_activated = False
        subnet['ip'] = args.ip
        subnet['next_hop'] = args.next_hop
        subnet['communities'] = None
        if (args.communities is not None):
            subnet['communities'] = list(args.communities.split(','))
        subnet['is_activated'] = is_activated
        subnet = self.mongo_db.put_route(subnet)
        response = self.exabgp.update_one_route(subnet)
        if response != 200:
            abort(404,
                  message='Cannot update the route on ExaBGP with id : {}'\
                          .format(subnet_id))
        subnet = self.mongo_db.put_route(subnet)
        return subnet, 200

    @marshal_with(subnets_fields)
    def patch(self, subnet_id):
        """
        patch PATCH Method

        PATCH api/subnet/<object_id:subnet_id>/

        {
            is_activated: <is_activated>
        }

        :return: The updated subnet
        :rtype: dict, HTTP status
        """
        patch_parser = self.simple_parser.copy()
        args = patch_parser.parse_args()
        is_activated = True
        if (args.is_activated == 'false' or args.is_activated == 'False'):
            is_activated = False
        patch = self.mongo_db.get_route_by_id({'_id' : subnet_id})
        if patch is None:
            abort(404,
                  message='Cannot find a route with id : {}'.format(subnet_id))
        patch['is_activated'] = is_activated
        patch['id'] = subnet_id
        subnet = {
            '_id': subnet_id,
            'is_activated': is_activated
        }
        response = self.exabgp.update_one_route(patch)
        if response != 200:
            abort(404,
                  message='Cannot update the route on ExaBGP with id : {}'\
                          .format(subnet_id))
        subnet = self.mongo_db.update_route(subnet)
        return patch, 200


    @marshal_with(subnets_fields)
    def delete(self, subnet_id):
        """
        delete DELETE Method

        DELETE api/subnet/<object_id:subnet_id>
        """
        subnet = self.mongo_db.get_route_by_id({'_id' : subnet_id})
        response = self.exabgp.withdraw_one_route(subnet)
        if response != 200:
            abort(404,
                  message='Cannot delete the route on ExaBGP with id : {}'\
                          .format(subnet_id))
        self.mongo_db.delete_route({'_id' : subnet_id})
        return subnet, 200
