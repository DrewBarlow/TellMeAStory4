from django.db import models

# Create your models here.
class Tag(models.Model):
    name_text = models.CharField(max_length=256) # tag name identifier
    ID = models.IntegerField(default=-1) # unique tag ID
    usage_count = models.IntegerField(default=0) # times used by users
    language = models.CharField(max_length=256) # language used by tag

    # Returns name_text
    def get_name_text(self):
        return self.name_text

    # Returns True if tag name is valid
    def is_valid_name(self):
        return False
    # Returns True if tag does not yet
    # exist. False, otherwise.
    def is_new_tag(self) -> bool:
        return False

    # Returns True if name is found in a dictionary
    # given a language.
    def is_tag_name_in_dictionary(self):
        return False

    # Returns properties needed to add tag to a node and
    # increments usage count when used.
    def add_tag_to_node(self):
        return {"name_text":self.name_text, "ID":self.ID}

    # Decrements usage count when add fails or user removes
    # their tag. Managed by user of Tag model. Returns new
    # usage count.
    def decrement_usage(self):
        return self.usage_count