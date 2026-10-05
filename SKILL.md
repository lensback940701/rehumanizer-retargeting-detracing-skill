---
name: rehumanizer-retargeting-detracing-skill
description: "Two-stage route correction for a complete academic manuscript that drifted during repeated revision: the original research target was lost or diluted, the contribution became cheap, the prose reads mechanical, disconnected or over-defensive, sections lack lead-ins, and workflow traces leaked into the text. Stage 1 (this invocation) diagnoses read-only, recovers the best supportable target from early artifacts and raw sources, audits inherited rule debt, confirms the route with the author, and writes a Goal plus a short launch prompt. Stage 2 runs in a new conversation under that Goal and rewrites at the chosen intensity, then verifies the final file. Sits before hq-final-polish-harness. Not for first drafts, local hedging fixes (press-conference-revision), final polish or word fitting, literature search, or submission."
---

# Rehumanizer · Retargeting · Detracing (RRD) — v3.4

A route-correction stage for manuscripts that have become *correct but lifeless*:
a strong idea, a reasonable first draft, then rounds of audit-driven revision,
each adding locks and caveats, until the paper argues nothing it could lose,
no person can be seen in it, its sentences no longer connect, and its
sections no longer lead the reader in or tell the eye where to look.

RRD does three things, in this order:

1. **Retarget**: recover the research claim that is both most valuable and
   best supported by the material. That is not necessarily the earliest,
   boldest or most general version. Re-anchor the paper on it.
2. **Rehumanize**: return to raw sources to restore people, situations, voices,
   numbers, turning points, the author's stance, prose whose sentences carry
   the reader from one step to the next, and sections that lead the reader in
   and guide the eye when the focus moves (07, 08).
3. **Detrace**: remove workflow residue, template paragraphs, strawman
   negations and caveat scatter, and retire the rule debt that produced them,
   without creating a new template in their place.

## Position among sibling skills

| | press-conference-revision | **RRD** | hq-final-polish-harness |
| --- | --- | --- | --- |
| when | any writing step | once, when a mature draft has drifted | once, at the end |
| unit | sentence/paragraph rhetoric | route: target, spine, section jobs, voice, flow | form, wording, word band, dual copies |
| claim rule | same or narrower | **best supportable** (may restore claims dropped without evidentiary reason; never raised for its own sake) | same or narrower than the RRD output |
| sources | the manuscript | manuscript **plus raw sources and origin artifacts** | admitted evidence |
| locks | respects all | **audits and retires inherited style/process locks** (never ethics, facts, source protection) | respects RRD's route contract |

Do not import final polish's no-net-word-loss rule, citation-PDF lane or
submission checklist. If the only problem is local hedging, use
press-conference-revision and say so.

## Integrity firewall (both stages)

- No invented facts, quotations, numbers, events, motives, feelings, outcomes,
  causal links or literature positions; restored detail comes from a located
  source passage. Quotations are verbatim (fillers may be cut with an ellipsis).
- Anonymization, consent, privacy and ethics locks always stand.
- The adversary is a position that exists in the cited literature or a
  documented common assumption, engaged as something to extend or correct.
- A claim is strengthened only as far as the located evidence supports; each
  strengthened claim records its support in the route contract.
- Genuine scope conditions, contradictions, negative cases and rival
  explanations stay, stated where they do analytic work.

The firewall forbids fabrication and overclaiming. It does not license
precautionary weakening (`references/04-anti-defense-charter.md`).

## Stage 1: diagnose, retarget, hand off (this conversation)

Read-only toward the manuscript; ends with a Goal and a launch prompt.

### S1.0 Intake

Identify, asking only for what cannot be found: `BASELINE`; `PROJECT_ROOT`;
`RAW_SOURCE_ROOTS`; `ORIGIN_ARTIFACTS` (proposals, outlines, early abstracts,
first drafts, memos, conversation logs); `VOICE_REFERENCES` (the author's
published papers; otherwise papers the author names as models);
`PRIOR_CONTROL_FILES` (earlier Goals, prompts, style cards, audits; for
human-revised papers, reviewer and co-author comments); `TARGET_JOURNAL`,
length limit; `PAPER_TYPE`; sibling papers from the same dataset.

`CONTEXT_SOURCES`: where macro and regional facts for the case chapter's
lead-in may come from (cited literature, official statistics, policy
documents, the author's published papers). Ask the author if none are found.

**Second Stage 1 on an RRD output.** When the baseline is itself a
route-corrected draft:
- re-score from scratch rather than carrying over the old symptoms;
- expect new problems (over-tidy logic, flat sections), not the old ones;
- read authority in this order: the user's current instruction → the latest
  author answers (`author_queries` / decisions) → earlier Stage 1 decisions →
  earlier Goals;
- do not re-ask decided questions.

Inputs and their consequences:

- **Missing origin artifacts** → use the earliest draft or ask the author for a
  five-sentence seminar pitch.
- **No extra raw sources but the argument is checkable from the manuscript**
  (theory, review) → continue; rehumanizing is limited to exemplars, stance and
  flow; record `RAW_SOURCES: none`.
- **The evidence for the core claim is inaccessible** → `HOLD_INPUTS`.
- **PDF inputs** → convert to Markdown first (e.g., an OCR skill); scanners read
  .md/.txt/.docx (PDF only with pypdf and a reliability warning).
- **Quantitative work** → raw sources are analysis outputs. Stage 2 may restate
  reported estimates in meaningful units by arithmetic shown in the route memo;
  it never re-runs analyses.

### S1.1 Symptom scan

```text
python <SKILL_ROOT>/scripts/trace_scan.py <file> --out-json <out>.json --out-md <out>.md
python <SKILL_ROOT>/scripts/target_drift_timeline.py --root <PROJECT_ROOT> --scan-manuscripts --out-md <HANDOFF_DIR>/target_drift_timeline.md [--file-list <whitelist.csv>]
```

Scan the baseline and each voice reference. Read the baseline in full. Score
the nine symptom dimensions in `references/01-retargeting.md` with excerpts,
including S8 disconnected prose and S9 flat section architecture (cold
context chapter, missing case-selection logic, thesis-first empirical
openers, unguided focus shifts). Name the round where the target or the
material was lost. The timeline orders files by dates written in their names
when present; mtime is a weak fallback. Confirm the version history with the
author when it matters.

### S1.2 Target recovery

Read origin artifacts in full. Build the Target Drift Ledger: each retreat is
classified `EVIDENCE_FORCED`, `SCOPE_SHARPENED` (both kept), `RULE_FORCED`,
`ANXIETY_FORCED`, `DILUTED`, `SUBSTITUTED` or `LOST_IN_PIPELINE`. Spot-check 3–8
source passages: this supports a provisional judgment only; Stage 2 rechecks
the target after full reading. Draft 1–3 two-layer Recovered Target Statements
(theoretical target + empirical mechanisms; `references/01-retargeting.md`).
Rank them by value × support, not by height. Apply the outcome test and the
baseline-echo test (01) before ranking. When siblings share the dataset,
check quotation overlap (`sibling_overlap_check.py`) and read the siblings'
claims for finding-level overlap.

### S1.3 Rule-debt audit

```text
python <SKILL_ROOT>/scripts/rule_debt_extract.py <PRIOR_CONTROL_FILES...> --out-csv <HANDOFF_DIR>/rule_debt_register.csv --out-md <HANDOFF_DIR>/rule_debt_summary.md
```

Classify `RETAIN` (ethics, privacy, fact integrity, source protection, verified
author decisions, active R&R commitments), `RELAX`, `RETIRE`, or
`CONVERT_TO_POSITIVE_GOAL`. Skip with a note when no prior constraints exist.

### S1.4 Author gate (one question round)

Ask only what changes Stage 2:

1. which target, or an edited version;
2. which locks to retire or relax (short list);
3. rewrite intensity `R1`/`R2`/`R3` (`references/05-structural-repairs.md`).
   R1 may rewrite every sentence, reorder material inside sections and replace
   material with stronger located material from the bank, but it never
   changes claims or section structure;
4. author-only facts (pseudonyms, sibling use of quotes).

If unanswered, write `PROVISIONAL_TARGET` and make Stage 2 stop after P1.
When the user supplies a written answers file (e.g., a benchmark's frozen
author answers), that file is the author's answer: use it, do not wait, and
record anything it does not cover in `author_queries`.

When the user restricts readable inputs to a list, that list is authoritative
for every script call (`--file-list` for the timeline; explicit file arguments
for the other scripts).

### S1.5 Emit the handoff

Into `<HANDOFF_DIR>`:
- `GOAL.md` from `assets/templates/GOAL_ROUTE_CORRECTION.md`, in the author's
  working language. It should be shorter than the previous Goal, with fewer
  prohibitions; spend its length on the target, locators and section jobs.
- `SHORT_LAUNCH_PROMPT.md`.
- `stage1_diagnosis.md`.
- the ledgers and scans.
- `gate_config.json`, copied from the default and adjusted only with the author.

Then give the user the target in one sentence, the retired locks, the folder
and the prompt.

## Stage 2: route correction (new conversation, under the Goal)

The Goal carries the procedure; its steps branch by intensity:

| phase | R1 re-route | R2 section rebuild | R3 full rewrite |
| --- | --- | --- | --- |
| P1 route contract | yes | yes | yes |
| P2 material bank | for passages to rewrite | for the empirical core | whole paper |
| P2b target recheck | yes | yes | yes |
| P3 spine | section openings + discussion | empirical core + frame | new outline |
| P4 rewrite scope | abstract, intro, section openings, discussion, conclusion, weakest passages | P4(R1) + empirical core + theory | everything |

- **P0 Freeze**: read the Goal before any other start-up action; do not use
  assistant memory, chat history or files outside the Goal's inputs as a source
  of facts. Hash inputs into `source_manifest.csv` (path,sha256); copy the
  baseline.
- **P1 Route contract**: target, claim table, adversary, section jobs, retained
  locks. Source IDs from Stage 1 may stand provisionally until P2 assigns bank
  IDs.
- **P2 Living material bank + material upgrade**: verbatim quotes, numbers,
  turning points, dilemmas, contradictions, counter-voices, with locators. For
  every claim, search the raw sources for material stronger than what the
  baseline uses and record the decision (keep / replace / add) in
  `registers/material_upgrade.csv`. Keeping only the baseline's material is a
  decision that needs a reason (W14 flags it).
- **P2b Target recheck (once)**: after full reading, look for the strongest
  counter-evidence. Keep, narrow or reshape the target, and record why. If
  the evidence cannot carry any version, stop with `HOLD_TARGET_EXCEEDS_EVIDENCE`
  and the best supportable alternative.
- **P3 Spine + section architecture map**: one claim per section, its strongest
  material, where the counter-case sits. Then, per section: entry move, where
  the claim surfaces, focus path with the bridge reason for each move, guide
  thread, exit (`references/08-narrative-architecture.md`). The case chapter
  gets its context ladder and case-selection argument here.
- **P4 Rewrite**: material and argument first, then architecture and flow.
  Write from the map, in connected prose (`references/07`, `08`); verify after.
- **P5 Gates**: `trace_scan.py`, `defense_gate.py` (with `--route-memo` and the
  route contract's concept terms as `--core-term`), and
  `sibling_overlap_check.py` when siblings exist. Fix FAILs by rewriting or by
  specific register/memo entries. Warnings are read in context.
- **P6 Verify after writing**: one pass over quotes, numbers, dates,
  attributions and citation roles; repair at the evidence level.
- **P7 Cold, architecture and flow reads**: the cold-read questions (02), the
  architecture read of openings, paragraph first sentences and endings (08),
  then the flow read of every paragraph (07); repair.
- **P8 Final binding**: after the last change and the md/docx export, re-run
  the gates on the final file. Then run
  `final_check.py --manuscript <final.docx> --manuscript <final.md> --gate-json <docx gate> --gate-json <md gate> --overlap-json ... [--semantic-review qa/sibling_semantic_review.md] --result-json rrd_result.json --write-result --source-manifest source_manifest.csv`
  (`--write-result` fills `final_hashes` and `sources_unchanged`; never type them by hand).
  The delivered file, the reports and `rrd_result.json` must carry the same
  hash. Deliver and stop.

Required references for Stage 2: 01–05, 07 and 08 in full, plus the matching
section of 06.

## Controls (summary; full text in references/04)

Hard checks in `defense_gate.py` (exit 2):
- `G0` unreadable/truncated input or malformed register;
- `G1` workflow traces in prose;
- `G2` new hedge/negation/hedged-finding cues, diffed against the matching
  baseline sentence, that are not registered with a source locator and a
  reader-specific reason;
- `G6` sourced quotations removed without an account in the route memo.

Densities are **warnings, not quotas**:
- negation, closers, material density;
- `W8` cohesion: topic linkage, sentence length, staccato runs,
  source-parenthesis clutter;
- `W13` section architecture: cold openers in empirical/context sections,
  unguided focus shifts, missing case-selection logic;
- `W14` material renewal: no sourced quotation added or upgraded;
- `W15` conversion-frame template: "使X成为Y" sentences far above references;
- `W16` relation-verb tic: placeholder link verbs (进入/接入/参与构成) or chained
  由此/因此 far above references, including a habit inherited from the baseline;
- `W17` tag word: a non-core word now in a large share of paragraphs, far more
  than in the baseline (the usual way a suppressed template comes back);
- actor codes, stance, caveat budget, literature chains, voice drift.

A registered caution is exempt from every count it appears in.

`final_check.py` binds deliverables to reports. `sibling_overlap_check.py` exits:
- 0: no match;
- 2: matches;
- 3: semantic review needed;
- 1: incomplete.

Enforced by the Goal:
- uncertainty → author query, never silent weakening;
- no new prohibitions mid-run;
- a PASS never replaces the cold and flow reads;
- never edit `gate_config.json` to pass.

## Status values

Stage 1:
- `HANDOFF_READY`
- `HANDOFF_READY_PROVISIONAL_TARGET`
- `HOLD_INPUTS` (core evidence inaccessible or no baseline)
- `NOT_RRD_CASE`

Stage 2 completion (work done):
- `ROUTE_CORRECTED_READY_FOR_FINAL_POLISH`
- `ROUTE_CORRECTED_WITH_AUTHOR_QUERIES`

Stage 2 halts (work paused, not success):
- `HOLD_TARGET_UNCONFIRMED`
- `HOLD_SOURCE_ACCESS`
- `HOLD_TARGET_EXCEEDS_EVIDENCE`
- `HOLD_DEFENSE_GATE`
- `HOLD_FINAL_BINDING`

## Resources

- `references/01-retargeting.md`: symptoms, drift taxonomy, two-layer target, claim table, rule debt
- `references/02-rehumanizing.md`: living material, actors, stance, section moves, cold read
- `references/03-detracing.md`: trace taxonomy T1–T15
- `references/04-anti-defense-charter.md`: rules, register, hard vs warning checks
- `references/05-structural-repairs.md`: literature as debate, framework as structure, R1/R2/R3, siblings
- `references/06-field-adapters.md`: by paper type and language
- `references/07-cohesion-and-flow.md`: how sentences and paragraphs hand the argument on
- `references/08-narrative-architecture.md`: context ladder, case selection, section entries, unfolding, guiding the eye, section map
- `assets/templates/`: Goal, prompt, diagnosis, contract, ledgers, registers, config, handoff, result
- `scripts/`: `trace_scan.py`, `defense_gate.py`, `final_check.py`, `sibling_overlap_check.py`, `target_drift_timeline.py`, `rule_debt_extract.py`
- tests in `tests/`
