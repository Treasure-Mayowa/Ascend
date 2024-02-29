from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class TestPages(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_tools_page(self):
        response = self.client.get(reverse("tools"))
        self.assertEqual(response.status_code, 200)

    def test_resources_page(self):
        response = self.client.get(reverse("resources"))
        self.assertEqual(response.status_code, 200)
