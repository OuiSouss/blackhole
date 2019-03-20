"""
Class ExaBGP
"""

from sys import stdout
from io import StringIO
from time import sleep

class ExaBGP:
    """
    ExaBGP class to provide methods to send routes to ExaBGP.
    """
    def __init__(self, output_file_path):
        """
        Initialization
        """
        self.output = output_file_path
        self.input = StringIO()

    def exabgp_response(self, file_d):
        """
        Simulation of an ExaBGP's response
        """
        stin = self.input
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
        out = open(self.output, "w")
        stdout.write(cmd+'\n')
        stdout.flush()
        sleep(1)
        response = self.exabgp_response(out)
        out.close()
        return response

    def announce_one_route(self, post):
        """
        Announce a route to send to ExaBGP
        :param post: A dictionnary with _id and its value
        :type post: dict
        :return: The ExaBGP's response
        """
        out = open(self.output, "w")
        stdout.write('announce route {} next-hop {} community {} \n'\
                     .format(post['ip'],
                             post['next_hop'],
                             post['communities']))
        stdout.flush()
        sleep(1)
        response = self.exabgp_response(out)
        out.close()
        return response

    def withdraw_one_route(self, delete):
        """
        Announce a route to delete for ExaBGP.
        :param delete: A dictionnary with _id and its value
        :type delete: dict
        :return:  The ExaBGP's response
        """
        out = open(self.output, "w")
        stdout.write('withdraw route {}\n'.format(delete['ip']))
        stdout.flush()
        sleep(1)
        response = self.exabgp_response(out)
        out.close()
        return response

    def update_one_route(self, patch):
        """
        Announce a route to update for ExaBGP.
        :param patch: A dictionnary with _id and its value
        :type patch: dict
        :return:  The ExaBGP's response
        """
        out = open(self.output, "w")
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
