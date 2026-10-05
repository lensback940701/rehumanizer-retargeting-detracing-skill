# Rehumanizer · Retargeting · Detracing (RRD)

**Recover the most valuable research claim the evidence can support.**

[简体中文](README.zh-CN.md) · [Download skill](downloads/rrd-v3.4-skill.zip) · [Skill specification](SKILL.md) · [Development record](docs/review-20261005/DEVELOPMENT_TEST_LOG.en.md) · [Known limitations](docs/KNOWN_LIMITATIONS.md)

<p align="center"><img src="docs/images/hero-cyber.png" width="560" alt="A human researcher and a holographic digital twin converge around evidence and a redirected research target." /></p>

RRD is a two-stage manuscript-revision skill for complete drafts that have drifted during repeated revision. It addresses weakened or displaced claims, flattened evidence, disconnected prose and workflow residue. It is not an AI-detection evasion tool and does not replace scholarly judgment.

**Version:** v3.4 · **Use:** supervised working baseline · **Acceptance hardening:** pending · **License:** maintainer decision pending; no license has been assigned.

## What it does

![Problems, core capabilities and intended deliverables](docs/images/overview.png)

| Capability | Purpose |
| --- | --- |
| Retargeting | Recover the most valuable claim that located evidence supports—not necessarily the earliest, boldest or broadest claim. |
| Rehumanizing | Revisit source materials; restore situated actors, context, author judgment, interpretive depth, cohesion and narrative structure. |
| Detracing | Remove generic or process-heavy prose and unnecessary defensive wording while preserving justified qualifications and counter-evidence. |

The images are explanatory illustrations. Their simplified file trees are not command specifications. The authoritative procedure is [SKILL.md](SKILL.md); the source manifest used by `final_check.py` is CSV, not the illustrative `.txt` name.

## Quickstart

![Four-step supervised use](docs/images/quickstart.png)

Make this directory available to an agent environment that supports local skills, following that environment's installation instructions. Python is required for the local checking scripts. Markdown and TXT are the simplest scanner inputs; optional document readers and additional dependencies depend on the formats used. The full regression suite uses `python-docx`.

1. Prepare the current manuscript, available earlier drafts, source materials and author constraints. Keep private research files outside the public repository.
2. Explicitly invoke `$rehumanizer-retargeting-detracing-skill` for **Stage 1 only**. It diagnoses read-only and produces a handoff Goal and launch prompt.
3. Review the recovered target, proposed changes to inherited constraints and revision intensity. Author authorization is required before revision.
4. Start a **new conversation** using the generated handoff Goal and launch prompt for Stage 2. Re-read evidence and counter-evidence, revise within the authorized scope, verify, then rerun checks after the final edit and export.

Example Stage 1 request:

```text
Use $rehumanizer-retargeting-detracing-skill for Stage 1 only.
Diagnose the supplied manuscript without modifying it.
Recover the best evidence-supported research target, audit inherited constraints,
and prepare the diagnosis, GOAL.md and SHORT_LAUNCH_PROMPT.md.
Ask only for author decisions that materially change the proposed revision.
```

Useful script commands, run from this repository root:

```bash
python scripts/trace_scan.py --help
python scripts/defense_gate.py --help
python scripts/final_check.py --help
python -m unittest discover -s tests -v
```

These scripts inspect and validate files; they do not themselves call a language model or automatically write the manuscript.

## Workflow and intended transformation

![Two-stage diagnosis, revision and verification](docs/images/workflow.png)

The full Stage 2 procedure returns to source materials and checks the target against counter-evidence **before the main rewrite**. The overview diagram compresses this ordering; follow the Goal template and skill specification when executing.

![Conceptual before-and-after transformation](docs/images/before-after.png)

This comparison illustrates the intended transformation, not a paired empirical demonstration. Narrowing a claim can be an improvement when evidence requires it; stronger scholarship is not synonymous with broader scope or fewer qualifications.

## Evaluation status

![Development observations and open engineering gaps](docs/images/test-results.png)

| Evidence track | Recorded observation | Interpretation |
| --- | --- | --- |
| Developer-reported manuscript evaluations | 39 → 41 → 42 → 37; the 42-point checkpoint was retained | One manuscript; score maximum, rubric and repeated-run stability were not supplied. |
| Archived independent engineering review, 2026-10-05 | 47 / 47 packaged tests passed | Covered synthetic scenarios; not a manuscript-quality score or a live CI badge. |
| Additional interface probes | 6 controls behaved as expected; 5 negative probes exposed gaps; 1 additional schema observation | Acceptance hardening remains open. |

The dashboard's five thematic gap rows group six observations; state/configuration checks share a row. The score labels A–D correspond to record-local B01–B04, not Git commits. No percentage score, statistical significance or cross-manuscript reliability claim is made. Packaging this repository did not rerun the 47-test suite or generate a new manuscript revision.

See the [bilingual development records](docs/review-20261005/README.md), [raw test summary](docs/review-20261005/evidence/test_summary.json) and [developer-reported score metadata](docs/review-20261005/benchmark_history.developer_reported.json).

## Repository layout

```text
SKILL.md                 Agent-facing entry point
agents/                  Explicit-invocation configuration
references/              Eight methodological and writing protocols
assets/templates/        Goals, ledgers, registers and result templates
scripts/                 Six inspection and verification scripts
tests/                   Packaged synthetic regression tests
docs/images/             Six README illustrations
docs/review-20261005/     Historical review records and test evidence
docs/KNOWN_LIMITATIONS.md Open acceptance issues and use boundaries
```

## Integrity and contribution boundaries

Preserve source files, anonymity, consent, accurate quotation and genuine counter-evidence. Do not fabricate facts, citations, numbers, motives or findings. Do not upload unpublished manuscripts or participant data as public bug-report fixtures; use synthetic or appropriately cleared examples.

For development, keep changes to writing instructions separate from acceptance-engineering fixes. Add a reproducing test for each bug. Do not weaken gate configuration merely to obtain a pass.

## License and publication status

No license was present in the supplied v3.4 artifact, and this preparation step does not assign one. The maintainer must choose a license before this project is described as licensed open source. The source is publicly available in this repository. A release tag is not created by this publication. Historical test evidence and current GitHub Actions results must be interpreted separately.
