from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class VerificationRequest(BaseModel):
    intent: str
    action: str
    model_id: str = "unknown"
    prompt: Optional[str] = None
    intermediate_steps: Optional[List[Dict[str, Any]]] = None


class VerificationResponse(BaseModel):
    verification_id: str
    timestamp: str
    intent_hash: str
    ees_metadata_commitment: str
    semantic_score: float
    policy_score: float
    adversarial_score: float
    epistemic_trust_score: float
    verdict: str
    proof_signature: str
    verifier_version: str = "1.0.0"
