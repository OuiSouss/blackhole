"""
 Units tests for exabgp
"""
import unittest
from backend.funct_exabgp import ExaBGP
from backend.resources.settings import URL_EXABGP

class ExaBGPTest(unittest.TestCase):
    """
    ExaBGPTest Test actions of ExaBGP class
    """

    def setUp(self):
        """
         Test initialization
        """
        self.exabgp = ExaBGP(URL_EXABGP)

    def test_action(self):
        """
         Tests if the command has successfully been activated on ExaBGP
        """
        cmd = 'restart'
        response = self.exabgp.action(cmd)
        self.assertEqual(response, 200, 'command failed')

    def test_announce_one_route(self):
        """
         Tests if the route has successfully been activated on ExaBGP
        """
        post = {
            'ip': '10.1.0.3',
            'next_hop': '2.2.2.2',
            'communities': '[45:65]'
        }
        post2 = {
            'ip': '10.1.0.3',
            'next_hop': '2.2.2.2',
            'communities': None
        }
        response = self.exabgp.announce_one_route(post)
        self.exabgp.withdraw_one_route(post)
        self.assertEqual(response, 200, 'announce failed')
        response = self.exabgp.announce_one_route(post2)
        self.exabgp.withdraw_one_route(post2)
        self.assertEqual(response, 200, 'announce failed')

    def test_withdraw_one_route(self):
        """
         Tests if the route has successfully been withdrawn on ExaBGP
        """
        post = {
            'ip': '10.1.0.3',
            'next_hop': '2.2.2.2',
            'communities': '[45:65]'
        }
        post2 = {
            'ip': '10.1.0.3',
            'next_hop': '2.2.2.2',
            'communities': None
        }
        self.exabgp.announce_one_route(post)
        response = self.exabgp.withdraw_one_route(post)
        self.assertEqual(response, 200, 'withdraw failed')
        self.exabgp.announce_one_route(post2)
        response = self.exabgp.withdraw_one_route(post2)
        self.assertEqual(response, 200, 'withdraw failed')

    def test_update_one_route(self):
        """
         Tests if the route has successfully been updated on ExaBGP
        """
        post = {
            'ip': '10.1.0.3',
            'next_hop': '3.3.3.3',
            'communities': '[45:65]'
        }
        self.exabgp.announce_one_route(post)
        post2 = {
            'ip': '10.1.0.3',
            'next_hop': '2.2.2.2',
            'is_activated': False,
            'communities': None
        }
        response = self.exabgp.update_one_route(post2)
        self.exabgp.withdraw_one_route(post)
        self.assertEqual(response, 200, 'update failed')

if __name__ == '__main__':
    unittest.main()
