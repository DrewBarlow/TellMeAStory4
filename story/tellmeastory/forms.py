from django.forms import CharField, Form, EmailField
from .models import User

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

from django import forms
from django.forms import ModelForm
from .models import Post,Report

#Create Post form
class PostForm(ModelForm):
    class Meta:
        #get the current Post database
        model = Post

        #controls what fields appear, MUST BE NAMED AFTER THE FIELDS IN THE DATABASE
        fields = ('postText',)

#Create Report form
class ReportForm(ModelForm):
    class Meta:
        #get the current Post database
        model = Report

        #controls what fields appear, MUST BE NAMED AFTER THE FIELDS IN THE DATABASE
        fields = ('report_reason',)

