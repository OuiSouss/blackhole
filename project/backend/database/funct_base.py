from datetime import datetime
from pprint import pprint
from pymongo import MongoClient

class MongoDB:
    def __init__(self, collection_name):
        self.client = MongoClient('mongodb://admin:admin45@ds127115.mlab.com:27115/route_base')
        self.database = self.client.route_base
        if collection_name == 'Route' :
            self.route = self.database.Route
        else:
            self.route = self.database.Test

#methods=['GET']
    def get_all_routes(self):
        routes = self.route.find()
        for route in routes:
            pprint (route) 

#methods=['POST']
    def add_route(self, post):
        route_ip = post['ip']
        route_nexthop = post['next_hop']
        route_communities = post['communities']
        self.route.insert_one({
            'ip': route_ip,
            'next_hop': route_nexthop,
            'communities': route_communities,
            'created_at': datetime.now(),
            'modified_at': datetime.now(),
            'is_activated': 1,
            'last_activation': datetime.now()})

#methods=['DELETE']
    def delete_route(self, post):
        route_ip = post['ip']
        self.route.delete_many({'ip': route_ip})

#methods=['PATCH']
    def update_route(self, ip):
        route_ip = ip['ip']
        r = self.route.find_one({'ip': route_ip})
        self.route.update_one({"ip": route_ip},
                {"$set":{ 'modified_at':datetime.now(),
                          'is_activated':1-r['is_activated'],
                          'last_activation': datetime.now()}})
