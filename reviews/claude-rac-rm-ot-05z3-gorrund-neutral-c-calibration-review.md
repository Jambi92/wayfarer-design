# RAC RM-OT-05Z3 — Gorrund-Neutral-C calibration GLB review: RODIN GORRUND ARM ROUTE RETIRED — HEROIC BODY PRIOR PERSISTS

**Order:** `reviews/chatgpt-rac-rm-ot-05z3-counterbiased-rodin-calibration-order.md` §7–§9.
**Date:** 2026-10-15.
**Evidence:** `reviews/rac-rmot05z-input/intake_gorrund_neutral_c/`.

## Outcome

| Item | Result |
|---|---|
| `Gorrund_Neutral.glb` (`513bc9e2…`), the calibration GLB | Single-body gate **PASS**. **Q1 NO, Q2 NO.** It is not less heroic than B, so it **fails the 05Z3 §8 calibration rule**. |
| `6-8-9.glb` (`a66b024c…`), a second upload | Single-body gate **FAIL**: three body-sized figures in one mesh. Recorded only; not reviewed and not extracted. |
| **Route outcome (05Z3 §8)** | **RODIN GORRUND ARM ROUTE RETIRED — HEROIC BODY PRIOR PERSISTS.** No fourth paid Rodin composition retry. |

The input was deliberately under-muscled (candidate 09: a flat mannequin chest, sloping shoulders, slim limbs, matte low-contrast clay). Rodin still produced a heroic physique:
- separated abdominals and serratus;
- pectoral separation and deltoid caps;
- corded, veined forearms;
- separated quadriceps and gastrocnemius;
- love handles;
- large round gluteals.

This is the third single-figure Gorrund GLB in a row to do so (A, B, C) from progressively softer inputs (candidates 03, 06, 09).

Nothing was edited. Gorrund **UNACCEPTED**; Grask E3 **FROZEN**; RM-OT-05 **OPEN**; Stage C **BLOCKED**.

## 1. Provenance and intake

| Item | `Gorrund_Neutral.glb` (C) | `6-8-9.glb` |
|---|---|---|
| Size | 29,805,740 bytes | 30,662,540 bytes |
| SHA-256 | `513bc9e2c5c4ba1da0a5a33661f230181bf18a24c50e0af0d49acdf5521dccf6` | `a66b024c8325b7eb2237f6ce937d7c961320e0ee058d66c53d6a9ac6403a79c8` |
| Presumed input | Candidate 09 (`34169ee8…`), single image | Candidates 06, 08 and 09 as a multi-image input (inferred from the filename) |
| Master on E: | `RaceBodies\source\Gorrund-Neutral-C\Gorrund_Neutral.glb` | `RaceBodies\source\Gorrund-6-8-9-multiview\` (2 parts plus `REJOIN.txt`) |

Both files were uploaded in chat at 16:39 with no message. They are kept distinct from `78ecfa87`, `1c23b92b`, `b0214fcf`, `aaeee37b` and `895d8854`. The working copies were unchanged after the review.

### Process deviations (recorded, not judged)

- **No approval in chat** named the image, the AssetName and the settings before generation (05Z3 §7).
- **Rodin website settings not recorded.** `RODIN_SETTINGS_RECORD_05Z3.md` is still empty.
- **Two generations arrived** where 05Z3 allowed one.
- **Inputs are presumed**, not confirmed by Tyler.

These do not change the geometry findings. The route outcome is decided on C, the single-figure calibration result.

## 2. Single-body gates

- **C** (`geometry/single_body_gate.json`): **PASS.** 1 node, 1 instance, 1 primitive, 1,000,000 triangles, 1 body-sized component, 0 boundary and 0 non-manifold edges.
- **6-8-9** (`multi_view_6-8-9/single_body_gate.json`): **FAIL.** Three body-sized components, each about 0.94 m tall, placed side by side at x ≈ −0.68, 0 and +0.69.
  - Per 05Z1 / 05Y rules, no figure is extracted or reviewed.
  - `whole_file_record.jpg` is kept as a record only. It shows the same defined abdominal and limb musculature on all three figures.

## 3. Geometry of C (read-only)

| Item | Finding |
|---|---|
| Topology | One closed manifold; Euler characteristic −4, so **genus 3**. **0** self-intersecting faces. |
| Height (raw ×100) | **189.8.** Not a stature. |
| Head | Clean leonine head facing forward, no mane or chin tuft, visible neck (`03`). |
| Hands / feet | Five digits each; plantigrade feet (`08`, `09`). |
| Foot length | 39.4 / 38.7 raw cm ≈ **20.6 % of height**: slightly smaller than A and B. |
| Heels | **0.87 / 1.57 raw cm** above the sole minimum (`feet.json`), the same pattern as A and B. |
| Tail | Root **close to the midline** (merge at x −4.5, z 93.4; A and B were at about x −11 to −12). This is an improvement. The tail still **runs straight down inside the gluteal cleft, fused to both buttocks**, before leaving the body (`05`), so it **does not clear the buttocks**. |
| Body-only diagnostic | `x_tailtrack.py`: 106,850 tail faces and everything above the neck section at z 168.3 deleted on a disposable copy. 4 whole-body tiles clean (`tile_check_bodyonly.json`). |

### Body-only sections in raw cm (`bodyonly_sections_A_B_C.json`)

Depths are front-to-back. Widths at z 135, 110 and 90 include the arms, so only depths are compared at those levels.

| Level | A | B | C |
|---|---|---|---|
| Chest depth, z 135 | 40.6 | 40.0 | 38.4 |
| Waist depth, z 110 | 41.0 | 35.6 | 33.4 |
| Hip / gluteal depth, z 90 | 37.8 | 34.9 | 34.8 |
| Thigh width × depth, z 70 | 32.5 × 29.3 | 32.0 × 26.4 | **29.5 × 25.4** |
| Calf width × depth, z 35 | 19.8 × 19.7 | 20.2 × 19.5 | 19.8 × 18.6 |

C is **slightly slimmer** than B in volume: thigh −2.5 cm wide, waist −2.2 cm deep. Its **muscle definition is at least as heroic** (`06`): the same abdominal, pectoral and deltoid separation, quadriceps teardrops and calf bellies. The gluteals are as large and round as in A and B.

## 4. Whole-source gate (05W REVIEW_SPEC Q1–Q4) and 05Z3 §8

| Check | Result | Evidence |
|---|---|---|
| Q1: structural identity at reference composition | **NO.** Heroic, defined musculature plus love handles and large gluteals. | `01`, `02`, `06` |
| Q2: not an enlarged human / bodybuilder with head and tail hidden | **NO.** Reads as a bodybuilder human. | `02`, `06`, `10` |
| Q3: pose, feet, landmarks | **Mostly yes.** Remaining issues: tail fused in the gluteal cleft; heel lift of about 1–1.6 cm. | `01`, `05`, `09` |
| Q4: local follow-up possible | **No** for composition. | — |
| Less heroic muscle than B | **NO.** Slightly less volume; definition is not lower. | `06` |
| No obesity compensation | Yes. Love handles are present but no belly. | `05` |

**Calibration rule: FAIL** because of heroic musculature.

## 5. Ruling

**RODIN GORRUND ARM ROUTE RETIRED — HEROIC BODY PRIOR PERSISTS.**

Across three single-figure generations, Rodin output stayed heroic regardless of input composition:
- **A:** muscle plus fat;
- **B:** lean, defined;
- **C:** lean, defined, from a deliberately under-muscled mannequin image.

The multi-image `6-8-9` attempt also produced three figures in one mesh, all heroic.

Preserve as failed-source evidence, unchanged:
- A (`aaeee37b…`);
- B (`895d8854…`);
- C (`513bc9e2…`);
- 6-8-9 (`a66b024c…`).

**Do not** sculpt, repair, merge, average or promote any of them.

**Returns for an alternate-source decision (order level).** The tail root is now near the midline, and the head, hands, feet and pose are consistently correct. Those facts may inform that decision. No alternate is proposed or started here.

**STOP.** No further Rodin generation, LOW, blind scoring, scaffold, D4, UE5, rigging, creator work or Stage C.

## 6. Evidence index (`reviews/rac-rmot05z-input/intake_gorrund_neutral_c/`)

**Views:**
- `01_whole_untouched`, `02_bodyonly_diagnostic`;
- close-ups `03`, `04`, `05`, `07`, `08`, `09`;
- `06_bodyonly_A_B_C` (same raw scale);
- `10_matched_height_vs_controls`.

**Geometry:**
- `single_body_gate.json`, `inspection.json`;
- `bodyonly_diagnostic.json`, `tile_check_bodyonly.json`;
- `feet.json`, `bodyonly_sections_A_B_C.json`.

**`multi_view_6-8-9/`:** `single_body_gate.json`, `whole_file_record.jpg`.
