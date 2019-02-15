from django.conf import settings
import requests

def post_new_route(route):
    requests.post(settings.API_URL,
                  json={
                      'ip': str(route.ip),
                      'communities': str(route.community),
                      'next_hop': str(route.next_hop)})

def delete_route(ident):
    requests.delete(settings.API_URL,
                    json={'id': ident})

def enable_disable_route(ident, boolean):
    requests.patch(settings.API_URL,
                   json={
                       'id': ident,
                       'is_activated': boolean})
