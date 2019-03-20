"""
Test Authentication
Correct authentication should allow the user to login
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.conf import settings

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
