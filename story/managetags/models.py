from django.db import models
from enchant import Dict

# Create your models here.
class Tag(models.Model):
    # TODO: Add many to one relationship with Node model using ForeignKey
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
        # If get raises an error, then the Tag does not
        # yet exist. Otherwise, it was found.
        # Warning: get() can raise an error if it found multiple
        # of the same name_text, however, the use of this function
        # should prevent such a case.
        try:
            isOldTag = Tag.objects.get(name_text=self.name_text)
        except:
            return True
        finally:
            return False

    # Returns True if new tag is saved.
    # False, otherwise.
    def add_new_tag(self) -> bool:
        # If Tag has a valid name and tag, save
        # tag to the database. Return True if
        # added or False if not added.
        if self.is_valid_name() and self.is_new_tag():
            self.save()
            return True
        return False

    # Returns True if name is found in a dictionary
    # given a language.
    def is_tag_name_in_dictionary(self) -> bool:
        return False

    # Returns properties needed to add tag to a node and
    # increments usage count when used.
    def add_tag_to_node(self) -> dict:
        # TODO: Add Tag relation to Node in database
        # Increment usage count and save to db
        self.usage_count = self.usage_count + 1
        self.save(update_fields="usage_count")

        # Return necessary details needed for the
        # connection of a Tag to a node.
        return {"name_text": self.name_text, "ID": self.ID, "id": self.id}

    # Decrements usage count when add fails or user removes
    # their tag. Managed by user of Tag model. Returns new
    # usage count.
    def decrement_usage(self) -> int:
        # Check if usage_count is already at zero
        if self.usage_count == 0:
            return self.usage_count
        # Decrement usage_count of Tag
        self.usage_count = self.usage_count - 1
        # Return updated usage_count
        return self.usage_count