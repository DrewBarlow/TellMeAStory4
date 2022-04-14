
# Create your models here.
from django.db import models
from django.db.models import BooleanField, ImageField, TextField, CharField, FloatField, ForeignKey, Model, FileField
from django.db.models import CASCADE
from django.urls import resolve, Resolver404
from re import fullmatch, Match
from validators import url


# Create your models here.
class User(Model):
    username: CharField = CharField(max_length=200)
    password: CharField = CharField(max_length=512)
    display_name: CharField = CharField(max_length=200)

    def __str__(self):
        return self.username

    def is_valid_username(self) -> bool:
        """
        Returns True if self.username consists of only the following:
        Unicode word characters, numbers, hyphens, underscores.
        Also, the length of self.username must be >= 5 and <= 14
        """
        # strip to remove leading/trailing spaces
        stripped_uname: str = self.username.strip()

        # \w   : Unicode word chars, numbers
        # (-_): Hyphens, underscores
        # *    : Any number of times, 0 inclusive
        PATTERN: str = r"[\w(-_)]*"
        regex_match: Match = fullmatch(PATTERN, stripped_uname)

        # fullmatch returns a Match object if the string matches the pattern
        # otherwise, it returns None
        return (5 <= len(self.username) <= 14) and regex_match != None

    def is_unique_username(self) -> bool:
        """
        Returns True if self.username is not associated with another
        User in the database.
        """
        # DoesNotExist should be raised if the query returns nothing
        # TODO: come back, I may be misinterpreting queries
        try:
            User.objects.get(username=self.username)
        except self.DoesNotExist:
            return True
        return False

    def is_valid_display_name(self) -> bool:
        """
        Returns True if self.display_name has a length of >= 5 and <= 20.
        """
        return 5 <= len(self.display_name) <= 20

class Node(models.Model):
    # Has possible story options for users who choose node/story
    longitude: float = 0
    latitude: float = 0
    thumbnail = models.FileField(upload_to='media/thumbnail', default='media/thumbnail/thumb1.jpg')
    audio_exists = models.BooleanField(default=False)
    node_text = models.TextField(max_length=2200, default="")
    node_audio = models.FileField(upload_to='media/audio')
    class Meta:
        db_table = 'Node'

    def __str__(self):
       # Returns the text for the story
        return self.node_text

    # audio to story
    def add_audio(self, sound=None) -> bool:
        # checks for audio
        if sound is not None:
            self.audio = sound
            try:
                self.audio_exists = True
                self.save()
                return True
            except:
                return False
        else:
            return False











