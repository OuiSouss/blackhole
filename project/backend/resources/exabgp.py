"""
exabgp.py
===================
REST API /api/exabgp
"""
from flask import abort
from flask_restful import Resource
from backend.funct_exabgp import ExaBGP
from backend.resources.settings import URL_EXABGP

exabgp_cmd = {
    'shutdown',
    'restart',
    'reload',
    'reset',
    'version',
    'show neighbor',
    'teardown'
}

class Exabgp(Resource):
    """
    Exabgp class to provide GET method.
    """

    def __init__(self):
        """
        Initialization of Exabgp class.
        """
        self.exabgp = ExaBGP(URL_EXABGP)
        super(Exabgp, self).__init__()

    def post(self, command):
        """
        Execute a command on the list to ExaBGP
        """
        if command not in exabgp_cmd:
            abort(404,
                  description='Command does not exist : {}'\
                          .format(command))
        response = self.exabgp.action(command)
        response = {
            "response": response.text.strip('\n'),
            "status": response.status_code
        }
        return response
