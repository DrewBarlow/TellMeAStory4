from django.db import models

class Post(models.Model):

    #hold user's id
    user_id = models.CharField(max_length=100)

    #hold the id of a post
    post_id = models.CharField(max_length=72,primary_key=True, default="")

    #hold the text that a user enters
    postText = models.CharField(max_length=200, default="")

    #add more fields for soundclips, pictures

    #this field would be for current date time
    #postTime = models.DateTimeField()


    # add more media types
    #post_id is shown in the database
    def __str__(self):
        return self.post_id


    #accessor methods
    def get_user_id(self):
        return self.user_id

    def get_post_id(self):
        return self.post_id

    def get_postText(self):
        return self.postText


