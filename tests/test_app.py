"""
MediBot-AI - Application & Prompt Unit Tests
--------------------------------------------
Validates health endpoints, file extension security filters,
and prompt template variables.
"""
import os
import sys
import unittest

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from app import app, allowed_file
from src.prompt import system_prompt


class MediBotAppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()

    def test_01_health_endpoint(self):
        """Verify /health endpoint returns 200 with service metadata."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data.get("status"), "healthy")
        self.assertEqual(data.get("service"), "medibot-ai")

    def test_02_allowed_file_types(self):
        """Verify allowed and blocked file extensions."""
        self.assertTrue(allowed_file("medical_scan.pdf"))
        self.assertTrue(allowed_file("xray.png"))
        self.assertTrue(allowed_file("report.jpg"))
        self.assertTrue(allowed_file("notes.txt"))
        self.assertTrue(allowed_file("image.WEBP"))

        self.assertFalse(allowed_file("malicious.exe"))
        self.assertFalse(allowed_file("script.sh"))
        self.assertFalse(allowed_file("payload.py"))
        self.assertFalse(allowed_file("no_extension"))
        self.assertFalse(allowed_file(""))
        self.assertFalse(allowed_file(None))

    def test_03_index_requires_login(self):
        """Verify unauthenticated access to root redirects to login."""
        response = self.client.get("/", follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

    def test_04_history_requires_login(self):
        """Verify unauthenticated access to /history redirects to login."""
        response = self.client.get("/history", follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    def test_05_system_prompt_structure(self):
        """Verify system prompt contains essential medical disclaimers and context placeholder."""
        self.assertIn("{context}", system_prompt)
        self.assertIn("MediBot", system_prompt)
        self.assertIn("doctor", system_prompt.lower())
        self.assertIn("educational purposes", system_prompt.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
