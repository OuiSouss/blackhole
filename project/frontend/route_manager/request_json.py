"""
Define some requests with JSON to call API REST.
"""
from django.conf import settings
import requests

def post_new_route(ip, next_hop, communities):
    """
    POST method

    //TODO
    """
    return requests.post(settings.API_URL,
                  json={
                      'ip': ip,
                      'communities': communities,
                      'next_hop': next_hop})

def put_route(ident, ip, next_hop, communities):
    """
    PUT method

    :param ident: the id of the route who will be update.
    :type ident: String
    :param ip: the ip of the route.
    :type ip: String
    :param next_hop: the next_hop of the route.
    :type next_hop: String
    :param communities: the communities of the route.
    :type communities: String
    """
    return requests.put(settings.API_URL_SINGLE+"/"+ident,
                 json={
                     'ip': ip,
                     'communities': communities,
                     'next_hop': next_hop,
                     'is_activated': True})

def delete_route(ident):
    """
    DELETE method

    :param ident: the id of the route who will be delete.
    :type ident: String
    """
    return requests.delete(settings.API_URL_SINGLE+"/"+ident)

def get_one_route(ident):
    """
    GET method

    :param ident: the id of the route who will be get.
    :type ident: String
    """
    return requests.get(settings.API_URL_SINGLE+"/"+ident)

def enable_disable_route(ident, boolean):
    """
    PATCH method

    :param ident: the id of the route who will be enable or disable.
    :type ident: String
    :param boolean: check if we want to disable (False) or enable (True).
    :type boolean: bool
    """
    return requests.patch(settings.API_URL_SINGLE+"/"+ident,
                   json={
                       'is_activated': boolean})
