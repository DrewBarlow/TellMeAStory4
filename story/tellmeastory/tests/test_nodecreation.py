from django.http import HttpResponse
from django.test import TestCase
from tellmeastory.models import Node, User

def insert_registered_user(username: str, password: str, dname: str) -> User:
    return User.objects.create(
        username=username,
        password=password,
        display_name=dname
    )

class NodeCreationViewTests(TestCase):
    pass