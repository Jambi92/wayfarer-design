# RAC RM-OT-05U8A: controlled crease-anchor release gate

**Order:** `reviews/chatgpt-rac-rm-ot-05u8a-controlled-crease-anchor-release-order.md` (8a66b01).
**Parent:** U8 cp1 `GO-05U8_cp1.blend` (`2341d554…`; gate 8a47583).
**Evidence:** `reviews/rac-rmot05u8a-evidence/`. **Tools (additive):** `tools/rac/w1/rmot05u8a_drivers/`. Readiness was committed before any desktop edit (cae9de8).

## **U8A LIMIT REACHED / PRESERVE CREASE OVER FURTHER FACET REDUCTION**

**Returned (preserved) scene:** the unchanged **U8 cp1**, `GO-05U8_cp1.blend` (sha `2341d554…60d6`).
- All 24 U8A gates pass on it (exit 0; `readiness/u8cp1_u8a_check/`).
- Crease A 0.7788 / B 0.3503.

**What happened:**
- **The attempt.** U8A checkpoint 1 lifted the crease-A anchor 61581 by 0.05995 cm (limit 0.06). It is technically safe: all 24 gates pass, crease A 0.7210, crease B 0.3503.
- **No visual gain.** It did **not** materially improve the lower wedge: identical-camera views at yaw 0, yaw 20 and pitch −45 are essentially unchanged.
- **Sharper facets.** The fold moved onto the crease-wall edge: 61219–61581 went from 34.16° to 45.90°, and corridor p95 from 31.83° to 36.69°.
- **Lost margin.** Crease A gave up 0.058 cm of margin for no visible benefit.
- **Checkpoint 2 not used.** The order permits it only after a material improvement, so it was **not** spent and **61580 was not moved**.

The finding: the residual wedge is not a removable anchor dent. It is the junction of the protected crease wall (61219, which sits flush, offset ≈ 0) with the posterior cap. Flattening it further would trade away the groove. Preserving the crease is the better outcome.

| Item | State |
|---|---|
| Gorrund | **UNACCEPTED**; author visual review of U8 cp1 |
| Grask E3 | FROZEN |
| RM-OT-05 | OPEN |
| Stage C | BLOCKED |
| Edited skin | INFERRED |
| Canon promotion | NOT PERFORMED |
| D4 / UE5 / production rigging / creator implementation | NOT STARTED |
| `base.glb` | unchanged |
| Rodin | not run |

## 1. U8A sets (`readiness/u8a_sets_v1.json`, sha `f3ac181c…`, pinned)

| Set | Contents |
|---|---|
| **Target** | {61580, 61581}, released for this block only |
| **Faces** | 13, all U2 cap faces. The P05U8A prefix equals P05U8, with the same prefix hash |
| Crease-run faces | A: 130140, 130141, 130353, 130354. B: 129904, 129905, 129906, 130132, 130133 |
| **Frozen ring** | 12, including the U8 cp1 edits 61562 / 61727 |
| Step limits | 61581 ≤ 0.06 cm, 61580 ≤ 0.04 cm, measured against U8 cp1 |
| Crease reference | `crease_reference_v1.json` (`c1efefde…`) and both thresholds **unchanged** |

## 2. Verifier and tests (additive; U2 / U4 / U6 / U7 / U8 unchanged)

- **`u8a_reintegrate.py`**: pinned U8 cp1, no topology change, every vertex outside the two anchors bit-exact. It explicitly reports the U8 cp1 edits, the U6 / U7 edits (except the released 61581) and the U6 target.
- **`u8a_guards.py`**: local quality on the 13 faces, anchor step limits, face 130139's minimum angle, and a dihedral diagnostic (61562–61580, 61219–61405, face 130139's edges, every edge at 61580 / 61581).
- **`u8a_aggregate.py`**: 24 mandatory gates, including U6 / U7 / U8 no-regression and crease A / B against the frozen reference by identity.
- **`check_return_u8a.sh`**: the whole path, plus U8cp1-vs-U8A renders.

**Tests** (`readiness/u8a_test_summary.json`): **7 / 7 as expected.**

| Test | Result |
|---|---|
| T0 | Unchanged U8 cp1: PASS, exit 0 |
| T1 | Another vertex (61562) moved: REJECTED |
| T2 | Topology change: REJECTED |
| T3 | Sub-10° face 130139: FAIL |
| T4 | Legal 0.02 cm 61581 move: accepted; crease A re-measured at the same frozen plane (0.7788 → 0.7581), exit 0 |
| T5 | Legal 0.02 cm 61580 move: accepted; crease B re-measured at the same frozen plane (section re-routed 9 → 7 faces; depth unchanged because B's deepest point lies near 62086), exit 0 |
| T6 | Lift pushing crease A below threshold (0.620): FAIL |

**Disclosed correction:** T5 first required the B **depth** to change. The fixture showed the measurement is recomputed but the maximum depth sits elsewhere, so the expectation was corrected. The measurement was not changed.

**Handoff:** `readiness/handoff/GO-05U8A_handoff.blend` (`1ec2240d…`). Positions are unchanged and the precheck result is byte-identical to U8 cp1.

## 3. Attempt (evidence; `attempt_cp1/`, `EDIT_LOG.md`)

| | U8 cp1 (returned) | U8A cp1 (attempt) |
|---|---|---|
| Scene sha | `2341d554…` | `5e07e11d…` |
| Moved | none | 61581, 0.05995 cm along its normal |
| Faces touched | none | 130137–130141, 130353, 130354 (all U8A faces) |
| U8A gates | 24 / 24 PASS | 24 / 24 PASS |
| Crease A / B | 0.7788 / 0.3503 | **0.7210** / 0.3503 |
| Face 130139 minimum angle | 14.87 | 16.09 |
| 61219–61581 | 34.16 | **45.90** |
| 61219–61405 | 30.51 | **38.13** |
| 61562–61580 | 32.28 | 32.28 |
| Corridor max / p95 / mean | 34.16 / 31.83 / 15.62 | 45.90 / 36.69 / 17.81 |
| Visual lower wedge | present | **unchanged** |

Global V4, V6 historical, V6c-1 and V6c-2 are reported as before, not waived.

## 4. Package

`gorrund_05U8A_crease_anchor_release_return.zip` holds:
- the preserved U8 cp1 scene and its reference;
- the attempt scene and its checks;
- readiness (sets, tests, handoff) and diagnostics;
- `EDIT_LOG`, the crease reference and `MANIFEST.sha256`.

Clean extraction, CRC check and reruns of `check_return_u8a.sh` on both extracted scenes are recorded in `package/`.

**→ STOP. U8A LIMIT REACHED / PRESERVE CREASE OVER FURTHER FACET REDUCTION.** Author visual review of U8 cp1 is required.
