"""
Tests for the frontend

Elements tested :
- Authentication (correct) => LogInTest
- Authentication (incorrect) => BadLogInTest
- Backend API (from frontend) => APIbackendTest
- Route Manager (form validation) => RouteManagerTest
"""


from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
import requests
from requests.exceptions import ConnectionError

from route_manager.forms import PostForm
import route_manager.request_json

from django.test import Client


#clear && python3 manage.py test blackhole_ui.tests.LogInTest
class LogInTest(TestCase):
    """
    Login test when correct credentials are provided
    """

    def setUp(self):
        """
        Setup the correct credentials
        The user is added to the temporary database
        Therefore allowing the database to recognize him
        """
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)


    def test_login_authenticated(self):
        """
        Test if the user is authenticated after a successful login
        Test if the user is not anonymous after a successful login
        """
        response = self.client.post(settings.LOGIN_URL, self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertFalse(response.context['user'].is_anonymous)


    def test_login_active(self):
        """
        Test if the user is active
        """
        response = self.client.post(settings.LOGIN_URL, self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)


    def test_access_restricted_content(self):
        """
        Test if the user cant access restricted element when anonymous
        Test if the user can access restricted element but only when authenticated
        """
        url_destination = settings.DASHBOARD_URL
        url_login = settings.LOGIN_URL

        # attempt to access restricted content, should refuse and redirect
        response = self.client.post(url_destination, self.credentials)
        self.assertNotEqual(response.url, url_destination)
        self.assertEqual(response.status_code, 302)

        # not authenticated already, but redirection should be successful
        response = self.client.post(url_destination, self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

        # going to login, should work (and redirect to dashboard)
        response = self.client.post(url_login, self.credentials)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(url_login, self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

        # attempt to access restricted content, should allow and not redirect
        response = self.client.post(url_destination, self.credentials)
        self.assertEqual(response.status_code, 200)


    def test_logout(self):
        """
        Test if the user becomes anonymous after a logout
        """
        response = self.client.post(settings.LOGIN_URL, self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertTrue(response.context['user'].is_authenticated)

        response = self.client.post(settings.LOGOUT_URL, self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertFalse(response.context['user'].is_authenticated)


#clear && python3 manage.py test blackhole_ui.tests.BadLogInTest
class BadLogInTest(TestCase):
    """
    Login test when wrong credentials are provided
    """

    def setUp(self):
        """
        Setup the wrong credentials
        The user is not added to the temporary database
        Therefore will not be recognized by the database
        """
        self.credentials = {
            'username': 'baduser',
            'password': 'whatever'}


    def test_login_authenticated(self):
        """
        Test if the user is not authenticated after a failed login
        Test if the user is anonymous after a failed login
        """
        response = self.client.post(settings.LOGIN_URL, self.credentials, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertTrue(response.context['user'].is_anonymous)


    def test_login_active(self):
        """
        Test if the user is not active
        """
        response = self.client.post(settings.LOGIN_URL, self.credentials, follow=True)
        self.assertFalse(response.context['user'].is_active)


    def test_access_restricted_content(self):
        """
        Test if the user cant access restricted element when anonymous
        Test if the user can access restricted element but only when authenticated
        """
        url_destination = settings.DASHBOARD_URL
        url_login = settings.LOGIN_URL

        # attempt to access restricted content, should refuse and redirect
        response = self.client.post(url_destination, self.credentials)
        self.assertNotEqual(response.url, url_destination)
        self.assertEqual(response.status_code, 302)

        # not authenticated already, but redirection should be successful
        response = self.client.post(url_destination, self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

        # going to login, should fail (and not redirect to dashboard)
        response = self.client.post(url_login, self.credentials)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url_login, self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

        # attempt to access restricted content, should refuse and redirect
        response = self.client.post(url_destination, self.credentials)
        self.assertEqual(response.status_code, 302)


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
    test_ip = '0.0.0.0/0'
    test_next_hop = '0.0.0.0'
    test_community = 'XYZ'

    # Class variables : performances
    amount = 128

    # clear ; python3 manage.py test blackhole_ui.tests.APIbackendTest.perf_route_creation
    def perf_route_creation(self):
        """
        Performance test
        Route creation
        """

        print("\n")
        for i in range(0, self.amount):
            # print("creation : ", i)
            self.add_default_route()

    # clear ; python3 manage.py test blackhole_ui.tests.APIbackendTest.perf_route_deletion
    def perf_route_deletion(self):
        """
        Performance test
        Route deletion
        """

        print("\n")
        for i in range(0, self.amount):
            # print("deletion : ", i)
            self.delete_default_route()

    def perf_route_destruction(self):
        """
        Performance test
        Route deletion but more violent and less slow
        """

        print("\n")
        json_data = []
        try:
            response = requests.get(settings.API_URL)
            json_data = response.json()
            self.assertGreaterEqual(len(json_data), 0) # there must be data, can't be None

        except ConnectionError:
            raise AssertionError("\n\n>>> Backend API unreachable, consider enabling it")

        # find the routes to delete
        for route in json_data:
            if(route['ip'] == self.test_ip and route['next_hop'] == self.test_next_hop):
                route_id = str(route['id'])
                route_manager.request_json.delete_route(route_id)


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
        self.client.post(settings.LOGIN_URL, {'username': self.username, 'password': self.password})

    def test_reachable_api(self):
        """
        Test if the API is reachable
        """
        try:
            requests.get(settings.API_URL)
        except ConnectionError:
            raise AssertionError("\n>>> Backend API unreachable, consider enabling it")

    def test_get_routes(self):
        """
        Test to get the available routes
        """

        try:
            response = requests.get(settings.API_URL)
            json_data = response.json()
            self.assertGreaterEqual(len(json_data), 0) # there must be data, can't be None

        except ConnectionError:
            raise AssertionError("\n\n>>> Backend API unreachable, consider enabling it")

    def test_add_empty_route(self):
        """
        Test to create a route with no information
        It's supposed to be impossible and no route should be created
        """

        # before route creation
        response = self.client.get(settings.DASHBOARD_URL, follow=True)
        before_len = len(response.content)

        # route creation
        response = self.client.post(settings.DASHBOARD_URL, follow=True, data=None)
        during_len = len(response.content)

        # after route creation
        response = self.client.get(settings.DASHBOARD_URL, follow=True)
        after_len = len(response.content)

        # checking that nothing changed
        self.assertEqual(before_len, after_len)# identical dashboard
        self.assertNotEqual(before_len, during_len)# dashboard + war

    def get_route_amount(self):
        """
        Intermediate testing function
        clarify the process of getting the amount of routes
        """
        json_data = []
        try:
            response = requests.get(settings.API_URL)
            json_data = response.json()
            self.assertGreaterEqual(len(json_data), 0) # there must be data, can't be None

        except ConnectionError:
            raise AssertionError("\n\n>>> Backend API unreachable, consider enabling it")
        return len(json_data)

    def add_default_route(self):
        """
        Intermediate testing function
        clarify the process of form creation, validation and route creation
        """
        form_data = {
            'ip': self.test_ip,
            'next_hop': self.test_next_hop,
            'community': self.test_community}
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

        # form POST
        route = form.save(commit=False)
        route_manager.request_json.post_new_route(route)

    def delete_default_route(self):
        """
        Intermediate testing function
        clarify the process of deleting the test route
        """

        # get the list of routes
        json_data = []
        try:
            response = requests.get(settings.API_URL)
            json_data = response.json()
            self.assertGreaterEqual(len(json_data), 0) # there must be data, can't be None

        except ConnectionError:
            raise AssertionError("\n\n>>> Backend API unreachable, consider enabling it")

        # find the route to delete
        testing_route_deleted = False
        for route in json_data:
            if(route['ip'] == self.test_ip and route['next_hop'] == self.test_next_hop):
                route_id = str(route['id'])
                testing_route_deleted = True
                route_manager.request_json.delete_route(route_id)
                break
        self.assertTrue(testing_route_deleted,"")

    # clear ; python3 manage.py test blackhole_ui.tests.APIbackendTest.test_add_delete_routes
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

        # print(initial_amount, " => ", after_addition_amount, " => ", after_deletion_amount)
        self.assertEqual(initial_amount + 1, after_addition_amount)
        self.assertEqual(after_addition_amount - 1, after_deletion_amount)




    # TODO : test functions to do

    #def test_activate_routes(self):
    #def test_desactivate_routes(self):
    #def test_modify_routes(self):


#clear && python3 manage.py test blackhole_ui.tests.RouteManagerTest
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
        form_data['community'] = self.correct_community

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
        #wrong_ip_adress_list.append('192.168.1.1/0') # Currently "accepted", wont be in the future
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
        form_data['community'] = self.correct_community

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


    def test_form_add_route_incorrect_community(self):
        """
        Test the form to add a route, but with a list of incorrect community
        """

        wrong_community_list = []
        wrong_community_list.append(None)
        wrong_community_list.append('')

        form_data = {}
        form_data['ip'] = self.correct_ip
        form_data['next_hop'] = self.correct_next_hop

        for wrong_community in wrong_community_list:
            form_data['community'] = wrong_community
            form = PostForm(data=form_data)

            # Testing impossible cases
            # the form must not become valid
            if form.is_valid():
                # If a wrong value is accepted as correct
                # Then an assert is triggered
                print("\n\n>>> accepted community : ", wrong_community)
                self.assertFalse(form.is_valid())


    def test_form_add_route_incorrect_next_hop(self):
        """
        Test the form to add a route, but with a list of incorrect next_hop
        """

        wrong_next_hop_list = self.get_incorrect_ip_adress_list()

        form_data = {}
        form_data['ip'] = self.correct_ip
        form_data['community'] = self.correct_community

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
