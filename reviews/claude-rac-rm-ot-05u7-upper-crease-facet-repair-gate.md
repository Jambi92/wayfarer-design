# RAC RM-OT-05U7: upper-crease facet repair gate

**Order:** `reviews/chatgpt-rac-rm-ot-05u7-minimal-upper-crease-facet-extension-order.md` (d22466e).
**Parent return:** U6A cp3 `GO-05U6_cp3.blend` (`22345d4d…`; gate bb65683).
**Evidence:** `reviews/rac-rmot05u7-evidence/`. **Tools (additive, opt-in):** `tools/rac/w1/rmot05u7_drivers/`. Readiness was committed before any production edit (5d2374e).

## **TECHNICALLY SAFE U7 RETURN / AUTHOR VISUAL REVIEW REQUIRED**

The return is U7 checkpoint 2, `GO-05U7_cp2.blend` (sha `1de9d0ac…b667`). Every U7 safety gate passes and `aggregate_u7.json` exits 0.

**Visual result: partial.**
- Inside the authorized U7 corridor (z ≈ 171–172), the upper saw-tooth cuts are visibly softer in the identical-camera views. The facet diagnostic agrees: p95 dihedral 30.42 → 23.50°, max 35.64 → 33.56°.
- The groove, deltoid / triceps relief and the U6A lower repair are intact, with no new dent, lip, ridge, spike or melted patch.
- **Not every visible cut is removed.** The most prominent remaining cut sits lower, at about z 168.7–169.7. That is U6-target cap geometry, frozen by this order: the sharpest corridor edge, 61562–61580, measures 41.8° at cp3 and is untouched.
- The remaining sharpest U7-adjacent edges run to frozen-ring vertices 61735 and 61940.

Further improvement would need an author decision to open those vertices. **The U7 budget is spent (2 / 2).**

| Item | State |
|---|---|
| Gorrund | **AUTHOR VISUAL REVIEW REQUIRED** (UNACCEPTED) |
| Grask E3 | FROZEN |
| RM-OT-05 | OPEN |
| Stage C | BLOCKED |
| Edited skin | INFERRED |
| Canon promotion | NOT PERFORMED |
| D4 / UE5 / production rigging / creator implementation | NOT STARTED |
| `base.glb` | unchanged |
| Rodin | not run |

## 1. U7 region: frozen sets (`readiness/u7_sets_v1.json`, sha `67aeca8d…`, pinned)

Built once from the pinned cp3 return (`cbb78605…`) by `u7_sets.py`.

| Set | Contents |
|---|---|
| Seeds (order §2) | 61522, 61771, 62027, 61586, 61183, 62063 |
| **Editable target (5)** | 61183, 61586, 61771, 62027, 62063 (z 171.2–172.1). Limit is ≤ 24 |
| **Held seed** | **61522 stays frozen**: it is an endpoint of the frozen crease-B entry edge 61355–61522 in `crease_reference_v1.json`. Moving it would invalidate the frozen crease measurement |
| **U7 faces (22)** | All faces incident to the target. 18 are P05U2 protected-prefix faces; 4 (129903, 130130, 130131, 130132) are approved U2 cap faces. Limit is ≤ 70 |
| **Frozen outer ring (14)** | One topological ring around the target, including 61522 and the U6-target vertices 61580 / 62086 |
| U6 target overlap | **None**; all 16 U6 cp3 vertices are frozen |
| Baseline | U7 faces' minimum angle at cp3 is 12.68°; no U7 edge is outside 0.25–2.5 cm |

The seed probe (`readiness/seed_region_probe.txt`) also lists the corridor's sharpest edges at cp3. The worst, 61562–61580 (41.8°), lies between U6-target vertices and is outside U7 scope.

## 2. Verifier (additive; U2 / U4 / U6 paths unchanged)

- **`u7_reintegrate.py`**
  - Pins S3, F1, cp3, the sets and the layout files.
  - Checks no topology change: one-to-one ids and S3 faces with the same orientation.
  - Requires **every vertex outside the 5-vertex target bit-exact to cp3**: the 14-vertex ring, the 16 U6 vertices and everything else.
  - Rejects non-finite values; keeps the cp3 labels unchanged.
  - Writes the s_verify layout with prefix **P05U7** (P05U2 minus the 18 U7 prefix faces), so the U7 faces are evaluated by V2 / V3 / V5 / V6c.
- **V1-U7.** `s_verify` runs on the P05U7 prefix (coordinate hash `d8e9af0f…`, pinned from cp3) with source exemption limited to the cp3 exemptions plus the 5 target vertices.
- **`u7_guards.py`**
  - Local quality on the 22 faces: no degenerate or inverted face, every face ≥ 10°, no edge outside 0.25–2.5 cm.
  - A **diagnostic-only** facet report: dihedrals on every edge touching a U7 face, with max / p95 / mean and per-seed values, compared with cp3. It has no pass threshold.
- **`u7_aggregate.py`** exits 0 only if all of these pass:
  - protection vs cp3, topology, outside-target, ring, U6A lower repair unchanged;
  - V1-U7, no FAIL verdict, V2, V3, V5, V6c-3;
  - crease A / B (frozen reference, by identity);
  - U7 local quality;
  - U6 no-regression (target roughness ≤ 36.3, exception identity, locus, cap quality).
- **`check_return_u7.sh`** runs the whole path, plus cp3-vs-U7 renders: posterior, zoom and upper close-up (each shaded and wire), and lateral / 3-4 / underside context.

**Focused tests** (`readiness/u7_test_summary.json`): **8 / 8 as expected.**

| Test | Result |
|---|---|
| T0 | Unchanged cp3: all PASS, exit 0 |
| T1 | A vertex just outside the target and ring moved: REJECTED |
| T2 | A U7 ring vertex (61735) moved: REJECTED |
| T2b | Held seed 61522 moved: REJECTED |
| T3 | U6 cp3 vertex 61581 moved: REJECTED |
| T4 | Sub-10° U7 face (129671): local quality FAIL |
| T5 | One face reversed (topology change): REJECTED |
| T6 | Positive: a legal 0.02 cm target move passes the full check, exit 0 |

**Handoff:** `readiness/handoff/GO-05U7_handoff.blend` (`ad610624…`), built from cp3 by `u7_build_handoff.py`. Positions are unchanged, only vertex groups and a README were added, and the precheck passes with a result byte-identical to cp3.

## 3. Desktop checkpoints (real Blender UI, Edit Mode; `EDIT_LOG.md`)

| CP | Moves (along each vertex's own normal) | U7 gates | Facet p95 / max (cp3 30.42 / 35.64) |
|---|---|---|---|
| cp1 `d2546bca…` | 61771 +0.12; 61586 +0.06; 62063 +0.07 | PASS, exit 0 | 33.22 / 35.40 (62027 became a relative pit) |
| **cp2** `1de9d0ac…` | 62027 +0.06 | **PASS, exit 0** | **23.50 / 33.56** |

## 4. Return safety results (`return/checks/aggregate_u7.json`, exit 0)

**All PASS:**
- protection vs cp3: 0 moved outside the target, 0 ring vertices moved, **0 U6A vertices moved**;
- topology unchanged;
- V1-U7; no FAIL verdict; V2; V3; V5; V6c-3;
- **crease A 0.7890** (≥ 0.6713; unchanged from cp3) and **crease B 0.3503** (≥ 0.2743; cp3 0.3658);
- U7 local quality: minimum angle 12.68, no degenerate / inverted / out-of-band face or edge;
- U6 no-regression: target roughness max 35.29, exceptions bit-exact, locus unchanged, cap minimum 13.41.

**Reported globally, not waived:** V4, V6 historical, V6c-1 and V6c-2 still fail, unchanged in scope.

**Exact changes vs cp3:** 4 vertices — 61771 (0.1197 cm), 61586 (0.0606), 62063 (0.0700), 62027 (0.0600).

**16 faces touched, all U7 faces:** 129666, 129667, 129668, 129897, 129898, 129899, 129900, 129901, 129902, 129903, 130127, 130128, 130129, 130130, 130131, 130132. The full list is in `diagnostics/changes_vs_cp3.json`. No topology change.

## 5. Package

`gorrund_05U7_upper_crease_facet_return.zip` holds:
- the return scene and its reference;
- checks, checkpoints, readiness (sets, tests, handoff) and diagnostics;
- `EDIT_LOG`, the crease reference and `MANIFEST.sha256`.

Clean extraction, CRC check and the corrected-path rerun on the extracted scene are recorded in `package/`.

**→ STOP for Tyler's visual review.**
