"""
exabgp.py
===================
REST API /api/exabgp
"""

from sys import stdout
from io import StringIO
from time import sleep
from flask_restful import Resource

class ExaBGP(Resource):
    """
    ExaBGP class to provide methods to send routes to ExaBGP.
    """
    def __init__(self, output_file_path):
        self.output = output_file_path
        self.input = StringIO()
        super(ExaBGP, self).__init__('output.txt')

    def exabgp_response(self, file_d):
        """
        Simulation of an ExaBGP's response
        """
        stin = StringIO()
        stin.write('yes')
        response = stin.getvalue()
        if response == '':
            response = 'No response'
        file_d.write(response + '\n')
        return response

    def action(self, cmd):
        """
        Execute a command to ExaBGP
        :param cmd: Command to execute. Can be shutdown, reload, retart only.
        :type cmd: str
        :return:  The ExaBGP's response
        """
        out = open(self.output, "a")
        stdout.write(cmd+'\n')
        stdout.flush()
        sleep(1)
        response = self.exabgp_response(out)
        out.close()
        return response

    def announce_routes(self, post):
        """
        Announce a list of routes to add for ExaBGP
        :param post: A dictionnary with _id and its value
        :type post: dict
        :return: A list contains all of the ExaBGP's responses
        """
        responses = []
        out = open(self.output, "a")
        for route in post:
            stdout.write('announce route {} next-hop {} community {} \n'\
                         .format(route['ip'],
                                 route['next_hop'],
                                 route['communities']))
            stdout.flush()
            sleep(1)
            responses.append(self.exabgp_response(out))
        out.close()
        return responses

    def announce_one_route(self, post):
        """
        Announce a route to send to ExaBGP
        :param post: A dictionnary with _id and its value
        :type post: dict
        :return: The ExaBGP's response
        """
        out = open(self.output, "a")
        stdout.write('announce route {} next-hop {} community {} \n'\
                     .format(post['ip'],
                             post['next_hop'],
                             post['communities']))
        stdout.flush()
        sleep(1)
        response = self.exabgp_response(out)
        out.close()
        return response+'\n'

    def withdraw_routes(self, delete):
        """
        Announce a list of routes to delete for ExaBGP
        :param delete: A dictionnary with _id and its value
        :type delete: dict
        :return: A list contains all of the ExaBGP's responses
        """
        responses = []
        out = open(self.output, "a")
        for route in delete:
            stdout.write('withdraw route {}\n'.format(route['ip']))
            stdout.flush()
            sleep(1)
            responses.append(self.exabgp_response(out))
        out.close()
        return responses

    def withdraw_one_routes(self, delete):
        """
        Announce a route to delete for ExaBGP.
        :param delete: A dictionnary with _id and its value
        :type delete: dict
        :return:  The ExaBGP's response
        """
        out = open(self.output, "a")
        stdout.write('withdraw route {}\n'.format(delete['ip']))
        stdout.flush()
        sleep(1)
        response = self.exabgp_response(out)
        out.close()
        return response

    def update_routes(self, patch):
        """
        Announce a list of routes to update for ExaBGP
        :param patch: A dictionnary with _id and its value
        :type patch: dict
        :return: A list contains all of the ExaBGP's responses
        """
        responses = []
        out = open(self.output, "a")
        for route in patch:
            stdout.write('update start \n')
            stdout.write('announce route {} next-hop {} community {} \n'\
                        .format(route['ip'],
                                route['next_hop'],
                                route['communities']))
            stdout.write('update end \n')
            stdout.flush()
            sleep(1)
            responses.append(self.exabgp_response(out))
            out.close()
        return responses

    def update_one_route(self, patch):
        """
        Announce a route to update for ExaBGP.
        :param patch: A dictionnary with _id and its value
        :type patch: dict
        :return:  The ExaBGP's response
        """
        out = open(self.output, "a")
        stdout.write('update start \n')
        stdout.write('announce route {} next-hop {} community {} \n'\
                     .format(patch['ip'],
                             patch['next_hop'],
                             patch['communities']))
        stdout.write('update end \n')
        stdout.flush()
        sleep(1)
        response = self.exabgp_response(out)
        out.close()
        return response
