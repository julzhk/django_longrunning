from django.core.urlresolvers import resolve
from django.test import TestCase
import json
from django.http import HttpRequest
from longprocess import index, urlpatterns, start_process, get_process_progress, stop_process, status
from time import sleep


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/', urlconf=urlpatterns)
        self.assertEqual(found.func, index)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        self.assertIn(b'long running python', response.content)
        self.assertTrue(response.content.startswith(b'<!doctype html>'))
        self.assertIn(b'<title>long running python</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))


class ProcessTest(TestCase):
    def test_start_process(self):
        request = HttpRequest()
        response = start_process(request)
        self.assertTrue(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data, {'started': True})

    def test_stop_started_process(self):
        request = HttpRequest()
        start_process(request)
        sleep(1.1)
        request = HttpRequest()
        response = stop_process(request)
        self.assertTrue(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('started' in data)
        self.assertEqual(data['started'], False)

    def test_get_started_process(self):
        request = HttpRequest()
        response = start_process(request)
        sleep(1.1)
        request = HttpRequest()
        response = get_process_progress(request)
        self.assertTrue(response.status_code, 200)

    def test_get_process_status(self):
        request = HttpRequest()
        response = start_process(request)
        response = status(request)
        data = json.loads(response.content)
        self.assertTrue(data['started'], True)

    def test_get_process_progress(self):
        request = HttpRequest()
        start_process(request)
        sleep(1.1)
        request = HttpRequest()
        response = get_process_progress(request)
        self.assertTrue(response.status_code, 200)
        self.assertTrue('progress' in json.loads(response.content))
        self.assertDictEqual({'progress': 1.0}, json.loads(response.content))
