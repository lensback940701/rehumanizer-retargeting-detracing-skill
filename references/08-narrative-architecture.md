# 08 Narrative architecture: how sections lead the reader in and guide the eye

Sentence-level cohesion (07) makes neighbouring sentences connect. A paper can
pass that test and still feel flat: the case chapter starts with a location
line, every findings section opens on its thesis, and paragraphs jump from one
actor to another without telling the reader where to look or why. Readers
describe this as "no lead-in" (没有导入) or "not drawn in" (不够娓娓道来、引人入胜). This
reference works at section level: entries, unfolding, focus shifts and exits.

## 1 The context-and-case entry (导入)

The chapter that introduces the study area must make the reader care about
the place before the paper uses it. Build a ladder and stop at the rung the
argument needs:

1. **Field significance**: why this sector or kind of place matters, with one
   or two sourced facts (share, scale, trend).
2. **Formation**: how the place came to be what it is, via the turning points
   that created the present problem (an entry of outside capital, a price
   collapse, a policy shift).
3. **Case leverage**: why this case reveals the paper's question better than
   others. Say it explicitly ("基于以上特点，本文选取……作为案例区"; "Baoshan
   offers a revealing case because ..."), and name the kind of case it is:
   typical, extreme, diverse, or a case where the usual explanation should
   work and does not.
4. **Within-case selection**: which sites, actors or episodes, and why they
   allow the comparison the paper makes.
5. **Materials**: what was gathered, from whom, when; stated once, plainly.

Facts on rungs 1–2 need sources: cited literature, official statistics,
policy documents, or the author's own published papers (cited). The Goal lists
the permitted context sources. If none exist, Stage 1 asks the author; Stage 2
never fills the ladder from memory.

## 2 Entering an empirical section

Do not open every findings section with its conclusion. Choose an entry that
puts the reader inside the material, then let the claim surface within the
first one or two paragraphs.

| entry move | what it does | example opening (domain-neutral) |
| --- | --- | --- |
| Historical arc | starts where the change began | "In 2014 the city announced that every pre-1990 block would be rebuilt within five years." |
| Scene | places the reader at a site and moment | "On the morning the survey team arrived, half the stalls on the east side of the market were already shuttered." |
| Actor trajectory | follows one person's path into the problem | "A former bus driver, she took over her mother's licence in 2019 and soon found that ..." |
| Puzzle or contrast | sets two observations against each other | "Two villages ten kilometres apart received the same irrigation grant; one doubled its harvest, the other let the pipes rust." |
| Return to the question | picks up the thread left by the previous section | "If the grant did not decide the outcome, the next question is who could keep the pumps running." |

Rules of use:
- The first empirical section never opens on a bare thesis.
- Vary entries across sections: three scene-openings in a row is a new
  template.
- A thesis-first opening is fine when the previous section has already set the
  scene and the reader is waiting for the claim.

## 3 Unfolding (娓娓道来)

Order the material as the reader needs to meet it:
1. the situation;
2. what the actor wanted;
3. what stood in the way;
4. what the actor did;
5. what that reveals.

Let analysis grow out of the account instead of preceding it. Use time order
where an actor's trajectory exists. Introduce the conceptual label at the
moment it explains something the reader has just seen, not before. Keep one or
two concrete details that let the reader picture the place (a reading on a
sensor, a drying rack, a price), but only those that do analytic work.

## 4 Guiding the eye when the focus shifts (视线引导)

When a paragraph moves to another actor, place, scale or time, the first
sentence must tell the reader where the camera is going and why. Useful moves:

| move | use when | bridge pattern |
| --- | --- | --- |
| Follow | the same actor continues to a new step | "Once the pipes were in, the problem became ..." |
| Pan | same problem, another actor or site in the same frame | "A few kilometres downhill, households with five-mu plots faced the same water question with ..." |
| Zoom out | from one case to the wider pattern | "This was not one estate's preference: across the village, ..." |
| Zoom in | from a pattern into a decisive detail | "The difference shows most clearly in the drying shed." |
| Cut back | return to an earlier actor | "Back on the hillside estate, the same question arose when ..." |
| Cross-cut | set two actors side by side on one axis | "Where the estate solved water with a pump, the family solved it with timing." |

A bridge sentence:
- names the destination;
- names the comparison axis (the reason for going there);
- relates the new focus to the previous one (same problem, opposite answer,
  next step).

Keep a **guide thread**, a recurring actor or place the reader can follow
through the section, and return to it at the end. Signal a section's route at
its entry when the route is not obvious ("本节从老城区的补偿谈判开始，沿搬迁路线
走到郊区安置点，再回到老城区留下的空房"); do this for complex sections only, not as
a fixed opening formula.

## 5 Section exits and hand-offs

End a section by completing its analytic step and pointing to what is still
unexplained, which the next section takes up. Do not end on a summary of the
section or on a slogan.

## 6 The section architecture map (Stage 2, P3)

Before rewriting, fill one row per section:

| section | entry move | where the claim surfaces | focus path (in order, with the bridge reason for each move) | guide thread | exit / hand-off |
| --- | --- | --- | --- | --- | --- |

The map is a plan, not a template. If a section's focus path has more than
four moves, ask whether it should be split, or whether the actors could be
cross-cut on one axis instead.

## 7 Architecture read (Stage 2, P7)

After the cold read and before the flow read (07), read only the section
openings, the first sentences of paragraphs and the section endings, in order:

1. Does the context chapter make me care about the place before using it, and
   does it say why this case was chosen?
2. Does each empirical section draw me in before telling me what to think?
3. Every time the focus changes, do I know where I am now and why I was
   brought here?
4. Is there a person or place I can follow through each section?
5. Does each section end by handing me to the next question?
6. Do the entries vary, or has a new formula appeared?

## 8 Signals

`trace_scan.py` lists:
- `abstract_section_opener`: a section whose first sentence has no place, time,
  person-in-scene, number, quotation or source;
- `unguided_focus_shift`: the paragraph's main source changes, and the first
  sentence neither signals a move nor introduces the new actor in a situated way;
- the sections where a case-selection move appears.

`defense_gate.py` reports them as W13 for empirical and context sections. They
are candidates for the architecture read, not counts to drive to zero.
Theoretical sections may properly open on a thesis.
