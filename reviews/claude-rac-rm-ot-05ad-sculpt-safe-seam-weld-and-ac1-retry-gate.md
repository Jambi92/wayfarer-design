# RAC RM-OT-05AD — sculpt-safe seam weld and AC1 retry: return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05ad-sculpt-safe-seam-weld-and-ac1-retry-order.md` (9c21caa).
**Date:** 2026-10-16.
**Evidence:** `reviews/rac-rmot05ad-evidence/`.

## Outcomes

1. **05AD SEAM-WELD PREP PASS / SCULPT-SAFE BASELINE FROZEN**
2. **05AC AC1 RETRY NOT CREDIBLE / STOP**

The retry is far cleaner than the rejected 05AC AC1. It still misses §7's zero thresholds, because of a narrow seam band at the neck base just above the weld scope, plus 5 flipped faces.

## Part 1 — seam weld (05AD)

### How it was done

- The weld ran in the cloud workspace with the Blender **5.2.2** Python module. That matches the PC's version; nothing ran on Tyler's PC.
- The result was written to `E:\…\Gorrund-Neutral-C\05AD\` with the device file tool.
- The immutable 05AB1 files were read, never written. Input `.blend` hash verified: `79727daa…`.
- Tool: `tools/rac/w1/rmot05ad_drivers/ad_seam_weld.py`.

### Candidates (reported before applying; `checks/weld_report_candidates.json`)

| | |
|---|---|
| Coincident duplicate groups, whole body (≤ 0.01 mm) | 37,441 groups / 93,836 vertices |
| Selected: torso/shoulder band 117.0–168.3 cm from floor, protection mask = 0 | **4,541 groups / 11,414 vertices** (sizes 2–9) |
| Max distance inside a selected group | **0.000 mm** (exact duplicates) |
| Excluded (head, neck above 168.3, hands, feet, legs, free tail + root, pelvis) | 32,900 groups |
| Selected bounding box (cm) | x −30.9…35.6, z 117.0…168.3 |

**Scope note.** The tighter AC1 region mask (`GO-05AC_mask_AC1.npy`) would have left 48 of the 1,480 seams opened by the rejected AC1 unwelded. Those 48 sit at the shoulder-cap / upper-back edge. The band rule above, still excluding every protected region, covers all **1,480 / 1,480**.

### Weld applied (`checks/weld_report_applied.json`, `checks/weld_gates.json`)

| §4 gate | Result |
|---|---|
| Vertices | 556,391 → **549,518** (6,873 merged); triangles 1,000,000 unchanged |
| Surface identity | every old vertex lands on its new vertex at **0.000 mm**; triangle-for-triangle identical after remap; vertex Hausdorff 0.000 mm both ways |
| Stature / bounding box | 204.52246 cm; extents identical |
| One connected organism; boundary / non-manifold (position-welded) | 1 / 0 / 0 |
| Self-intersecting faces | 0 → 0 |
| Flipped / degenerate faces | 0 / 0 |
| Protected vertices merged / moved | 0 / 0 |
| Merges confined to | z 117.0–168.3 cm |
| Unwelded seam edges inside the band | 12,134 → **96**. The 96 remaining are at the right wrist/hand, which is protected. |

### Display data removed (geometry unchanged)

UV map, custom split normals, sharp-face flags and selection attributes were removed. §4 allows UV loss for this working derivative. This also brings the `.blend` under the 30 MB device-transfer limit. Positions were verified identical after removal.

### Frozen sculpt-safe baseline

- `GO-05AD_sculpt_safe_baseline.blend`, sha256 `74de02e61dff24751a5e16b41b3b6d8d5f9a1ecc800f86ec944fd9dcb8c4a7bc`. The PC copy was re-hashed after transfer and matches.
- `GO-05AD_sculpt_safe_baseline.glb`, sha256 `c65e1b768fd0f5912dd83a1ee3fff882cc6f4078fa248e47043371352bdcdeda`.
- Both are unmodified since 11:20 (PC modified times unchanged).

## Part 2 — AC1 retry (UI only)

### Method

- Normal Blender UI only: File > Open, Save As `GO-05AD_working_AC1.blend`, Sculpting workspace. No console, scripting workspace or shell.
- Protection: the same four Box Masks as the rejected attempt (head/neck, both arms below the shoulder cap, hips and below).
- Smooth (0.5): abs, pec split, lower-pec shelf, serratus, flank crease, lateral abs, pec–deltoid groove.
- Flatten (0.35): both pecs and the deltoid fronts (front view); the chest profile and deltoid cap (right view).
- Additional Smooth passes from the three-quarter view, the same angle as before.
- Saved `GO-05AD_AC1.blend` (sha256 `73fc8477…`); exported `GO-05AD_AC1.glb` (sha256 `00b86e718bfc90d1d65db835e10400111edd509c671683292cdef50e048c7034`).

### §7 gates (`checks/ac1_gates.json`)

| Gate | Required | Retry | Rejected 05AC AC1 |
|---|---|---|---|
| Topology identical to the 05AD baseline | yes | **yes** | n/a |
| Opened welded seams | 0 | **0 inside the weld band.** 11 unwelded pairs opened *just above* it at the neck base (z 168.5–170.1 cm), max gap **0.10 mm** | 1,480 (max 8.7 mm) |
| Self-intersecting faces | 0 | **27**, all at the neck base (z 169.3–170.3 cm), on those same seams | 3,024 |
| Flipped faces | 0 | **5** (2 at the lower-pec / armpit edge, 2 at the hip-mask edge at z 117, 1 on the flank) | 316 |
| Degenerate faces | 0 | **0** | 310 |
| Components / boundary / non-manifold (position-welded) | 1 / 0 / 0 | 2 / **32** / 0 (the neck-base seam opening) | — |
| Stature / bounding box | preserved | **identical** (204.5225 cm) | identical |
| Protected head / hands / feet / tail | unchanged | **0 vertices moved** | unchanged |
| Moved geometry outside the AC1 region | none | 53 vertices at z 170.0–170.3 cm (neck transition), max **0.07 mm**; everything else within 117–170 cm | — |
| Visual: pec / deltoid / abs / serratus reduction vs the rejected AC1 | clearer | abs and serratus clearly softer; pec split softened; **no crease lines along old seams**; pec mass and deltoid cap only moderately reduced | creased along seams |

Sheet: `views/ad_ac1_compare.jpg` — 05AD baseline | rejected 05AC AC1 | 05AD AC1 retry | retry defects (front and profile).

## Root cause of the remaining failures

- The weld stopped at **168.3 cm**, the neck-minimum line used by the protection mask.
- The head Box Mask edge in the viewport sat about 1–2 cm higher. Brush falloff therefore reached unwelded neck-base seams between 168.3 and about 170.3 cm and opened 11 pairs by ≤ 0.10 mm. That caused all 27 self-intersections and the 32 boundary edges.
- The 5 flips are isolated single faces at mask edges and the lower-pec fold.

## Recommendation (author ruling)

One more bounded derivative would very likely pass:
1. Extend the 05AD weld band to about **172 cm**, covering neck-base seams only, with the same exact-duplicate rule.
2. Re-run AC1 on that baseline. Place the head mask edge at or below the weld boundary, and finish with one light Smooth over the 5 flip sites.

Not done here, because §8 budget is exhausted.

## Files on Tyler's PC (`…\Gorrund-Neutral-C\05AD\`)

- `GO-05AD_sculpt_safe_baseline.blend` / `.glb`: **FROZEN** (pass).
- `GO-05AD_working_AC1.blend`, `GO-05AD_AC1.blend`, `GO-05AD_AC1.glb`: retry, **not promoted** (evidence).
- 05AB1 and 05AC files untouched.

## State

- Budget used: 1 topology-prep derivative and 1 AC1 retry.
- No AC2 / AC3.
- Gorrund **UNACCEPTED**; Grask E3 **FROZEN**; RM-OT-05 **OPEN**; Stage C **BLOCKED**.
