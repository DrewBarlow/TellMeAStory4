from django.forms import CharField, Form
from .models import Node, User

class LoginForm(Form):
    username: CharField = CharField(max_length=200, required=True)
    password: CharField = CharField(max_length=200, required=True)

class RegisterForm(Form):
    username: CharField = CharField(max_length=200, required=True)
    password: CharField = CharField(max_length=200, required=True)

    # default to the username if not specified
    display_name: CharField = CharField(max_length=200, required=False)

class NameChangeForm(Form):
    # this may not need to be required?
    new_display_name: CharField = CharField(max_length=200, required=True)

class NodeCreationForm(Form):
    title: CharField = CharField(max_length=200, required=True)
    content: CharField = CharField(max_length=10_000, required=True)