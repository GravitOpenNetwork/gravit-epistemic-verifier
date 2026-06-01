# Semantic Settlement Flow with Gravit + AllUnity

## Step-by-Step Flow

1. **Intent**
   AI agent generates payment intent: *"Pay 10 EURAU to provider_xyz for 100 GPU-seconds"*

2. **Epistemic Commitment**
   Agent attaches reasoning chain: user authorization, provider reputation, task completion

3. **Gravit Verification**
   - Semantic consistency
   - Policy compliance
   - Adversarial risk
   - Output: `passed, score: 0.96, trace_id: tx_123`

4. **x402 Payment Request**
   Agent sends x402 request with payment amount + Gravit `trace_id`

5. **Settlement**
   AllUnity executes EURAU transfer (Solana/CCIP)

6. **Audit Trail**
   Gravit stores proof, AllUnity stores settlement proof, linked via `trace_id`

## Benefits

- **AllUnity**: Verifiable agentic payments without building trust layer
- **Gravit**: Regulated settlement without becoming an EMI
- **Regulator**: Complete, machine-verifiable audit trail
