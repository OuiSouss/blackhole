"""
Define some requests with JSON to call API REST
"""
from django.conf import settings
import requests

def post_new_route(route):
    """
    POST method

    :param route: the dict who contain the data
    :type route: dict
    """
    requests.post(settings.API_URL,
                  json={
                      'ip': str(route.ip),
                      'communities': str(route.community),
                      'next_hop': str(route.next_hop)})

def delete_route(ident):
    """
    DELETE method

    :param ident: the id of the route who will be delete.
    :type ident: String
    """
    requests.delete(settings.API_URL,
                    json={'id': ident})

def enable_disable_route(ident, boolean):
    """
    PATCH method

    :param ident: the id of the route who will be enable or disable.
    :type ident: String
    :param boolean: check if we want to disable (False) or enable (True).
    :type boolean: bool
    """
    requests.patch(settings.API_URL,
                   json={
                       'id': ident,
                       'is_activated': boolean})
