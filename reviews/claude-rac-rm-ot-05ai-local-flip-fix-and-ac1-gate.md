# RAC RM-OT-05AI — local flip/sliver fix and AC1 rerun: return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05ai-local-flip-fix-and-ac1-order.md` (1318a3c).
**Date:** 2026-10-16.
**Evidence:** `reviews/rac-rmot05ai-evidence/`.

## Outcomes

1. **05AI LOCAL QUALITY PREP PASS / AC1 RETRY AUTHORIZED**
2. **05AI AC1 PASS / READY FOR AC2**

STOP. AC2 was not started.

## Part 1 — local quality prep

### Method

- Source: `GO-05AF_full_sculpt_safe_baseline.blend` (sha verified `6ef02c29…`), processed in Blender 5.2.2 (bpy) in the cloud workspace.
- Tool: `tools/rac/w1/rmot05ai_drivers/ai_local_flip_fix.py`.
- Neighbourhoods: the 2-ring around the 7 listed faces, **202 vertices**.

1. **Diagnosis.** Faces 643992, 686657 and 907533 were pre-existing **micro-crimps**. Each was folded 102–128° against *all three* neighbours, with corners only 0.07–0.52 mm off the local surface. That is why any smoothing flipped them. The four 05AH faces were near-flat and flipped only because of the hard-mask pinning.
2. **Crimp relax.** The 9 corner vertices of the 3 crimp faces got 8 iterations of a half-step uniform-Laplacian relax, capped at **0.5 mm** from the original position.
   - Moved vertices (mm): 51578: 0.50, 51945: 0.50, 51946: 0.50, 164013: 0.35, 165900: 0.40, 165901: 0.50, 186825: 0.19, 189022: 0.50, 189023: 0.50.
   - An earlier variant projected the corners onto a plane instead. It created a needle face, so it was rejected.
3. **Edge rotations.** 45 rotations, only on near-coplanar pairs (fold < 15°). Each needed:
   - a convex quad;
   - a new diagonal not already present;
   - new triangles within 14° of the local plane;
   - an orientation check after the rotation.

   Result: **82 faces changed**, all inside the neighbourhoods. Full lists are in `checks/prep_changes.json`.

### Prep gate (`checks/prep_gates.json`)

| Gate | Result |
|---|---|
| Movement outside the neighbourhoods | **0.000 mm** |
| Max vertex move inside | 0.50 mm |
| Patch nearest-surface deviation | **0.36 mm** new→old / **0.46 mm** old→new (target ≤ 0.5) |
| Folds > 60° in the patch | 9 → **0** (max fold 128.3° → 54.3°) |
| Faces inverted against the old surface | **0** |
| Components / boundary / non-manifold | **1 / 0 / 0** |
| Self-intersections / degenerate / duplicate faces | **0 / 0 / 0** |
| Head / hands / feet / tail / tail junction / genital / perineal | **0.000 mm** |
| Stature / bounding box | unchanged (204.52246 cm) |

### Frozen

- `GO-05AI_local_quality_baseline.blend`, sha256 `eb50d6e48027ce53e2d71d12eacee7ba27c2b96952741e6f1db3cdbf126df5df`.
- `GO-05AI_local_quality_baseline.glb`, sha256 `07f37c1e5d2bb33dbd005ce9e43ae23b6429f9132489dcc287aedac09c89cb04`.
- Location: `E:\…\Gorrund-Neutral-C\05AI\`.

## Part 2 — AC1 rerun (UI only)

### Masks

- Order: arm and hip boxes → **Mask > Smooth Mask** → **hard** head/upper-neck box (edge at about 170.5 cm) → **hard** central hip/tail-junction box. No Smooth Mask after the hard masks.
- **No masks on the seven repaired neighbourhoods**, so there is no pinning; they measured 0.0 before sculpting.
- The saved `.sculpt_mask` was verified before any stroke: head, tail, tail junction, genital, hands, feet and perineal fold all **1.0**.

### Sculpt

- Smooth (0.5): abs, pec split, lower-pec shelf.
- Flatten (0.35): pecs and deltoid fronts (double passes, front view); chest profile and deltoid cap (right view).
- Smooth from the three-quarter view: serratus, flank, lateral abs, lower-pec edge, pec–deltoid groove.
- **No trapezius strokes.**

### Files

- `GO-05AI_AC1.blend`, sha256 `89a19ba2721e80662dc5f09dfa3c0782e975b2e69291bea3439f619391810dae`.
- `GO-05AI_AC1.glb`, sha256 `68d876df38b39bc3f1d1f87cdc1a991d678cdb1da08114f9e1165f9b133f5e36`.

### §6 gate (`checks/ac1_gates.json`)

| Gate | Required | Result |
|---|---|---|
| Topology vs 05AI | identical | **PASS** |
| Opened seams | 0 | **PASS — 0** |
| Self-intersections | 0 | **PASS — 0** |
| Flipped faces | 0 | **PASS — 0** |
| Degenerate faces | 0 | **PASS — 0** |
| Components / boundary / non-manifold | 1 / 0 / 0 | **PASS** |
| Head | 0.000 mm | **PASS — 0.000** |
| Tail / tail junction / genital / hands / feet / perineal | 0.000 mm | **PASS — all 0.000** |
| Stature / bounding box | unchanged | **PASS** (204.5225 cm; extents identical) |
| Moved band | — | z 116.8–170.0 cm; max 12.1 mm, p99 8.1 mm (soft tissue only) |
| Visual | improvement vs 05AF | **yes, moderate**: abs and serratus largely neutralized, central pec split softened, lower-pec shelf reduced; pec projection and deltoid cap moderately reduced; no new creases, shelves or dents (`views/ai_ac1_compare.jpg`, `views/ai_whole_FPB34.jpg`) |

### Visual note for the author

AC1 removes the clearest bodybuilder markers on the trunk: the six-pack, the serratus and the hard pec split. Pec mass and deltoid caps remain broad. Further reduction there could follow in a later pass if Tyler wants a softer chest. The traps were deliberately left unchanged (§3 of 05AH).

## Files on Tyler's PC (`…\Gorrund-Neutral-C\05AI\`)

- `GO-05AI_local_quality_baseline.blend` / `.glb`: frozen prep baseline.
- `GO-05AI_working.blend`: working copy with masks.
- `GO-05AI_AC1.blend` / `.glb`: **passed AC1 checkpoint**.

## Housekeeping

- Blender was closed after export.
- The frozen Blender window and the File Explorer window from this morning remain for Tyler to close.

## State

- AC1 passed.
- Gorrund **UNACCEPTED** until the remaining checkpoints and Tyler's visual review.
- Grask E3 **FROZEN**; RM-OT-05 **OPEN**; Stage C **BLOCKED**.
