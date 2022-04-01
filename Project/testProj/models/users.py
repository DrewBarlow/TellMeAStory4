from django.db import models


class UserTable(models.Model):
    #hold user's id
    user_id = models.CharField(max_length=100, primary_key=True)

    # hold user's name (display)
    name = models.CharField(max_length=50)

    # hold user's email
    email = models.EmailField(max_length=70)

    # hold the user's username
    username = models.CharField(max_length=200)

    # hold the user's password
    password = models.CharField(max_length=200)

    # accessor methods
    def get_user_id(self):
        return self.user_id

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password