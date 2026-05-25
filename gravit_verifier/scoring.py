from dataclasses import dataclass
from typing import Dict


@dataclass
class WeightedScore:
    name: str
    weight: float


class ScoringEngine:
    """Minimal scoring engine used by tests. Combines named scores with weights.

    This is intentionally lightweight — tests only import the symbol from the
    package, so we provide a simple implementation.
    """

    def __init__(self, weights: Dict[str, float] = None):
        self.weights = weights or {"semantic": 0.45, "policy": 0.35, "adversarial": 0.2}

    def compute(self, scores: Dict[str, float]) -> float:
        total = 0.0
        for k, w in self.weights.items():
            val = scores.get(k, 0.0)
            total += w * val
        return total
