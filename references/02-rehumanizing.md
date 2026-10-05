# 02 Rehumanizing: put people, situations and an author back on the page

"Human feel" (活人感) in an academic paper is not literary decoration. It is the
reader's sense that real actors faced real choices under real constraints, and
that an author with a view is explaining why. It comes from material and
stance, not adjectives.

## Living material (P2)

Mine the raw sources around the route contract. Collect what makes an
argument visible, not everything that is interesting. Log each item in
`living_material_bank.csv` with a locator and verbatim text.

| kind | what to look for | why it matters |
| --- | --- | --- |
| Turning point | the moment an actor changed course, and what triggered it | shows the mechanism in time |
| Dilemma | a choice between two costly options, in the actor's words | makes the decision intelligible |
| Self-description | how actors name their own role, doubt or identity | gives a person, not a code |
| Telling number | a price, ratio, quantity, duration, count that carries the logic ("selling one unit earns what three used to") | converts a claim into a stake |
| Contrast pair | two actors facing the same problem who chose differently | the backbone of comparison |
| Contradiction | what actors say vs. do; plan vs. outcome; rule vs. practice | the most credible data a paper has |
| Situated detail | the physical, institutional or economic detail without which the choice makes no sense | context that explains, not scenery |
| Counter-voice | the actor who disagrees, refuses, or failed | protects against a too-tidy story |

Selection rules:

- Prefer the line that carries the argument over the line that merely confirms
  it. The quote that surprised the interviewer is usually the one.
- Use the speaker's punchline, not the safe half of the sentence.
- A stronger quotation may replace a weaker one; removing a sourced
  quotation is recorded in the route memo with its reason.
- A quote must be followed by analysis that adds a step the quote does not
  already state. Never paraphrase the quote back to the reader.
- Keep two or three uncomfortable items (counter-voice, contradiction). They
  make the rest believable.
- Every item: source ID, locator (page/paragraph/timestamp/table), speaker or
  variable, verbatim text, verification status, intended use.

## Actor presence

- Introduce each recurring actor once with a situated role: where they came
  from, what they had at stake, what they controlled. One or two clauses.
- After that, refer to them by a stable, memorable descriptor or an authorized
  pseudonym. Keep source codes inside citation parentheses, not as the
  grammatical subject of sentences.
- Let actors be grammatical subjects of active verbs: they decide, refuse,
  bargain, wait, gamble. Avoid "the operator's adjustment was related to…".
- Do not assign gender, age, feelings or motives that the source does not
  state. "He said he did not want to leave" is sourced; "he loved the
  mountains" is not.
- For quantitative work the "actors" may be units (counties, firms,
  households). Name a concrete unit when it illustrates the pattern.

## Author stance

- The author argues. Use "本文认为 / 我们发现 / we argue / this shows" where a
  judgement is being made, especially in the introduction, the start of each
  empirical section, the discussion and the conclusion.
- State the claim, then the qualification it really needs, not the reverse.
- Put the adversary on the page by name or citation and say where it goes
  wrong.
- One strong claim with one precise limit beats five soft claims.

## Calibrating to the author's own voice

Run `trace_scan.py` on the author's published papers. Compare: sentence length
and its variation; quote and number density; stance density; how quotations
are introduced; how paragraphs open; how strongly conclusions are phrased.
Write a short `voice_profile.md` (10 lines) and write toward it. Match moves and
register, never copy sentences or content. Where the published paper had a
known weakness (e.g., overclaiming), note it and do not imitate it.

The defaults below (three actors, a surprise per section, a quotable
paragraph) suit case-based papers; theoretical and quantitative papers apply
their equivalents from `06-field-adapters.md` rather than these literally.
Prose flow is part of rehumanizing: see `07-cohesion-and-flow.md`.

## Section moves

- **Introduction**: open with the puzzle or the accepted view under pressure,
  not with policy background. Within the first two paragraphs the reader knows
  what is usually assumed, what this case shows that the assumption misses, and
  what the paper claims.
- **Theory**: a debate with sides, ending in the exact question the case can
  answer (see 05 §Literature as debate).
- **Context/method**: the minimum the reader needs to understand the choices
  actors face; the material's real reach (who, how many, when) said once,
  plainly, without apology.
- **Empirical sections**: each brings the reader into the material first (entry
  moves in `08-narrative-architecture.md`) and lets its claim surface within
  the first one or two paragraphs; shows it through actors and material,
  including the counter-case; ends on a step forward, not a summary.
- **Discussion**: what the findings change in the adversary's account; one
  paragraph of honest limits; no re-listing of findings.
- **Conclusion**: the memory point in two or three sentences; the payoff; a
  specific next question.

## Cold-read questions (P7)

Read the whole draft once without the change log, as a reader would:

1. After the first page, can I state the claim and whom it argues against?
2. Can I name three people or units in the paper and what each was up against?
3. Is there a moment in each empirical section where something surprised me?
4. Does any paragraph end by restating itself?
5. Do I ever learn how the author handled the files rather than what happened?
6. Does the discussion tell me something the findings sections did not?
7. Would the author's published papers recognize this voice?
8. Is there anything here I could not trust because it reads too tidy?
9. Does the title's key concept get real analysis, not just a mention?
10. Which single paragraph would I quote to a colleague? If none, the route is
    not yet corrected.
11. Does each sentence follow from the one before, and each paragraph from the
    previous one, without my having to supply the link? (Then do the flow read
    in `07-cohesion-and-flow.md`.)
12. Was I led into each section, and did I always know where I was when the
    focus moved? (Then do the architecture read in `08-narrative-architecture.md`.)
