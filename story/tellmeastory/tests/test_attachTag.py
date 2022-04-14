from django.test import TestCase
from tellmeastory.models import Node
from managetags.models import Tag

class AttachTagTests(TestCase):

    def test_attaching_main_tag_to_node(self):
        '''
        A created Tag is tested by attempting to attach it
        to an exisiting Node. The Tag and Node are tested
        elsewhere and can be assumed as functioning seperately
        for now.
        '''
        # Establish a new Tag and Node to connect
        new_tag: Tag = Tag(name_text="Test1Tag", language="en")
        new_node: Node = Node(node_title="Test1Node")
        new_node.save()
        # Attach the Tag to the Node using the Tag's properties
        self.assertIs(new_tag.add_new_tag(), True)
        self.assertIs(new_node.attach_main_tag(new_tag.add_tag_to_node()), True)
        # Check if the Tag is attached properly
        self.assertEqual(new_tag.id, new_node.main_tag.id)
        self.assertIs(new_tag, new_node.main_tag)
        return

    def test_change_main_tag_on_node(self):
        '''
        The main tag on a node can change after creation.
        This function tests that change.
        '''
        # Establish a new Tag and Node to connect
        new_tag: Tag = Tag(name_text="Test2Tag", language="en")
        new_node: Node = Node(node_title="Test2Node")
        new_node.save()
        # Attach the Tag to the Node using the Tag's properties
        self.assertIs(new_tag.add_new_tag(), True)
        self.assertIs(new_node.attach_main_tag(new_tag.add_tag_to_node()), True)
        # Check if the Tag is attached properly
        self.assertEqual(new_tag.id, new_node.main_tag.id)
        self.assertIs(new_tag, new_node.main_tag)

        # Now Change the Main Tag
        new_tag: Tag = Tag(name_text="Test3Tag", language="en")
        # Attach the Tag to the Node using the Tag's properties
        self.assertIs(new_tag.add_new_tag(), True)
        self.assertIs(new_node.attach_main_tag(new_tag.add_tag_to_node()), True)
        # Check if the Tag is attached properly
        self.assertEqual(new_tag.id, new_node.main_tag.id)
        self.assertIs(new_tag, new_node.main_tag)
        return

    def test_attaching_other_tags(self):
        '''
        Tests attaching other tags to a Node.
        '''
        # Establish a new Tag and Node to connect
        new_tag: Tag = Tag(name_text="Test4Tag", language="en")
        new_node: Node = Node(node_title="Test4Node")
        new_node.save()
        # Attach the Tag to the Node using the Tag's properties
        self.assertIs(new_tag.add_new_tag(), True)
        self.assertIs(new_node.attach_tag(new_tag.add_tag_to_node()), True)
        # Check if the Tag is attached properly
        self.assertIs(new_tag, new_node.other_tags.objects().filter(id=new_tag.id))

        new_tag: Tag = Tag(name_text="Test5Tag", language="en")
        # Add multiple Tags (in addition to first)
        # Attach the Tag to the Node using the Tag's properties
        self.assertIs(new_tag.add_new_tag(), True)
        self.assertIs(new_node.attach_tag(new_tag.add_tag_to_node()), True)
        # Check if the Tag is attached properly
        self.assertIs(new_tag, new_node.other_tags.objects().filter(id=new_tag.id))
        return
