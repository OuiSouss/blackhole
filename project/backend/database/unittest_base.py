import unittest
from funct_base import MongoDB

class BaseTest(unittest.TestCase):

    def setUp(self):
        self.database = MongoDB('Test')

    def test_add_route(self):
        post = {
            'ip': 'test_ip',
            'next_hop': 'test_nexthop',
            'communities': 'test_commu'
        }
        self.database.add_route(post)
        post2 = self.database.route.find_one({'ip': post['ip']})
        self.assertEqual(post2['ip'], post['ip'], 'insertion failed')
        self.assertEqual(post2['next_hop'], post['next_hop'],
                         'insertion failed')
        self.assertEqual(post2['communities'], post['communities'],
                         'insertion failed')
        self.database.delete_route({'ip': post['ip']})

    def test_get_all_routes(self):
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
        self.database.add_route(post)
        self.database.add_route(post2)
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
        self.database.delete_route({'ip': post['ip']})
        self.database.delete_route({'ip': post2['ip']})

    def test_update_route(self):
        post = {
            'ip': 'test_ip',
            'next_hop': 'test_nexthop',
            'communities': 'test_commu'
        }
        self.database.add_route(post)
        self.database.update_route({'ip': post['ip']})
        post2 = self.database.route.find_one({'ip': post['ip']})
        self.assertEqual(post2['is_activated'], 0, 'activation failed')
        self.database.delete_route({'ip': post['ip']})

    def test_delete_route(self):
        post = {
            'ip': 'test_ip',
            'next_hop': 'test_nexthop',
            'communities': 'test_commu'
        }
        self.database.add_route(post)
        self.database.delete_route({'ip': post['ip']})
        route = self.database.route.find_one({'ip': post['ip']})
        self.assertEqual(route, None, 'deletion failed')

if __name__ == '__main__':
    unittest.main()
