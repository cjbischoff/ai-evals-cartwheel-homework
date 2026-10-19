# Testing: Framework, Structure, and Practices

**Analysis Date:** 2025-07-16

## Framework

- **pytest 8.x** — configured in `pyproject.toml [tool.pytest.ini_options]` with `testpaths = ["tests"]`.
- No doctests, no unittest.TestCase, no hypothesis/property-based testing.
- No coverage configuration present (no `.coveragerc`, no `pytest-cov`).

## Test Structure

```
tests/
├── conftest.py                    # Shared fixtures (seeded world DB, auth contexts)
├── test_hw_holes.py               # Contract tests for HW1 + HW2 (xfail markers)
├── test_agent_tools.py            # Tool-level unit tests
├── test_auth.py                   # AuthContext permission matrix tests
├── test_db.py                     # Data access layer tests
├── test_cli.py                    # CLI interaction tests
├── test_eligibility.py            # Refund eligibility logic tests
├── test_adversarial.py            # Adversarial fixture tests
├── test_seed_determinism.py       # Seed reproducibility tests
├── test_harbor_adapter.py         # Harbor adapter tests
├── test_langfuse_export.py        # Langfuse export tests
├── test_normalization_metadata.py # Trace normalization tests
├── test_optimization.py           # Module 5 optimization tests
├── test_replay_harness.py         # Module 3 replay tests
├── test_scenario_runner.py        # Scenario execution tests
├── test_scenario_validation.py    # Scenario validation tests
└── eval/                          # Module 2 eval tests
    ├── conftest.py                # Eval-specific fixtures
    ├── test_e2e.py                # End-to-end eval scenarios
    ├── test_integration.py        # Integration tests
    ├── test_unit.py               # Unit-level eval tests
    ├── passk.py                   # pass@k calculation helper
    └── fake_model.py              # Deterministic fake model for testing
```

## Test Fixtures

- `tests/conftest.py` provides a seeded world DB (`world` fixture via `seed/generate.py`).
- `AuthContext` fixtures for `SHOPPER_1`, `SHOPPER_2`, `MERCHANT_STORE_1`, `SUPPORT`.
- Tests run against real SQLite (not mocked DB). Seed is deterministic.
- Eval tests use a `fake_model.py` for deterministic agent responses.

## HW Contract Tests Pattern

```python
def hw(n: int, name: str):
    return pytest.mark.xfail(
        raises=NotImplementedError,
        reason=f"HW{n}: implement {name}",
        strict=False,
    )

@hw(1, "get_policy")
def test_hw1_get_policy(world: dict) -> None:
    result = tools.get_policy(SHOPPER_1, "cw-returns")
    assert result["ok"] is True
    assert result["policy_id"] == "cw-returns"
```

- `strict=False` — an early-implemented function produces XPASS (still green).
- A wrong implementation fails loudly with assertion error (not XPASS).

## Running Tests

```bash
uv run pytest                          # all tests
uv run pytest -k hw1                   # HW1 contract tests
uv run pytest tests/test_auth.py       # auth tests only
uv run pytest -x --ff                  # stop on first failure, run failures first
```

## CI

- GitHub Actions in `.github/workflows/evals.yml`.
- Module 3 (HW6) integrates these tests into the CI pipeline.
- No linting or formatting checks in CI currently.
