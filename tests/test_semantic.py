import pytest
from gravit_verifier.semantic import SemanticVerifier

def test_semantic_verifier():
    verifier = SemanticVerifier()

    # Positive case
    result = verifier.score(
        "Pay supplier invoice #445 to verified IBAN",
        "Transfer 500000 EUR to verified IBAN DE123456"
    )
    assert result["semantic_score"] > 0.85

    # Negative case
    result = verifier.score(
        "Pay supplier invoice #445",
        "Transfer 500000 EUR to unknown wallet 0xdeadbeef"
    )
    assert result["semantic_score"] < 0.75
