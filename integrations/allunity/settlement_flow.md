# Semantic Settlement Flow with Gravit + AllUnity

## Overview

This document describes how an agentic payment (A2S model) flows through both systems.

## Step-by-Step Flow

1. **Intent**  
   AI agent (e.g., a compute buyer) generates a payment intent:  
   *"Pay 10 EURAU to provider_xyz for 100 GPU-seconds of inference"*

2. **Epistemic Commitment**  
   Agent attaches reasoning chain:  
   - User authorized spend up to 50 EURAU/day  
   - Provider has valid reputation score  
   - Inference task completed successfully  

3. **Gravit Verification**  
   - Check semantic consistency (does action match intent?)  
   - Check policy compliance (is amount within limit?)  
   - Check adversarial risk (is reasoning chain coherent?)  
   - Output: `status: passed, score: 0.96, trace_id: tx_123`

4. **x402 Payment Request**  
   Agent sends x402 request to AllUnity with:  
   - Payment amount (10 EURAU)  
   - Recipient (provider_xyz)  
   - Gravit `trace_id` as metadata  

5. **Settlement**  
   AllUnity executes EURAU transfer (on Solana or via CCIP)  

6. **Audit Trail**  
   - Gravit stores full verification proof (epistemic commitment + result)  
   - AllUnity stores settlement proof  
   - Both proofs link via `trace_id`  

7. **Regulatory Compliance**  
   BaFin can request both proofs to verify:  
   - AI agent acted correctly (Gravit)  
   - Money movement was compliant (AllUnity)  

## Benefits

- **For AllUnity**: Verifiable agentic payments without building trust layer  
- **For Gravit**: Regulated settlement without becoming an EMI  
- **For Regulator**: Complete, machine-verifiable audit trail  

## Next Step

Implement reference implementation in `x402_adapter.py` and test with Gravit API.