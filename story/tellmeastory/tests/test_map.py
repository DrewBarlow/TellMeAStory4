from django.http import HttpResponse
from django.test import TestCase

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