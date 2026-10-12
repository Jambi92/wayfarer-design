# RAC RM-OT-05K: Gorrund envelope revision, then reference-first fallback (gate)

**Order:** `reviews/chatgpt-rac-rm-ot-05k-gorrund-envelope-reference-first-order.md` (9c650b7)
**Author of this report:** Claude
**Date:** 2026-10-12
**Evidence:** `reviews/rac-rmot05k-evidence/` (hashes in `SHA256SUMS.txt`)
**Tools:** `tools/rac/w1/rmot05k_drivers/`

## Gate lines

| Line | Status |
|---|---|
| Branch A bounded envelope | **FAIL** |
| Branch A selected candidate | **NONE** (EA1 and EA2 tested; EA3 not justified, §7) |
| Branch A skin-level validation | **PASS** for every binding guard. Diagnostic skin depth rows **FAIL**, inherited from S2 (§2.3) |
| Branch A low-composition read | **FAIL**. Low composition re-fills the waist and keeps the belly / chest read |
| Branch A blind gate | **NOT RUN** (§11 visual gates not met) |
| Branch A Stage C | **NOT RUN** |
| Branch B triggered | **YES** (automatic, §11 / §12) |
| Branch B starting skeleton used | **NO** |
| Branch B final reference revision | **RF2** (RF1, then the single authorized RF2) |
| Branch B reference body read | **FAIL** |
| Branch B low companion read | **FAIL** |
| Branch B concept blind gate | **FAIL**, both RF1 and RF2 |
| Branch B measurement scaffold | **NOT DERIVED** (§21 requires a concept pass first) |
| Gorrund structural readability | **REJECT** |
| RM-OT-05 | **OPEN** |
| Canon promotion | **NOT PERFORMED** |
| D4 | **NOT STARTED** |
| UE5 | **NOT STARTED** |

Grask E3 is still frozen and untouched. I stopped after RF2 failed, as §20 / §28 require. No RF3 was made.

## 1. Branch A: bounded envelope revision

### 1.1 Method

`k_envelope.py` applies a single smooth skin-level field to S4. S4 was used because it carries the S4 structural-cue work (§8).

- **What moves:** the trunk flanks move inward. The move peaks at the lower axial trunk (z 139–144 cm, the ALPC S4 level). It falls to zero at z 128 above the hip joints and at z 163 in the upper rib cage.
- **What stays untouched:**
  - the anterior / posterior midline (no depth added, so no belly and no barrel);
  - arms, legs, hands, head;
  - the skeleton.
- **Floor clamp:** a true-floor clamp keeps the ASIS subcutaneous. Without it, the first build failed 05F I5 at the ASIS (x ±20.7, z 131).
- **The only parameter varied:** strength A, the flank displacement at the peak.

| | A (cm) | Vertices moved | Waist breadth z 136–145 (cm) | Upper rib cage z 163 | Hips z 121 |
|---|---|---|---|---|---|
| S4 | 0 | – | 45.8–47.0 | 45.8 | 47.2 |
| EA1 | 1.25 | 557 | 44.1–44.6 | 45.7 | 47.2 |
| EA2 | 2.5 | 621 | 41.9–42.4 | 45.6 | 47.2 |

S4 itself shows where the box comes from. In the old route reference the waist was narrower (42 cm) than the chest (44 cm) and the hips (49–51 cm). The S2–S4 sculpts widened the z 139–154 band to 46–47 cm and narrowed the hips. That is what produced the near-parallel column.

### 1.2 Validation

Both candidates pass the exporter preflight against the 05I overlay package. Both pass the full 05F re-entry (I1–I6 and every guard in all four states):
- true floor;
- self-intersection;
- arm–trunk clearance;
- composition ordering;
- frame ordering;
- plantigrade;
- hand / foot topology.

Volume ratio is ≈ 0.9999998.

| State (EA2) | Pierce edges (route) | Arm gap (cm) | Skin S2 breadth | Skin S4 breadth | S4 / S2 |
|---|---|---|---|---|---|
| Reference | 76 (67) | 0.69 | 46.6 | 42.7 | 0.916 |
| **Low** | 81 (78) | 0.84 | 47.7 | **45.7** | **0.958** |
| Narrow | 63 (57) | 0.93 | 43.6 | 40.6 | 0.931 |
| Broad | 60 (53) | 0.96 | 46.7 | 43.9 | 0.940 |

The S2 and S4 columns are the guard's own station readings.

### 1.3 Skin-layer rows (§10)

Skin readings come from `k_envelope.py` on the delivered surface, at the skeleton-anchored station levels.

**Breadth rows** (ALPC-1 / -2a / -2b / -7 against Marchfolk and Skarn) all pass. S4/S2 breadth is 1.035 for EA1 and 0.98 for EA2, against the Marchfolk value of 0.79. Canon wants Gorrund to taper less than Marchfolk, so this direction is correct.

**Depth rows FAIL.** These are pelvic AP / thoracic depth and lumbar depth / thoracic depth. The failure was not created by the envelope; its depth is unchanged from S4.

| Body | Pelvic AP / thoracic depth (Marchfolk ≥ 0.971) |
|---|---|
| Route template | 0.973 |
| S2 | 0.779 |
| S3 | 0.753 |
| S4 / EA | 0.721 |

The 05H–05J posterior and abdominal flattening caused this. The 05E ruling makes these readings diagnostic only: the protected relations are held on the skeleton, and those are unchanged. The 05H–05J gates did not report this regression, so I am disclosing it here.

The ALPC-0 shape screen at fixed levels fails on every body, including the route template. It is a reading artifact of the level grid.

### 1.4 Visual gates (§11)

Sheets: `branchA/EA_S4_full_comparison.jpg`, `EA2_vs_S4_trunk.jpg`, `EA_states_low_narrow_broad.jpg`.

- **Reference (EA2):** a modest lower-axial minimum is now visible from front and rear, and the trunk is no longer a parallel column. It still reads as an ordinary human male.
- **Low:** the composition re-fills the waist (S4/S2 goes from 0.916 to 0.958). The read is again navel, soft lower belly and deep chest, so "belly / chest fat" is not removed.
- **Broad:** still close to rectangular.
- **Cue families in low:** unchanged from the 05J audit. Only B (posterior load path) is CLEAR. A, C, D, E and F are MARGINAL. That is below the four-family bar.

**Branch A FAILS at §11.**
- **EA3:** EA1 and EA2 do not bracket a promising region, so EA3 was not run.
- **Blind gate and Stage C:** not run.
- **Specific report required by §9:** the envelope partly fixes the reference outline, but the low composition removes most of the change.

## 2. Branch B: reference-first sculpt, skeleton later

### 2.1 What was and was not used

**Not used:**
- the Gorrund rig, the GO5 route skeleton or its joint centres;
- the S1–S4 meshes;
- any Gorrund generator.

**Substrate (§14, "neutral humanoid topology / sculpting medium"):**
- RF-REF is built on the ordinary-human Marchfolk male reference MF-M-R (`reviews/reference-assets/r6`).
- RF-LOW is built on MFM-RFLOW, a new low-muscle, low-fat build of that same substrate (muscle 0.1, weight 0.25; `branchB/substrate/`). It reduces both muscle and adipose tissue, as §17 asks.

The substrate's segment weights were used only as soft sculpt masks. Its joint points were used only as working axes for the sculpt. Neither is kept as a skeleton.

### 2.2 Sculpt operations

`k_rf.py` writes the body form as explicit, documented fields. The same anatomy is applied to both substrates, so LOW is a leaner build, not a shrunken copy.

1. **Segment relation:** legs × 0.93, trunk lengthened to compensate, arms × 0.95. Axial share goes up and reach is not dominant.
2. **Stance:** hip joints carried 1.8–3 cm wider.
3. **Trunk sections:** a deep, three-dimensional thorax (anterior × 1.30, breadth × 1.17–1.22). The lower anterior wall is recessed. The sacral platform is deep.
4. **Gluteal mass reduced:** posterior × 0.78–0.82, giving sacrum-to-hamstring continuity.
5. **Shoulder girdle:** arms carried outward with the girdle.
6. **Limb bone scale:** radial scale is larger at the joints than along the shafts (knee 1.30, ankle 1.42, elbow 1.28–1.32, wrist 1.40).
7. **Hands and feet:** hands × 1.18, feet × 1.25 / 1.18 / 1.12. Five digits, plantigrade.
8. **Neck root and finish:** neck root × 1.35, Taubin fairing, stature 229 cm.

Both builds reproduce bit-for-bit from the saved parameters. Self-intersection is 4 piercing edges, against 48 on the substrate itself.

### 2.3 RF1

**Internal review (§18, `RF1_neutralized_review.jpg`):**
- not obese, not slab-sided, not a Grask read;
- REF and LOW read as the same body.

I judged its non-human read uncertain and ran the concept blind gate to settle it.

**Blind setup:** the unchanged 05F protocol, run through `k_blind.py` (a protocol copy):
- same 8 human-family controls plus the frozen Grask E3;
- new seeds, neutral filenames;
- 6 fresh scorers given the verbatim prompt;
- tallied with the unchanged `f_tally.py`.

| Line | Run 1 (K) | Run 2 (L) |
|---|---|---|
| G1 reference C | **2 / 3 PASS** | 0 / 3 FAIL |
| G2 low C | **2 / 3 PASS** | 2 / 3 PASS |
| G3 stable group | 0 FAIL | 0 FAIL |
| G4 distinct from Grask | 3 PASS | 3 PASS |
| G5 organization basis | **2 PASS** | 0 FAIL |
| G6 axial + limb cues | 3 PASS | 3 PASS |
| G7 no control collapse | PASS | PASS |

RF1 is the closest Gorrund result in the 05-series: for the first time, two of three scorers called both states C on an "organization" basis in one run. It still fails.

**Scorer reasons:**
- Run 1 C calls cite a "columnar / rectangular trunk without waist", "thick untapered limbs" and "heavy forearms". One scorer called the reference B for muscularity.
- In run 2 the reference reads as a "broad / athletic human" (bulk), and the low reads as "extreme V-taper" (B) or "a barrel trunk tapering to a narrow pelvis" (C).
- Every scorer marked the grouping unstable.

**Blind-reason audit: FAIL.** The forbidden reasons boxy, rectangular, bulky and muscular carry the read.

### 2.4 RF2: the one revision allowed by §20

The one coherent RF1 issue was the trunk silhouette: columnar in the reference, V-taper in the low.

RF2 was the single bounded fix:
- a lower-axial minimum (waist breadth × 1.06 against thorax × 1.16–1.17);
- a less dorsal hump (posterior × 1.10);
- a narrower stance shift.

Internal review: the first try at a waist factor of 1.02 gave a pinched hourglass in LOW. I discarded it before testing and used 1.06.

| Line | Run 1 | Run 2 |
|---|---|---|
| G1 / G2 | 0 / 0 FAIL | 0 / 0 FAIL |
| G3 / G5 | FAIL | FAIL |
| G7 | **FAIL** | PASS |

Run 1's G7 failed because the reference sat in the ordinary-human group with six controls.

Scorers now read the reference as an ordinary human, and in several cases a "female-type torso with bust". They read the low as an "hourglass / pear-shaped" human (B: fatness or single feature). The deep anterior thorax reads as breasts once the waist is defined.

**RF2 fails. I stopped under §20.**

### 2.5 Measurement scaffold

**NOT DERIVED.** Under §21, a scaffold is derived only after a concept pass.

## 3. Decision record (§26)

**Why Branch A was exhausted:**
- The envelope cannot add structural identity.
- Low composition re-fills the waist, and the belly / chest read comes back.
- Only one cue family is CLEAR in low.
- This is the same global box-vs-fat failure as before.

**Branch B:**
- No starting Gorrund skeleton was used.
- Two free-sculpt revisions (RF1, RF2) failed the concept blind gate.

**What the RF1 → RF2 pair shows.** Under a height-normalized, head-free blind read, Gorrund's canonical identity lands on one of three human reads:
- "broad / muscular / boxy human" when the trunk has no waist;
- "obese human" when depth is pushed (S3, 05I);
- "hourglass / female human" when a waist is cut under a deep thorax (RF2).

The only setup that earned organization-based C calls was RF1, in run 1. It had a waistless trunk, thick joint-dominant limbs and big hands and feet. That trunk is the "rectangular" read §11 forbids.

## 4. Unresolved canon conflict (returned to the author)

These are not silent changes. They are for the author to decide.

1. **Possible conflict in the readability bar itself.** At matched height, without a head, canon Gorrund identity is broad / deep skeletal mass plus substantial joints, with no hunch, no ogre and no armor. Two independent construction orders (skeleton-first S1–S4 / EA, and reference-first RF1 / RF2) did not make that read as non-human through structure alone. A decision is needed on one of these:
   - (a) accept a constrained identity, where body-only Gorrund reads as "unusual human-family" and identity comes from the head / face, scale and other channels;
   - (b) allow a canon-legal but more distinctive structural signature. RF1's columnar trunk with joint-dominant limbs was the only arrangement that drew organization-based C calls;
   - (c) commission an artist / Rodin-style source body, as Saurin had. Saurin's reference-first success started from an external sculpt source, not a parametric field on a human substrate.
2. **Skin pelvic-depth rows.** These have failed as diagnostics since S2 (§1.3). They need a ruling if the skin layer is ever made binding.

## 5. Principal hashes (SHA-256)

| Artifact | Hash |
|---|---|
| `branchA/GO_sculpt_EA1_r6.obj` | `6078e618eddea9990e4ce132ad52863e220a9ef232ebd0547358ed5360e13799` |
| `branchA/GO_sculpt_EA2_r6.obj` | `48516259aafbb854919cf1b7f480fd14142996b990180df4ba5d7555bd90f6e3` |
| `branchB/GO-RF1-REF.obj` | `76350bfe720ab60fcce9ec74ddd2807441082dbb8dd6e2725e7eb4cfbd50e80f` |
| `branchB/GO-RF1-LOW.obj` | `fd0bcf9b505891be43da52b49a4bd86626337e1f5d8c3814cb0b9279b2c6bbc7` |
| `branchB/GO-RF2-REF.obj` | `cae0d149d4edc93508a03ec0c2bceb59f46c777a2e4f3017c660273c082ce256` |
| `branchB/GO-RF2-LOW.obj` | `fda62b16684588f1d9ff1f47f313d157d22b6a4b6c82797bbd5504edccaf0605` |

Full hashes are in `SHA256SUMS.txt`.

## 6. Confirmation

The following did **not** change:
- the Gorrund skeleton, proportions, rig or route;
- the 05F re-entry validator, guards and thresholds;
- the 05I overlay;
- the scorer prompt (used verbatim) and `f_tally.py`;
- canon rules;
- Grask E3.

The blind protocol was not altered. `k_blind.py` changes only the body paths, seeds and output folder.

I stopped at the RM-OT-05K author gate.
