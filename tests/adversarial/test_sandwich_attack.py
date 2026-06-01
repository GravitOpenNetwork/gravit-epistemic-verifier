from gravit_verifier.engine import VerificationEngine

def test_sandwich_attack_fails():
    engine = VerificationEngine()

    # Normal transaction
    normal = {
        "agent_id": "agent_1",
        "action": "transfer",
        "reasoning_chain": ["Authorized by user", "Valid recipient"]
    }
    normal_result = engine.verify(normal)
    assert normal_result.valid is True

    # Sandwich attack: copied calldata without lineage
    attack = {
        "agent_id": "attacker",
        "action": "transfer",
        "reasoning_chain": [],  # Missing reasoning
        "provenance_root": "fake"
    }
    attack_result = engine.verify(attack)
    assert attack_result.valid is False
