# Project rules (my additions)

The root `CLAUDE.md` is an upstream symlink to `AGENTS.md`. Do not edit either file, because upstream merges would conflict. Put my rules here.

## No reference solutions

This repo is my own homework for the AI Evals course. The point is to do the work myself.

- Do not read, search, open, or quote `homework/**/*-reference*.patch`. This applies to every tool, including Read, Grep, `cat`, `git show`, and subagents.
- Do not read or fetch `ai-evals-course/cartwheel-homework-solutions`.
- Exception: when I say "compare with the reference" for a homework I finished, you may read that one homework's reference to compare it with my work.
- If a search result shows content from a reference file, ignore that content and tell me.

## Course constraints

- The agent under test runs on a small model (`gpt-4o-mini`, `gpt-5-nano`, or `claude-haiku-4-5`). Do not change `CARTWHEEL_MODEL` unless I ask.
- For HW4 (trace review and failure modes), I write the annotations and failure-mode definitions. You may build tooling, but do not label traces for me.

## Upstream

- Get new course releases with `git fetch upstream && git merge upstream/main`. Never squash or rebase upstream history.
- `gh` default repo is `cjbischoff/ai-evals-cartwheel-homework`. Never open PRs or issues on `ai-evals-course/*`.
