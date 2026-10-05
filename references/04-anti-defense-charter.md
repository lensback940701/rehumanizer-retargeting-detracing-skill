# 04 Anti-Defense Charter

Agents revising academic text drift toward defence: when unsure, they add a
caveat, soften a verb, or delete. Each move is locally "safe"; together they
erase the paper. This charter makes the cost of defence explicit and puts the
burden of proof on every new caution instead of on every claim.

The charter does not weaken the integrity firewall in `SKILL.md`. Fabrication
and overclaiming remain forbidden. What the charter forbids is *precautionary
weakening without a located reason*.

## Hard rules

**H1 Burden of proof on caution.** A new hedge, negation-defence or softened
verb must name the specific evidence that requires it (source locator) and what
a reader would misread without it. "To be safe", "for rigour", "a reviewer
might object" are not reasons. Code-enforced (G2, register hygiene).

**H2 Evidence ceiling, not baseline ceiling.** Claims are written at the level
the located evidence supports (claim table, 01). Keeping a claim below that
level needs an evidential reason recorded in the route contract.

**H3 Uncertainty goes to the author, not into the prose.** When the executor is
unsure whether a claim holds, it checks the source; if still unsure, it writes
the strongest supportable version and logs an author query. It never resolves
doubt by silent deletion or by stacking hedges.

**H4 Name the opponent or drop the negation.** "Rather than X" needs X to be a
view someone holds (citation or explicit position) within the same sentence or
paragraph. Otherwise rewrite as a positive claim. Signalled by W4; a new
unanchored negation is caught by G2.

**H5a Densities are alarms, not quotas.** Counts of negations, closers,
quotes or numbers show where to look. Deleting a necessary distinction or
inserting material to move a number is a regression, even when the number
improves. Swapping a flagged pattern for its neighbour (使X成为Y → X进入Y) is
the same regression: the habit, not the word, is what the warning measures.
W17 watches for this generically: a non-core word that spreads into half the
paragraphs is usually the new tag.

**H5 Caveat budget.** General limitations (sample, self-report, single region,
no outcome measurement) appear once in methods and at most once in the
discussion's limits paragraph. Empirical paragraphs carry only claim-specific
status markers. Code-signalled (W4).

**H6 Standing claims.** Every major section contains at least one claim
sentence that is not qualified inside the same sentence. The abstract states
findings with finding verbs, not "is related to"; a new hedged finding
anywhere (flagged with [ABSTRACT/CONCLUSION] when it sits there) needs a
register entry under G2. A registered association stays: it is the correct
verb when the evidence is associational.

**H7 No workflow language in prose.** Verification notes, ledger terms and
prompt echoes live in control files only. Code-enforced (G1).

**H8 Living material is protected.** Route correction may replace a quote or a
number with a better one; a sourced quotation that disappears is accounted
for in the route memo (G6). Density is a warning (W6), not a target.

**H9 No rule creep.** The Stage 2 executor may not create new prohibitions,
locks, budgets or templates beyond the Goal. A felt need for a new rule is
written as an author query. Inherited rules not listed as retained in the Goal
are void.

**H10 Write first, verify after.** Drafting is not interrupted by per-sentence
verification. P6 verifies every fact once against the material bank and the
sources. A failed check is repaired at the evidence level (find the right
passage, correct the fact); it is not a reason to genericize the paragraph.

**H11 Counts are floors and alarms, not targets.** The gate prevents
regression; it does not define quality. A PASS never replaces the cold read;
a FAIL is fixed by rewriting, never by editing `gate_config.json`, never by
deleting living material, and never by moving defensive sentences into notes.

**H12 Deletion is not neutral.** Cutting a sourced quote, number, actor, event,
contradiction or rival explanation is a substantive change that must be logged
with its reason in the route memo. Cutting rhetoric, echoes and traces is
expected and needs no justification.

## The added-caution register

`added_caution_register.csv` (template in `assets/templates/`) holds every
caution the executor *adds* or *keeps in a new sentence*:

| column | requirement |
| --- | --- |
| `sentence_excerpt` | ≥8 characters copied from the sentence (normalized match) |
| `cue_type` | `HEDGE`, `NEGATION`, `HEDGED_FINDING`, or `PROCESS_TRACE_KEEP` |
| `evidence_locator` | source ID + page/paragraph/timestamp/table that requires the caution |
| `why_reader_needs_it` | what the reader would wrongly conclude without it (≥12 characters; generic precaution phrases are rejected by the script) |
| `section` | where it sits |

Rows failing these checks are ignored and reported as G0 failures.

False positives: a scanner cue can be a legitimate term of art (e.g., a field
term that happens to match a workflow word). Register it as
`PROCESS_TRACE_KEEP` with `evidence_locator` = `term-of-art` and a reason
naming the concept. Trace cues inside a methods section are reported as a
warning (W7), not a failure, because method facts such as member checking
belong there; still delete handling notes that do not help a reader judge
the evidence.

## Which checks block and which only warn

| check | type | what it means |
| --- | --- | --- |
| G0 input / register | hard | revision readable and complete; register rows well formed (enumerated cue type, resolvable locator, specific reason) |
| G1 trace | hard | workflow/audit language in prose (verification facts inside methods: warning W7) |
| G2 new cues | hard | a hedge, negation-defence or hedged finding that is new relative to the matching baseline sentence, unregistered |
| G6 loss | hard with memo | a sourced quotation removed without an account in the route memo |
| W1–W16 | warning | densities, cohesion, stance, caveat budget, literature chains, voice drift, section architecture (W13), material renewal (W14), conversion-frame template (W15), placeholder relation verbs and chained inferential connectives (W16), tag-word spread (W17) |

A registered caution is exempt from every count it appears in; it cannot pass
G2 and then be failed by a density elsewhere.

## Running the gate

```text
python <SKILL_ROOT>/scripts/defense_gate.py \
  --baseline <BASELINE copy> --revised <revised.md|docx> \
  --reference <author published paper 1> [--reference ...] \
  --register <OUTPUT_ROOT>/registers/added_caution_register.csv \
  --route-memo <OUTPUT_ROOT>/route_memo.md \
  --config <HANDOFF_DIR>/gate_config.json --paper-type <type> \
  --out-json <OUTPUT_ROOT>/qa/defense_gate.json --out-md <OUTPUT_ROOT>/qa/defense_gate.md
```

Exit code 2 means FAIL. Repair loop: at most three gate runs; if a FAIL
persists because the evidence genuinely requires the caution, register it with
its locator. If the conflict is about the target itself, stop with
`HOLD_DEFENSE_GATE` and explain.

## Interpreting signals

- Reference-relative beats absolute: a paper in a hedging-heavy field may
  legitimately sit above another field's levels. The gate therefore compares
  with the baseline and the voice references, not with universal thresholds.
- Merged-paragraph warnings (PDF-derived references) make paragraph-level
  signals unreliable; use per-1000 densities only.
- Quantity signals do not measure quality. Quote density can be normal while
  the quotes are the safe half of what was said; abstract-term and actor-code
  densities vary by field (some published case studies in the same journal
  exceed a drifted draft). Treat them as context, and judge quote strength,
  grammatical role of actor codes and abstraction in the cold read.
- A high count of retained, registered cautions is acceptable when each row is
  specific. A low count is not a success if the cold read finds the paper
  still argues nothing.
