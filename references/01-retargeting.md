# 01 Retargeting: recover the target the paper set out to hit

Many manuscripts lose their best idea during revision, not because the
evidence refuted it but because each round of review added a safer phrasing,
another caveat or another lock. Retargeting reverses retreats that were not
forced by evidence and re-anchors the whole paper on one claim worth arguing.

## Symptom profile (Stage 1, S1.1)

Score each dimension `0 none · 1 mild · 2 marked · 3 dominant` and quote two or
three excerpts. Use scanner signals as pointers, not as the score.

| # | dimension | what it looks like | typical scanner pointers |
| --- | --- | --- | --- |
| S1 | Target drift | Title promises X; findings answer a smaller, safer Y. The research question became "how do actors adjust" instead of "why does the accepted account fail". | timeline: target lines change from "challenge / overturn" verbs to "relate / connect / adjust" verbs |
| S2 | Contribution dilution | Contribution phrased as "more specific", "more complex", "connects A with B", "provides a perspective". No view is corrected. | `stance` = 0; hedged_finding in abstract/conclusion |
| S3 | Tautological finding | A finding a reader could have written without the data ("actors adjust what they can control"; "implementation needs conditions"). | high abstract-term density; abstract closers |
| S4 | Mechanical prose | Every paragraph: topic → material → generic wrap-up; nominal stacks; repeated openings; uniform rhythm. | abstract_closer_share, abstract_terms_per_k, repeated openings |
| S5 | Process / audit traces | Text tells the reader how sources were handled sentence by sentence. | process_trace, source_first |
| S6 | Living-material starvation | People appear as codes; the most telling quotes and numbers stayed in the transcripts or tables. | quotes_per_k, numbers_per_k, code_tokens_per_k vs voice references |
| S7 | Promise–content gap | A title/keyword concept is barely developed (e.g., the paper names an environmental, institutional or material dimension it never analyses). | count of title keywords in body + manual check |
| S9 | Flat section architecture | Case chapter starts with a location line and never says why this case; findings sections open on their thesis; paragraphs jump between actors without saying where or why. | W13: abstract_section_opener, unguided_focus_shift, case_selection_sections |
| S8 | Disconnected prose | Sentences do not pick up what the previous one said; paragraphs start from nowhere; source parentheses after most sentences; slogan-like closers. | topic_link_rate, sentence length, attributions_per_100_sentences, staccato runs, epigram closers vs voice references |

A paper is an RRD case when S1 or S2 is ≥2, or when three or more dimensions
are ≥2. If only S4/S5 are high and the target is intact, route to
press-conference-revision or a local edit and report `NOT_RRD_CASE`.

## Drift taxonomy (Target Drift Ledger)

For every major retreat between the origin artifacts and the baseline, record
the before/after wording, the round where it happened, and the cause:

| code | cause | default action |
| --- | --- | --- |
| `EVIDENCE_FORCED` | Located sources contradict or cannot carry the original claim. | Keep the retreat; reshape the target honestly around what the evidence does show. |
| `SCOPE_SHARPENED` | Narrowing made the claim more precise and more interesting. | Keep. |
| `RULE_FORCED` | A workflow lock caused it (quote freeze, anchor-only evidence, ban on new material, word-loss threshold, naming rule). | Reverse if the lock is retired; re-verify against sources. |
| `ANXIETY_FORCED` | A caveat or softening added against an imagined reviewer, with no specific evidence. | Reverse. |
| `DILUTED` | The contribution was split across many lenses/concepts until none carries it. | Re-concentrate on one primary concept; demote the rest to tools. |
| `SUBSTITUTED` | A specific, risky term was replaced by a generic, safe one. | Restore the specific term or justify the substitution with evidence. |
| `LOST_IN_PIPELINE` | Content vanished in a multi-agent pass without any recorded reason. | Restore if sourced. |

Evidence for the classification is the round's own records (audit reports,
Goal texts, change logs) plus the source passages. When the cause cannot be
established, mark `UNKNOWN` and treat it as reversible only after a source check.

## Target statement

**Two layers, theory first.** A target recovered from empirical mechanisms alone
tends to be too small: authors usually began with a paradigm-level ambition
(often visible in a call for papers, a proposal or an early abstract) and the
mechanisms were how they meant to show it. Write every candidate as:

1. **Theoretical target**: the proposition about the field's way of thinking
   that the paper revises, stated so that it would still make sense with the
   case removed (e.g., "selectivity is constitutive of resource-making, not an
   implementation deficit"). Its adversary is a theoretical position in the
   literature, engaged as something to extend or correct, not to caricature.
   State its portability conditions once.
2. **Empirical mechanism layer**: the two to four mechanisms (L3) through
   which the case carries the theoretical target, each with its material.

When a neighbouring framework theorizes a *kind of actor* (returnees,
entrepreneurs, cooperatives) as the driver, decide whether actor identity is a
theoretical dimension in this paper or only the empirical form the driver
takes. Often the paper's driver is a practice (introducing a technology,
imposing a quality rule) and the actor type is how it shows up in the field;
then cite the framework for its question, re-specify the driver, and keep
actor identity in the case description.

**Frame, outcome, means.** A strong theoretical target names three things:
the frame (what is being selected, compared or decided), the **outcome** the
paper's main concept promises (the title's verb: activated, excluded,
transformed, stabilized), and the means by which the outcome comes about.
Varied practices, coexisting uses and "different combinations" are means;
a target that stops at them is soft. Write the outcome into the theoretical
target and make each mechanism lead to it, not to "uses differ". In the prose,
show the outcome rather than chanting it: the reader should see what X was used
for before and after the change. Restating "X became Y" at the end of every
paragraph is a new template (T16, W15), and so is telling the mechanism
through placeholder verbs (X 进入/接入/参与构成 Y; T17, W16). State the outcome
at the strength the evidence supports: if the material shows that selection
constitutes the usable resource, write that it does, not that it "participates
in" doing so.

If the author says the target feels "too empirical", lift layer 1 from the
origin artifacts' most abstract formulation and the field's current debate;
do not invent a grander claim the mechanisms cannot carry.

Write the mechanism layer of each Recovered Target Statement in this shape (one paragraph, ≤120 words
or ≤220 Chinese characters, plus fields):

> Against **[adversary: an accepted view, default assumption or explanatory
> gap that exists in the cited literature or documented practice]**, this paper
> shows that **[claim]**, because **[mechanism]**, as seen in **[evidence
> pattern: which contrast, sequence or variation in the material]**. This
> matters because **[payoff: which theoretical understanding or practical
> judgement changes]**.

Fields: `claim_type` and `scope` (see the claim table below), `evidence_risk` (what in the sources
could undercut it), `material_to_carry_it` (3–6 source passages), `what_it_drops`
(content of the baseline that no longer serves the spine).

Tests every candidate must pass:

- **Altitude test**: the theoretical layer names what the field should think
  differently, not only what happened in the case.
- **Outcome test**: the target states the result promised by the main concept
  (e.g., what gets activated), not only the processes or the variety of uses.
- **Baseline-echo test**: compare the candidate's frame and mechanism
  vocabulary with the baseline's own framework. If they are the same ideas
  renamed, the target has not been recovered; either show what the baseline
  lost or justify keeping its frame with evidence.
- **Adversary test**: someone in the cited field would plausibly disagree or
  be surprised. "Context matters" and "it is more complex" fail.
- **Tautology test**: the claim could not have been written without the data.
- **Swap test (findings only)**: replacing the empirical object (crop, city,
  firm, policy) should break at least one sentence of the finding. Theoretical
  propositions may be general; findings may not be generic.
- **Ownership test**: the author would defend this claim at a seminar without
  retreating to "we only describe".
- **Evidence test**: the spot-checked passages support it at the stated level.

## Best supportable claim, not the highest one

Restoring ambition means restoring the claim that is most valuable **and**
best supported, not the earliest, boldest or most general formulation. A
single-case paper that precisely corrects the conditions under which a theory
holds may be at its best without any generalization. Record three things per
key claim instead of one ranking:

- **claim type**: description, pattern/contrast, mechanism, theoretical
  revision, or generalization;
- **scope**: where and for whom the claim is meant to hold;
- **support**: which passages carry it and how strongly (direct observation,
  consistent accounts, single account, inference).

The levels below are a vocabulary for claim type, not a ladder to climb.

| level | form | example verbs |
| --- | --- | --- |
| L1 | description | describe, document, record |
| L2 | pattern / contrast | differ, cluster, co-occur, sequence |
| L3 | mechanism | because, through, by way of, which makes |
| L4 | theoretical revision | corrects, qualifies, overturns, extends, shows the limit of |
| L5 | generalization beyond the case | holds where, predicts, travels to |

The **evidence ceiling** is what the located material supports; the
**baseline ceiling** is what the current draft dares to say. Where the
baseline sits below the evidence for no evidential reason, restore it; where a
higher claim type would add nothing the reader needs, do not climb. Each
strengthened claim cites its supporting passages in the route contract. Stage
1's spot-check is provisional: Stage 2 rechecks the target once after reading
the material in full (P2b), looking for the strongest counter-evidence.

## Rule debt

Rule debt is the stack of constraints inherited from earlier Goals, prompts
and audits. Each rule may have been sensible; together they make lively
writing impossible. Classify with the author:

| disposition | applies to | examples |
| --- | --- | --- |
| `RETAIN` | ethics, privacy, consent, anonymization; fact integrity (no invention); source and baseline protection; verified author decisions (title, named concept); commitments made to editors/reviewers in an active revise-and-resubmit (e.g., agreed causal-language limits) unless the author withdraws them | "no real names", "do not fabricate motives", "never overwrite originals" |
| `RELAX` | useful intent, harmful form | "keep all N quotations verbatim" → keep them unless a stronger quote does the same work; "use role codes" → codes in citations, situated descriptions in prose |
| `RETIRE` | process or style locks that froze the text | quote freezes; "only previously admitted anchors"; per-sentence verification while drafting; net-word-loss thresholds; bans on restructuring; mandated paragraph templates |
| `CONVERT_TO_POSITIVE_GOAL` | negative quality rules | "don't be generic" → "each finding names a contrast and a mechanism" |

A rule the author marks `RETAIN` goes into the Goal's retained-lock list. Every
other inherited rule is void in Stage 2; the Goal says so explicitly.
