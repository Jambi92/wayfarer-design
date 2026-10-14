# RAC RM-OT-05U8: final lower-cut facet cleanup gate

**Order:** `reviews/chatgpt-rac-rm-ot-05u8-final-lower-cut-facet-cleanup-order.md` (8e105da).
**Parent return:** U7 cp2 `GO-05U7_cp2.blend` (`1de9d0ac…`; gate bd4a7e8).
**Evidence:** `reviews/rac-rmot05u8-evidence/`. **Tools (additive):** `tools/rac/w1/rmot05u8_drivers/`. Readiness was committed before any production edit (ecc4bcb).

## **U8 BLOCKED ON CREASE-B ANCHOR 61580 / AUTHOR RULING REQUIRED**

The best safe checkpoint is returned: **U8 checkpoint 1**, `GO-05U8_cp1.blend` (sha `2341d554…60d6`). It passes **every** U8 safety gate (exit 0) and **materially reduces** the lower cut: edge 61562–61580 went from 41.82° to 32.28°, and corridor p95 from 35.32° to 29.53°.

The cut nevertheless **remains visibly conspicuous**. Its residual is carried by two frozen crease anchors that sit as dents:

| Anchor | Offset (inside neighbour centroid) | Status |
|---|---|---|
| **61580** (crease B) | 0.117 cm | Frozen by this order |
| **61581** (crease A; edited in U6; in the U8 frozen ring) | 0.121 cm | Frozen; its face 130139 is the wedge's outlier at 29.9° |

The editable U8 vertices are now nearly level, 0.066 cm (61562) and 0.107 cm (61727) inside their neighbours. Lifting them further would deepen the anchors' relative pits. Per order §7, checkpoint 2 was **not** spent, and neither anchor was moved.

**Disclosed:** the order names only 61580. The diagnostic shows the crease-A anchor 61581 is co-responsible for the residual wedge, whose apex is at about z 168.6, nearer 61581 than 61580. Any further repair needs an author ruling on one or both anchors. Both also define the frozen crease measurements, so moving either needs a ruling on the crease reference.

| Item | State |
|---|---|
| Gorrund | **UNACCEPTED**; author ruling required |
| Grask E3 | FROZEN |
| RM-OT-05 | OPEN |
| Stage C | BLOCKED |
| Edited skin | INFERRED |
| Canon promotion | NOT PERFORMED |
| D4 / UE5 / production rigging / creator implementation | NOT STARTED |
| `base.glb` | unchanged |
| Rodin | not run |

## 1. U8 micro-region (`readiness/u8_sets_v1.json`, sha `54414665…`, pinned)

Built once from the pinned U7 cp2 return (`cb2f1052…`).

| Set | Contents |
|---|---|
| Seeds | 61562, 61735, 61940 |
| **Support** | **61727**, the one-ring neighbour of 61562 that shares the two sharpest lower edges (61562–61727 40.6°, 61727–62061 32.0° at cp2) |
| **Editable** | **4** vertices (limit 8) |
| **Faces** | **19** (limit 28): 5 P05U7 prefix faces, 10 U2 cap faces, and U7 faces |
| Crease-run faces in U8 | A: 130352, 130353. B: 129905, 129906 |
| **Frozen ring** | **15**: includes **61580**, the U6-edited 61405 / 61581 / 61750 and the U7-edited 61586 / 62063 |
| Baseline | U8 faces' minimum angle 15.30°; no edge out of band |

## 2. Verifier (additive; U2 / U4 / U6 / U7 unchanged)

- **`u8_reintegrate.py`** (copy of the U7 adapter): pinned baseline U7 cp2, no topology change, every vertex outside the 4-vertex target bit-exact to cp2. It explicitly reports 61580, the U6-edited and U7-edited vertices, and the U6 target outside U8. It writes the P05U8 s_verify layout.
- **`u8_guards.py`**: local quality on the 19 faces, plus a diagnostic-only dihedral report with 61562–61580, every edge at 61735 / 61940, and corridor max / p95 / mean.
- **`u8_aggregate.py`**: 22 mandatory gates, listed in §4. Exit 0 only if all pass.
- **`check_return_u8.sh`**: the whole path, plus U7cp2-vs-U8 renders (posterior, zoom, lower-close, upper; shaded and wire; lateral / 3-4 / underside context).

**Focused tests** (`readiness/u8_test_summary.json`): **7 / 7 as expected.**

| Test | Result |
|---|---|
| T0 | Unchanged cp2: PASS, exit 0 |
| T1 | **61580 moved**: REJECTED |
| T2 | U8 ring vertex moved: REJECTED |
| T3 | U7 cp2 vertex 61771 moved: REJECTED |
| T4 | Topology change: REJECTED |
| T5 | Sub-10° U8 face: FAIL |
| T6 | Legal 0.02 cm target move: PASS, exit 0 |

**Handoff:** `readiness/handoff/GO-05U8_handoff.blend` (`d71cba07…`). Positions are unchanged, only groups and a README were added, and the precheck result is byte-identical to cp2.

## 3. Checkpoint 1 (real Blender UI, Edit Mode; `EDIT_LOG.md`)

| Vertex | Lift along its normal | Moved |
|---|---|---|
| 61562 | +0.10 | 0.0995 cm |
| 61727 | +0.08 | 0.0792 cm |
| 61735 | +0.05 | 0.0502 cm |
| 61940 | +0.08 | 0.0806 cm |

**19 faces touched, all U8 faces:** 129663, 129664, 129665, 129666, 129895–129899, 129905–129908, 130135–130138, 130352, 130353.

## 4. Return results (`return/checks/aggregate_u8.json`, exit 0)

**All 22 PASS:**
- U8 protection; topology; outside target bit-exact; ring unmoved;
- **61580 unmoved**; U6-edited unmoved; U7-edited unmoved; U6 target outside U8 unmoved;
- V1-U8; no FAIL verdict; V2; V3; V5; V6c-3;
- **crease A 0.7788** (≥ 0.6713) and **crease B 0.3503** (≥ 0.2743; unchanged);
- U8 local quality, minimum 16.16;
- U7 local quality 12.68;
- U6 target roughness max **32.41** (improved from 35.29); exceptions bit-exact; locus unchanged; cap minimum 13.41.

**Reported globally, not waived:** V4, V6 historical, V6c-1 and V6c-2 still fail, unchanged in scope.

**Dihedral diagnostic** (`diagnostics/dihedral_cp2_vs_cp1.json`):

| Edge or measure | U7 cp2 | U8 cp1 |
|---|---|---|
| 61562–61580 | 41.82 | **32.28** |
| 61586–61735 | 33.56 | 29.20 |
| 61675–61735 | 27.12 | 20.28 |
| 61940–62063 | 30.89 | 21.17 |
| 61940–61994 | 24.84 | 22.59 |
| Corridor max | 41.82 | 32.28 |
| Corridor p95 | 35.32 | 29.53 |
| Corridor mean | 14.31 | 13.64 |

**Visual** (identical cameras):
- **Upper (61735 / 61940):** the facets are visibly smoother.
- **Lower:** the wedge is reduced but still conspicuous at yaw 0 / 20 / pitch −45.
- The groove, deltoid / triceps relief and the U6 / U7 repairs are intact, with no new dent, spike, ridge, lip or melted patch.

## 5. Package

`gorrund_05U8_lower_cut_cleanup_return.zip` holds:
- the cp1 scene and its reference;
- checks, readiness (sets, tests, handoff) and diagnostics;
- `EDIT_LOG`, the crease reference and `MANIFEST.sha256`.

Clean extraction, CRC check and the corrected-path rerun are recorded in `package/`.

**→ STOP. U8 BLOCKED ON CREASE-B ANCHOR 61580 (with crease-A anchor 61581 co-responsible) / AUTHOR RULING REQUIRED.**
