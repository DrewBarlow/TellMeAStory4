from django.db import models
from django.db.models import ManyToManyField, BooleanField, ImageField, TextField, CharField, FloatField, ForeignKey, Model, CASCADE, FileField
from django.urls import resolve, Resolver404
from re import fullmatch, Match
from validators import url
from managetags.models import Tag

# Create your models here.
class User(Model):
    username: CharField = CharField(max_length=200)
    password: CharField = CharField(max_length=512)
    display_name: CharField = CharField(max_length=200)
    profile_pic = models.ImageField(default="profile_pic.jpg", null=True, blank=True)
    mature: BooleanField = BooleanField(default=False)
    user_blurb = models.CharField(max_length=1000, default="")
    admin = models.BooleanField(default=False)

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

    def is_mature(self) -> bool:
        """
        Returns True if self.mature is True.
        """
        return self.is_mature

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

class Node(Model):
    """ Story Node class. Holds a story's contents to present
    to users that select the respective story node. """
    image: ImageField = ImageField(upload_to="storyimages" ,
                                   default=None)  # File for an image if a file is given by user
    image_url: TextField = TextField()  # URL to source an image from if URL is given by user
    node_title: CharField = CharField(max_length=200)  # Title of the story stored in the Node
    node_content: CharField = CharField(max_length=10_000)  # Story content (text) of node
    # The Node has an url if False, otherwise it has an image file
    has_image_file: BooleanField = BooleanField(default=False)  # True only when user gave a file for an image
    # Node coordinates on map
    longitude: float = 0
    latitude: float = 0
    node_author: ForeignKey = ForeignKey(User , on_delete=CASCADE , null=True)  # Account/user who created the Node
    main_tag_id: int = 0  # Primary story content Tag's id. One main Tag can relate to many story Nodes.
    other_tags: ManyToManyField = ManyToManyField(Tag)  # A Node can have many tags for further filtering
    node_audio: FileField = FileField(upload_to="storyaudio", default=None)
    audio_exists = models.BooleanField(default=False) # True only when user gave an audio file

    def __str__(self):
        """
        Returns current Title for A Story Node.
        """
        return self.node_title

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

    def add_image(self , newFile=None , newURL=None) -> bool:
        """
        Allows for image to be attached to a Story Node.
        """
        # If both parameters are given, then the image cannot
        # be updated to just one. Return False.
        if newFile is not None and newURL is not None:
            return False
        # newFile is given and can be updated as current image
        elif newFile is not None:
            return self.add_image_from_file(file=newFile)
        # newURL is given and can be updated as current image
        elif newURL is not None:
            return self.add_image_from_url(URL=newURL)
        # Nothing was given. No changes made. Return False
        else:
            return False

    def add_image_from_file(self , file) -> bool:
        """
        Allows for image url to be attached to a Story Node.
        Returns True if attached, otherwise false.
        """
        # Try to find image file
        self.image = file
        try:
            # Update image properties
            self.has_image_file = True
            self.image_url = TextField(default=None)
            self.save()
            return True
        except:
            # Error thrown
            # Change nothing
            return False

    def add_image_from_url(self , URL) -> bool:
        """
        Allows for image url to be linked to a node.
        Returns True if downloaded and attached, otherwise false.
        """
        # Try to find url
        self.image_url = URL
        try:
            # Will not throw error if valid file
            if url(self.image_url):
                # Update image properties
                self.has_image_file = False
                self.image = None
                self.save()
                return True
            # Failsafe for no exception and invalid url
            return False
        except:
            # Error thrown, meaning file does not exist
            # Change nothing
            return False

    def attach_main_tag(self , properties: dict) -> bool:
        '''
        The Node (self) is given a Foreign key to
        its main Tag. The id and properties of the
        Tag are given in a dict:
        {"name_text": Tag.name_text, "countID": Tag.countID, "id": Tag.id}
        Returns True if attached or False otherwise
        '''
        try:
            # Valid Tag attachment
            self.other_tags.add(Tag.objects.get(id=properties["id"]))
            self.main_tag_id = properties["id"]
            self.save()
            return True
        except:
            # Invalid Tag attachment
            return False

    def attach_tag(self , properties: dict) -> bool:
        '''
        The Node (self) is given a relationship to
        many Tags. The id and properties of the
        Tag are given in a dict:
        {"name_text": Tag.name_text, "countID": Tag.countID, "id": Tag.id}
        Returns True if attached or False otherwise
        '''
        try:
            # Attach given Tag to this Node
            self.other_tags.add(Tag.objects.get(id=properties["id"]))
            self.save()
            return True
        except:
            # Invalid Tag attachment
            return False

    def is_mature(self) -> bool:
        """
        Returns True if this node has the "Mature" tag in other_tags.
        """
        return self.other_tags.filter(name_text="Mature").exists()

    def attach_mature_tag(self) -> None:
        """
        Adds the "Mature" tag to this Node.
        If the tag does not already exist, create it. Otherwise, retrieve it
        and add it.
        """
        tag: Tag = None

        # retrieve the mature tag if it exists, otherwise make it
        try:
            tag = Tag.objects.get(name_text="Mature")
        except Tag.DoesNotExist:
            tag = Tag(name_text="Mature")
            tag.save()

        self.other_tags.add(tag)
        self.save()

        return

    # audio to story
    def add_audio(self, sound=None) -> bool:
        # checks for audio
        if sound is not None:
            self.node_audio = sound
            try:
                self.audio_exists = True
                self.save()
                return True
            except:
                return False
        else:
            return False