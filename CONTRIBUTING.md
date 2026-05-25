# Contributing to Gravit Epistemic Verifier

Thank you for your interest in contributing.

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
2. Create a feature branch
3. Write tests for your changes
4. Ensure all tests pass: `pytest tests/ -v`
5. Run linter: `ruff check gravit_verifier/`
6. Run formatter: `black gravit_verifier/ --line-length 88`
7. Commit with a clear message
8. Push and open a Pull Request to the `main` branch

## Development Setup

```bash
git clone https://github.com/GravitOpenNetwork/gravit-epistemic-verifier.git
cd gravit-epistemic-verifier
pip install -e "[dev]"
pytest tests/ -v
```

## Coding Standards

- Language: All code (comments, strings, variables) in English only
- Style: Black with line length 88
- Linting: Ruff
- Tests: Pytest with coverage > 80%

## Commit Message Format

Use Conventional Commits:

```text
type(scope): subject

Body

Footer
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

- Update version in `pyproject.toml`
- Update `CHANGELOG.md`
- Create a PR with branch name `release/vX.Y.Z`
- After merge, create a GitHub Release with tag `vX.Y.Z`

## Questions

Open an issue or contact maintainers at `info@gravit.network`.

Thank you for contributing.
