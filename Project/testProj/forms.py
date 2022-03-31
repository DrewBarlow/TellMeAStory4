from django import forms
from django.forms import ModelForm
from .models import Post

#Create Post form
class PostForm(ModelForm):
    class Meta:
        #get the current Post database
        model = Post

        #controls what fields appear, MUST BE NAMED AFTER THE FIELDS IN THE DATABASE
        fields = ('postText',)
