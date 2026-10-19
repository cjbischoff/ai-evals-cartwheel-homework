# Integrations: External Services and APIs

**Analysis Date:** 2025-07-16

## External Integrations

### 1. LLM Provider (one of several, selected by config)

- **OpenAI** — default provider. `CARTWHEEL_MODEL=gpt-4o-mini`. `OPENAI_API_KEY` env var.
- **Anthropic** — `CARTWHEEL_MODEL=claude-haiku-4-5`. `ANTHROPIC_API_KEY` env var.
- **Together AI** — `CARTWHEEL_MODEL=glm-5.2`. `TOGETHER_API_KEY` env var.
- **Ollama** — local. No key required.

Provider selection flows through **LiteLLM** (`litellm` package), which normalizes the API shape. The OpenAI Agents SDK talks to LiteLLM, which talks to the real provider. The agent code never imports provider SDKs directly.

### 2. Langfuse (observability)

- **Purpose**: Trace agent runs, record tool calls and model responses.
- **Connection**: HTTP via `LANGFUSE_*` env vars (host, public key, secret key).
- **Mode**: Self-hosted (`observability/docker-compose.yml`) or cloud.
- **Integration**: `observability/instrument.py` configures OTel + Langfuse exporter. All agent runs through the SDK send traces automatically when enabled.

### 3. OpenAI Tracing (optional)

- OpenAI SDK's built-in tracing (`--trace-openai` flag on CLI). Cannot combine with Langfuse tracing. Disabled by default.

## No External Integrations

Cartwheel explicitly does not integrate with:

- **Vector databases / embeddings** — search_help_center uses local BM25 (`rank-bm25`), no external service.
- **Payment processors** — refunds are simulated in SQLite, no Stripe/Adyen call.
- **Email or notification services** — no SMTP, no webhook delivery.
- **External auth providers** — auth is session-based with local SQLite user lookup.
- **CI/CD platforms** — GitHub Actions defined in `.github/workflows/evals.yml`, but not called by the application at runtime.

## Data Flow

```
Chat CLI / FastAPI → OpenAI Agents SDK Runner →
  Agent (model + tools) →
    LiteLLM → real provider (OpenAI/Anthropic/etc.)
    Tool functions → SQLite (data) → structured response
  → Response to user
  ↓
  OTel exporter → Langfuse (traces)
```

## Seed Data

Not an integration, but the sole data source: `seed/generate.py` creates a deterministic SQLite world (20 stores, 800 products, 525 users, 10,000 orders, 18 policies). Run with `uv run python -m seed.generate`. Deterministic per seed in `facts.yaml` or env var.
