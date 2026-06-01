"""
Data models for epistemic verification.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


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
class ValidationResult:
    valid: bool
    score: float
    proof: str
    latency_ms: float
    details: Dict[str, Any] = field(default_factory=dict)
