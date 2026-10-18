# RAC RM-OT-05AW3 — Gorrund final feline nail finish: return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05aw3-gorrund-final-nail-finish-order.md` (f10b6b4)
**Sequencing:** `reviews/chatgpt-rac-autonomous-continuation-aw3-ax3-stagec-order.md` (fd3e67f)
**Source:** `GO-05AW2_nails_final.blend` (sha `75734a39…9206`). It was verified before the first write.
**Executor:** Claude.
- All shape edits were authored in the Blender 5.2.2 UI on Tyler's PC: Mesh Filters and Hook modifiers.
- Cloud scripts were used only for sculpt masks and vertex-group weights (0.000 mm geometry change), prediction, read-back, gates and evidence.
- Blender is closed (single instance).

## Verdict

**05AW3 FINAL NAIL FINISH FAILED / AUTHOR REVIEW REQUIRED**

Per the continuation order §4: STOP. AX3 is not run, Stage C is not released, RM-OT-05 stays OPEN and Grask E3 stays FROZEN.

This is again a near-pass: the main 05AW2 gap is fixed and the technical gate is fully clean. The verdict is FAIL because two order items are not met:

1. **Side-wall groove / inlay read: not materially reduced** (§5, §11).
   - The AW3-A side-wall build-up (Inflate, 0.385 mm on a ring outside the plate side walls) softened the outline lines only slightly. In 3/4 views they still read as incised outlines (`views/AW3A_sidewall_closeups.jpg`, `views/AW3_vs_AW2_front_top_34.jpg`).
   - The crease and concavity statistics on the edge band do not improve (`checks/AW3_sidewall_metric.json`).
   - Root cause: the dark line is the plate's own step wall (about 1–1.7 mm). Raising the surrounding skin 0.4 mm does not change how that wall reads.
2. **Lesser-toe projection slightly below the envelope** (§6).

   | Nail | Forward projection vs 05AW2 (target 1.5–2.5 mm) |
   |---|---|
   | Big toes L1 / R1 | **1.74 / 1.69 mm** (in envelope) |
   | Lesser toes L2–L4 / R2–R4 | **1.25–1.42 mm**, 0.08–0.25 mm short of the 1.5 mm floor |

   - This is my design error: I scaled the lesser toes at 0.8 × 1.8 mm.
   - Drop and curl are in range on all nails: tracked distal vertex 0.92–1.20 mm (target 0.5–1.2).

All 3 authorised checkpoints are used (AW3-A, B, C), so neither item can be corrected without a new order.

**What did work (§7, §11).**
- The profile-read requirement is met. Every nail is now visible in lateral and medial profile, with a down-curving free edge that clears the soft toe tip by **2.9–4.1 mm** (05AW2: 1.5–2.1 mm). See `views/AW3_vs_AW2_profiles.jpg`.
- The front-view clarity of 05AW2 is kept.
- The L1 lower shelf line is removed.
- Specks on L4 / R2 / R3 are reduced. A soft crease above the R3 nail remains.

**Author options.**
- (a) Accept AW3-C as is. Freeze it as `GO-05AW3_nails_final` (blend + GLB; a no-geometry-change export), then run AX3.
- (b) Issue a short order with one more checkpoint:
  - lift the lesser-toe projection by about 0.2 mm (re-weighting the same Hooks);
  - re-shape the side wall itself, i.e. a narrow bevel on the plate edge (Smooth on the plate's own outer 0.6 mm) rather than raising the skin.

## 1. Files (PC `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\source\Gorrund-Neutral-C\05AW3\`; `checks/AW3_files_and_operations.json`)

| File | sha256 | Role |
|---|---|---|
| `GO-05AW3_A_mask.blend` | `1fb32f87…641c` | source + Stage A mask + Hook weight groups (0.000 mm) |
| **`GO-05AW3_A.blend`** | `f89aa8f2…a495` | **AW3-A** side-wall transition |
| **`GO-05AW3_B.blend`** | `5c3dcbe0…3334` | **AW3-B** projection / curl |
| `GO-05AW3_C1_mask.blend` | `d7ab9730…5cfd` | B + cleanup mask 1 |
| `GO-05AW3_Cw.blend` | `b781da44…69b9` | cleanup pass 1 (working save inside C) |
| `GO-05AW3_C2_mask.blend` | `258d5094…6942` | Cw + L1 shelf mask |
| **`GO-05AW3_C.blend`** | `1d68c9f5e496ce0076318a96220667040b5a4b467dc380d8c49a8e354823cc78` | **AW3-C** cleanup = **candidate** |

`GO-05AW3_nails_final.blend/.glb` was **not** written. `GO-05AV_feet_final` remains the active frozen source; the 05AW2 and 05AW3 candidates await the author.

## 2. Operations

**AW3-A — Mesh Filter Inflate.**
- Strength 0.002, one 51 px drag.
- Mask: a ring outside each plate outline (full weight to 0.3 mm, 1.2 mm ramp), faded out over the distal 22–34 % so the free edge stays crisp.
- Peak 0.385 mm (model 0.380); real / model = 1.012.
- Gate: SI 0, folds 0.

**AW3-B — four Hook modifiers (No Falloff), each with a Plain Axes empty at the origin.**

| Hook group | Direction | Typed empty location |
|---|---|---|
| `AW3_LP` / `AW3_RP` | forward along each foot axis | 1.8 mm |
| `AW3_LD` / `AW3_RD` | down | −1.2 mm Z |

- Weights cover the plate core only:
  - forward: (1 − t)^1.3 over the distal 38 % of the plate;
  - down: (1 − t)^1.2 over the distal 50 %, which gives the curl;
  - lesser toes scaled × 0.8.
- All four were applied, then the empties deleted.
- Read-back vs model: **max 0.00013 mm**.

**AW3-C — cleanup.**
1. **Surface Smooth** (Shape Preservation 0.0, Per Vertex Displacement 0.6), about 10 HC iterations on toe skin near the nails. The nails are excluded, and fold-prone face 1033963 is pinned; simulated safe range 5–12.
2. **Smooth**, about 37 iterations on the L1 front band (shelf line); simulated safe range 15–40.

No topology edit. No remesh or Dyntopo.

## 3. Profile projection per nail (`checks/AW3_projection_per_nail.json`)

| Nail | Forward (mm) | Drop of distal vertex (mm) | Free edge ahead of toe pad, AW2 → AW3 (mm) |
|---|---|---|---|
| L1 | 1.74 | 1.20 | 2.07 → 4.09 |
| L2 | 1.40 | 0.96 | 1.69 → 3.09 |
| L3 | 1.42 | 0.96 | 1.96 → 3.38 |
| L4 | 1.39 | 0.96 | 1.54 → 2.93 |
| R1 | 1.69 | 1.14 | 1.61 → 3.32 |
| R2 | 1.31 | 0.92 | 1.78 → 3.10 |
| R3 | 1.33 | 0.96 | 1.88 → 3.21 |
| R4 | 1.25 | 0.93 | 1.82 → 3.07 |

## 4. Technical gate (AW3-C; `checks/AW3C_final_gate.json`)

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
| Stature | unchanged |
| Lowest moved vertex | 2.62 mm above the floor; no ground intersection |
| Toe contact | none new (SI 0) |
| Foot length vs 05AV | **L +1.25 mm, R +2.43 mm** (limit 3.5) |
| Footprint width | 0.0 (limit 1.0) |
| Heel lift | L −0.009 cm, R 0.0 (limit 0.1 cm) |

The −0.009 cm on L is a measurement shift from the longer foot: no heel vertex moved.

**"Inverted vs source surface" (old coarse reference metric): 11.**
- 8 are inherited from 05AW2.
- The other 3 are tilted faces at the new L2 and L4 free edges (now · local 0.29–0.40, i.e. outward). None is folded.

The AW3-A, AW3-B and C1 gates are all clean as well (`checks/AW3A_gate.json`, `checks/AW3B_gate.json`, `checks/AW3C1_gate.json`).

**Protected regions.** Everything outside the nail supports is 0.000 mm. See `views/AW3_final_whole_body.jpg` and `views/AW3_final_feet_front.jpg`.

## 5. Visual gate (§11)

| Item | Result |
|---|---|
| Crack / chip / split read stays gone | ✓ |
| Nail surfaces smooth | ✓ (minor soft crease above R3 remains) |
| **Side-wall groove / inlay read materially reduced** | **✗**: slightly softer, still reads as an incised outline in 3/4 |
| Nail sits slightly proud of the toe | ✓ front view; partly undercut by the groove read in 3/4 |
| Profile projection visible | ✓ |
| Mild downward curve visible | ✓ |
| Taper reads feline | ✓ |
| No exaggerated hook / talon | ✓ |
| Both feet coherent | ✓ |
| §6 envelope | lesser toes 1.25–1.42 mm vs the 1.5 mm floor |

## 6. Evidence (`reviews/rac-rmot05aw3-evidence/`)

**Views:**
- `views/AW3_vs_AW2_front_top_34.jpg`: front / top / 3-4.
- `views/AW3_vs_AW2_profiles.jpg`: lateral and medial profiles.
- `views/AW3A_sidewall_closeups.jpg`
- `views/AW3_checkpoints_ABC.jpg`
- `views/AW3_final_feet_front.jpg`, `views/AW3_final_whole_body.jpg`

**Checks:**
- `checks/AW3A_gate.json`, `checks/AW3B_gate.json`, `checks/AW3C1_gate.json`, `checks/AW3C_final_gate.json`
- `checks/AW3_projection_per_nail.json`
- `checks/AW3_sidewall_metric.json`
- `checks/AW3_files_and_operations.json`

**Tools:** `tools/rac/w1/rmot05aw3_drivers/`. The gate is unchanged (`rmot05aw2_drivers/aw2gate.py`).

## 7. State

| Item | Status |
|---|---|
| Gorrund BODY COMPOSITION | AUTHOR ACCEPTED / FROZEN |
| Head share; tail root; foot size and heel stance | AUTHOR APPROVED / FROZEN |
| Toenail morphology | **FINAL FINISH — AUTHOR REVIEW REQUIRED**. Candidate `GO-05AW3_C` is technically clean, with real profile projection and curl; open items are the side-wall groove read and lesser-toe projection (−0.1 to −0.25 mm). |
| Active frozen source | `GO-05AV_feet_final` |
| RM-OT-05 | OPEN |
| Stage C Gorrund blocker | BLOCKED (AX3 not run) |
| Grask E3 | FROZEN |
| Connectivity cleanup | CARRIED TO RETOPOLOGY / RIG PREP |
