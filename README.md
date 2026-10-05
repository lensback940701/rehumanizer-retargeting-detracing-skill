# Rehumanizer · Retargeting · Detracing (RRD)

**Keep the idea ambitious. Make scholarly voice measurable. Sharpen the work while it is being built.**

[简体中文](README.zh-CN.md) · [Original v3.4 snapshot](downloads/rrd-v3.4-skill.zip) · [Skill specification](SKILL.md) · [Development record](docs/review-20261005/DEVELOPMENT_TEST_LOG.en.md) · [Known limitations](docs/KNOWN_LIMITATIONS.md)

<p align="center"><img src="docs/images/hero-cyber.png" width="560" alt="A human researcher and a holographic digital twin converge around evidence and a redirected research target." /></p>

RRD is a reusable, two-stage academic sharpening skill for manuscripts in progress. It preserves the ambition of the idea, makes selected dimensions of human scholarly voice measurable, and restores focus, material force and narrative clarity whenever an existing draft or section needs them. It is not a finalization or closure skill, an AI-detection evasion tool, or a replacement for author judgment.

**Version:** v3.4 · **Use:** supervised working baseline · **Acceptance hardening:** pending · **License:** maintainer decision pending; no license has been assigned.

## Core commitments

<p align="center">
  <img src="docs/images/core-highlights-art.png" width="100%" alt="RRD's three core commitments: ambition first, measurable human voice without fixed quotas, and sharpening while building." />
</p>

RRD is guided by three commitments: protect the ambition of the idea, make human scholarly voice observable without prescribing a formula, and strengthen the manuscript while research and writing are still underway. These commitments define what the skill protects, how it diagnoses problems, and when it should be used.

### 1. Ambition first

**Preserving the idea's scholarly ambition is RRD's highest editorial principle.** The goal is not to make a manuscript merely safer, tidier or less exposed. It is to recover the most valuable research claim that the available evidence can genuinely support.

RRD therefore does more than remove hedges. It is designed to end the repeated **soften–restore–soften loop** that can take over AI-assisted revision. Once the author has confirmed a supportable research target, later checks should not quietly weaken it merely to sound more cautious. Reconsidering that target requires new evidential grounds or an explicit author decision, not a generic preference for safer prose.

Facts, accurate quotation and genuine counter-evidence remain non-negotiable boundaries. They are not a standing excuse for lowering the paper's intellectual ambition. Retargeting restores the argument's direction; retiring unnecessary defensive constraints prevents subsequent checks from undoing that recovery.

### 2. Measurable human voice

RRD makes selected dimensions of human scholarly voice **observable, measurable and comparable**. Rather than treating human feel as an undefined aesthetic preference, it examines sentence rhythm, quotation density, authorial stance, paragraph cohesion, expressive variation and recurring templates.

**These indicators can be counted and interpreted, but their realized quantities must not be prescribed as fixed quotas.** RRD does not decide in advance that a draft must contain exactly three quotations, a transition every two sentences, or a fixed density of stance markers. The model generates context-sensitive phrasing, rhythm and material placement; the resulting counts and distributions are then measured and read in context.

**Measurable diagnostics; stochastic realization; no fixed quotas.** Variation belongs to the model's generative process, not to a separate sampler allocating stylistic quantities in advance. Reference writing provides a basis for comparison, not a statistical template every draft must reproduce. A warning directs attention to broken flow, flattened material or monotonous expression; it does not instruct the writer to optimize a number for its own sake.

The aim is not a universal human-voice score. It is to make selected writing problems easier to detect and repair while preserving room for expressive variation. Facts, quotations, source fidelity and the agreed research target are not randomized.

### 3. Sharpen while building

**RRD is an in-process sharpening tool, not a finalization skill.** Bring it into the workflow when an idea has been diluted, evidence has become detached from the argument, prose has become mechanical, or a new insight requires a sharper research target.

It can be used throughout drafting, revision and rethinking, on either a whole manuscript or a clearly scoped section. The prerequisite is inspectable text and accessible supporting material—not proximity to submission. Each invocation retains the **read-only diagnosis → author authorization → scoped revision** structure.

The output is a stronger working checkpoint that returns to research and writing. It does not declare the manuscript finished, certify submission readiness, or require a handoff to final polish. Reuse responds to substantive development needs; it is not an instruction to keep revising an unchanged draft.

**Ambition sets the direction. Measurable signals inform the diagnosis. In-process sharpening defines the role.**

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

For the current description and in-process usage guidance, use the files on `main`. The linked ZIP is the original v3.4 snapshot and does not include this positioning update; the publication manifests and archived tests refer to that original snapshot.

Make this directory available to an agent environment that supports local skills, following that environment's installation instructions. Python is required for the local checking scripts. Markdown and TXT are the simplest scanner inputs; optional document readers and additional dependencies depend on the formats used. The full regression suite uses `python-docx`.

1. Prepare the current draft or selected sections, available earlier drafts, source materials and author constraints. Declare the revision scope. Keep private research files outside the public repository.
2. Explicitly invoke `$rehumanizer-retargeting-detracing-skill` for **Stage 1 only**. It diagnoses read-only and produces a handoff Goal and launch prompt.
3. Review the recovered target, proposed changes to inherited constraints and revision intensity. Author authorization is required before revision.
4. Start a **new conversation** using the generated handoff Goal and launch prompt for Stage 2. Re-read evidence and counter-evidence, revise within the authorized scope, verify, then rerun checks after the last edit and export of this checkpoint. Return to drafting or research; final polish remains a separate choice.

Example Stage 1 request:

```text
Use $rehumanizer-retargeting-detracing-skill for Stage 1 only.
Diagnose the supplied draft or selected sections without modifying them.
Preserve the idea's ambition as the highest editorial principle.
Use measurable voice signals without imposing fixed stylistic quotas.
Recover the best evidence-supported target for the declared scope, audit inherited constraints,
and prepare the diagnosis, GOAL.md and SHORT_LAUNCH_PROMPT.md.
Ask only for author decisions that materially change the proposed revision.
Treat the output as an in-process checkpoint, not a finalization decision.
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

The dashboard's five thematic gap rows group six observations; state/configuration checks share a row. The score labels A–D correspond to record-local B01–B04, not Git commits. No percentage score, statistical significance or cross-manuscript reliability claim is made. The 42-point record is not a validated human-voice score or a separate estimate of the effect of generative variability. Packaging this repository did not rerun the 47-test suite or generate a new manuscript revision.

See the [bilingual development records](docs/review-20261005/README.md), [raw test summary](docs/review-20261005/evidence/test_summary.json) and [developer-reported score metadata](docs/review-20261005/benchmark_history.developer_reported.json).

## Repository layout

```text
SKILL.md                 Agent-facing entry point
agents/                  Explicit-invocation configuration
references/              Eight methodological and writing protocols
assets/templates/        Goals, ledgers, registers and result templates
scripts/                 Six inspection and verification scripts
tests/                   Packaged synthetic regression tests
docs/images/             README illustrations
docs/review-20261005/     Historical review records and test evidence
docs/KNOWN_LIMITATIONS.md Open acceptance issues and use boundaries
```

## Integrity and contribution boundaries

Preserve source files, anonymity, consent, accurate quotation and genuine counter-evidence. Do not fabricate facts, citations, numbers, motives or findings. Do not upload unpublished manuscripts or participant data as public bug-report fixtures; use synthetic or appropriately cleared examples.

For development, keep changes to writing instructions separate from acceptance-engineering fixes. Add a reproducing test for each bug. Do not weaken gate configuration merely to obtain a pass.

## Positioning update

This update changes the description, invocation guidance and bilingual README to foreground ambition-first, measurable and reusable in-process sharpening. It does not change the scanner, gates, test suite or original downloadable ZIP, add a sampler, or establish a new benchmark result. Stochastic realization describes the existing generative approach, not a missing feature or a new algorithm. The archived 47-test result remains historical evidence for the tested v3.4 snapshot.

## License and publication status

No license was present in the supplied v3.4 artifact, and this preparation step does not assign one. The maintainer must choose a license before this project is described as licensed open source. The source is publicly available in this repository. A release tag is not created by this publication. Historical test evidence and current GitHub Actions results must be interpreted separately.
