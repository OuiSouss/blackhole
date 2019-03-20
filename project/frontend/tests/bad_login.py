"""
Test Bad Authentication
Incorrect authentication should not allow the user to login
"""

from django.test import TestCase
from django.conf import settings

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
