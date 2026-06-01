"""
A2M (Agent-to-Merchant) Delegated Purchase Example
"""

from gravit_verifier.engine import VerificationEngine

def a2m_delegated_purchase():
    reasoning = [
        "User authorized purchase of 'Pro Plan' up to 50 EURAU/month",
        "Plan price: 29 EURAU",
        "User has valid payment method on file",
        "Delegation scope: only SaaS purchases under 50 EURAU"
    ]

    payment_intent = {
        "agent_id": "saas_buyer_02",
        "action": "purchase_license",
        "reasoning_chain": reasoning,
        "context": {
            "user_id": "corp_456",
            "delegation_scope": "saas_purchases",
            "monthly_limit": 50
        }
    }

    engine = VerificationEngine()
    result = engine.verify(payment_intent)

    if result.valid:
        print(f"✅ Purchase verified (score: {result.score})")
    else:
        print(f"❌ Verification failed")

if __name__ == "__main__":
    a2m_delegated_purchase()
