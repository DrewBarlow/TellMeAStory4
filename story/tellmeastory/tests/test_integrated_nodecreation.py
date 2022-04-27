from django.test import TestCase
from tellmeastory.models import Node, User
from selenium import webdriver
from django.test import LiveServerTestCase
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class AddNodeFromUserTests(TestCase):

    def test_enter_node_information(self):
        """
        Test a user entering information about a node.
        The fields should all be present for title, text
        content, image, and tags.
        """
        return

    def test_submit_node_information(self):
        """
        Tests submitting a node with various data
        needed for a node.
        """
        return

    def test_author_story(self):
        """
        Tests if a logged in user submitting a node
        can author a story as their user.
        """
        return

    def test_attach_tag_to_authored_story(self):
        """
        Tests if a tag can be attached to a story
        and if a new tag can be attached to a story.
        """
        return

    def test_existing_stories_present(self):
        """
        Tests if the existing stories of a user are present
        on the node creation page.
        """
        return
