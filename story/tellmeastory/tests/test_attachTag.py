from django.test import TestCase
from tellmeastory.models import Node
from managetags.models import Tag

class AttachTagTests(TestCase):

    def test_attaching_tag_to_node(self):
        '''
        A created Tag is tested by attempting to attach it
        to an exisiting Node. The Tag and Node are tested
        elsewhere and can be assumed as functioning seperately
        for now.
        '''

        return

    def test_change_tag_on_node(self):
        '''
        The main tag on a node can change after creation.
        This function tests that change.
        '''

        return