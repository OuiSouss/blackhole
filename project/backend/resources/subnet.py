"""
REST API /api/subnet
"""
from datetime import datetime
from flask_restful import Resource, reqparse, fields, marshal_with
from flask import jsonify, abort

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

def create_delete_parser():
    """
    Create a parser for DELETE request which need a ID of a resource
    :return: delete_parser
    """
    delete_parser = reqparse.RequestParser()
    delete_parser.add_argument(
        "id", dest="id", location=["form", "json"], required=True,
        help="The ID",
    )
    return delete_parser

class Subnet(Resource):
    """
    Subnet class to provide GET, POST, PUT, DELETE and PATCH methods to
    frontend. This class communicates with ExaBGP and store info in MongoDB
    database.
    """

    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument(
            "ip", dest="ip", location=["form", "json"], required=True,
            help="The IP",
        )
        self.reqparser.add_argument(
            "next_hop", dest="next_hop", location=["form", "json"],
            required=True, help="The next hop",
        )
        self.reqparser.add_argument(
            "communities", dest="communities", location=["form", "json"],
            required=True, help="The community", action="append"
        )
        super(Subnet, self).__init__()


    def get(self):
        """
        GET request
        :return: List of subnets in json stored
        """
        return jsonify(subnets)

    @marshal_with(subnets_fields)
    def post(self):
        """
        POST request create a new subnet
        It will announced to ExaBGP and store in database
        :return: The new subnet with 201 status
        """
        args = self.reqparser.parse_args()
        id_subnet = 1
        if subnets:
            id_subnet = subnets[-1]['id'] + 1
        subnet = {
            'id': id_subnet,
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

    @marshal_with(subnets_fields)
    def put(self):
        """
        PUT request need all fields infos
        :return: The subnet modify
        """
        put_parser = self.reqparser.copy()
        put_parser.add_argument(
            "id", dest="id", location=["form", "json"], required=True,
            help="The ID",
        )
        put_parser.add_argument(
            "is_activated", dest="is_activated", location=["form", "json"],
            required=True, help="The activation",
        )
        args = put_parser.parse_args()
        index_id = None
        for i in range(len(subnets)):
            if subnets[i]['id'] == int(args.id):
                index_id = i
        if index_id is None:
            abort(404)
        last_activation_state = subnets[index_id]['is_activated']
        last_activation = subnets[index_id]['last_activation']
        if bool(args.is_activated) != last_activation_state:
            last_activation = str(datetime.now())
        subnet = {
            'id': args.id,
            'ip': args.ip,
            'next_hop': args.next_hop,
            'communities': args.communities,
            'created_at': subnets[index_id]['created_at'],
            'modified_at': str(datetime.now()),
            'is_activated': args.is_activated,
            'last_activation': last_activation,
        }
        subnets[i] = subnet
        return subnet, 200

    @marshal_with(subnets_fields)
    def delete(self):
        """
        DELETE request delete a subnet which has a specific ID
        """
        args = create_delete_parser().parse_args()
        for s in subnets:
            if s["id"] == int(args.id):
                subnets.remove(s)
                return {"message": "Success"}, 204
        return 404
