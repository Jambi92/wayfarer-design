# RAC Stage C — validation protocol (frozen at C0)

**Order:** `reviews/chatgpt-rac-stage-c-entry-order.md`, executed under `reviews/chatgpt-rac-stage-c-execute-after-d1-d3-order.md` (5aa5501).
**Rulings:** `reviews/tyler-chatgpt-rac-stage-c-d1-d3-author-ruling.md` (95e7bc3): D1 = (a), D2 = (c), D3 = (a).
**Written:** 2026-10-18, by Claude at C0, before any C2 result was read.

This file records which validators exist and how each one maps onto the two Stage C sources. **It adds no thresholds.** Every threshold, operator and comparator below is the one already in the frozen code or a committed gate. Where a validator cannot apply, it is marked **N/A** or **DEFERRED** with the reason, and nothing replaces it.

## 1. Sources

| Race | Stage C source | Rule |
|---|---|---|
| Gorrund | `GO-05AW4_nails_final.blend` `5a4e45d4…2d5e` / `.glb` `e6b32503…6fc8` (05AX4). One sculpted mesh at 204.5225 cm. No rig, no skinning, no composition or Frame states. | D1(a): reference state only. D2(c): native height. |
| Grask E3 | Procedural build from the frozen `GR.E3` entry in `reviews/rac-rmot05d-evidence/candidates.json`, using the 05B arch from `reviews/rac-rmot05b-evidence/cfg_final.json`. The 05D route is `gr_body.build(..., arch=A['GR'], racebase=SP['GR']['E3'])`. | D3(a). The mesh hash is recorded at C0. Grask W2 records are not modified. |
| Roster comparators | Frozen r6 assets in `reviews/reference-assets/` (hash-checked against `manifest.json`), Skarn `SK208-C1R` (`reviews/rac-w3d-evidence/geometry/`), and the Saurin canonical W2 base `saurin_w2_final_base.npz` `f86ae800…`. | Read-only. |

**Grask E3 states used.** These are the states the frozen E3 contract already supports:
- reference 218;
- LOW composition;
- Narrow (GRN5 frame);
- Broad (GRB2 frame);
- the stature points 198 / 208 / 229 / 239, which the W2C suite requires.

The named W2 extremes (GR-BODY-06…18) are **not** re-derived for E3. Deriving them would be a new block.

## 2. Validators and mapping

| # | Validator (frozen code) | Grask E3 | Gorrund sculpt |
|---|---|---|---|
| V1 | **W2C suite**, families U C G S K B F D M X (`tools/rac/w1/w2c_drivers/w2c_eval.py`), run through `tools/rac/w1/stagec_drivers/stc_w2c_eval.py` | RUN. Each E3 body is placed in the W2C registry slot of the same name (GR198/208/218/229/239, GR-LOW, GRN5, GRB2). | **N/A.** The suite reads the MPFB rig joints, vertex-group slab breadths (`jbw`), the composition grid (CIB) and the stature series. The sculpt has none of these. |
| V2 | **Canonical G rows** (W1 row set: skeletal CIB, skin, directional), `gr_eval` | RUN on every E3 body | **N/A**, same reason |
| V3 | **05D minimal guards** (`guard_all`): stature, ground, skeleton unchanged, outward normals, true floor, self-intersection, arm clearance, posture, protected skeletal stations | Taken from the frozen 05D record. The E3 bodies are rebuilt bit-identical (§4), so the guard values apply unchanged. | **N/A** (procedural-route guards) |
| V4 | **W2D suite** (Gorrund families U C G S K B F M X AD3 D) | not applicable (Grask uses W2C) | **N/A / DEFERRED.** Same inputs as V1. Families C, B, F, M and X also need variant or stature states, which D1(a) defers to the creator. |
| V5 | **05AX4 mesh-integrity gate**: components / boundary / non-manifold 1 / 0 / 0, genus 3, self-intersections 0, stature 204.5225 | n/a | RUN by hash identity. The source hash matches 05AX4, so the AX4 integrity record applies unchanged. It is re-hashed after the run. |
| V6 | **UFCA / MPFB / ALPC guards** | Already folded into V1 to V3 (ALPC skeletal stations, MPFB proxy). Nothing extra. | **N/A**: there is no MPFB proxy or ALPC station set |
| V7 | **C3 visual / roster read** (05E §9.3, 05F §6, 05H / 05J purpose rules) | RUN | RUN |

## 3. Measurement rules (all already ruled)

1. **Protected skeletal relations.** These are GR-P2b and the related protected relations. Author ruling 2 in `reviews/chatgpt-rac-rm-ot-05e-gorrund-structural-readability-closure-order.md` applies: they are read **on the skeleton at skeleton-anchored stations**, which is the 05D `protected_unorganized_route` reading.
   - The W2C / G readings taken on the organized surface are **diagnostics**.
   - A failure in an organized-surface reading of a protected relation is reported. It is not counted as a protected failure.
2. **Retired comparators.** Rows whose comparator is the procedural Gorrund (W1i `GO217` / `GO224` / `GOH208`, or the "GO" candidate in G rows) compare against a body that D1(a) retires.
   - These rows are **N/A** for Stage C.
   - They are not re-pointed at the sculpt, because the sculpt cannot produce the same readings.
3. **Mixed generations.** Rows that compare a W2-era named extreme (GR-BODY-06…18) with the E3 central body are **N/A**. The extreme is not an E3 state.
4. **Stature (D2(c)).**
   - The sculpt is measured at its native 204.5225 cm.
   - For matched-height pairs only, a uniformly scaled copy is made in memory at 203, 208, 218 or 229 cm. The factors are 0.9926, 1.0170, 1.0659 and 1.1197.
   - These copies are never saved as bodies, never treated as height variants, and never used as evidence of stature construction.
   - The canon envelope stays roughly 208 / 229 (230.9) / 251.
5. **Silhouette overlap (C3).** The IoU numbers are **REPORT-only**, with no pass line. Each pair is shown with the accepted-distinct Skarn ↔ Marchfolk pair as a baseline. The distinctness decision is visual (§7 of the entry order) and goes to the author.

## 4. Reproduction proof required before C2 counts

- **W2 bodies.** The W2-era Grask bodies (GR198/208/218/229/239, GRN5, GRB2) are rebuilt through the W1 → W2C pipeline. The canonical G rows must reproduce the committed W2C record exactly (57 / 57 rows).
- **Adapter.** `stc_w2c_eval.py` must reproduce all 373 committed W2C checks with the rebuilt W2 bodies in the race slots.
  - The only change from `w2c_eval.py` is that registry entries marked `frozen` read their measurement values and canonical rows from the committed `reviews/rac-w2c-gr-evidence/w2c.json`.
  - This lets the W2 bodies remain as continuity comparators while E3 fills the race slots, without rerunning or editing Grask W2.
- **E3 builds.** The E3 reference, LOW, N and B must be geometry-identical to the frozen 05D r6 assets.

## 5. Status vocabulary

| Status | Meaning |
|---|---|
| PASS / REPORT | As the frozen code emits them |
| FAIL / NOT ALL PASS / NON-MONOTONIC / NOT DEMONSTRATED | As emitted, then classified (P / N / I / R / A) in the gate |
| N/A (reason) | The validator cannot run on this source |
| DEFERRED TO CREATOR | The check needs a Gorrund variant (D1(a)) |
