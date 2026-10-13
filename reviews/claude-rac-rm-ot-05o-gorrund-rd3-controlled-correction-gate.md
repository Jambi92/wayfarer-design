# RAC RM-OT-05O: Gorrund RD3 controlled correction and evidence audit (gate)

**Order:** `reviews/chatgpt-rac-rm-ot-05o-gorrund-rd3-controlled-correction-order.md` (77f3f10)
**Author:** Claude
**Date:** 2026-10-12
**Evidence:** `reviews/rac-rmot05o-evidence/` (`SHA256SUMS.txt`; replay commands in `REPLAY.md`)
**Tools:** `tools/rac/w1/rmot05o_drivers/`
**Pre-registration commit (before any scoring):** 2c14a86

## Gate lines

| Line | Status |
|---|---|
| Corrected measurement audit | **DONE** (§1). The 05N trunk-breadth rows are void (mask artifact). |
| Source vs edit attribution | **PARTIAL**. Stance and leg proportion were isolated and corrected; the contribution of the 05N trunk / pelvis edits is unmeasured (§2). |
| RD3a stance-only comparison | **DONE** (§3) |
| RD3b surface transitions | **DONE** (§4) |
| RD3c proportion comparison | **DONE**: proposal first, one execution (§5) |
| Selected final RD3 candidate | **GO-RD3-REF = RD3c** |
| LOW companion | **CREATED** (`GO-RD3-LOW`) |
| REF / LOW preservation audit | **PASS with one design flaw** carried from 05N (iliac / sacral regions not fully protected; §6) |
| Revised neutralized structural gate | **FAIL**: C1–C4 PASS 3/3 in both runs; **C5 FAIL 0/3 in both runs** (§7) |
| Old 05F criteria G1–G7 (provenance only) | Pass 2/2 runs (does not override C5) |
| Full-organism confirmation | **NOT RUN** (§6 of the order: only after the structural pass) |
| Measurement scaffold / canon reconciliation | **NOT RUN** (failed candidate) |
| Gorrund | **UNACCEPTED**, pending author review |
| Grask E3 | **FROZEN** |
| RM-OT-05 | **OPEN** |
| Stage C | **BLOCKED** |
| D4 / UE5 / production rigging / creator implementation | **NOT STARTED** |
| Canon promotion | **NOT PERFORMED**. No canon line changed in this block. |
| Source master | Untouched; `base.glb` hash `78ecfa87d169380ecb46ece3f0c0df3491d10e4547038a3c35c06df933f38a7b` |

**Bottom line**

The stance and leg-proportion corrections worked as measured:
- the hip–ankle line is now vertical (it was 26.8 cm off);
- crotch / stature rose from 0.430 to 0.452, the floor of the accepted W2D series;
- "ogre / troll" group labels fell from 6/6 (05N) to 2/6.

The body still fails C5. All 6 scorers named `segment_relations` as the primary driver, which is a structural reason. But all 6 also rated **muscularity "major"**, 5/6 rated **boxiness "major"** and 4/6 rated **posture "major"**. The scorers still describe bowed, bent legs even though the sagittal knee chain is straight; §7.3 gives the measured coronal (bow-leg) cause. Every driver text names oversized hands and feet and lumpy joint masses.

I stopped here: no RD4.

## 1. Corrected measurement findings (§2 of the order; `audit/AUDIT_FINDINGS.md`)

1. **05N trunk breadths were a mask artifact.** The 05N `audit.py` clipped every trunk slice to |X| < 29 cm. "REF 57.5 cm at four stations" is the mask edge, and "waist 57.5 → 48.5" is an artifact. The corrected tool (`o_sections.py`) measures on the delivered meshes. It separates hanging arms by component, or by a marker watershed where they touch, reports the method per station, and adds an arm-independent midline AP depth. Overlays: `audit/RD2_REF_LOW_section_overlays.png`.
2. **Corrected RD2 REF → LOW trunk values**

   | Station | Result |
   |---|---|
   | lower trunk, 146 cm (arms free) | 44.0 → 44.0 cm; area 0 % |
   | waist, 138 cm | 54.2 → 48.0 cm (−6.2 cm, −7.5 % area). REF elbow contact plus the designed flank reduction. |
   | pelvis, 115 cm | 58.5 → 58.5 cm (−0.3 % area) |
   | 155–170 cm | Upper arm against the chest, so trunk breadth is not uniquely defined. Watershed breadths differ by segmentation, e.g. a spurious +8.5 cm at 155. Midline AP depth: 0.0 / 0.0 / −1.6 cm. |

3. **Preservation, measured separately from design** (signed distance LOW → REF surface):

   | Region | Measured | Design reach |
   |---|---|---|
   | Knee, ankle, wrist, acromion | ≤ 0.05 cm max (preserved) | — |
   | Elbow | p95 0.12 cm | 0.34 cm |
   | Sacral platform | p95 0.25 cm | 0.76 cm |
   | **Iliac crest / ASIS** | **p95 0.67 cm** | **1.07 cm** |

   The 05N LOW recipe's flank and gluteal ellipsoids reach these "protected" regions. That is a design flaw, now reported.
4. **Stance.** The 05N "20° knee zig-zag" was wrong. The knee was nearly straight (2.4° sagittal). The **whole leg sloped back 16–17° from the hip**: ankle 26.8 cm behind the hip, foot held flat by about 16° of dorsiflexion, trunk vertical (`stance/RD2_leg_axes.png`).
5. **Blind sheets (05N K / L).** Keys correct, stature matched (each body normalized at its neck root), orientation consistent (every profile faces left), no clipping. Old scores are untouched. The 05N reason audit already kept driver keywords (monster words REF 0 / LOW 1) separate from group labels (6/6).

## 2. Source vs edit attribution and uncertainty

| Possible contributor | Source of it | Tested here | Result |
|---|---|---|---|
| Backward leg inclination (hip extension, ankle dorsiflexion) | Inherited F1 pose | Yes, RD3a | Corrected. Posture still read (§7.3). |
| Short leg-to-trunk relation (crotch / stature 0.430) | Inherited proportions (the RD3a hip rotation also lowers the perineum about 3 cm) | Yes, RD3c | Corrected to 0.452. "Short legs" is still named 6/6. |
| Bowed legs in front view (knee 3.2 cm lateral of the hip–ankle line on RD2; 4.5 cm on RD3c) | Inherited F1 pose | **No**. Coronal alignment was outside the order's stance-only operation. | Unresolved, probable posture driver |
| Oversized hands and feet, large forearms, knee / ankle masses | Inherited F1 anatomy (feet shortened to 0.18 H in 05N) | No (hand / foot redesign excluded) | Named 6/6 |
| Lower-trunk thickening (+4 cm lateral), convex reconstructed pelvis, arm–trunk windows | **My 05N edits** | No (outside RD3 scope) | Plausible "blocky / waistless" contributor; **unmeasured** |
| Residual muscularity (quadriceps, deltoid, pectoral relief) | Source; reduced in 05N | No | Muscularity "major" 6/6 |

Attribution is therefore **not** "source only". Stance and leg length were tested by controlled comparison and corrected; the scorer reads changed (fewer monster labels) but did not clear C5. The remaining drivers mix inherited anatomy with my 05N trunk / pelvis reconstruction, and this block did not separate them.

## 3. RD3a: stance-only comparison (`stance/`)

- **Operation** (`o_stance.py`): a rigid rotation of both legs about the common hip axis (X-parallel through y 12.21, z 106) by **15.77°**, chosen so the hip–ankle line is vertical. The foot is counter-rotated about the ankle axis (y −14.62, z 11) so the sole stays flat.
- **Weights:** linear-blend skin weights ramp from the pelvis (z 116) to the legs (z 94); the foot band is 4 cm. Forearms and hands are excluded as separate components; they moved only by the grounding.
- **Unchanged:** knee angle (rigid), segment lengths (thigh 52.005 → 52.005, shank 47.568 → 47.568 cm), trunk, arms, head.
- **Grounding:** +3.55 cm. No limb or global scaling.

| Measure | RD2 | RD3a |
|---|---|---|
| Hip–ankle sagittal offset | 26.83 cm | 0.00 cm |
| Max z (ears / mane) | 236.93 cm | 240.49 cm |
| Crown | 229.0 cm | 232.55 cm |
| Volume | 301.7 L | 307.8 L (+2 %, linear-blend gain in the hip blend zone) |

Mesh: watertight; no visible hip creasing (`RD2_vs_RD3a_turn.jpg`). This was a comparison, not an accepted asset.

## 4. RD3b: surface transitions (`surface/`)

**Operation** (`o_brush.py` with the 05L brush engine): 9 named strokes, mirrored, points snapped to the surface, leg points carried by the stance transform.

| Stroke | Purpose |
|---|---|
| Lower abdominal fold (smooth) | Remove the belly-roll shading line |
| Flank-to-iliac transition (smooth) | Soften the lateral hip shelf |
| Lateral hip plane (flatten) | Natural radius, no shelf |
| Inguinal / crotch notch (smooth) | |
| Gluteal crease scratches (smooth) | Remesh artifacts |
| Popliteal pit (smooth) | |
| Ankle-front strap ridge (smooth) | |
| Heel ledge (smooth) | |
| Anterior tibial plane (flatten) | |

1,859 vertices moved, max 1.61 cm. No bulk was added. Before / after close views: `surface/RD3a_vs_RD3b_close.jpg`.

**Unresolved after RD3b**
- the popliteal pit is still deep;
- the toes still read partly paw-like (not canonized);
- small arm–trunk contact windows remain (source arm pose);
- the hands and their capability read are unchanged.

## 5. RD3c: proportion comparison (`proportion/`)

**Justification** (`PROPOSAL_RD3c.md`, written before execution):
- The 05N scorers named short legs.
- RD3b crotch / stature is 0.430, below the accepted W2D series (GO208 to GO251: 0.452–0.475) and the Grask E3 ceiling (0.489).
- Canon says "never meaning short-legged".

**Smallest adjustment:** reach the series floor, 0.4515. Shafts only:

| Segment | Change | Length |
|---|---|---|
| Femur | +4.8 cm | 52.0 → 56.74 cm |
| Shank | +4.4 cm | 47.56 → 51.96 cm |

The thigh band is z 67.3–92.0; the shank band is z 19.8–49.3. Joints, pelvis, thorax, arms and head are unchanged in shape and move up by the full 9.2 cm. Measured crotch / stature: **0.4516**. No visible distortion (`RD2_RD3a_RD3b_RD3c_turn.jpg`).

**Consequence for stature.** RD3c's crown is **241.75 cm** (max z with ears / mane 249.69 cm). The 05N canon bookkeeping has 229 cm as the nominal design stature. Returning to 229 would need a global ×0.947 scale. §3 of the order forbids hidden compensation, so I did not do it. **Author ruling needed** (D-05O-2).

## 6. Selected candidate, LOW and preservation audit (`final/`)

**Selected:** GO-RD3-REF = RD3c (stance + surface + proportion). It is the only variant that addresses both measured inherited causes, and it stays inside the accepted W2D leg relation and below Grask.

**GO-RD3-LOW** is the 05N GO-RD2-LOW (the bounded local soft-tissue reduction) carried through the identical RD3 chain: same stance transform, same strokes, same shaft bands. The REF / LOW pairing is therefore exact. There is no uniform shrink and no Marchfolk deformation.

**Audit in the RD3 frame.** RD2 stations are carried by `station_z_RD3.json`.

| Measure | Result |
|---|---|
| Trunk stations | Identical to the RD2 audit (trunk untouched by RD3) |
| Knee / ankle / wrist sections | Δ area 0.0 to −0.1 % |
| Pelvis | −0.3 % |
| Thigh / calf | −20.4 % / −6.2 % (soft tissue) |
| Landmarks: crotch, fingertip, acromion proxy, stature | REF = LOW within 0.01 cm |
| Volume | 310.8 → 299.1 L (−3.8 %) |
| Protected-region measurements | Same as §1.3, including the iliac / ASIS design flaw |

**Independent leg axes on GO-RD3-REF** (`RD3_leg_axes.json`):
- thigh −1.4°, shank +5.2° from vertical;
- knee 3.1 cm posterior of the hip–ankle line (6.6° fitted back-knee);
- coronal: knee 4.5 cm lateral of the hip–ankle line.

The knee angle is unchanged by construction (rigid). The fitted value moved from 2.4° to 6.6° because the fit bands moved with the stretched shafts; the fitting sensitivity is about ±4°. It is flagged as a **possible mild hyperextension read**, not claimed as corrected.

## 7. Revised neutralized structural gate (§6 of the order)

### 7.1 Protocol

| Item | Detail |
|---|---|
| Renderer / controls | Unchanged `k_blind.py` set: 8 frozen MF / SK controls, Grask E3 ref + low, GO-RD3 REF + LOW |
| Display | Body only, neck cut z 203.75; matched display stature; front + profile; grey + silhouette |
| Runs | Two runs with new seeds (SID GO-RD3, sets K and L), 3 fresh scorers each, keys retained |
| Prompt | Revised and pre-registered: `o_scorer_prompt_05O.md`. It keeps every 05F field and adds `structure`, `non_structural_factors` and `primary_driver`; it states that deciding species is not required. |
| Decision rules | Pre-registered and committed before scoring (2c14a86). Not tuned afterwards; no output replaced. |
| Operational note | Each scorer was asked to also write its JSON to a file; that sentence sits outside the study text. |

### 7.2 Results (`blind/gate_eval_revised.json`, `tally_old_criteria.json`)

| Condition | Run K | Run L |
|---|---|---|
| C1 REF and LOW one stable type (no control or Grask in the group) | 3/3 PASS | 3/3 PASS |
| C2 no Marchfolk collapse (not grouped with MF, not class A) | 3/3 PASS | 3/3 PASS |
| C3 no Skarn Broad collapse | 3/3 PASS | 3/3 PASS |
| C4 distinct from Grask | 3/3 PASS | 3/3 PASS |
| **C5 structural reasons (REF / LOW)** | **0/3 / 0/3 FAIL** | **0/3 / 0/3 FAIL** |
| C6 beastfolk compatibility | not assessed (gated) | |
| Old G1–G7 (provenance) | pass | pass |
| posture_read REF / LOW (author attention) | 2 / 2 | 3 / 3 |

**Revised gate: FAIL.**

### 7.3 Reasons, read from the explanations (`blind/reason_audit.json`)

| Factor | Finding |
|---|---|
| Primary driver | `segment_relations` 6/6 (a structural category). C5 fails on the non-structural ratings, not on the primary driver. |
| Current pose / posture | Rated "major" 4/6, "minor" 2/6; `posture_read` true 5/6. Drivers say "short bowed legs", "bent knee", "forward-pitched trunk". Measured: sagittal hip–knee–ankle vertical (back-knee 3 cm), trunk vertical. The read most plausibly comes from the **coronal bow** (knee 4.5 cm lateral) and the large knee / calf masses breaking the leg contour. Inherited, not corrected here. |
| Limb bulk | "major" 6/6: huge forearms and fists; massive thighs (reported separately, not part of C5) |
| Muscularity | "major" 6/6 |
| Fat | "none" or "minor" 6/6 |
| Axial section shape | "block / barrel trunk, chest and pelvis nearly the same width, no waist" 5–6/6. Boxiness "major" 5/6 (REF). |
| Joint integration | "lumpy, knobby, bulbous knees and ankles; shoulders sunk into the trunk" 6/6 |
| Segment relations | "short legs, oversized hands and feet, long heavy trunk" 6/6. This persists at crotch / stature 0.452; in the height-normalized display the legs still read short against the deep trunk. |
| Monster words | Group labels 2/6 (05N: 6/6). Driver / cue texts 0/6. |

## 8. Unresolved issues returned to the author

1. **D-05O-1, structural read.** The body still reads as massive, block-trunked, muscular and short- / bow-legged. The next candidate levers are coronal leg alignment (the inherited bow) and reversing or reshaping my 05N lower-trunk thickening and convex pelvis (to restore an anatomical waist minimum). Both are outside this block. Reducing hand / foot / forearm scale is a separate canon question ("large capable hands", "large plantigrade feet"). No RD4 was run.
2. **D-05O-2, stature.** RD3c's crown is 241.75 cm, not the 229 cm nominal. A global rescale would restore 229 but was forbidden here.
3. **LOW recipe.** The iliac crest / ASIS and sacral platform are not fully protected (design reach 1.07 / 0.76 cm). A future LOW should tighten the flank and gluteal ellipsoids.
4. **Residuals.** Paw-like toes, a deep popliteal pit, arm–trunk contact windows, possible mild back-knee (fitted 6.6°), and the short curled tail study (unchanged; the organism review was not run).
5. **Rig contract.** The RD meshes are remeshed references, not the 13,380-vertex rig contract. Any production transfer needs its own validation (§7 of the order).

## 9. Files and hashes (SHA-256; the full list is in `SHA256SUMS.txt`)

| Artifact | Hash |
|---|---|
| `final/GO-RD3-REF.obj` (= `proportion/GO-RD3c-REF_proportion.obj`) | `6e7ce39eae3f2e70660ef3adba3bfd2c19c0884877c463639954d82feaa1b7f3` |
| `final/GO-RD3-LOW.obj` | `0e30fb427d85e09294467f386d27c0fb1e9bd8533d370ad4217d9175c660fc28` |
| `stance/GO-RD3a-REF_stance.obj` | `ba6f103e5dae09f53345661c8f35da013476d8d51552206d2175d831c803ec85` |
| `surface/GO-RD3b-REF_surface.obj` | `79c513bd22141b27df28e56c6535ebeca590526dc1e911de2dcee0f2d1a3100c` |

RD0, RD1, RD2, the 05N LOW, the 05N scorer outputs and all earlier lineages are unchanged.

I stopped at the RM-OT-05O author gate. No acceptance, Stage C, RD4, canon promotion or further redesign.

---

## Follow-up correction (added by RM-OT-05P, 2026-10-12; measurements and scores above unchanged)

- **REF/LOW preservation is NOT PASSED for 05N/05O.** The iliac crest / ASIS (measured p95 0.67 cm, max 0.78 cm) and the sacral platform (p95 0.25 cm, max 0.35 cm) moved. "PASS with one design flaw" in §6 and in the gate table must not be read as acceptance. The LOW is rebuilt from the repaired REF with real protection in `reviews/claude-rac-rm-ot-05p-gorrund-anatomical-repair-gate.md`.
- **05O's stance instruction was not sagittal-only.** The coronal alignment (knee 3.1–4.5 cm lateral of the hip–ankle line) was left unresolved here. It is addressed in 05P stage A.
- **Kept as corrected:** the 05N "20° knee flexion" diagnosis was wrong. The 05N leg was nearly straight but inclined backward from the hip, and should not be called a bent knee.
- **Author check:** the author independently verified the 50 v119 manifest files. The sculpt and scoring results in this report are Claude's reported execution; the author did not rerun them.
