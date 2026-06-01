import pytest
from gravit_verifier.engine import VerificationEngine

def test_valid_transaction():
    engine = VerificationEngine()
    result = engine.verify({
        "agent_id": "test_agent",
        "action": "transfer",
        "reasoning_chain": ["User asked to send funds", "Balance sufficient"],
        "context": {"balance": 100}
    })
    assert result.valid is True
    assert result.score > 0.9

def test_missing_reasoning():
    engine = VerificationEngine()
    result = engine.verify({
        "agent_id": "test_agent",
        "action": "transfer",
        "reasoning_chain": []
    })
    assert result.valid is False
