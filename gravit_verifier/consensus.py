"""
GRTVP (Gravit Real-Time Verification Protocol) consensus.
"""

import numpy as np
from scipy.special import softmax


def cross_entropy(p: np.ndarray, q: np.ndarray) -> float:
    """Compute cross-entropy between two distributions."""
    return -np.sum(p * np.log(q + 1e-12))


def grtvp_consensus(hypotheses: list, stakes: list, reputations: list) -> dict:
    """Compute final truth vector from validator votes."""
    n = len(hypotheses)
    weights = [0.4 * stake + 0.6 * rep for stake, rep in zip(stakes, reputations)]

    # Cross-entropy outlier detection
    scores = []
    for i in range(n):
        ce_sum = 0
        for j in range(n):
            if i != j:
                ce_sum += cross_entropy(hypotheses[i], hypotheses[j])
        scores.append(ce_sum / (n - 1))

    threshold = np.mean(scores) + 2 * np.std(scores)
    outliers = [i for i, s in enumerate(scores) if s > threshold]

    for i in outliers:
        weights[i] *= 0.5

    weighted_h = np.average(hypotheses, axis=0, weights=weights)
    return {
        "truth_vector": softmax(weighted_h).tolist(),
        "outliers": outliers,
        "consensus_reached": len(outliers) < n / 2
    }
