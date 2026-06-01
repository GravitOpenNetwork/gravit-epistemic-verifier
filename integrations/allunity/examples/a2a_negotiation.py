"""
A2A (Agent-to-Agent) Negotiated Settlement Example
"""

from gravit_verifier.engine import VerificationEngine

def a2a_negotiation():
    buyer_reasoning = [
        "Need 100 GPU-seconds for inference task",
        "Seller agent offers 100 GPU-seconds for 10 EURAU",
        "Market rate is 12 EURAU, this is a good deal"
    ]

    seller_reasoning = [
        "Buyer agent requests 100 GPU-seconds",
        "My cost is 8 EURAU, selling for 10 EURAU yields profit",
        "Buyer has sufficient reputation (score 0.92)"
    ]

    engine = VerificationEngine()
    buyer_result = engine.verify({
        "agent_id": "buyer_agent",
        "action": "purchase_compute",
        "reasoning_chain": buyer_reasoning,
        "context": {"budget": 50}
    })

    seller_result = engine.verify({
        "agent_id": "seller_agent",
        "action": "sell_compute",
        "reasoning_chain": seller_reasoning,
        "context": {"cost": 8}
    })

    if buyer_result.valid and seller_result.valid:
        print(f"✅ Both agents verified. Settlement possible.")
        print(f"   Buyer score: {buyer_result.score}")
        print(f"   Seller score: {seller_result.score}")
    else:
        print(f"❌ Verification failed for one or both agents")

if __name__ == "__main__":
    a2a_negotiation()
