# 03 Detracing: remove the fingerprints of the workflow

A manuscript revised through many audited rounds absorbs the language of its
own process: verification notes, ledger vocabulary, template paragraphs and
reflexive disclaimers. Readers experience this as stiffness even when they
cannot name it. Detracing removes the residue while keeping every real
source-status distinction.

Scanner families in `scripts/trace_scan.py` map to the codes below. A scanner
hit is a pointer; decide in context.

## Trace taxonomy

| code | trace | zh cues (examples) | en cues (examples) | repair move |
| --- | --- | --- | --- | --- |
| T1 | Audit metadiscourse: the text reports how a source was checked or ordered | 据受访者介绍整理；事件顺序依其明确叙述整理；主观判断随其表达者呈现；经核对 | as recorded in the transcript; according to the source file; not independently verified | Delete from prose. If a source-status distinction matters (reported vs observed), express it once through the verb ("she recalled", "the plan stated") or in methods. |
| T2 | Workflow vocabulary | 证据上限、锚点、台账、准入、保护项、基线稿、回指 | claim ceiling, evidence anchor, ledger, protected baseline, pass | Delete; these words belong to the control files. |
| T3 | Echo ending | paragraph ends by restating its previous sentence | — | Cut, or replace with the next analytic step (consequence, contrast, link to the claim). |
| T4 | Strawman negation | 而非……；不能仅……；并不意味着……；不只是…… with no named view | rather than; not merely; should not be read as | Name the view being corrected (citation or explicit position) or state the claim positively. |
| T5 | Caveat scatter | the same general limitation repeated in empirical paragraphs (样本有限、仅为受访者自述、不作效果认定) | "this is based on self-report", repeated | State once in methods or the limits paragraph; keep only claim-specific status markers in the findings. |
| T6 | Code personae | 受访者（R2）认为……这位受访者……该负责人（C1）…… | Respondent R7 noted… | Situated role introduction once; stable descriptor afterwards; codes in citation parentheses. |
| T7 | Abstract-noun fog | 条件、安排、关系、环节、范围、进入、组织、实施 stacked | conditions, arrangements, dynamics, configurations | Replace with actor + verb + object; name the actual thing (price, labour, rainfall, contract). |
| T8 | Literature chain | X研究强调…[1]；Y研究关注…[2]；Z研究说明…[3] | Smith (2019) argues…; Jones (2020) highlights… | Rebuild as a debate (see 05). Cut citations with no argumentative job. |
| T9 | Template uniformity | every paragraph: claim → quote → generic wrap-up; every section same length and shape | same | Vary paragraph jobs; let some paragraphs be all material, some all argument; vary length. |
| T10 | Instruction echo | prose repeats the wording of the Goal or prompt ("恢复情境""具有解释用途""人物处境") | "to restore context", "for explanatory purposes" | Delete the echo; show the thing instead. |
| T11 | Hedged finding verb | 与……有关；可能影响；存在一定联系 for the paper's own core claims | is related to; may shape; some association | Use the verb the evidence supports (claim table, 01); if support is truly weak, say what is uncertain and why, once. |
| T12 | Safe generic substitution | 相关项目、有关部门、某些环节、一定条件 replacing a specific term | relevant actors, certain conditions | Restore the specific term from the sources. |
| T13 | Source-first narration | 访谈显示…；材料表明…；受访者介绍… as the sentence subject, repeatedly | the interviews show…; respondents reported… | Make the actor or the phenomenon the subject; keep the citation in parentheses. |

| T14 | Staccato or aphoristic prose (a new template) | short declaratives in a row; closers such as “X没有变，变的是Y”, “它挑地，也挑人”; paragraph openers “……也……” repeated | "Control changes shape." as a closer; one-clause sentence chains | Re-link sentences (given → new), state the relation, end on the consequence; see 07. |
| T17 | Placeholder relation verbs | the mechanism told through 进入/接入/纳入/相接/连接/嵌入/参与构成 (政策进入社区；资金接入项目；居民参与构成治理), often chained with 由此/因此 | `X enters / is integrated into / feeds into Y`, `helps constitute` | Name the act and its actor: who did what to which thing, when and with what (the clerk copied the form by hand and carried it to the township office the same afternoon). Keep one conceptual statement where the mechanism is first claimed; elsewhere let the sequence carry the logic. A suppressed template returns in a neighbouring form; fixing the surface word is not a fix (W16). |
| T16 | Conversion-frame template | the same "使/让/把 X 成为/获得/进入 Y" sentence closing paragraph after paragraph (规则成为可协商的对象；关系进入日常治理) | "turns X into Y", "makes X an operable object" repeated | State the change once where it matters; elsewhere show it through who did what and how the thing was used before and after. Vary the analytic move (contrast, consequence, condition). |
| T15 | Attribution clutter | （R2，2025） after most sentences of one passage | (Interview 7) after every sentence | Attribute once per passage; repeat only when the source changes. |

## What is NOT a trace (keep)

- Logical connectives that name a real relation (因此、然而、由于、从而、
  相比之下 / therefore, however, because). Removing them to satisfy a scanner
  makes the prose disconnected; the scanner no longer counts them as closers.
- A contrast with a named view or with the previous sentence ("not A but B"
  where A is someone's position).

- A source-status distinction that changes how a claim must be read: a plan vs
  an outcome, a recollection vs a document, a promise vs a payment. Keep it,
  phrased through the verb or a short clause, next to the claim it qualifies.
- A method fact readers need to judge reach: number of interviews, time span,
  who was and was not interviewed. Say it once in methods.
- A named rival explanation and why the material favours the paper's account.
- A contradiction or negative case: this is data.

## Rhythm and register checks

- Paragraph openings: no opening word or phrase used three or more times in a
  row of sections; no section in which most paragraphs open with "本文 / This
  study".
- Sentence length: let it follow the logic. Chinese academic prose usually
  links claim, evidence and implication in one sentence through clauses; keep
  short sentences for emphasis, not as the default unit.
- Verbs over nominalizations: "farmers stopped selling to the trader" over "the
  discontinuation of trader-based sales relations".
- Concrete before abstract inside a paragraph when the paragraph presents
  material; abstract before concrete when it states a claim. Not both
  everywhere.
- No paragraph exists only to announce the next paragraph.
