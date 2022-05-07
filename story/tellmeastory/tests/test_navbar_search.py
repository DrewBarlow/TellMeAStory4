from django.test import TestCase
from tellmeastory.models import Node, User
from managetags.models import Tag
from selenium import webdriver
from django.test import LiveServerTestCase
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from hashlib import sha512
from django.core.files.uploadedfile import SimpleUploadedFile

class AddNodeFromUserTests(LiveServerTestCase):

    def test_enter_node_information(self):
        """
        Tests that navbar search redirects to correct
        search results page on all modified pages.
        """
        # Navigate to profile not found page
        # Test search redirect here
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
        # Enter longitude and latitude
        title_input = selenium_browser.find_element(By.NAME, value="latitude")
        title_input.send_keys(0)  # Enter latitude
        title_input = selenium_browser.find_element(By.NAME, value="longitude")
        title_input.send_keys(0)  # Enter longitude
        # Submit content entered from above
        selenium_browser.find_element(By.XPATH, value='//input[@value="Create"]').click()
        # Test search redirect here
        # Navigate to account page
        # Test search redirect here
        # Navigate to login page
        # Test search redirect here
        # Navigate to map page
        # Test search redirect here
        # Navigate to profile page
        # Test search redirect here
        # Navigate to register page
        # Test search redirect here
        return

    def test_content_present_in_search_results(self):
        """
        Test checks for the presence of all required parts
        of a story presentation. This includes the title,
        author, maturity, and location.
        """
        return

    def test_immature_user_cannot_search_mature_content(self):
        """
        Test checks that an immature user cannot find
        mature story content.
        """
        return

    def test_exact_search_results(self):
        """
        Tests the search results of a variety of
        scenarios. This includes but is not limited
        to no results, some results, all results.
        TEST ONLY TESTS FOR EXACT MATCHES
        """
        return

    def test_partial_search_results(self):
        """
        Tests the search results of a variety of
        scenarios. This includes but is not limited
        to no results, some results, all results.
        TEST ONLY TESTS FOR PARTIAL MATCHES
        """
        return
