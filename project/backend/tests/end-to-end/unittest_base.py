"""
 Units tests for the database
"""
import unittest
from backend.database.funct_base import MongoDB

class BaseTest(unittest.TestCase):
    """
    BaseTest Test actions on MongoDB
    """

    def setUp(self):
        self.database = MongoDB('Test')
        self.database.delete_all_route()

    def test_get_route_by_id(self):
        """
        test_get_route_by_id

        Tests if the route has successfully been got to the database
        """

        post = {
            'ip': 'test_ip',
            'next_hop': 'test_nexthop',
            'communities': 'test_commu'
        }
        route_id = self.database.add_route(post)
        post2 = self.database.get_route_by_id({'_id': route_id})
        self.database.delete_route({'_id': route_id})
        self.assertEqual(post2['ip'], post['ip'], 'insertion failed')
        self.assertEqual(post2['next_hop'], post['next_hop'],
                         'insertion failed')
        self.assertEqual(post2['communities'], post['communities'],
                         'insertion failed')

    def test_add_route(self):
        """
        test_add_route

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
        test_get_all_routes

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
        self.assertFalse(len(post3) > 2,
                         'Database was not empty before this function')
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
        test_update_route

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
        test_delete_route

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
        test_put_route

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
        self.assertEqual(post2['is_activated'], post3['is_activated'],
                         'activation failed')

    def test_update_route_and_activation(self):
        """
        test_update_route_and_activation

        Test if last_activation is updated when
        is_activated change from false to true
        """

        patch = {
            'ip': 'test_ip',
            'next_hop': 'test_nexthop',
            'communities': 'test_commu'
        }
        route_id = self.database.add_route(patch)
        patch_activated_false = self.database.update_route({
            '_id': route_id,
            'is_activated': False,
        })
        last_activation_when_false = patch_activated_false['last_activation']
        patch_activated_true = self.database.update_route({
            '_id': route_id,
            'is_activated': True,
        })
        last_activation_when_true = patch_activated_true['last_activation']
        self.database.delete_route({'_id': route_id})
        self.assertNotEqual(last_activation_when_false,
                            last_activation_when_true,
                            'last_activation must be change')

    def test_put_route_and_activation(self):
        """
        test_put_route_and_activation

        Test if last_activation is updated when
        is_activated change from false to true
        """

        patch = {
            'ip': 'test_ip',
            'next_hop': 'test_nexthop',
            'communities': 'test_commu'
        }
        route_id = self.database.add_route(patch)
        patch_activated_false = self.database.put_route({
            '_id': route_id,
            'ip': 'test_ip',
            'next_hop': 'test_nexthop2',
            'communities': 'test_commu2',
            'is_activated': False,
        })
        last_activation_when_false = patch_activated_false['last_activation']
        patch_activated_true = self.database.put_route({
            '_id': route_id,
            'ip': 'test_ip',
            'next_hop': 'test_nexthop2',
            'communities': 'test_commu2',
            'is_activated': True,
        })
        last_activation_when_true = patch_activated_true['last_activation']
        self.database.delete_route({'_id': route_id})
        self.assertNotEqual(last_activation_when_false,
                            last_activation_when_true,
                            'last_activation must be change')


if __name__ == '__main__':
    unittest.main()
