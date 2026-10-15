# RAC RM-OT-05Z2 — Gorrund-Neutral-B GLB: intake, single-body gate, whole-source review and body-only comparison (no repair)

**Order:** `reviews/chatgpt-rac-rm-ot-05z2-gorrund-source-composition-correction-order.md` §6–§8.
**Date:** 2026-10-15.
**Evidence:** `reviews/rac-rmot05z-input/intake_gorrund_neutral_b/`.

## Outcome

| Gate | Result |
|---|---|
| **Single-body gate** | **PASS** |
| **Whole-source review** | **Q1 NO, Q2 NO → REVISE AT SOURCE (composition).** |
| **Body-only comparison vs `aaeee37b…`** | **Less fat, more muscle.** Not closer to the reference composition. |

**What changed.** Against `Gorrund-Neutral` (`aaeee37b…`), the belly and soft tissue went down: body-only depth is −5.4 raw cm at the waist and −2.9 at the hips and thighs. Muscle definition went **up**:
- shredded abdominals and serratus;
- separated pectorals with deltoid caps;
- corded forearms;
- separated quadriceps.

With the head and tail hidden, the body reads as a lean bodybuilder or strongman human. The 3D generator re-imposed heroic musculature for the second time, from a softer image (candidate 06) than before.

**What stayed the same.**
- The gluteals are still large and round.
- The tail still lies on the right buttock from a root right of the midline.
- The heels are still about 1 raw cm up.
- The feet are still large.

Nothing was edited. Gorrund **UNACCEPTED**; Grask E3 **FROZEN**; RM-OT-05 **OPEN**; Stage C **BLOCKED**.

## 1. Provenance and intake

| Item | Value |
|---|---|
| Input image | Presumed **candidate 06** (`83042148…`, gate PASS; job prep AssetName `Gorrund-Neutral-B`). Tyler's message was "latest GLB file- Male Gorrund"; the image used is **not confirmed**. |
| Paid-generation record | **Gap (05Z2 §6).** There was no chat approval naming the image, the AssetName and the tier/settings before generation. The website tier, quality, detail and smoothing settings are **not recorded**; Tyler can supply them. Recorded as a process gap. It does not change the geometry findings. |
| File | Uploaded in chat as `base.glb`. Size **29,640,940 bytes**. SHA-256 **`895d8854f67831d901297f684911f34cdf6ed28d45170e7226330c1f5e6d290e`**. |
| Master | Kept read-only in the session and placed on E: at `RaceBodies\source\Gorrund-Neutral-B\Gorrund-Neutral-B.glb`. It is distinct from `78ecfa87`, `1c23b92b`, `b0214fcf` and `aaeee37b`. The working copy's hash was unchanged after the review. |

## 2. Single-body gate (`geometry/single_body_gate.json`)

**PASS:** 1 scene node, 1 mesh instance, 1 primitive, 1,000,000 triangles, and one body-sized connected component. There are no small pieces, no nested shells and no coincident duplicates.

## 3. Geometry (read-only; `geometry/inspection.json`, `feet.json`, `bodyonly_sections_A_vs_B.json`)

| Item | Finding |
|---|---|
| Topology | One closed manifold. Euler characteristic −2, so **genus 2**. **0** self-intersecting faces (whole mesh, pymeshlab). |
| Height (raw ×100) | **189.8.** Not a stature; no scaling applied. |
| Head | Clean leonine head facing forward, no mane, no chin tuft, visible neck (`03`). |
| Hands | Five digits; relaxed (`08`). |
| Feet | Five toes, plantigrade (`09`). Length **42.0 / 41.1 raw cm ≈ 22 % of height**: large, slightly larger than A's 21 %. |
| Heels | Heel pads **1.29 / 0.96 raw cm** above the sole minimum (forefoot contact), the same as A. |
| Tail | One continuous surface. Tube-tracked from the free part to where it **merges with the body at raw (x −11.1, z 94.7)**. The root emerges right of the midline, and the tail **lies along the right buttock** before leaving it (`05`). Practically identical to A (−12.3, 93.6). The image's "tail clears the buttocks" wording did not carry through. |
| Groin / pelvis | Unclothed and featureless. Real body surface throughout. |
| Body-only diagnostic | Made with `x_tailtrack.py` (seed 0.40·H, PMAX 40): 73,010 tail faces deleted, plus everything above the neck section at z 162.4, on a disposable copy. The 4 whole-body tiles are clean (`geometry/tile_check_bodyonly.json`). The tail-root crop tiles are excluded from that check because cropping cuts the arm and hand silhouettes into separate islands. |

### Body-only sections, A (`aaeee37b`) vs B (`895d8854`), raw cm

Widths at z 135, 110 and 90 include the hanging arms, so only the depths are compared there.

| Level | Depth A | Depth B | Change |
|---|---|---|---|
| Chest z 135 | 40.6 | 40.0 | −0.6 |
| Waist z 110 | 41.0 | 35.6 | **−5.4** |
| Hip / gluteal z 90 | 37.8 | 34.9 | −2.9 |
| Thigh z 70 (one leg) | 29.3 | 26.4 | −2.9 |
| Calf z 35 (one leg) | 19.7 | 19.5 | −0.2 |

Thigh width is 32.5 vs 32.0 and calf width 19.8 vs 20.2. **The limbs are not slimmer**; only the trunk depth fell.

## 4. Whole-source gate (05W REVIEW_SPEC Q1–Q4)

| Q | Answer | Evidence |
|---|---|---|
| Q1: Gorrund structural identity at reference composition | **No.** Composition is lean and heavily muscled: abdominal and serratus separation, pectoral separation, deltoid caps, corded forearms, quadriceps separation, large round gluteals. Not reference composition (RA R-4). | `01`, `02`, `06` |
| Q2: Distinct from an enlarged human / bodybuilder with head and tail hidden | **No.** Reads as a bodybuilder or strongman human (checklist B1, B3). Yes against Grask; yes against ogre. | `02`, `06`, `10` |
| Q3: Pose, feet, landmarks, continuity | **Mostly yes.** Upright, head forward, arms relaxed, five-toed plantigrade feet. Remaining: heel lift of about 1 raw cm; tail lying on the right buttock with its root right of the midline; large feet. | `01`, `05`, `09` |
| Q4: Later work can stay local | **No for composition** (whole body). **Yes for the other items.** | `02`, `05` |

**05Z2 §7 success criteria (Q1 = YES and Q2 = YES): not met.** The tail-root, heel and feet items therefore stay unconverted.

## 5. What this second result shows

Two passing images now exist:
- candidate 03, ordinary composition;
- candidate 06, softer still.

Each produced a GLB with heroic anatomy. A gives muscle plus fat; B gives lean, defined muscle. The tail position and the gluteals are nearly identical in both, even though the image direction changed. The generator seems to apply its own body prior for large male figures, so further softening of the image alone is unlikely to reach Q1 and Q2. That is an inference from n = 2, not a proven cause.

Options, for the author to decide. None is authorized here, and each paid step needs its own approval naming the image, AssetName and settings:

1. **Record and change the generation settings.** Tyler supplies the website tier and settings used for A and B. A single regeneration then uses a lower-detail or smooth surface option, if one is offered.
2. **Change the input type rather than the wording.** For example, use a smooth, unshaded, "clay-mannequin" style image in which no muscle-shading cues exist for the generator to amplify, or use a multi-view input if the website offers one. This needs a new image round through the 05Z gate.
3. **Re-scope the source route.** Accept that this generator will not give reference composition, and decide at order level whether composition is reached some other way. This is an order-level decision; nothing here proposes sculpting.

**STOP.** No repair, LOW, blind scoring, scaffold, ARM acceptance or Stage C.

## 6. Evidence index (`reviews/rac-rmot05z-input/intake_gorrund_neutral_b/`)

**Views:**
- `01_whole_untouched`
- `02_bodyonly_diagnostic`
- `03_close_head_neck_girdle`
- `04_close_chest_back`
- `05_close_pelvis_tailroot`
- `06_bodyonly_A_vs_B` (same raw scale)
- `07_close_knee_ankle`
- `08_close_hands`
- `09_close_feet`
- `10_matched_height_vs_controls` (MF/SK/GR-E3 frozen controls, A, B)

**Geometry:**
- `single_body_gate.json`
- `inspection.json`
- `bodyonly_diagnostic.json`
- `tile_check_bodyonly.json`
- `feet.json`
- `bodyonly_sections_A_vs_B.json`

Close-up framing reuses A's centres so the comparison is direct.
