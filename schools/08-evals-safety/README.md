# School 08 — Evals & safety

**Job:** Red team, injection, PII, human override — proof over vibes.

## Beginner model
If you cannot break it on purpose, you do not understand it.

## Mechanism
- Fixed suites (`golden10.json`, optional `golden25_domain.json`)  
- Keyword gate + meaning gate + honesty gate  
- Red-team prompts monthly  
- Human override UX that is actually usable  
- Incident → postmortem → new eval  

## Labs in this pack
- Lab 03 golden-10 (required)  
- Lab 05 golden-25 (expanded bar)  
- Lab 04 RTMA quiz  

## Lab GREEN
- [ ] Lab 03 ≥ 80%  
- [ ] Lab 05 ≥ 80%  
- [ ] Personal safety policy written  
- [ ] Read `evals/judge_rubric.md`  

## Personal safety starter
1. No autonomous email/post  
2. No training on private customer audio  
3. No secrets in committed prompts  

## RTMA
**Run** suite · **Trace** per-item pass/fail · **Metric** pass_rate · **Artifact** report md/json.

## Interview 30 / 90
**30s:** Fixed suites catch regressions; safety is permissions plus drills.  
**90s:** Keyword, meaning, honesty gates. Red teams try to skip approvals. Incidents birth new evals.

## Three-layer release harness

1. Deterministic: schema, exact values, citations, permissions, budgets.
2. Model judge: rubric-only meaning checks, blinded and versioned.
3. Human: calibrated labels and named release owner for material risk.

Measure judge-human agreement, inspect disagreements, and keep deterministic
safety checks authoritative. Controlled sabotage research tests code sabotage,
oversight, sandbagging, or harmful choices in isolated scenarios; it is not proof
of a deployed autonomous real-world attack. The lesson is to sandbox, cap, tripwire,
audit, and approval-gate powerful tools. Start with `evals/production_readiness.json`.

## 2026 eval-at-scale practice

- Maintain dataset lineage, task/risk slices, evaluator version, and expected uncertainty.
- Track judge-human agreement and inspect disagreements before trusting aggregate scores.
- Pair safety escape rate with false-refusal rate so one cannot hide the other.
- Shadow-run and canary candidate models before changing the broad production route.
- Convert incidents into sanitized fixtures with deterministic and semantic regression checks.
- Require a named release owner, threshold rationale, monitoring window, and rehearsed rollback.
