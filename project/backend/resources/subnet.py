"""
subnet.py
===================
REST API /api/subnet
"""
from flask import jsonify, abort
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
            action='append'
        )
        self.simple_parser = reqparse.RequestParser()
        self.simple_parser.add_argument(
            'is_activated', dest='is_activated', location=['form', 'json'],
            required=True, help='The activation',
        )
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

        PUT api/subnet/<object_id:subnet_id>/

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
        subnet['communities'] = args.communities
        subnet['is_activated'] = is_activated
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
        subnet = {
            '_id': subnet_id,
            'is_activated': is_activated
        }
        subnet = self.mongo_db.update_route(subnet)
        return subnet, 200


    @marshal_with(subnets_fields)
    def delete(self, subnet_id):
        """
        delete DELETE Method

        DELETE api/subnet/<object_id:subnet_id>
        """
        self.mongo_db.delete_route({'_id' : subnet_id})
