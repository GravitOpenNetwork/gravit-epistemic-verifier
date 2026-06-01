"""
Data models for epistemic verification.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class EpistemicCommitment:
    agent_id: str
    action: str
    reasoning_chain: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    provenance_root: str = ""
    timestamp: str = ""


@dataclass
class TruthVector:
    valid: float = 0.0
    invalid: float = 0.0
    need_review: float = 0.0


@dataclass
class VerificationResult:
    valid: bool
    score: float
    proof: str
    latency_ms: float
    intent_hash: str = ""
    action_hash: str = ""
    semantic_score: float = 0.0
    policy_score: float = 0.0
    adversarial_score: float = 0.0
    verdict: str = "NEEDS_AUDIT"
    lineage_commitment: str = ""
    formal_proof_available: bool = False
    audit_proof: Dict[str, Any] = field(default_factory=dict)
    details: Dict[str, Any] = field(default_factory=dict)


ValidationResult = VerificationResult
