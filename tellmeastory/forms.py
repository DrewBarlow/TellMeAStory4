from django.forms import IntegerField, CharField, FileField, Form, forms
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


class AudioForm(Form):
    class Meta:
        model=Node
        fields = ['node_audio']
    audio_file: FileField = FileField(required=False)
    node_id: IntegerField = IntegerField(required=True)

class TextForm(Form):
    class Meta:
        model = Node
        fields = ['node_text']

class ThumbForm(forms.Form):
    class Meta:
        model = Node
        fields = ['thumbnail']
   # thumb = forms.ImageField()
   # def __init__(self, *args, **kwargs):
    #    super(ThumbForm, self).__init__(*args, **kwargs)

