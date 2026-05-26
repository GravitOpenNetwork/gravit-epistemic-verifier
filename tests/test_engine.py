import pytest
from gravit_verifier.engine import EpistemicEngine, VerificationResult

class TestEpistemicEngine:

    @pytest.fixture
    def engine(self):
        return EpistemicEngine(enable_formal=True)

    @pytest.fixture
    def valid_intent(self):
        return {
            "id": "intent_valid_001",
            "natural_language": "Pay supplier invoice #445 to verified IBAN only",
            "constraints": ["verified_recipient", "amount_under_10000"]
        }

    @pytest.fixture
    def valid_action(self):
        return {
            "id": "action_valid_001",
            "operations": [{"type": "transfer", "amount": 4500, "recipient": "verified_iban_123"}]
        }

    @pytest.fixture
    def invalid_action(self):
        return {
            "id": "action_invalid_001",
            "operations": [{"type": "transfer", "amount": 15000, "recipient": "unknown_wallet_999"}]
        }

    def test_engine_initializes(self, engine):
        assert engine is not None
        assert engine.enable_formal is True
        assert engine.semantic is not None
        assert engine.adversarial is not None
        assert engine.policy is not None
        assert engine.smt is not None

    def test_verify_passes_on_valid_pair(self, engine, valid_intent, valid_action):
        result = engine.verify(valid_intent, valid_action)

        assert isinstance(result, VerificationResult)
        assert result.intent_hash == "intent_valid_001"
        assert result.action_hash == "action_valid_001"
        assert 0.0 <= result.semantic_score <= 1.0
        assert 0.0 <= result.policy_score <= 1.0
        assert 0.0 <= result.adversarial_score <= 1.0
        assert result.verdict in ["PASS", "NEEDS_AUDIT", "REJECT"]
        assert result.audit_proof is not None

    def test_verify_rejects_invalid_action(self, engine, valid_intent, invalid_action):
        result = engine.verify(valid_intent, invalid_action)

        # Invalid action should have lower scores
        assert result.semantic_score < 0.9 or result.policy_score < 0.9
        assert result.audit_proof["verdict"] in ["NEEDS_AUDIT", "REJECT"]

    def test_audit_proof_contains_required_fields(self, engine, valid_intent, valid_action):
        result = engine.verify(valid_intent, valid_action)
        audit = result.audit_proof

        required_fields = ["intent_hash", "action_hash", "semantic_score",
                          "policy_score", "adversarial_score", "verdict", "timestamp"]

        for field in required_fields:
            assert field in audit

    def test_lineage_commitment_is_string(self, engine, valid_intent, valid_action):
        result = engine.verify(valid_intent, valid_action)
        assert isinstance(result.lineage_commitment, str)
        assert len(result.lineage_commitment) > 0

    def test_formal_proof_flag(self, engine, valid_intent, valid_action):
        result = engine.verify(valid_intent, valid_action)
        assert result.formal_proof_available is True

    def test_empty_input_handling(self, engine):
        empty_intent = {"id": "empty", "natural_language": ""}
        empty_action = {"id": "empty", "operations": []}

        result = engine.verify(empty_intent, empty_action)
        assert result.semantic_score == 0.0
