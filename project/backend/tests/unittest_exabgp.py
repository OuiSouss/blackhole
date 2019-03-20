"""
 Units tests for exabgp
"""
import unittest
import os
from io import StringIO
from backend.funct_exabgp import ExaBGP

class ExaBGPTest(unittest.TestCase):
    """
    ExaBGPTest Test actions of ExaBGP class
    """

    def setUp(self):
        """
         Test initialization
        """
        self.exabgp = ExaBGP('out_test_exabgp.txt')

    def tearDown(self):
        """
        Clear after tests
        """
        os.remove('out_test_exabgp.txt')

    def test_action(self):
        cmd = 'restart'
        response = self.exabgp.action(cmd)
        out = open(self.exabgp.output, "r")
        test = out.read()
        out.close()
        test = test.rstrip("\n")
        self.assertEqual(response, 'yes', 'command failed')
        self.assertEqual(response, test, 'command failed on file')
	
    def test_announce_one_route(self):
        post = {
            'ip': 'test_ip',
            'next_hop': 'test_nexthop',
            'communities': 'test_commu'
        }
        response = self.exabgp.announce_one_route(post)
        out = open(self.exabgp.output, "r")
        test = out.read()
        out.close()
        test = test.rstrip("\n")
        self.assertEqual(response, 'yes', 'command failed')
        self.assertEqual(response, test, 'command failed on file')

    def test_withdraw_one_route(self):
        post = {
            'ip': 'test_ip'
        }
        response = self.exabgp.withdraw_one_route(post)
        out = open(self.exabgp.output, "r")
        test = out.read()
        out.close()
        test = test.rstrip("\n")
        self.assertEqual(response, 'yes', 'command failed')
        self.assertEqual(response, test, 'command failed on file')

    def test_update_one_route(self):
        post = {
            'ip': 'test_ip',
            'next_hop': 'test_nexthop',
            'communities': 'test_commu'
        }
        response = self.exabgp.update_one_route(post)
        out = open(self.exabgp.output, "r")
        test = out.read()
        out.close()
        test = test.rstrip("\n")
        self.assertEqual(response, 'yes', 'command failed')
        self.assertEqual(response, test, 'command failed on file')

if __name__ == '__main__':
    unittest.main() 