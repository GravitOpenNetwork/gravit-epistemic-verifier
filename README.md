# Gravit Epistemic Verifier

**Production-grade Epistemic Verification Engine for Autonomous Economic Agents**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](pyproject.toml)
[![Version](https://img.shields.io/badge/version-0.0.2-brightgreen)](https://github.com/GravitOpenNetwork/gravit-epistemic-verifier/releases)
[![CI/CD](https://github.com/GravitOpenNetwork/gravit-epistemic-verifier/actions/workflows/ci.yml/badge.svg)](https://github.com/GravitOpenNetwork/gravit-epistemic-verifier/actions)

## What is Epistemic Verification?

**Epistemic Verification** is an independent trust layer that verifies whether an autonomous AI agent's action is:

- Semantically consistent with its declared intent
- Compliant with defined policies
- Resilient to adversarial manipulation
- Supported by a reconstructible reasoning lineage

It serves as a **pre-settlement trust gate** for agentic finance and autonomous operations.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/GravitOpenNetwork/gravit-epistemic-verifier.git
cd gravit-epistemic-verifier

# Run with Docker Compose
docker compose up --build

# API will be available at:
# http://localhost:8080/docs
```

### API Usage Example

```bash
curl -X POST http://localhost:8080/v1/verify \
  -H "Content-Type: application/json" \
  -d '{
    "action": "transfer_funds",
    "agent_id": "agent_42",
    "reasoning_chain": [
      "User requested to send 100 GRAVIT to wallet 0xabc...",
      "Verified wallet belongs to known recipient Alice",
      "User has sufficient balance (550 GRAVIT available)"
    ],
    "context": {
      "user_id": "user_7",
      "balance": 550
    }
  }'
```

### Example Response (Passed)

```json
{
  "status": "passed",
  "score": 0.94,
  "checks": {
    "semantic_compliance": true,
    "policy_compliance": true,
    "adversarial_risk": false,
    "reasoning_lineage": "valid"
  },
  "decision": "allowed",
  "trace_id": "trace_xyz789"
}
```

## Features

- Hybrid verification: Heuristic + SMT (Z3)
- Verifiable `AuditProof` generation
- Semantic divergence measurement
- Adversarial pattern detection
- Prometheus metrics
- Kubernetes ready (Helm chart)

## Documentation

See the `docs/` folder for detailed specifications:

- `CATEGORY.md` – Epistemic Verification definition
- `FORMAL_METHODS.md` – Formal verification approach
- `THREAT_MODEL.md` – Security considerations

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run linter
ruff check gravit_verifier/

# Run formatter
black gravit_verifier/ --line-length 88
```

## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests.

## License

Apache 2.0 – see `LICENSE` file for details.

## Authors

Gravit Open Network – info@gravit.network

## Acknowledgments

- Z3 Prover (Microsoft Research)
- Lean 4 community
