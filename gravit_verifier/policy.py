"""
Policy validator for intent/action approval.
"""

from __future__ import annotations

from typing import Any, Dict


class PolicyValidator:
    def validate(self, intent: Dict[str, Any], action: Dict[str, Any]) -> Dict[str, float]:
        intent_text = (intent or {}).get("natural_language", "").lower()
        operations = (action or {}).get("operations", [])
        action_text = " ".join(str(operation) for operation in operations).lower()

        score = 0.35
        if not intent_text or not operations:
            score = 0.1
        if "verified" in intent_text or "verified" in action_text:
            score += 0.25
        if any(keyword in action_text for keyword in ["transfer", "send", "pay"]):
            score += 0.15
        if any(keyword in intent_text for keyword in ["invoice", "salary", "supplier"]):
            score += 0.1
        if any(keyword in action_text for keyword in ["unknown", "bypass", "force"]):
            score -= 0.35
        return {"policy_score": float(max(0.0, min(0.99, score)))}