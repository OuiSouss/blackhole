"""
Tests for the frontend

Elements tested :
- login/logout
- form validation (add route)
"""


from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
import requests
from requests.exceptions import ConnectionError

from route_manager.forms import PostForm

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

    def test_reachable_api(self):
        """
        Test if the API is reachable

        Exception when unavailable :
        <class 'requests.exceptions.ConnectionError'>

        The standard "ConnectionError" doesnt work
        """
        try:
            requests.get(settings.API_URL)

        except ConnectionError:
            raise AssertionError("\n>>> Backend API unreachable, consider enabling it")


    def test_get_routes(self):
        """
        Test to get the routes
        """

        try:
            response = requests.get(settings.API_URL)
            json_data = response.json()

            self.assertGreaterEqual(len(json_data), 0)

        except ConnectionError:
            raise AssertionError("\n>>> Backend API unreachable, consider enabling it")


    #def test_add_routes(self):
    #def test_delete_routes(self):
    #def test_activate_routes(self):
    #def test_desactivate_routes(self):
    #def test_modify_routes(self):


#clear && python3 manage.py test blackhole_ui.tests.RouteManagerTest
class RouteManagerTest(TestCase):
    """
    Test elements of the route manager
    """

    def test_form_add_route(self):
        """
        Test the form to add a route, with correct elements
        """
        form_data = {}
        form_data['ip'] = '192.168.1.1'
        form_data['community'] = '1234x'
        form_data['next_hop'] = '0.0.0.0'

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
        wrong_ip_adress_list.append('')
        wrong_ip_adress_list.append(None)
        return wrong_ip_adress_list



    def test_form_add_route_incorrect_ip(self):
        """
        Test the form to add a route, but with a list of incorrect ip
        """

        wrong_ip_list = self.get_incorrect_ip_adress_list()

        form_data = {}
        form_data['community'] = '1234x'
        form_data['next_hop'] = '0.0.0.0'

        for wrong_ip in wrong_ip_list:
            form_data['ip'] = wrong_ip
            form = PostForm(data=form_data)

            # Testing impossible cases
            # the form must not become valid
            if form.is_valid():
                # If a wrong value is accepted as correct
                # Then an assert is triggered
                print(">> accepted wrong_ip : ", wrong_ip)
                self.assertFalse(form.is_valid())


    def test_form_add_route_incorrect_community(self):
        """
        Test the form to add a route, but with a list of incorrect community
        """

        wrong_community_list = []
        wrong_community_list.append(None)
        wrong_community_list.append('')

        form_data = {}
        form_data['ip'] = '192.168.1.1'
        form_data['next_hop'] = '0.0.0.0'

        for wrong_community in wrong_community_list:
            form_data['community'] = wrong_community
            form = PostForm(data=form_data)

            # Testing impossible cases
            # the form must not become valid
            if form.is_valid():
                # If a wrong value is accepted as correct
                # Then an assert is triggered
                print(">> accepted community : ", wrong_community)
                self.assertFalse(form.is_valid())


    def test_form_add_route_incorrect_next_hop(self):
        """
        Test the form to add a route, but with a list of incorrect next_hop
        """

        wrong_next_hop_list = self.get_incorrect_ip_adress_list()

        form_data = {}
        form_data['ip'] = '192.168.1.1'
        form_data['community'] = '1234x'

        for wrong_next_hop in wrong_next_hop_list:
            form_data['next_hop'] = wrong_next_hop
            form = PostForm(data=form_data)

            # Testing impossible cases
            # the form must not become valid
            if form.is_valid():
                # If a wrong value is accepted as correct
                # Then an assert is triggered
                print(">> accepted next_hop : ", wrong_next_hop)
                self.assertFalse(form.is_valid())
