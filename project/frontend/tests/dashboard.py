"""
Test Dashboard (Route Manager)

Basic operations accessible to the user
Tested using the frontend functions
"""

from django.test import TestCase
from route_manager.forms import PostForm

class RouteManagerTest(TestCase):
    """
    Test elements of the route manager
    """

    correct_ip = '192.168.1.1/30'
    correct_next_hop = '0.0.0.0'
    correct_community = '1234x'

    def test_form_add_route(self):
        """
        Test the form to add a route, with correct elements
        """
        form_data = {}
        form_data['ip'] = self.correct_ip
        form_data['next_hop'] = self.correct_next_hop
        form_data['communities'] = self.correct_community

        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())


    def get_incorrect_ip_adress_list(self):
        """
        Create a non-exhaustive list of incorrect ip adress to test
        """
        wrong_ip_adress_list = []
        wrong_ip_adress_list.clear()
        wrong_ip_adress_list.append('wrong')
        wrong_ip_adress_list.append('0.0.0.0.0')
        wrong_ip_adress_list.append('0.0.0')
        wrong_ip_adress_list.append('A.B.C.D')
        wrong_ip_adress_list.append('300.300.300.300')
        wrong_ip_adress_list.append('265.168.1.1')
        wrong_ip_adress_list.append('192.265.1.1')
        wrong_ip_adress_list.append('192.168.265.1')
        wrong_ip_adress_list.append('192.168.1.265')
        wrong_ip_adress_list.append('192.168.1.1/33')
        wrong_ip_adress_list.append('192.168.1.1/123')
        wrong_ip_adress_list.append('192.168.1.1/01')
        # TODO : Currently "accepted", should not in the future
        # wrong_ip_adress_list.append('192.168.1.1/0')
        wrong_ip_adress_list.append('192.168.1.1//24')
        wrong_ip_adress_list.append('192.168.1.1 /23')
        wrong_ip_adress_list.append('192.168.1.1/ 24')
        wrong_ip_adress_list.append('')
        wrong_ip_adress_list.append(None)
        return wrong_ip_adress_list


    def test_form_add_route_incorrect_ip(self):
        """
        Test the form to add a route, but with a list of incorrect ip
        """

        wrong_ip_list = self.get_incorrect_ip_adress_list()

        form_data = {}
        form_data['next_hop'] = self.correct_next_hop
        form_data['communities'] = self.correct_community

        for wrong_ip in wrong_ip_list:
            form_data['ip'] = wrong_ip
            form = PostForm(data=form_data)

            # Testing impossible cases
            # the form must not become valid
            if form.is_valid():
                # If a wrong value is accepted as correct
                # Then an assert is triggered
                print("\n\n>>> accepted wrong_ip : ", wrong_ip)
                self.assertFalse(form.is_valid())

    def test_form_add_route_incorrect_next_hop(self):
        """
        Test the form to add a route, but with a list of incorrect next_hop
        """

        wrong_next_hop_list = self.get_incorrect_ip_adress_list()

        form_data = {}
        form_data['ip'] = self.correct_ip
        form_data['communities'] = self.correct_community

        for wrong_next_hop in wrong_next_hop_list:
            form_data['next_hop'] = wrong_next_hop
            form = PostForm(data=form_data)

            # Testing impossible cases
            # the form must not become valid
            if form.is_valid():
                # If a wrong value is accepted as correct
                # Then an assert is triggered
                print("\n\n>>> accepted next_hop : ", wrong_next_hop)
                self.assertFalse(form.is_valid())
