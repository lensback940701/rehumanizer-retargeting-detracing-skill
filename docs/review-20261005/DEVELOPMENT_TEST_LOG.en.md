# RRD v3.4 — Development and Regression Test Record

**Record date:** 2026-10-05  
**Project:** Rehumanizer · Retargeting · Detracing (RRD)  
**Artifact reviewed:** `rehumanizer-retargeting-detracing-skill_v3.4_20261004.zip`  
**In-package version:** v3.4  
**Current disposition:** Retain the developer-selected 42-point checkpoint; acceptance hardening remains open.

> Evidence provenance: developer-reported manuscript evaluations, statically inspected implementation changes, and independently executed script tests are recorded separately. None is presented as a substitute for the others. Unavailable metadata is not inferred.

## 1. Development objective

RRD targets complete academic manuscripts whose research focus, contribution, empirical material, or prose has deteriorated through repeated revision. Its objective is not stronger wording or lower hedge counts. It is to recover the most valuable claim that the evidence can support, then improve material selection, authorial stance, paragraph cohesion, and section development.

The workflow retains two stages: read-only diagnosis and author confirmation in Stage 1, followed by source rereading, target revalidation, intensity-specific revision, evidence verification, and final-artifact binding in Stage 2. Route correction does not relax factual, source-protection, anonymity, or ethical requirements.

## 2. Changes relative to the package reviewed on 2026-10-03

| Area | Current implementation | Verification |
| --- | --- | --- |
| Target recovery | Replaces a single claim-height hierarchy with the best-supportable-claim principle; records claim type, scope, and support; revalidates the target after source rereading | Static review |
| Narrative repair | Adds cohesion and section-architecture references covering entry moves, focus shifts, guide threads, and section handoffs | Static review and associated script tests |
| Material renewal | Adds `material_upgrade.csv` to account for retained, replaced, and newly incorporated material | Static review and W14 test |
| Template migration | Adds or refines warnings for conversion frames, placeholder relation verbs, inferential connectives, and non-core tag-word spread (W15–W17) | Static review and synthetic tests |
| Gate behavior | Diffs new cues against corresponding baseline sentences; treats densities as warnings; improves empty-input, quotation-span, bibliography, and reader-consistency handling | Packaged regression tests |
| Delivery binding | Adds `final_check.py` to check manuscript hashes, gate reports, source manifests, and result records after final revision and export | Packaged tests and independent contract probes |

This is a comparison against the 2026-10-03 artifact, not a reconstructed commit history. Individual changes are not assigned to the 39-, 41-, 42-, or 37-point checkpoints because the intermediate artifacts were not supplied.

## 3. Single-manuscript iterative evaluation — developer reported

**Evaluation fixture:** The same manuscript.  
**Evaluation unit:** Revised manuscript outputs associated with successive development checkpoints.  
**Evidence source:** The developer's reported score sequence and rollback decision in the current conversation.

| Evaluation ID | Reported score | Change from preceding record | Disposition |
| --- | ---: | ---: | --- |
| B01 | 39 | — | First reported checkpoint evaluation |
| B02 | 41 | +2 | Higher observed score |
| B03 | 42 | +1 | Highest observed score in the reported sequence; rollback target |
| B04 | 37 | −5 | Observed score regression; not retained as the active checkpoint |

B01–B04 are record-local sequence identifiers, not Git commits or semantic versions. The association between the supplied v3.4 package and the selected 42-point checkpoint is developer reported; historical artifact hashes were unavailable for an independent byte-level comparison. The description of the selected version as scoring 42 is not counted as a fifth independent evaluation after rollback.

### Rollback decision

Following the five-point decline from B03 to B04, the developer reverted to B03 as the working baseline. This is recorded as **checkpoint selection and rollback in response to an observed regression**, rather than an assumption that later revisions are necessarily better.

The reported sequence supports a bounded finding: the 42-point checkpoint outscored the subsequent 37-point checkpoint on the reported single-manuscript evaluation and was therefore retained. It does not establish a stable repeated-run score, statistical significance, or equivalent gains on unseen manuscripts. The three-point difference between 39 and 42 compares candidate checkpoints; it is not a measured improvement over an untreated manuscript.

### Evaluation metadata not supplied

The scoring rubric and maximum score, dimension-level scores, untreated-manuscript score, evaluator identity and version, generation model and parameters, per-run input/output hashes, repeat counts, input-reset procedure, and blinding/randomization procedure were not provided. No percentage conversion, stable mean score, success rate, or significance test is reported.

The package's S1–S9 symptom profile uses 0–3 ratings. It is not identified as the quality rubric underlying the reported score of 42, and the two are not conflated.

## 4. Independent engineering verification — 2026-10-05

**Environment:** Python 3.13.5 on Linux x86_64; full environment details are recorded in `evidence/environment_and_metadata.json`.  
**Scope:** Package scripts and synthetic fixtures. No language model was invoked to produce a new revision of a real manuscript, and the developer's local Stage 1→Stage 2 workflow was not executed.

| Test group | Executed | Passed | Skipped |
| --- | ---: | ---: | ---: |
| ScanTests + ToolTests | 14 | 14 | 0 |
| GateTests | 13 | 13 | 0 |
| V3Tests + V31Tests + V32Tests | 11 | 11 | 0 |
| V33Tests + V34Tests | 9 | 9 | 0 |
| Total | **47** | **47** | **0** |

The package contains regression coverage corresponding to the 13 issue categories from the previous review; R03 and R11 are covered within one test method. These results confirm the encoded scenarios, not the absence of every related failure mode. After two monolithic invocations exceeded the tool execution window, the suite was completed in four groups. Incomplete invocations were not counted as completed tests.

Static checks found an 830-character `description` and a 296-line `SKILL.md`, with the declared name matching the directory. The description satisfies the current Agent Skills limit of 1,024 characters. All Python source files parsed successfully, and the reviewed source files were unchanged. This is not a client installation test.

## 5. Additional boundary and interface checks

Eleven isolated interface calls were executed. Six positive controls met their respective expectations; five negative scenarios exposed the validation gaps below. One additional result-schema inconsistency was observed. Inputs were synthetic; final-binding probes used minimal gate-report fixtures to isolate interface behavior. These are not manuscript-quality evaluations.

| ID | Observed behavior | Required hardening |
| --- | --- | --- |
| A01 | Two final files with a gate report for only one file still produce a final-check PASS | Require report coverage of every supplied final artifact, not merely a match for each report |
| A02 | A header-only source manifest yields `sources_unchanged=true` | Validate manifest population, schema, and coverage of required frozen inputs |
| A03 | An undefined nonempty workflow status is accepted | Validate the status enum and distinguish binding status from release readiness |
| A04 | Registering HEDGE authorizes a sentence that also adds an unregistered NEGATION | Require a matching registration for each newly added cue type |
| A05 | An explicitly requested missing configuration silently falls back to built-in defaults | Fail explicitly rather than substituting configuration |
| A06 | `rrd_result.final_check` changes from a template object to a string | Preserve a stable JSON schema containing `overall` and `report` |

A03 is a state-interface hardening requirement. A valid halted workflow can have a successful file-binding check without being complete; binding PASS must not be treated as release approval. A01–A06 are not asserted to explain the 37-point output. No evidence connecting these findings to that score was supplied.

## 6. Assessment and version disposition

**Packaged test status:** `PACKAGED_TESTS_PASS`.  
**Manuscript-evaluation disposition:** `BENCHMARK_SELECTED_CHECKPOINT`, retaining the developer-reported 42-point version.  
**Acceptance-interface status:** `HARDENING_PENDING`.  
**Independent end-to-end quality reproduction:** `NOT_INDEPENDENTLY_REPRODUCED`.

The current design and covered script behaviors show substantive improvement over the initially reviewed package. The artifact is a reasonable baseline for further supervised use, but the available evidence does not justify an unattended, cross-manuscript stable-release designation.

Engineering fixes should be separated from writing-policy experiments. Freeze the selected checkpoint's writing instructions, address A01–A06 on a narrowly scoped hardening branch, and add regression cases. Do not mix attempts to raise manuscript scores into the same patch, so that behavior changes remain attributable.

## 7. Planned validation — not yet executed

Repeat runs using frozen inputs, a fixed rubric, and fully recorded model settings. Evaluate transfer on held-out manuscripts that did not drive rule changes. Compare candidate outputs in blinded pairs while independently checking evidence accuracy. Quality scores and factual integrity should be separate acceptance dimensions; a high aggregate score must not offset factual or anonymity violations.

## 8. Artifact identity and evidence index

SHA-256 of the reviewed ZIP:

```text
e700905b50a965377fea54e851cac721c4cbea2436a8f0acab8538fcd6402c2b
```

`evidence/test_summary.json` summarizes the 47 packaged tests; the four `tests_*.log` files retain individual outcomes. `evidence/contract_probes/summary.json` and its case directories retain interface observations. `evidence/probe_v34.py` regenerates the synthetic fixtures and probe results. Source locations and further analysis are provided in `REVIEW.zh-CN.md`.

Specification and evaluation-method references are listed in `REFERENCE_NOTES.md`. This review did not modify the skill, execute a rollback, or present the developer-reported score of 42 as an independently reproduced score.
