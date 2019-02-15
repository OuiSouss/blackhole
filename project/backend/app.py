"""
Define a blueprint and all resources
"""
from flask import Blueprint
from flask_restful import Api

from backend.resources.subnet import Subnet

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(Subnet, '/subnet')
