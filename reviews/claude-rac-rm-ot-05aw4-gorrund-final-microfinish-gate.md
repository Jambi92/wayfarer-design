# RAC RM-OT-05AW4 — Gorrund final nail micro-finish: return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05aw4-gorrund-final-microfinish-order.md` (a9710d1)
**Sequencing:** `reviews/chatgpt-rac-autonomous-continuation-aw4-ax4-stagec-order.md` (38dfda0)
**Source:** `GO-05AW3_C.blend` (sha `1d68c9f5…23cc78`, verified).
**Executor:** Claude.
- Both shape edits were authored in the Blender 5.2.2 UI on Tyler's PC: a Mesh Filter and Hook modifiers.
- Cloud scripts were used only for the mask and weight groups (0.000 mm change), prediction, read-back, gates, evidence, and the freeze (removing the mask attribute; geometry identical) plus the GLB export.
- Blender is closed.

## Verdict

**05AW4 FINAL NAIL MICRO-FINISH PASS / READY FOR FINAL GORRUND CLOSURE REVIEW**

Both remaining 05AW3 misses are resolved:

1. **Side-wall groove / inlay read materially reduced.** The AW4-A bevel works on the plate edge itself.
   - The dark trench lines along the side walls are gone in 3/4 views.
   - The outline still reads as a soft raised rim, and the plate still sits proud in front view.
   - See `views/AW4A_sidewall_closeups.jpg` and `views/AW4_vs_AW3_front_top_34.jpg`.
   - Edge-band crease angle drops: median 5.1° → 2.6°, p90 9.4° → 6.5°, p99 16.7° → 11.3° (`checks/AW4_sidewall_metric.json`).
2. **Every lesser nail now projects 1.55–1.58 mm** (floor 1.50, ceiling 1.70).
   - Big toes are unchanged at 1.74 / 1.69 mm.
   - The curl is untouched.

The technical gate is fully clean.

## 1. Files (PC `...\Gorrund-Neutral-C\05AW4\`; `checks/AW4_files_and_operations.json`)

| File | sha256 | Role |
|---|---|---|
| `GO-05AW4_prep.blend` | `06f97a18…c1b5` | source + bevel mask + groups `AW4_LP` / `AW4_RP` |
| **`GO-05AW4_A.blend`** | `3826c564…cddd1` | **AW4-A** plate-edge bevel |
| **`GO-05AW4_B.blend`** | `63cf0924…8d32` | **AW4-B** lesser-toe projection |
| **`GO-05AW4_nails_final.blend`** | `5a4e45d40158e7dc92f6f8ba13d67ada2403e3e3dcda9048382323ee43a22d5e` | **FROZEN** = AW4-B geometry (difference 0.0), mask attribute removed, 1 mesh object, no modifiers |
| **`GO-05AW4_nails_final.glb`** | `e6b325039993b48de1daf1b82da7054c9f466131daf41c2dcc14a0709adb6fc8` | **FROZEN** GLB (27.9 MB) |

Both final files were staged back from the PC; the hashes match.

The optional cleanup checkpoint was not used. The soft crease above the R3 nail remains; it is minor.

## 2. Operations

**AW4-A — plate-edge bevel.**
- Mesh Filter **Smooth**, one long drag: about 33 Laplacian iterations. In simulation the result is safe from 25 to 80 iterations.
- Mask: a band from 1.4 mm inside to 0.8 mm outside each plate outline, with 0.6 mm ramps.
  - The distal 12 % of each plate is excluded, so the free edge and projection are untouched.
  - Projection was unchanged by A.
- Peak move 0.62 mm.
- Plate core height kept: mean drop 0.015 mm.

**AW4-B — lesser-toe projection.** Two Hooks with No Falloff:
- weight groups `AW4_LP` and `AW4_RP` hold the lesser-toe forward profile from 05AW3, scaled per nail to reach 1.58 mm;
- empties are typed 0.35 mm along each foot axis;
- added: L2 +0.17, L3 +0.16, L4 +0.18, R2 +0.24, R3 +0.24, **R4 +0.30 mm**.

R4 needed slightly more than the order's "approximately +0.15–0.25" to reach the 1.5 mm floor.

Read-back vs model: max 0.00007 mm.

## 3. Per-nail projection (`checks/AW4_projection_per_nail.json`)

| Nail | AW3 (mm) | **AW4 (mm)** | Free edge ahead of toe pad (mm) |
|---|---|---|---|
| L1 | 1.74 | **1.74** | 4.09 |
| L2 | 1.40 | **1.58** | 3.27 |
| L3 | 1.42 | **1.58** | 3.54 |
| L4 | 1.40 | **1.57** | 3.11 |
| R1 | 1.69 | **1.69** | 3.32 |
| R2 | 1.31 | **1.56** | 3.35 |
| R3 | 1.33 | **1.57** | 3.45 |
| R4 | 1.25 | **1.55** | 3.37 |

## 4. Technical gate (final = AW4-B; `checks/AW4B_final_gate.json`)

| Check | Result |
|---|---|
| Self-intersections | 0 |
| Seams opened | 0 |
| Degenerates | 0 |
| Welded components / boundary / non-manifold | 1 / 0 / 0 |
| Genus | 3 (unchanged) |
| Folded / flipped faces vs local surface | **0** |
| Old vertices moved outside the support | 0, max 0.000 mm |
| New vertices outside the support | 0 |
| Ankle drift L / R | 0.0 / 0.0 mm |
| Stature | unchanged (204.52 cm) |
| Lowest moved vertex | 2.62 mm above the floor; no ground intersection |
| Toe contact | none new (SI 0) |
| Foot length vs 05AV | **L +1.43 mm, R +2.43 mm** (limit 3.5) |
| Footprint width | unchanged |
| Heel lift | L −0.009 cm (measurement shift from the longer foot; no heel vertex moved), R 0.0 |

**"Inverted vs source surface" (old coarse reference metric): 12.**
- 11 are carried over from AW3.
- The new one is face 1120828 at the L2 free edge, which faces outward (now · local 0.55).

AW4-A was gated separately and is clean (`checks/AW4A_gate.json`).

**Protected regions.** Everything outside the nail supports is 0.000 mm. See `views/AW4_final_whole_body.jpg` and `views/AW4_final_feet_front.jpg`.

## 5. Visual gate (§8)

| Item | Result |
|---|---|
| Crack / chip / split read stays gone | ✓ |
| Side-wall groove / inlay read materially reduced | ✓ |
| Clear readable outline | ✓ |
| Plate slightly proud of toe | ✓ |
| All nails show profile projection | ✓ (`views/AW4_vs_AW3_profiles.jpg`) |
| Lesser-toe projection ≥ 1.5 mm | ✓ (1.55–1.58) |
| Mild curl remains | ✓ |
| Feline taper | ✓ |
| No exaggerated hook / talon | ✓ |
| Feet coherent | ✓ |

## 6. Evidence (`reviews/rac-rmot05aw4-evidence/`)

**Views:**
- `views/AW4_vs_AW3_front_top_34.jpg`
- `views/AW4_vs_AW3_profiles.jpg`
- `views/AW4A_sidewall_closeups.jpg`
- `views/AW4_final_feet_front.jpg`, `views/AW4_final_whole_body.jpg`

**Checks:**
- `checks/AW4A_gate.json`, `checks/AW4B_final_gate.json`
- `checks/AW4_projection_per_nail.json`
- `checks/AW4_sidewall_metric.json`
- `checks/AW4_files_and_operations.json`

**Tools:** `tools/rac/w1/rmot05aw4_drivers/`

## 7. State

STOP 05AW4. Under the continuation order, 05AX4 runs next.

| Item | Status |
|---|---|
| Toenail morphology | **FINAL MICRO-FINISH PASS** (`GO-05AW4_nails_final`) |
| RM-OT-05 | OPEN, pending AX4 |
| Stage C Gorrund blocker | BLOCKED, pending AX4 |
| Grask E3 | FROZEN |
