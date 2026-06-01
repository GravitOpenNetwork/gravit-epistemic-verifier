# Threat Model for Epistemic Verification

## Attack Classes

### 1. Sandwich Attack
**Description:** Attacker copies calldata and places transactions before and after target.

**Mitigation:** Epistemic commitment includes model state hash. Copied calldata lacks valid provenance → semantically invalid.

### 2. Replay Attack
**Description:** Valid transaction is replayed in different context.

**Mitigation:** Nonce + timestamp + context hash in commitment.

### 3. Intent Substitution
**Description:** Agent's stated intent differs from actual action.

**Mitigation:** Reasoning chain must be cryptographically linked to execution.

### 4. Adversarial Delegation
**Description:** Malicious agent delegates to another with harmful intent.

**Mitigation:** Delegation scope must be explicitly declared and verified.

### 5. Hallucinated Execution
**Description:** Agent invents reasoning steps not grounded in user input.

**Mitigation:** Consistency check between reasoning chain and available context.

## Formal Guarantees

- Continuity: Hash chain from user intent to execution
- Provenance: 2/3 validator signatures required
- Auditability: Every decision leaves verifiable proof
