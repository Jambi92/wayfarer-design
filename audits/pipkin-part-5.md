# Audit: Pipkin v1.0 Part 5, Movement, Posture, Locomotion and Whole-Character Physical Expression

**Auditor:** Claude
**Audited file:** `specs/pipkin/PIPKIN_V1.md` at commit `7acc6fc`
**Request:** `reviews/pipkin-part-5-audit-request.md`
**Compared against:**
- Pipkin Parts 1–4
- `rules/character-creation-brief.md`
- `decisions/PROJECT_RULES.md`
- `register/decision-register.md`
- the Part 5 sections of Durrim, Grask and Gorrund
- the Marchfolk, Fenn and Halvren specs

These are findings, not changes. The spec was not edited.

## 1. Result

**PASS WITH CLARIFICATIONS.** Part 5 is a strong movement section. It:
- keeps adult mechanics
- rejects every halfling and dwarf movement stereotype
- keeps resting alignment separate from body language
- makes the world adapt to the anatomy
- keeps canonical objects at true scale
- separates visual, interaction and combat reach
- puts every gameplay statistic behind an explicit firewall

Two items need Tyler's attention before Part 5 is accepted:
- **4a.** Part 5 contradicts the brief's movement wording. It may well be the right call, but the brief is approved text, so the change needs Tyler's explicit approval.
- **4b.** Part 5 doesn't cover the "equipment fit and final first-pass review" scope that every completed race's Part 5 included. Either a Part 6 is planned or this is a gap.

The Part 4 status line was correctly updated to FIRST-PASS ACCEPTED.

## 2. The thirteen requested checks

| # | Check | Result |
| --- | --- | --- |
| 1 | Movement follows Pipkin anatomy, not scaled Marchfolk | PASS. §4, §6 and §31 forbid uniform retiming or spatial shrinking, and §35 says the same for Marchfolk |
| 2 | Adult movement distinct from a child's without relying on performance | PASS, with a note in 4d. Supported by §11, §21, §28, PIP-MOVE-07 and 21, and the stress cases |
| 3 | No waddle, bounce, scurry, "nimble halfling" or heavy dwarf | PASS. Ruled out in §4, §8, §11, §27, §29 and §36 |
| 4 | Resting alignment separate from body language | PASS. §2 and §27 match project rules |
| 5 | Biomechanical coherence without over-specified numbers | PASS, with an ambiguity in 4c |
| 6 | No silent gameplay bonus or penalty from size | PASS. §9, §10, §12, §13, §15 and §32 cover acceleration, turning, stealth, jumping and terrain. **This conflicts with the brief; see 4a** |
| 7 | World adapts to the anatomy | PASS. §14 (stairs), §16 (obstacles), §17 (ladders), §19 (sitting), §21 (counters) and §26 (eye lines) |
| 8 | Canonical objects independent of the holder | PASS. §22, PIP-MOVE-19 and the stress cases |
| 9 | Visual, interaction and combat reach separable | PASS. §21, §23 and §32 |
| 10 | Functional requirements, not premature UE5 | PASS. §31 is explicitly "not an implementation prescription" |
| 11 | Cross-race boundaries | PASS. §35 uses the approved terms for Durrim, Fenn, Grask and Gorrund ("Axial Load-Path Continuity"), and Cogling is undefined |
| 12 | Validation coverage | Good. Gaps are in 4b and 4d |
| 13 | What stays OPEN | See §6 |

## 3. Contradictions with Parts 1–4

None.
- **Part 1 §72–81.** It said "movement never automatically quick, nimble, scurrying, bouncy, slow or comically short-stepped" and "short legs never mean slow gameplay movement." Part 5 implements both.
- **Part 2.** The mature-pelvis rules hold: no hip-sway caricature (§5).
- **Part 3.** The rule that age is never the maturity mechanism holds (§28).
- **Part 4.** The rule that surface doesn't carry identity holds (stress cases).
- **Sneak trait.** It stays a legacy gameplay trait (§12).

## 4. Findings

### 4a. Part 5 overrides the brief's Pipkin movement description (needs Tyler's explicit approval)

The approved brief (`rules/`, listed under Approved Design Specification) says:
- §16.11: "Short stride, quick acceleration, rapid turns and excellent balance."
- Principles ("Movement is identity"): "Pipkin accelerate quickly with a short stride."

Part 5 rules against three of these four:
- §9: "Short stature must not automatically grant quicker acceleration, tighter turning … greater agility."
- §10: "Small body size does not automatically approve smaller gameplay turning radius or superior maneuverability."
- §3 and §7: a low center of mass and substantial feet do not grant "superior balance."

Only "short stride" survives, as the absolute biomechanical consequence in §4.

On design grounds Part 5's position is consistent with every completed race. Cosmetic anatomy never grants gameplay effects, and Part 1 already began moving this way. The brief's line can reasonably be read as describing *visible movement character* rather than stats. Even so, it is a direct conflict with approved text. Under the authority rule, a later race spec doesn't silently overwrite the brief.

There's a precedent. The brief's "large head" was superseded explicitly in Part 2, with a recorded decision.

**Recommended:** Tyler decides one of the following:
- **(a)** Part 5 supersedes the brief's "quick acceleration, rapid turns and excellent balance" (and "accelerate quickly" in the Principles). Record it the way "large head" was recorded, and add the brief wording to the terminology review.
- **(b)** Part 5 keeps those as *visual movement tendencies*, still with no gameplay effect.
- **(c)** Some of them stay as intended racial gameplay traits, to be decided in the race-biology-gameplay review.

Until then, the register logs this as OPEN.

### 4b. Equipment fit, camera and collision, presets and the final review aren't covered (needs a scope decision)

Every completed race's Part 5 included these, under titles such as "Movement, animation, equipment, world interaction and final first-pass review" (Grask, Gorrund) and "… equipment fit and final validation" (Durrim). The request mentions "do not begin Part 6," which suggests another part is planned. But `specs/STATUS.md` (and the brief's 14-item race template, §20) expect these items in the race spec, and none of them is covered yet:

- **Equipment fit.**
  - Clothing and armor fit (§30 says garments "must fit the Pipkin body" but sets no fit requirements).
  - Helmets and hoods over the mature head with rounded ears.
  - Footwear on the larger-valid Pipkin feet (Part 2).
  - Gloves on moderate adult hands.
  - Backpacks and belts on the low-set trunk.
- **Collision and camera.** Part 1 left collision OPEN ("never a scaled-down Marchfolk capsule") and the cameras OPEN. Part 5 §26 covers dialogue eye lines only: no third-person framing, creator camera or targeting.
- **Character and presentation presets, and race-aware randomization.** These are covered for every completed race. Part 4 touched surface randomization only.
- **Lifecycle.** Part 1 left it OPEN, and Parts 4–5 defer to it.
- **Final consolidated review.** That means a combined Pipkin identity statement, a consolidated OPEN list, the permanent validation set and a FIRST-PASS COMPLETE statement.

**Recommended:** confirm with Tyler whether a Part 6 ("Equipment, world scale, presets, randomization and final first-pass review") is planned, and update `specs/STATUS.md` to match. If not, these belong in a Part 5 patch. Either way, Pipkin can't be marked FIRST-PASS COMPLETE until they're covered.

### 4c. Equal gameplay speed and "no rapid-step caricature" need a defined boundary

Speed equals stride length multiplied by cadence. If a later review chooses equal walk speed with taller races (one of the open options in §8 and the stress cases in §34), a Pipkin with roughly 60% of Marchfolk leg length must use a higher cadence, relatively longer strides, or both. That is biomechanically unavoidable.

§4 forbids "tiny rapid footsteps used to fake equal speed," and §34 requires solving equal speed "without tiny rapid-step caricature." Without a boundary, those two requirements could be read as incompatible.

As a rough estimate (not a spec value): an ordinary 1.4 m/s human walk puts a Pipkin with a leg length of about 0.5 m near a brisk walk, but still below the usual walk-run transition. So equal walk speed is feasible as a visibly brisk adult walk.

**Recommended:** one sentence distinguishing the two. A biomechanically necessary higher cadence and relatively longer stride at matched speed are valid. Caricature means cadence beyond what the anatomy and speed require, shortened excursion, or added bounce. The equal-speed stress test should also check the walk-run transition.

### 4d. Step width and base of gait (child-read risk)

Toddlers and young children walk with a wide base and a higher, less consistent cadence. Part 2's mature, structurally broad pelvis places the hip joints relatively wider apart. §3 lets stance width "emerge from anatomy," and §5 forbids hip sway, but neither addresses **step width during gait**. A wide pelvis that translates directly into a wide-based walk would read toddler-like, or as a waddle.

**Recommended:** a line saying adult Pipkin keep an adult narrow-base gait, with foot placement converging toward the midline relative to hip width, so the broad pelvis isn't expressed as a wide-based walk. Extend PIP-MOVE-03 and 05 (or PIP-MOVE-07) to check step width.

### 4e. Minor points

- **Sex like-for-like.** Like-for-like sex comparisons (PIP-BODY-28 and 29, PIP-FACE-22 and 23) have no movement counterpart. Because the mature pelvis is the main movement-sensitive trait, one same-sex walk comparison against Marchfolk would close the loop on the Part 2 sex-coding fix. Optional.
- **Swimming.** §24 makes Pipkin swimming OPEN and calls for "its own cross-race review." That review isn't in `decisions/PROJECT_RULES.md`. This is the same issue as the dentition review in Part 4. Either Tyler adds it, or the wording should point to the existing OPEN gameplay items.
- **"Low absolute center of mass."** §3 and §15 are consistent with Part 1 §50 ("may give a relatively low absolute center of mass"). No change needed.

## 5. Prototype conflicts known from available evidence

The UE5 project was not opened. From the plan's recorded state:
- **Animation.** All races currently share one human animation set at uniform scale, which is the exact approach Part 5 §4 and §31 rule out for the final system. This is an accepted placeholder (plan gap #10). Note it for the implementation audit.
- **Scale and objects.** The prototype draws Pipkin at about 0.7× scale (about 121 cm) and scales held weapons with the body. §22 and §23 require canonical object scale, which matches plan gap #6.
- **Playtest notes.** The queued playtest notes (the swim-to-ramp exit, the roll that doesn't roll, janky landings) are prototype animation issues. They're unrelated to Pipkin design but will need re-checking against Part 5 §11 and §13 once per-race motion exists.

## 6. What should stay OPEN for the later movement and gameplay review

- walk, run and sprint speed
- acceleration, turning rate and stamina
- jump height, fall damage and landing
- stealth detection and footstep noise (the legacy sneak trait)
- balance and knockdown
- climbing and mantle height
- swimming
- interaction and combat reach
- dodge distance
- encumbrance and large-weapon feasibility
- ladder and stair world standards
- mount and vehicle contact points
- lifecycle timing and age-related movement
- the technical motion architecture (retargeting, IK, motion matching, race-specific clips)
- the brief-wording decision in 4a

## 7. Completion recommendation

- **Before Part 5 is accepted:** Tyler decides 4a and confirms the scope in 4b.
- **Patches for ChatGPT:** 4c and 4d (one line each, plus the test extensions); 4e is optional.
- **Then:** Part 5 can be marked first-pass accepted.
- **Pipkin v1.0 FIRST-PASS COMPLETE** needs the 4b scope covered, by Part 6 or a patch, and a final consistency audit.
