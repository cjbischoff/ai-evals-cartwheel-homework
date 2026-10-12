# Cartwheel Course Homework

## What This Is

AI Evals course homework repository built on the Cartwheel fictional commerce platform. Complete the support agent, then use it for trace analysis, automated evaluation, CI, adversarial evaluation, and improvement experiments across 5 modules.

## Core Value

Complete all module homeworks with working, tested implementations that pass the course's automated tests and produce the required artifacts.

## Requirements

### Validated

The existing Cartwheel codebase provides:

- ✓ Agent scaffold (`agent/`) with auth, DB, help center, CLI
- ✓ Server with session/message routes (`server/`)
- ✓ Policy corpus from `facts.yaml` (18 policy documents)
- ✓ Deterministic seed data (20 stores, 800 products, 525 users, 10,000 orders, 3 demo orders)
- ✓ Self-hosted Langfuse observability via Docker Compose
- ✓ Scenario runner, validator, and Langfuse exporter (`scenarios/`)
- ✓ Test framework with contract tests

### Active

- [ ] **MOD1-HW1**: Implement 5 support agent tools (`get_policy`, `search_products`, `list_my_orders`, `cancel_order`, `find_order`)
- [ ] **MOD1-HW2**: Implement authenticated session/message endpoints and tracing attributes
- [ ] **MOD1-HW3**: Build support scenario dataset with trace export
- [ ] **MOD2-HW4**: Review traces, define failure modes
- [ ] **MOD2-HW5**: Develop and test LLM judges
- [ ] **MOD3-HW6**: Build CI for the Cartwheel agent
- [ ] **MOD3-HW7**: Monitor one failure mode after deployment
- [ ] **MOD5-HW8**: Improve accuracy on one failure mode, Pareto comparison
- [ ] **MOD5-HW9**: Reduce cost with fewer tokens, prompt caching, model cascade

### Out of Scope

- Modifications to course-provided evaluation fixtures and test oracles — preserve for regression
- Changes to the auth/permission system (provided complete, do not weaken)
- Greenfield features outside the course assignments

## Context

Built on [ai-evals-course/cartwheel-homeworks](https://github.com/ai-evals-course/cartwheel-homeworks) starter. The repo is already set up with Python 3.12, uv, pytest, and all dependencies. Current branch is `feat/hw1-tools` with partial HW1 implementation in progress.

Workflow per homework: user provides the spec (handout), we discuss, I build test-first, tests verify. New branch per homework (`feat/hwN-{slug}`), conventional commits.

## Constraints

- **Agent model**: Small/cheap model (`gpt-4o-mini`, `claude-haiku-4-5`, `gpt-5-nano`) — frontier models bypass the synthetic-world mistakes the course depends on
- **Auth/permissions**: Supplied complete — do not weaken or bypass
- **Evaluation cases**: Supplied — preserve as regression tests
- **Branch**: One branch per homework, conventional commits
- **Test-first**: Write the failing test, implement, verify green
- **No Git push**: No secrets committed, no force push, no amend on pushed commits

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| 4 phases = 5 modules | Module 4 has no standalone homework deliverables | — Pending |
| Phase per module, homework per branch | Clear scope per phase, per-homework isolation | — Pending |
| Spec-driven discussion then build | User provides the handout each time | — Pending |
| Start with HW1 in progress | Already on `feat/hw1-tools` with partial implementation | ✓ Current state |
| GSD agents not installed | Subagent calls disabled — roadmap generated inline | ✓ Confirmed |

---

*Last updated: 2026-10-12 after project initialization*
