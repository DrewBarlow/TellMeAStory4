from django.forms import BooleanField, IntegerField, CharField, ImageField, Form
from .models import Node, User

class LoginForm(Form):
    username: CharField = CharField(max_length=200, required=True)
    password: CharField = CharField(max_length=200, required=True)

class RegisterForm(Form):
    username: CharField = CharField(max_length=200, required=True)
    password: CharField = CharField(max_length=200, required=True)

    # default to the username if not specified
    display_name: CharField = CharField(max_length=200, required=False)

    maturity: BooleanField = BooleanField(label="Are you over 18?", required=False)

class AccountForm(Form):
    # this may not need to be required?
    new_display_name: CharField = CharField(max_length=200, required=True)
    edit_blurb: CharField = CharField(max_length=1000, required=True)

class NodeCreationForm(Form):
    node_title: CharField = CharField(max_length=200, required=True)
    node_content: CharField = CharField(max_length=10_000, required=True)
    mature_node: BooleanField = BooleanField(label="Is this story mature?", required=False)

class AddImageForm(Form):
    # If no image is given, then no image is added.
    image_file: ImageField = ImageField(required=False)
    image_url: CharField = CharField(max_length=200, required=False)
    node_id: IntegerField = IntegerField(required=True)
