# Saurin Creator Biology — Candidate Parameter / Coupling Register (DIAGNOSTIC)

**Author:** Claude
**Status:** CANDIDATE. It is written to be reconciled later into `specs/saurin/SAURIN_V1.md` (§§4, 10–11a, 21–24, 40, 73, 85, 102, 137, 145–160) and is **not** canon until the author accepts it.
**Companion report:** `reviews/claude-saurin-creator-biology-variation.md`
**Measurements:** taken on the frozen closure reference (aff1b52) and on warps derived from it. Lengths are in cm, standing height excludes the tail, and "ref" is the frozen value.

## How to read the columns

| Column | Meaning |
|---|---|
| **Ref** | Measured value on the frozen reference |
| **Soft** | Candidate central distribution for presets, Biological Randomization and NPC generation: roughly the central 80 %, with weighted tails beyond it |
| **Hard** | Candidate validity boundary for Advanced Mode. *Canon* marks a value the spec already sets |
| **Class** | One of five: **IND** independent, **COR** correlated (soft population correlation only, no lock), **CPL** coupled (a relationship constraint is enforced), **PRES** presentation-only, **LOCK** locked racial biology |
| **OPEN** | Truly unresolved; listed in report §10 |

Percentages are multipliers on the reference dimension, measured at constant standing height unless the row says otherwise.

## Measured reference (frozen)

**Stature and head**
- Standing height 187.88 cm.
- Head length (rostral tip to occiput) 31.87 cm, which is 0.170 H.
- Rostral projection (tip ahead of the eye centres) 9.18 cm; rostral index 0.288.
- Head width 14.19 cm.

**Trunk**
- Thoracic depth/width 0.88.
- Shoulder breadth (torso) 38.7 cm.
- Pelvic width (with thighs) 41.7 cm.

**Tail**
- Length along the relaxed centreline, caudal base to tip: 121.4 cm (64.6 % H).
- Free-tail root area 527 cm²; mid-tail area 0.371 × root.

**Mass and balance**
- Body volume 136.9 L; free-tail volume 21.2 L (15.5 %).
- Uniform-density centre of mass at f = −11.5 cm, which is 6.3 cm behind the heel contact (see report §3.4).

## A — Biological Anatomy

| # | Parameter | Class | Ref | Soft | Hard (candidate unless canon) | Coupled with / rule | Status |
|---|---|---|---|---|---|---|---|
| A1 | Standing height | IND (COR with nothing biological) | 187.9 cm | 176–200 cm | **168–208 cm (canon §4)** | All absolute dimensions scale with it; tail length is defined in % H | Valid across the full range; extremes rendered |
| A2 | Head-to-body proportion | CPL | 0.170 H | ±4 % | ±8 % (0.156–0.184 H) | Neck depth and frame; +8 % head-scale decision is the centre | Valid; combinations x07/x08/x16 PASS |
| A3 | Cranial length | CPL | — | ±4 % | ±8 % | **Rostral floor:** cranial length and rostrum length together must keep rostral index ≥ 0.255 | x24 constrained |
| A4 | Cranial width (temporal breadth) | COR (weak, with frame in randomization only) | 14.19 cm | ±4 % | ±8 % | Canon §60: cranial robusticity varies independently; no frame lock | Valid |
| A5 | Cranial depth (vault / posterior depth) | IND | 14.95 cm | ±3.5 % | ±7 % | Must not inflate the vault; adult-read guard §61 | Valid |
| A6 | Rostrum length | CPL | 9.18 cm projection | ±7 % | −15 % … +20 %, and rostral index 0.255–0.335 | **§40:** above +10 %, posterior jaw depth and rostral depth must be ≥ reference | x19 constrained |
| A7 | Rostral base width | CPL | — | ±6 % | ±12 % | Base width ≥ anterior width (taper preserved); integration with the orbital platform | Valid |
| A8 | Anterior rostral width | CPL | — | ±7 % | ±15 % | ≤ rostral base width | Valid |
| A9 | Rostral depth | CPL | — | ±6 % | ±12 % | With rostrum length (A6) | Valid alone |
| A10 | Posterior jaw depth / mandibular mass | CPL | — | ±6 % | −12 % … +15 % | With rostrum length (A6); deep jaw base is mandatory identity | Valid alone |
| A11 | Orbital size (visible opening / orbit) | CPL | — | ±4 % | ±8 % | Eyeball size and opening move together (§158); brow/orbit planes are frozen | Valid |
| A12 | Orbital placement / spacing | **LOCK** (≤ ±3 %, untested) | — | — | Locked to the frozen brow → temporal/postorbital architecture | — | OPEN numeric |
| A13 | Neck length | CPL | — | ±7 % | ±15 % | With head proportion and display moment | Valid |
| A14 | Neck structural depth | COR (with composition) | — | ±5 % | ±10 % | — | Valid |
| A15 | Thoracic depth | CPL | d/w 0.88 | ±4 % | ±8 %, and d/w 0.80–1.00 | **Depth floor scales with breadth:** d/w ≥ 0.80 (deep shell §7–8); ≤ 1.00 (not Vael thoracic depth) | x23 constrained |
| A16 | Thoracic width | CPL (frame) | — | via frame | ±7 % | With A15 | Valid |
| A17 | Axial trunk length | CPL | — | ±5 % | ±10 % | Lower trunk must stay longer than the Marchfolk tendency (§6) | Numeric cross-race floor OPEN |
| A18 | Pelvic width | CPL (frame) | 41.7 cm | via frame | ±7 % | Legs move with it; tail-base support follows the frame (B) | Valid |
| A19 | Pelvic depth / sacral integration | **LOCK** | — | — | Frozen Counterbalanced Pelvic-Axial Architecture | Tail base is carried **through** it, never by changing it | — |
| A20 | Shoulder breadth | CPL (frame) | 38.7 cm | via frame | ±8 % | Arms follow; thoracic d/w (A15) | Valid |
| A21 | Arm length | IND | — | ±3 % | ±6 % | Forearm emphasis relation locked (§17) | Valid |
| A22 | Leg length | CPL | — | ±3 % | ±6 % | Trunk and leg shares (§158); x17 PASS | Valid |
| A23 | Hand size | COR (stature, frame) | — | ±4 % | ±8 % | Grasp preserved | Valid |
| A24 | Foot size | COR (stature, frame) | — | ±4 % | ±8 % | Plantigrade contact preserved; slightly helps balance | Valid |
| A25 | Tail length | **CPL** | 64.6 % H (121.4 cm) | 58–72 % | **55–80 % H canon**, but reachable only through the tail rule (Tail rule section): ~78 % is the maximum on the reference body; 80 % needs a Broad frame | Tail base, tail fullness, frame/composition, balance | See Tail rule |
| A26 | Tail base mass / diameter | **CPL** (dependent) | root 527 cm² | b_c(k) ± 5 % | b ∈ [0.90 · b_c, min(1.18 · b_c, taper cap, balance cap)] | b_c = k^1.18 (keeps the root-sufficiency index at 1) | Rule |
| A27 | Tail taper profile (mid/distal fullness) | **CPL** | mid area 0.371 × root | ±6 % | ±15 %, subject to peak loss rate ≤ 1.25 × ref and mid area 0.27–0.48 × root | Low fullness plus a heavy base is the "heavy root + threadlike tail" failure | x21 FAIL |
| A28 | Tail muscularity | CPL — **not a separate slider**; driven by Composition (C1) | — | — | Follows the C1 range | Proximal-mid emphasis, zero at the tip | Valid |
| A29 | Tail resting curvature (neutral carriage) | COR (with tail mass) | — | ±4° | +8° lift … +10° droop; no ground contact; not rigidly horizontal; no scorpion curl | Candidate correlation: heavier tails droop more | Valid; pose itself is animation (Part 5) |
| A30 | Tail cross-section tendency | IND | — | ±5 % | ±10 % (rounder / broader / deeper) | §11a | Valid |
| A31 | Digit / claw proportion | CPL | frozen claws | — | §151 constraints: grasp and plantigrade/footwear | Not exercised geometrically this pass | OPEN test |
| A32 | Scale-field structural size / relief | CPL (per field) | RSA | Within each field: structural size ±20 %, relief ±25 %; fine fields ±10 % | **No global scale slider (§85, §147)**; field boundaries and functions locked | — | Rule only, not rendered |
| A33 | Cranial display anatomy | CPL (family + parameters) | six accepted families | See §5 of the report | Footprint ratio ≥ 0.060; crest ≤ 2.5 cm (current upper reference); no growth from invalid regions | Display never rescues a skull | See report §5 |
| A34 | Pigmentation / pattern / material | (accepted Gate 8) | — | — | Unchanged | Pattern coordinates follow the deformation; no re-design | — |
| A35 | Sex-related anatomy | **OPEN** | — | — | Canon supports **no** dimorphic ranges (§24, §62, §154, §235) | — | Report §7 |

## B — Skeletal Frame (editable starting distributions, not castes)

| Dimension | Narrow | Balanced | Broad | Notes |
|---|---|---|---|---|
| Shoulder breadth | ×0.93 | 1 | ×1.08 | Arms translate with the girdle |
| Thoracic width | ×0.95 | 1 | ×1.05 | — |
| Thoracic depth | ×0.98 | 1 | ×1.02 | Protects d/w: Narrow 0.94, Broad 0.82, both inside 0.80–1.00 |
| Pelvic width | ×0.94 | 1 | ×1.07 | Legs translate |
| Limb girth / joint breadth (radial) | ×0.94 | 1 | ×1.06 | §19: joint dimensions follow the frame |
| Hand / foot breadth | ×0.96 | 1 | ×1.04 | — |
| Tail base breadth (frame component) | ×0.95 | 1 | ×1.06 | Tail support follows the pelvis |
| Long-bone lengths, axial lengths, head, sacral-caudal organization | 1 | 1 | 1 | **Protected** |

- Frame does not touch stature or the skull.
- Frame shifts the tail-length limit: Broad carries 80 % (x27); Narrow ≈ 72 % (x18).

## C — Physical Composition (independent of frame)

| # | Parameter | Class | Range tested | Distribution (regional weights) | Notes |
|---|---|---|---|---|---|
| C1 | Current muscularity | IND | low (−0.45 cm peak) … high (+0.9 cm peak) | Upper arm and forearm, shoulder girdle, epaxial neck and dorsal trunk, thigh, posterior shank, proximal-mid tail. Joints and hands/feet excluded. | No pectoral blocks, no abdominal segmentation, no bodybuilder width (§8) |
| C2 | Body-fat amount | IND | low (−0.35 cm) … high (up to +2.2 cm) | — | +18 L at high, +13 % body volume |
| C3 | Body-fat distribution | IND pattern selector (OPEN tendencies, §23/§153) | — | Default: ventral-abdominal (1.0), flank/hip (0.5–0.6), **graded caudal-proximal over the proximal ~half (0.55)**, minor gular (0.3), general subcutaneous (0.15) | **Rule:** caudal adipose may not concentrate in the caudal base (x25 FAIL: abrupt mass step). No gluteal/buttock mass. |
| C4 | Muscular development capacity | IND (canon §22) | not rendered | — | Gameplay-neutral |

## D — Personal Presentation

Presentation is not inherited biology. It includes: paint/dye, jewelry, keratin caps, wraps, bands, clothing and armor, and polish or decorative treatment of display keratin and claws.

Its only links to biology:
- it **selects presentation of existing biological features** (for example, how a display is decorated);
- tail coverings may lie on the tail but never erase it (§195).

## Tail rule

Notation:
- k = tail-length multiplier on the reference (k = 1 ↔ 64.6 % H).
- b = tail-base multiplier.
- t = mid/distal fullness multiplier.

All measured on the reference body, Balanced frame, reference composition.

**1. Root sufficiency.** RSI = (free-tail volume × centre-of-mass lever) / root area^1.5, normalized to the reference and to stature.
- RSI ≈ k² / b^1.7. Measured: k = 0.851 gives 0.72; k = 1.238 gives 1.53; b = 1.15 gives 0.79.
- Hard: 0.75 ≤ RSI ≤ 1.20. Soft: 0.85–1.10.
- Centre line: **b_c(k) = k^1.18**.

**2. No abrupt loss.** Peak area-loss rate ≤ 1.25 × reference (soft ≤ 1.12). This caps the base at b ≈ 1.24 for t = 1, and lower for t < 1.

**3. No threadlike or cylindrical tail.** Mid-tail area / root ∈ [0.27, 0.48] (soft 0.31–0.44), and area at 25 % from the tip ≥ 0.065 × root.

**4. Counterbalance (relative).** Forward lean needed to stand over the feet ≤ reference + 3.0° (soft + 1.5°). Equivalent to a free-tail volume share ≤ ~19.5 %.

**Resulting valid base band at t = 1:**

| Tail length (% H) | Valid base band | RSI = 1 at |
|---|---|---|
| 55.1 | 0.80–0.98 | b 0.82 |
| 61.4 | 0.84–1.12 | b 0.94 |
| 64.6 | 0.90–1.19 | b 1.00 |
| 71.0 | 1.01–1.27 | b 1.12 |
| 77.4 | 1.12–1.16 | — |
| 79.9 | none on the reference body | — |

**Fullness:**
- t = 0.85 is valid only up to ~71 % and with a reduced base.
- t = 1.15 is valid up to ~71 %.

**Creator behaviour (§159):**
- Tail length drives base and fullness as dependents.
- The base slider moves inside the band.
- The length slider is capped where no valid base exists: ~78 % H on a Balanced/reference body, 80 % on Broad frames or heavier compositions.
- Randomization samples b around b_c(k).

## Head rule

**Rostral index** = rostral projection / head length. Hard range 0.255–0.335 (soft 0.268–0.315). The floor is provisional until the cross-race numeric check against the Marchfolk/Grask/Gorrund projection ranges (§39, §146) is done.

**§40 coupling:** rostrum length > +10 % requires posterior jaw depth ≥ 1.0 and rostral depth ≥ 1.0.

## Display rule (candidate)

- **Footprint ratio** (base radius / structure chord) ≥ 0.060. The accepted swept-back pair is 0.069.
- **Crest height** ≤ 2.5 cm above the roof; the accepted restrained crest (2.43 cm) is the current upper reference.
- **Growth regions:** displays grow only from the §101 attachment regions.
- **Length and moment:** limited by the moment index and by neck clearance (report §5).
- **Asymmetry:** paired asymmetry ≥ 0.70 length ratio counts as natural; below that it reads as injury (an acquired layer).

— Claude
