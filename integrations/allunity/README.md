# Gravit + AllUnity Integration Reference

## Alignment with Agentic Payments (x402)

Gravit's epistemic verification is a natural complement to AllUnity's x402 payment standard:

1. **Agent initiates payment** → attaches epistemic commitment (intent, provenance, reasoning chain)
2. **Gravit verifies** semantic validity (continuity, compliance, adversarial risk)
3. **AllUnity settles** in EURAU/CHFAU via x402
4. **Audit proof generated** for MiCAR compliance (BaFin)

## How EURAU Fits

EURAU serves as the regulated settlement layer for verified agentic payments:

- Gravit provides the **trust proof** (epistemic commitment + audit trail)
- AllUnity provides the **compliant money rail** (MiCAR, 1:1 backed, redeemable)

## Three Agentic Models

| Model | Gravit Role | AllUnity Role |
|-------|-------------|---------------|
| **A2S (Agent-to-Service)** | Verify payment intent for API/data calls | Settle micropayments in EURAU |
| **A2M (Agent-to-Merchant)** | Verify delegated mandate & consumer protection | Settle with compliance proofs |
| **A2A (Agent-to-Agent)** | Epistemic consensus between agents | Regulated settlement layer |

## Next Steps for Co-Development

1. Define semantic settlement verification API (see `specification/`)
2. Implement reference adapter (`x402_adapter.py`)
3. Pilot with A2S use case (AI agents paying for compute/inference)
4. Joint whitepaper: "Epistemic Verification for Agentic Finance"

## Reference

- [AllUnity Agentic Payments Announcement](https://allunity.com/news/allunity-announces-intent-to-launch-the-first-swedish-krona%E2%80%93backed-stablecoin-and-launches-agentic-payments)
- [Peter Grosskopf on Agentic Payments Models](https://www.linkedin.com/posts/petergrosskopf)
