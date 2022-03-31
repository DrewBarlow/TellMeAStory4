from django.db import models


class UserTable(models.Model):
    #hold user's id
    user_id = models.CharField(max_length=100, primary_key=True)

    # hold user's name
    name = models.CharField(max_length=50)

    # hold user's email
    email = models.EmailField(max_length=70)

    # hold the user's username
    username = models.CharField(max_length=200)

    # hold the user's password
    password = models.CharField(max_length=200)


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

    #post_id is shown in the database
    def __str__(self):
        return self.post_id

    #add more media types


class Report(models.Model):
    #the id of the user who put in the report
    reporting_id = models.CharField(max_length=36, primary_key=True)

    #the id of the user who was reported
    reported_id = models.CharField(max_length=36)

    #the reason the user was reported (text field)
    report_reason = models.CharField(max_length=400)

    def __str__(self):
        return self.reporting_id

