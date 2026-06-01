"""
Reference adapter between Gravit Epistemic Verifier and AllUnity x402 Agentic Payments.
"""

from typing import Dict, Any
import requests
from gravit_verifier.engine import VerificationEngine


class X402Adapter:
    def __init__(self, gravit_endpoint: str = "http://localhost:8080"):
        self.gravit_endpoint = gravit_endpoint
        self.engine = VerificationEngine()

    def verify_payment(self, payment_request: Dict[str, Any]) -> Dict[str, Any]:
        verification_input = {
            "agent_id": payment_request.get("agent_id"),
            "action": payment_request.get("action"),
            "reasoning_chain": payment_request.get("reasoning_chain", []),
            "context": payment_request.get("context", {}),
            "metadata": {
                "amount": payment_request.get("amount"),
                "currency": payment_request.get("currency", "EURAU")
            }
        }

        try:
            response = requests.post(
                f"{self.gravit_endpoint}/v1/verify",
                json=verification_input,
                timeout=5
            )
            response.raise_for_status()
            result = response.json()
        except requests.RequestException:
            result = self.engine.verify(verification_input).__dict__

        return {
            "status": "passed" if result.get("decision") == "allowed" else "failed",
            "score": result.get("score", 0.0),
            "audit_proof": result.get("trace_id", ""),
            "checks": result.get("checks", {})
        }

    def generate_audit_proof(self, trace_id: str) -> Dict[str, Any]:
        response = requests.get(f"{self.gravit_endpoint}/v1/audit/{trace_id}")
        return response.json() if response.status_code == 200 else {"error": "not found"}
