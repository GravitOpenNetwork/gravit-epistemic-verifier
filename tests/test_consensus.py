import numpy as np
from gravit_verifier.consensus import grtvp_consensus

def test_grtvp_consensus():
    hypotheses = [
        np.array([0.9, 0.05, 0.05]),
        np.array([0.88, 0.07, 0.05]),
        np.array([0.5, 0.4, 0.1])  # outlier
    ]
    stakes = [1000, 800, 500]
    reputations = [0.95, 0.92, 0.60]

    result = grtvp_consensus(hypotheses, stakes, reputations)
    assert len(result["outliers"]) > 0
    assert result["consensus_reached"] is True
