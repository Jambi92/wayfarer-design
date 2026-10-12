# RAC RM-OT-05J — Gorrund S4 structural articulation and Stage C gate

Order: `reviews/chatgpt-rac-rm-ot-05j-gorrund-structural-articulation-order.md` (b4a0d79). Sculptor: Claude, working by hand in desktop Blender 5.2.2 LTS on Windows. Date: 2026-10-12.

Evidence: `reviews/rac-rmot05j-evidence/`. Hashes are in `SHA256SUMS.txt`.

## Gate lines

| Line | Status |
|---|---|
| 05I protection overlay | **ACCEPTED** (applied unchanged; `NO_TOUCH_hands_digits_guard05i` honoured) |
| Final sculpt revision | **S4** (no S5; see §6) |
| Canon-form audit | **FAIL** (Q1, Q2, Q5, Q11, Q14 = YES; Q15, Q16 = NO) |
| Distributed structural-cue audit | **FAIL** (only 1 family CLEAR in low; §18 needs ≥ 4) |
| Reference structural read | **FAIL** (2 CLEAR, 4 MARGINAL) |
| Low-composition structural read | **FAIL** (1 CLEAR, 5 MARGINAL) |
| Narrow structural read | **FAIL** (2 CLEAR, 4 MARGINAL) |
| Broad structural read | **FAIL** (1 CLEAR, 5 MARGINAL) |
| Exporter | **PASS** |
| Preflight | **PASS** (05I overlay package) |
| 05F re-entry | **PASS** |
| Replicated blind gate | **NOT RUN.** §18 bars blind entry. This is not a pass. |
| Blind-reason canon audit | **NOT RUN** (no blind data) |
| Gorrund structural readability | **REJECT** |
| Grask E3 Stage C | **NOT RUN** (E3 frozen, untouched) |
| Gorrund Stage C | **NOT RUN** |
| Combined Stage C | **NOT RUN** |
| RM-OT-05 | **OPEN** |
| Canon promotion | **NOT PERFORMED** |
| D4 | **NOT STARTED** |
| UE5 | **NOT STARTED** |

**Design-level blocker reported (order §4, §21).** After a six-family structural pass inside the accepted route, the global box-vs-fat failure persists:
- In the reference and Narrow states, the trunk still reads as a rectangular block.
- In the authoritative low state, it reads as a deep chest over a soft abdomen.

Structural cues that can be legally sculpted (about 0.5–6 cm of surface relief) do not survive into low composition strongly enough to carry identity. The reasons are in §5.

## 1. Final artifacts

| Artifact | SHA-256 |
|---|---|
| `S4/GO_sculpt_S4_r6.obj` | `04d258431a55a484249b116a438e905cbc625dd4c860e7dddb864cce48fc9244` |
| `S4/GO_sculpt_S4_r6_export_report.json` | `06a70cb226d8c88b9e65be5c4c8211ea4d40f30e82a8c1a52ca7a0ebb45c85ad` |
| `S4/GO_sculpt_S4_preflight.txt` | `3a75ff491abcf4d8e3d82c5bddc22e6b7a02b0d52df5330ae77f0fbe49adf42d` |
| Working blend at S4 (stays on the author PC, `sculpt/S1/backups/GO_sculpt_S1_work_28.blend`) | `9b152fe862f0586f75c6c0f03005729e3e53f031d0b238944b3c811d1822dbeb` |

**Base:**
- S3 (`753355ce…bf7d`);
- 13380 vertices;
- topology unchanged.

**Moves:**
- 3223 vertices moved.
- Per-family max displacement (cm): A 6.38, B 6.03, C 4.22, D 3.74, E 2.22, F 5.54.

**Operations:** all were made per side, by hand, with translate or partial flatten under proportional falloff. There was:
- no scaling of limbs or segments;
- no repose;
- no remesh;
- no skeleton or proportion change.

| Family | Operations |
|---|---|
| A axial/costal | Sternal strip +0.4. Upper abdomen recessed −1.3 so the costal margin overhangs. |
| B posterior | Paraspinal columns lowered −0.5 y. Interscapular plane flattened. Sacral plate flattened. |
| C pelvis→femur | Trochanteric lateral plane flattened in two passes. Trochanteric step +0.4. |
| D knee/ankle | Femoral condyles widened. Knee side planes and patellar front flattened. Tibial plateau step added. Anterior shank and calf belly flattened. Malleoli offset (lateral out, medial in). |
| E elbow/forearm/wrist | Olecranon set back. Lateral epicondyle raised. Forearm AP flattened. |
| F girdle/neck root | Clavicle line brought forward. Neck-base lateral widening. |

**Floor fixes** (local outward pushes, needed to keep the authoritative low state above the floor):
- knee-front verts 4624/4632/11242/11250;
- forearm verts 3514/10182.

## 2. Canon-form audit (§15)

The audit uses matched reference and low close views: `audit/S4_family_close_views.jpg`, `audit/S4_low_state.jpg` and `audit/S4_cue_persistence_sheet.jpg`.

| # | Question | Answer |
|---|---|---|
| 1 | Rectangular trunk? | **YES.** The front silhouette from shoulder to hip is still a near-parallel block (route widths). |
| 2 | Boxy trunk? | **YES.** The front and three-quarter views read as a block of ribcage. |
| 3 | Slab-sided trunk? | NO |
| 4 | Cylindrical / barrel torso? | NO |
| 5 | Belly / chest bulk carrying the read? | **YES (low).** Chest depth in profile is the dominant low read. |
| 6 | Armor-like costal/sternal forms? | NO |
| 7 | Monster-like joints? | NO |
| 8 | Girdle overhang? | NO |
| 9 | Trapezius bulk as identity? | NO |
| 10 | Pelvic outrigging? | NO |
| 11 | Uniform pillar shanks? | **YES (low / Broad).** The shank flattening and malleolar offsets are absorbed. |
| 12 | Grask calf / forearm cues? | NO |
| 13 | Human pectoral shelf still dominant? | NO |
| 14 | Navel/nipple relief still controlling the low read? | **YES (partial).** The navel and soft upper abdomen are the most legible front-of-trunk relief in low. |
| 15 | ≥ 4 distributed cue families clearly readable? | **NO** (2 in reference) |
| 16 | Same cues survive low composition? | **NO** (1) |
| 17 | Posterior load path legible? | YES |
| 18 | Joint structure legible without knobs? | YES (knee, elbow) |
| 19 | Thorax→pelvis continuity valid? | YES |
| 20 | Upright plantigrade humanoid? | YES |

**Result: FAIL.** The order says to keep sculpting when the audit fails. I exported and ran preflight and re-entry anyway. Those runs were diagnostics, to confirm the geometry is legal and to see whether it survives low composition. They do not override this audit.

## 3. Distributed structural-cue disposition by state (§18)

| Family | Reference | Low (authoritative) | Narrow | Broad |
|---|---|---|---|---|
| A axial/costal | MARGINAL | MARGINAL | MARGINAL | MARGINAL |
| B posterior sacral load path | **CLEAR** | **CLEAR** | **CLEAR** | **CLEAR** |
| C pelvis→proximal femur | MARGINAL | MARGINAL | MARGINAL | MARGINAL |
| D knee/ankle | **CLEAR** (knee) / MARGINAL (ankle) | MARGINAL | **CLEAR** (knee) | MARGINAL |
| E elbow/forearm/wrist | MARGINAL (olecranon clear in profile only) | MARGINAL | MARGINAL | MARGINAL |
| F girdle/neck root | MARGINAL | MARGINAL | MARGINAL | MARGINAL |
| **CLEAR count** | 2 | **1** | 2 | 1 |

No family is LOST in any state. §18 requires at least four CLEAR families in low, and S4 has one. **Blind testing is therefore not permitted, and it was not run.**

The 05F re-entry retention figures (median / p10 vs the sculpt delta) agree with the visual read: the transport mostly keeps the cues. The problem is that the cues are too low-contrast to read once the low body shape is applied.

| Family | Reference | Low |
|---|---|---|
| A | 0.94 / 0.79 | 0.93 / 0.71 |
| B | 1.00 / 0.80 | 1.00 / 0.82 |
| C | 0.87 / 0.69 | 0.85 / 0.70 |
| D | 0.83 / 0.62 | 0.83 / 0.64 |
| E | 1.00 / 1.00 | 0.99 / 0.90 |
| F | 1.00 / 1.00 | 1.01 / 0.93 |

## 4. Export / preflight / re-entry / symmetry

**Exporter and preflight:** PASS, against the 05I overlay package (`regions_05i.json`, sha `f5ef813f…113f35`).

**05F re-entry S4:** PASS. I1–I6 pass, and every guard passes in all four states.
- Volume ratio ≈ 0.9999998.
- Reproduction p90 is 0.235 and max is 0.407.

| State | Piercing edges (S4 vs route) | Arm–trunk gap (cm) |
|---|---|---|
| Reference | 73 vs 67 | 0.60 |
| Low | 74 vs 78 | 0.77 |
| Narrow | 61 vs 57 | 0.84 |
| Broad | 57 vs 53 | 0.87 |

Files: `reentry/`.

**L/R audit** (`symmetry/lr_S4.json`), asymmetry p90 / max (cm):

| A | B | C | D | E | F |
|---|---|---|---|---|---|
| 0.88 / 2.67 | 0.79 / 1.85 | 1.24 / 2.67 | 0.08 / 0.53 | 0.00 / 0.22 | 0.23 / 1.10 |

The A and C maxima come from local floor fixes. The asymmetry inherited from the template is up to 1.16 cm.

**Advisory note:** the advisory preview low (not authoritative) flags 23 floor-inside vertices (17 introduced by the sculpt). The authoritative low passes the floor check.

## 5. Blocker analysis

The S3, S4 and S2 evidence together point to one global cause, not a weak family. Three reasons:

1. **The route fixes the trunk silhouette.** The trunk's front width profile, from shoulder to waist to hip, is a near-parallel column set by the route's proportions. The order forbids changing them. Surface articulation inside that column cannot remove the "rectangular / boxy" read (Q1/Q2). Pushing depth instead (S3 and S4 Family A) produces the "obese / chest-belly" read (Q5/Q14).
2. **Low composition compresses fine relief.** The cues that are legal under §4 are ≤ 1.5 cm local planes and steps. In the authoritative low state, the low-frequency fat layer dominates them. Re-entry shows they are transported (retention ≥ 0.83 median), but their visual contrast falls to MARGINAL everywhere except the posterior paraspinal columns.
3. **More of the same would be micro-tuning.** Five of six families are MARGINAL in low. Under §21, S5 is for one or two weak families. Spending it on deeper relief would be the micro-tuning the order rules out. Larger relief would also breach Q6/Q7 (armor or knob joints).

**Author decision needed.** One of these, at the design level:
- **(a) Trunk silhouette:** permit a bounded change to the trunk's width profile (waist and costal flare), i.e. a skeleton/proportion change. The order currently forbids this.
- **(b) Low composition:** revise how the low body shape is built so it doesn't flatten structural relief (a different low-state authority).
- **(c) Canon target:** accept that within the current route, Gorrund cannot be told apart by trunk structure alone, and move identity weight to other canon channels.

I have not taken any of these.

## 6. Scorer rationale summary

There is none for S4: no blind run is permitted. The S3 baseline (05I) is the latest blind evidence:
- **Run 1** read the reference as an obese human.
- **Run 2** based its C votes on a "boxy rectangular" trunk.

S4 is meant to move away from both reads, but the cue audit shows it does not do so strongly enough to justify a blind run.

## 7. Every fail / marginal / blocker

- **Canon audit FAIL:** Q1, Q2, Q5 (low), Q11 (low/Broad), Q14 (partial) = YES; Q15, Q16 = NO.
- **Cue audit FAIL:** low has 1 CLEAR (B). A, C, D, E and F are MARGINAL.
- **Blind gate:** NOT RUN (§18).
- **Readability:** REJECT.
- **Design-level blocker:** as in §5.
- **Advisory preview low:** 23 floor-inside vertices. This is advisory only; the authoritative low passes.

## 8. Confirmation

The following did **not** change:
- skeleton, proportions, rig, route or topology;
- the re-entry validator, guards or thresholds;
- the 05I protection overlay (used as is);
- the scorer prompt (`f_scorer_prompt.md`) and tally rule (`f_tally.py`);
- canon rules;
- Grask E3.

Stopped at the RM-OT-05J author gate.
