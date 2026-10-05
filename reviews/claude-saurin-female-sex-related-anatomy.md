# Saurin Female / Sex-Related Anatomy (DIAGNOSTIC / NOT FINAL)

**Author:** Claude
**Responds to:** `reviews/chatgpt-saurin-female-sex-related-anatomy-order.md` (0a4b65f)
**Phase:** design only.
- The frozen male/reference and every racial structure are unchanged.
- No spec text was changed: canonization waits for author review, as the order requires.
- No UE5, rig, animation, clothing or pigmentation-system work.

**Images:** `reviews/images/saurin-female/` (`v19_*`). **Numbers:** `v19_metrics.json`. **Tools:** `tools/rodin/female/`.

## 0. The female GLB reference was not accessible

I looked for it in every location I could reach on Tyler's PC:

| Location | Result |
|---|---|
| Rodin source masters (`C:\Users\Tyler\Wayfarer-Rodin\Source-Masters`, junctioned to `E:\Wayfarer-Rodin\Source-Masters`) | Only `Vael-Male` and `Vael-Female`, and only their folder names are visible: the E: target isn't connected to this session |
| `Wayfarer-Rodin\Jobs` | Records for Vael only |
| `E:\UnrealProjects` (RaceBodies, ImportPacks, Wayfarer-Design) | No Saurin GLB |
| Downloads, both Desktops, `E:\Tools` | No Saurin GLB |
| This workspace | No Saurin GLB |

Tyler chose to proceed without it, so **I did not inspect it, and §10 (GLB comparison) cannot be completed.**

Everything below comes from the frozen male/reference and the approved spec. If the GLB is provided later, the comparison can be run against the variants here; the warp tools take parameters, so any useful GLB proportion can be measured and tested directly.

## 1. Method

The female is **derived from the frozen reference** with the creator-variation warp system. It is not a new sculpt and not a human-female morph.

Because of this:
- Every racial structure is carried over exactly: skull, rostrum, orbit, jaw, scale fields, hands, feet, claws, sacral-caudal tail origin and tail logic.
- The only changes are the sex-correlated tendencies in §2.

**Equal-stature comparisons** hold standing height constant. Head and tail are compensated so they keep the reference's absolute size and % H (×1.0114), because sex does not change them.

**Measured with the same tools** as the variation package: tail cross-sections, root sufficiency, taper, balance, head ratios and thoracic depth/width.

## 2. Dimorphism model: LOW overall, regionally mixed

**Canon audit:**
- §24, §62, §154 and §235 forbid sex from determining height, frame, muscle, fat, tail, face, rostrum, displays or coloration.
- They allow only soft, overlapping population correlations.
- No spec defines Saurin reproductive anatomy, and no project rule requires a dimorphism.

**Biological reasoning, kept minimal:**
- Among reptiles, the most general and repeatable female tendency is a **relatively longer trunk between the limbs**, which gives internal capacity for developing eggs or young (fecundity selection).
- The Saurin canon already makes the *elongated lower axial trunk* a racial trait, so a female tendency in the same direction reinforces racial identity instead of importing a human cue.
- A modest pelvic-canal tendency follows from the same capacity argument.
- Male-biased head and display size, common in combat- or display-driven lizards, is **not** adopted. Canon §102 forbids displays as sex markers, and nothing in Saurin canon establishes male-male combat or courtship display.

**The one assumption this needs** (for the author to confirm): Saurin females carry developing eggs or young internally for some period. That holds for essentially all amniote reproduction. Oviparity vs viviparity is left unspecified.

**Accepted differences (candidates):**

| Domain | Female tendency | Class |
|---|---|---|
| Lower axial trunk length | **+6 % mean** (+1.8 cm at 187.9 cm), with the species range of ±10 % unchanged | Sex-correlated, strong overlap |
| Skeletal pelvic band width | **+3 % mean** (+0.6 cm external, thighs included). Internal canal, no lateral hip flare. Species ±7 % unchanged | Sex-correlated, strong overlap |
| Everything else listed below | — | No sex difference at first pass |

The domains with **no sex difference at first pass**:
- stature distribution;
- frame distribution;
- shoulder breadth;
- thoracic depth/width;
- limb ratios;
- hands and feet;
- tail length, base and fullness;
- muscle and fat amount and distribution;
- neck;
- head proportion;
- skull, rostrum, jaw and orbit;
- display incidence, size, base and shape;
- scale fields, ventral field, keratin and claws;
- baseline pigmentation and pattern.

Each of these varies individually, independent of sex.

**Never biological** (presentation/culture only):
- jewellery, paint and clothing;
- display decoration;
- posture and gait styling.

**Magnitude:**
- The sex shift is smaller than individual variation in every domain: trunk ±10 % individually vs a +6 % mean shift; pelvis ±7 % vs +3 %.
- Rule: **sex shifts the centre of the soft distribution; it never extends the species hard bound** (a10, a11).

A **moderate option** is available if the author wants a more visible difference: trunk at the +10 % species maximum (a9) passes every rule. I recommend low, because the brief is "biologically coherent", not "always tellable".

## 3. Female whole-body reference (`v19_01`, `v19_02`)

**Placement:** a central point in the same envelope: 187.9 cm, Balanced, reference composition (the same centre as the male), plus the §2 tendencies.

**Change accounting** (equal stature, frame and composition; measured):

| Quantity | Male / reference | Female reference | Difference |
|---|---|---|---|
| Standing height | 187.9 cm | 187.9 cm | 0 |
| Lower axial trunk (hip → costal margin) | — | — | **+1.8 cm (+5 %)**, from the warp |
| Leg and thorax segments | — | — | −1.1 % each (stature held constant) |
| Head length / width | 31.87 / 14.19 cm | 31.89 / 14.20 cm | ~0 (no head dimorphism) |
| Shoulder breadth | 38.73 cm | 38.32 cm | −1.1 % (stature normalization only) |
| Thoracic depth / width | 0.880 | 0.880 | 0 |
| Pelvic width (incl. thighs) | 41.73 cm | 42.27 cm | **+1.3 %** |
| Tail length | 121.4 cm (64.6 % H) | 121.5 cm (64.7 % H) | 0 |
| Tail root area | 527 cm² | 516 cm² | −2.1 % (normalization side effect; RSI 1.01, inside the soft core) |
| Body volume / free-tail share | 136.9 L / 15.5 % | 135.2 L / 15.3 % | −1.3 % |
| Lean needed to stand over the feet | 8.82° | 8.80° | 0: counterbalance unchanged |

**Audit of the order's list:**
- **Unchanged:** stature, frame, shoulder relationship, limbs, hands/feet, neck, head proportion, tail root, tail length and fullness, muscle and adipose distribution.
- **Kept the same:** thoracic width/depth ratio.
- **Changed:** axial trunk longer; pelvis/sacrum slightly wider in the skeletal band only, with the sacral platform and posterior organization unchanged.
- **Centre of mass and counterbalance:** identical within 0.02°.

The posterior mass and load path are preserved, and the female reads as the same species in neutral grey without colour or clothing.

## 4. Reproductive / sex-anatomy boundary

**Is externally visible primary-sex anatomy needed for the standard unclothed reference?** **No**, for either sex. The ventral pelvic field is the same closed scale field on the male and the female (`v19_05`, ventral view).

**What must differ in pelvic-floor or external morphology?** Nothing externally beyond the subtle pelvic-band tendency. There is no external genital anatomy, no mammary anatomy, no buttock and no cleft.

**Deliberately unspecified (not needed for character creation):**
- reproductive mode (oviparity or viviparity, clutch or brood);
- internal reproductive organs;
- the morphology of any vent or cloacal opening;
- mating behaviour;
- maturation and fertility timing.

The result is non-mammalian, as canon requires.

## 5. Cranial identity and displays

**Sex does not affect** skull dimensions, rostrum, jaw depth, orbital architecture or display incidence/size/base/shape at first pass.

The **frozen naked skull is valid for both sexes** and stays recognizably Saurin without displays (`v19_06`).

The whole display family is shown on the female (`v19_07`): naked, minimal ridges, swept-back pair, strong mixed/asymmetric, restrained crest. All PASS.
- A female with strong displays is valid, and so is a male without displays (the male reference is naked).
- Displays are not sex markers.

A possible weak male weighting of display size, as in some lizards, is listed OPEN but **not recommended** under §102.

## 6. Surface biology

**No sex effect is asserted** on:
- scale size or field behaviour;
- the ventral field;
- keratin;
- claws;
- baseline pigmentation/pattern;
- display coloration.

The female uses the identical Regional Scale Architecture. Two things are recorded only, so later work doesn't contradict this pass:
- Any future seasonal or breeding coloration would be a separate, OPEN decision.
- Pink/purple or any colour-as-sex coding is excluded.

## 7. Composition and creator controls (`v19_04`)

**Same four layers:**
- Biological Anatomy (sex lives here as a slot with soft distribution shifts);
- Skeletal Frame;
- Physical Composition;
- Personal Presentation.

Narrow, Broad, low/high muscle and low/high fat on the female all use the same maps and rules as the male. High fat is ventral/flank/graded-caudal volume, **not an hourglass**. Low fat is the same skeleton, **not a "reduced male"**.

**Sex is not a body preset.** Height, frame, muscle, fat, head, tail and displays are independent of sex.

**Controls whose distribution changes with sex:**
- lower-trunk length: the soft centre moves +6 %;
- pelvic band width: the soft centre moves +3 %.

Hard bounds are identical for both sexes.

**Randomization and NPCs:** pick sex, then sample the trunk and pelvis soft distributions from the shifted centres; everything else is sampled exactly as for the other sex, under the same validity system (Part 7 §264 parity preserved).

## 8. Male/female boundary and overlap tests (`v19_02`, `v19_03`, `v19_08`)

- **Male vs female reference and equal-height pair (180 cm, Balanced):** the trunk is the only change.
- **Deliberate overlap:**
  - a male with trunk +6 % / pelvis +3 % (inside individual variation) is **geometrically identical** to the female reference;
  - a female at the male mean is identical to the male reference.
- **Tail extremes on the female under the existing coupling rules:**
  - 55 % with coupled base 0.83: PASS;
  - 78 % with base 1.15: PASS, +3.0° lean (edge);
  - Broad + 80 % with base 1.16: PASS, RSI 1.11, +2.6°.

  The tail rules are sex-neutral.

**Answer to the test question:** yes. The sexes overlap completely as individuals, while the small real dimorphism stays coherent with Saurin biology: trunk capacity, in the direction of an existing racial trait.

## 9. Anti-stereotype stress matrix (`v19_09`)

| Case | Status | Why |
|---|---|---|
| Female: tallest + Broad + high muscle | PASS | Every tail, balance and head rule holds (RSI 0.83, −0.6°) |
| Male: shortest + Narrow | PASS | — |
| Female with strong swept / mixed display | PASS | `v19_07` |
| Male with minimal / naked display | PASS | The male reference |
| Female: high fat | PASS | Same distribution as the male; no hourglass, no human hip |
| Female: low fat | PASS | Same skeleton; not a reduced male |
| Equal-height / equal-frame male and female | PASS | Only the trunk differs |
| Male: low muscle + high fat + Narrow | PASS | — |
| Female trunk at the species maximum (+10 %) | PASS | — |
| Female trunk requested at +16 % (mean shift stacked) | **CONSTRAIN** | Clamped to the +10 % species bound: sex never extends the racial envelope |
| Female pelvis requested at +10 % | **CONSTRAIN** | Clamped to the +7 % species bound |
| Female Broad + 80 % tail | PASS | Tail rules are sex-neutral |

There are no FAIL cases: no combination makes sex behave like a hidden body preset.

## 10. GLB comparison at closure

**Not possible:** the GLB was not accessible (§0). Nothing was preserved from it or rejected from it.

## 11. Closure criteria, as tested

| Criterion | Result |
|---|---|
| Same species without colour or clothing | Yes |
| Frozen racial identity survives | Yes; nothing racial changed |
| No human-female template | Yes: no breasts, hourglass, human pelvis, feminized face, eyelashes or colour coding |
| Pelvic/tail integration credible | Yes: sacral platform and tail root unchanged; counterbalance identical |
| Sex separate from frame and composition | Yes |
| Substantial overlap possible | Yes; geometrically identical individuals exist |
| Displays coherent | Yes |
| Creator / randomization / NPC parity | Yes |
| New blocking contradiction | None |

## 12. OPEN / CLOSED

**Proposed CLOSED** (pending author review; canon not yet edited):
- Dimorphism model: low, regionally mixed.
- Female tendencies: lower trunk +6 %, pelvic band +3 %, both soft mean shifts inside unchanged species hard bounds.
- No sex difference in stature, frame, composition, head, skull, displays, tail, surface or claws.
- No external primary-sex anatomy in the standard reference.
- Sex shifts soft distributions only; it never extends the racial envelope.
- Creator/NPC parity.

**OPEN:**

| # | Item |
|---|---|
| 1 | The internal-gestation assumption that justifies the trunk tendency (author/canon confirmation) |
| 2 | Reproductive mode and internal anatomy; vent morphology. Deliberately unspecified; not needed for character creation |
| 3 | Whether any weak display-size or jaw-mass weighting should ever exist. Not recommended under §102 |
| 4 | Seasonal / breeding coloration |
| 5 | Final magnitude: low (recommended) vs moderate (+10 % trunk, already validated) |
| 6 | The female GLB comparison, if the file is provided |
| 7 | Age-related sex effects (out of scope) |

**STOP: diagnostic female / sex-related anatomy package. Awaiting ChatGPT author review before any canonization.** No universal review, facial-control architecture, rigging, animation, clothing, UE5 or pigmentation-system pass.

— Claude
