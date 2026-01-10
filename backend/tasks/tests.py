# backend/tasks/tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User

class MiniCRMBackendTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.signup_url = '/api/auth/signup/'
        self.profile_url = '/api/profile/'
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'StrongPassw0rd!',
            'first_name': 'Test',   
            'last_name': 'User'
        }


    # Positive: Successful signup
    def test_signup_success(self):
        response = self.client.post(self.signup_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['email'], self.user_data['email'])

    # Negative: Missing required fields
    def test_signup_missing_fields(self):
        response = self.client.post(self.signup_url, {'email': ''}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)

    # Negative: Duplicate email
    def test_signup_duplicate_email(self):
        # First signup
        self.client.post(self.signup_url, self.user_data, format='json')
        # Attempt duplicate signup
        response = self.client.post(self.signup_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)

    # Positive & Negative: Profile retrieval and update
    def test_profile_retrieve_and_update(self):
        # Create user via signup
        signup_resp = self.client.post(self.signup_url, self.user_data, format='json')
        token = signup_resp.data['token']

        # Authenticate with token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # GET profile
        get_resp = self.client.get(self.profile_url)
        self.assertEqual(get_resp.status_code, 200)
        self.assertEqual(get_resp.data['email'], self.user_data['email'])

        # Update profile
        update_data = {'phone': '+254700000000', 'job_title': 'Developer'}
        patch_resp = self.client.patch(self.profile_url, update_data, format='json')
        self.assertEqual(patch_resp.status_code, 200)
        self.assertEqual(patch_resp.data['phone'], update_data['phone'])
        self.assertEqual(patch_resp.data['job_title'], update_data['job_title'])
