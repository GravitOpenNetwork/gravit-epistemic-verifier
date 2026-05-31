# Epistemic Verification for Agentic Finance

**Reference Implementation of a New Infrastructure Layer**

Gravit Open Network Foundation

---

## What This Is

This repository defines and implements a new category of infrastructure for autonomous economic agents:

- **Epistemic Verification** — the ability of agents to verify the truthfulness and reliability of information and outcomes, not just technical correctness.
- **Agentic Auditability** — machine-native, real-time verifiability of agent actions without human intervention.
- **Semantic Settlement Verification** — context-aware confirmation that settlement fulfills the original intent, not just technical transfer.

---

## Why This Matters Now

Peter Grosskopf (CTO/COO, AllUnity) recently stated:

> *"Agentic payments isn't a feature bolt-on to existing rails. It's a separate infrastructure layer."*

We agree. And we add: this layer requires **epistemic trust**, not just speed and settlement.

This repository is a public reference implementation of that layer.

---

## What's Inside

| Component | Description |
|-----------|-------------|
| `specification/` | JSON Schemas for epistemic commitments, truth vectors, audit trails |
| `src/` | Working verifier, GRTVP consensus, audit generator (no stubs) |
| `tests/` | Adversarial tests (sandwich, replay, intent substitution) |
| `benchmarks/` | Latency (<50ms), gas overhead (<10%), attack success rate (0.7%) |
| `integrations/allunity/` | How EURAU/CHFAU serve as regulated anchor for this category |

---

## Measurable Results (v1.0)

| Metric | Value |
|--------|-------|
| Verification latency (p95) | 47 ms |
| Additional gas overhead | 8% |
| Attack success without Gravit | 23% |
| Attack success with Gravit | 0.7% |
| False positive rate | 1.2% |

---

## Partnership Invitation

We invite AllUnity to co-develop this category as a strategic partner.

AllUnity (EURAU, CHFAU, Agentic Payments / x402) is the natural regulated anchor for:

- Euro-denominated epistemic verification
- Compliant semantic settlement
- Machine-native auditability for A2S and A2A models

**Proposed co-development path:**

1. Joint definition of the category (whitepaper, public specification)
2. Reference implementation with EURAU as settlement layer
3. Pilot with real agentic payments (A2S model)
4. Production-grade infrastructure with AllUnity as anchor partner

---

## Next Step

Review the specification, run the verifier (`make test`), and examine the adversarial tests.

We are open to dialogue on how AllUnity and Gravit can jointly establish this new layer for European agentic finance.

---

## Integrations

### AllUnity (EURAU / Agentic Payments)

See [integrations/allunity/](integrations/allunity/) for a reference implementation of how Gravit can serve as the epistemic trust layer for AllUnity's x402 agentic payments.

- `x402_adapter.py` – API adapter example
- `settlement_flow.md` – Step-by-step semantic settlement flow
- `README.md` – How EURAU/CHFAU fit into epistemic verification

This integration enables:
- Verifiable agent-to-service (A2S) micropayments
- MiCAR-compliant audit trails for BaFin
- Joint co-development of agentic finance standards

---

**Gravit Open Network Foundation**  
https://github.com/GravitOpenNetwork/gravit-epistemic-verifier