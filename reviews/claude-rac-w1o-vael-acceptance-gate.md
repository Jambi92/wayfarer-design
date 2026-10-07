# RAC W1o — Vael Final W1 Author-Acceptance Gate (Broad-frame correction)

**Author:** Claude **Date:** October 7, 2026
**Author ruling (October 7, 2026; GitHub Issue #1 final Vael ruling (2026-10-07T16:06Z); reviews/chatgpt-vael-final-acceptance-fenn-w1-order.md):** VAEL W1 ACCEPTED — VAL4 central; breadth-only frames; Broad pelvis X x1.12. Residuals (skin AP-depth diagnostic, arm vs Aelari BM-3, thin margins, Fenn-dependent rows) carried forward. The analysis below is unchanged.
**Order:** `reviews/chatgpt-vael-w1n-author-ruling-w1o-order.md`, the same text as GitHub Issue #1 comment 2026-10-07T15:53Z.
**Basis:** `reviews/claude-rac-w1n-vael-acceptance-gate.md`; VAL4 accepted as the Vael W1 central reference.
**Evidence:** `reviews/rac-w1o-va-evidence/` (`tables.md` holds every number quoted)
**Construction record:** `tools/rac/w1/cfg/w1n/VA.json`

Nothing here is accepted. Specs and `STATUS.md` are untouched.

## Recommendation: PASS — ready for final Vael author acceptance

**The bounded correction (as ordered).** The breadth-only Broad frame keeps its +8 % crest-level breadth. The **pelvis, which carries the hip joints, is widened ×1.12 instead of ×1.08**, so the hip apparatus moves out with the crest.
- **Unchanged:** central VAL4, limb lengths, thoracic depth, joint robusticity, head, tissue, and every accepted comparator.

**Result (tables §1):**

| Body | E-A2 (bitrochanteric ÷ crest ≥ MF, skeletal) | Result |
|---|---|---|
| W1n Broad | 1.1855 vs 1.1992 | FAIL |
| **W1o Broad** | **1.2010 (+0.15 %)** | **PASS** |

- **All other rows on the W1o Broad body:** 8 / 8 skeletal, 14 / 14 directional, 15 / 15 added. Arm < AE stays NOT DEMONSTRATED under BM-3, and the known skin AP-depth diagnostic remains; both are as on the central body.
- **No regression to compact continuity:**

| Body | hip ÷ thorax | waist rise |
|---|---|---|
| Central | 0.964 | 1.094 |
| Narrow | 0.976 | 1.096 |
| **W1o Broad** | **0.978** | **1.108** |
| Fenn | 0.985 | 1.112 |

  The W1o Broad sits beside the Narrow body and below Fenn on both readings. Thoracic depth and the shallow waist interval are untouched, and the trunk crop shows no step-in at the waist (`sheets/va_w1o_broad_trunk_crop.jpg`).

**Why ×1.12 and not wider.** Wider pelvis values give healthier E-A2 margins but push the Broad Vael past Fenn's hip prominence, toward a flared, less compact read. ×1.12 is the smallest tested value that restores E-A2:

| Pelvis X | E-A2 margin | hip ÷ thorax | waist rise |
|---|---|---|---|
| ×1.12 (chosen) | +0.15 % | 0.978 | 1.108 |
| ×1.14 | +0.78 % | 0.991 | 1.115 |
| ×1.16 | +1.40 % | 1.004 | 1.123 |

**The cost is a thin E-A2 margin on Broad (+0.15 %).** E-A2 is a non-strict "not lower than" row, so it passes. The central body's own margin is +0.37 %.

**No accepted canon was challenged.**

## 1. Rows (tables §2–§6)

| Body | Skeletal | Added | Directional | Skin | Not PASS |
|---|---|---|---|---|---|
| VAL4 central (accepted) | 8 / 8 | 15 / 15 | 14 / 14 | 7 / 8 | Arm < AE ND (BM-3); skin AP depth ≥ MF (known diagnostic) |
| W1n Broad (pelvis ×1.08) | 7 / 8 | 15 / 15 | 14 / 14 | 6 / 8 | **E-A2 FAIL** (skeletal and skin); arm < AE ND; skin AP depth |
| **W1o Broad (pelvis ×1.12)** | **8 / 8** | **15 / 15** | **14 / 14** | **7 / 8** | Arm < AE ND (BM-3); skin AP depth (as central) |
| Probes ×1.14 / ×1.16 | 8 / 8 | 15 / 15 | 14 / 14 | 7 / 8 | same as W1o |

Accepted Aelari rows that compare against Vael all pass on the W1o Broad body as well.

## 2. Construction

The W1o Broad frame write, a diagnostic frame construction (not authored Vael frame magnitudes):
- **Widened +8 %:** clavicle Y, spine_01–03 X.
- **Pelvis X ×1.12:** net pelvis [1.1424, 1, 1.03] on VAL4's [1.02, 1, 1.03].
- **Unchanged:** thoracic depth, limb robusticity and lengths.

**Frame principle for later creator work:** a Broad Vael must widen hip-joint spacing at least as much as the crest-level breadth, or E-A2 fails. That is the same mechanism found for Grask.

## 3. Residuals carried forward (non-blocking per the order)

| Item | Status |
|---|---|
| Skin AP depth ≥ MF | −1.4 %, diagnostic only (AD-W1G-12). Skeletal and same-composition rows pass |
| Arm < AE | NOT DEMONSTRATED within 1 %, accepted under BM-3 |
| Thin margins | E-A2 on Broad +0.15 %; central rows 1.06–1.46 % (W1n §6) |
| **Fenn dependency** | Rows against Fenn (leg, torso, AP depth, joints, palms, feet, arm, neck ÷ torso) to be re-checked after Fenn's W1 pass |
| NOT RUN (W2) | VL-02 / VL-03 statures; VL-24; named frame, composition and combined bodies; ears-hidden neutralization row; arm clearance |

## 4. Canon statement

**No accepted canon was challenged.** The correction changes only the diagnostic Broad frame write, inside the ordered limits.

No accepted comparator and no other race was touched. No UE5, topology, rigging, animation, equipment, gameplay or class work was done.

## 5. Recommendation

**PASS.** With the hip apparatus carried with the crest, the Broad Vael frame passes every row, and its compact continuity sits within the Vael frame range.

**For the author:** final Vael W1 acceptance (VAL4 central; breadth-only frames with hip-joint spacing following the crest).

Fenn is not started.

STOP.

— Claude
