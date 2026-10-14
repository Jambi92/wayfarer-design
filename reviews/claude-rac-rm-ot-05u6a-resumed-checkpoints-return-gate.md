# RAC RM-OT-05U6A: resumed desktop checkpoints, return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05u6a-resume-remaining-desktop-checkpoints-order.md` (b344af7).
**Parent order:** 05U6 (a5279b1). **Parent gate:** `reviews/claude-rac-rm-ot-05u6-targeted-desktop-notch-repair-gate.md` (c4b2634).
**Evidence:** `reviews/rac-rmot05u6-evidence/` (`checkpoints/cp2`, `checkpoints/cp3`, `return_u6a/`, `diagnostics/`, `EDIT_LOG.md`).
**Verifier:** the unchanged U6 contract, `check_return_u6.sh` with the frozen `u6_sets_v1.json` (`34646b31…`) and `crease_reference_v1.json` (`c1efefde…`). No threshold, set, ring or scope changed.

## **TECHNICALLY VALID BOUNDED RETURN / AUTHOR VISUAL REVIEW REQUIRED**

The return is checkpoint 3, `GO-05U6_cp3.blend` (sha `22345d4d…6029`). Every U6 mandatory gate passes and `aggregate_u6.json` exits 0.

**Visual caveat for Tyler:**
- The lower notch / sliver cluster and the underside spike are clearly reduced.
- The groove, deltoid and triceps relief are preserved, with no new dent, lip, spike or melted patch.
- **The upper saw-tooth cuts along the crease line remain visible.** They sit at roughly z 169.4–172.3 cm, mostly above the cap's top (z ≈ 170.1). The geometry there is frozen ring (61522, 61771, 62027) and protected skin outside U2 (61586, 61183, 62063) (`diagnostics/cp3_upper_crease_roughness.txt`).
- That region is outside the U6 authorization and was not touched. None of those vertices exceeds 36.3°: the cuts are visible shading facets, not roughness outliers.

The order's visual success clause (upper saw-tooth resolved) is therefore **not** met. Per the order, this is a technically valid result that is visually questionable, stopped for Tyler's review rather than iterated. The budget is fully spent in any case.

| Item | State |
|---|---|
| Gorrund | **UNACCEPTED** (pending Tyler's visual ruling) |
| Grask E3 | FROZEN |
| RM-OT-05 | OPEN |
| Stage C | BLOCKED |
| Edited skin | INFERRED |
| Canon promotion | NOT PERFORMED |
| D4 / UE5 / production rigging / creator implementation | NOT STARTED |
| `base.glb` | unchanged |
| Rodin | not run |

## 1. Checkpoints (real desktop Blender 5.2.2, Edit Mode)

Each move was a vertex picked by click, confirmed by its coordinates, then given a hand-chosen typed position (`EDIT_LOG.md`).

| CP | Moves | U6 result |
|---|---|---|
| cp1 (05U6) | 61303 +0.25, 62065 +0.20 along their normals; 61405 to its neighbour centroid | NOT MET: R1 on 61559 54.23, 61581 42.43, 61580 40.95 |
| **cp2** (resumed from cp1 `6262620e…`) | 61559 +0.30, 61581 +0.10, 61750 +0.10 along their normals, as documented | NOT MET: R1 on **61581 only (45.44)**. Crease A 0.7890 |
| **cp3** (final small correction inside the target) | 61652 +0.12 along its normal (the 0.22 cm dent tilting outlier face 130354) | **PASS, all gates, exit 0** |

- 61580, the crease-B anchor, was **never moved**; 61750 fixed it indirectly (40.95 → 26.38).
- The budget is spent: cp1, cp2 and cp3. 05U5 remains completed evidence.

## 2. Target roughness (all 16) and frozen crease depths

Limit 36.3°; bold marks over the limit. Source: `diagnostics/target_roughness_by_checkpoint.md`.

| S3 vertex | 05U baseline | cp1 | cp2 | **cp3** |
|---|---|---|---|---|
| 61130 | 24.01 | 14.40 | 14.40 | 14.40 |
| 61219 | 34.25 | 12.50 | 20.93 | 20.93 |
| 61303 | **47.95** | 29.60 | 32.74 | 32.41 |
| 61368 | 14.22 | 11.39 | 14.23 | 16.95 |
| 61405 | 28.97 | 0.01 | 7.85 | 7.85 |
| 61559 | 35.11 | **54.23** | 16.64 | 14.97 |
| 61562 | 35.21 | 36.02* | 35.29 | 35.29 |
| 61580 | **40.95** | **40.95** | 26.38 | 26.38 |
| 61581 | **47.85** | **42.43** | **45.44** | 32.07 |
| 61652 | 28.71 | 34.29 | 32.45 | 15.65 |
| 61727 | 21.38 | 21.38 | 24.77 | 24.77 |
| 61750 | 27.95 | 27.95 | 4.92 | 4.92 |
| 62061 | 29.57 | 29.57 | 27.12 | 27.12 |
| 62065 | **36.57** | 25.16 | 26.15 | 26.15 |
| 62086 | 34.70 | 34.70 | 17.95 | 17.95 |
| 70433 | 17.48 | 18.57 | 16.63 | 16.63 |
| **Max** | 47.95 | 54.23 | 45.44 | **35.29** |
| **Crease A ≥ 0.6713** | 0.8951 | 0.8951 | 0.7890 | **0.7890** |
| **Crease B ≥ 0.2743** | 0.3658 | 0.3658 | 0.3658 | **0.3658** |

*At cp1, 61562 at 36.02 was below the limit; only 3 vertices exceeded it.

## 3. U6 gates for the return (`return_u6a/checks/aggregate_u6.json`, exit 0)

**All PASS:**
- U2 protection; 0 moved outside the 365; 0 moved on the 106 ring; topology unchanged;
- V1-U2; no FAIL verdict; V2; V3; V5; V6c-3;
- crease A 0.7890 and B 0.3658 (frozen reference, by identity);
- **R1 target roughness, max 35.29**;
- R1 exception identity: 70735, 70592 and 70408 bit-exact;
- locus: 0 editable vertices moved outside the target;
- **R2 cap quality**: minimum cap angle 13.63; face 130139 **6.24 → 14.87**; no degenerate, inverted or out-of-band face or edge.

**Reported globally, not waived and unchanged in scope:** V4 (8 taper edges), V6 historical, V6c-1 (θ −90) and V6c-2 (anterior taper) still fail. The far-posterior and anterior offenders are untouched by design.

## 4. Exact changes (return vs the 05U baseline)

**7 vertices**, all inside the 16-vertex target:

| Vertex | Baseline (cm) | Return (cm) | Moved |
|---|---|---|---|
| 61303 | (28.4065, −12.2459, 167.4383) | (28.589, −12.416, 167.458) | 0.250 |
| 61405 | (28.5595, −13.3114, 168.7177) | (28.620, −13.378, 168.827) | 0.142 |
| 61559 | (28.7675, −12.1007, 167.7268) | (28.915, −12.359, 167.679) | 0.301 |
| 61581 | (28.7970, −12.8169, 168.6922) | (28.860, −12.883, 168.652) | 0.100 |
| 61652 | (28.8853, −12.5128, 168.3566) | (28.929, −12.608, 168.298) | 0.120 |
| 61750 | (28.9971, −13.3585, 170.0225) | (29.031, −13.434, 169.968) | 0.099 |
| 62065 | (29.4131, −11.9516, 167.5247) | (29.391, −12.150, 167.517) | 0.200 |

**25 faces touched:**
- **18 cap faces:** 129905, 129907, 130133, 130134, 130135, 130137, 130138, 130139, 130140, 130141, 130142, 130143, 130144, 130353, 130354, 130355, 130356, 130539.
- **7 strip faces:** 140468, 140482, 140483, 140485, 140488, 140514, 140791.

The legacy diagnostic stays within the authorized 15 / 35. No topology change.

## 5. Evidence and package

**`return_u6a/`:**
- the return `.blend` (`22345d4d…`);
- `return.npz`, `return.obj.gz`, `result.obj.gz`, maps and labels;
- verify, crease, `guards_u6`, `aggregate_u6`, the historical U4 aggregate and `guards`;
- `RETURN_HASHES.sha256`;
- identical-camera 05U-baseline vs return views: posterior shaded / wire, zoom shaded / wire, arm context, and lateral / 3-4 / underside.

Checkpoint evidence is in `checkpoints/cp1–cp3/`.

**Package:** `gorrund_05U6A_bounded_notch_repair_return.zip` (a new, distinctly named package with its own manifest). Clean extraction, CRC check and the corrected-path rerun on the extracted scene are recorded in `package_u6a/`.

**→ STOP for Tyler's visual review.** The upper crease saw-tooth lies outside the authorized region and is the main open visual question.
