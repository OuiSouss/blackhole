"""
app.py
===================
Define a blueprint and all resources
"""
from flask import Blueprint
from flask_restful import Api

from backend.resources.subnet import Subnet
from backend.resources.subnets import Subnets

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(Subnet, '/subnet/<object_id:subnet_id>')
api.add_resource(Subnets, '/subnets')
