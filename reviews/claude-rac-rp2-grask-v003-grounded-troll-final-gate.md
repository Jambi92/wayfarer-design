# RAC RP2 — Grask v003 grounded-troll identity correction: final gate

**Date:** 2026-10-23
**Order:** `reviews/chatgpt-rac-rp2-grask-v003-grounded-troll-correction-order.md` (fb85653)
**Bounds:**
- v001 is the too-human lower bound (`81f579f9…9c0a`).
- v002 is the too-alien upper bound, rejected (`9622a062…23ee`).

Both are preserved unchanged on the PC and re-hashed.

**Executor:** Claude, autonomous. Internal candidates v003a–g were gated; failures were rejected internally (§8).

**Status: RP2 GRASK GROUNDED-TROLL IDENTITY BUILD PASS / READY FOR AUTHOR REVIEW**

## 1. Candidate

| Item | Value |
|---|---|
| File | `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Grask/RP2/GR_U_REF_RP2_production_v003.blend` |
| Companion files (same folder) | `…_v003.json` (sidecar), `…_v003_landmarks.json`, `…_v003_edit_masks.npz`, `…_v003_mpfb_mapping.npz` |
| File SHA-256 | `46697d1b140da23e141d4d85e4ba584ab5edb58f2c2ffacc05cb8caf25d55b52` (PC readback match) |
| Geometry hash | `7f154d5941bbedb37d6fbca155142b93a0dbec3a33ceff4f7de9a64d6406bdd2` |
| Object | `GR_U_REF_RP2_production_v003`, the only object. Blender metres; world matrix identity; ground contact at z = 0. |
| Topology | Same vertex and face order as v001 and v002: 214 146 vertices, 214 144 quads. MPFB mapping unchanged. |
| Source | GR5DE3 `d859eb18…d778`, unchanged. |

## 2. Why v001 and v002 failed

**v001 read as too human.**
- Human facial proportions: brow-to-menton 16.3 cm.
- Human ears (6.5 cm).
- A smooth tall-human trunk and joints.
- Slender human hands (29.4 cm) and a scaled human foot (35.7 × 13.9 cm).
- Faceted reference artefacts at the mouth corner and orbits.

**v002 read as too alien.** The elongation cues stacked on top of each other:
- face +31 % (brow-to-menton 21.3 cm, crown-to-menton 32.2 cm), narrowed midface, long nose, forehead set back;
- 8.7 cm ears with a 1.6× upper elongation and extra stand-off;
- trunk narrowed 5.5 % over very long limbs;
- hands 32.5 cm (0.86 of forearm) with +14 % finger thickness and bulbous pads;
- feet 39.2 × 16.6 cm.

Each cue was plausible on its own; together they produced an extraterrestrial mask on a stick body.

## 3. v003: what was kept and what was pulled back

The correction is selective by region, not a global v001/v002 average. The parameters are in `tools/params_v003.json`.

| Region | Kept from v002 | Pulled back or new | Result |
|---|---|---|---|
| **Face / head** | Brow torus (stronger than v001), continuous brow-nose line, vertical zygomatic body, deep ramus and chin | Facial elongation k 0.22 → 0.13 (59 % of the increase); midface narrowing 6 % → 2 %; nose length +0.35 → +0.15; forehead set-back 0.4 → 0.15. **New:** broader lateral cheekbones, broader nasal base and alae, jaw breadth at the angle +12 %, wider mouth, softer submandibular fold. | Brow-to-menton 19.0 cm (v001 16.3, v002 21.3); crown-to-menton 30.0 cm (27.2 / 32.2). Robust, broad structural planes, vertically organized without stretch. |
| **Ears** | Folded auricle, late taper, lobe, robust cartilage | Upper elongation 1.6× → 1.25×; lateral flare 0.15 → 0.05; wing 0.35 → 0.25; taper 0.45 → 0.35. **More** fold relief (0.6 → 0.8) and cartilage depth (0.5 → 0.7), so folds rather than length carry the identity. | Length 7.85 cm (6.5 / 8.7); compact-to-moderate, robust, non-elven. |
| **Neck / girdle** | Thicker integrated neck, clavicle shafts, acromion | Neck profile kept moderate (+8 / +5 %). **New:** upper-trapezius and scapular mass behind the girdle, for grounded upper-body presence with no front widening. | Head carried on a substantial neck–trapezius base; no wrestler neck, no hunch. |
| **Torso** | Sternal keel, reduced pectoral shelf (half strength) | Thoracic breadth restored to −2.5 % (v002 −5.5 %); depth +3.5 % (v002 +5 %). | Narrow-to-moderate deep trunk; it no longer reads as a thin alien trunk, and there is no V-taper or barrel chest. |
| **Joint structure** | Elbow, knee, wrist and ankle structure and bony landmarks | Breadth profiles about 2/3 of v002 (knee +8 %, elbow +9 %, wrist +4–6 %, ankle +5–7 %); bony relief at 70 % amplitude. | Structurally substantial, not swollen. |
| **Hands** | Larger scale, strong metacarpal and knuckle structure, robust digits | Hand scale 1.05 → 1.04; finger elongation 5 % → 0; finger thickness 14 % → 10 %; knuckles 0.13 → 0.09; pads 0.22 → 0.12. | 31.1 cm (0.82 of forearm; v001 0.77, v002 0.86): large troll hands, not alien. |
| **Feet** | Heel, instep and forefoot structure; robust toes | Toe elongation 0.24 → 0.10; forefoot breadth 0.06 → 0.04; heel 2.2 → 1.2 cm; instep 1.0 → 0.7; toe splay 0.22 → 0.16 (keeps toe clearance). | 37.1 × 15.6 cm (v001 35.7 × 13.9, v002 39.2 × 16.6); grounded plantigrade. |
| **Limbs** | Long arms, forearm and shank emphasis, femur, reach | No limb shortening | Canonical long-limb architecture kept. |

## 4. Delta accounting

Masks: `GR_U_REF_RP2_production_v003_edit_masks.npz`. Full numbers: `gates/deltas_vs_v001_v002.json`.

| Mask | vs v001 (mean / max mm) | vs v002 (mean / max mm) | Share of the v001 → v002 change retained | Nearer to |
|---|---|---|---|---|
| Head / face | 8.2 / 33.0 | 5.9 / 22.6 | 0.58 | v002, partly new |
| Ears | 4.7 / 14.0 | 2.1 / 11.1 | 0.69 | v002, folds stronger and length shorter |
| Neck / girdle | 8.7 / 31.7 | 5.8 / 22.2 | 0.60 | v002, plus new trapezius and scapular mass |
| Torso | 2.2 / 8.9 | 1.8 / 5.8 | 0.55 | between; breadth closer to v001 |
| Hands | 8.8 / 17.4 | 5.8 / 14.5 | 0.58 | between |
| Feet | 8.4 / 23.1 | 8.7 / 18.3 | 0.49 | v001 |
| Joint structure / limbs | 1.5 / 10.0 | 0.7 / 5.1 | 0.70 | v002 (kept as directed) |

Stature, bounding box and silhouette:
- **Stature:** 217.949 cm. That is −0.40 mm against E3, +0.03 mm against v001 and +0.32 mm against v002.
- **Bounding box against v001:**
  - x ±2.8 mm (ears, hands);
  - forward +12.8 mm (toes), back −2.2 mm (heel); against v002, forward −18.1 mm;
  - ground at z = 0 (v001 sat 0.35 mm above it).
- **Silhouette IoU:** against v001 0.970 / 0.966 / 0.970 (front / profile / rear); against v002 0.983 / 0.981 / 0.983. Area is +2.0 % against v001 and −0.6 % against v002 (front).

## 5. Technical result

| Gate | Result |
|---|---|
| Components / boundary / non-manifold edges and vertices / genus | 1 / 0 / 0 / 0 / 0 |
| Degenerate faces / coincident vertices / unused vertices / directed-edge duplicates / hidden shells | 0 / 0 / 0 / 0 / 0 |
| **Self-intersections** | **0**: float64 design data and the float32 stored file, both quad diagonals |
| Normals | Outward; +111.30 L in the Blender frame |
| Quads overall / in deformation zones | 100 % / 100 % |
| T-4 (quality target) | Angles 45–135°: 98.23 % (v001 98.05, v002 97.88). Aspect ≤ 4: 95.60 %. |
| Zone audit with the v003 joints | Loops and creator density pass |
| T-1, unchanged region vs H | prod → ref 0.21 / 0.79 / 1.86 mm; ref → prod 0.32 / 1.14 / 2.03 mm — **PASS** |
| T-3 | Stature −0.40 mm — **PASS**; ground contact z = 0 |
| T-6 | 42 of 106 heads and tails unchanged. 64 finger and toe-tip joints re-swept by the intentional extremity correction, maximum 10.5 mm (v002: 23.5 mm). |
| T-7 | Unchanged-region IoU vs v001 0.9998 / 1.000 / 0.9998; vs E3 0.998. The change in the full silhouette is confined to the edited regions. |
| **Deformation (48 poses, v003 joints)** | 32 clean, 16 local flexion-crease contact, **0 non-local**, return to rest 0.000 mm. Same classes as v002, and the half finger curl is cleaner than in v001. Deepest contact: knee flexion 120° at 4.5 mm. No collapse. |

## 6. Self-review (order §15)

| # | Question | Answer |
|---|---|---|
| 1 | Grask with all surface cues removed? | **Yes.** Neutral gray, bald, no texture. |
| 2 | Troll-like, not alien? | **Yes.** Broad robust head on a neck–trapezius base, compact folded ears, large knobby hands and grounded feet. The stretched mask is gone. |
| 3 | Torso grounded enough for the long limbs? | **Yes.** Thoracic breadth near v001, keel and back mass kept. |
| 4 | Non-human head without alien elongation? | **Yes.** Brow torus, brow-nose line, broad zygoma and nasal base, deep broad jaw; +17 % facial height, not +31 %. |
| 5 | Robust, folded ears, not elven or alien? | **Yes.** |
| 6 | Hands large and troll-like? | **Yes** (0.82 of forearm, knuckled, no claws). |
| 7 | Feet grounded and large? | **Yes** (37 × 15.6 cm, plantigrade, five toes). |
| 8 | Still rangy? | **Yes.** No added bulk; long-limb architecture unchanged. |
| 9 | Distinct from Skarn? | **Yes.** No power-torso widening. |
| 10 | Distinct from Aelari? | **Yes.** Heavy broad face, folded ears, knobby joints. |
| 11 | Distinct from Gorrund? | **Yes.** No claws, muzzle or compact mass. |
| 12 | No generic-orc clichés? | **Yes.** No tusks, underbite, giant brow, giant nose or brute torso. |
| 13 | Coherent at about 218 cm? | **Yes.** All relationships sit between v001 and v002. |
| 14 | Production-ready? | **Yes** (§5). |

## 7. Comparison sheets

All sheets are in `reviews/rac-rp2-evidence/grask_v003_grounded_troll/sheets/`, with rows v001 / v002 / v003 on identical cameras and neutral material:

| Sheet | Views |
|---|---|
| `sheet_1_body.jpg` | Front, profile, back, 3/4 |
| `sheet_2_head.jpg` | Head front, profile and 3/4; orbit / midface / jaw front; jaw profile and 3/4 |
| `sheet_3_ears.jpg` | Ear profile, 3/4, from behind |
| `sheet_4_hands_feet.jpg` | Palm, back and side of the hand; top, side and 3/4 of the foot |
| `sheet_5_carriers.jpg` | Girdle front and back, chest / abdomen, pelvis, lower-leg profile |

## 8. Internal candidates rejected

| Candidate | Problem | Fix |
|---|---|---|
| v003a | Face narrowed back toward human; weak front read | Broader cheekbones, nasal base and jaw |
| v003b | Round submandibular fold | Jaw body relief reduced |
| v003c | Trunk fully reverted to v001 | Partial breadth (−2.5 %) plus back and trapezius mass |
| v003d / e | Stature −1.03 mm (ground offset 0.64 mm plus crown), failing T-3 | Sole ground restore, giving stature −0.40 mm and ground at 0 |
| v003f | Toe extension 30° produced 2 small toe-toe contacts (regression) | Toe splay 0.16, toe thickening 0.05 |

v003g is the final candidate and ships as v003.

The optional canine diagnostic stays deferred. The base passes without it.

## 9. Scope

STOP. No next race, canon freeze, rig promotion, creator or UE5 work.
