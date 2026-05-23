# Verification Pipeline — Gravit Epistemic Verifier

## Overview

The verification pipeline is a **pre-execution gate** that runs in under 800ms for typical financial actions.

## Stages

1. **Intent Ingestion**
   - Receive structured Intent + context
   - Generate `intent_hash`

2. **EES Metadata Collection**
   - Capture origin, prompt, model info, conditions
   - Build Reasoning Lineage
   - Compute recursive commitments

3. **Parallel Verification Modules**
   - Semantic Verifier
   - Policy Engine
   - Adversarial Detector
   - Lineage Validator

4. **Scoring & Decision**
   - Compute Epistemic Trust Score
   - Apply thresholds → Verdict

5. **Proof Generation**
   - Create cryptographic proof
   - Package output schema
   - Optional: publish commitment on-chain / Gravit Continuum

## Performance Targets

- p95 latency: < 800ms
- Throughput: > 200 verifications/sec (single instance)
- Deterministic & Reproducible

## Failure Modes

- Any module failure → default to `REJECT`
- Timeout → `REVIEW`
