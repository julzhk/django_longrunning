from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest, QueryDict
from hello import index,urlpatterns

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/', urlconf = urlpatterns)
        self.assertEqual(found.func, index)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        self.assertIn(b'Hello', response.content)
        # self.assertTrue(response.content.startswith(b'<html>'))
        # self.assertIn(b'<title>Artist Search API</title>', response.content)
        # self.assertTrue(response.content.endswith(b'</html>'))
