# Stack: Technologies and Dependencies

**Analysis Date:** 2025-07-16

## Language and Runtime

- **Python 3.12+** — sole language. No TypeScript, JavaScript, Go, or Rust.
- Package manager: **uv** (Astral). Fast pip-compatible resolver. All deps in `pyproject.toml`.
- No Docker in core — `docker-compose.yml` is for optional Langfuse self-hosting in `observability/`.

## Core Dependencies

| Dep | Version | Purpose |
|---|---|---|
| `openai-agents` | >=0.2 | SDK for agent/tool/loop primitives (`Agent`, `Runner`, `function_tool`, `RunContextWrapper`). The same package regardless of provider — LiteLLM adapts the backend. |
| `litellm` | >=1.70 | Provider router. Lets the agent use OpenAI, Anthropic, Together AI, or Ollama through a common interface. Selection via `CARTWHEEL_MODEL` and provider env vars. |
| `langfuse` | 3.x | Observability backend. Traces agent runs. Self-hosted or cloud. Configured via `LANGFUSE_*` env vars. |
| `opentelemetry-instrumentation-openai-agents` | 0.62.3 | Bridges the OpenAI Agents SDK traces into OTel, which feeds Langfuse. |
| `fastapi` + `uvicorn` | >=0.115 / >=0.30 | HTTP server for the Homework 2 chat API (`/api/create_session`, `/api/message`). |
| `pydantic` | >=2.7 | Runtime type-checked models for agent config, orders, users, stores. |
| `rank-bm25` | 0.2.2 | BM25 retrieval for `search_help_center` — the help-center search tool. |
| `pyyaml` | >=6.0 | Reads `facts.yaml` (the single source of policy numbers). |
| `numpy` | >=1.24 | Used in the analysis/eval helpers for pass@k calculations. |
| `docetl` | >=0.2 | Document processing pipeline library (used in Module 3+ workflows). |

### Dev-only

| Dep | Version | Purpose |
|---|---|---|
| `pytest` | >=8.0 | Test runner. Configuration in `pyproject.toml [tool.pytest.ini_options]`. |
| `gepa` | 0.1.4 | Optimization harness (optional, `[optimization]` extra). Used by Module 5. |

## Key Configuration Files

| File | Purpose |
|---|---|
| `pyproject.toml` | Python deps, build, test paths |
| `facts.yaml` | Single source of truth for policy numbers (return window, refund threshold, SLA) |
| `.env` (gitignored) | API keys, Langfuse credentials, model selection |
| `.env.example` | Template for `.env` |
| `promptfooconfig.yaml` | Promptfoo adversarial eval config (Module 4) |

## Environment Variables

| Variable | Purpose |
|---|---|
| `CARTWHEEL_MODEL` | Model string (e.g. `gpt-4o-mini`, `claude-haiku-4-5`) |
| `LANGFUSE_*` | Langfuse host/public/secret keys |
| `OPENAI_API_KEY` | OpenAI provider key |
| `ANTHROPIC_API_KEY` | Anthropic provider key |
| `TOGETHER_API_KEY` | Together AI provider key |

## Summary

A thin-agent stack: OpenAI Agents SDK as the loop + LiteLLM for provider flexibility + Langfuse/OTel for observability. The only novel component is BM25 local retrieval for policy search — no vector DB, no embedding service.
