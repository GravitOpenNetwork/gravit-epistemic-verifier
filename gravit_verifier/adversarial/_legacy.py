class AdversarialDetector:

    def detect(self, intent: str, action: str) -> float:
        # baseline heuristic (v1)
        risk = 0.0

        if "transfer" in action.lower() and "unknown" in action.lower():
            risk += 0.7

        if intent.lower() not in action.lower():
            risk += 0.3

        return min(risk, 1.0)
