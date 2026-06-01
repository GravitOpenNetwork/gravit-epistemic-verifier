"""
GRTVP (Gravit Real-Time Verification Protocol) consensus.
"""

import numpy as np


def softmax(values: np.ndarray) -> np.ndarray:
    shifted = values - np.max(values)
    exp_values = np.exp(shifted)
    return exp_values / np.sum(exp_values)


def cross_entropy(p: np.ndarray, q: np.ndarray) -> float:
    """Compute cross-entropy between two distributions."""
    return -np.sum(p * np.log(q + 1e-12))


def grtvp_consensus(hypotheses: list, stakes: list, reputations: list) -> dict:
    """Compute final truth vector from validator votes."""
    n = len(hypotheses)
    weights = [0.4 * stake + 0.6 * rep for stake, rep in zip(stakes, reputations)]

    baseline = np.mean(hypotheses, axis=0)
    scores = [float(np.linalg.norm(hypothesis - baseline, ord=1)) for hypothesis in hypotheses]
    threshold = np.mean(scores) + np.std(scores)
    outliers = [i for i, s in enumerate(scores) if s > threshold]

    for i in outliers:
        weights[i] *= 0.5

    weighted_h = np.average(hypotheses, axis=0, weights=weights)
    return {
        "truth_vector": softmax(weighted_h).tolist(),
        "outliers": outliers,
        "consensus_reached": len(outliers) < n / 2
    }
