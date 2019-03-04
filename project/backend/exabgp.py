"""
    Methods to send messages to ExaBGP
"""

from sys import stdout
from time import sleep

def annouce_routes(post):
    for route in post :
        stdout.write('announce route {} next-hop {} community {} \n'.format(route['ip'], route['nexthop'], route['communities']))
        stdout.flush()
        sleep(1)

def annouce_one_route(post):
    stdout.write('announce route {} next-hop {} community {} \n'.format(post['ip'], post['nexthop'], post['communities']))
    stdout.flush()
    sleep(1)

def withdraw_routes(delete):
     for route in delete :
        stdout.write('withdraw route {}\n'.format(route['ip']))
        stdout.flush()
        sleep(1)

def withdraw_one_routes(delete):
     stdout.write('withdraw route {}\n'.format(delete['ip']))
     stdout.flush()
     sleep(1)

def update_routes(patch):
    for route in patch :
        stdout.write('update start \n')
        stdout.write('announce route {} next-hop {} community {} \n'.format(route['ip'], route['nexthop'], route['communities']))
        stdout.write('update end \n')
        stdout.flush()
        sleep(1)

def update_one_route(patch):
    stdout.write('update start \n')
    stdout.write('announce route {} next-hop {} community {} \n'.format(patch['ip'], patch['nexthop'], patch['communities']))
    stdout.write('update end \n')
    stdout.flush()
    sleep(1)
