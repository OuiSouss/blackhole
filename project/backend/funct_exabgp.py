"""
Class ExaBGP
"""
import os
import subprocess
from flask import abort
import requests

class ExaBGP:
    """
    ExaBGP class to provide methods to send routes to ExaBGP.
    """
    def __init__(self, url_exabgp):
        """
        Initialization
        """
        self.url_exabgp = url_exabgp

    def is_exabgp_running(self):
        """
        is_exabgp_running check is exabgp is running

        :return: True if an instance of exabgp is find, false if not
        :rtype: boolean
        """

        exabgp_pid = 0
        try:
            exabgp_pid = int(subprocess.check_output(['pgrep', 'exabgp'])\
                             .decode('utf-8').rstrip())
            os.kill(exabgp_pid, 0)
        except subprocess.CalledProcessError:
            return False
        except OSError:
            return False
        return True

    def action(self, command):
        """
        Execute a command to ExaBGP
        :param cmd: Command to execute. Can be shutdown, reload, retart only.
        :type cmd: str
        :return:  The ExaBGP's response
        """
        if not self.is_exabgp_running():
            abort(503, description='ExaBGP is not running')
        response = requests.post(self.url_exabgp, data={'command' : command})
        return response

    def announce_one_route(self, post):
        """
        Announce a route to send to ExaBGP
        :param post: A dictionnary with _id and its value
        :type post: dict
        :return: The ExaBGP's response
        """
        if not self.is_exabgp_running():
            abort(503, description='ExaBGP is not running')
        if post['communities'] is None:
            command = 'announce route {} next-hop {} \n'\
                     .format(post['ip'],
                             post['next_hop'])
        else:
            command = 'announce route {} next-hop {} community {} \n'\
                     .format(post['ip'],
                             post['next_hop'],
                             post['communities'])

        response = requests.post(self.url_exabgp, data={'command' : command})
        return response.status_code

    def announces_routes(self, post):
        """
        Announce routes to send to ExaBGP
        :param post: A dictionnary with routes
        :type post: dict
        :return: The ExaBGP's response
        """
        if not self.is_exabgp_running():
            abort(503, description='ExaBGP is not running')
        for route in post:
            if route['is_activated'] is True:
                response = self.announce_one_route(route)
                if response != 200:
                    abort(404, description='Can\'t announce route')
        return 200

    def withdraw_one_route(self, delete):
        """
        Announce a route to delete for ExaBGP.
        :param delete: A dictionnary with _id and its value
        :type delete: dict
        :return:  The ExaBGP's response
        """
        if not self.is_exabgp_running():
            abort(503, description='ExaBGP is not running')
        if delete['communities'] is None:
            command = 'withdraw route {} next-hop {}\n'\
                     .format(delete['ip'],
                             delete['next_hop'])
        else:
            command = 'withdraw route {} next-hop {} community {} \n'\
                     .format(delete['ip'],
                             delete['next_hop'],
                             delete['communities'])
        response = requests.post(self.url_exabgp, data={'command' : command})
        return response.status_code

    def update_one_route(self, patch):
        """
        Announce a route to update for ExaBGP.
        :param patch: A dictionnary with _id and its value
        :type patch: dict
        :return:  The ExaBGP's response
        """
        if not self.is_exabgp_running():
            abort(503, description='ExaBGP is not running')
        response = self.withdraw_one_route(patch)
        if response != 200:
            abort(404, description='Can\'t update route at withdraw time')
        if patch['is_activated'] is True:
            response = self.announce_one_route(patch)
            if response != 200:
                abort(404, description='Can\'t udpdate route at announce time')
        return response
