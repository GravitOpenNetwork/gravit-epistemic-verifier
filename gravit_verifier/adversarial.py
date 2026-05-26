import re
from typing import List, Dict, Any, Tuple

class AdversarialDetector:
    """
    Detects adversarial patterns, prompt injection, and manipulation attempts
    in agent reasoning chains and action descriptions.
    """

    def __init__(self, risk_threshold: float = 0.6):
        self.risk_threshold = risk_threshold

        self.suspicious_patterns = [
            (r"(?i)ignore (all|previous|security|policy|check|verification)", "instruction_override"),
            (r"(?i)bypass (security|verification|check|policy)", "security_bypass"),
            (r"(?i)pretend (you are|to be)", "role_impersonation"),
            (r"(?i)do not (verify|check|validate)", "verification_skip"),
            (r"(?i)you must (obey|follow) me", "authority_override"),
            (r"(?i)system override", "system_override"),
            (r"(?i)disable (safety|security|verification)", "safety_disable"),
            (r"(?i)previous (instructions|rules?) (are (wrong|invalid|incorrect))", "rule_invalidation"),
            (r"(?i)forget (your|all|the) (constraints|policies|rules)", "memory_override"),
            (r"(?i)act as (admin|superuser|root)", "privilege_escalation")
        ]

    def detect(self, intent_text: str, action_text: str) -> float:
        """
        Returns adversarial risk score between 0.0 (safe) and 1.0 (high risk)
        """
        combined = (intent_text + " " + action_text).lower()

        total_risk = 0.0
        detected_patterns = []

        for pattern, category in self.suspicious_patterns:
            if re.search(pattern, combined):
                total_risk += 0.15
                detected_patterns.append(category)

        # Additional heuristics
        if self._has_contradictory_claims(intent_text, action_text):
            total_risk += 0.25

        if self._has_unusual_length_mismatch(intent_text, action_text):
            total_risk += 0.1

        return min(total_risk, 1.0)

    def analyze(self, intent_text: str, action_text: str) -> Dict[str, Any]:
        """
        Returns detailed adversarial analysis
        """
        risk_score = self.detect(intent_text, action_text)

        return {
            "risk_score": round(risk_score, 4),
            "is_suspicious": risk_score >= self.risk_threshold,
            "threshold": self.risk_threshold,
            "detected_patterns": self._get_matched_patterns(intent_text, action_text),
            "recommendation": "block" if risk_score >= self.risk_threshold else "review" if risk_score >= 0.3 else "allow"
        }

    def _get_matched_patterns(self, intent: str, action: str) -> List[str]:
        combined = (intent + " " + action).lower()
        matched = []
        for pattern, category in self.suspicious_patterns:
            if re.search(pattern, combined):
                matched.append(category)
        return matched

    def _has_contradictory_claims(self, intent: str, action: str) -> bool:
        """Check for explicit contradictions"""
        contradict_pairs = [
            ("approve", "deny"),
            ("allow", "forbid"),
            ("confirm", "cancel"),
            ("increase", "decrease")
        ]

        intent_lower = intent.lower()
        action_lower = action.lower()

        for a, b in contradict_pairs:
            if a in intent_lower and b in action_lower:
                return True
            if b in intent_lower and a in action_lower:
                return True
        return False

    def _has_unusual_length_mismatch(self, intent: str, action: str) -> bool:
        """Detect extreme length differences (possible obfuscation)"""
        len_intent = len(intent.split())
        len_action = len(action.split())

        if len_intent == 0 or len_action == 0:
            return False

        ratio = max(len_intent, len_action) / min(len_intent, len_action)
        return ratio > 5
