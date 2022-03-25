from django.db import models

# Create your models here.
class User(models.Model):
    username: str = models.CharField(max_length=200)
    password: str = models.CharField(max_length=512)
    display_name: str = models.CharField(max_length=200)

    def __str__(self):
        return self.username

    def is_valid_username(self) -> bool:
        """
        Returns True if self.username consists of only the following:
        lower/upper english letters, numbers, spaces, hyphens, underscores.
        Also, the length of self.username must be >= 5 and <= 14
        """
        # should use a regex, just using a string for now
        DESIRABLES: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -_"

        for char in self.username:
            if char not in DESIRABLES:
                return False

        return 5 <= len(self.username) <= 14

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

    # should not be present here--
    # refer to tests.py in UserRegistrationTests
    #     at function test_password_is_secure()
    def is_strong_password(self) -> bool:
        return False
