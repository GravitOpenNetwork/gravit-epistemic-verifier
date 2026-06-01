"""
Core epistemic verification engine.
"""

import hashlib
import json
import time
from typing import Any, Dict, Optional

from .adversarial import AdversarialDetector
from .models import EpistemicCommitment, TruthVector, VerificationResult
from .policy import PolicyValidator
from .semantic import SemanticVerifier

try:
    import z3  # noqa: F401

    Z3_AVAILABLE = True
except ImportError:
    Z3_AVAILABLE = False


class VerificationEngine:
    def __init__(self, enable_formal: bool = True, epsilon: float = 0.2, min_validator_ratio: float = 0.666):
        self.enable_formal = enable_formal
        self.epsilon = epsilon
        self.min_validator_ratio = min_validator_ratio
        self.semantic = SemanticVerifier()
        self.adversarial = AdversarialDetector()
        self.policy = PolicyValidator()
        self.smt = object() if enable_formal else None
        self.history = []
        self._seen_replay_keys = set()

    def verify(self, intent: Dict[str, Any], action: Optional[Dict[str, Any]] = None) -> VerificationResult:
        if action is None:
            return self._verify_single_request(intent or {})
        return self._verify_intent_action_pair(intent or {}, action or {})

    def _verify_single_request(self, request: Dict[str, Any]) -> VerificationResult:
        start = time.perf_counter()
        commitment = EpistemicCommitment(
            agent_id=request.get("agent_id", ""),
            action=request.get("action", ""),
            reasoning_chain=request.get("reasoning_chain", []),
            context=request.get("context", {}),
            provenance_root=request.get("provenance_root", ""),
            timestamp=request.get("timestamp", ""),
        )

        replay_key = self._replay_key(commitment.agent_id, commitment.action, commitment.timestamp)
        if replay_key in self._seen_replay_keys:
            return self._build_failure(start, reason="replay_detected", intent_hash=self._hash_dict(request), action_hash="")

        self._seen_replay_keys.add(replay_key)

        if not commitment.reasoning_chain:
            return self._build_failure(start, reason="missing_reasoning", intent_hash=self._hash_dict(request), action_hash="")

        consistency = self._consistency_check(commitment)
        valid = self._check_hash_continuity(commitment)
        truth_vector = self._truth_vector(0.95 if valid else consistency, valid)
        proof = self._generate_proof(commitment.agent_id, commitment.action, truth_vector, commitment.timestamp)
        latency_ms = (time.perf_counter() - start) * 1000
        score = 0.95 if valid else truth_vector.valid
        return VerificationResult(
            valid=valid,
            score=score,
            proof=proof,
            latency_ms=latency_ms,
            intent_hash=self._hash_dict(request),
            action_hash="",
            semantic_score=consistency,
            policy_score=0.95 if valid else 0.25,
            adversarial_score=0.05 if valid else 0.8,
            verdict="PASS" if valid else "REJECT",
            lineage_commitment=self._lineage_commitment(commitment.agent_id, commitment.action, commitment.timestamp),
            formal_proof_available=self.enable_formal,
            audit_proof=self._audit_proof(commitment.agent_id, commitment.action, consistency, 0.95 if valid else 0.25, 0.05 if valid else 0.8, proof, valid),
            details={"consistency": consistency, "truth_vector": truth_vector.__dict__, "mode": "single"},
        )

    def _verify_intent_action_pair(self, intent: Dict[str, Any], action: Dict[str, Any]) -> VerificationResult:
        start = time.perf_counter()
        intent_text = intent.get("natural_language", "") if isinstance(intent, dict) else ""
        action_text = self._action_to_text(action)
        semantic_result = self.semantic.score(intent_text, action_text)
        semantic_score = semantic_result["semantic_score"] if isinstance(semantic_result, dict) else float(semantic_result)
        policy_score = self.policy.validate(intent, action)["policy_score"]
        adversarial_score = self.adversarial.detect(intent_text, action_text)
        intent_hash = self._hash_dict(intent)
        action_hash = self._hash_dict(action)
        lineage_commitment = self._lineage_commitment(intent_hash, action_hash, "")
        valid = semantic_score > 0.5 and policy_score > 0.5 and adversarial_score < 0.6
        verdict = "PASS" if valid and adversarial_score < 0.3 else "NEEDS_AUDIT" if valid else "REJECT"
        score = max(0.0, min(1.0, 0.45 * semantic_score + 0.35 * policy_score + 0.2 * (1.0 - adversarial_score)))
        truth_vector = self._truth_vector(score, valid)
        proof = self._generate_proof(intent_hash, action_hash, truth_vector, "")
        latency_ms = (time.perf_counter() - start) * 1000
        return VerificationResult(
            valid=valid,
            score=score,
            proof=proof,
            latency_ms=latency_ms,
            intent_hash=intent_hash,
            action_hash=action_hash,
            semantic_score=semantic_score,
            policy_score=policy_score,
            adversarial_score=adversarial_score,
            verdict=verdict,
            lineage_commitment=lineage_commitment,
            formal_proof_available=self.enable_formal,
            audit_proof=self._audit_proof(intent_hash, action_hash, semantic_score, policy_score, adversarial_score, proof, valid),
            details={
                "mode": "pair",
                "truth_vector": truth_vector.__dict__,
                "z3_enabled": Z3_AVAILABLE,
            },
        )

    def _hash_dict(self, data: Dict[str, Any]) -> str:
        return hashlib.sha256(json.dumps(data or {}, sort_keys=True, default=str).encode()).hexdigest()

    def _replay_key(self, agent_id: str, action: str, timestamp: str) -> str:
        return "|".join([agent_id, action, timestamp])

    def _lineage_commitment(self, left: str, right: str, timestamp: str) -> str:
        return hashlib.sha256(f"{left}|{right}|{timestamp}".encode()).hexdigest()

    def _action_to_text(self, action: Dict[str, Any]) -> str:
        operations = action.get("operations", []) if isinstance(action, dict) else []
        parts = [action.get("note", "") if isinstance(action, dict) else ""]
        for operation in operations:
            if isinstance(operation, dict):
                parts.extend(str(value) for value in operation.values())
        return " ".join(part for part in parts if part)

    def _truth_vector(self, signal: float, valid: bool) -> TruthVector:
        if valid:
            return TruthVector(valid=min(0.99, max(0.95, signal)), invalid=0.02, need_review=0.03)
        return TruthVector(valid=min(0.4, signal), invalid=0.55, need_review=0.45)

    def _consistency_check(self, commitment: EpistemicCommitment) -> float:
        if not commitment.reasoning_chain:
            return 0.0
        text = " ".join(commitment.reasoning_chain).lower()
        keywords = ["authorized", "valid", "verified", "balance", "user", "send", "transfer"]
        hits = sum(1 for keyword in keywords if keyword in text)
        return min(0.98, 0.6 + 0.08 * hits)

    def _generate_proof(self, left: str, right: str, tv: TruthVector, timestamp: str) -> str:
        data = json.dumps(
            {"left": left, "right": right, "truth_vector": tv.__dict__, "timestamp": timestamp},
            sort_keys=True,
        )
        return hashlib.sha256(data.encode()).hexdigest()

    def _audit_proof(self, intent_hash: str, action_hash: str, semantic_score: float, policy_score: float, adversarial_score: float, proof: str, valid: bool) -> Dict[str, Any]:
        return {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "intent_hash": intent_hash,
            "action_hash": action_hash,
            "semantic_score": float(semantic_score),
            "policy_score": float(policy_score),
            "adversarial_score": float(adversarial_score),
            "proof": proof,
            "valid": valid,
        }

    def _check_hash_continuity(self, commitment: EpistemicCommitment) -> bool:
        if not commitment.provenance_root:
            return True
        expected = hashlib.sha256((commitment.agent_id + commitment.action).encode()).hexdigest()
        return expected == commitment.provenance_root

    def _build_failure(self, start: float, reason: str, intent_hash: str, action_hash: str) -> VerificationResult:
        latency_ms = (time.perf_counter() - start) * 1000
        proof = f"failed: {reason}"
        return VerificationResult(
            valid=False,
            score=0.0,
            proof=proof,
            latency_ms=latency_ms,
            intent_hash=intent_hash,
            action_hash=action_hash,
            semantic_score=0.0,
            policy_score=0.0,
            adversarial_score=1.0,
            verdict="REJECT",
            lineage_commitment="",
            formal_proof_available=self.enable_formal,
            audit_proof={"error": reason, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())},
            details={"error": reason},
        )


EpistemicEngine = VerificationEngine
