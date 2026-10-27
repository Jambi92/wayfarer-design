# RAC RP3 — Marchfolk v003 shared family-core gate

**Date:** 2026-10-26
**Order:** `reviews/chatgpt-rac-rp3-marchfolk-family-core-v003-order.md` (103c832)
**Parent:** v002, `reviews/claude-rac-rp3-marchfolk-production-baseline-gate.md` (5fd48e2)
**Evidence:** `reviews/rac-rp3-evidence/marchfolk_family_core_v003/`
**Tools:** `tools/rac/rp/marchfolk_rp3_v001/` (v003 files listed in §12)

## Result: FAMILY BASE FAIL / NEEDS AUTHOR DECISION

v003 is a clear improvement on v002, and it keeps both configurations on one shared topology.

| | Configuration 1 (MF-M-R) | Configuration 2 (MF-F-R) |
|---|---|---|
| Firm §7 failures | 19 → 3 | 20 → 7 |
| T-4 violating quads | −39 % | −37 % |

Density, anatomy, face readiness and contact all pass. No new deformation-class failure appears.

Mandatory §7 items remain unresolved, so the order requires this decision rather than PASS. The residuals fall into two classes, and §5 asks for an author decision on each:

1. **Measurement-undefined stations: thumb MCP (both configurations) and the configuration-2 shoulders.**
   - On every failing side, the band method's ray finds no outward-facing surface.
   - Its endpoint is therefore arbitrary: it falls to tie order, not to geometry.
   - The literal closed-ring test passes for the thumb with a thumb-sized radius.
2. **Toe interphalangeal crease poles in toe contact zones: toe3 j3 (both configurations) and toe4 j2 (configuration 2).**
   - Loop counts are 5–6 against 2 required.
   - Each station has one crease pole.
   - Every relocation tried creates 16–326 new self-intersecting face pairs with neighbouring surface (adjacent toe or interdigital web) that lies within about 1 mm.

**Production files** (`E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Marchfolk/RP3/`):

| File | Verts / quads | sha256 | Geometry hash |
|---|---|---|---|
| `MF_M_REF_RP3_retopo_v003.blend` | 57,674 / 57,672 | `5b793eda…` | `64ecbff0…` |
| `MF_F_REF_RP3_retopo_v003.blend` | 57,674 / 57,672 | `a5d8adfe…` | `ebf5829d…` |

- Both files share face topology hash `68f7b6a9…`.
- Alongside them: sidecars, `_hm08_map.npz` per configuration, `MF_REF_RP3_v002_to_v003_map.npz`, v003 landmark packages, and `MF_RP3_v003_manifest.json`.
- v001 and v002 are untouched.
- PC read-back: both v003 blends, both v002 blends and the manifest re-stage with identical sha256.

## 0. Answers to the §16 questions

| Question | Answer |
|---|---|
| Are both configurations on identical v003 topology? | **Yes.** Same face list, vertex order, UV layout and map structure. The hm08→v003 map files are byte-identical in content. Face hash `68f7b6a9…` for both. See `mapping/MF_v003_common_topology.json` and `MF3_core_diagram.jpg`. |
| Are all mandatory joint-loop stations passing? | **No.** Configuration 1 fails thumb_mcp_l, toe3_j3_l and toe3_j3_r. Configuration 2 fails shoulder_l, shoulder_r, thumb_mcp_l, toe3_j3_l/r and toe4_j2_l/r. Every other station passes in both: elbows, wrists, all four finger MCP roots, hips, knees, ankles, all MTP / toe-root (j1) stations, toe2 j3 and neck. |
| What firm / strict failures remain? | Firm: as above (3 / 7 of 69). Strict: 9 (configuration 1) and 11 (configuration 2) of 69, down from 27 and 26. The added strict-only items are middle and ring MCP (a pole 1.7–2.0 loops off the crease, just inside the 2-loop band) and toe4 j3 in configuration 1. Full table: `v3_report.json` → `configs.{M,F}.stations`. |
| How much did T-4 improve? | Union of angle- and aspect-violating quads: 3,797 → 2,322 (6.61 → 4.03 %) for configuration 1 and 3,594 → 2,271 (6.26 → 3.94 %) for configuration 2. Angle: 1,326 → 935 and 1,368 → 938. Aspect: 2,596 → 1,563 and 2,338 → 1,489. Hands improved most (730 → 230), then head (72 → 10), face (1,514 → 996) and feet (1,119 → 797). |
| Are all density zones still passing? | **Yes**, all 9 zones in both configurations. Mean edge changes by ≤ 0.002 % of stature from v002 (§4). |
| Did anatomy remain within tolerance? | **Yes.** T-1, T-2, T-3 and T-7 pass for each configuration independently (§3). |
| Did face / UFCA readiness remain intact? | **Yes.** Mouth rings 35, orbit rings 43 + 43, 0 poles within 2 cm of the mouth or at its corners, 4 poles per eye (outside the lid rings), as in v002. Face density 0.137 / 0.134 %. Surface-fit landmark drift ≤ 0.0007 mm. The jaw-hinge estimate remains provisional. |
| Did any new topology-class deformation failure appear? | **No.** All 16 poses match v002 within ±1 count and ±2 % volume, with two contact-class exceptions. In configuration 1, hip flex 90 in-zone contact pairs went 52 → 62 (thigh against abdomen). In configuration 2, fist folds went 4 → 5 (finger–palm). |
| Result of the configuration-1 knee-centre comparison? | **Mechanically acceptable.** Moving the knee centre to the section centroid (+1.92 cm lateral) on v003 changes knee 90 from −31.1 to −29.5 % volume (self-x 54 → 43, flips 15 → 11), and knee 140 from −47.5 to −46.2 % (self-x 63 → 62, folds 3 → 5). That is ≤ 1.6 points of volume and mixed elsewhere. The source-rig landmark is unchanged. |
| Is v003 ready to freeze as the shared MPFB-family base? | **Not without the author decisions in §7.** Everything else the freeze rule lists is met. |

## 1. What v003 changed (local and conservative)

The v002 architecture is kept unchanged: linear subdivision, the 98 leg rings and the hm08 map.

**Topology.** Ten closed root rings were inserted, five per side, mirrored, with appended vertices only (+240). v002 vertex order is kept.

| Ring | Strip quads | Added vertices |
|---|---|---|
| Pinky MCP / hypothenar root | 28 | 28 |
| Toe-1 MTP root | 24 | 24 |
| Toe-2 MTP root | 24 | 24 |
| Toe-3 MTP root | 24 | 24 |
| Toe-4 / toe-5 MTP root | 20 | 20 |

No pole was added or removed: 164 valence-3 and 156 valence-5+ poles, as in v002.

**Junction-pole relocation.** Each pole was slid along its joint axis to about 2.3 local loops off the crease, with a cosine falloff over the neighbouring rings and a short tangential relax.

- Every relocated vertex is a barycentric point on one hm08 source triangle of the configuration-average surface, inside its own UV chart.
- Its map row therefore has 3 hm08 weights. It is identical for both configurations and lies on each configuration's own source surface.
- Accepted moves:
  - ankle crease;
  - index, middle, ring and pinky MCP roots;
  - the forefoot MTP fan, moved as one group (the shared poles between toe roots, slid proximally past every toe-root crease);
  - toe2 j3.
- Every move was accepted only if, in both configurations, it caused:
  - no station regression;
  - no source vertex more than 0.8 mm off the surface;
  - no new self-intersection.

**T-4 relaxation.** Violating quad clusters in the face, hands and feet were relaxed using a tangential Laplacian plus parallelogram completion. The same acceptance rules applied, plus face-ring preservation.

**Repair and restore.**
- An envelope / contact repair pass restored 318 relocated vertices to their v002 rows. These were vertices that had moved a source vertex more than 0.8 mm off the surface, or created hand / foot contact in an earlier build iteration.
- T-4 relaxation within 18 cm of the shoulders was also restored (322 vertices).

**T-4 caveat.** The feet improved overall (1,119 → 797 / 797 → 752 violating quads). But new angle and aspect outliers now sit on the interdigital webs at the toe roots, where the MTP root rings and the grouped forefoot pole slide meet the web (`MF3_quality_{M,F}.jpg`, foot panel). These are the obvious next T-4 targets if a further cycle is authorised.

Per-zone change table (changed and added vertices, changed faces, maximum relocation, T-4 before → after, reason): `v3_report.json` → `configs.{M,F}.zones`.

- Vertices moved more than 0.1 mm from v002: 11,083 (configuration 1) and 10,989 (configuration 2).
- Moved more than 1 mm: 2,140 and 2,064.
- Maximum 15.9 / 12.9 mm, which is the ankle pole slide.

## 2. Mapping (§6)

| Map | File | Notes |
|---|---|---|
| hm08 → v003 | `MF_{M,F}_REF_RP3_retopo_v003_hm08_map.npz` | Identical content in both files. Every row sums to 1. |
| v002 → v003 | `MF_REF_RP3_v002_to_v003_map.npz` | The first v002 block is the hm08 vertex set, so the same rows apply. Routing through v002 reproduces v003 exactly (max difference 0.0). |

Transfer paths:
- **Weights:** `M3 @ W_hm08`, renormalised.
- **UVs:** unchanged corners keep their v002 corner UVs. Relocated vertices take the barycentric UV of their source triangle, in the same chart; seam vertices were pinned.
- **MPFB targets / morphs:** `M3 @ D`.

Common-topology proof: `mapping/MF_v003_common_topology.json`.

## 3. Anatomy preservation (§7), per configuration

| | Stature Δ | bbox max \|Δ\| | prod→src median / p95 / max | Identity-zone max (head / ears / hands / feet) | src→prod max (body / hands / feet) | IoU front / rear / profile L / R |
|---|---|---|---|---|---|---|
| Configuration 1 | −0.41 mm | 0.41 mm | 0.00 / 0.19 / 1.76 mm | 0.88 / 0.47 / 0.82 / 1.45 | 0.78 / 0.76 / 0.78 | 0.9978 / 0.9978 / 0.9973 / 0.9973 |
| Configuration 2 | −0.00 mm | 0.20 mm | 0.00 / 0.16 / 2.00 mm | 0.91 / 0.45 / 0.73 / 0.83 | 0.79 / 0.73 / 0.79 | 0.9980 / 0.9980 / 0.9975 / 0.9975 |
| Limits | T-3 ±1 | ±2 | T-1 0.5 / 1.5 / 3.0 | T-2 max 1.5 (p95 0.8) | T-2 max 1.5 | T-7 ≥ 0.995 |

- Production → source maximum improved on v002 (2.57 / 2.19 → 1.76 / 2.00 mm).
- Source → production rose from ~0 to ≤ 0.79 mm, held under 0.8 mm by the acceptance rule.
- Self-intersecting face pairs: 68 → 60 (configuration 1) and 122 → 122 (configuration 2). All are source arm–trunk / face / toe contact.
- Sheets: `MF3_overlay_{M,F}.jpg` (deviation heat, v002→v003 relocation heat, silhouette) and `MF3_body_{M,F}.jpg`. `MF3_closeups_{M,F}.jpg` covers head, hands, feet, shoulder and groin.

## 4. Density (§9)

All zones pass in both configurations. Mean edge as % of stature, v002 → v003 (p95 in brackets):

| Zone | Configuration 1 | Configuration 2 |
|---|---|---|
| face | 0.137 → 0.137 (0.38 → 0.38) | 0.135 → 0.134 |
| hands | 0.140 → 0.139 (0.30 → 0.29) | 0.127 → 0.126 |
| feet | 0.198 → 0.197 (0.59 → 0.58) | 0.187 → 0.186 |
| trunk | 0.509 → 0.509 | 0.511 → 0.511 |
| arms | 0.483 → 0.483 | 0.443 → 0.443 |
| legs | 0.514 → 0.514 | 0.501 → 0.501 |
| ears / neck / head | unchanged | unchanged |

Totals: 57,674 vertices / 57,672 quads, against v002's 57,434 / 57,432. Sheet: `MF3_density_{M,F}.jpg`.

## 5. Loop audit — all 69 stations (§8)

Full per-station table for both configurations, with loops, crease poles, poles within 2 loops, nearest pole and firm / strict verdicts for v002 and v003: `v3_report.json` → `configs.{M,F}.stations`. The raw audits are `audit/MF-{M,F}-R_v003_audit.json`.

| | v002 firm fail | v003 firm fail | v003 strict fail |
|---|---|---|---|
| Configuration 1 | 19 | **3** (thumb_mcp_l, toe3_j3_l/r) | 9 |
| Configuration 2 | 20 | **7** (shoulder_l/r, thumb_mcp_l, toe3_j3_l/r, toe4_j2_l/r) | 11 |

## 6. Face readiness (§10)

Unchanged from v002 in both configurations:
- mouth rings 35, orbit rings 43 + 43;
- 0 poles within 2 cm of the mouth, 0 at its corners;
- 4 poles per eye;
- open orbit / lip pockets kept, with the sharp-fold rim vertices pinned during relaxation.

Sheet: `MF3_closeups_{M,F}.jpg`, face row.

## 7. Residual stations — why they are not fixed, and the decision needed (§8)

Detail for every side of every residual: `residuals_final.json`. It records ray-exit defined or undefined, endpoint axial separation, path, axial edges, and closed rings at the station radius and at a 3 cm radius.

### 7.1 Thumb MCP (configuration 1 left, configuration 2 left; the right passes in both)

- On **all four** band sides the ray-exit test is undefined. No vertex in the probe ball faces the side direction (normal · side > 0.3), so `surf()` falls back to tie order among the candidates.
- The thumb MCP sits inside the thenar mass, so rays from the band ends run through the palm.
- Under the band method, the counted sides give 3 / 2 / 5 (configuration 1) and 3 / 1 / 5 (configuration 2). The short sides span 0.3–0.9 cm of axial separation, against a 1.6 cm band.
- The **literal contract test passes**: closed edge rings encircle the thumb axis within ±0.8 cm of the joint. There are 3 (configuration 1) and 4 (configuration 2) with a 3 cm radius. The thumb MCP cross-section reaches about 2.8 cm; the station radius of 1.6 cm is the finger value.
- Forcing the band count would need two to three more loops inside a 0.3 cm axial span. That is a local edge length of about 0.1 cm, roughly 3× denser than the hand, which conflicts with §4.1 ("do not increase hand density globally without justification") and with T-4.

### 7.2 Configuration-2 shoulders

- The failing side is undefined: `+p` on the left and `−p` on the right.
- shoulder_l: 3 there; its other sides are 9 / 7 / 13. v002 also failed (4).
- shoulder_r: 4; it passed in v002 with 6.
- The configuration-2 right shoulder region is **bit-identical to v002**: no vertex within 15 cm moved. The candidate vertices and their normals are identical.
- The changed count is only a tie-break among equally invalid candidates. The 240 appended ring vertices change the kd-tree order.
- Configuration 1 passes both shoulders (10 / 6).
- Fixing would mean changing geometry where nothing is wrong. I do not recommend doing so.

### 7.3 Toe IP crease poles in toe contact zones

Stations: toe3 j3 (both configurations) and toe4 j2 (configuration 2).

- Loops are 5–6 against 2 required.
- Each station has one IP junction pole 0.01–0.2 loops from the crease.
- Every relocation attempted created 16–326 new self-intersecting face pairs:
  - 5 displacement variants;
  - toward the digit root and the original side;
  - source-surface and v002-surface projection.
- The new pairs are between the slid toe faces and faces outside the moved patch that lie only 0.7–1.2 mm away (centre to centre): the adjacent toe or the interdigital web. v002 has 0 hand / foot pairs in configuration 1.
- Moving these poles therefore needs either a toe-separation anatomy change (not authorised) or a topological pole reroute of the toe-IP fan (a re-design of the hm08 toe tube, beyond "local and conservative").

### Decisions requested

- **D1.** Accept the thumb-MCP closed-ring result with a thumb radius (3 / 4 rings), and the defined sides of the configuration-2 shoulders, as passing §7 for these stations. Or name another measure.
- **D2.** Accept the three toe-IP crease poles as recorded contact-zone residuals. Or authorise a toe-tube pole reroute, or a toe-separation change.

With D1 + D2 accepted, every other freeze criterion in §13 is met.

## 8. Diagnostic deformation (§11)

Same 16 poses, same source rig and weights carried through each map. Native, v002 and v003 results: `deformation/deform_*_v003.json` (v002 and native are in the parent evidence).

- **v003 ≈ v002 everywhere.** Configuration 1: fist contact 296 → 286; hip flex 90 contact 52 → 62 (thigh against abdomen, contact class). Configuration 2: fist 400 → 404, folds 4 → 5; hip flex strain p95 47 → 49.
- **Failure classes are unchanged from v002:**
  - weights: LBS volume collapse at elbow, knee, hip and shoulder flex;
  - contact / setup: fist, thumb, wrist into thigh, deep flexion.
- **No topology-class failure.**

Sheet: `MF3_deform_{M,F}.jpg` (v002 | v003).

## 9. Configuration-1 knee centre (§12)

| v003, source weights | Self-x (in zone) | Folds | Flips | Strain p95 | Volume |
|---|---|---|---|---|---|
| knee 90, source-rig centre | 54 | 8 | 15 | 62.8 % | −31.1 % |
| knee 90, section-centroid candidate | 43 | 8 | 11 | 62.9 % | −29.5 % |
| knee 140, source-rig centre | 63 | 3 | 76 | 69.8 % | −47.5 % |
| knee 140, section-centroid candidate | 62 | 5 | 75 | 70.2 % | −46.2 % |

The v002 run gives the same picture (`knee/deform_MF-M-R_v002_kneeC.json`).

**Verdict: mechanically acceptable.** The centroid gives ≤ 1.6 points of volume and is mixed elsewhere; the remaining loss is weights-class. No canonical landmark change. Sheet: `MF3_knee.jpg`.

## 10. Hashes (§1 / §16)

- **Before and after** this order, the source hashes are unchanged:
  - MF-M-R R-6 `2caaf056…`, build `c5be9ca0…`;
  - MF-F-R R-6 `c254fb4b…`, build `252907fd…`.
- **Parent v002 unchanged:**
  - `MF_M_…v002.blend` `c02f77bf…`;
  - `MF_F_…v002.blend` `9f228ad1…`;
  - v002 map `28d4e46e…`.
- v003 file hashes: `production_files_sha256.txt` and `source_hashes_before_after.json`.

## 11. Evidence index (`reviews/rac-rp3-evidence/marchfolk_family_core_v003/`)

| Folder / file | Contents |
|---|---|
| `audit/` | v003 audits and face rings for both configurations |
| `anatomy/` | anatomy preservation |
| `landmarks/` | v003 landmark packages |
| `deformation/` | v003 deformation results |
| `knee/` | knee-centre comparison (v002 and v003) |
| `mapping/` | `MF_v003_common_topology.json` |
| `v3_report.json` | zone change table, T-4, density, 69-station table |
| `residuals_final.json` | residual-station detail |
| `MF_*_REF_RP3_retopo_v003.json`, `MF_RP3_v003_manifest.json` | sidecars and manifest |
| `sheets/` | `MF3_body`, `MF3_closeups` (face, shoulder / axilla, elbow, hand dorsal / palmar MCP, ankle, foot dorsal / plantar, with pole maps and counted rings), `MF3_quality` (T-4 heat), `MF3_density`, `MF3_overlay` (source / v002 / v003), `MF3_deform`, `MF3_knee`, `MF3_core_diagram` (junctions changed v002 → v003) |

## 12. Tools (`tools/rac/rp/marchfolk_rp3_v001/`)

- `core3lib.py`: base loading; station audit with the same maths as `audit.py`; surface projection; ring insertion; mirror map.
- `ring_search.py`: candidate root rings.
- `v003_build.py`: R / P / T stages with acceptance; `--resume`, `--env-mm`, `--surf2`, `--prox-ip`.
- `repair.py`: envelope / contact repair.
- `revert_region.py`.
- `residuals.py`, `v3diag.py`, `revert_probe.py`.
- `make_v3cand.py`, `v3_report.py`, `mf3_sheets.py`, `sidecars3.py`.
- `mf_deform.py`: adds `KNEE_OFF_CM` and `ONLY_POSES`.

**Build lineage.** Full build (`core_e`) → `repair.py` → resume P + T (`core_g`) → `revert_region.py shoulder_l,shoulder_r 18` → `core_final`.

## 13. Stop

**STOP FOR CHATGPT REVIEW.**

v003 is **not frozen**. Not started: Skarn, Sagekin or any other race, family propagation, production rig or weights, creator morphs, final UVs or materials, LODs, UE5, Turnfall.
