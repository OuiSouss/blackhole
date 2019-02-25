"""
 Units tests for the database
"""
import sys
import unittest
from backend.database.funct_base import MongoDB

class BaseTest(unittest.TestCase):
    """
    BaseTest Test actions on MongoDB
    """

    def setUp(self):
        """
         Test initialization
        """
        self.database = MongoDB('Test')
        self.database.delete_all_route()

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
        self.database.delete_route({'_id': route_id})
        self.assertEqual(post2['ip'], post['ip'], 'insertion failed')
        self.assertEqual(post2['next_hop'], post['next_hop'],
                         'insertion failed')
        self.assertEqual(post2['communities'], post['communities'],
                         'insertion failed')

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
        post3 = self.database.get_all_routes()
        self.assertFalse(len(post3) > 2, 'Database was not empty before this function')
        self.database.delete_route({'_id': route1_id})
        self.database.delete_route({'_id': route2_id})
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

    def test_update_route(self):
        """
         Test if the route has succesfully been updated in the database
        """
        patch = {
            'ip': 'test_ip',
            'next_hop': 'test_nexthop',
            'communities': 'test_commu'
        }
        route_id = self.database.add_route(patch)
        patch2 = self.database.update_route({
            '_id': route_id,
            'is_activated': False,
        })
        self.database.delete_route({'_id': route_id})
        self.assertEqual(patch2['is_activated'], False, 'activation failed')

    def test_delete_route(self):
        """
         Test  if the route has succesfully been deleted in the database
        """
        delete = {
            'ip': 'test_ip',
            'next_hop': 'test_nexthop',
            'communities': 'test_commu'
        }
        route_id = self.database.add_route(delete)
        self.database.delete_route({'_id': route_id})
        route = self.database.route.find_one({'_id': route_id})
        self.assertEqual(route, None, 'deletion failed')

    def test_put_route(self):
        """
         Test  if the route has succesfully been updated in the database
        """
        post = {
            'ip': 'test_ip',
            'next_hop': 'test_nexthop',
            'communities': 'test_commu'
        }
        route_id = self.database.add_route(post)
        post3 = {
            'ip': 'test_ip',
            'next_hop': 'test_nexthop2',
            'communities': 'test_commu2',
            'is_activated': False,
        }
        put = self.database.route.find_one({'_id': route_id})
        route_id2 = self.database.put_route({
            '_id': put['_id'],
            'ip': post3['ip'],
            'communities': post3['communities'],
            'next_hop':  post3['next_hop'],
            'is_activated': post3['is_activated']
        })
        post2 = self.database.route.find_one({'_id': route_id2['_id']})
        self.database.delete_route({'_id': route_id2['_id']})
        self.assertEqual(post2['ip'], post3['ip'], 'insertion failed')
        self.assertEqual(post2['next_hop'], post3['next_hop'],
                         'insertion failed')
        self.assertEqual(post2['communities'], post3['communities'],
                         'insertion failed')
        self.assertEqual(post2['is_activated'], post3['is_activated'], 'activation failed')

if __name__ == '__main__':
    unittest.main()
