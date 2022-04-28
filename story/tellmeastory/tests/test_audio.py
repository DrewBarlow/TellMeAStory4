from django.http import HttpResponse
from django.test import TestCase
from tellmeastory.models import Node
from django.db.models import FileField
from tellmeastory.forms import AudioForm
from django.core.files.uploadedfile import SimpleUploadedFile

class NodeAudioTests(TestCase):
    def test_add_audio_to_node(self):
        """
        Creates a node and adds an audio to it, then test
        updates the audio stored to a new image.
        """
        # Check form comes back
        self.assertIsNotNone(AudioForm(data={"audio_file": "storyaudio/test_audio.wav", "id": 1}))
        # Add an audio from a valid file
        test_audio_path = "media/storyaudio/test_audio.wav"
        test_audio_file = SimpleUploadedFile(name='test_audio.wav',
                                             content=open(test_audio_path, 'rb').read(),
                                             content_type='audio/wav')
        node: Node = Node(node_title="Test1")
        node.save()
        self.assertIs(Node.objects.get(id=node.id).add_audio(newFile=test_audio_file), True)
        self.assertIs(Node.objects.get(id=node.id).audio_exists, True)
        return

    def test_add_audio_view(self):
        '''
        Test for proper responses from submitting multiple possible forms
        to the add audio to a node view.
        '''
        # Test image file
        test_audio_path = "media/storyaudio/test_audio.wav"
        test_audio_file = SimpleUploadedFile(name='test_audio.wav',
                                             content=open(test_audio_path, 'rb').read(),
                                             content_type='audio/wav')

        all_nodes = Node.objects.filter()
        err_msg = "N/A"

        # Create test node
        node: Node = Node(node_title="Test5")
        node.save()

        # Process basic request for audio
        self.client.get("/story/audio/")  # Process basic request for prompts
        res: HttpResponse = self.client.post("/story/audio/", data={
            "form": AudioForm,
            "err_msg": err_msg,
            "audio_file": test_audio_file,
            "id": node.id,
            "nodes": all_nodes
        })
        self.assertEqual(res.status_code, 200)
        # Process basic request with invalid node
        self.client.get("/story/audio/")  # Process basic request for prompts
        res: HttpResponse = self.client.post("/story/audio/", data={
            "form": AudioForm,
            "err_msg": err_msg,
            "image_file": test_audio_file,
            "id": 0,
            "nodes": all_nodes
        })
        self.assertEqual(res.status_code, 200)
        return