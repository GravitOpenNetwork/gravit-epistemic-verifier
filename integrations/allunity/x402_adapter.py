"""
Reference adapter between Gravit Epistemic Verifier and AllUnity x402 Agentic Payments.

This is a conceptual example showing how to integrate the two systems.
"""

from typing import Any, Dict

import requests

from gravit_verifier.engine import VerificationEngine


class X402Adapter:
    """
    Adapter for AllUnity x402 Agentic Payments.

    Usage:
        adapter = X402Adapter(gravit_endpoint="http://localhost:8080")
        result = adapter.verify_payment(payment_request)
        if result["status"] == "passed":
            # Proceed with EURAU settlement
    """

    def __init__(self, gravit_endpoint: str = "http://localhost:8080"):
        self.gravit_endpoint = gravit_endpoint
        self.engine = VerificationEngine()  # local fallback

    def verify_payment(self, payment_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify an agentic payment before settlement.

        Expected payment_request structure:
        {
            "agent_id": str,
            "action": str (e.g., "transfer_funds", "api_call"),
            "amount": float,
            "currency": str (e.g., "EURAU"),
            "reasoning_chain": List[str],
            "context": Dict
        }

        Returns:
        {
            "status": "passed" | "failed",
            "score": float,
            "audit_proof": str,
            "checks": {...}
        }
        """
        # Convert payment request to Gravit verification format
        verification_input = {
            "agent_id": payment_request.get("agent_id"),
            "action": payment_request.get("action"),
            "reasoning_chain": payment_request.get("reasoning_chain", []),
            "context": payment_request.get("context", {}),
            "metadata": {
                "amount": payment_request.get("amount"),
                "currency": payment_request.get("currency", "EURAU"),
            },
        }

        # Call Gravit verifier (prefer remote, fallback to local)
        try:
            response = requests.post(
                f"{self.gravit_endpoint}/v1/verify",
                json=verification_input,
                timeout=5,
            )
            response.raise_for_status()
            result = response.json()
        except requests.RequestException:
            # Fallback to local engine
            result = self.engine.verify(verification_input)

        return {
            "status": "passed" if result.get("decision") == "allowed" else "failed",
            "score": result.get("score", 0.0),
            "audit_proof": result.get("trace_id", ""),
            "checks": result.get("checks", {}),
        }

    def generate_audit_proof(self, trace_id: str) -> Dict[str, Any]:
        """Retrieve full audit proof for compliance (BaFin/MiCAR)."""
        response = requests.get(f"{self.gravit_endpoint}/v1/audit/{trace_id}")
        if response.status_code == 200:
            return response.json()
        return {"error": "not found"}
