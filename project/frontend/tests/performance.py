"""
Test Performances

Help to create/delete small/massive amounts of elements
No testing function will be executed by default
They have to be called remotely and individually
"""

from random import choice as random_choice

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.conf import settings

from requests.exceptions import ConnectionError as connection_error
from requests import get as requests_get

import route_manager.request_json
# TODO : another file to clarify the creation/destruction of routes
#        instead of duplicating code would be nice

from route_manager.forms import PostForm as post_form
from route_manager import request_json

class PerformanceTest(TestCase):
    """
    Test backend API performances

    Usable to test frontend performances
    These functions only target the testing routes
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
    amount = 3
    massive_amount = 30

    #TODO

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

    # clear ; python3 manage.py test tests.performance.PerformanceTest.perf_route_creation
    def perf_route_creation(self):
        """
        Performance test
        Route creation ( 'amount' )
        Can be used in parallel
        Fast but no feedback
        """

        print("\n")
        for _ in range(0, self.amount):
            # print("creation : ", i)
            #self.add_default_route()
            self.add_default_route()

    # clear ; python3 manage.py test tests.performance.PerformanceTest.perf_route_v_create
    def perf_route_v_create(self):
        """
        Performance test
        Massive route creation ( 'massive_amount' )
        Slow but feedback
        """
        print(" ")
        print(self.massive_amount, "routes to create\n")
        
        # Amount of groups, useful to display progress
        # If that value is too close to 'massive_amount', progress will invisible (0%)
        # If that value is too small, progress will be invisible (not enough info)
        partition = 10

        step_iteration = int(self.massive_amount / partition)
        rest_iteration = self.massive_amount - step_iteration * partition
        progress_iteration = int(step_iteration / self.massive_amount * 100) 

        advancement = 0
        # print("massive_amount :", self.massive_amount)
        # print("partition :", partition)
        # print("step_iteration :", step_iteration)
        # print("rest_iteration :", rest_iteration)
        # print("progress_iteration :", progress_iteration,"%")
        # print("\n")

        for _ in range(0, partition):
            self.show_advancement(advancement)
            for _ in range(0, step_iteration):
                self.add_default_route()
            advancement += progress_iteration

        for _ in range(0, rest_iteration):
            advancement += progress_iteration
            self.add_default_route()

        print("100 %")

    # clear ; python3 manage.py test tests.performance.PerformanceTest.perf_route_deletion
    def perf_route_deletion(self):
        """
        Performance test
        Route deletion ( 'amount' )
        Fast but no feedback
        """

        print("\n")

        json_data = self.get_route_list()
        amount_deleted = 0

        for route in json_data:
            if self.is_deletable_route(route):
                route_id = str(route['id'])
                request_json.delete_route(route_id)
                amount_deleted += 1

                if (amount_deleted == self.amount):
                    break

    # clear ; python3 manage.py test tests.performance.PerformanceTest.perf_route_destruction
    def perf_route_destruction(self):
        """
        Performance test
        Route deletion ( all )
        """

        json_data = self.get_route_list()
        json_size = len(json_data)

        limit_percent = int(json_size/100)
        deletions = 0
        advancement = 0
        
        # print("json_size",json_size)
        # print("limit_percent",limit_percent)

        print(" ")
        print(json_size, "routes to destroy\n")
    
        self.show_advancement(advancement)

        # find the routes to delete
        for route in json_data:
            if self.is_deletable_route(route):
                route_id = str(route['id'])
                route_manager.request_json.delete_route(route_id)

                deletions += 1
                advancement += 1
                
                if advancement > limit_percent:
                    advancement = 0
                    progress = int((deletions-1)/json_size*100)
                    self.show_advancement(progress)

        self.show_advancement(100)

    # clear ; python3 manage.py test tests.performance.PerformanceTest.delete_random
    def delete_random(self):
        """
        Route deletion ( almost all )
        Efficient in parrallel, unreliable alone
        May ask to delete routes that have already been deleted 
        """

        response = requests_get(settings.API_URL)
        json_data = response.json()
        json_size = len(json_data)
        
        print(json_size, "routes to destroy\n")

        # find the routes to delete
        for _ in range(int(json_size)):
            route = random_choice(json_data)
            if self.is_deletable_route(route):
                route_id = str(route['id'])
                print(">> ", route_id)
                route_manager.request_json.delete_route(route_id)


    def show_advancement(self, advancement):
        """
        Print function (100 %)
        """
        print(advancement, "%")

    def is_deletable_route(self, route):
        """
        Check if route is a test route
        """
        ip_bool = route['ip'] == self.test_ip
        next_hop_bool = route['next_hop'] == self.test_next_hop
        return ip_bool and next_hop_bool

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
            self.assertGreaterEqual(size_json, 0) # there must be data, can't be None

        except connection_error:
            raise AssertionError("\n\n>>> Backend API unreachable, consider enabling it")

        return json_data

    def add_default_route(self):
        """
        Intermediate testing function
        Clarify the process of form creation, validation and route creation
        """
        route_data = {
            'ip': self.test_ip,
            'next_hop': self.test_next_hop,
            'community': self.test_community}
        form = post_form(data=route_data)
        self.assertTrue(form.is_valid())

        # form POST
        request_json.post_new_route(
            route_data['ip'],
            route_data['next_hop'],
            route_data['community']
            )