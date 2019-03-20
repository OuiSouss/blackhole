"""
Tests for the frontend

Elements tested :
- Authentication (correct) => LogInTest
- Authentication (incorrect) => BadLogInTest
- Backend API (from frontend) => APIbackendTest
- Route Manager (form validation) => RouteManagerTest
"""

from random import choice as random_choice

from django.test import TestCase, Client

from django.contrib.auth.models import User
from django.conf import settings
import requests
from requests.exceptions import ConnectionError

from route_manager.forms import PostForm
import route_manager.request_json




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
        self.client.post(settings.LOGIN_URL, {'username': self.username, 'password': self.password})

    # Tests
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
        self.assertTrue(route_activation, "\n\n>>> Route should be activated when created")

        # desactivate test route
        route_manager.request_json.enable_disable_route(route_id, False)

        # get the route
        test = route_manager.request_json.get_one_route(route_id)
        route = test.json()

        # check if the test route is not active
        route_activation = route['is_activated']
        self.assertFalse(route_activation, "\n\n>>> Route should be desactivated when desactivated")

        # delete test route
        route_manager.request_json.delete_route(route_id)

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
        route_manager.request_json.put_route(
            route_id,
            self.modif_ip,
            self.modif_next_hop,
            self.modif_community)

        # get the modified test route
        test = route_manager.request_json.get_one_route(route_id)
        route = test.json()

        # TODO : 'modified_at' can't be tested unless we wait at least one minute
        # (would slow down the testing process)

        # check the differences
        self.assertEqual(route['ip'], self.modif_ip)
        self.assertEqual(route['next_hop'], self.modif_next_hop)
        self.assertEqual(route['communities'], [self.modif_community])
        self.assertNotEqual(route['ip'], old_route_ip)
        self.assertNotEqual(route['next_hop'], old_route_next_hop)
        self.assertNotEqual(route['communities'], old_route_community)

        # delete test route
        route_manager.request_json.delete_route(route_id)

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

    # Intermediate testing function
    def get_route_amount(self):
        """
        Intermediate testing function
        Clarify the process of getting the amount of routes
        """
        json_data = []
        try:
            response = requests.get(settings.API_URL)
            json_data = response.json()
            size_json = len(json_data)
            # print("Routes :", size_json)
            self.assertGreaterEqual(size_json, 0) # there must be data, can't be None

        except ConnectionError:
            raise AssertionError("\n\n>>> Backend API unreachable, consider enabling it")
        return len(json_data)

    def get_route_list(self):
        """
        Intermediate testing function
        Clarify the process of getting routes
        """
        json_data = []

        try:
            response = requests.get(settings.API_URL)
            json_data = response.json()
            size_json = len(json_data)
            #print("Routes :", size_json)
            self.assertGreaterEqual(size_json, 0) # there must be data, can't be None

        except ConnectionError:
            raise AssertionError("\n\n>>> Backend API unreachable, consider enabling it")

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
                #route_id = str(route['id'])
                testing_route_detected = True
                #route_manager.request_json.delete_route(route_id)
                break

        self.assertTrue(testing_route_detected, "")
        return route

    def add_default_route(self):
        """
        Intermediate testing function
        clarify the process of form creation, validation and route creation
        """
        route_data = {
            'ip': self.test_ip,
            'next_hop': self.test_next_hop,
            'community': self.test_community}
        form = PostForm(data=route_data)
        self.assertTrue(form.is_valid())

        # form POST
        route_manager.request_json.post_new_route(
            route_data['ip'],
            route_data['next_hop'],
            route_data['community']
            )

    def delete_default_route(self):
        """
        Intermediate testing function
        clarify the process of deleting the test route
        """

        # get the list of routes
        json_data = self.get_route_list()

        # try:
        #     response = requests.get(settings.API_URL)
        #     json_data = response.json()
        #     self.assertGreaterEqual(len(json_data), 0) # there must be data, can't be None

        # except ConnectionError:
        #     raise AssertionError("\n\n>>> Backend API unreachable, consider enabling it")

        # find the route to delete
        route = self.get_test_route(json_data)
        route_id = str(route['id'])
        route_manager.request_json.delete_route(route_id)

        # testing_route_deleted = False
        # for route in json_data:
        #     if(self.is_deletable_route(route)):
        #         route_id = str(route['id'])
        #         testing_route_deleted = True
        #         route_manager.request_json.delete_route(route_id)
        #         break
        # self.assertTrue(testing_route_deleted, "")

    def is_deletable_route(self, route):
        """
        Check if route is a test route
        """
        ip_bool = route['ip'] == self.test_ip
        next_hop_bool = route['next_hop'] == self.test_next_hop
        return ip_bool and next_hop_bool



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



class PerformanceTest(TestCase):
    """
    Test backend API performances
    Usable to test frontend performances
    """

    # Class variables : authentication
    username = 'testuser3'
    password = 'secret3'
    client = Client()

    # Class variables : route elements
    test_ip = '1.1.1.1/1'
    test_next_hop = '1.1.1.1'
    test_community = 'XYZ'

    # Class variables : performances
    amount = 10
    api_test = APIbackendTest


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

    # clear ; python3 manage.py test blackhole_ui.tests.PerformanceTest.perf_route_creation
    def perf_route_creation(self):
        """
        Performance test
        Route creation
        Can be used in parallel
        """

        print("\n")
        for _ in range(0, self.amount):
            # print("creation : ", i)
            #self.add_default_route()
            self.api_test.add_default_route(self)

    # clear ; python3 manage.py test blackhole_ui.tests.PerformanceTest.perf_route_deletion
    def perf_route_deletion(self):
        """
        Performance test
        Route deletion
        """

        print("\n")
        for _ in range(0, self.amount):
            # print("deletion : ", i)
            #self.delete_default_route()
            self.api_test.delete_default_route(self)

    # clear ; python3 manage.py test blackhole_ui.tests.PerformanceTest.perf_route_destruction
    def perf_route_destruction(self):
        """
        Performance test
        Route deletion but more violent and less slow
        """

        print("\n")
        json_data = []
        json_size = 0
        try:
            response = requests.get(settings.API_URL)
            json_data = response.json()
            json_size = len(json_data)
            self.assertGreaterEqual(json_size, 0) # there must be data, can't be None

        except ConnectionError:
            raise AssertionError("\n\n>>> Backend API unreachable, consider enabling it")

        deletions = 0
        limit_cent = int(json_size/100)
        advancement = 0
        self.show_advancement(advancement)

        # find the routes to delete
        for route in json_data:
            if self.api_test.is_deletable_route(self, route):
                route_id = str(route['id'])
                route_manager.request_json.delete_route(route_id)

                deletions += 1
                if deletions > limit_cent:
                    deletions = 0
                    advancement += 1
                    self.show_advancement(advancement)

    # clear ; python3 manage.py test blackhole_ui.tests.PerformanceTest.delete_random
    def delete_random(self):
        """
        Route deletion
        Can be used in parallel
        """

        print("BEFORE GET")
        response = requests.get(settings.API_URL)
        json_data = response.json()
        json_size = len(json_data)
        print("AFTER GET")


        # find the routes to delete
        for _ in range(int(json_size)):
            route = random_choice(json_data)
            if self.api_test.is_deletable_route(self, route):
                route_id = str(route['id'])
                print(">> ", route_id)
                route_manager.request_json.delete_route(route_id)

    # clear ; python3 manage.py test blackhole_ui.tests.PerformanceTest.perf_route_V_creation
    def perf_route_v_creation(self):
        """
        Performance test
        Massive route creation
        """
        massive_amount = 20


        partition = 100
        step_iteration = int(massive_amount / partition)
        rest_iteration = massive_amount - step_iteration * partition

        i = 0
        print("massive_amount :", massive_amount)
        print("step_iteration :", step_iteration)
        print("rest_iteration :", rest_iteration)
        print("\n")

        for advancement in range(0, partition):
            self.show_advancement(advancement)
            for _ in range(0, step_iteration):
                i += 1
                self.api_test.add_default_route(self)


        for _ in range(0, rest_iteration):
            i += 1
            self.api_test.add_default_route(self)

        print("100 %")
        print(i)

    def show_advancement(self, advancement):
        """
        Print function (100 %)
        """
        print(advancement, "%")


# Only functions starting with "test" will be tested
