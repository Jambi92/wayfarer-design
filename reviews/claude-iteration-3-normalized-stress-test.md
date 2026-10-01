# Iteration 3 — Normalized-Height Stress Test and Remaining Sculpt Work

**Author:** Claude
**Responds to:** `reviews/claude-iteration-3-validation-follow-up.md` and `reviews/visual-validation-iteration-3-true-scale-disposition.md`
**Status:** READY FOR AUTHOR / TYLER REVIEW
**Scope:** Visual validation only. No spec edits, no Pass 2 work, no UE5 work.

## Sheets

All sheets are in `reviews/images/race-references-iteration-3/`. They are NON-CANONICAL / DIAGNOSTIC and use the same fixed orthographic camera.

- **Full normalized sets, already generated with Iteration 3:**
  - `setA_Masc_normalized.jpg`, `setA_Fem_normalized.jpg`
  - `setB_Masc_normalized.jpg`, `setB_Fem_normalized.jpg`
- **New grouped stress-test sheets:** `stress_Masc_normalized.jpg`, `stress_Fem_normalized.jpg`. The groups are:
  - Skarn and Marchfolk
  - Durrim, Pipkin and Cogling
  - Grask and Gorrund
  - Fenn, Aelari and Vael
  - Halvren A and B
  - Saurin
- **New Skarn check:** `skarn_Masc_normalized.jpg`, `skarn_Fem_normalized.jpg`. These show Marchfolk, accepted Skarn and a skeletal-only Skarn candidate.

## Result: no accepted reference fails

Normalized measurements below are shares of stature (masculine, then feminine).

**1. Skarn vs Marchfolk — PASS, but the margin is modest.**

| Measurement | Marchfolk | Skarn | Difference |
|---|---|---|---|
| Shoulder joint width (masc) | 21.5% | 23.5% | +9% |
| Shoulder joint width (fem) | 19.3% | 21.1% | +9% |
| Chest depth | 11.6% | 12.2% | +5% |
| Wrist girth | 8.6% | 9.2% | +7% |
| Knee girth | 19.8% | 21.0% | +6% |
| Ankle girth | 13.7% | 14.6% | +6% |
| Neck girth | 21.1% | 22.2% | +5% |

- Identity survives in the shoulder girdle, neck base and joints. Muscle and fat are identical to Marchfolk, so no muscle is involved.
- The difference is readable but quiet, most of all in the feminine profile view.
- For a decision, I built a **skeletal-only candidate (Skarn_S2)**. It changes the frame only:
  - shoulder joint width 24.3%
  - chest depth 12.6%
  - wrist 9.6%
  - knee 21.8%
  - hip joint width +3%

  Muscle and fat are unchanged.
- It is not substituted. Accepted Skarn stays the reference unless Tyler/Author pick the candidate.

**2. Durrim, Pipkin and Cogling — PASS.**
- **Durrim:** reads compact and deep without height. Trunk is 35.5% of stature, chest depth 13.3%, wrist 9.7%.
- **Pipkin:** light and compact, with a lower trunk share (30.7%).
- **Cogling:** fine and distal (forearm-to-upper-arm 1.20, wrist 7.7%).
- Pipkin and Cogling are close in front silhouette. They separate in the arm and shin segment ratios and in joint fineness. That overlap is allowed.
- All three read as adults.

**3. Grask vs Gorrund — PASS on direction.**
- **Grask:** rangy, with trunk at 30.1% of stature and shin-to-thigh 1.09.
- **Gorrund:** axial, with trunk at 33.4%, chest depth 14.0% and shoulder joint width 24.4%.
- Gorrund still lacks the full load-path mass; see the sculpt task below.

**4. Fenn, Aelari and Vael — PASS.**
- **Fenn:** distal; forearm-to-upper-arm 1.17, wrist 7.2%.
- **Aelari:** distributed elongation, with neck and trunk length up.
- **Vael:** deepest central body of the three (chest depth 12.4%).
- They are subtle at equal height, as expected.

**5. Halvren A and B — PASS.**
- They are two distinct mixed-ancestry points: A is distal and elf-leaning, B has a human-leaning torso.
- Neither is a midpoint.

**6. Saurin body — PASS (provisional).**
- The pelvis is deeper front-to-back (hip depth 1.12) and the lower trunk longer.
- The full tail is shown: 128 cm long, a 22 × 24 cm base sized from the pelvis, tapered, in a gravity curve.
- The head is a placeholder and is not part of this result.

## Carried sculpt tasks (tooling limits, not spec changes)

**1. Gorrund load-path sculpt.**
- MPFB's torso-depth and shoulder-distance controls are at their maximum.
- A direct sculpt should strengthen this chain: shoulder girdle → thorax → lower axial trunk → pelvis → proximal lower limbs.
- The goal is structural continuity, not muscle bulk.
- Base files: `RaceBodies/out/Gorrund_Masc.blend` and `RaceBodies/out/Gorrund_Fem.blend`.

**2. Saurin dedicated head and extremities sculpt.** This needs:
- Layered Rostral-Cranial Integration;
- a compact rostrum and rostral floor;
- the orbital/temporal platform;
- deep posterior jaw integration;
- recessed auricular openings;
- Regional Scale Architecture;
- hands, feet, claws and contact surfaces;
- a sculpted tail base that blends into the sacrum (the current tail is a separate bone-parented mesh).

The body and the complete tail stay as they are.

**3. Optional: Skarn.** Adopt Skarn_S2 or keep the current Skarn. This is an Author/Tyler choice.

## Spec/model conflicts

None found. No canonical spec was edited.
