"""
MediBot Emergency Symptom Triage Classifier
Detects high-acuity medical emergencies and triggers immediate safety warnings
advising users to seek emergency care (911 / 112 / 999).
"""

import re
from typing import Dict, List, Tuple


EMERGENCY_SIGNALS = {
    "cardiac": [
        r"\b(crushing chest pain|heart attack|chest tightness radiating to arm|chest pressure)\b"
    ],
    "respiratory": [
        r"\b(can'?t breathe|severe shortness of breath|suffocating|choking|gasping for air)\b"
    ],
    "neurological": [
        r"\b(sudden numbness on one side|facial drooping|slurred speech|stroke symptoms|sudden blindness)\b"
    ],
    "trauma_hemorrhage": [
        r"\b(uncontrolled bleeding|coughing up blood|severe head trauma|deep stab|compound fracture)\b"
    ],
    "crisis": [
        r"\b(suicide|suicidal|end my life|kill myself|overdose)\b"
    ],
    "anaphylaxis": [
        r"\b(throat closing|severe allergic reaction|anaphylaxis|swollen tongue)\b"
    ]
}

URGENT_SIGNALS = [
    r"\b(high fever above 104|persistent vomiting|severe abdominal pain|dehydration)\b"
]


class MedicalTriageClassifier:
    @classmethod
    def classify(cls, query: str) -> Dict:
        """
        Analyzes user input for emergency or urgent indicators.
        Returns triage level, category, and standard clinical guidance.
        """
        if not query or not query.strip():
            return {
                "triage_level": "ROUTINE",
                "is_emergency": False,
                "category": None,
                "matches": [],
                "advisory": None
            }

        q_lower = query.lower()

        # Check for Critical Emergency
        for category, patterns in EMERGENCY_SIGNALS.items():
            for pat in patterns:
                matched = re.findall(pat, q_lower)
                if matched:
                    return {
                        "triage_level": "CRITICAL_EMERGENCY",
                        "is_emergency": True,
                        "category": category,
                        "matches": [m[0] if isinstance(m, tuple) else m for m in matched],
                        "advisory": (
                            "CRITICAL MEDICAL ALERT: Your symptoms may indicate an acute, life-threatening "
                            "medical emergency. Do NOT rely on AI. Call emergency services immediately (911 in US, "
                            "112 in EU/India, 999 in UK) or proceed to the nearest emergency room."
                        )
                    }

        # Check for Urgent Evaluation
        for pat in URGENT_SIGNALS:
            matched = re.findall(pat, q_lower)
            if matched:
                return {
                    "triage_level": "URGENT_EVALUATION",
                    "is_emergency": False,
                    "category": "urgent_medical",
                    "matches": [m[0] if isinstance(m, tuple) else m for m in matched],
                    "advisory": "URGENT: These symptoms require prompt evaluation by a licensed healthcare professional within 12-24 hours."
                }

        return {
            "triage_level": "ROUTINE",
            "is_emergency": False,
            "category": None,
            "matches": [],
            "advisory": None
        }
