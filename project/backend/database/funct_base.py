"""
Database on MongoDB
"""

from datetime import datetime
from pymongo import MongoClient
from backend.database.settings import get_uri

class MongoDB:
    """
    Class of the database on MongoDB
    """

    def __init__(self, collection_name):
        mongo_db = get_uri()
        mongo_connection = 'mongodb://' + mongo_db
        self.client = MongoClient(mongo_connection)
        self.database = self.client.route_base
        if collection_name == 'Route':
            self.route = self.database.Route
        else:
            self.route = self.database.Test

    def get_route_by_id(self, get):
        """
        get_route_by_id Get a route with a specific id

        :param get: A dictionnary with _id and its value
        :type get: dict
        """

        route = self.route.find_one({'_id' : get['_id']})
        return route


    def get_all_routes(self):
        """
        get_all_routes stored in the database

        :return: A list of all of the routes
        :rtype: list
        """

        routes = self.route.find()
        output = []
        for route in routes:
            output.append(route)
        return output

    def add_route(self, post):
        """
        add_route in database

        :param post: Informations of what need to add
        :type post: dict
        :return: id of created route
        :rtype: ObjectID
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

    def delete_route(self, delete):
        """
        delete_route

        :param delete: id to delete
        :type delete: ObjectID
        """

        route_id = delete['_id']
        self.route.delete_many({'_id': route_id})

    def delete_all_route(self):
        """
        delete_all_route
        """

        self.route.delete_many({})

    def update_route(self, patch):
        """
        update_route

        Update the field 'is_activated'.
        If the field value is False, the fied value become True (vice versa).
        modified_at is updated every time and last_activation when
        is_activated was False and becomes True

        :param patch: Dict with id and is_activated
        :type patch: dict
        :return: The update route
        :rtype: dict
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

    def put_route(self, put):
        """
        put_route

        Update all fields except created_at
        If the field value is False, the fied value become True (vice versa).
        modified_at is updated every time and last_activation when
        is_activated was False and becomes True

        :param put: Dict with id, ip, next_hop, communities and is_activated
        :type put: dict
        :return: The updated route
        :rtype: dict
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
