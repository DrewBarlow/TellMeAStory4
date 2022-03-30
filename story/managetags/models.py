from django.db import models

# Create your models here.
class Tag(models.Model):
    name_text = models.CharField(max_length=255) # tag name identifier
    ID = models.IntegerField(default=-1) # unique tag ID
    usage_count = models.IntegerField(default=0) # times used by users
    language = models.CharField(max_length=255) # language used by tag

    # Returns name_text
    def __str__(self):
        return self.name_text

    # Returns True if tag name is valid alphanumeric and
    # greater than 3 characters (valid tag name).
    def is_valid_name(self) -> bool:
        MIN_LEN = 3 # minimum Tag name length
        if self.name_text.isalnum() and len(self.name_text) >= MIN_LEN:
            return True
        return False

    # Returns True if tag does not yet exist
    # and can be inserted. False, otherwise.
    def is_new_tag(self) -> bool:
        return False

    # Returns True if new tag is saved.
    # False, otherwise.
    def add_new_tag(self) -> bool:
        return False

    # Returns True if name is found in a dictionary
    # given a language.
    def is_tag_name_in_dictionary(self) -> bool:
        return False

    # Returns properties needed to add tag to a node and
    # increments usage count when used.
    def add_tag_to_node(self) -> dict:
        return {"name_text":self.name_text, "ID":self.ID}

    # Decrements usage count when add fails or user removes
    # their tag. Managed by user of Tag model. Returns new
    # usage count.
    def decrement_usage(self) -> int:
        return self.usage_count