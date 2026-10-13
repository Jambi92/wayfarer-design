# RAC RM-OT-05P: Gorrund anatomical repair and LOW protection (author visual checkpoint)

**Order:** `reviews/chatgpt-rac-rm-ot-05p-gorrund-anatomical-repair-low-protection-order.md` (bcab9bc)
**Source commit of this study:** bcab9bc (parent 64a8925)
**Author:** Claude
**Date:** 2026-10-12
**Evidence:** `reviews/rac-rmot05p-evidence/` (`SHA256SUMS.txt`, `REPLAY.md`)
**Tools:** `tools/rac/w1/rmot05p_drivers/`

## Status

| Line | Status |
|---|---|
| Declared working baseline | **GO-RD3b** `reviews/rac-rmot05o-evidence/surface/GO-RD3b-REF_surface.obj`, sha256 `79c513bd22141b27df28e56c6535ebeca590526dc1e911de2dcee0f2d1a3100c`. Frame: RD2 trunk +3.55 cm; legs after the 05O hip rotation. Not accepted. |
| RD3c (shaft lengthening) | Not used. Failed evidence, frozen. |
| 05O closure correction | **ADDED** (appended to the 05O gate; old numbers unchanged) |
| Stage A, coronal stance | **DONE** (bow corrected on the proxy axes) |
| Stage B, trunk / pelvis repair | **DONE, small effect** (§4) |
| Stage C, joints / surface | **C2 / C3 DONE, small effect**. **C1 arm pose clearance ATTEMPTED and REJECTED** (artifacts) |
| LOW rebuilt from the repaired REF | **CREATED** |
| LOW protected-region preservation | **PASS ON MEASUREMENT** (vertex-identical: protected interiors move 0.000 cm; independent surface distance 0.0) |
| Internal visual review | **FAIL / NOT CREDIBLE AS A REFERENCE** (§7) |
| Replicated blind study / scaffold / canon reconciliation | **NOT RUN** (order) |
| Gorrund | **UNACCEPTED** |
| Grask E3 | **FROZEN** |
| RM-OT-05 | **OPEN** |
| Stage C | **BLOCKED** |
| D4 / UE5 / production rigging / creator implementation | **NOT STARTED** |
| Canon promotion | **NOT PERFORMED** |
| Source master | Unchanged; `base.glb` hash `78ecfa87d169380ecb46ece3f0c0df3491d10e4547038a3c35c06df933f38a7b` |

**Bottom line**

The bounded RD4 study did what each stage asked mechanically:
- the bow-legged coronal chain is now straight on the proxy axes;
- a slight lower-trunk minimum was restored;
- the knee bulb, popliteal pit and instep were softened;
- the LOW now truly leaves its protected regions untouched.

**Visually, RD4 is only a marginal change from RD3b and is not a credible reference.** The comparison with the untouched source (`compare/02_bodyonly_MATCHED_DISPLAY.jpg`) shows the main problem clearly. The 05N field rebuild (voxel remesh, blur, large-radius opening, z-relaxation) erased almost all of the source's surface anatomy. The RD bodies read as smooth, soft clay. Local edits on that surface cannot bring the anatomy back. I recommend a different route; it is in §8 for the author.

## 1. Correction of the 05O closure (§2)

Appended to `reviews/claude-rac-rm-ot-05o-gorrund-rd3-controlled-correction-gate.md`. The old text and scores are untouched.

- 05N/05O REF/LOW preservation is **NOT PASSED**. The iliac crest / ASIS (p95 0.67, max 0.78 cm) and the sacral platform (p95 0.25, max 0.35 cm) moved.
- 05O's stance instruction was not sagittal-only. The coronal alignment had been left unresolved.
- The corrected finding stands: the old "20° knee flexion" was wrong. The 05N leg was nearly straight but inclined backward from the hip.
- The author checked the 50 v119 manifest files; the results remain Claude's reported execution, not an author rerun.

## 2. Plan (`plan/`)

**Disclosure.** The plan sheets were drawn from the pre-edit baseline measurements, but committed together with the results. No separate plan commit preceded the edits.

| File | Contents |
|---|---|
| `plan/baseline_RD3b_views_axes.jpg` | Baseline front / profile / rear / 3/4, real scale, with the proxy hip–knee–ankle axes |
| `plan/RD4_plan_zones.png` | X-ray projection of the planned zones: A leg chain (green), B trunk zones (blue; plot only, the edit excludes the arms), C joint zones (purple), LOW protected skeletal regions (red) |
| `baseline/RD3b_leg_axes.json` | Baseline axes |

**Baseline axes:** sagittal thigh 4.3°, shank 3.4°, knee 0.38 cm ahead of the hip–ankle line (no flexion). Coronal knee **3.13 cm lateral** (bow).

**Landmark uncertainty.** The joint centres are proxies: section mid-point line fits at declared heights. The hip centre's X is about ±3 cm uncertain, so the bow magnitude itself is about ±1.5 cm.

**Inherited source forms vs 05N artifacts**

| Origin | Forms |
|---|---|
| Inherited from F1 | Bowed leg chain, supra-patellar narrowing above a bulbous knee, large forearms / hands / feet, paw-like toes, arms hanging against the trunk |
| 05N reconstruction artifacts | Lower-trunk thickening, the pelvis zone rebuilt by a large-radius opening plus z-relaxation (smeared pelvis breadth up to ~135 cm), the wrap-relaxed tubular shank, global blur / voxel softening |

**Intended load path.** Thorax over a deep pelvis; the femoral heads carry the load into straight, slightly abducted legs (stance width kept); plantigrade feet flat. Large but integrated joints.

## 3. Stage A: coronal stance (`A_coronal/`)

**Operation** (`p_coronal.py`): rigid articulated chain, bilateral mirror, linear-blend weights.

| Joint | Rotation |
|---|---|
| Hip | Adduction **3.43°** about the AP axis, so the knee sits on the hip–ankle line |
| Knee | Coronal **−7.16°**, returning the ankle to its original X (stance width unchanged, 24.69 cm) |
| Foot | Counter-rotated **3.72°** so the sole stays flat |

- Blend: pelvis → thigh z 120 → 98; knee band ±5 cm; foot band ±4 cm; the two legs share the midline 50/50. Forearms and hands are excluded.
- Lengths exact: thigh 52.107 → 52.107, shank 47.634 → 47.634 cm. Grounding +0.20 cm. Max z 240.49 → 240.68 cm. Volume 307.77 → 308.04 L (+0.27 L from the blend zone).
- Independent refit on the final RD4 (`C_limbs/RD4_leg_axes.json`): coronal knee **−0.53 cm** (was +3.13); sagittal knee +0.09 cm (no hyperextension); thigh / shank fitted 52.0 / 47.5 cm.
- Checkpoint: `A_checkpoint_baseline_vs_RD4A.jpg` (identical camera; real scale; axes drawn).
- **Visual:** the knees come in and the legs read straighter. The bulky knee and calf contours still make the legs look bowed from the rear 3/4.

## 4. Stage B: trunk / pelvis (`B_trunk/`)

**Operations.** All are named, mesh-based and arm-excluded. Arm vertices are found by the arm medial edge, and trunk edits fade within 2–6 cm of the arm. The displacement and the normals are diffused before applying.

| Zone | Change |
|---|---|
| **B1** flank roll above the iliac crest (05N thickening + pelvis smear) | −3.0 cm lateral at z 124–146 |
| **B2** lower-trunk wall below the costal margin | −1.2 cm (partial reversal of the 05N thickening) |
| **B3** lower rib-cage lateral wall | **+2.0 cm**. Reconstruction of continuity where the source V-taper and the 05N latissimus deflation left a 43.5 cm pinch. Documented as reconstructed. |
| **B4** convex reconstructed lateral pelvis | −1.0 cm |
| **B5** strokes | Subtle iliac crest (lateral only), ASIS, sacral dimples, flat sacral platform, gluteal fold, lateral hip hollow behind the greater trochanter, trochanter prominence, inguinal transition, blend |

**Trunk breadth, arm-separated** (`RD4A_trunk_profile.json` → `RD4B_trunk_profile.json`; cm):

| z | 104 | 116 | 124 | 128 | 132 | 148 | 152 |
|---|---|---|---|---|---|---|---|
| Before | 63.0 | 60.5 | 57.0 | 56.5 | 58.5 | 45.5 | 43.5 |
| After | 62.5 | 59.0 | 55.5 | 55.0 | 57.0 | 47.5 | 46.5 |

Stations 134–146 and 156+ are arm-contact slices; their breadth is unreliable there.

- **Effect is small.** The diffusion that prevents crumpling also diluted the planned amounts (B1 achieved about −1.5 cm, not −3). Volume 308.04 → 307.10 L.
- A first, undiffused attempt crumpled the surface at the elbow contact. It was replaced; no file was kept.
- Close views: `B_checkpoint_close.jpg`.
- **Visual:** a slight waist now shows in front view. Iliac and sacral landmarks are faint. The pelvis is still the widest part of the trunk, and the trunk still reads columnar behind the hanging arms.

## 5. Stage C: knee / shank / ankle and arms (`C_limbs/`)

**C1 arm pose clearance: REJECTED** (`C1_rejected/`). This was a field-based split of the arms from the trunk (3-D marker watershed), 5–6° abduction about a declared glenohumeral centre (29, −1, 184), and remesh.

It produced a severed upper arm at the split (about 155–158 cm) and comb-like ridges over the deltoid, because the rigid split cannot represent the fused shoulder. Mesh-based skinning would stretch the fused contact surfaces into webs. A coherent pose clearance was not achievable with this tooling, so I stopped that edit as the order requires. **The arm–trunk contact windows remain.**

**C2 region edits** (diffused normal displacement):

| Edit | Change |
|---|---|
| Knee medial bulge | −1.6 cm |
| Knee lateral bulge | −1.4 cm |
| Distal thigh (fill the supra-patellar waist) | +1.6 cm |
| Popliteal fossa | +1.4 cm |
| Upper shank transition | +0.7 cm |
| Calf belly | +0.8 cm |
| Instep mass | −1.2 cm |

Max actual displacement 1.03 cm; volume 307.04 → 307.07 L.

**C3 strokes:** heel ledge, Achilles line, tibial plane, patellar plane, malleoli, knee periphery.

- Checkpoint: `C_checkpoint_legs.jpg`.
- **Visual:** the knee is a little less bulbous from the front, and the popliteal pit is shallower. The knee still reads as a knob in profile and from the rear, the shank is still tubular, and the toes are still paw-like (**unresolved, not canonized**).
- Hand scale and segment lengths are unchanged.

**Final:** `C_limbs/GO-RD4-REF.obj` (sha256 `7a1d7212…bc5ff06`).

| Measure | Value |
|---|---|
| Crown | **232.75 cm** (the 229 cm nominal issue stays unresolved; no rescale) |
| Max z (ears / mane) | 240.68 cm |
| Crotch / stature | 0.4315 |
| Volume | 307.07 L |

## 6. LOW rebuilt with real protection (`LOW/`)

**Built from GO-RD4-REF**, not from the 05N LOW (`p_low.py`). Vertex-identical normal displacement: correspondence = vertex index.

**Protected regions** (defined before the reductions):
- iliac crest / ASIS, plus the lateral iliac crest;
- sacral platform + tail root;
- sternum;
- clavicle / acromion / girdle;
- knee, ankle, elbow, wrist.

Displacement × (1 − P): P = 1 inside each region, with a 3 cm smoothstep falloff outside. Tissue regions are the 12 named soft-tissue masses (first pass under-reached: −0.6 % volume; radii ×1.4 and amounts ×1.7 recorded in `low_regions.json`). No uniform shrink, no Marchfolk deformation, no remesh or position smoothing afterwards.

**Measured on the delivered meshes**

| Check | Result |
|---|---|
| Protected interiors (1,867 vertices) | max **0.0000**, p99 0.0000 cm by vertex identity |
| Falloff band | max 1.48, p99 0.54, p95 0.09 cm |
| Independent signed surface distance LOW → REF (`o_preserve.py`) | 0.000 median / p95 / max in every protected region |
| Sections (`RD4_REF_LOW_sections.json`, overlays) | knee / ankle / wrist / pelvis Δ area 0.0 %; thigh −19 %; calf −6 %; upper arm −10 % |
| Landmarks | crotch, fingertip, acromion and stature unchanged (≤ 0.01 cm) |
| Volume | 307.05 → 300.49 L (−2.1 %) |

Mask visualisation: `RD4_LOW_masks.png` (x-ray vertex projection).

**Limits.** This proves the mask was obeyed on this mesh. It does not prove the masks sit on the true skeletal landmarks: the regions are hand-placed ellipsoids at proxy positions. The old 0.5 cm rig-ingest tolerance was **not** used as an acceptance criterion.

## 7. Visual checkpoint and honest internal review (`compare/`)

| Sheet | Contents |
|---|---|
| `01_source_RD2_RD3b_RD4_REALSCALE.jpg` | Source (untouched, clothed), RD2, RD3b and RD4: front, profile, rear, 3/4; identical camera / material; real scale with a 10 cm grid |
| `02_bodyonly_MATCHED_DISPLAY.jpg` | The same four, body only, **matched display stature** (labelled) |
| `03_RD4_REF_LOW_REALSCALE.jpg` | REF / LOW in 5 views |
| `04_RD4_organism_REALSCALE.jpg` | Organism review presentation: the body's own leonine head, plus the provisional mane-over-nape and short curled tail unchanged from 05N, carried +3.55 cm and kept attached. **Review only.** |
| `05_close_arm_contact.jpg` | Shoulder / arm contact |

The torso / pelvis, knee / popliteal and shank / ankle closes are the B and C checkpoints. Stature and coordinate records are in the stage records and `C_limbs/RD4_*`.

**Internal review: reject as a reference.**
1. **Clay softness (dominant).** The source F1 has defined anatomy under the clothing: deltoids, pectorals, abdominal wall, quadriceps, calves, knees, a back with erectors and scapulae. RD2, RD3b and RD4 have lost almost all of it to the 05N field rebuild. The body reads as an inflated, softened figure. No local RD4 edit restores this.
2. **Columnar trunk / pelvis block.** The trunk is only slightly improved; the pelvis is still the widest part. The arms still hang against the trunk and frame it as a block (contact windows remain because C1 was rejected).
3. **Knees and shanks.** Coronally straighter, but still knobby in profile and rear; the shank is still a tube.
4. **Extremities.** Large forearms and hands, paw-like toes: unresolved; no redesign was authorised.
5. **Organism.** The head and mane are coherent. The tail study is small, tightly curled and sits low on the buttocks, which reads oddly from the rear; it is provisional and unresolved.

I am not describing RD4 as finished or improved enough to proceed. It is a bounded study that shows the local-repair route has reached its limit on this surface.

## 8. Recommendation for the author (decision, not executed)

Restart the sculpt from the **source surface**, not from the 05N field.
1. Take F1's own mesh.
2. Remove the clothing only where it sits (the loincloth panels, belts, wraps and necklace are separable surface layers in many places).
3. Re-project the source's surface detail onto any reconstructed patch, instead of rebuilding the whole body through a voxel field.
4. Do the stance work (sagittal and coronal) as articulated edits of that detailed mesh.

That would keep the anatomy the author liked in the source and remove only what is clothing. It is a new study and is not authorised here; RD5 is forbidden in this block.

## 9. Files and hashes (SHA-256; full manifest in `SHA256SUMS.txt`)

| Checkpoint | Hash |
|---|---|
| Baseline RD3b | `79c513bd22141b27df28e56c6535ebeca590526dc1e911de2dcee0f2d1a3100c` |
| A: `A_coronal/GO-RD4A-REF_coronal.obj` | `d8d8e8ab27f75e43a24f989a97870942257a60846f57b07b7e45c210d4622385` |
| B1: `B_trunk/GO-RD4B1-REF_displace.obj` | `3bb78a5ae598882face3c2564a1f2dca5b538a4813e17244a1010715b637e772` |
| B: `B_trunk/GO-RD4B-REF_trunk.obj` | `e87db37471dfa1a6f22eac230660e0730413a6a851431682ef72fe2113bc2f34` |
| C2: `C_limbs/GO-RD4C2-REF_joints.obj` | `a7d2a7852180f77d62757c4b1a9e7da5b03793b35e5913194fbda70f31f58216` |
| RD4 REF: `C_limbs/GO-RD4-REF.obj` | `7a1d72123d251aa4ba718f00af693b5cead180f9f75389e850e404a9bdc5ff06` |
| RD4 LOW: `LOW/GO-RD4-LOW.obj` | `5ac46fa40ce4b2f039e8987029226af2bb4db1fe2fb7ad54592380fad6691cf9` |
| Organism overlay: `organism/GO-RD4-ORG-REF.obj` | `d644c07fcb0bcf91d8e9973c075cffd900cbc6a6cefa827050efad2dbf82c7eb` |

RD2, RD3a/b/c and their LOW meshes, the old scoring and all earlier evidence are unchanged. The RD meshes remain remeshed references, not replacements for the 13,380-vertex rig contract.

I stopped at the author visual checkpoint. No RD5, sculpt search, blind retry, scaffold or promotion.
