"""
Adversarial detector for suspicious intent/action pairs.
"""

from __future__ import annotations

import re


class AdversarialDetector:
    def detect(self, intent_text: str, action_text: str) -> float:
        text = f"{intent_text or ''} {action_text or ''}".lower()
        suspicious = ["ignore", "bypass", "unknown wallet", "replay", "fake", "attack", "steal", "instructions"]
        safe = ["verified", "authorized", "employee", "iban"]
        risk = 0.02
        risk += 0.24 * sum(1 for keyword in suspicious if keyword in text)
        risk -= 0.1 * sum(1 for keyword in safe if keyword in text)
        if not re.search(r"[a-z0-9]", text):
            return 0.0
        return float(max(0.0, min(0.99, risk)))