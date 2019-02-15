"""
 Units tests for the database
"""

import unittest
from funct_base import MongoDB

class BaseTest(unittest.TestCase):
    """
     Test class for MongoDB
    """

    def setUp(self):
        """
         Test initialization
        """
        self.database = MongoDB('Test')

    def test_add_route(self):
        """
         Tests if the route has successfully been added to the database
        """
        post = {
            'ip': 'test_ip',
            'next_hop': 'test_nexthop',
            'communities': 'test_commu'
        }
        route_id = self.database.add_route(post)
        post2 = self.database.route.find_one({'ip': post['ip']})
        self.assertEqual(post2['ip'], post['ip'], 'insertion failed')
        self.assertEqual(post2['next_hop'], post['next_hop'],
                         'insertion failed')
        self.assertEqual(post2['communities'], post['communities'],
                         'insertion failed')
        self.database.delete_route({'_id': route_id})

    def test_get_all_routes(self):
        """
         Test is the route has succesfully been got to the database
        """
        post = {
            'ip': 'test_ip',
            'next_hop': 'test_nexthop',
            'communities': 'test_commu'
        }
        post2 = {
            'ip': 'test_ip2',
            'next_hop': 'test_nexthop2',
            'communities': 'test_commu2'
        }
        route1_id = self.database.add_route(post)
        route2_id = self.database.add_route(post2)
        post3 = self.database.route.find()
        for r in post3:
            if r['ip'] == post['ip']:
                self.assertEqual(r['ip'], post['ip'], 'insertion failed')
                self.assertEqual(r['next_hop'], post['next_hop'],
                                 'insertion failed')
                self.assertEqual(r['communities'], post['communities'],
                                 'insertion failed')
            else:
                self.assertEqual(r['ip'], post2['ip'], 'insertion failed')
                self.assertEqual(r['next_hop'], post2['next_hop'],
                                 'insertion failed')
                self.assertEqual(r['communities'], post2['communities'],
                                 'insertion failed')
        self.database.delete_route({'_id': route1_id})
        self.database.delete_route({'_id': route2_id})

    def test_update_route(self):
        """
         Test if the route has succesfully been updated in the database
        """
        post = {
            'ip': 'test_ip',
            'next_hop': 'test_nexthop',
            'communities': 'test_commu'
        }
        route_id = self.database.add_route(post)
        self.database.update_route({
            '_id': route_id,
            'is_activated': False,
        })
        post2 = self.database.route.find_one({'_id': route_id})
        self.assertEqual(post2['is_activated'], False, 'activation failed')
        self.database.delete_route({'_id': route_id})

    def test_delete_route(self):
        """
         Test  if the route has succesfully been deleted of the database
        """
        post = {
            'ip': 'test_ip',
            'next_hop': 'test_nexthop',
            'communities': 'test_commu'
        }
        route_id = self.database.add_route(post)
        self.database.delete_route({'_id': route_id})
        route = self.database.route.find_one({'_id': route_id})
        self.assertEqual(route, None, 'deletion failed')

if __name__ == '__main__':
    unittest.main()
