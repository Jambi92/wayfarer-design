# RAC RP2 — Grask E3 internal asymmetry adjudication

**Date:** 2026-10-23
**Order:** `reviews/chatgpt-rac-rp2-grask-production-pilot-execute-order.md` §4
**Executor:** Claude
**Source:** `reviews/reference-assets/r6/GR5DE3_r6.npz`, sha256 `d859eb18…d778`. Re-hashed before and after; unchanged. The source was not modified.

**Result:** every significant region is classified. There is no Class A region and no contradiction, so there is **no escalation**. Production target **H**:
- the bilateral average S* below z = 167 cm (Class B regions);
- the original E3 above z = 173 cm (Class C base kept);
- a smoothstep blend between those two heights.

Evidence is in `reviews/rac-rp2-evidence/`:
- `gates/asym_tables.json`, `gates/stations.json`, `gates/shading_geo.json`;
- `sheets/sheet_asymmetry.jpg`: E3, E3 mirrored, S*, H and W2 GR218R from front, profile, back and 3/4, plus E3 and W2 heat maps;
- `tools/asym_evidence.py`, `tools/hybrid.py`.

## 1. Diagnostic surfaces

| Surface | Definition |
|---|---|
| E3 | The source body, 13 380 vertices on the shared hm08 topology. |
| E3 mirrored | Each vertex takes the x-mirrored position of its mirror partner. The mirror map comes from W2 GR218R by nearest neighbour. Two midline vertices map to themselves. |
| S* | Bilateral average (E3 + E3 mirrored) / 2. Volume 107.91 L; stature 217.98872 cm, the same as E3. |
| H | The adjudicated production target. S* + β(z)·(E3 − S*), with β = 0 below 167 cm, 1 above 173 cm, smoothstep between. |
| W2 GR218R | The prior Grask reference, near-symmetric. |

## 2. Measurements

Mirror deviation is |X − mirror(X)| in mm. That is twice the distance to the bilateral average.

| Region | n | E3 p95 | E3 max | W2 p95 | W2 max |
|---|---|---|---|---|---|
| Whole body | 13 380 | 2.58 (rms 1.93, p99 10.57) | 27.19 | 0.05 (p99 0.48) | 6.28 |
| Head / face (z ≥ 195) | 3 826 | 2.04 | 2.82 | 0.00 | 0.01 |
| Shoulder / neck / trapezius (170–195, trunk) | 886 | 11.48 | 17.25 | 0.01 | 0.20 |
| Upper arm / deltoid (≥ 150, arm) | 496 | 15.04 | 18.62 | 0.18 | 1.01 |
| Axilla / scapular (150–170, trunk) | 574 | 0.48 | 1.37 | 0.01 | 0.05 |
| Chest / abdomen band (120–150, trunk) | 526 | 10.60 | 13.72 | 0.17 | 0.76 |
| Pelvis / crotch (100–120) | 86 | 3.14 | 27.19 | 1.41 | 3.20 |
| Forearm / hand | 3 740 | 0.08 | 5.48 | 0.01 | 6.28 |
| Thigh / knee | 552 | 0.64 | 1.27 | 0.62 | 0.99 |
| Shin / ankle / foot | 2 360 | 0.91 | 3.16 | 0.08 | 0.22 |

The heat map (`sheet_asymmetry.jpg`) shows two concentrated features:
- a **ring around the trunk at z 120–150**: the chest/abdomen band, front and back;
- a **cap over both shoulders and the trapezius line**.

Everywhere else is below about 1 mm.

**Landmarks.** The E3 rig joint pairs (_l / _r) are exactly bilateral: the maximum side difference over all pairs is **0.000 mm**. So the skeleton carries no asymmetry.

**Silhouettes.** Measured in the front view at 10 px/cm (`stations.json`):
- Trunk half-widths at z 110 / 120 / 135 / 150 / 165 differ left to right by at most 0.1 cm in E3, S* and production. Profile depths are identical.
- The one silhouette-level asymmetry is the shoulder line:

| Reading | E3 | S* |
|---|---|---|
| Girdle slope, x 10 → 20 cm | 30.96° one side, 25.17° the other | 28.37° both sides |
| Shoulder top at x = ±20 cm | 181.4 / 183.4 cm | 182.3 / 182.4 cm |
| Trunk half-width at z 180 | 23.6 / 21.4 cm | 22.6 / 22.5 cm |

**Family persistence.** The asymmetry field correlates with E3's in the whole construction family:

| Family | Correlation | p99 |
|---|---|---|
| GR5B198 / 218 / 239 | 0.79–0.80 | ≈ 7.7 mm |
| GRA218 | 0.80 | 7.8 mm |
| GR5CA / CB / CC | 0.92–0.94 | ≈ 9.6 mm |
| GR5DE1 / DE2 | 0.997–0.998 | 10.5 mm |

W2 GR218R has essentially none (p99 0.48 mm). The asymmetry therefore entered with the GR5B construction stage and was inherited and slightly amplified through C, D and E. It was not introduced as an E3-specific design decision.

**Mechanism.**
- The shared hm08 quad graph is not mirror-consistent: 28 edges have no mirror edge, and the source has 224 mirror-inconsistent triangles concentrated at the crotch, the trunk at 120–150 and the feet.
- A plain 40-iteration uniform Laplacian on W2 does **not** reproduce the pattern (correlation −0.17, p99 0.12 mm). So the exact operator that produced it is not identified.
- What is shown: the pattern is construction-stage (family-persistent from GR5B), surface-only (skeleton exactly bilateral) and sits on the same band the Stage C ruling names as a retopology / surface issue.

**Shading.** The shading-normal left/right asymmetry in the band, at fixed sample points with their mirror images, is p50 0.46° / p95 1.61° for E3. The bilateral average reduces the p95 to 1.15°, and production v001 reduces it to p50 0.00° / p95 0.34° (`shading_geo.json`).

## 3. Classification and decision

| Region | Class | Reason | Production |
|---|---|---|---|
| Chest / abdomen band, z 120–150, front and back | **B** | One-sided surface organization: a trunk ring. Skeleton bilateral; no silhouette effect (half-widths and depths equal). The Stage C ruling names it a retopology / surface / normal issue, not canon. | Symmetrized (S*). Keel, flank and abdominal organization are untouched; they are bilateral in E3. |
| Pelvis / crotch, z 100–120 | **B** | Localized at the mirror-inconsistent crotch triangles and inside the self-intersection lens. No skeletal support. | Symmetrized, then resolved by the crotch slot (gate report §4). |
| Shin / ankle / foot | **B** | ≤ 3 mm, at the mirror-inconsistent foot triangles. No landmark support. | Symmetrized. |
| Axilla / scapular, thigh / knee, forearm / hand | below significance (≤ 1.4 mm, matching W2's own level) | — | S* (no visible change). |
| **Shoulder / neck / trapezius line and deltoid cap, z ≥ 170** (head and face included; ≤ 1.4 mm there) | **C** | Family-persistent construction origin with a bilateral skeleton, so the base looks like artefact. But it is the only asymmetry that **forms the accepted front silhouette**: girdle slope differs by 5.8° side to side and the shoulder line by about 2 cm. Symmetrizing it changes the accepted front-view girdle read and alone drops front silhouette IoU against the source to 0.9952, leaving no T-7 margin. Order §4.3 allows removal only when it does not weaken the front-view read and the result still passes the contract, so the conservative default applies: keep the accepted shape. | **Base kept as E3.** The superimposed surface artefact (facet and shading noise of the 13k reference) is removed by production fairing. The blend in 167–173 cm is a smooth, low-passed displacement with no seam. |

No region has the equal support for "intentional anatomy" and "artefact" that §4.4 requires, so no alternative pair was needed. One candidate was still built and gated for comparison:
- **cand_s3**, fully symmetric (S* everywhere), passed T-1 and T-2 against S*.
- It **failed T-7 against the source**: front 0.9909, profile 0.9935.
- It also lowered one shoulder line and changed both girdle slopes to 28.4°.
- It was rejected internally (gate report §6).

The chosen interpretation passes every gate (gate report).

## 4. Result against the accepted identity

| Reading | E3 | H | Production v001 |
|---|---|---|---|
| Girdle slope, both sides | 30.96° / 25.17° | 30.96° / 25.17° | 30.54° / 25.17° |
| Shoulder tops at x = ±20 cm | 181.4 / 183.4 cm | 181.4 / 183.4 cm | 181.4 / 183.4 cm |
| Trunk half-widths and profile depths (z 110–180) | — | — | Within 0.1 cm of E3 at every station |
| Front-silhouette IoU against E3 | — | 0.9989 | 0.9959 |

GR-G1 and GR-P2b are read on the skeletal proxy route, and the rig joints are unchanged, so their readings are unchanged by construction.

**Recommendation:** use H as the RP2 production target (as implemented).

**For later stature points (RP3 and the creator):** apply the same split per stature. Symmetrize the band and crotch; carry the girdle-line asymmetry as part of the accepted E3 organization (Stage C rule 1: relationship-aware across stature).
