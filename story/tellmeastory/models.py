from django.db.models import ImageField, CharField, ForeignKey, Model
from django.db.models import CASCADE
from re import fullmatch, Match

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

class Node(Model):
    """ Story Node class. Holds a story's contents to present
    to users that select the respective story node. """
    image: ImageField = ImageField(upload_to="storyimages")
    node_title: CharField = CharField(max_length=200)
    node_content: CharField = CharField(max_length=10_000)
    # location (long/lat)
    node_author: ForeignKey = ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        """ Returns current Title for A Story Node. """
        return self.node_title

    def add_image(self):
        """ Allows for image to be attached to a Story Node. """
        return True

    def is_valid_title(self) -> bool:
        """
        The title should be at least 5 characters and no more than 200.
        """
        sanitized: str = self.node_title.strip()
        return 5 <= len(sanitized) <= 200

    def is_valid_content(self) -> bool:
        """
        The content should be no more than 10,000 chars long.
        """
        sanitized: str = self.node_content.strip()
        return len(sanitized) <= 10_000
