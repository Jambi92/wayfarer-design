# Audit: Cogling v1.0 Part 1, Racial foundation, scale and positive body anatomy

**Auditor:** Claude
**Audited file:** `specs/cogling/COGLING_V1.md` at commit `8805df9`
**Request:** `reviews/cogling-part-1-audit-request.md`
**Compared against:**
- `rules/character-creation-brief.md` (§15–16.12)
- `decisions/PROJECT_RULES.md`
- `register/decision-register.md`
- the approved Pipkin, Durrim, Fenn, Grask and Marchfolk specs
- the plan's prototype gap list

These are findings, not changes. The spec was not edited.

## 1. Result

**PASS WITH CLARIFICATIONS.** Part 1 does a lot right:
- It defines Cogling positively instead of as the leftover middle between Durrim and Pipkin.
- Its adult-read rules are strong.
- "Fine" construction never means fragile.
- Long fingers stay anatomy, not a tinkering stereotype.
- The culture and movement firewalls demote the brief's tinkering, quick-turn and climbing language without turning it into gameplay traits.
- Combined-proportion validity is in place.

There are no contradictions with project rules. Two findings should be resolved before Part 1 is accepted:
- **4a.** The positive specialization converges on approved Fenn and Grask relationships.
- **4b.** The stature range creates a broad Pipkin overlap that the spec describes as a single-height boundary test.

## 2. Contradictions

None with project rules or approved races.

**Brief.** The ~0.45× height reference is replaced by a provisional range. That is consistent with the brief, which calls its multipliers "preliminary design references, not final dimensions." No supersession is needed. See §5 for brief wording that a later part may supersede.

## 3. The fourteen requested checks

| # | Check | Result |
| --- | --- | --- |
| 1 | Positively defined, not leftover space | PASS in intent (§2–3). The positive content converges with Fenn and Grask, see 4a |
| 2 | ~76–91–107 cm defensible and provisional | Provisional: PASS. Framing of the Pipkin overlap: see 4b |
| 3 | Adult read at very small stature | PASS in rules (§5, §17–18); needs a sharper test, see 4c |
| 4 | Central body distinct from Durrim and Pipkin | PASS on negatives; the positive definition is thin, see 4d |
| 5 | Fine construction is not fragility | PASS (§7, §19–21) |
| 6 | Distal emphasis coherent, not Fenn or Grask reach | Coherent; **not yet distinct from Fenn and Grask**, see 4a |
| 7 | Long fingers anatomical, not a tinkering stereotype | PASS (§10–11) |
| 8 | Pelvis, shoulders, head and composition adult | PASS (§15–18, §20–23) |
| 9 | Culture and movement firewalls demote legacy language | PASS (§11, §27–28), with a note in §5 |
| 10 | Equal-height Pipkin, Durrim and child validation | Partly: COG-BODY-10 can't be run as written, and COG-BODY-11 needs a specific comparison (4c, 4e) |
| 11 | No prototype claims imported | PASS (§31). The prototype values are worth recording, see 4f |
| 12 | Combined-proportion validity | PASS (§33) |
| 13 | Terminology for the Short-Race Review | See 4g |
| 14 | Brief wording this would supersede | See §5 |

## 4. Findings

### 4a. Fine-Scale Elongated Articulation overlaps approved Fenn and Grask relationships (should be resolved before acceptance)

The listed Cogling tendencies are:
- narrow long-bone shafts and smaller joints
- relatively greater forearm and lower-leg contribution
- hands that take a larger share of arm length
- fingers that are long relative to the palm
- arms "somewhat emphasized relative to central-body size"
- a compact central body

Compare the approved text:
- **Fenn (v1.0 §5–7):** "longer arms relative to torso, slightly longer forearms, longer hands and fingers, narrower wrists"; legs with "greater leg share of height, slightly longer lower legs, narrower ankles"; "narrower joints and slenderer long bones."
- **Grask (Parts 1–2):** "compact-to-moderate torso contribution compared with limb length," "long forearms and lower legs as meaningful contributors," large hands, and forearm contribution "proportionally emphasized."

So, at normalized displayed height, the Cogling recipe is roughly Fenn gracility plus Grask distal emphasis. §9 and §12 say "not Grask reach" and "not miniature Fenn," but they don't say what keeps them apart. "Segment distribution and distal articulation" is the stated distinction (§9), yet both of those races already have distal emphasis too.

Stature keeps the races apart in the actual game: Fenn start at 157 cm and Grask at 198 cm. Normalized-silhouette tests, though, are how every race's identity has been validated, and the Cogling recipe as written wouldn't pass them.

**Recommended:** state Cogling's **total** limb contribution separately from its **within-limb** distribution. One coherent option:
- total arm and leg contribution to stature stays near the Marchfolk range, so Cogling aren't limb-dominant like Grask and don't take Fenn's greater leg share;
- the Cogling-specific signal is **redistribution within a near-human total limb length** toward the forearm, lower leg and hand.

If that is the intent, §9's "somewhat emphasized relative to central-body size" should be softened or removed.

Then add normalized-silhouette tests against both:
- **COG-BODY-16:** vs Fenn at normalized height, ears hidden.
- **COG-BODY-17:** vs Grask at normalized height, hands neutralized.

### 4b. The Pipkin overlap is broad, not a single-height boundary (should be resolved before acceptance)

§4 says "the ~91 cm reference intentionally meets the current provisional Pipkin minimum as an equal-height boundary test." But the Cogling maximum (~107 cm) equals the **Pipkin reference**. Cogling and Pipkin therefore overlap from 91 to 107 cm:
- the upper half of the Cogling range
- the lower third of the Pipkin range, including the central Pipkin adult

That is a broad overlap, not a boundary point. Durrim and Pipkin were deliberately set up as a single-height boundary at 122 cm, "no broad overlap implied" (Pipkin Part 2).

Broad overlap isn't forbidden; Marchfolk and Sagekin overlap heavily. But it changes what the spec must guarantee: a central-reference Pipkin and a maximum Cogling must stay distinct at the same height. As written, the overlap doesn't fit the boundary-test framing.

**Recommended:** pick one:
- **(a)** Keep 76–107 cm. Reword §4 as an intentional overlap zone of about 91–107 cm, add a test (central-reference Pipkin vs maximum Cogling at about 107 cm), and drop the "single boundary" framing.
- **(b)** Narrow the Cogling maximum to about 91 cm, so it is a single-height boundary like Durrim and Pipkin. This is close to the brief's ~0.45× of ~78 cm.

Either is valid. It's a design choice inside the spec, so it doesn't need Tyler unless ChatGPT presents it as an open option.

### 4c. At 76 cm, "human child" means an infant or toddler

Using ordinary human growth references as a rough guide, the Cogling range of 76–107 cm matches human children from about age 1 to about age 4. At those ages:
- the head is roughly a quarter to a fifth of stature
- limbs are short
- the trunk and abdomen are relatively large

COG-BODY-11 ("similar-height human child") should name the age band, so the hardest case actually gets tested: **minimum-height Cogling vs a toddler of about 1–2 years**.

Two practical consequences of the adult-head rule in §18 at this scale:
- A Cogling head at an adult-valid ratio is roughly 11–13 cm tall. Face and expression readability in third-person and dialogue cameras becomes a camera and presentation problem that Part 3 and the equipment and camera section will have to solve, without enlarging the head.
- The brief's "expressive face" will have to be delivered through anatomy and animation at that size.

Log both as OPEN for later parts. Neither is a Part 1 defect.

### 4d. The central body is defined mostly by what it isn't

§6 lists six things the central body is not. Its positive content is "fully adult but relatively small in absolute scale, moderate depth, narrow-to-moderate transverse envelope." Pipkin also have a moderate thorax (Part 2). So against Pipkin the central body adds little; the Cogling-Pipkin distinction rests on limbs (4a) and on Pipkin's pelvis anchor.

**Recommended:** one positive trunk statement, for example torso contribution to stature relative to Marchfolk, or how the narrow core reads at normalized height. It should be consistent with whatever 4a settles about limb totals. Otherwise "compact" has no measurable meaning.

### 4e. COG-BODY-10 can't be run as written

The Cogling maximum (~107 cm) is below the Durrim minimum (~122 cm), so "same-height Cogling and Durrim where ranges permit" never applies.

**Recommended:** replace it with a **normalized displayed-height** Cogling vs Durrim test (Broad, high-muscle Cogling vs Narrow Durrim), plus a body-context comparison at actual heights (maximum Cogling beside minimum Durrim).

### 4f. Prototype values worth recording (minor)

The prototype currently draws Cogling at about 0.72× Marchfolk scale (plan gap #5), roughly 125 cm. That is:
- above the provisional Cogling maximum (~107 cm)
- above the Durrim minimum (~122 cm)
- **taller than the prototype Pipkin** (0.70×, about 121 cm)

So the prototype reverses the approved Pipkin and Cogling height order. It is non-authoritative under §31. Record it in the eventual Cogling prototype ledger, as Pipkin's 0.7× value was recorded.

### 4g. Terminology for the Short-Race Comparative Anatomy Review (minor)

"Compact central body" adds a fourth "compact" term across the short races:
- Durrim: compact structural concentration
- Pipkin: Low-Set Compact Trunk and Compact Rounded Auricular
- Cogling: compact central body

This is exactly the convergence risk the Pipkin Part 3 audit raised (4e there). Consider a distinct word, such as "small stable core" or "narrow central core," and leave final wording to the Short-Race Review.

## 5. Brief wording a later part may supersede

| Brief text (§15–16.12) | Part 1 treatment | Later action |
| --- | --- | --- |
| ~0.45× height, ~0.40× mass | Replaced by a provisional range; the brief calls these preliminary | None needed. Mass is derived, not set |
| "Compact torso, long fingers, narrow limbs" | Kept as anatomy | None |
| "Expressive face" | Deferred to the face part (§26) | Part 3 must define positive anatomy, not caricature |
| "Fine motor control" | Not converted into a gameplay dexterity bonus (§11) | If the movement part rejects it as a racial trait, it needs **Tyler's explicit supersession**, as Pipkin's movement line did |
| "Quick steps, frequent turns, efficient climbing, precise hand movements, small physical adjustments" | Logged as legacy, subject to review (§28) | Same: **Tyler decision required** when the movement part settles it. It is not for Claude or ChatGPT to decide |
| "Engineering and tinkering show through culture" | Fully consistent (§27) | None |
| "Avoid oversized noses, enormous hats, giant goggles, comedic proportions" | Consistent (§5, §26–27) | None |

## 6. Cross-population summary

| Race | Status |
| --- | --- |
| Pipkin | Distinct by limbs, pelvis anchor and finer construction; the overlap framing needs fixing (4b), and the central body needs a positive statement (4d) |
| Durrim | Clearly distinct on mass, joints and limb reduction; COG-BODY-10 needs to be normalized (4e) |
| Fenn | **Converges** at normalized height (4a) |
| Grask | **Converges** on distal emphasis (4a) |
| Marchfolk | Distinct via stature and fine construction; normalized comparison depends on 4a and 4d |
| Human child or toddler | Strong rules; the test needs the age band (4c) |

## 7. Completion recommendation

1. ChatGPT patches 4a, 4b, 4d and 4e. 4c's test wording and 4f–4g are recommended.
2. I re-audit.
3. On a PASS and Tyler's approval, Part 1 is accepted and Cogling Part 2 can begin.

The brief movement and dexterity wording (§5) stays flagged for Tyler when the movement part arrives.
