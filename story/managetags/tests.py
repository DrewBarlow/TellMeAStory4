from django.test import TestCase
# TODO: from .models import Tag
# Create your tests here.
class TagModelTests(TestCase):
    def test_was_tag_name_correct(self):
        # Returns False for tags created with incorrect
        # names when given a name.
        is_name_correct = False
        self.assertIs(is_name_correct, True)

    def test_was_tag_ID_correct(self):
        # Returns False for tags created with incorrect
        # ID when given an ID.
        is_ID_correct = False
        self.assertIs(is_ID_correct, True)

    def test_was_tag_added(self):
        # Returns False for tags that don't exist in the db
        # after insertion.
        tag_in_db = False
        self.assertIs(tag_in_db, True)

    def test_was_tag_added_without_repeat(self):
        # Returns False for tags that don't reject
        # insertion when repeated.
        tag_in_db = False
        tag_repeated = False
        self.assertIs(tag_repeated, False)