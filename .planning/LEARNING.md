# Learning progress

Teaching mode: I write all homework code and run all commands. The agent explains, reads code with me, and gives hints. Rules are in `.planning/config.json` under `homework_rules`.

## Step loop

1. Explain the concept (diagram if useful).
2. Read the code the step touches.
3. Predict what will happen.
4. Write the code. Hints in order: concept, API or line, pseudocode. Full answer only on request.
5. Run it, explain the output, one check question, update this file.

## HW2 lessons

| # | Lesson | Handout part | Status |
|---|---|---|---|
| 0 | Calibrate and review HW1 (`agent/tools.py`, `AuthContext`) | — | done |
| 1 | Traces and spans: write `record_tool_result` | A | done, checked in Langfuse |
| 2 | Identity and tokens: write `create_session` | B | done |
| 3 | Root span and prompt versions: write `post_message` | C | done, checked in Langfuse |
| 4 | Testing: write `tests/test_observability.py` | D | done |
| 5 | Live traces in Langfuse (setup checklist) | E | done |
| 6 | Prompt comparison, `hw2-traces.json`, commit and PR | F | next |

Video: recorded by me after Lesson 6.

## Session log

- 2026-10-19: Plan agreed. Coding level: none. Explain all Python syntax at first use.
- 2026-10-19: Lesson 0 started. Step 0.1: big picture and reading `list_my_orders`.
- 2026-10-20: Step 0.1 done. Understood: scope comes from `ctx.user_id`, not from the chat. Step 0.2: `cancel_order` and `permission_denied`.
- 2026-10-20: Step 0.2 done. Learned: order IDs are global (primary key); the permission check, not the lookup, filters by user. Step 0.3 done: `_call` runs every tool and then `record_tool_result(ctx, result)`.
- 2026-10-20: Lesson 0 done. Next: Lesson 1 (traces and spans, Part A).
- 2026-10-22: Lesson 1 started. Step 1.1: what traces, spans and attributes are.
- 2026-10-22: Step 1.1 done. Needed help: model spans vs tool spans (one tool span per tool run); permission_denied is set on every tool span, false when allowed. Step 1.2: read the stubs in `observability/instrument.py`.
- 2026-10-22: Step 1.2: user asked for bigger steps, with the agent writing the code and explaining it. Rules updated in config.json.
- 2026-10-22: Part A written by the agent with explanation. 3 tests in tests/test_observability.py fail first, then pass. Full suite: 150 passed, 0 failed. Not committed. Next: Lesson 2 (Part B, `create_session`).
- 2026-10-22: Check answer correct (not_found is not a denial). Part B written: 3 rejection tests (400, 404, 403) fail first, then pass; supplied hw2 test passes. Suite: 153 passed, 0 failed. Next: Lesson 3 (Part C).
- 2026-10-22: Check answer mostly right. Demo: edited token -> 401 bad token signature. Learned the two layers (signature check, then card from server memory; token role never used).
- 2026-10-22: Part C written: 3 tests (root span, content off, cross-session 403) fail first, then pass. Suite: 156 passed, 0 failed. Ruff clean. Not committed. Next: Lesson 4 (review the tests, run the Part D commands).
- 2026-10-25: Check answer "they will be different" was half right. Demo showed: same version for every user (template is hashed before filling in user fields); a one-word edit changes it.
- 2026-11-02: Lesson 4: user ran all three Part D commands. hw2: 1 passed. test_observability: 9 passed. Full suite: 156 passed, 4 skipped, 18 xfailed, 9 xpassed, 0 failed. Waiting on check question (what breaks if the role check is deleted).
- 2026-11-02: Lesson 4 done (needed help finding the test from the -v list). Lesson 5 started.
- 2026-11-02: Lesson 5 step 1 done: other project containers stopped, Langfuse up, Langfuse keys added to .env, server up (health ok). Step 2: send 5 requests (HW1 records 1, 4, 8, 9, 10).
- 2026-11-02: Lesson 5 step 2 done. 5 live requests (gpt-4o-mini), 5 traces in Langfuse. Trace ids (first 8): 66f6e7d1 shopper get_order; d8e66ba7 merchant get_order DENIED; 252a646b merchant list_my_orders store 2; 7cfb61bd support get_order; 7a691dfd shopper find_order. All prompt_version cdfb0444e3d3. Langfuse shows gen_ai.input/output.messages as the root span Input/Output, not metadata. Next: step 3, read the traces in the Langfuse UI.
- 2026-11-02: Lesson 5 done (user read trace d8e66ba7: model turned the denial into a friendly reply; it offered escalation but did not call escalate_to_human, which is worth reviewing in HW4). Lesson 6 started.
- 2026-11-02: Part F done. Baseline trace 66f6e7d1 (current prompt) = cdfb0444e3d3. Pre-HW1 prompt (2 escalation lines removed) trace f561e359 = d108f6949e5e, as predicted. Same request (shopper 1, order 4127), new sessions, gpt-4o-mini. Prompt restored; agent/ matches the committed file. Server restart with restored prompt pending.
- 2026-11-02: hw2-traces.json written from Langfuse data: 66f6e7d1 (shopper, allowed) and d8e66ba7 (merchant, denied). Both final_status completed. Next: commit and PR.
- 2026-11-02: Full suite: 1 failure, test_m2_run_judge_persists_store_predictions_for_prevalence. Root cause: litellm/__init__.py:27 runs load_dotenv() on import, so the Langfuse keys added to .env in Lesson 5 make analysis use live Langfuse (no Module 2 traces). Not an HW2 bug. With LANGFUSE_PUBLIC_KEY= set empty: 0 failures. Decision on fix pending.
- 2026-11-02: Suite decision: option 1 (no file changes; run with LANGFUSE_PUBLIC_KEY= and note in PR). PR body drafted at .git/PR_BODY_HW2.md. Next: user runs commit and PR commands.
