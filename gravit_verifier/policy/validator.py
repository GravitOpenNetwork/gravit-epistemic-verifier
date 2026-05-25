class PolicyValidator:
    def __init__(self):
        self.forbidden = ["blacklist", "sanctioned", "unknown wallet", "hack", "launder"]

    def validate(self, intent: str, action: str) -> bool:
        text = (intent + " " + action).lower()
        return all(p not in text for p in self.forbidden)
