# Architecture: System Design and Patterns

**Analysis Date:** 2025-07-16

## Architectural Pattern

**Thin-wrapped agent with authorization-gated tools.** The agent (LLM) decides *what to do* and produces tool calls. Code enforces *who can do it* via auth checks inside each tool function. The model does not control access — `agent/auth.py` and tool-level permission checks do.

```
User input
  │
  ▼
Agents SDK Runner          (loop: model → tool → model → tool ...)
  │
  ├─ Agent (model + system prompt)
  │    │
  │    ├─ search_help_center(query)     → BM25 → policy docs
  │    ├─ get_order(order_id)           → SQL → order record
  │    ├─ issue_refund(order, amount)   → auth + eligibility → SQL
  │    ├─ get_policy(policy_id)         → policy file lookup
  │    ├─ search_products(query)        → SQL → product list
  │    ├─ list_my_orders()              → auth-scoped SQL
  │    ├─ cancel_order(order)           → auth + killswitch → SQL
  │    ├─ find_order(description)       → BM25 → orders
  │    └─ escalate_to_human(summary)    → SQL → ticket
  │         │
  │         ▼
  │    LiteLLM → provider API
  │
  └─ Response to user
```

## Layers

### Layer 1: Entry

| Entry point | File | Role |
|---|---|---|
| CLI | `agent/cli.py` | Interactive chat. `uv run python -m agent.cli --role shopper --user 1` |
| FastAPI | `server/app.py` | Homework 2: session creation + message posting over HTTP |
| Replay harness | `replay/harness.py` | Batch replay eval cases from JSONL (Module 3) |
| Scenario runner | `scenarios/runner.py` | Executes scenario datasets, exports traces |

### Layer 2: Agent

| File | Responsibility |
|---|---|
| `agent/agent.py` | System prompt template, lecture tools (`search_help_center`, `get_order`, `issue_refund`, `escalate_to_human`), SDK wiring |
| `agent/tools.py` | Homework 1 tools (`get_policy`, `search_products`, `list_my_orders`, `cancel_order`, `find_order`) — initially `NotImplementedError` |
| `agent/config.py` | `load_facts()`, `db_path()` — loads `facts.yaml` and resolves DB location |

### Layer 3: Auth and Guards

| File | Responsibility |
|---|---|
| `agent/auth.py` | `AuthContext` dataclass, `can_view_order`, `can_refund_order`, `can_cancel_order`, `permission_denied()` |
| `agent/guards.py` | `can_refund_order()` — expanded permission check |
| `agent/killswitch.py` | Global kill switch (`refunds_paused`, `cancellations_paused`) with contextual reason |

### Layer 4: Data

| File | Responsibility |
|---|---|
| `agent/db.py` | Typed dataclasses (`Order`, `User`, `Store`, etc.), connection helpers, typed queries |
| `agent/helpcenter.py` | Policy doc loader (YAML front matter + markdown body), BM25 index builder |
| `seed/eligibility.py` | `refund_needs_approval()` — computes refund eligibility from order state, return window, and `facts.yaml` constants |

### Layer 5: Observability

| File | Responsibility |
|---|---|
| `observability/instrument.py` | Langfuse/OTel setup, `record_tool_result()` decorator, `configure_model_tracing()` |

## Key Patterns

### Result Convention

Every tool returns `dict[str, Any]`:
- **Success**: `{"ok": True, ...payload fields...}`
- **Failure**: `{"ok": False, "error": "<code>", "reason": "<human-readable>"}`

Error codes: `permission_denied`, `not_found`, `not_eligible`, `invalid_argument`, `paused`, `not_implemented`.

### Authorization is Code, Not Prompt

The system prompt does not list permission rules. Every tool checks `AuthContext` before touching data. The module-level docstring in `agent/auth.py` states: *"authorization is not a prompt"*.

### No Async

The entire agent loop is synchronous (OpenAI Agents SDK runs `function_tool` synchronously). Server endpoints use `asyncio` for HTTP, but the agent run itself is synchronous.

### Configuration Through Facts

`facts.yaml` is the single source of numeric policy values. `seed/validate.py` checks every claim in every policy doc against these facts. The agent does not read YAML — it reads rendered policy markdown from `data/policies/`.
