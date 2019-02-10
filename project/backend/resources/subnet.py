"""
REST API /api/subnet
"""
from datetime import datetime
from flask_restful import Resource, reqparse, fields, marshal_with
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

def create_post_parser():
    """
    Create a parser for POST request which needs
    an IP, the next_hop, and communities on which we need
    to apply the route
    :return: post_parser
    """
    post_parser = reqparse.RequestParser()
    post_parser.add_argument(
        "ip", dest="ip", location=["form", "json"], required=True,
        help="The IP",
    )
    post_parser.add_argument(
        "next_hop", dest="next_hop", location=["form", "json"], required=True,
        help="The next hop",
    )

    post_parser.add_argument(
        "communities", dest="communities", location=["form", "json"],
        required=True, help="The community", action="append"
    )
    return post_parser

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
        args = create_post_parser().parse_args()
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
