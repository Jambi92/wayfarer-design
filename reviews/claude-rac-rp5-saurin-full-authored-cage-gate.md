# RAC RP5 — Saurin full authored cage: Option B closure gate

Orders:
- `reviews/chatgpt-rac-rp5-saurin-option-b-fold-census-closure-order.md` (fe3b98a);
- `reviews/chatgpt-rac-rp5-saurin-continue-option-b-audit-until-pass-order.md` (50ef121).

Standing directive: de3a185.
Evidence: `reviews/rac-rp5-evidence/saurin/full_cage/optionb_final/`. Tools: `tools/rac/rp/saurin_rp5_v002/`.

## SAURIN RP5 FULL AUTHORED CAGE PASS — READY FOR CHATGPT / AUTHOR REVIEW

Status of the pilot files: **PILOT / NOT FROZEN**. Nothing is frozen.

What was not touched:
- the canonical W2I6 files (229 / 229 immutables unchanged, `immutable_hashes_final.txt`);
- the accepted biology;
- the accepted tail module: sha 559565cc, vertices identical to 1e-12 mm, face list identical.

No rig, UV / material, LOD, creator, UE5 or other-race work was done.

## 1. The cage

`SA_RP5_full_cage_optionb_final.npz` (sha256 `5a1f7a01…`):
- 190,948 V / 190,946 Q, 100 % quads, one closed, consistently oriented manifold (chi 2);
- c1 and c2 share one face list and vertex order.

**Architecture: Option B (author decision), as approved.**
- Body, head, axillary vault patches, nostril pits, hip-root loops and the tail module come from the gated revision cage t2. That design is the authored coarse cage with the thumb fix.
- Hands and feet are the Option B local-density region:
  - every hand / foot coarse quad is split 1 → 4 (`sa_localsub.py`);
  - fine 2:1 transition rings are added at the wrists (Fa6 8 → Wr 16) and the ankles (S10 10 → S11 20).
- The two parts share the authored forearm / shin ring (64 / 80 fine vertices). They are stitched by `sa_graft.py`.
- No loop runs through the body (Option A was not used). There is no accepted fold residual (Option C was not used).
- Merged design (corner names on the assembled indices): `SA_coarse_cage_design_optionb_final.pkl`.

**Local topology additions, all inside the Option B scope:**
- closed digit rings through anisotropic finger blocks (`sa_ringsplit.py`);
- deeper nostril pit insets (2 support rings).

## 2. Fold census: validated, then closed (order 50ef121 §1–§4)

**Authoritative method** (`sa_foldcensus.py`, host-aware).
- Reference normal: the area-weighted normal of the barycentric host faces of the quad's own 4 corners.
- The corners are projected into that tangent plane. In that plane:
  - **bow-tie** = a true crossing of opposite edges (segment test);
  - **inverted** = a simple polygon with signed area < −1e-6 · mean edge²;
  - **concave** = a simple, positively oriented polygon with a signed turn < −0.02.
- No nearest-face or opposite-wall classification is used.

**Old method vs new method** (`audit_prerepair_b5c/census_method_comparison.json`, on the pre-repair Option B cage):
- Old-method false positives: 212 quads, flagged by the old method but simple and correctly oriented on their own source patch.
- Old-method false negatives: 60 quads.
- The new method still found 685 inverted, 345 bow-tie and 360 concave quads. These folds were genuine.
- They sat in web blocks, palm / forefoot blocks next to the webs and 2:1 rows, the thumb base and the orbit fans.

**Fix.** `sa_xparam.py`, local cross-parameterisation:
1. A disk region is formed around each folded group.
2. The source under it is refined locally, and its border is traced as a simple vertex loop. The flood fills the side of that loop with the same orientation as the cage, so the opposite wall of a slot is never used.
3. The source patch is mapped with a mean-value map (bijective). The cage region is mapped with a Tutte map.
4. The cage is optimised inside the map: MIPS energy with a regularised barrier, plus aspect, angle and coverage terms.
5. A region is kept only when its census / coverage / quality score improves.

**Final census, c1 and c2 identical:**

| | Final |
|---|---|
| Inverted (outside tip caps) | **0** |
| Bow-tie | **0** |
| Concave | **0** |
| Concave in deformation-critical regions | **0** |
| Tip caps (exempt) | 1 / 6 / 1 |
| Accepted tail module (unchanged) | 1 / 1 / 6 |

**Visual verification** (`audit_renders/`, 35 sheets):
- Each sheet shows a close-up from outside and from inside (back faces).
- Overlays: quad IDs (flagged ones + every 37th), corner host triangles, edge-0→1 orientation arrows, new-class fill and old-flag hatching.
- Structures covered:
  - every finger web (6) and toe web (8);
  - the palm and forefoot 2:1 rows;
  - the thumb bases;
  - the orbit fans;
  - the wrist and ankle 2:1 rings.
- Deterministic samples of quads whose classification changed are rendered separately (`sample_*.png`).
- The pre-repair sheets are in `audit_prerepair_b5c/`.
- On the final cage, the old method still flags 6 quads (3 of them at the thumb base). All 6 are old-method false positives: ok under the new census and visually clean.

## 3. T-1 – T-7 (`SA_full_cage_optionb_T1-T7.json`)

| Gate | SA-M188 (c1) | SA-F188 (c2) | Target | Result |
|---|---|---|---|---|
| T-1 median / p95 / max (mm) | 0.060 / 0.434 / **2.44** | 0.061 / 0.433 / **2.40** | ≤ 0.5 / 1.5 / 3.0 | PASS |
| T-2 max: head / hands / feet (mm) | 1.32 / 1.17 / 1.15 | 1.32 / 1.16 / 1.13 | ≤ 1.5 | PASS |
| T-2 max: tail root / tail stations (mm) | 0.98 / 1.18 | 0.99 / 1.22 | ≤ 1.5 | PASS |
| T-3 stature / bbox | −0.03 mm | −0.03 mm | | PASS |
| T-4 inverted / bow-tie / concave outside tips | 0 / 0 / 0 | 0 / 0 / 0 | 0 | PASS |
| T-4 aspect > 4 outside tip / tail exemptions | **0** (max 4.0) | **0** | 0 | PASS |
| T-4 collapsed edges | none (min edge 0.15 mm, aspect ≤ 4) | none | none | PASS |
| T-4 angles outside 45–135, outside exemptions | 65 quads (0.034 %) | 166 quads (0.087 %) | documented | individually documented (below) |
| T-5 density | within | within | | PASS |
| T-6 landmarks max | 1.03 mm | 1.02 mm | tool pass rule | PASS |
| T-7 silhouette with tail | ≥ 0.996 | ≥ 0.996 | ≥ 0.995 | PASS |

The T-4 aspect count of 13 in the eval JSON includes the claw / toe tip caps and the tail module. Outside those exemptions the count is 0.

**Angle residual register** (`SA_T4_angle_residuals.csv` / `.json`). One row per quad, per configuration, with:
- region and authored structure;
- min / max angle and aspect;
- centre and nearest landmark;
- fold class (all ok) and the deformation-critical flag.

Severity on c1:
- 59 mild (≤ 5° outside the band);
- 2 moderate: trunk quads at the sacral flank near the tail root (min angles 37.7° and 38.8°);
- 4 strong:
  - quad 2049, trunk, sacral flank (32.7°);
  - quad 54957, trunk, xneg axilla (34.8°);
  - quad 83708, xneg thumb base (10.8°);
  - quad 85405, xneg palm 2:1 row (18.6°).

All of these are convex, correctly oriented and have aspect ≤ 3.5, and their deformation steps are clean (§4). Repeated local repairs at the two thumb-base quads traded the angle against a concave corner, so they stay as documented residuals.

The extra c2 quads are mild (≤ 5°) hip / pelvis / trunk quads from the SA-F188 body shape on the shared face list.

## 4. Closure reruns on the final cage

**Deformation, 4-step ownership** (`SA_deformation_4step_final.json`). 34 poses:
- jaw;
- neck flexion / rotation;
- shoulder abd45 / abd90 / flex;
- elbow 90 / 130;
- hip, knee, ankle;
- fist, grasp, opposition;
- toe flexion / extension;
- trunk twist, lower axial flexion;
- tail-root lateral / vertical bends, tail twist.

Results: **0 TOPOLOGY-classified poses** and **0 step-4 topology-only flips**. 33 poses are WEIGHTING / SCAFFOLD and 1 is CLEAN. The xneg fist / grasp topology flips that showed up during the work are gone on the final cage.

**PD-2 creator states** (`SA_PD2_ownership_final.json`). All 19 states give **0 cage-owned flips**, including T80, FAHI, MUHI, MUFAHI and B-T80. The source-owned flips in high fat / muscle states sit over folds of the dense source (98 / 25 / 169).

**Head creator states:** ORB-8, ORB+3, RDG0.90, RDG1.30, DSP-LOW and DSP-HIGH all give 0 cage flips.

**Detail layer** (`SA_detail_layer_final.json`), on c1, c2 and creator state NAR:
- p95 deviation is 0.449 mm;
- detail edge-jump p99.9 is 1.564 mm against the canonical 1.581 mm;
- max is 2.30 mm against the canonical 2.41 mm;
- no cage-induced discontinuity.

**Direct identity metrics** (`SA_identity_metrics_final.json`):
- stature −0.003 cm;
- thorax / pelvic band ≤ 0.31 cm;
- joint ratios from the cage's own rings ≤ 0.0007;
- rostral projection −0.03 cm, orbit spacing −0.02 cm;
- tail areas ≤ 0.18 cm².

**Semantic map** (`SA_semantic_map_final.json` + `.face_semantic.npy`):
- 210 authored loops. The only open ones are the same as before, open by design: T2, P1–P3, Hd10 and the mouth slit.
- Face classes include hand / foot density (finger 16,896, palm 13,824, toe 20,864, foot 10,240 …) and a `2:1 reduction row` class of 18,432 faces (wrist / ankle transitions and palm / forefoot rows).
- Topology sha `255645a1…`.

**Boards A–P** (`boards/`, 43 sheets, no WIP labels). Hand / foot web close-ups: `boards/G_hand_*`, `boards/I_foot_*` and the web / row close-ups in `audit_renders/`.

**Pilot files** (`pilot/`):
- `SA_M_REF_RP5_pilot_v001.blend` and `SA_F_REF_RP5_pilot_v001.blend`;
- sidecar JSON and barycentric map.

Read-back: face list identical, semantic attribute identical, vertex error 7.6e-6 cm, same topology sha. Status **PILOT / NOT FROZEN**.

## 5. Tools added in this order

| Tool | Purpose |
|---|---|
| `sa_xparam.py` | Cross-parameterisation repair with census / coverage / quality score |
| `sa_gsmooth.py` | Global L-BFGS on the source with census-frame barrier and fold / aspect roll-back |
| `sa_ringsplit.py` | Local closed digit rings |
| `sa_graft.py` | Assembly + merged design |
| `sa_audit_renders.py` | Old / new census comparison + close-ups |
| `sa_angle_residuals.py` | T-4 angle register |

`sa_vault.py` now gives distinct pocket targets, so it no longer collapses edges. `sa_qopt.py` and `sa_gopt.py` gained `FREEZE_LABELS`.

STOP FOR CHATGPT / AUTHOR REVIEW.
