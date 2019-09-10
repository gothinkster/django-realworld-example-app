from django.test import TestCase
from rest_framework.test import APIClient
from .factories import UserFactory


class BaseConfig(TestCase):

    def setUp(self):
        self.client = APIClient()
        user = UserFactory()
        self.token = user.token
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token)



