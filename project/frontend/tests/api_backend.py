"""
Test Backend API

Using the same functions of the frontend
"""

from django.test import TestCase, Client

from django.contrib.auth.models import User
from django.conf import settings

from requests.exceptions import ConnectionError as connection_error
from requests import get as requests_get

from route_manager.forms import PostForm as post_form
from route_manager import request_json


#clear && python3 manage.py test blackhole_ui.tests.APIbackendTest
class APIbackendTest(TestCase):
    """
    Test backend API
    """

    # Class variables : authentication
    username = 'testuser2'
    password = 'secret2'
    client = Client()

    # Class variables : route elements
    test_ip = '1.1.1.1/1'
    test_next_hop = '1.1.1.1'
    test_community = 'XYZ'

    modif_ip = '2.2.2.2/2'
    modif_next_hop = '3.3.3.3'
    modif_community = 'ABC'

    def setUp(self):
        """
        Setup the correct credentials and authenticate the user
        The user is added to the temporary database
        Therefore allowing the database to recognize him
        """
        self.credentials = {
            'username': self.username,
            'password': self.password}
        User.objects.create_user(**self.credentials)
        self.client.post(settings.LOGIN_URL,
                         {'username': self.username,
                          'password': self.password})

    # Tests
    def test_reachable_api(self):
        """
        Test if the API is reachable
        """
        try:
            requests_get(settings.API_URL)
        except connection_error:
            raise AssertionError("\n>>> Backend API unreachable,\
                                 consider enabling it")

    def test_get_routes(self):
        """
        Test to get the available routes
        """

        try:
            response = requests_get(settings.API_URL)
            json_data = response.json()
            self.assertGreaterEqual(len(json_data), 0)

        except connection_error:
            raise AssertionError("\n\n>>> Backend API unreachable, \
                                 consider enabling it")

    def test_add_empty_route(self):
        """
        Test to create a route with no information
        It's supposed to be impossible and no route should be created
        The elements tested are the presence of "warning" texts
        """

        # TODO : not possible anymore to detect the apparition of warnings
        #        because the logs are doing interferences

        # before route creation
        self.client.get(settings.DASHBOARD_URL, follow=True)
        before_len = self.get_route_amount()

        # route creation
        self.client.post(settings.DASHBOARD_URL, follow=True, data=None)

        # after route creation
        self.client.get(settings.DASHBOARD_URL, follow=True)
        after_len = self.get_route_amount()

        # checking that nothing changed
        self.assertEqual(before_len, after_len)# identical dashboard

        #self.assertNotEqual(before_len, during_len)# dashboard + warnings

    def test_activate_desactivate_route(self):
        """
        Test the activation/desactivation of temporary route
        """

        # add test route
        self.add_default_route()

        # get the test route
        route_list = self.get_route_list()
        route = self.get_test_route(route_list)
        route_id = route['id']

        # check if the test route is active
        route_activation = route['is_activated']
        self.assertTrue(route_activation, "\n\n>>> Route should be activated\
                                           when created")

        # desactivate test route
        request_json.enable_disable_route(route_id, False)

        # get the route
        test = request_json.get_one_route(route_id)
        route = test.json()

        # check if the test route is not active
        route_activation = route['is_activated']
        self.assertFalse(route_activation, "\n\n>>> Route should be \
                                            desactivated when desactivated")

        # delete test route
        request_json.delete_route(route_id)

    def test_modify_route(self):
        """
        Test to modify a temporaty route
        """

        # add test route
        self.add_default_route()

        # get the test route
        route_list = self.get_route_list()
        route = self.get_test_route(route_list)

        route_id = route['id']
        #old_route_modified_at = route['modified_at']
        old_route_ip = route['ip']
        old_route_next_hop = route['next_hop']
        old_route_community = route['communities']

        # update route
        request_json.put_route(
            route_id,
            self.modif_ip,
            self.modif_next_hop,
            self.modif_community)

        # get the modified test route
        test = request_json.get_one_route(route_id)
        route = test.json()

        # TODO : 'modified_at' can't be tested unless we wait at least a minute
        # (would slow down the testing process)

        # check the differences
        self.assertEqual(route['ip'], self.modif_ip)
        self.assertEqual(route['next_hop'], self.modif_next_hop)
        self.assertEqual(route['communities'], [self.modif_community])
        self.assertNotEqual(route['ip'], old_route_ip)
        self.assertNotEqual(route['next_hop'], old_route_next_hop)
        self.assertNotEqual(route['communities'], old_route_community)

        # delete test route
        request_json.delete_route(route_id)

    def test_add_delete_routes(self):
        """
        Test to add a temporary route then delete it
        """

        # get current routes : before adding the new route
        initial_amount = self.get_route_amount()

        # adding the test route
        self.add_default_route()

        # get current routes : after adding the test route
        after_addition_amount = self.get_route_amount()

        # removing the test route
        self.delete_default_route()

        # get current routes : after removing the test route
        after_deletion_amount = self.get_route_amount()

        # print(initial_amount, " => ", after_addition_amount, " => ",
        # after_deletion_amount)
        self.assertEqual(initial_amount + 1, after_addition_amount)
        self.assertEqual(after_addition_amount - 1, after_deletion_amount)

    # Intermediate testing function
    def get_route_amount(self):
        """
        Intermediate testing function
        Clarify the process of getting the amount of routes
        """
        json_data = []
        try:
            response = requests_get(settings.API_URL)
            json_data = response.json()
            size_json = len(json_data)
            # print("Routes :", size_json)
            self.assertGreaterEqual(size_json, 0)

        except connection_error:
            raise AssertionError("\n\n>>> Backend API unreachable, consider \
                                  enabling it")
        return len(json_data)

    def get_route_list(self):
        """
        Intermediate testing function
        Clarify the process of getting routes
        """
        json_data = []

        try:
            response = requests_get(settings.API_URL)
            json_data = response.json()
            size_json = len(json_data)
            #print("Routes :", size_json)
            self.assertGreaterEqual(size_json, 0)

        except connection_error:
            raise AssertionError("\n\n>>> Backend API unreachable, consider \
                                 enabling it")

        return json_data

    def get_test_route(self, route_list):
        """
        Intermediate testing function
        Clarify the process of getting one testing route
        """
        testing_route_detected = False

        route = None
        for route in route_list:
            if self.is_deletable_route(route):
                testing_route_detected = True
                break

        self.assertTrue(testing_route_detected, "")
        return route

    def add_default_route(self):
        """
        Intermediate testing function
        Clarify the process of form creation, validation and route creation
        """
        route_data = {
            'ip': self.test_ip,
            'next_hop': self.test_next_hop,
            'communities': self.test_community}
        form = post_form(data=route_data)
        self.assertTrue(form.is_valid())

        # form POST
        request_json.post_new_route(
            route_data['ip'],
            route_data['next_hop'],
            route_data['communities']
            )

    def delete_default_route(self):
        """
        Intermediate testing function
        Clarify the process of deleting the test route
        """

        # get the list of routes
        json_data = self.get_route_list()


        # find the route to delete
        route = self.get_test_route(json_data)
        route_id = str(route['id'])
        request_json.delete_route(route_id)


    def is_deletable_route(self, route):
        """
        Check if route is a test route
        """
        ip_bool = route['ip'] == self.test_ip
        next_hop_bool = route['next_hop'] == self.test_next_hop
        return ip_bool and next_hop_bool
