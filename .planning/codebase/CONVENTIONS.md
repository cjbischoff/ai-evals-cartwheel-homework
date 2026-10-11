# Conventions: Code Style and Patterns

**Analysis Date:** 2025-07-16

## Python Style

- **Type annotations** required on every function signature, including `-> None` for void functions.
- **Docstrings** on every public function and module (Google style). Module docstrings explain purpose, responsibility, and key relationships.
- **`from __future__ import annotations`** used in every file — deferred evaluation of annotations.
- **No third-party formatter/linter config** — no `.ruff.toml`, no `.flake8`, no `.pylintrc`. Relies on Python 3.12+ conventions.

## Error Handling Pattern

Every tool function returns a `dict` with a standard shape:

```python
# Success
return {"ok": True, "order_id": order_id, "status": "cancelled"}

# Failure
return {"ok": False, "error": "not_eligible", "reason": "Order status is 'shipped', not 'placed'"}
```

Error codes used across the codebase:
- `permission_denied` — caller lacks access
- `not_found` — entity does not exist
- `not_eligible` — entity exists but cannot be acted on
- `invalid_argument` — bad input (empty query, nonpositive amount)
- `paused` — feature is kill-switched
- `not_implemented` — placeholder

Unexpected runtime errors raise exceptions (not caught). The SDK handles propagation.

## Import Patterns

- `from __future__ import annotations` at the top of every module.
- Standard library imports first, then third-party, then local.
- Use `from agent import db` style, not relative imports within the `agent` package.
- Type-only imports use `TYPE_CHECKING` guard in `agent/config.py`.

## Data Access Pattern

```python
# Tools call db functions (never direct SQL), after auth check.
def cancel_order(ctx: AuthContext, order_id: int, reason: str) -> dict[str, Any]:
    if kill_switch.cancellations_paused():
        return {"ok": False, "error": "paused", "reason": kill_switch.cancellations_reason()}

    with db.connection() as conn:
        order = db.get_order(conn, order_id)
        if order is None:
            return {"ok": False, "error": "not_found", "reason": f"No order '{order_id}'"}
        if not can_cancel_order(ctx, order):
            return permission_denied(f"Cannot cancel order '{order_id}'")
        if order.status != "placed":
            return {"ok": False, "error": "not_eligible", ...}
        db.cancel_order(conn, order_id, reason)
        return {"ok": True, "order_id": order_id, "status": "cancelled"}
```

## Control Flow

- No `async` in agent tools. The SDK runs synchronous `function_tool` functions.
- No context managers for single DB reads — use `db.connection()` as a context manager.
- `with closing(db.connect()) as conn:` in non-context-manager paths.

## Testing Conventions

- Tests use `pytest` with `conftest.py` fixtures.
- HW contract tests use `pytest.mark.xfail(raises=NotImplementedError)` — they "fail as expected" before implementation.
- Test functions named `test_<unit>_<scenario>`.
- No mocking layer in HW tests — they run against a real seeded DB (from `conftest.py`).
- Authorization tests in `test_auth.py` test the `AuthContext` checks directly, not through tools.

## Configuration Pattern

- `facts.yaml` loaded at agent startup via `agent/config.py:load_facts()`.
- `agent/config.py` reads `.env` for secrets and `facts.yaml` for policy numbers.
- No environment-variable-based feature flags in the agent. Kill switch is a singleton in code.
