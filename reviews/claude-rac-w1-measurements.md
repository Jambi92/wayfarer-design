# RAC Wave 1 — Measurements (DIAGNOSTIC)

**Author:** Claude **Date / pass:** October 5, 2026, W1 pass 1
**Status:** Every value here is **DIAGNOSTIC** (order §6). Nothing is canon, no bound moved, no envelope adopted.
**Raw data:** `reviews/rac-w1-evidence/*.json` (full precision). Tables round for reading only; no borderline value was rounded across a limit.

Only accepted-pending-author ARMs were measured: **SA-M** and **SA-F**. Marchfolk candidates were not measured (CONSTRAIN / FAIL).

## 1. Common identification

| Field | SA-M | SA-F |
|---|---|---|
| ARM ID / version | SA-M v1 (aff1b52 frozen) | SA-F v1 (derived, §263 CEN) |
| Asset hash | `a925e067…8b8c9c` | derived from the same hash; params in ARM record |
| Race / stature | Saurin / 187.880 cm (tail excluded) | Saurin / 187.881 cm |
| Configuration | male centre | female centre |
| Frame | head-local = body frame (x right, f forward, u up); accepted as FH*-equivalent in r3, no rotation applied | same |
| Tools | `tools/rac/w1/saurin_w1.py`, `saurin_convention.py`, `saurin_sym_regions.py`; prior chain `tools/rodin/v1` (metrics), `v5` (tissue), `wf_saurin_head63.py` (eye centres) | same |

## 2. RM-CF-01 — Saurin rostral projection (r3 convention)

**Landmarks (r3):** HL = f(FAL) − f(Op). FAL = most anterior vertex with head-region weight > 0.95 within |x| < 1 cm of the midline; Op = most posterior vertex with head-region weight > 0.95 above u 176 cm. No separate keratin/lip exclusion was applied: the base is one continuous surface and the midline tip vertex was taken as FAL. If the author places FAL behind a keratin or lip layer, the projection values shrink; this is listed in D-1. **OC_mid** = midpoint of the two eyeball centres (eye centres at (±3.56, 10.31, 183.47) cm, tracked under deformation by the mean displacement of their 200 nearest vertices). FPI = (f(FAL) − f(OC_mid)) ÷ HL.

| Case | HL (raw, cm) | Projection FAL−OC (raw, cm) | FPI (derived) | FAL repeatability (top-20 spread, cm) |
|---|---|---|---|---|
| SA-M base | 31.871 | 10.371 | **0.3254** | 0.024 |
| SA-M pitch −3° | 31.652 | 10.063 | 0.3179 | 0.024 |
| SA-M pitch +3° | 32.025 | 10.660 | 0.3329 | 0.025 |
| SA-M scaled-surface file | 31.824 | 10.335 | 0.3248 | — |
| SA-F base | 31.898 | 10.379 | **0.3254** | 0.025 |
| Corner: rostrum length −15 % | 30.648 | 9.147 | 0.2985 | 0.021 |
| Corner: cranium length +8 % | 33.241 | 10.371 | 0.3120 | 0.025 |
| Corner: rostrum −15 % × cranium +8 % (uncoupled) | 32.018 | 9.147 | 0.2857 | 0.021 |
| Corner: rostrum length +20 % | 33.502 | 12.002 | 0.3582 | 0.029 |

**Uncertainty:** landmark placement ±0.03 cm on FAL (≈ ±0.001 FPI). Head pitch is the dominant sensitivity: ±3° moves FPI by ≈ ±0.0075. Left/right: FAL lies on the midline (|x| 0.002 cm); OC is the midpoint of symmetric eyes (head mirror median 0.06 cm), so separate L/R values do not differ at reported precision.

## 3. RM-CF-01 under the Part 7 (closure) convention

The canon rostral index (reference 0.288; band 0.255–0.335; floor 0.255 provisional) was defined at Saurin closure with a **corneal-surface proxy** landmark ~1.19 cm anterior of the eye centre, not the r3 eye centre.

| Case | Head length (cm) | Rostral projection (cm) | Part 7 index | vs floor 0.255 |
|---|---|---|---|---|
| Reference | 31.871 | 9.177 | 0.2879 | above |
| Rostrum −15 % | 30.648 | 7.953 | 0.2595 | above |
| Cranium +8 % | 33.241 | 9.177 | 0.2761 | above |
| Uncoupled corner (−15 % × +8 %) | 32.018 | 7.953 | **0.2484** | **below** — the canon coupling rule would CONSTRAIN this combination |
| Rostrum +20 % | 33.502 | 10.808 | 0.3226 | above |
| **Coupled corner** (bisection at cranium +8 %): rostrum length factor 0.8847 | — | — | **0.2550** | at floor; **r3 FPI there = 0.2920** |

**Finding (diagnostic):** the same anatomy reads ≈ +0.037 higher under r3 than under Part 7 (an offset of ≈ 1.19 cm ÷ HL). The Saurin floor is stated in Part 7 terms. Which convention defines the floor is an author decision (D-1); the floor was not changed. Under either convention the reference body sits well inside the band and the coupled minimum sits exactly at the floor by construction.

## 4. Saurin body readings (raw; reproduce the closure reference)

| Item | SA-M | SA-F | Canon |
|---|---|---|---|
| Stature (vertex) | 187.880 | 187.881 | 188 |
| Head length / ratio | 31.871 cm / 0.1696 | 31.898 cm / 0.1698 | ratio 0.156–0.184 |
| Head width / depth | 14.188 / 14.951 cm | — | — |
| Shoulder breadth | 38.731 cm | — | — |
| Thorax width / depth / d÷w | 37.986 / 33.410 cm / 0.8796 | d÷w 0.9217 | 0.88 / 0.922 |
| Lower trunk | 32.000 cm | 33.640 cm | 32.0 / 33.6 |
| Pelvic width | 41.732 cm | 43.055 cm | 41.7 / 43.1 |
| Tail length | 121.40 cm (64.61 %) | 64.66 % | — |
| Tail mass share | 0.1545 | — | — |
| Required balance lean | 8.82° | — | — |
| Body volume | 136.94 L | — | — |

## 5. Symmetry readings (R-5 support; SA-M)

| Region | Median mirror distance (cm) | p99 | max |
|---|---|---|---|
| Head | 0.057 | 0.42 | 0.73 |
| Tail | 0.199 | 2.23 | 2.59 |
| Torso | 0.473 | 3.10 | 3.55 |
| Arms | 1.351 | 3.41 | 4.73 |
| Legs | 1.968 | 6.91 | 7.73 (left knee, x −30.5, u 38.8) |

## 6. Not measured

All RM items needing Marchfolk or any purpose-built ARM: RM-UB-07, RM-LR-01/02/05/06/07, RM-OT-01, RM-CF-02…10 (except 01), RM-UF-01, RM-SR-01…04, RM-UB-01 (except SA basis), RM-UB-06. See `claude-rac-w1-blocked-assets.md`.

— Claude
