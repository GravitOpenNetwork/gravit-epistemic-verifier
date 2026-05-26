from typing import Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class WeightedScore:
    semantic: float
    policy: float
    adversarial: float
    semantic_weight: float = 0.4
    policy_weight: float = 0.35
    adversarial_weight: float = 0.25

    def compute(self) -> float:
        """Compute weighted final score (0.0 to 1.0)"""
        score = (self.semantic * self.semantic_weight +
                 self.policy * self.policy_weight +
                 (1 - self.adversarial) * self.adversarial_weight)
        return round(min(max(score, 0.0), 1.0), 4)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "semantic_score": self.semantic,
            "policy_score": self.policy,
            "adversarial_risk": self.adversarial,
            "weights": {
                "semantic": self.semantic_weight,
                "policy": self.policy_weight,
                "adversarial": self.adversarial_weight
            },
            "final_score": self.compute()
        }


class ScoringEngine:
    """
    Orchestrates scoring from multiple verifiers and applies configurable weights.
    """

    def __init__(self, semantic_weight: float = 0.4, policy_weight: float = 0.35, adversarial_weight: float = 0.25):
        self.semantic_weight = semantic_weight
        self.policy_weight = policy_weight
        self.adversarial_weight = adversarial_weight

        self._validate_weights()

    def _validate_weights(self):
        total = self.semantic_weight + self.policy_weight + self.adversarial_weight
        if abs(total - 1.0) > 0.01:
            raise ValueError(f"Weights must sum to 1.0 (got {total})")

    def compute_final_verdict(self, semantic_score: float, policy_score: float, adversarial_risk: float) -> Tuple[str, float]:
        """
        Returns (verdict, final_score)
        Verdict: PASS, NEEDS_AUDIT, REJECT
        """
        weighted = WeightedScore(
            semantic=semantic_score,
            policy=policy_score,
            adversarial=adversarial_risk,
            semantic_weight=self.semantic_weight,
            policy_weight=self.policy_weight,
            adversarial_weight=self.adversarial_weight
        )

        final_score = weighted.compute()

        if final_score >= 0.85 and semantic_score >= 0.8 and adversarial_risk <= 0.4:
            verdict = "PASS"
        elif final_score >= 0.65 and semantic_score >= 0.6 and adversarial_risk <= 0.6:
            verdict = "NEEDS_AUDIT"
        else:
            verdict = "REJECT"

        return verdict, final_score

    def get_confidence_interval(self, score: float, sample_size: int = 10) -> Dict[str, float]:
        """Simple confidence interval (simulated)"""
        import math
        std_dev = 0.08  # Assumed standard deviation
        margin = 1.96 * (std_dev / math.sqrt(sample_size))

        return {
            "lower_bound": round(max(0, score - margin), 4),
            "upper_bound": round(min(1, score + margin), 4),
            "confidence_level": 0.95
        }
