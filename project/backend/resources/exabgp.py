"""
exabgp.py
===================
REST API /api/exabgp
"""
from flask import abort
from flask_restful import Resource, reqparse
from backend.funct_exabgp import ExaBGP

exabgp_cmd = {
    'shutdown',
    'restart',
    'reload'
}

class Exabgp(Resource):
    """
    Exabgp class to provide GET method.
    """

    def __init__(self):
        """
        Initialization of Exabgp class.
        """
        self.general_parser = reqparse.RequestParser()
        self.exabgp = ExaBGP()
        super(Exabgp, self).__init__()

    def get(self):
        """
        Execute a command on the list to ExaBGP
        """
        cmd = self.general_parser.copy()
        cmd.add_argument(
            'command', dest='command', location=['form', 'json'], required=True,
            help='The command',
        )
        arg = cmd.parse_args()
        if arg['command'] not in exabgp_cmd:
            abort(404,
                  message='Command does not exist : {}'\
                          .format(arg['command']))
        response = self.exabgp.action(arg['command'])
        if response != 'yes':
            abort(404,
                  message='Cannot launch command : {}'\
                          .format(arg['command']))
        return 200
