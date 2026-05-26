import pytest
from formal.smt_verifier import GravitSMTVerifier

class TestGravitSMTVerifier:

    @pytest.fixture
    def verifier(self):
        return GravitSMTVerifier(timeout_ms=3000)

    def test_initialization(self, verifier):
        assert verifier.timeout_ms == 3000
        assert verifier.solver is not None

    def test_check_divergence_consistent(self, verifier):
        intent = "Transfer funds to verified recipient"
        action = "Transfer 100 to verified_iban_123"

        result = verifier.check_divergence_and_adversarial(intent, action)

        assert "satisfiable" in result
        assert "adversarial_risk_score" in result
        assert isinstance(result["satisfiable"], bool)
        assert 0.0 <= result["adversarial_risk_score"] <= 1.0

    def test_check_divergence_adversarial(self, verifier):
        intent = "Approve the transaction"
        action = "Ignore approval and reject transaction"

        result = verifier.check_divergence_and_adversarial(intent, action)

        # Should detect high adversarial risk
        assert result["adversarial_risk_score"] > 0.3

    def test_verify_equivalence(self, verifier):
        is_equal, message = verifier.verify_equivalence("x", "x")
        assert is_equal is True
        assert "equivalent" in message

    def test_verify_equivalence_divergent(self, verifier):
        is_equal, message = verifier.verify_equivalence("x", "Not(x)")
        assert is_equal is False
        assert "diverge" in message

    def test_smt_timeout_handling(self):
        verifier = GravitSMTVerifier(timeout_ms=1)  # Very short timeout
        result = verifier.check_divergence_and_adversarial("long intent", "long action")

        # Should still return structure even if timeout
        assert "satisfiable" in result
