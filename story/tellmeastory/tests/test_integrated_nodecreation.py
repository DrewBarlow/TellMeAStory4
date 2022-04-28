from django.test import TestCase
from tellmeastory.models import Node, User
from managetags.models import Tag
from selenium import webdriver
from django.test import LiveServerTestCase
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class AddNodeFromUserTests(LiveServerTestCase):

    def test_enter_node_information(self):
        """
        Function contains Sections 1 and 2.
        Section 1 is Setup and Input
        Section 2 is Submission and Check

        Section 1 of Function
        Test a user entering information about a node.
        The fields should all be present for title, text
        content, image, and tags.
        """
        # Create a test user for login
        username = "namename"
        password = "password1"
        display_name = "display"
        # Register above credentials
        selenium_browser = webdriver.Chrome(ChromeDriverManager().install())
        selenium_browser.get('%s%s' % (self.live_server_url, '/register/'))
        username_input = selenium_browser.find_element(By.NAME, value="username")
        username_input.send_keys(username)  # Enter username
        password_input = selenium_browser.find_element(By.NAME, value="password")
        password_input.send_keys(password)  # Enter password
        display_name_input = selenium_browser.find_element(By.NAME, value="display_name")
        display_name_input.send_keys(display_name)  # Enter display name
        selenium_browser.find_element(By.XPATH, value='//input[@value="Register"]').click()
        # Login using the above credientials
        selenium_browser.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = selenium_browser.find_element(By.NAME, value="username")
        username_input.send_keys(username)  # Enter username
        password_input = selenium_browser.find_element(By.NAME, value="password")
        password_input.send_keys(password)  # Enter password
        selenium_browser.find_element(By.XPATH, value='//input[@value="Login"]').click()
        # Navigate to Story Posting for given user
        selenium_browser.get('%s%s' % (self.live_server_url, '/author-story/'+username))
        # Enter Title, Content, One Image, and a Main Tag ID (after first creating a Tag)
        TagToInsert = Tag(name_text="name123", language="en_US")
        TagToInsert.add_new_tag() # Create Main Tag to Add
        title_input = selenium_browser.find_element(By.NAME, value="node_title")
        title_input.send_keys("title")  # Enter story title
        content_input = selenium_browser.find_element(By.NAME, value="node_content")
        content_input.send_keys("content")  # Enter story content
        image_input = selenium_browser.find_element(By.NAME, value="image_url")
        image_input.send_keys("www.google.com")  # Enter valid URL
        main_tag_input = selenium_browser.find_element(By.NAME, value="main_tag_id")
        main_tag_input.send_keys(TagToInsert.id)  # Enter valid tag id
        """
        Section 2 of Function
        Tests submitting a node with various data
        needed for a node and check if node was 
        correctly saved.
        """
        # Submit content entered from above
        selenium_browser.find_element(By.XPATH, value='//input[@value="Create"]').click()
        # Check that node success message was printed
        success_message = "Successfully Added your Story!"
        self.assertTrue(selenium_browser.page_source.find(success_message) != -1)
        # Check that node exists and the author is the user that registered
        self.assertTrue(Tag.objects.count())  # Check if tags exist
        self.assertTrue(Node.objects.count())  # Check if nodes exist
        self.assertTrue(Node.objects.filter(node_author__username=username).first().node_title == "title")  # Check title
        self.assertTrue(Node.objects.filter(node_author__username=username).first().node_content == "content")  # Check content
        self.assertFalse(Node.objects.filter(node_author__username=username).first().has_image_file)  # Check image
        self.assertTrue(Node.objects.filter(node_author__username=username).first().main_tag_id == TagToInsert.id)  # Check main tag
        return

    def test_add_invalid_story_fields(self):
        """
        Tests invalid input for all story fields. The correct error
        message should appear and no additional nodes should exist.
        """
        return

    def test_existing_stories_and_tags_present(self):
        """
        Tests if the existing stories of a user are present
        on the node creation page and tags too.
        """
        # Create a test user for login
        username = "namename"
        password = "password1"
        display_name = "display"
        # Register above credentials
        selenium_browser = webdriver.Chrome(ChromeDriverManager().install())
        selenium_browser.get('%s%s' % (self.live_server_url, '/register/'))
        username_input = selenium_browser.find_element(By.NAME, value="username")
        username_input.send_keys(username)  # Enter username
        password_input = selenium_browser.find_element(By.NAME, value="password")
        password_input.send_keys(password)  # Enter password
        display_name_input = selenium_browser.find_element(By.NAME, value="display_name")
        display_name_input.send_keys(display_name)  # Enter display name
        selenium_browser.find_element(By.XPATH, value='//input[@value="Register"]').click()
        # Login using the above credientials
        selenium_browser.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = selenium_browser.find_element(By.NAME, value="username")
        username_input.send_keys(username)  # Enter username
        password_input = selenium_browser.find_element(By.NAME, value="password")
        password_input.send_keys(password)  # Enter password
        selenium_browser.find_element(By.XPATH, value='//input[@value="Login"]').click()
        # Navigate to Story Posting for given user
        selenium_browser.get('%s%s' % (self.live_server_url, '/author-story/'+username))
        # Enter Title, Content, One Image, and a Main Tag ID (after first creating a Tag)
        TagToInsert = Tag(name_text="name123", language="en_US")
        TagToInsert.add_new_tag() # Create Main Tag to Add
        title_input = selenium_browser.find_element(By.NAME, value="node_title")
        title_input.send_keys("title")  # Enter story title
        content_input = selenium_browser.find_element(By.NAME, value="node_content")
        content_input.send_keys("content")  # Enter story content
        image_input = selenium_browser.find_element(By.NAME, value="image_url")
        image_input.send_keys("www.google.com")  # Enter valid URL
        main_tag_input = selenium_browser.find_element(By.NAME, value="main_tag_id")
        main_tag_input.send_keys(TagToInsert.id)  # Enter valid tag id
        # Submit content entered from above
        selenium_browser.find_element(By.XPATH, value='//input[@value="Create"]').click()
        """ Now the stories should be present as well as the tags on the posting page. """
        # Navigate to Story Posting for given user
        selenium_browser.get('%s%s' % (self.live_server_url, '/author-story/'+username))
        # Check if the added tag is present on the page with its ID
        tag_with_ID = "ID: " + str(TagToInsert.id) + " Name: " + TagToInsert.name_text
        self.assertTrue(selenium_browser.page_source.find(tag_with_ID) != -1)
        # Check if the added story is present on the page with its ID
        story_with_ID = "ID: " + str(Node.objects.filter(node_author__username=username).first().id)\
                      + " Title: " + Node.objects.filter(node_author__username=username).first().node_title
        self.assertTrue(selenium_browser.page_source.find(story_with_ID) != -1)
        return

