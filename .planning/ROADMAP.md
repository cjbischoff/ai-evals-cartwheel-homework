# Roadmap

## Phase 1: Module 1 — Support Agent, Tracing, and Scenarios
**Goal:** Implement the Cartwheel support agent tools, authenticated server endpoints with tracing, and build a scenario dataset.

**Success Criteria:**
1. All 5 HW1 tools pass contract tests (test_hw_holes.py)
2. Session creation and message posting endpoints work with auth
3. Tracing attributes populate correctly on tool result and permission-denied spans
4. Auth tests pass and verify endpoint security
5. Scenario dataset created with schema validation
6. Traces exported from Langfuse

**Requirements:** MOD1-HW1-01 through MOD1-HW3-03

---

## Phase 2: Module 2 — Trace Review and LLM Judges
**Goal:** Review exported traces, define failure modes, and develop/test LLM judges.

**Success Criteria:**
1. Exported traces reviewed with documented failure modes
2. At least one LLM judge developed and tested
3. Judge validated against human-labeled data

**Requirements:** MOD2-HW4-01 through MOD2-HW5-02

---

## Phase 3: Module 3 — CI and Monitoring
**Goal:** Build CI pipeline with automated evaluation and configure monitoring for one failure mode.

**Success Criteria:**
1. CI pipeline runs tests and evaluates agent
2. Monitoring configured for selected failure mode
3. Alerts trigger on detected failures

**Requirements:** MOD3-HW6-01 through MOD3-HW7-02

---

## Phase 4: Module 5 — Optimization
**Goal:** Improve agent accuracy and reduce cost through optimization techniques.

**Success Criteria:**
1. Accuracy improved on target failure mode
2. Pareto frontier produced comparing configurations
3. Token usage reduced
4. Prompt caching and model cascade working
5. Score and cost comparison documented

**Requirements:** MOD5-HW8-01 through MOD5-HW9-04
