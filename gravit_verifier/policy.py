class PolicyValidator:

    def validate(self, intent: str, action: str) -> bool:
        forbidden = ["blacklist", "sanctioned", "unknown wallet"]

        for f in forbidden:
            if f in action.lower():
                return False

        return True
