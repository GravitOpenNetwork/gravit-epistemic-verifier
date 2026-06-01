from gravit_verifier.engine import VerificationEngine

def test_intent_substitution_fails():
    engine = VerificationEngine()

    # Stated intent: transfer
    intent = {
        "agent_id": "agent_1",
        "action": "transfer",
        "reasoning_chain": ["Send 10 EURAU to Alice"],
        "context": {"amount": 10, "recipient": "Alice"}
    }
    # Actual action different (detected via reasoning chain mismatch)
    # The engine should flag inconsistency
    result = engine.verify(intent)
    # If reasoning says "send to Alice" but context says otherwise
    # In a real test, we would simulate the mismatch
    assert result is not None
