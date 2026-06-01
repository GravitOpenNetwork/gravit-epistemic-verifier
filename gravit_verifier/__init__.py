"""
Gravit Epistemic Verifier

Production-grade epistemic verification for AI agents.
"""

from .engine import EpistemicEngine, VerificationEngine, VerificationResult
from .models import EpistemicCommitment, TruthVector, ValidationResult

__version__ = "1.0.0"
__all__ = [
	"VerificationEngine",
	"EpistemicEngine",
	"VerificationResult",
	"EpistemicCommitment",
	"TruthVector",
	"ValidationResult",
]
