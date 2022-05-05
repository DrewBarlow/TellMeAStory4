from django.http import HttpResponse
from django.test import LiveServerTestCase, TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

USERNAME: str = "namename"
PASSWORD: str = "password"
DIS_NAME: str = "display"

URL_MAPS = "/story/map/"
class MapPageViewTests(TestCase):

    # We can use this to check if the webpage loaded. Since the
    # Map is loaded client sided. Client can view map as long as the API key is correct
    def test_map_page_loading(self) -> None:
        res: HttpResponse = self.client.get(URL_MAPS)
        print(res.items())
        # Checks to make sure the page loaded correctly
        self.assertEqual(res.status_code, 200)
        # Checks to make sure the map frame loaded within the HTTPResponse
        self.assertContains(res, "<div id='map' width='100%' style='margin-top:100px; height:800px'></div>")

class CreateStoryFromMap(LiveServerTestCase):
    selenium_browser = None

    # setup stolen from test_integrated_nodecreation.py
    def setUp(self) -> None:
        # Register credentials
        self.selenium_browser = webdriver.Chrome(ChromeDriverManager().install())
        self.selenium_browser.get('%s%s' % (self.live_server_url, '/register/'))
        username_input = self.selenium_browser.find_element(By.NAME, value="username")
        username_input.send_keys(USERNAME)  # Enter username
        password_input = self.selenium_browser.find_element(By.NAME, value="password")
        password_input.send_keys(PASSWORD)  # Enter password
        display_name_input = self.selenium_browser.find_element(By.NAME, value="display_name")
        display_name_input.send_keys(DIS_NAME)  # Enter display name
        self.selenium_browser.find_element(By.XPATH, value='//input[@value="Register"]').click()
        # Login using the above credientials
        self.selenium_browser.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium_browser.find_element(By.NAME, value="username")
        username_input.send_keys(USERNAME)  # Enter username
        password_input = self.selenium_browser.find_element(By.NAME, value="password")
        password_input.send_keys(PASSWORD)  # Enter password
        self.selenium_browser.find_element(By.XPATH, value='//input[@value="Login"]').click()

        return

    def test_create_story_from_map(self) -> None:
        # redirect to map page and click in the middle of the screen
        self.selenium_browser.get(f"{self.live_server_url}{URL_MAPS}")
        self.selenium_browser.find_element(By.XPATH, value='//div[@id="map"]').click()

        # verify that we were redirected to the story creation page
        self.assertIn(
            f"{self.live_server_url}/story/author-story/{USERNAME}/",
            self.selenium_browser.current_url
        )