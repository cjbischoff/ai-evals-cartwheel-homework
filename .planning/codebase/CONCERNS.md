# Concerns: Technical Debt, Known Issues, and Fragile Areas

**Analysis Date:** 2025-07-16

## 1. Unimplemented Homework Functions (Intentional)

Five tools in `agent/tools.py` raise `NotImplementedError` as starter code:

| Tool | File | Line |
|---|---|---|
| `get_policy` | `agent/tools.py:40` | Needs policy doc lookup via `load_policy_docs()` |
| `search_products` | `agent/tools.py:60` | Needs product search + filtering |
| `list_my_orders` | `agent/tools.py:~80` | Needs DB query scoped by role |
| `cancel_order` | `agent/tools.py:~100` | Needs auth + killswitch + DB |
| `find_order` | `agent/tools.py:~120` | Needs fuzzy order matching |

**Risk**: A student who does not implement these cannot run the agent beyond the three lecture tools. **Intentional** — these are the HW1 deliverables.

Additionally, `observability/instrument.py` and `server/app.py` have HW2 holes.

## 2. No Linting or Type Checking

- No `ruff`, `mypy`, `pyright`, `flake8`, or `pylint` in the project or CI.
- No pre-commit hooks.
- No formatting standard enforced.
- **Risk**: Style drift across contributions. Unused imports, type errors, and dead code can accumulate.

## 3. No Async Support in Agent Loop

The OpenAI Agents SDK runs synchronous `function_tool` functions. Long-running DB queries or policy lookups block the loop. Not a problem at current scale (~synthetic 10,000 orders), but would need async conversion for production.

## 4. SQLite as Single Data Store

- **Risk**: No connection pooling. All tools open/close connections per call via `db.connection()` context manager.
- Concurrent access from FastAPI could cause `SQLITE_BUSY`. The seed DB is small (~100MB), but there is no migration system.
- Schema is created by `seed/generate.py` only — no Alembic, no schema versioning.

## 5. BM25 Without Embeddings

`search_help_center` uses `rank-bm25` for retrieval. No embeddings, no vector DB:
- **Good**: Zero infra cost, deterministic, works offline.
- **Bad**: No semantic matching. Misses synonym queries ("return policy" vs "refund policy"). No hybrid search fallback.

## 6. Kill Switch Is In-Memory Only

`agent/killswitch.py` uses a module-level singleton:
```python
class KillSwitch:
    _refunds_paused: bool = False
```

**Risk**: Restart resets the state. Not cluster-safe if the server were scaled.

## 7. No Rate Limiting or Retry Logic

- No rate limiting on tool execution.
- No retry on DB contention (`SQLITE_BUSY`).
- The LiteLLM layer has its own retry logic, but tool functions do not.

## 8. No Secret Rotation or Key Management

- API keys stored in `.env` (gitignored).
- No key rotation mechanism.
- No encryption at rest for the `.env` file.

## 9. Testing Gaps

- No linting tests (ruff, mypy).
- No coverage threshold or reporting.
- No performance/benchmark tests.
- No property-based tests for edge cases.
- HW tests use `strict=False` xfail — a function could partially pass without being caught.

## 10. Documentation Fragility

- `SPEC.md` is authoritative for behavior. `facts.yaml` is authoritative for numbers. Both must stay in sync with `data/policies/*.md`.
- `seed/validate.py` checks policy docs against `facts.yaml` — but only at seed time. No runtime validation that the agent's understanding matches the spec.
