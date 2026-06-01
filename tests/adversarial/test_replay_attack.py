from gravit_verifier.engine import VerificationEngine

def test_replay_attack_fails():
    engine = VerificationEngine()
    timestamp1 = "2026-05-31T10:00:00Z"
    timestamp2 = "2026-05-31T10:01:00Z"

    original = {
        "agent_id": "agent_1",
        "action": "transfer",
        "reasoning_chain": ["Valid"],
        "timestamp": timestamp1
    }
    original_result = engine.verify(original)
    assert original_result.valid is True

    # Replay with same timestamp
    replay = {
        "agent_id": "agent_1",
        "action": "transfer",
        "reasoning_chain": ["Valid"],
        "timestamp": timestamp1
    }
    replay_result = engine.verify(replay)
    # Should fail due to duplicate detection
    assert replay_result.valid is False
