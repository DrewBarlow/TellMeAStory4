from django.http import HttpResponse
from django.test import TestCase
from tellmeastory.models import Node

class NodeImageTests(TestCase):
    def test_add_node_to_database(self):
        """
        Creates a node to insert into the database.
        Tests if nodes can be created from Node model
        and stored as necessary.
        """
        return

    def test_add_image_to_node(self):
        """
        Creates a node and adds an image to it, then test
        updates the image stored to a new image.
        """
        return

    def test_add_url_image_to_node(self):
        """
        Add image sourced from another website to be attached to a
        node. The image must be stored in the node after adding the
        url.
        """
        return