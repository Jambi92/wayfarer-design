# RAC RM-OT-05AE — extended seam weld and final AC1: return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05ae-*.md` (6ace97d).
**Date:** 2026-10-16.
**Evidence:** `reviews/rac-rmot05ae-evidence/`.

## Outcomes

1. **05AE EXTENDED SEAM-WELD PASS / FINAL AC1 BASELINE FROZEN**
2. **05AC AC1 FINAL RETRY FAILED / HUMAN SCULPTOR OR RETOPOLOGY REQUIRED**

Stopped. No further autonomous AC1 retry.

## Part 1 — extended weld (05AE)

The weld started from the frozen 05AD baseline. Its hash was verified as `74de02e6…`. It ran in Blender 5.2.2 (bpy) in the cloud workspace; tool: `tools/rac/w1/rmot05ae_drivers/ae_seam_weld.py`.

| | |
|---|---|
| Newly merged vs 05AD | **280 groups / 302 vertices**; sizes 2–5; max intragroup distance **0.000 mm** |
| z range | **168.31–171.98 cm** (neck base and trapezius tops; muzzle lies forward and above 172) |
| Rule | exact duplicates ≤ 0.01 mm; 117.0–172.0 cm; hands, feet and free tail + root excluded; protection-mask head rule lifted only up to 172.0 cm |
| Vertices | 549,518 → **549,216**; triangles 1,000,000 unchanged |
| Surface identity | vertex Hausdorff **0.000 mm** both ways; triangle-for-triangle identical after remap |
| Stature / bounding box | unchanged (204.52246 cm) |
| Position-welded components / boundary / non-manifold | 1 / 0 / 0 |
| Self-intersections / flips / degenerates | 0 / 0 / 0 |
| Protected vertices moved | 0 |
| Coverage | all 11 neck-base pairs opened in the 05AD retry are now welded |

### Frozen

- `GO-05AE_sculpt_safe_baseline.blend`, sha256 `f1df5b334c6d21c06d39cceeff2a2ddaf4282cba79873a25d3454732192bfca8`.
- `GO-05AE_sculpt_safe_baseline.glb`, sha256 `6b2c672f5139112ed58a8830e6b0ed9da7dda3a66fe499f27f5f15f710d3ef40`.
- On the PC at `…\Gorrund-Neutral-C\05AE\`; unmodified since 12:46.

## Part 2 — final AC1 (UI only)

### Method

- Opened the 05AE baseline with File > Open; Save As `GO-05AE_working_AC1.blend`; Sculpting workspace.
- Masks: four Box Masks. The head/neck edge was placed lower than in 05AD, at about 171 cm, below the 172 cm weld bound.
- Then **Mask > Smooth Mask** once, to soften the transitions as §5 asked.
- Sculpt sequence identical to the 05AD retry:
  - Smooth (0.5): abs, pec split, lower-pec shelf.
  - Flatten (0.35): pecs and deltoid fronts (front view); chest profile and deltoid cap (right view).
  - Smooth: serratus, flank crease, lateral abs, lower-pec edge, pec–deltoid groove (three-quarter view).
- Saved `GO-05AE_AC1.blend` (sha256 `16f62eb23c6f5f7f57c0dc2b8a6d0126a40662d3b6afd3a47be64c5cc1a355d9`). Exported `GO-05AE_AC1.glb`.
- No console, scripting workspace or shell.

### §8 gates (`checks/ac1_gates.json`)

| Gate | Required | Final AC1 |
|---|---|---|
| Topology vs 05AE | coherent | **identical** |
| Neck base (prior failure) | — | **fixed**: no opened pairs or self-intersections above 117 cm |
| Opened seams | 0 | **25 pairs**, max **1.02 mm**, in one ~1 cm patch: left groin/hip seam, x ≈ −12 cm, **z 116.2–117.0 cm** |
| Self-intersections | 0 | **37**, all in that same patch (z 116.0–117.0) |
| Flipped faces | 0 | **5**: 2 in the groin patch; 3 single faces at the lower-pec / armpit edge (z 146, 153); same sites as 05AD |
| Degenerate faces | 0 | 0 |
| Components / boundary / non-manifold | 1 / 0 / 0 | 1 / **50** / 0 (the groin patch) |
| Stature / bounding box | unchanged | unchanged |
| Head / hands / feet / free tail | unmoved | **0 vertices moved** |
| Movement outside AC1 | none meaningful | 288 vertices at 115.7–117 cm (max 1.26 mm); 51 at 170–170.3 cm (max 0.03 mm, welded) |
| Visual | clear reduction | as 05AD retry: abs and serratus largely gone, pec split softened, no seam creases; pec mass and deltoid cap moderately reduced (`views/ae_ac1_compare.jpg`) |

## Why it failed

**Smooth Mask** (requested in §5 for a softer hip transition) spread partial sculptability a few millimetres below the hip box edge. That reached **below the 117.0 cm weld floor**, where seams are still unwelded. One left groin/hip seam opened there; it caused all 25 opened pairs, 37 self-intersections and 50 boundary edges.

The §7 micro-cleanup can fix flips, but it cannot rejoin separated duplicates without a weld, which this order does not authorize below 117 cm. Cleanup was therefore not attempted, and the §8 verdict stands.

## If the author wants one more bounded attempt

The remaining defects are localized and well understood:
- lower the weld floor to about **112 cm**, exact duplicates only, excluding the gluteal / tail-root and genital landmarks;
- keep a hard hip mask edge above 117 cm (no Smooth Mask);
- then one light Smooth on the 3 lower-pec / armpit flip faces.

That is an author ruling. Otherwise, a human sculptor working from `GO-05AE_sculpt_safe_baseline.blend` is the route.

## Files (PC, `…\05AE\`)

- Baseline `.blend` / `.glb`: FROZEN.
- `GO-05AE_working_AC1.blend`, `GO-05AE_AC1.blend`, `GO-05AE_AC1.glb`: final AC1, **not promoted**.
- All prior baselines and rejected attempts untouched.

## Housekeeping

- After export, Blender was closed through its window controls.
- A second Blender window, left open since the morning bridge drop, did not respond to clicks or keys. It is still open for Tyler to close.
- While closing, `05AC\GO-05AC_AC1.blend` was opened by accident from Open Recent and then closed without saving.

## State

- Gorrund **UNACCEPTED**; Grask E3 **FROZEN**; RM-OT-05 **OPEN**; Stage C **BLOCKED**.
- No AC2.
