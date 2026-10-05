# Saurin Creator Biology Variation (DIAGNOSTIC / NOT FINAL)

**Author:** Claude
**Responds to:** `reviews/chatgpt-saurin-creator-biology-variation-order.md` (909c0e0)
**Prerequisite:** Anatomical/Surface Convergence CLOSED (aff1b52)
**Phase:** design validation only. No UE5, no production morphs, no rig, no creator UI, no external sex anatomy.

**Candidate parameter/coupling table:** `reviews/saurin-creator-parameter-register.md`. It is written to be reconciled into `specs/saurin/SAURIN_V1.md` later.

**Images:** `reviews/images/saurin-creator-biology/`
**Numbers:** `v17_metrics.json` (every variant), `v17_tailgrid.json` (192-point tail grid), `v17_tail_rule.json`, `v17_display_metrics.json`.
**Tools:** `tools/rodin/creator-biology/`

## 1. Method: derived, never modified

The frozen reference was **not touched**. Every variant is the reference base mesh, or its scaled surface, passed through smooth, continuous region warps:

| Area | Warps used |
|---|---|
| Stature | Uniform scale |
| Segments | Segment stretches; arms follow the girdle and the tail follows its root |
| Frame | Torso breadth bands; limb and joint girth about each limb's section centroid |
| Composition | Real soft-tissue volume along smoothed normals with regional maps |
| Tail | Tail rebuilt along its own centreline, so length, carriage, base, fullness and cross-section are separate controls |
| Head | Head-local warps in the skull's own frame for rostrum, cranium, jaw and orbit |

The cranial display range was rebuilt from the accepted display generator with only its parameters scaled. That generator is `wf_saurin_head66.py`, a wrapper around the unchanged head65.

**Stature is held at 187.9 cm** for every variant except the stature rows, so proportion changes are not disguised by scale.

**Measurements per variant:**
- standing height;
- head length ratio and rostral index;
- thoracic depth/width;
- tail length (% H) along the relaxed centreline;
- true planar tail cross-sections, which give the root-sufficiency index, peak loss rate, and mid and distal area fractions;
- whole-body volume and uniform-density centre of mass, which give the forward lean needed to stand over the feet;
- tail ground clearance;
- tail reach behind the heel.

**Status definitions:**
- **PASS:** inside every hard bound.
- **CONSTRAIN:** violates a relationship, but the creator restores validity by adapting a dependent, unlocked control (§159 behaviour).
- **FAIL:** the requested combination is itself one of the named invalid shapes, so the creator must refuse it rather than adjust it.

**Value types (the order's four categories):**

| Type | Meaning |
|---|---|
| Reference | Measured on the frozen model |
| Soft distribution | Candidate centre and weighted range for presets, randomization and NPCs |
| Hard boundary | Candidate validity limit, or canon where marked |
| OPEN | Unresolved |

## 2. Package

| Order item | File |
|---|---|
| Reference (identical cameras used throughout) | `v17_01_reference.jpg`, `v17_01b_reference_close.jpg` |
| Neutral + single-variable extremes: stature and segment proportions | `v17_02_body_proportion.jpg` |
| Single-variable extremes: breadth, depth, extremities | `v17_03_body_breadth.jpg` |
| Skeletal frame and physical composition | `v17_04_frame_composition.jpg` |
| Tail single-variable extremes | `v17_05_tail_singles.jpg` |
| Tail coupling diagnostics | `v17_06a_tail_profiles.jpg`, `v17_06b_tail_envelope.jpg`, `v17_06c_balance.jpg`, `v17_06d_tail_coupling_cases.jpg` |
| Cranial identity, displays disabled (single extremes) | `v17_07a_cranial_rostral.jpg`, `v17_07b_cranial_vault.jpg` |
| Cranial identity, displays disabled (coupled extremes) | `v17_08_cranial_coupled.jpg` |
| Combined-extreme stress matrix | `v17_09a_combined_matrix.jpg`, `v17_09b_combined_matrix.jpg` |
| Display-family range | `v17_10a_display_range.jpg`, `v17_10b_display_range.jpg` |
| Displays on extreme crania | `v17_11_display_cranial.jpg` |
| Parameter/coupling table | `reviews/saurin-creator-parameter-register.md` |
| Unresolved decisions | §10 below |

## 3. Body: single variables, frame, composition

### 3.1 Single variables

All body single-variable extremes are **PASS** at the tested hard bounds:

| Parameter | Range tested | Notes |
|---|---|---|
| Stature | 168 / 208 cm | Canon limits |
| Head proportion | ±8 % | Head length 0.157–0.182 H |
| Neck length | ±15 % | — |
| Neck depth | ±10 % | — |
| Thoracic depth | ±8 % | d/w 0.81–0.95 |
| Thoracic width | ±7 % | — |
| Axial trunk length | ±10 % | — |
| Shoulder breadth | ±8 % | d/w 0.82 at the broad end |
| Pelvic width | ±7 % | — |
| Arm length | ±6 % | — |
| Leg length | ±6 % | — |
| Hand size | ±8 % | — |
| Foot size | ±8 % | — |

In the renders (`v17_02`, `v17_03`) the axial/pelvic/tail architecture keeps every one of them Saurin. The tail still reads as inevitable on the body at every stature and proportion.

Thoracic depth/width is the only body ratio that approaches its bound. It does so in combination (§8), not alone.

**Stature is isometric for every relationship tested:** tail % H, root sufficiency, taper, balance and rostral index are all unchanged at 168 and 208 cm. Stature therefore needs no coupling of its own. The tail is defined in % H, so a taller Saurin carries a proportionally longer tail automatically.

The one physical effect of size is that isometric bending stress in the tail root rises about 11 % at 208 cm. I report this but do **not** use it as a limit. The RSI in §4 is normalized for size.

### 3.2 Skeletal frame (Narrow / Balanced / Broad)

These are editable starting distributions, not castes. The register (§B) lists the exact multipliers.

**What changes:**
- shoulder breadth;
- thoracic width (and depth by ±2 % only);
- pelvic width;
- limb and joint girth;
- hand and foot breadth;
- the frame component of the tail base.

**What is protected:**
- every long-bone and axial length;
- the head;
- pelvic depth and sacral-caudal organization;
- thoracic depth/width ≥ 0.80. Measured: Narrow 0.94, Broad 0.82.

**Result:**
- Narrow remains Saurin through axial/pelvic/tail architecture.
- Broad gets broader without becoming massive. It is a girdle-and-girth change, not a Gorrund-style axial mass change.
- Frame moves balance by about ±0.8°. Broad is better.

### 3.3 Physical composition

Composition is kept fully separate from frame.

**Muscle** adds up to 0.9 cm of real volume (+10.7 L) in:
- upper arm and forearm;
- shoulder girdle;
- epaxial neck and dorsal trunk;
- thigh and posterior shank;
- proximal-mid tail.

Joints, hands and feet are excluded. Low muscle removes up to 0.45 cm.

**Fat** adds up to 2.2 cm (+20 L at high) in:
- the ventral abdomen (strongest);
- flank and hip;
- the tail, graded over its proximal half;
- the throat (minor);
- a light general subcutaneous layer.

**Not imported from humans:**
- no pectoral blocks;
- no abdominal segmentation;
- no gluteal or buttock mass;
- no bodybuilder width.

High fat reads as a heavier adult Saurin (`v17_04`), not a dry lizard and not a human.

**Rule found (x25, FAIL):** concentrating caudal fat at the caudal base creates a mass step: peak loss rate 1.56 × the reference, the "thick root + thin appendage" read the Gate 6 work removed. Caudal adipose must be **graded over the proximal ~half** of the tail. With that distribution, high fat keeps the tail inside every bound (RSI 0.84, loss rate 0.99).

Exact Saurin adipose tendencies remain OPEN (§23/§153). The graded-caudal pattern is a candidate.

### 3.4 Finding: the frozen neutral pose is not statically balanced

With uniform density, the reference centre of mass sits at f = −11.5 cm. That is **6.3 cm behind the heel contact**.
- Free tail: 21.2 L of 136.9 L, centred 48 cm behind the body.
- Body without the free tail: centre of mass at f ≈ −1.2.

To stand with its centre of mass over the forefoot side of the ankle, the reference needs about **8.8° of forward whole-body lean**.

Real tissue densities make this worse, not better: lungs lighten the thorax and the tail is dense muscle and bone.

This is not an anatomy defect for this pass to fix. The frozen target is not to be reopened. It means the frozen pose is a **reference stance**, and the balanced neutral standing posture is a Part 5 decision. Candidate solutions include a slight forward axial inclination, a lower tail carriage, or both.

I therefore use **balance relative to the reference**: no variant may need more than **+3.0°** of lean beyond the reference (soft +1.5°). This is listed as an unresolved author decision (§10).

## 4. Tail coupling

**Data:** a 3 × 8 × 8 measured grid (`v17_06b`), plus the single and combined variants.
- fullness t ∈ {0.85, 1.0, 1.15};
- length 52–84 % H;
- base 0.80–1.30.

**Measured relationships:**

| Relationship | Result |
|---|---|
| Standing height × tail length | Isometric. Tail length is defined in % H, so stature needs no tail coupling. |
| Tail length × base × taper (root sufficiency) | Size-normalized root bending index **RSI ≈ k² / b^1.7** (k = length multiplier, b = base multiplier). A 55 % tail on the reference base is oversized at the root (0.72); an 80 % tail on it is 1.53. Constant-sufficiency centre line: **b_c(k) = k^1.18**. |
| Pelvis/sacral dimensions × tail-base mass | The tail base carries a frame component (Narrow ×0.95, Broad ×1.06) that follows pelvic width. Pelvic depth and sacral integration are locked: base mass is never obtained by changing the pelvis. |
| Composition × visible tail muscularity | Tail muscularity is not its own slider. It follows Composition (proximal-mid emphasis, zero at the tip). High muscle: RSI 0.90, loss rate 0.97. High fat (graded): 0.84 / 0.99. |
| Tail mass × resting curvature | Carriage +8° lift to +10° droop changes clearance and reach, not balance (±0.03°). Candidate correlation: heavier tails rest lower. No ground contact in any valid variant (minimum tip height 58.9 cm). Pose itself is Part 5. |
| Tail proportions × whole-body counterbalance | Balance scales with free-tail volume share: about 92° per unit share. The +3° limit corresponds to a **free-tail volume share ≤ ~19.5 %** (reference 15.5 %). This is what caps long tails. |

**Validity rules (candidate hard / soft):**

| Rule | Hard | Soft |
|---|---|---|
| RSI | 0.75–1.20 | 0.85–1.10 |
| Peak area-loss rate | ≤ 1.25 × ref (Gate 6 abrupt-taper guard) | ≤ 1.12 |
| Mid-tail area / root | 0.27–0.48 (threadlike / cylindrical guard) | 0.31–0.44 |
| Area at 25 % from tip / root | ≥ 0.065 | — |
| Extra lean vs reference | ≤ +3.0° | — |

**Valid base band (reference fullness):**

| Tail length (% H) | Valid base band |
|---|---|
| 55 | 0.80–0.98 |
| 61 | 0.84–1.12 |
| 65 | 0.90–1.19 |
| 71 | 1.01–1.27 |
| 77 | 1.12–1.16 |
| 80 | none on the reference body |

**Canon 55–80 % H, as validated:**
- The whole canon range is valid **only with the base coupled to length**.
- On a Balanced frame at reference composition, the longest valid tail is about **78 % H**: x28, base 1.15, +3.0°.
- The **80 % end needs a Broad frame**: x27, base 1.16, RSI 1.09, +2.6°.
- A Narrow, high-fat body tops out around 72 % (x18).
- The creator should cap tail length by body mass rather than by a fixed number.

**Rejected or auto-constrained (the order's list):**

| Invalid shape | How it is caught |
|---|---|
| Root too small for distal mass | RSI > 1.20. Base raised automatically (x03, tb_lo, tn_hi). |
| Oversized root with threadlike distal tail | RSI < 0.75 → base lowered automatically (tn_lo, x04, x15, x20). Requested outright as heavy base + low fullness, it is **FAIL** (x21: loss rate 1.46, mid 0.27). |
| Attached-appendage / cylindrical tail | Mid area > 0.48: **FAIL** (x22: short + thin base + full mid, 0.51). |
| Tail mass inconsistent with pelvis/load path | Base mass only through the tail rule plus the frame component; pelvis locked. |
| Implausible balance | Extra lean > +3° (x18, x26 FAIL on the reference body; x14 capped). |
| Hidden return of the Gate 6 failures | Loss-rate guard plus the graded caudal-fat rule (x25 FAIL). |

**There is no tail-off control.** Every variant keeps a complete, mandatory tail.

**Creator behaviour:**
- Tail length is the driver; base and fullness are dependents.
- The base slider moves inside the band for the current length.
- The length slider stops where no base exists.
- Randomization samples base around k^1.18.
- Tail reach is reported for Part 5 world validation: the 208 cm + 80 % extreme reaches 170 cm behind the heel, about 208 cm overall body length.

## 5. Cranial identity, displays disabled

**Single-variable extremes** (`v17_07a/b`, naked skull) are all **PASS**:

| Control | Range tested |
|---|---|
| Rostrum length | −15 / +20 % |
| Rostral base width | ±12 % |
| Anterior rostral width | ±15 % |
| Rostral depth | ±12 % |
| Posterior jaw depth | −12 / +15 % |
| Cranial length | ±8 % |
| Cranial width | ±8 % |
| Cranial depth | ±7 % |
| Orbit size | ±8 % |

At every extreme the skull keeps:
- the compact projecting rostrum (rostral index 0.260–0.323; reference 0.288);
- the layered rostral-cranial integration;
- the final brow → temporal/postorbital transition (frozen planes, carried through the warp);
- the embedded orbit;
- the deep jaw base;
- no chin, lips, external nose or pinnae.

**Coupled extremes** (`v17_08`):

| Case | Combination | Status | Why |
|---|---|---|---|
| x05 | Longest rostrum + narrow cranium | PASS | Index 0.323, at the edge of the dragon-wedge guard (0.335) |
| x06 | Shortest rostrum + broad cranium | PASS | Index 0.260, at the rostral floor (0.255) |
| x24 | Shortest rostrum + long cranium | **CONSTRAIN** | Index 0.248 is below the floor; the rostrum minimum rises with cranial length |
| x19 | Long rostrum + shallow jaw + shallow rostral depth | **CONSTRAIN** | Canon §40; above +10 % rostral length, jaw depth and rostral depth are held at ≥ reference |

The **rostral floor** (index 0.255) is a candidate derived from the frozen reference. Its required non-overlap with the Marchfolk/Grask/Gorrund projection ranges (§39, §146) needs a numeric cross-race check before it is canon.

Orbital **placement** is locked to the frozen brow/orbit architecture. Only size varies.

## 6. Display anatomy as a creator family

**Display range** (`v17_10a/b`, `v17_display_metrics.json`):

The accepted generator was rebuilt with scaled parameters. Same naked skull and closure surface; 18 builds.

| Variant | Measured | Status |
|---|---|---|
| Neutral naked | Complete skull | PASS |
| Minimal ridges | 0.4 cm relief | PASS |
| Low hornlets (reference) | 3 pairs, 2.0 cm, footprint 0.29 | PASS |
| Hornlets: count 1 pair (brow only) | — | PASS |
| Hornlets: length ×1.5 | 3.2 cm, footprint 0.19 | PASS; family edge toward small horns |
| Hornlets: ×0.7, base ×0.85 | — | PASS |
| Hornlets: ×1.5 on base ×0.7 | Footprint 0.135 | PASS by rule; reads spiky, soft edge |
| Swept-back (reference) | Footprint 0.069, neutral neck clearance 8.7 cm | PASS |
| Swept: length ×0.75 | Footprint 0.092 | PASS |
| Swept: length ×1.25 | Footprint 0.055 < 0.060 | **CONSTRAIN**: base follows length (≥ ×1.10) |
| Swept: 10° lower | Neck clearance 7.1 cm at neutral | PASS |
| Swept: 12° raised | +0.5 cm above the roof | PASS |
| Swept: ×1.25 on base ×0.8 | Footprint 0.044 | **FAIL**: long structure on a reduced base, §102 |
| Mixed/asymmetric (reference) | — | PASS |
| Mixed: asymmetry 0.70 | — | PASS (natural edge) |
| Restrained crest 2.43 cm (reference) | — | PASS (current upper reference) |
| Crest 1.6 cm | — | PASS |
| Crest 3.0 cm | Above the 2.5 cm upper reference | **CONSTRAIN** (capped) |

**Can vary safely (candidate):**
- count: 1–3 pairs for hornlets;
- length: ×0.7–1.5 for hornlets, ×0.75–1.15 for swept horns without a base change;
- base footprint: ratio ≥ 0.060, so the base follows length;
- sweep: −12° … +10°, neck clearance ≥ 7 cm at neutral;
- paired asymmetry: ≥ 0.70;
- crest height: 1.6–2.5 cm.

Measured display volumes from the patch difference were too noisy to use (±10 cm³ meshing noise), so the moment limit stays OPEN (§10). Length, footprint, clearance and height are the measured controls.

**Rules (candidate):**
- **Footprint:** base radius / chord ≥ 0.060 (the accepted swept pair is 0.069).
- **Crest height:** ≤ 2.5 cm above the roof. The accepted restrained crest (2.43 cm) is the current upper reference, as the order requires; taller crests are outside the current approval rather than biologically impossible.
- **Paired asymmetry:** down to 0.70 length ratio counts as natural; beyond that it belongs to the acquired-injury layer.
- **Placement:** displays grow only from §101 attachment regions.
- **Moment and clearance:** count and length are bounded by the display moment index and by neutral neck clearance. Clearance through head/neck motion is a Part 5 test.

**Firewalls:**
- Display carries **no sex, culture, class, status or gameplay meaning**.
- Display sits in the hair-selection slot but **is not hair**.
- No dragon/dinosaur horn architecture was introduced: every variant stays within the six accepted families and their attachment logic.

**Displays on extreme crania** (`v17_11`): the strongest displays (mixed/asymmetric, swept-back) and near-naked ridges, on the long-narrow and short-broad cranial extremes. The displays re-seat on the warped skull and follow it. They neither cause nor hide a skull failure; the skull verdict comes from §5 with displays off.

All six cases are PASS:
- The displays are carried by the same head-local warp as the skull. On a broad cranium the swept pair sits wider; on a long-narrow skull, closer.
- None of them changes the skull verdict.
- The near-naked heads read as Saurin on the skull alone.
- The short-rostrum + broad-cranium skull sits at the rostral floor with or without displays, as it should.

## 7. Surface phenotype variability (rules, not rendered)

The accepted Regional Scale Architecture becomes variation rules **within** fields:

| Field type | Size | Relief | Other |
|---|---|---|---|
| Structural scutes (cranial roof, nape, upper dorsal thorax, dorsal forearm and shin, dorsal tail) | ±20 % | ±25 % | Local shape and orientation follow the existing flow fields |
| Expressive fine fields (eyelids, mouth margin, rostral sides) | ±10 % | ±25 % | Never coarsened toward structural size |
| Articulation fields | ±10 % | — | Fineness only; must stay finer than the adjacent structural field |
| Ventral organization | — | — | Transverse-plate tendency ±15 % in plate width, never pebbled |
| Contact surfaces | — | Pad thickening ±25 % within the contact field | — |

- The tail scale-size gradient (root → tip) is kept, scaled with tail length.
- **Field boundaries and functions are locked.**
- **No global "scale size" control** (§85, §147).
- Warped variants carry their scales with the body, so a structural scute stretches with a longer tail.
- When anatomy changes, the closure surface code regenerates scale size from the region map, so stretching does not accumulate. This is how the frozen pipeline already works.
- Gate 8 pigmentation, pattern and material are unchanged. Pattern coordinates ride on the deformation, so pattern families survive every variant.

## 8. Combined-proportion stress matrix

The order's 12 cases plus 14 more (`v17_09a/b`):

| # | Combination | Status | Key measurements / reason |
|---|---|---|---|
| x01 | Shortest + broadest frame | PASS | Thoracic d/w 0.82; balance −0.8° |
| x02 | Tallest + narrowest frame | PASS | RSI 1.09; balance +0.8° |
| x03 | Long tail (80 %) + minimum base | CONSTRAIN | RSI 2.01 → base raised to ≥ 1.16; then balance caps length at ~78 % (Balanced body) |
| x04 | Short tail (55 %) + maximum base | CONSTRAIN | RSI 0.58 (oversized root) → base lowered to ≤ 0.98 |
| x05 | Longest rostrum + narrow cranium | PASS | Rostral index 0.323 |
| x06 | Shortest rostrum + broad cranium | PASS | Rostral index 0.260 (floor) |
| x07 | Max head proportion + Narrow frame | PASS | Head 0.182 H; no bobble-head read |
| x08 | Min head proportion + Broad frame | PASS | Head 0.157 H |
| x09 | High muscle + low fat | PASS | — |
| x10 | Low muscle + high fat | PASS | Graded caudal fat |
| x13 | Long tail (80 %) + drooped carriage | CONSTRAIN | As x03; minimum tip height 58.9 cm |
| x14 | Tallest + longest tail + max base | CONSTRAIN | Stature doesn't help (isometric): RSI 1.22, +3.4° → length capped ~78 % |
| x15 | Shortest + short tail + high fat | CONSTRAIN | RSI 0.61 → base lowered |
| x16 | Long neck + max head | PASS | — |
| x17 | Long legs + short trunk + short neck | PASS | — |
| x18 | Narrow + high fat + long tail | CONSTRAIN | RSI 1.40 and +3.6° → a Narrow body carries ≤ ~72 % |
| x19 | Long rostrum + shallow jaw + shallow rostrum | CONSTRAIN | §40 coupling |
| x20 | Broad + high muscle + max tail base | CONSTRAIN | RSI 0.65: frame and muscle already thicken the base, so the base slider is capped |
| x21 | Long tail + max base + low fullness | **FAIL** | Heavy root + threadlike tail (loss rate 1.46) |
| x22 | Short tail + min base + full mid | **FAIL** | Cylindrical / attached appendage (mid 0.51) |
| x23 | Broad + shallow + wide thorax | CONSTRAIN | d/w 0.73 → thoracic depth floor scales with breadth |
| x24 | Short rostrum + long cranium | CONSTRAIN | Rostral index 0.248 < floor |
| x25 | High fat, caudal fat concentrated at the base | **FAIL** | Mass step, loss rate 1.56 |
| x26 | Long tail (80 %) + coupled base, reference body | **FAIL** | +3.8° lean |
| x27 | Broad + long tail (80 %) + coupled base | PASS | RSI 1.09, +2.6° |
| x28 | Reference body, longest valid tail (78 %) | PASS | Base 1.15, +3.0° (edge) |

Strongest display + extreme cranium, and near-naked + extreme cranium: see §6 (`v17_11`).

## 9. Sex-related anatomy

**What canon supports today:**
- §24, §62, §154 and §235 all state that Saurin sex-related anatomy is **non-human and not yet designed**.
- Selecting it may not determine height, frame, muscularity, body fat, tail length or thickness, face, rostrum, displays, coloration, culture, class or personality.
- Any population correlations must be soft and overlapping.

**Answers to the order's three questions:**
1. *Which visible skeletal/surface differences are justified by established Saurin biology?* **None yet.** Nothing in canon establishes a skeletal or surface difference.
2. *Does canon support distinct dimorphic ranges?* **No.** Every range in the register is therefore shared. No dimorphic range was created.
3. *What remains genuinely unresolved?* Whether any dimorphism exists, and in which domains it would live: overall size distribution, pelvic/caudal-base proportion, display-frequency weighting, pattern contrast. Its magnitude and degree of overlap. The underlying reproductive biology, which this pass deliberately leaves untouched. Whether the creator exposes a sex-related control before that biology exists.

The creator architecture must keep a reserved, empty biological slot. No external genital anatomy was designed.

## 10. Unresolved decisions (author / canon)

1. **Neutral standing balance.** The frozen pose needs ~8.8° forward lean (uniform density) to stand over the feet. This must be decided before tail limits become absolute.
   - Which posture or carriage solution applies (Part 5 posture/animation)?
   - Should balance in the creator stay relative to the reference (+3° candidate), or move to an absolute limit once posture is fixed?
2. **Tail range vs balance.** Canon allows 55–80 % H. Validated: 80 % only on Broad/heavier bodies; ~78 % on the reference body; ~72 % on Narrow, high-fat bodies. Accept "tail cap follows body mass", or change canon?
3. **Caudal base landmark.** Tail length here is measured from the axis point at the posterior pelvic plane (121.4 cm on the reference). Canon says "from the caudal base"; the exact landmark needs fixing.
4. **Numeric rostral floor.** The candidate rostral index of 0.255 needs the cross-race non-overlap check against the Marchfolk/Grask/Gorrund projection ranges (§39, §146).
5. **Lower-trunk minimum.** The trunk must stay longer than the Marchfolk tendency (§6). A numeric cross-race floor is needed for A17.
6. **Gorrund boundary for Broad + high muscle.** The Broad frame here is girdle/girth only. A numeric "never Gorrund" check needs Gorrund reference dimensions.
7. **Adipose distribution tendencies (§23/§153).** The candidate pattern (ventral, flank/hip, graded caudal-proximal, minor gular) needs author acceptance, and so does the graded-caudal rule.
8. **Crest above 2.5 cm.** Stays outside the current approved range unless the author widens it. Prominent horns, spikes and plates (§100, which needs bony cores) were not extended in this pass.
9. **Display moment and neck clearance through the head/neck range of motion** (Part 5).
10. **Sex-related anatomy** (§9): whether dimorphism exists at all, and where.
11. **Orbital spacing** variation (locked here; untested).
12. **Claw and digit proportion** variation (§151): not exercised geometrically.
13. **Density model** for balance: uniform here. Should lungs and tail tissue be modelled?
14. **World-space limits** for the longest tails (doors, corridors, seating, crowds; Part 5): up to 170 cm tail reach behind the heel.

**STOP: complete diagnostic package. Awaiting author review.** The frozen reference was not modified. No UE5, production morph targets, rig, animation, clothing/equipment fitting, creator UI, gameplay modifiers, external sex anatomy or aging implementation.

— Claude
