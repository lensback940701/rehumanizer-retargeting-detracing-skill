# Reference and provenance notes

## U1 — Developer report

The current conversation reports manuscript-evaluation scores of 39, 41, 42 and 37, followed by rollback to the penultimate 42-point version. No underlying rubric or per-run artifacts were supplied. These numbers are developer-reported observations, not independently reproduced evaluation results.

## C1 — Uploaded implementation

Artifact: `rehumanizer-retargeting-detracing-skill_v3.4_20261004.zip`.

SHA-256: `e700905b50a965377fea54e851cac721c4cbea2436a8f0acab8538fcd6402c2b`.

Source locations in `REVIEW.zh-CN.md` refer to the extracted files in this exact artifact. Current source hashes and the comparison with the earlier uploaded package are retained in `evidence/package_manifest.json` and `evidence/changes.diff`.

## T1 — Independent script execution

See the four completed `tests_*.log` files, `test_summary.json`, `probe_v34.py`, and `contract_probes/summary.json`. Probe acceptance requirements are stated explicitly. Five negative cases exposed gaps; six positive controls behaved as expected; one additional result-schema inconsistency was observed during a positive write-result invocation. These are targeted counterexamples, not an error-rate estimate.

## D1 — Agent Skills specification

Publisher: Agent Skills. Page: Specification. Accessed 2026-10-05.

Official location: `https://agentskills.io/specification`

Relevant requirements: a nonempty description of no more than 1,024 characters; name and directory conventions. The guidance also recommends keeping the main skill file below 500 lines. Runtime installation was not independently tested.

## D2 — Evaluation best practices

Publisher: OpenAI. Page: Evaluation best practices. Accessed 2026-10-05.

Official location: `https://developers.openai.com/api/docs/guides/evaluation-best-practices`

Used only for general methodological context: task-specific evaluations, logging, human calibration, repeated/continuous evaluation, held-out examples, and pairwise comparisons. No OpenAI scoring scale, model identity, or platform-specific test configuration is attributed to the developer's experiment. Recommendations in the records are proposed future work, not completed experiments.
