"""
Class ExaBGP
"""
from flask import abort
import requests

class ExaBGP:
    """
    ExaBGP class to provide methods to send routes to ExaBGP.
    """

    def __init__(self, url_exabgp):
        self.url_exabgp = url_exabgp

    def action(self, command):
        """
        action Execute a command to ExaBGP

        :param command: Command to execute. Can be shutdown, reload, retart only.
        :type command: str
        :return: ExaBGP response
        :rtype: HTTP response
        """

        response = requests.post(self.url_exabgp, data={'command' : command})
        if response.ok:
            return response
        return None

    def announce_one_route(self, post):
        """
        announce_one_route Announce a route to send to ExaBGP

        :param post: Dict with id and its values
        :type post: dict
        :return: ExaBGP response
        :rtype: HTTP response
        """

        command = ''
        if post['communities'] is None:
            command = 'announce route {} next-hop {} \n'\
                     .format(post['ip'],
                             post['next_hop'])
        else:
            for com in  post['communities']:
                community = '[%s]' % com
            command = 'announce route {} next-hop {} community {} \n'\
                     .format(post['ip'],
                             post['next_hop'],
                             community)

        response = requests.post(self.url_exabgp, data={'command' : command})
        return response.status_code

    def announces_routes(self, post):
        """
        announces_routes Announce routes to send to ExaBGP

        :param post: Dict with routes
        :type post: dict
        :return: ExaBGP response
        :rtype: HTTP response
        """

        for route in post:
            if route['is_activated'] is True:
                response = self.announce_one_route(route)
                if response != 200:
                    abort(404, description='Can\'t announce route')
        return 200

    def withdraw_one_route(self, delete):
        """
        withdraw_one_route Announce a route to delete for ExaBGP.

        :param delete: Dict with _id and its values
        :type delete: dict
        :return: ExaBGP response
        :rtype: HTTP response
        """

        command = ''
        if delete['communities'] is None:
            command = 'withdraw route {} next-hop {}\n'\
                     .format(delete['ip'],
                             delete['next_hop'])
        else:
            for com in  delete['communities']:
                community = '[%s]' % com
            command = 'withdraw route {} next-hop {} community {} \n'\
                     .format(delete['ip'],
                             delete['next_hop'],
                             community)
        response = requests.post(self.url_exabgp, data={'command' : command})
        return response.status_code

    def update_one_route(self, patch):
        """
        update_one_route Announce a route to update for ExaBGP.

        :param patch: Dict with _id and its values
        :type patch: dict
        :return: ExaBGP response
        :rtype: HTTP response
        """

        response = self.withdraw_one_route(patch)
        if response != 200:
            abort(404, description='Can\'t update route at withdraw time')
        if patch['is_activated'] is True:
            response = self.announce_one_route(patch)
            if response != 200:
                abort(404, description='Can\'t udpdate route at announce time')
        return response
