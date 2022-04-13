from django.forms import IntegerField, CharField, FileField, Form
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

class AddImageForm(Form):
    # If no image is given, then no image is added.
    image_file: FileField = FileField(max_length=200, required=False)
    image_url: CharField = CharField(max_length=200, required=False)
    node_id: IntegerField = IntegerField(required=True)
