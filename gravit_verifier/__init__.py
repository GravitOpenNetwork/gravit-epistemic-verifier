"""
Gravit Epistemic Verifier

Production-grade epistemic verification for AI agents.
"""

from .engine import VerificationEngine
from .models import EpistemicCommitment, TruthVector, ValidationResult

__version__ = "1.0.0"
__all__ = ["VerificationEngine", "EpistemicCommitment", "TruthVector", "ValidationResult"]
