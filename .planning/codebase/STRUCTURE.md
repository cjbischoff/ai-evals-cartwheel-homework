# Structure: Directory Layout and Organization

**Analysis Date:** 2025-07-16

```
ai-evals-cartwheel-homework/
├── agent/                    # Cartwheel support agent
│   ├── __init__.py
│   ├── agent.py              # System prompt, 4 lecture tools, SDK wiring
│   ├── tools.py              # HW1: 5 student tools (NotImplementedError initially)
│   ├── auth.py               # AuthContext dataclass + permission checks
│   ├── cli.py                # Interactive CLI entry
│   ├── config.py             # load_facts(), db_path()
│   ├── db.py                 # SQLite data layer (typed dataclasses + queries)
│   ├── guards.py             # Extended refund permission check
│   ├── helpcenter.py         # Policy doc loader + BM25 index
│   ├── killswitch.py         # Refund/cancellation kill switch
│   ├── approvals.py          # Approval queue model
│   └── review.py             # Review-related model
│
├── seed/                     # World generator (deterministic)
│   ├── generate.py           # Main: creates DB with stores/users/orders/policies
│   ├── adversarial.py        # Adversarial fixture generation
│   ├── eligibility.py        # refund_needs_approval() logic
│   ├── policies.py           # Policy renderer from facts.yaml
│   └── validate.py           # Validates policy documents against facts.yaml
│
├── server/                   # FastAPI chat API
│   └── app.py                # create_session, post_message endpoints
│
├── scenarios/                # Scenario dataset runner + export
│   ├── runner.py             # Execute scenario JSONL → traces
│   ├── validate.py           # Validate scenario structure
│   ├── export_langfuse.py    # Export scenarios to Langfuse
│   └── atif_export.py        # ATIF format export
│
├── analysis/                 # Module 2: trace analysis + judges
│   ├── server.py             # Analysis server
│   └── helpers/              # Analysis helpers (8 modules)
│
├── replay/                   # Module 3: eval case replay
│   ├── harness.py            # Replay harness
│   └── rollout.py            # Rollout utilities
│
├── monitoring/               # Module 3: monitoring
│   ├── sample.py             # Trace sampling
│   ├── correct.py            # Correction/annotation
│   ├── run_judges.py         # Batch judge execution
│   ├── write_scores.py       # Score persistence
│   └── chart.py              # Chart generation
│
├── optimize/                 # Module 5: accuracy/cost optimization
│   ├── prepare.py            # Preparation scripts
│   ├── runner.py             # Evaluation runner
│   ├── workflow.py           # Optimization workflow
│   ├── gepa_adapter.py       # GEPA optimization harness
│   ├── frontier.py           # Pareto frontier computation
│   ├── save_version.py       # Version snapshot
│   └── check_models.py       # Model capability checks
│
├── harbor_adapter/           # Harbor job analysis
│   ├── agent.py              # Harbor analysis agent
│   ├── analysis.py           # Analysis logic
│   ├── export.py             # Export utilities
│   ├── runtime.py            # Runtime configuration
│   └── summary.py            # Summary generation
│
├── tests/                    # Test suite
│   ├── test_hw_holes.py      # Contract tests for HW1 + HW2 (xfail)
│   ├── test_agent_tools.py   # Agent tool unit tests
│   ├── test_auth.py          # Authorization tests
│   ├── test_db.py            # DB layer tests
│   ├── test_cli.py           # CLI tests
│   ├── test_adversarial.py   # Adversarial fixture tests
│   ├── test_eligibility.py   # Refund eligibility tests
│   ├── test_harbor_adapter.py
│   ├── test_langfuse_export.py
│   ├── test_normalization_metadata.py
│   ├── test_optimization.py
│   ├── test_replay_harness.py
│   ├── test_scenario_runner.py
│   ├── test_scenario_validation.py
│   └── test_seed_determinism.py
│   └── eval/                 # Module 2: evaluation tests
│       ├── conftest.py
│       ├── test_e2e.py
│       ├── test_integration.py
│       ├── test_unit.py
│       ├── passk.py          # pass@k calculation
│       └── fake_model.py     # Fake model for deterministic tests
│
├── data/                     # Runtime data
│   ├── policies/             # Policy markdown files (18 docs)
│   └── *.sqlite              # Seeded world DB (gitignored)
│
├── homework/                 # Student handouts
│   ├── module-1/             # HW1, HW2, HW3
│   ├── module-2/             # HW4, HW5
│   ├── module-3/             # HW6, HW7
│   └── module-5/             # HW8, HW9
│
├── eval_cases/               # Evaluation scenario JSONL files
├── reports/                  # Smoke-test SQL queries
├── scripts/                  # Analysis scripts (harbor jobs)
├── .github/workflows/        # CI: evals.yml
├── .agents/                  # Agent skill definitions
├── .planning/                # GSD planning artifacts
│
├── facts.yaml                # Single source of truth for policy numbers
├── SPEC.md                   # Full specification (access matrix, tool contracts)
├── AGENTS.md                 # Coding agent instructions
├── README.md                 # Setup, usage, homework index
├── pyproject.toml             # Python dependencies and build config
└── promptfooconfig.yaml      # Adversarial eval config
```

## Naming Convention

- **Packages**: lowercase, single word (`agent`, `seed`, `scenarios`, `replay`).
- **Modules**: snake_case (`tools.py`, `killswitch.py`, `helpcenter.py`, `export_langfuse.py`).
- **Functions and variables**: snake_case (`can_view_order`, `refund_needs_approval`, `order_id`).
- **Classes**: PascalCase (`AuthContext`, `Store`, `Order`, `User`).
- **DB column names**: snake_case.
- **Tools**: named as verbs (`get_order`, `issue_refund`, `cancel_order`, `search_products`).
- **Tests**: `test_<module>.py` with `test_<function>` test functions.
