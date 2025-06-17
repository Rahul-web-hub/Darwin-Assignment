# blog_app/tests.py
from django.test import TestCase, Client
import json

class TitleSuggestionTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_title_suggestion(self):
        test_content = "How to build a Django project with AI features"
        response = self.client.post(
            '/api/blog/suggest-titles/',
            data=json.dumps({'content': test_content}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['titles']), 3)