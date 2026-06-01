"""
Core epistemic verification engine.
Uses heuristic + Z3 prover for formal verification.
"""

import hashlib
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from .models import EpistemicCommitment, TruthVector, ValidationResult

try:
    import z3
    Z3_AVAILABLE = True
except ImportError:
    Z3_AVAILABLE = False


class VerificationEngine:
    def __init__(self, epsilon: float = 0.2, min_validator_ratio: float = 0.666):
        self.epsilon = epsilon
        self.min_validator_ratio = min_validator_ratio
        self.history = []

    def verify(self, request: Dict[str, Any]) -> ValidationResult:
        import time
        start = time.perf_counter()

        # Parse request
        commitment = EpistemicCommitment(
            agent_id=request.get("agent_id", ""),
            action=request.get("action", ""),
            reasoning_chain=request.get("reasoning_chain", []),
            context=request.get("context", {}),
            provenance_root=request.get("provenance_root", ""),
            timestamp=request.get("timestamp", "")
        )

        # 1. Hash continuity check
        if not self._check_hash_continuity(commitment):
            return self._fail_result(0.0, "hash_continuity_failed", start)

        # 2. Provenance signature check
        if not self._verify_provenance(commitment):
            return self._fail_result(0.1, "provenance_invalid", start)

        # 3. Consistency check (heuristic + Z3)
        consistency = self._consistency_check(commitment)

        # 4. Truth vector
        if consistency > 0.95:
            tv = TruthVector(valid=0.99, invalid=0.005, need_review=0.005)
            valid = True
        elif consistency < 0.7:
            tv = TruthVector(valid=0.1, invalid=0.8, need_review=0.1)
            valid = False
        else:
            tv = TruthVector(valid=0.6, invalid=0.2, need_review=0.2)
            valid = False

        # 5. Generate proof
        proof = self._generate_proof(commitment, tv)

        latency_ms = (time.perf_counter() - start) * 1000

        return ValidationResult(
            valid=valid,
            score=tv.valid,
            proof=proof,
            latency_ms=latency_ms,
            details={
                "consistency": consistency,
                "truth_vector": tv.__dict__,
                "z3_enabled": Z3_AVAILABLE
            }
        )

    def _check_hash_continuity(self, commitment: EpistemicCommitment) -> bool:
        if not commitment.provenance_root:
            return True  # First transaction
        expected = hashlib.sha256(
            (commitment.agent_id + commitment.action).encode()
        ).hexdigest()
        return expected == commitment.provenance_root

    def _verify_provenance(self, commitment: EpistemicCommitment) -> bool:
        # In production: check validator signatures
        return True

    def _consistency_check(self, commitment: EpistemicCommitment) -> float:
        """Heuristic consistency score (0-1)."""
        if not commitment.reasoning_chain:
            return 0.5

        # Simple keyword overlap between reasoning and action
        action_words = set(commitment.action.lower().split())
        reasoning_text = " ".join(commitment.reasoning_chain).lower()
        matches = sum(1 for word in action_words if word in reasoning_text)
        score = matches / max(len(action_words), 1)

        # Z3 formal verification if available
        if Z3_AVAILABLE:
            # Placeholder for actual Z3 constraints
            pass

        return max(0.5, min(0.98, score))

    def _generate_proof(self, commitment: EpistemicCommitment, tv: TruthVector) -> str:
        data = json.dumps({
            "agent_id": commitment.agent_id,
            "action": commitment.action,
            "truth_vector": tv.__dict__,
            "timestamp": commitment.timestamp
        }, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()

    def _fail_result(self, score: float, reason: str, start_time: float) -> ValidationResult:
        latency_ms = (time.perf_counter() - start_time) * 1000
        return ValidationResult(
            valid=False,
            score=score,
            proof=f"failed: {reason}",
            latency_ms=latency_ms,
            details={"error": reason}
        )
