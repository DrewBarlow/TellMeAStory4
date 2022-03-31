from django.http import HttpResponse
from django.test import TestCase

URL_MAPS = "/story/map/"
class MapPageViewTests(TestCase):

    # We can use this to check if the webpage loaded. Since the
    # Map is loaded client sided. Client can view map as long as the API key is correct
    def test_map_page_loading(self) -> None:
        res: HttpResponse = self.client.get(URL_MAPS)
        self.assertEqual(res.status_code, 200)


