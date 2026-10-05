# 05 Structural repairs

Route drift is rarely only a sentence problem. These repairs address the
architecture that lets a paper avoid its own claim.

## Literature as debate, not inventory

Symptom: one sentence per study, each with a reporting verb and a citation;
many works cited once for decoration; no side is taken.

Repair:

1. Group the admitted literature into two or three positions on the paper's
   question, one of which is (or contains) the adversary.
2. For each position: what it explains well, the assumption it rests on, and
   the case or situation where that assumption breaks.
3. End the section with the specific question that the paper's material can
   answer and the position cannot.
4. Give every remaining citation a job: `anchor` (the concept used),
   `adversary` (the view corrected), `bridge` (connects two debates), `method`,
   `fact`. Cut citations with no job; do not add new literature unless the
   Goal allows it and the work is in the local library.
5. Keep the citation count honest rather than fixed. Removing decorative
   citations is expected; removing an anchor or adversary is a substantive
   change and goes in the route memo.

## Title and keyword promise

Every term in the title and keywords must receive substantive analysis in the
findings, not just mentions. For each term list where it is analysed. If a
term is not carried, either develop it from sources (only if the material
exists) or change the title/keyword and log the change as an author query.
A frequent case: a paper titled after a material, spatial, ecological or
institutional dimension whose findings only discuss actors' talk about it.

## Framework as structure

If the paper has an analytic framework (figure, typology, stages, mechanisms),
the empirical sections should visibly use it: headings, paragraph claims or a
comparison table organized by its terms. A framework that appears only as a
figure and in the discussion is decoration. Either restructure the findings
around it or simplify it to what the findings actually use.

## Organizing findings by claim, not by informant

Person-by-person sections ("the founder… the official… the supplier…")
produce description. Organize each empirical section around a claim or a
contrast; bring actors in where they show it; let the same actor reappear
across sections. Keep at least one sustained actor thread so readers can follow
a person over time.

## Discussion that adds a step

The discussion must do at least one thing the findings did not:

- state precisely which part of the adversary's account fails and under what
  conditions it still holds;
- connect two findings into a mechanism that neither shows alone;
- name the condition under which the finding should travel (portability
  ceiling) and where it should not.

Cut paragraphs that re-list findings with citations attached.

## Section architecture

Section-level entries, unfolding and focus shifts are in
`08-narrative-architecture.md`; plan them in the section architecture map
before rewriting.

## Introduction funnel

Puzzle or accepted view under pressure → why it matters → what is usually
assumed → what this case makes visible → claim → how the paper shows it. Policy
or industry background comes in only as far as it creates the puzzle.

## Sibling-paper differentiation (when several papers share one dataset)

List the sibling papers' core claims. For each overlapping passage (same
informant, same quote, same event), state the job it does here versus there.
If the current paper's target overlaps a sibling's, sharpen it toward the
dimension only this paper analyses, and say in one sentence how it relates.
Do not weaken the current target to avoid overlap; differentiate it.

Run `scripts/sibling_overlap_check.py` on the rewritten manuscript against every
sibling paper. It flags verbatim or near-verbatim re-use of a quotation and
lists the quotations of siblings written in another language for semantic
review. A different statement by the same informant is not a duplicate unless
the author has ruled otherwise. Finding-level overlap (a sibling already made
the same argument with other quotes) is the more serious risk and is only
caught by reading the siblings' claims: when found, cite the sibling, disclose
the shared fieldwork, and move this paper's claim to what only it shows.

## Rewrite intensity

- `R1 re-route`: keep claims and section structure; any sentence may be
  rewritten, material reordered within sections, and weak material replaced
  with stronger located material from the bank.
- `R2 section rebuild`: R1 plus rewrite the empirical core and the theory
  section from the outline; reorganize findings by claim.
- `R3 full rewrite`: new outline from the spine; the baseline is a quarry for
  verified sentences, citations, tables and figures.

Choose the lowest intensity that can deliver the target. The Goal's steps
branch by intensity (material bank, spine and rewrite scope follow the chosen
level); an R1 job must not be executed as a full rewrite.

Refer to sibling papers in the prose only by citation or by their published
title. Internal labels the author uses for them (论文①, paper ②, 姊妹论文)
are workflow traces; G1 fails on them. Write 本文, not 本稿.
