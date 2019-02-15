"""
Database on MongoDB
"""

from datetime import datetime
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
        mongo_db = 'admin:admin45@ds127115.mlab.com:27115/route_base'
        mongo_connection = 'mongodb://' + mongo_db
        self.client = MongoClient(mongo_connection)
        self.database = self.client.route_base
        if collection_name == 'Route':
            self.route = self.database.Route
        else:
            self.route = self.database.Test

    # methods = ['GET']
    def get_all_routes(self):
        """
        Get all of the routes stored in the database
        :return: A list contains all of the routes
        """
        routes = self.route.find()
        output = []
        for route in routes:
            output.append(route)
        return output

    # methods = ['POST']
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
            'is_activated': True,
            'last_activation': datetime.now()}).inserted_id
        return route_id

    # methods = ['DELETE']
    def delete_route(self, delete):
        """
        Delete one route in the database
        :type delete: dict
        """
        route_id = delete['_id']
        self.route.delete_many({'_id': route_id})

    # methods = ['PATCH']
    def update_route(self, patch):
        """
        Update the field 'is_activated'.
        If the field value is False, the fied value become True (vice versa).
        modified_at is updated every time and last_activation when
        is_activated was False and becomes True
        :param patch: dict
        :return: The updated route
        """
        route_id = patch['_id']
        route_is_activated = patch['is_activated']
        r = self.route.find_one({'_id': route_id})
        last_activation = r['last_activation']
        if not r['is_activated'] and route_is_activated:
            last_activation = datetime.now()
        self.route.update_one({'_id': route_id},
                              {'$set': {
                                  'modified_at': datetime.now(),
                                  'is_activated': route_is_activated,
                                  'last_activation': last_activation
                              }})
        return self.route.find_one({'_id': route_id})

    # methods = ['PUT']
    def put_route(self, put):
        """
        Update all fields except created_at
        If the field value is False, the fied value become True (vice versa).
        modified_at is updated every time and last_activation when
        is_activated was False and becomes True
        :param put: dict
        :return: The update route
        """
        route_id = put['_id']
        route_ip = put['ip']
        route_nexthop = put['next_hop']
        route_communities = put['communities']
        route_is_activated = put['is_activated']
        r = self.route.find_one({'_id': route_id})
        last_activation = r['last_activation']
        if not r['is_activated'] and route_is_activated:
            last_activation = datetime.now()
        self.route.update_one({'_id': route_id},
                              {'$set': {
                                  'ip': route_ip,
                                  'next_hop': route_nexthop,
                                  'communities': route_communities,
                                  'modified_at': datetime.now(),
                                  'is_activated': route_is_activated,
                                  'last_activation': last_activation
                              }})
        return self.route.find_one({'_id': route_id})
