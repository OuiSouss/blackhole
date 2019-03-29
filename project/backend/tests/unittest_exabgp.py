"""
 Units tests for exabgp
"""
from unittest.mock import Mock, patch
from unittest import TestCase, main
from backend.funct_exabgp import ExaBGP
from backend.resources.settings import URL_EXABGP

class ExaBGPTest(TestCase):
    """
    ExaBGPTest Test actions of ExaBGP class
    """

    def setUp(self):
        """
         Test initialization
        """
        self.exabgp = ExaBGP(URL_EXABGP)
        self.exabgp_cmd = [
            'shutdown',
            'restart',
            'reload',
            'reset',
            'version',
            'show neighbors',
            'teardown'
        ]

    @patch('backend.funct_exabgp.requests.post')
    def test_action_when_command_good(self, mock_post):
        """
         Tests if the command has successfully been activated on ExaBGP
        """
        mock_post.return_value.ok = True
        for cmd in self.exabgp_cmd:
            response = self.exabgp.action(cmd)
            self.assertIsNotNone(response)

    @patch('backend.funct_exabgp.requests.post')
    def test_action_when_command_not_good(self, mock_post):
        """
         Tests if the command has successfully been activated on ExaBGP
        """
        mock_post.return_value.ok = False
        cmd = [
            'toto',
            '',
            'fj',
            'help',
            'kqslfqlsfpaoi)é65eze5a6e5zae6',
        ]
        for cmd in self.exabgp_cmd:
            response = self.exabgp.action(cmd)
            self.assertIsNone(response)

    @patch('backend.funct_exabgp.requests.post')
    def test_announce_one_route(self, mock_post):
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
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_post.return_value = mock_resp
        response = self.exabgp.announce_one_route(post)
        self.assertEqual(response, 200, 'announce failed')
        response = self.exabgp.announce_one_route(post2)
        self.assertEqual(response, 200, 'announce failed')

    @patch('backend.funct_exabgp.requests.post')
    def test_withdraw_one_route(self, mock_post):
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
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_post.return_value = mock_resp
        response = self.exabgp.withdraw_one_route(post)
        self.assertEqual(response, 200, 'withdraw failed')
        response = self.exabgp.withdraw_one_route(post2)
        self.assertEqual(response, 200, 'withdraw failed')

    @patch('backend.funct_exabgp.requests.post')
    def test_update_one_route(self, mock_post):
        """
         Tests if the route has successfully been updated on ExaBGP
        """
        post = {
            'ip': '10.1.0.3',
            'next_hop': '3.3.3.3',
            'communities': '[45:65]'
        }
        post2 = {
            'ip': '10.1.0.3',
            'next_hop': '2.2.2.2',
            'is_activated': False,
            'communities': None
        }
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_post.return_value = mock_resp
        response = self.exabgp.update_one_route(post2)
        self.assertEqual(response, 200, 'update failed')

if __name__ == '__main__':
    main()
