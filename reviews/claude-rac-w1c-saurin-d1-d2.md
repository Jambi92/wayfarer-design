# RAC W1 Continuation — Saurin D-1 Conversion Record and D-2 Measurement Copy

**Author:** Claude **Date:** October 5, 2026
**Order:** `reviews/chatgpt-rac-wave1-continuation-asset-build-order.md` §2 (D-1), §3 (D-2), §4 (D-3), §7 item 15
**Status:** D-1 **RECORDED**. D-2 measurement copy **NOT PRODUCED** (attempt 1 failed its invariance check; see §2). SA-M and SA-F are author-accepted W1 ARMs.

## 1. D-1 — rostral-index conversion on the accepted anatomy

The Part 7 convention stays canonical for the Saurin 0.288 reference, the 0.255–0.335 band and the provisional 0.255 floor. r3 FPI is the common-framework diagnostic. FAL stays at the anterior biological facial surface of the current base anatomy (rostral tip). The Part 7 floor was not rewritten.

Measured on SA-M (sha256 `a925e067…8b8c9c`). Raw data: `reviews/rac-w1-evidence/saurin_w1.json`, `saurin_part7_convention.json`, `saurin_coupled_corner.json`.

| Case | Head length HL (cm) | Part 7 index | r3 FPI | r3 − Part 7 | Difference × HL (cm) |
|---|---|---|---|---|---|
| Male centre (reference) | 31.871 | 0.2879 | 0.3254 | 0.0375 | 1.194 |
| Rostrum −15 % | 30.648 | 0.2595 | 0.2985 | 0.0390 | 1.194 |
| Cranium +8 % | 33.241 | 0.2761 | 0.3120 | 0.0359 | 1.194 |
| Uncoupled corner | 32.018 | 0.2484 | 0.2857 | 0.0373 | 1.194 |
| Rostrum +20 % | 33.502 | 0.3226 | 0.3582 | 0.0356 | 1.194 |
| Coupled corner at the Part 7 floor (rostrum factor 0.8847, cranium +8 %) | — | 0.2550 | 0.2920 | 0.0370 | — |

**Conversion relationship (measured, this anatomy):** r3 FPI = Part 7 index + 1.194 cm ÷ HL.
- The constant 1.194 cm is the f-distance between the Part 7 corneal-surface proxy point and the r3 eyeball centre. It does not change with rostrum or cranium length, because the corners change neither the eyes nor their position relative to the cranium.
- The conversion is valid only while the eye geometry is the accepted reference eye. It is not a canon re-expression of the floor; that needs a later author order (D-1).
- Reporting rule from now on: where Saurin is involved, both values are given. RM-CF-05 will compare populations in r3.

## 2. D-2 — measurement-only re-posed copy: attempt 1

**Requirement:** keep the vertex identity, topology and every anatomical dimension; change only the articulated pose that R-6 bilateral comparability needs; keep the tail geometry and the tail-base relationship; record the transform provenance. Verify with invariant local segment lengths, region dimensions and volume.

**Problem:** the frozen SA-M mesh (1,124,235 vertices) has **no skeleton, joint centres or skin weights**.
- The repository and the PC copy hold only the `v` and `f` arrays.
- The working labels (`Lbase.pkl`) give region masks and horizontal-section centrelines, not joints.

**Method tried** (`tools/rac/w1/saurin_d2_copy.py`, `saurin_d2_check.py`):
1. Estimate the hip/knee/ankle and shoulder/elbow/wrist centres from line fits through horizontal-section centroids.
2. Rotate each segment about its proximal joint to the mirror-mean posture.
3. Blend over 8–10 cm bands at each joint.
4. Keep the foot orientation, so the sole stays in plantigrade contact.

**Result: FAILED the invariance check.** Values are from `reviews/rac-w1c-evidence/saurin_d2_check.json`.

| Check | Before | After | Verdict |
|---|---|---|---|
| Stature (cm) | 187.88 | 189.46 | **Changed +1.58**. Re-grounding lifted the whole body: the moved feet rose |
| Volume (L) | 136.94 | 137.20 | +0.19 % |
| Left thigh / left lower leg (joint-to-joint, cm) | 38.72 / 39.04 | 35.82 / 42.92 | **Not invariant** |
| Right thigh / right lower leg (cm) | 46.55 / 34.19 | 44.65 / 34.28 | **Not invariant**; left and right also disagree before the re-pose |
| Left upper arm / forearm (cm) | 12.47 / 51.96 | 14.62 / 50.05 | **Joint estimate invalid** (an upper arm of 12 cm is not anatomy) |
| Leg mirror-distance median (cm) | 1.968 | 1.735 | Small improvement only |
| Arm mirror-distance median (cm) | 1.351 | 1.422 | Worse |

**Diagnosis:** the joint centres are not identifiable from section centroids on this body.
- Horizontal sections cut the oblique limbs at different angles on each side.
- The hands sit beside the thighs.
- The proximal joints were fixed at a common height.

So the "segment lengths" differ between sides **before** any re-pose: by 7.8 cm for the thigh and about 19.6 cm / 19.3 cm for the upper arm / forearm. The copy cannot be verified. Per D-2 the copy is **not used**. No Saurin bilateral limb or segment reading was taken from it.

**What unblocks it:** one of the following.
- **(a)** A joint-centre set for SA-M: hip, knee, ankle, shoulder, elbow and wrist per side, placed anatomically. Recording it is a builder act, and it is **identity-relevant** because Saurin limb segmentation is not in canon, so it needs author acceptance.
- **(b)** The closure build's rig correspondence, if it still exists anywhere. It was not found in the repository or on the PC.

With either one, the same tool re-runs with fixed joints, and the invariance table becomes a clean test.

**Saurin items that stay blocked:**
- RM-UB-01 (SA) limb/segment shares;
- RM-UB-04 basis.

Head, torso, pelvis and tail readings from the frozen body stand.

— Claude
