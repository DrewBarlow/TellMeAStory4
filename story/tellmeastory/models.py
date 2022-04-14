from django.db import models

from re import fullmatch, Match

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=512)
    display_name = models.CharField(max_length=200)
    admin = models.BooleanField(default=False)
    user_blurb = models.CharField(max_length=1000, default="")

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

class Post(models.Model):

    #hold user's id
    username = models.ForeignKey(User,on_delete=models.CASCADE)


    #hold the id of a post
    post_id = models.CharField(max_length=72,primary_key=True, default="")

    #hold the text that a user enters
    postText = models.CharField(max_length=200, default="")

    #add more fields for soundclips, pictures

    #this field would be for current date time
    #postTime = models.DateTimeField()

    def __str__(self):
        return "%s " % self.username