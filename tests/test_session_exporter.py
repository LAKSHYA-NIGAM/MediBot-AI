import json
import unittest
from src.session_exporter import SessionExporter


class TestSessionExporter(unittest.TestCase):
    def setUp(self):
        self.session_id = "sess_med_889"
        self.patient_id = "pat_456"
        self.messages = [
            {"role": "user", "timestamp": "2026-11-21 10:00:00", "content": "I have a mild headache."},
            {"role": "assistant", "timestamp": "2026-11-21 10:00:05", "content": "Stay hydrated and rest."}
        ]

    def test_export_to_markdown(self):
        md = SessionExporter.to_markdown(self.session_id, self.messages, self.patient_id)
        self.assertIn("Clinical Consultation Transcript", md)
        self.assertIn("sess_med_889", md)
        self.assertIn("User (2026-11-21 10:00:00)", md)
        self.assertIn("Disclaimer", md)

    def test_export_to_json(self):
        json_str = SessionExporter.to_json(self.session_id, self.messages, self.patient_id)
        data = json.loads(json_str)
        self.assertEqual(data["session_id"], "sess_med_889")
        self.assertEqual(data["message_count"], 2)
        self.assertEqual(len(data["messages"]), 2)

    def test_export_to_csv(self):
        csv_str = SessionExporter.to_csv(self.messages)
        lines = csv_str.strip().splitlines()
        self.assertEqual(len(lines), 3)  # Header + 2 rows
        self.assertTrue(lines[0].startswith("index,role,timestamp,content"))
        self.assertIn("user", lines[1])
        self.assertIn("mild headache", lines[1])


if __name__ == "__main__":
    unittest.main()
