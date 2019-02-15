"""
    Database on MongoDB
"""

from datetime import datetime
from pprint import pprint
from pymongo import MongoClient

class MongoDB:
    """
	 Class of the database on MongoDB
    """

    def __init__(self, collection_name):
        """
         Initialization of the connection to the database
	     :param collection_name: The name of the collection in the database
	     :type collection_name: string
        """
        mongo_db = "admin:admin45@ds127115.mlab.com:27115/route_base"
        mongo_connection = "mongodb://" + mongo_db
        self.client = MongoClient(mongo_connection)
        self.database = self.client.route_base
        if collection_name == 'Route':
            self.route = self.database.Route
        else:
            self.route = self.database.Test

#methods=['GET']
    def get_all_routes(self):
        """
         Get all of the routes stored in the database
         :return: A list contains all of the routes
        """
        routes = self.route.find()
        output = []
        for route in routes:
            pprint(route)
            output.append(route)
        return output

#methods=['POST']
    def add_route(self, post):
        """
         Add one route in the database
         :type post: dict
         :return: id of created route
        """
        route_ip = post['ip']
        route_nexthop = post['next_hop']
        route_communities = post['communities']
        route_id = self.route.insert_one({
            'ip': route_ip,
            'next_hop': route_nexthop,
            'communities': route_communities,
            'created_at': datetime.now(),
            'modified_at': datetime.now(),
            'is_activated': 1,
            'last_activation': datetime.now()}).inserted_id
        return route_id

#methods=['DELETE']
    def delete_route(self, post):
        """
         Delete one route in the database
         :type post: dict
        """
        route_id = post['_id']
        self.route.delete_many({'_id': route_id})

#methods=['PATCH']
    def update_route(self, ip):
        """
         Update the field 'is_activated'.
         If the field value is 0, the fied value become 1 (vice versa).
         :param ip: dict
        """
        route_ip = ip['ip']
        r = self.route.find_one({'ip': route_ip})
        self.route.update_one({"ip": route_ip},
                              {"$set": {
                                  'modified_at': datetime.now(),
                                  'is_activated': 1-r['is_activated'],
                                  'last_activation': datetime.now()
                                  }})
