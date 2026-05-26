import json
from typing import Dict, Any, List, Tuple
from pathlib import Path

class PolicyValidator:
    """
    Validates agent actions against predefined policies and constraints.
    Supports role-based, amount-based, and recipient-based rules.
    """

    def __init__(self, policy_file: str = None):
        self.policies = self._load_default_policies()
        if policy_file and Path(policy_file).exists():
            self._load_policy_file(policy_file)

    def _load_default_policies(self) -> Dict[str, Any]:
        return {
            "version": "1.0",
            "rules": [
                {
                    "id": "POL001",
                    "name": "max_transfer_amount",
                    "type": "numeric_limit",
                    "parameter": "amount",
                    "max_value": 10000,
                    "severity": "high"
                },
                {
                    "id": "POL002",
                    "name": "verified_recipient_required",
                    "type": "whitelist",
                    "parameter": "recipient",
                    "allowed_values": ["verified_iban_123", "verified_wallet_456"],
                    "severity": "critical"
                },
                {
                    "id": "POL003",
                    "name": "no_self_transfer",
                    "type": "inequality",
                    "parameter": "recipient",
                    "forbidden_equals": "sender",
                    "severity": "medium"
                }
            ]
        }

    def _load_policy_file(self, path: str) -> None:
        with open(path, 'r') as f:
            file_policies = json.load(f)
            if "rules" in file_policies:
                self.policies["rules"].extend(file_policies["rules"])

    def validate(self, intent_text: str, action_text: str) -> bool:
        """
        Returns True if action complies with all relevant policies
        """
        violations = self._check_violations(intent_text, action_text)
        return len(violations) == 0

    def validate_detailed(self, intent_text: str, action_text: str) -> Dict[str, Any]:
        """
        Returns detailed policy validation report
        """
        violations = self._check_violations(intent_text, action_text)

        return {
            "passed": len(violations) == 0,
            "violations": violations,
            "violation_count": len(violations),
            "policies_checked": len(self.policies["rules"])
        }

    def _check_violations(self, intent: str, action: str) -> List[Dict[str, Any]]:
        violations = []

        for rule in self.policies["rules"]:
            if rule["type"] == "numeric_limit":
                violation = self._check_numeric_limit(rule, action)
                if violation:
                    violations.append(violation)

            elif rule["type"] == "whitelist":
                violation = self._check_whitelist(rule, action)
                if violation:
                    violations.append(violation)

            elif rule["type"] == "inequality":
                violation = self._check_inequality(rule, action)
                if violation:
                    violations.append(violation)

        return violations

    def _check_numeric_limit(self, rule: Dict, action: str) -> Dict | None:
        """Check amount limits against action description"""
        param = rule["parameter"]
        max_val = rule["max_value"]

        # Simple extraction: look for numbers
        import re
        numbers = re.findall(r'\b\d+\b', action)

        for num_str in numbers:
            value = int(num_str)
            if value > max_val:
                return {
                    "rule_id": rule["id"],
                    "rule_name": rule["name"],
                    "violation": f"{param} {value} exceeds maximum {max_val}",
                    "severity": rule["severity"]
                }
        return None

    def _check_whitelist(self, rule: Dict, action: str) -> Dict | None:
        """Check if parameter value is in allowed list"""
        param = rule["parameter"]
        allowed = rule["allowed_values"]

        # Simple heuristic: check if any allowed value appears in action
        found = any(str(value) in action for value in allowed)

        if not found and "transfer" in action.lower():
            return {
                "rule_id": rule["id"],
                "rule_name": rule["name"],
                "violation": f"{param} not in allowed list",
                "severity": rule["severity"]
            }
        return None

    def _check_inequality(self, rule: Dict, action: str) -> Dict | None:
        """Check forbidden equality constraints"""
        param = rule["parameter"]
        forbidden = rule["forbidden_equals"]

        # Heuristic: detect self-transfer patterns
        if "self" in action.lower() or "own" in action.lower():
            if "transfer" in action.lower():
                return {
                    "rule_id": rule["id"],
                    "rule_name": rule["name"],
                    "violation": f"{param} equals {forbidden} (self-transfer)",
                    "severity": rule["severity"]
                }
        return None
