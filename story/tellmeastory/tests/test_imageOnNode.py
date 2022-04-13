from django.http import HttpResponse
from django.test import TestCase
from tellmeastory.models import Node
from django.db.models import ImageField
from tellmeastory.forms import AddImageForm
from django.core.files.uploadedfile import SimpleUploadedFile

class NodeImageTests(TestCase):
    def test_add_image_to_node(self):
        """
        Creates a node and adds an image to it, then test
        updates the image stored to a new image.
        """
        # Check form comes back
        self.assertIsNotNone(AddImageForm(data={"image_file": "storyimages/test_image.jpeg", "id": 1}))
        self.assertIsNotNone(AddImageForm(data={"image_url": "www.google.com", "id": 1}))
        # Add an image from a valid file
        test_image_path = "media/storyimages/test_image.jpeg"
        test_image_file = SimpleUploadedFile(name='test_image.jpeg',
                                             content=open(test_image_path, 'rb').read(),
                                             content_type='image/jpeg')
        node: Node = Node(node_title="Test1")
        node.save()
        self.assertIs(Node.objects.get(id=node.id).add_image(newFile=test_image_file), True)
        self.assertIs(Node.objects.get(id=node.id).has_image_file, True)
        self.assertNotEqual(Node.objects.get(id=node.id).image.url, None)
        return

    def test_add_url_image_to_node(self):
        """
        Add image sourced from another website to be attached to a
        node. The image must be stored in the node after adding the
        url.
        """
        # Add an image from a valid URL
        test_image_url = "https://img.sunset02.com/sites/default/files/styles/marquee_large_2x/public/image/2016/07/main/western-palm-trees-mexican-fan-palms-elysian-park-0214.jpg"
        node: Node = Node(node_title="Test2")
        node.save()
        self.assertIs(Node.objects.get(id=node.id).add_image(newURL=test_image_url), True)
        # Add an image from an invalid URL
        test_image_url = "invalidlink_testing"
        node: Node = Node(node_title="Test3")
        node.add_image(newURL=test_image_url)
        return

    def test_change_image(self):
        """
        Swap between URL and file images. Should not cause
        errors and properties must be updated.
        """
        test_image_file ="media/storyimages/test_image.jpeg"
        test_image_url = "https://img.sunset02.com/sites/default/files/styles/marquee_large_2x/public/image/2016/07/main/western-palm-trees-mexican-fan-palms-elysian-park-0214.jpg"
        node: Node = Node(node_title="Test4")
        # Intialize with a valid file
        node.add_image(newFile=test_image_file)
        # Swap to URL from file
        node.add_image(newURL=test_image_url)
        # Swap to file from URL
        node.add_image(newFile=test_image_file)
        return
