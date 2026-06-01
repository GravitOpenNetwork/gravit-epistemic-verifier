# MiCAR Compliance Matrix

How Gravit Epistemic Verifier supports AllUnity's MiCAR obligations.

| Article | Requirement | How Gravit Fulfills |
|---------|-------------|---------------------|
| **Art. 51** | Whitepaper with risks, redemption rights, environmental impact | `docs/THREAT_MODEL.md` + `benchmarks/` (energy estimation) |
| **Art. 49** | Redemption right at par value anytime | Verified before mint/redeem flow (see `settlement_flow.md`) |
| **Art. 63** | Risk management framework | Epistemic scoring + adversarial tests |
| **Art. 45** | Audit trail for all transactions | `specification/agentic_audit_trail.schema.json` |
| **Art. 76** | Complaints handling | Human-in-the-loop for `need_review` outcomes |

## For BaFin Reviewers

This matrix maps each article to concrete implementation files in this repository.
