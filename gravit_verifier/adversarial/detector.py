import re
from typing import Dict

class AdversarialDetector:
    def detect(self, intent: str, action: str) -> float:
        risk = 0.0
        a_lower = action.lower()
        if any(w in a_lower for w in ["ignore previous", "disregard", "override"]):
            risk += 0.8
        if ("unknown" in a_lower or "blacklist" in a_lower) and "transfer" in a_lower:
            risk += 0.7
        if re.search(r"delegate|sub-agent", a_lower):
            risk += 0.35
        return round(min(risk, 1.0), 4)
