# Contributing to Gravit Epistemic Verifier

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Code of Conduct

By participating, you agree to maintain a respectful and constructive environment.

## How to Contribute

### Reporting Bugs

Open an issue with:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)

### Suggesting Enhancements

Open an issue with:
- Clear use case
- Proposed solution
- Alternatives considered

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Write tests for your changes
4. Ensure all tests pass (`pytest tests/ -v`)
5. Run linter (`ruff check gravit_verifier/`)
6. Run formatter (`black gravit_verifier/ --line-length 88`)
7. Commit with clear message (Conventional Commits preferred)
8. Push and open a Pull Request to `main` branch

## Development Setup

```bash
git clone https://github.com/GravitOpenNetwork/gravit-epistemic-verifier.git
cd gravit-epistemic-verifier
pip install -e "[dev]"
pytest tests/ -v
```

## Coding Standards

- Language: All code (comments, strings, variables) in English only
- Style: Black (line-length 88)
- Linting: Ruff
- Types: MyPy (optional but recommended)
- Tests: Pytest with coverage > 80%

## Commit Message Format

Use Conventional Commits:

```text
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`

Example:

```text
feat(verifier): add semantic divergence threshold

Add configurable threshold for semantic similarity checks.
Closes #42
```

## Release Process

Maintainers only:

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create PR with `release/vX.Y.Z` branch
4. After merge, create GitHub Release with tag `vX.Y.Z`

## Questions?

Open an issue or contact maintainers at `info@gravit.network`

Thank you for contributing!
