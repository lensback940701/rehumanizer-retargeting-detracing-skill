# Rehumanizer · Retargeting · Detracing (RRD)

**Keep the idea ambitious. Make scholarly voice measurable. Sharpen the work while it is being built.**

[简体中文](README.zh-CN.md) · [Original v3.4 snapshot](downloads/rrd-v3.4-skill.zip) · [Skill specification](SKILL.md) · [Development record](docs/review-20261005/DEVELOPMENT_TEST_LOG.en.md) · [Known limitations](docs/KNOWN_LIMITATIONS.md)

<p align="center"><img src="docs/images/hero-cyber.png" width="560" alt="A human researcher and a holographic digital twin converge around evidence and a redirected research target." /></p>

RRD is a reusable, two-stage academic sharpening skill for manuscripts in progress. It preserves the ambition of the idea, makes selected dimensions of human scholarly voice measurable, and restores focus, material force and narrative clarity whenever an existing draft or section needs them. It is not a finalization or closure skill, an AI-detection evasion tool, or a replacement for author judgment.

**Version:** v3.4 · **Use:** supervised working baseline · **Acceptance hardening:** pending · **License:** maintainer decision pending; no license has been assigned.

## Three defining commitments

### 1. Ambition first: end the soften-restore-soften loop

**Preserving the idea's scholarly ambition is the highest editorial principle.** RRD is not another cycle of adding cautions and then removing them. It puts the research target above generic style rules, retires inherited constraints that diluted the contribution, and places the burden of proof on any new weakening. Once the author has agreed a supportable target, later checks do not reopen it merely to sound safer: a change needs new evidence or a new author decision.

The aim is to keep the strongest worthwhile argument the evidence supports, not to manufacture certainty. Facts, accurate quotation and genuine counter-evidence remain boundaries; they are not excuses for routine precautionary retreat.

### 2. Human scholarly voice made measurable, with room for variation

Instead of requesting vaguely more human prose, RRD translates selected dimensions into **inspectable, quantitative proxies**:

| Dimension | Existing measurements and checks |
| --- | --- |
| Sentence rhythm | Sentence-length mean, standard deviation and coefficient of variation; short-sentence share and staccato runs |
| Material presence | Quotation and number densities, sourced-quotation records, and attribution load |
| Authorial presence | Explicit stance cues and actor-code signals, interpreted alongside a qualitative reading of situated actors |
| Argumentative continuity | Adjacent-sentence topic linkage and relation-marker signals |
| Template pressure | Repeated paragraph openings, stock conversion frames, relation-verb tics and spreading non-core labels |

**Human-voice indicators are observable statistics, not prescribed output quantities.** RRD does not tell the writer to insert exactly three quotations, use a transition every two sentences, or hit a fixed stance density. It leaves their realization to the model's context-sensitive, potentially variable generation, then measures what actually appeared. The observed counts and distributions may differ across passages and runs; they are not targets sampled or allocated in advance.

**Measurable diagnostics; stochastic realization; no fixed quotas.** The generative process supplies the variation; the skill supplies the research priorities, source boundaries, reference-relative diagnostics and interpretive review. No separate random sampler is required by this design. Compare the resulting signals with the author's reference writing, and investigate warnings in context. Repair broken argument, flattened material or monotonous prose—not a count merely because it differs from a reference. Quantification makes selected features inspectable without prescribing a single template for human voice.

Variation applies to expression; the agreed research target and fidelity to the sources remain fixed.

### 3. A tool for work in progress, not a finalization skill

Use RRD whenever an existing draft or section needs reinforcement: after the idea has been diluted, when material has become detached from the argument, when prose has become mechanical, or when a new insight requires retargeting. A whole paper is not a prerequisite for a scoped invocation; sufficient inspectable text and accessible support are.

Each invocation keeps the **read-only diagnosis → author authorization → scoped revision** structure. Its output is a stronger working checkpoint that returns to research and writing. It does not close the project, certify submission readiness or automatically hand control to final polish. Reuse is available throughout development, not a requirement to keep revising an unchanged manuscript.

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
docs/images/             Six README illustrations
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
