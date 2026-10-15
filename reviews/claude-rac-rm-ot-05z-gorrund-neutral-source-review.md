# RAC RM-OT-05Z — Gorrund-Neutral GLB: intake, single-body gate and whole-source review (no repair)

**Order:** `reviews/chatgpt-rac-rm-ot-05z-single-image-regeneration-input-order.md` §6–§7 (with 05Z1).
**Date:** 2026-10-15.
**Evidence:** `reviews/rac-rmot05z-input/intake_gorrund_neutral/`.

## Outcome

| Gate | Result |
|---|---|
| **Single-body gate** | **PASS.** This is the first single-organism, garment-free Gorrund source. |
| **Whole-source review** | **REVISE AT SOURCE: composition only.** |

**What is now right:**
- one closed body, no garment of any kind;
- clean leonine head facing forward, no mane or chin tuft;
- upright stance;
- five-toed plantigrade feet;
- the tail emerges from the lower back.

**What is still wrong.** Rodin turned the soft image back into muscle-plus-fat. The result has:
- defined deltoids, pectorals and biceps / triceps;
- separated quadriceps;
- a soft belly with love handles;
- **greatly enlarged, round gluteals**.

With the head and tail hidden, the body reads as a heavy, muscular human, so composition again carries the size. Reducing that is a whole-body change, not a bounded correction.

**Smaller, genuinely local items:**
- the tail lies fused along the right buttock from its root;
- the root sits slightly right of the midline;
- the heels are about 1 cm (raw) off the ground;
- the feet are large.

Nothing was edited. Gorrund **UNACCEPTED**; Grask E3 **FROZEN**; RM-OT-05 **OPEN**; Stage C **BLOCKED**.

## 1. Provenance and intake

| Item | Value |
|---|---|
| Input image | Candidate 03 (`49b72dfc…`). It passed the image gate. Tyler's chat approval for the Gorrund-Neutral submission was recorded at 12:32. |
| Generation | Run by Tyler on the **Rodin website** (not the PC pipeline), about 12:35. Per Tyler, only this image was used. **There is no pipeline job record.** Tier, quality and settings are **not recorded**; Tyler can supply them. |
| File | Uploaded in chat as `base.glb`. Size **29,777,356 bytes**. SHA-256 **`aaeee37b9d6fa7ca68d9ff87b161d9c2cc2cb6778fe5df9dee2a7f6db52865b5`**. |
| Master | Kept read-only in the session. Placed on E: at `RaceBodies\source\Gorrund-Neutral\` (see §6). It is kept distinct from `base.glb` (`78ecfa87`), `Gorrund.glb` (`1c23b92b`) and `base_1.glb` (`b0214fcf`). The working copy's hash was unchanged after the review. |

## 2. Single-body gate (`geometry/single_body_gate.json`)

**PASS.**
- 1 scene node, 1 mesh instance, 1 primitive, 1,000,000 triangles.
- **1 connected component; 1 body-sized.** No small pieces, no nested shells, no coincident duplicates.
- 0 boundary edges, 0 non-manifold edges.
- World bounds: X −0.520…0.520, Y 0…1.897, Z −0.368…0.372.

## 3. Geometry (read-only; `geometry/inspection.json`)

| Item | Finding |
|---|---|
| Topology | One closed, orientable manifold. The 55,510 split vertices are UV/normal seam duplicates. Euler characteristic −6, so **genus 4**: four small handles, not located in this review (05X's were axillary). |
| Self-intersection | **0 faces** (whole mesh, pymeshlab). |
| Facing / axes | glTF Y-up; the figure faces +Z. A rigid display translation was used only to centre the renders. |
| Height (raw units ×100) | Skull vertex on the midline is **188.7**; the topmost point is an ear at 189.7. Not a stature; no scaling applied. |
| Neck | Minimum section at raw z 168.3. Visible neck. |
| Feet | Five toes with nails, plantigrade (`09`). Length ≈ **40 raw cm ≈ 21 % of height**: large, close to the "oversized feet" caution (GO L238). Toes are slightly bulbous. |
| Heels | Forefoot contact; heel pads **≈ 1.0–1.4 raw cm** above the lowest sole point (a small rigid-pitch item, R-6). |
| Hands | Five digits with nails; hands relaxed (`08`). |
| Tail | One continuous surface. Tube-tracked from the free part to where it **merges with the right buttock surface at raw z ≈ 94** (x ≈ −12, right of the midline). The tail **lies fused along the buttock** from its root down to that point (`05`, diagnostic row). The root is high on the sacral / lumbar region, slightly right of the midline. No ground contact. |
| Groin / pelvis | **Unclothed**; featureless, non-explicit groin; no garment surface or edge. The iliac / hip region, lower abdomen and buttocks are all real body surface. |

**Body-only diagnostic** (`x_tailtrack.py`, `geometry/bodyonly_diagnostic.json`): 81,707 tail faces and the head above z 168.3 were deleted on a disposable copy. All 6 tiles are clean (`geometry/tile_check_bodyonly.json`). The short tail stub remaining in the profile is the fused part, shown deliberately.

## 4. Whole-source gate (05W REVIEW_SPEC Q1–Q4)

| Q | Answer | Evidence |
|---|---|---|
| Q1 Gorrund structural identity at reference composition | **No.** Composition is muscle plus fat: defined deltoid caps and pectorals, separated quadriceps, soft belly with love handles, very large round gluteals. Not reference composition (RA R-4). | `01`, `02`, `04` |
| Q2 Distinct from enlarged human / bodybuilder / ogre with head and tail hidden | **No.** Reads as a heavy, muscular "strongman" human (checklist B1, B3, B4 tendency). **Yes** against Grask; **yes** against ogre (upright, not hunched). | `02`, `10` |
| Q3 Pose, feet, landmarks, continuity | **Mostly yes.** Upright, knees extended, head forward, arms relaxed, five-toed plantigrade feet; pelvic landmarks unobscured. Remaining: a heel lift of about 1 cm; the **tail fused along the right buttock, root slightly off the midline**; large feet. | `01`, `05`, `07`–`09` |
| Q4 Later work can stay local | **No for composition** (whole body). **Yes for the other items** (tail separation and re-rooting; rigid heel pitch). | `02`, `05` |

**Kept separate:**
- **Direction:** clearly the best Gorrund source yet: single body, no garments, clean head.
- **Bounded-correction source:** not yet, because the composition is broad.
- **Final reference:** no.

## 5. Recommendation

**REVISE AT SOURCE: composition only. Keep everything else.**

The image passed with ordinary composition, so the muscle and gluteal mass came from the 3D generator's interpretation. Options are listed below. The choice is the author's; no paid action is authorized here.

1. **Regenerate from the same passing image** (candidate 03) with the website's settings set toward smoother, less detailed geometry, if it offers that, for example a lower-detail or "smooth" option. Record the settings this time.
2. **Make the image softer still,** then regenerate. Keep v3 and add:
   - "small natural buttocks, flat back of thighs";
   - "no defined shoulder or chest muscles";
   - "slim-to-average limbs on a big frame";
   - "tail grows from the exact centre of the lower back and does not touch the buttocks".
3. **Author decision:** treat this composition as an accepted *variant* and look for a different reference-composition source later. Not recommended for an ARM, because R-4 requires reference composition.

If a later source passes Q1 and Q2, the local items become one bounded-correction proposal:
- separating the tail from the buttock, with a midline root;
- a rigid pitch for heel contact;
- checking the feet.

**STOP.** No repair, LOW, blind scoring, scaffold, ARM acceptance or Stage C.
