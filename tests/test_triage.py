import unittest
from src.triage_classifier import MedicalTriageClassifier


class TestMedicalTriageClassifier(unittest.TestCase):
    def test_detects_cardiac_emergency(self):
        query = "I have sudden crushing chest pain radiating to arm"
        res = MedicalTriageClassifier.classify(query)
        self.assertTrue(res["is_emergency"])
        self.assertEqual(res["triage_level"], "CRITICAL_EMERGENCY")
        self.assertEqual(res["category"], "cardiac")
        self.assertIn("911", res["advisory"])

    def test_detects_respiratory_emergency(self):
        query = "Help, my child can't breathe and is gasping for air"
        res = MedicalTriageClassifier.classify(query)
        self.assertTrue(res["is_emergency"])
        self.assertEqual(res["category"], "respiratory")

    def test_detects_neurological_stroke_symptoms(self):
        query = "My grandfather has sudden numbness on one side and slurred speech"
        res = MedicalTriageClassifier.classify(query)
        self.assertTrue(res["is_emergency"])
        self.assertEqual(res["category"], "neurological")

    def test_detects_anaphylaxis_crisis(self):
        query = "I ate peanuts and my throat closing fast"
        res = MedicalTriageClassifier.classify(query)
        self.assertTrue(res["is_emergency"])
        self.assertEqual(res["category"], "anaphylaxis")

    def test_urgent_evaluation_level(self):
        query = "I have had persistent vomiting and severe abdominal pain all morning"
        res = MedicalTriageClassifier.classify(query)
        self.assertFalse(res["is_emergency"])
        self.assertEqual(res["triage_level"], "URGENT_EVALUATION")

    def test_routine_inquiry(self):
        query = "What is the recommended daily intake of Vitamin D?"
        res = MedicalTriageClassifier.classify(query)
        self.assertFalse(res["is_emergency"])
        self.assertEqual(res["triage_level"], "ROUTINE")
        self.assertIsNone(res["advisory"])


if __name__ == "__main__":
    unittest.main()
