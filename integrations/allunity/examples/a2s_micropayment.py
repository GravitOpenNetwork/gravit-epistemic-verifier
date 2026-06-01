"""
A2S (Agent-to-Service) Micropayment Example
"""

from gravit_verifier.engine import VerificationEngine

def a2s_micropayment():
    reasoning = [
        "User requested to fetch weather data for Berlin",
        "API provider 'weather_api' charges 0.5 EURAU per call",
        "User has sufficient balance (10 EURAU available)"
    ]

    payment_intent = {
        "agent_id": "weather_bot_01",
        "action": "api_call",
        "reasoning_chain": reasoning,
        "context": {"user_id": "user_123", "balance": 10.0}
    }

    engine = VerificationEngine()
    result = engine.verify(payment_intent)

    if result.valid:
        print(f"✅ Payment verified (score: {result.score})")
        print(f"   Trace ID: {result.proof[:16]}...")
    else:
        print(f"❌ Verification failed")

if __name__ == "__main__":
    a2s_micropayment()
