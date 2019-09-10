from .base_config import BaseConfig
from django.urls import reverse

class AuthTestCase(BaseConfig):

    def test_user_can_register_for_account(self):
        response = self.client.post(
            reverse('authentication:registration'),
            data = {
                "user" : {
                "email": "testuser@conduit.com",
                "username": "test_user",
                "password": "testuser123"
            }
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["email"], "testuser@conduit.com")
        self.assertEqual(response.data["username"], "test_user")

    def test_user_can_login_after_registration(self):
        self.test_user_can_register_for_account()
        response = self.client.post(
            reverse('authentication:login'),
            data={
                "user": {
                    "email": "testuser@conduit.com",
                    "password": "testuser123"
                }
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], "testuser@conduit.com")

