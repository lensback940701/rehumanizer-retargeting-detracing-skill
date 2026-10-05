# 07 Cohesion and flow: sentences that hand the argument on

A route-corrected draft can have the right target, real material and no
defensive tics, and still read as stiff: each sentence is a separate
assertion, paragraphs start from nowhere, and every second sentence ends in a
source parenthesis. Readers experience this as "no transitions" (没有过渡衔接).
It is a predictable side effect of detracing: deleting restating closers,
strawman negations and hedges also deletes the words that carried logical
relations, unless the rewrite puts relations back on purpose.

## Why route correction tends to go staccato

- **Connectives removed together with closers.** "因此 / 由此 / 这说明 / thus"
  are relation words, not traces. Only a closing sentence that *restates* the
  paragraph is a defect; a sentence that draws the consequence is the argument.
- **Contrast scaffolding removed with negation-defence.** "不是 A，而是 B /
  not A but B" is defensive only when A is a straw view. Contrast against a
  named view or a previous sentence is how analysis moves.
- **Per-sentence attribution.** A parenthesis after every sentence chops a
  passage that draws on one interview into separate claims.
- **A new template replaces the old one.** Aphoristic closers ("X 没有变，变的
  是 Y" / "it picks land, and it picks people") and pivot openers ("……也……")
  appear in paragraph after paragraph.
- **"Vary sentence length" read as "write short sentences".** Chinese academic
  prose carries claim, evidence and implication in one sentence through
  clauses (由于……，……；虽然……，但……；……，从而……). A chain of short
  declaratives leaves the reader to supply every relation.

## Six working rules

1. **Given before new.** Each sentence starts from something the reader
   already holds and adds one new thing:
   - the previous sentence's endpoint, the paragraph topic, or a pronoun with
     a noun (这一做法 / 此类地块 / this arrangement);
   - repeating the key noun is cohesion, not redundancy.
2. **Say the relation when it is not obvious.** If a reader could ask "why
   does this sentence come next?", answer with a word or a clause:
   - cause (因此、由于、从而);
   - contrast (但、然而、反而、相比之下);
   - concession (虽然……但);
   - condition (只有……才、一旦);
   - extension (进一步、更重要的是);
   - example (例如).
   Do not add connectives where the relation is already plain, and do not
   build cohesion out of a chain of 由此/因此/从而: a sequence of concrete
   steps carries its own logic. Likewise, a link verb (进入、接入、纳入、相接 /
   enters, feeds into) names a relation without showing it; say what someone
   did instead (T17, W16).
3. **Paragraph handoff.** The first sentence of a paragraph says how it
   relates to the previous paragraph (next mechanism, counter-case, extension,
   consequence). The last sentence either completes the analytic step or
   opens the next one; it never restates or ends on a slogan.
4. **Quotes inside the flow.** Before the quotation, say why this speaker is
   heard here. After it, pick up the quotation's own words and take one step
   beyond them (what it shows that the reader could not see before).
5. **Attribute once per passage.** When several sentences draw on the same
   interview or document, attribute at the first use and again only when the
   source changes or a new claim needs its own warrant. Reporting verbs (他说、
   按她的说法、the official recalled) can replace repeated parentheses.
   - A "source" is one interview (or document), not one person: interviews of
     the same person in different years are different sources, so mark the
     year when you switch between them.
   - After a sentence that cites two sources, re-attribute the next quotation
     explicitly, so the reader knows whose words follow.

6. **Do not let one analytic sentence shape become the paragraph ending.**
   When every paragraph closes on "this made X into Y" (使X成为Y), the
   reader hears a refrain, not an argument. Close instead on the consequence,
   the contrast with the previous case, or the question the next paragraph
   takes up.

## Before / after (domain-neutral examples)

**Staccato:**
> 新规要求每栋楼统一加装电梯。老旧小区的楼间距不够。业主意见不一。电梯
> 只装进了新区。规则没有变，变的是楼。

**Connected:**
> 新规要求每栋楼统一加装电梯，但这一要求预设了足够的楼间距；老旧小区恰恰
> 缺少这种空间，加之业主对分摊费用意见不一，电梯最终只装进了楼距宽、产权
> 集中的新区。换言之，同一条规则之所以落地不均，原因在于它所要求的空间条件
> 本身只存在于部分社区。

**Staccato (English):**
> Couriers share routes. The platform does not see them. Earnings rise. Control
> changes shape.

**Connected:**
> Couriers share route rules in group chats that the platform cannot see, and
> those who follow the rules earn about a seventh more per shift. Control does
> not disappear here; it moves from the dispatch algorithm to the peer group
> that decides which rules count.

## Flow read (Stage 2, P7)

After the cold read, read every paragraph once more for flow only:

1. For each adjacent sentence pair: can I say why the second follows? If the
   answer needs a word, write the word; if it needs a clause, merge the
   sentences.
2. For each paragraph opening: what in the previous paragraph does it continue,
   qualify or turn against? Make that visible.
3. For each paragraph ending: does it add a step or only stamp the paragraph?
   Replace stamps and slogans with the consequence or the next question.
4. For each run of source parentheses: keep the first, keep any that marks a
   change of source, delete the rest.
5. Read the section aloud in your head. If it sounds like a list of findings,
   it is not yet an argument.

## Reading the W8 signals

`defense_gate.py` reports these, compared with the baseline and the voice
references in the same language:
- topic linkage (share of sentences whose opening clause reuses content from
  the previous sentence);
- mean sentence length;
- staccato runs;
- source-parenthesis density.

They are alarms. Published papers in the same journal differ, so judge in
context. A low topic-linkage rate together with short sentences and dense
parentheses almost always means the draft reads as disconnected; repair it
with the five rules above, not by inserting connectives mechanically.
