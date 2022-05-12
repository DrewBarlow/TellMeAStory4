from django.http import HttpResponse
from django.test import TestCase
from hashlib import sha512
from tellmeastory.models import User


class UserModelTests(TestCase):
    def emailExists(self):
        account = User.objects.create(
            username="Letsgo123",
            email="ojjosh55@gmail.com",
            password="Migrate123",
        )
        account.save()
        exist = self.client.post()
        self.assertContains(account)
        self.assertContains(response="Email already exists")
        self.assertContains(response="Letsgo123")
