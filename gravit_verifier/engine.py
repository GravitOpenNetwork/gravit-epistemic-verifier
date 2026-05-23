import uuid
import hashlib
from datetime import datetime
from .semantic import SemanticVerifier
from .policy.validator import PolicyValidator
from .adversarial.detector import AdversarialDetector
from .ees.metadata import EESMetadata
from proofs.commitment import build_proof


class EpistemicEngine:
    def init(self):
        self.semantic = SemanticVerifier()
        self.policy = PolicyValidator()
        self.adversarial = AdversarialDetector()

    def verify(
        self,
        intent: str,
        action: str,
        model_id: str = "unknown",
        prompt: str = None,
        intermediate_steps: list = None,
    ):
        verification_id = str(uuid.uuid4())
        timestamp = int(datetime.utcnow().timestamp())
        ees = EESMetadata(
            verification_id=verification_id,
            timestamp=timestamp,
            model_id=model_id,
            prompt_hash=hashlib.sha256((prompt or intent).encode()).hexdigest(),
            intermediate_steps=intermediate_steps or [],
            conditions={"temperature": 0.0},
        )
        semantic_result = self.semantic.score(intent, action)
        policy_ok = self.policy.validate(intent, action)
        adversarial_score = self.adversarial.detect(intent, action)
        epistemic_trust_score = (
            semantic_result["semantic_score"] * 0.45
            + (1.0 if policy_ok else 0.0) * 0.35
            + (1.0 - adversarial_score) * 0.20
        )
        verdict = "ACCEPT"
        if (
            epistemic_trust_score < 0.90
            or semantic_result["semantic_score"] < 0.85
            or adversarial_score > 0.25
            or not policy_ok
        ):
            verdict = "REJECT"
        elif epistemic_trust_score < 0.95:
            verdict = "REVIEW"

        proof = build_proof(intent, action, ees, verdict)
        return {
            "verification_id": verification_id,
            "timestamp": datetime.utcfromtimestamp(timestamp).isoformat(),
            "intent_hash": hashlib.sha256(intent.encode()).hexdigest(),
            "ees_metadata_commitment": ees.commitment(),
            "semantic_score": semantic_result["semantic_score"],
            "policy_score": 1.0 if policy_ok else 0.0,
            "adversarial_score": adversarial_score,
            "epistemic_trust_score": round(epistemic_trust_score, 4),
            "verdict": verdict,
            "proof_signature": proof["signature"],
        }
