"""
    Methods to send messages to ExaBGP
"""

from sys import stdout, stdin
from time import sleep

def annouce_routes(post):
    """
    Announce a list of routes to add for ExaBGP
    :param post: A dictionnary with _id and its value
    :type post: dict
    :return: A dictionnary contains all of the ExaBGP's responses
    """
    response = {}
    for route in post:
        stdout.write('announce route {} next-hop {} community {} \n'.format(route['ip'], route['nexthop'], route['communities']))
        stdout.flush()
        sleep(1)
        response.update(stdin.read())
    return response

def annouce_one_route(post):
    """
    Announce a route to send to ExaBGP
    :param post: A dictionnary with _id and its value
    :type post: dict
    :return: The ExaBGP's response
    """
    stdout.write('announce route {} next-hop {} community {} \n'.format(post['ip'], post['nexthop'], post['communities']))
    stdout.flush()
    sleep(1)
    response = stdin.read()
    return response

def withdraw_routes(delete):
    """
    Announce a list of routes to delete for ExaBGP
    :param delete: A dictionnary with _id and its value
    :type delete: dict
    :return: A dictionnary contains all of the ExaBGP's responses
    """
    response = {}
    for route in delete:
        stdout.write('withdraw route {}\n'.format(route['ip']))
        stdout.flush()
        sleep(1)
        response.update(stdin.read())
    return response

def withdraw_one_routes(delete):
    """
    Announce a route to delete for ExaBGP.
    :param delete: A dictionnary with _id and its value
    :type delete: dict
    :return:  The ExaBGP's response
    """
    stdout.write('withdraw route {}\n'.format(delete['ip']))
    stdout.flush()
    sleep(1)
    response = stdin.read()
    return response

def update_routes(patch):
    """
    Announce a list of routes to update for ExaBGP
    :param patch: A dictionnary with _id and its value
    :type patch: dict
    :return: A dictionnary contains all of the ExaBGP's responses
    """
    response = {}
    for route in patch:
        stdout.write('update start \n')
        stdout.write('announce route {} next-hop {} community {} \n'.format(route['ip'], route['nexthop'], route['communities']))
        stdout.write('update end \n')
        stdout.flush()
        sleep(1)
        response.update(stdin.read())
    return response

def update_one_route(patch):
    """
    Announce a route to update for ExaBGP.
    :param patch: A dictionnary with _id and its value
    :type patch: dict
    :return:  The ExaBGP's response
    """
    stdout.write('update start \n')
    stdout.write('announce route {} next-hop {} community {} \n'.format(patch['ip'], patch['nexthop'], patch['communities']))
    stdout.write('update end \n')
    stdout.flush()
    sleep(1)
    response = stdin.read()
    return response
