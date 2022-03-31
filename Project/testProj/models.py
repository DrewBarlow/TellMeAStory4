from django.db import models


class UserTable(models.Model):
    user_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=70)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)


class Post(models.Model):

    user_id = models.CharField(max_length=100)
    post_id = models.CharField(max_length=72,primary_key=True, default="")
    postText = models.CharField(max_length=200, default="")
    #postTime = models.DateTimeField()


    def __str__(self):
        return self.post_id

    #add more media types


class Report(models.Model):
    reporting_id = models.CharField(max_length=36, primary_key=True)
    reported_id = models.CharField(max_length=36)
    report_reason = models.CharField(max_length=200)

    def __str__(self):
        return self.reporting_id

