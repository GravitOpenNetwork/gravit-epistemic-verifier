# Threat Model — Epistemic Verification (Gravit)

**Version:** 1.0
**Last Updated:** 2026-05-21

## 1. Purpose

This document defines the adversarial model that Epistemic Verification is designed to defend against in autonomous financial systems.

## 2. Assets to Protect

- User/Agent Intent
- Reasoning Lineage (EES Metadata)
- Semantic Alignment between Intent and Action
- Policy Compliance Decisions
- Epistemic Trust Score
- Final Verdict and Proofs

## 3. Adversaries

| Adversary Type          | Capabilities                              | Motivation                     |
|-------------------------|-------------------------------------------|--------------------------------|
| Malicious Prompt Engineer | Prompt injection, jailbreaking           | Theft, unauthorized transfer   |
| Compromised Model       | Hidden objectives, trojaned weights      | Long-term fund drainage        |
| Rogue Agent             | Semantic drift, tool misuse              | Personal gain                  |
| Supply Chain Attacker   | Backdoors in dependencies                | Systemic compromise            |
| Regulatory Evasion Actor| Creative rephrasing, policy bypass       | Compliance circumvention       |

## 4. Core Threats & Mitigations

### 4.1 Prompt Injection & Hidden Intent
- **Threat**: Attacker embeds conflicting instructions.
- **Mitigation**: Strict Intent-Action semantic boundary + multi-angle verification + EES origin tracking.

### 4.2 Semantic Drift
- **Threat**: Reasoning diverges from original intent across steps.
- **Mitigation**: Full Reasoning Lineage with recursive commitments + intermediate semantic checks.

### 4.3 Hallucinated Execution
- **Threat**: Model invents actions not grounded in intent.
- **Mitigation**: High semantic_score threshold + adversarial_score.

### 4.4 Policy Bypass
- **Threat**: Creative language to avoid blacklist/policy triggers.
- **Mitigation**: Hybrid rule-based + embedding-based policy engine + human-in-the-loop for REVIEW verdicts.

### 4.5 Adversarial Delegation
- **Threat**: Agent delegates to untrusted sub-agents.
- **Mitigation**: Lineage must include all downstream calls with their own EES metadata.

### 4.6 Model Poisoning / Backdoors
- **Mitigation**: Use of verifiable models (ONNX + checksums), ensemble verification, reproducible environments.

## 5. Assumptions

- Underlying cryptographic primitives (ed25519, SHA-256) are secure.
- Intent is declared honestly by the user/owner.
- Verifier runs in a trusted execution environment or is itself verified.

## 6. Out of Scope

- Physical attacks on hardware
- Key compromise of the user
- Consensus layer attacks on the blockchain itself

---

**This threat model SHALL be maintained as a living document** and updated with each major version of the verifier.
