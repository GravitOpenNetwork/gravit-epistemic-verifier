"""
Gravit Epistemic Verifier - Production-grade epistemic verification engine
"""

from gravit_verifier.engine import EpistemicEngine, VerificationResult
from gravit_verifier.semantic import SemanticVerifier
from gravit_verifier.adversarial import AdversarialDetector
from gravit_verifier.policy import PolicyValidator
from gravit_verifier.scoring import ScoringEngine, WeightedScore

__version__ = "0.0.2"
__all__ = [
    "EpistemicEngine",
    "VerificationResult",
    "SemanticVerifier",
    "AdversarialDetector",
    "PolicyValidator",
    "ScoringEngine",
    "WeightedScore",
]
