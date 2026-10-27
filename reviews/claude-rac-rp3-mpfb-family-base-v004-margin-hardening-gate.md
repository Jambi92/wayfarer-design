# RAC RP3 — MPFB Family Base v004 margin hardening: Marchfolk + Skarn dual validation — gate

**Date:** 2026-10-26
**Order:** `reviews/chatgpt-rac-rp3-mpfb-family-base-v004-margin-hardening-order.md` (a18371c)
**Evidence:** `reviews/rac-rp3-evidence/mpfb_family_base_v004/`
**Production candidates:** `E:/…/production/Marchfolk/RP3/` and `E:/…/production/Skarn/RP3/`, with copies in the session outputs.

## Verdict

**MPFB FAMILY BASE v004 — NEEDS AUTHOR DECISION (one validator rule, D5). NOT FROZEN.**

What the successor delivers:
- one topology on all four configurations;
- the heel fix (C1R feet T-2 1.70 → 1.19 mm, all four ≤ 1.30 mm);
- hip margin (Marchfolk 5 → 6, C1R 4 → 5);
- toe-3 root margin (MF-F and SK-F 2 → 3; the C1R crease pole is cleared);
- 0 new contact defects and unchanged anatomy, identity, density and face;
- T-4 within budget.

Firm PASS under the authoritative D1 + D3 + D4 validator:

| MF-M | MF-F | SK-C1R | SK-F |
|---|---|---|---|
| **69 / 69** | **69 / 69** | **67 / 69** | **67 / 69** |

**The one blocker is `toe2_j1_l/r` on both Skarn configurations (1 / 2).**
- No single closed ring can fix it (§4.3).
- It is a probe-endpoint condition at the toe-2 web, not Skarn anatomy.
- Under the proposed rule **D5**, all four configurations are 69 / 69 and nothing else changes verdict.

Following §17, nothing was frozen; v003 remains the active, immutable MPFB Family Base v1.

## Answers to §20

| Question | Answer |
|---|---|
| Is D4 implemented and stable on Marchfolk + Skarn? | **Yes.** `val2lib.py` (`validator_v2.py --scale-ref 173.143`). Station scale: MF-M 0.9998, MF-F 0.9991, C1R 1.2011, SK-F 1.2014. Refactor regression: station verdicts are byte-identical to the v003 and Skarn outputs. Marchfolk stays 69 / 69 under D1 + D3 + D4. |
| Did the heel correction bring Skarn configuration 1 within T-2? | **Yes.** C1R feet T-2 max 1.704 → **1.195 mm**. All four are ≤ 1.30 mm: MF-M 0.918, MF-F 0.826, SK-F 0.865. The 8 re-expressed rows sit exactly on every race's source (0.000 mm). |
| Did the hip band gain usable margin? | **Yes.** MF-M 5 → **6**, MF-F 14 → 15, C1R 4 → **5**, SK-F 12 → 12 (target ≥ 6 / ≥ 5 met). The preferred Skarn 6 is not reached: C1R is at margin 0. |
| Did the toe-2 / toe-3 roots gain usable margin? | **Toe 3: yes.** MF-M 5 → 6, MF-F 2 → 3, SK-F 2 → 3; C1R stays 3 and its own-digit crease poles are cleared. **Toe 2: partly.** MF-F 2 → 3; the ring adds a loop on the measured plantar side everywhere. But MF-M stays 2 and both Skarn stay **1 / 2** because of the web-side probe condition (§4.3). |
| Are all four configurations on one identical successor topology? | **Yes.** 57,854 V / 57,852 Q, face hash `2bd4c8b3…`, one hm08 map `19a83550…`, one UV layout. Read-back of all four blends is exact. |
| Do all four have 69 / 69 firm PASS? | **No.** MF-M 69, MF-F 69, C1R **67**, SK-F **67** (`toe2_j1_l/r`). Under proposed D5: 69 / 69 / 69 / 69. |
| Which zero-margin stations remain? | `toe1_j1_l/r` in all four. Also `thumb_mcp_l/r` (MF-M, C1R), `toe2_j1_l/r` and `toe2_j2_l/r` (MF-M), `toe4_j1_l/r` (MF-M, MF-F, C1R) and `hip_l/r` (C1R). Removed from the zero-margin list: hip (MF-M), toe3_j1 (MF-F, SK-F), toe2_j1 (MF-F). |
| Did any new self-intersection / contact defect appear? | **No.** Pair counts are identical to the v003 fit (60 / 122 / 54 / 94), and no pair touches a changed vertex. No groin, toe, web, sole or hand change. |
| Did all anatomy gates pass? | **Yes, all four.** T-1, T-2, T-3 and T-7 pass. Every zone maximum except feet is unchanged. All 124 landmarks are identical, including the hip joints. |
| Is C1R identity preserved? | **Yes.** The face is unchanged. Face → C1R source median 0.000 / p95 0.089 / max 1.016 mm; face → pre-C1R median 1.10 mm. The identity signal is mean 1.55 mm. |
| Did density pass? | **Yes, 9 / 9 zones in all four.** Only the foot and trunk means change (−0.001 %), and the successor is not over-dense. |
| Did T-4 stay within the regression budget? | **Globally yes:** MF-M +0.124 pp, MF-F +0.112 pp (budget 0.15). **Locally:** splitting the tapered web side of the toe-root strips adds 18–24 quads with aspect > 10 per configuration. The maximum aspect is unchanged (it is a pre-existing v003 quad). Conservative fairing did not remove them and cost loops (§7). |
| Did any topology-class deformation failure appear? | **A small local one.** In toe extension 30°, 4–8 flipped faces per configuration lie in the new toe-ring quads whose v003 parents did not flip. Hip flex adds 1 such face in MF-F and C1R. Every other increase is an existing v003 flip region split into more faces. |
| Is the successor ready to freeze as the active MPFB Family Base? | **Not under the accepted validator.** It is ready if the author accepts D5 and the toe-ring local cost (§10). |
| Is Skarn ready for freeze? | **Not yet.** It is 67 / 69 under D1 + D3 + D4. With D5 it would pass every §18 criterion. |
| Is MPFB Family Propagation Standard v1 ready for author acceptance? | **Not yet.** It is updated with D4 accepted, D5 proposed and the successor metrics. The status stays DRAFT until the D5 / toe-2 decision. |

## 1. Provenance firewall

**Verified before work started and again before commit:** frozen v003 MF_M / MF_F blends, maps and freeze record, the four accepted sources, and all v001–v003 production files (`immutable_hashes_before_after.txt`).

| Item | SHA-256 prefix |
|---|---|
| `MF_M_REF_RP3_retopo_v003.blend` | `5b793eda` |
| `MF_F_REF_RP3_retopo_v003.blend` | `a5d8adfe` |
| v003 hm08 map | `bc3b7c54` |
| v002 → v003 map | `0829d1dc` |
| Freeze record | `4af62f81` |
| MF-M-R R-6 | `2caaf056` |
| MF-F-R R-6 | `c254fb4b` |
| SK208-C1R R-6 / build | `fd8a43d2` / `c1c54d28` |
| SKF208 R-6 / build | `0245683e` / `ddf77a84` |
| Skarn v001 blends | `9d84ea36` / `d8084ac7` |

v003 was neither modified nor relabelled. The successor names are new.

## 2. Successor construction

Build: `tools/rac/rp/marchfolk_rp3_v001/v004_build.py --relocate-toe3`, deterministic. Every operation is a row of the one family map and is mirrored.

### A. Posterior heel (order §4)

- **Selection rule.** Foot vertices behind the ankle whose v003 row is a linear hm08 quad-centre row (4 × 0.25 on one quad) and whose v003 deviation exceeds 1.0 mm on any accepted configuration. This selects exactly **8 vertices, 4 mirrored pairs**, all on the posterior heel / Achilles insertion.
- **New row.** Each row becomes the barycentric point of the **same hm08 quad** closest to the old linear point on the family reference surface. That is ≤ 0.8 mm along the surface; it is not a reshaping.
- **Records.** Old and new rows are in `provenance/MPFB_FAMILY_v004_heel_rows.json`.
- **Effect.** Those vertices now lie exactly on every race's own source.

Feet T-2 max (production → source):

| | MF-M | MF-F | C1R | SK-F |
|---|---|---|---|---|
| v003 | 1.449 | 0.826 | 1.704 | 0.865 |
| v004 | 0.918 | 0.826 | **1.195** | 0.865 |

The new C1R maximum is a medial-arch quad-centre row. It was out of scope for "posterior heel" and left unchanged.

### B. Hip support ring (order §5)

- **Placement.** One closed ring split into the strip between frozen-v003 loops 195 | 790. It runs around the pelvis at the hip-joint height (MF-M ring z 90.4–93.4 cm vs thigh head 92.1 cm; C1R 106.9–110.5 vs 109.1).
- **Symmetry.** It crosses the midline, so it is **self-mirrored**: one ring serves both hips.
- **Size.** +84 V / +84 Q.
- **What it avoids.** It passes above the pubic / perineal region: no groin topology is touched, no new contact, no T-4 change in the trunk or legs.
- **How it was chosen.** `v004_ringsearch.py` scored every closed strip through the band on all four configurations; the chosen ring is the one closest to the joint centre among those giving MF ≥ 6 and C1R ≥ 5.
- **No alternative met the preferred C1R 6.**

### C. Toe-2 / toe-3 root rings (order §6)

- **Toe 2:** one ring in the strip 497 | 1262.
- **Toe 3:** one ring in the strip 508 | 1264.
- Both are mirrored, +48 V / +48 Q each; no other toes were touched.
- New vertices: 171 of 180 were re-expressed as on-surface barycentric rows (≤ 0.55 mm move). The 9 UV-seam vertices keep their linear edge-midpoint rows.
- **Toe-3 crease poles.** On C1R the D4-scaled toe3_j1 window contains two forefoot valence-5 poles (12596 / 13154, mirrors 5999 / 6558) that D3 assigns to toe 3. Each was slid along the toe-3 axis by the minimum 0.02 cm grid step that clears the window on all four configurations: 0.8 mm distal / 0.6 mm proximal, 1-ring cosine falloff, 22 rows. Toe spacing, webs, MTP positions and toe lengths are unchanged (§5).

### Map provenance

Row classes:

| Class | Meaning | Rows |
|---|---|---|
| 0 | unchanged v003 | 57,644 |
| 1 | linear ring (seam) | 9 |
| 2 | heel barycentric | 8 |
| 3 | ring barycentric | 171 |
| 4 | toe-3 pole slide | 22 |

Every successor vertex is a convex combination of at most 4 hm08 vertices, identical for every race.

## 3. Maps and transfer proofs (order §8)

`maps/MPFB_FAMILY_v004_transfer_proof.json`.

**hm08 → v004** (`MPFB_FAMILY_BASE_v004_hm08_map.npz`, `19a83550…`):
- row sums 1.0000;
- 0 negative weights;
- row support ≤ 4;
- unchanged rows bit-identical to the frozen map.

**v003 → v004** (`MPFB_FAMILY_v003_to_v004_map.npz`):
- exact for the 57,644 unchanged rows;
- topological parent edge midpoints for ring vertices;
- identity for re-expressed rows.

The authoritative geometry is the hm08 map. The residual by class is recorded (max 1.71 mm, at the C1R heel rows, which is the correction itself).

**Weights.**
- 53 bones; per-vertex sums 0.99990–1.00000 (inherited from the source); min 0.
- Unchanged rows are identical to v003 (max diff 0).

**UVs.**
- 57,492 faces unchanged, UV diff 0.
- Seam vertices 2,369 → 2,378 (the 9 seam ring vertices).
- All UVs in [0, 1].

**MPFB targets.** M4 @ (A + Δ) = M4 @ A + M4 @ Δ to 6e-14 cm, and it equals the target race's own realization exactly. Tested for MF-M → MF-F, MF-F → SK-F and MF-M → C1R (Δ up to 35 cm).

## 4. 69-station validator (order §11)

Files:
- `validator/*_v004_validator_v2.json` — legacy and D1 + D3, unscaled;
- `*_v004_validator_v2_D4.json` — authoritative;
- `*_D4_D5proposed.json`.

Sheets: `v004_validator_D4.jpg` and `MPFB_v004_margin_table.jpg`. Tables: `MPFB_FAMILY_v004_margin_table.{json,csv}`, giving loops, minimum, margin, crease poles (all / own digit), mode and D5 for every station × configuration × {v003, v004}.

### 4.1 Firm PASS, D1 + D3 + D4

| | MF-M | MF-F | SK-C1R | SK-F |
|---|---|---|---|---|
| frozen v003 fit | 69 | 69 | 63 | 67 |
| **successor v004** | **69** | **69** | **67** | **67** |
| v004 under proposed D5 | 69 | 69 | 69 | 69 |

### 4.2 Target stations (loops / minimum, v003 → v004)

| Station | MF-M | MF-F | SK-C1R | SK-F |
|---|---|---|---|---|
| hip_l/r (5) | 5 → **6** | 14 → 15 | 4 → **5** | 12 → 12 |
| toe3_j1_l/r (2) | 5 → 6 | 2 → **3** | 3 → 3 (crease pole cleared: FAIL → PASS) | 2 → **3** |
| toe2_j1_l/r (2) | 2 → 2 | 2 → **3** | **1 → 1 FAIL** (D5: 2) | **1 → 1 FAIL** (D5: 3) |

### 4.3 Why toe2_j1 cannot pass on Skarn with a ring

On both Skarn configurations, one band side measures only the toe-2 web side (the 2–3 cleft).
- **No usable probe.** At the proximal band end (D4: 0.48 cm before the MTP cube) no toe-2 surface vertex answers the probe. The nearest is 0.64 cm (C1R) / 0.76 cm (SK-F) off the probe line, which is more than W.
- **Same loop at both ends.** The selected endpoint and the distal endpoint therefore both lie on the same edge loop (frozen loop 1120). That loop runs along the toe axis at the web. The band "path" is **one edge** of that loop, so loops = 1.
- **No ring can split it.** No closed quad strip crosses that edge. Through one end runs a 2,228-vertex longitudinal loop; through the other only open loop segments. So no single closed ring can split it.
- **Search result.** All 16 candidate toe-2 strips were tested on all four configurations (`ring_search_toe.json`). None reaches 2 on Skarn.
- **Marchfolk.** It sits at exactly 2 on the same side for the same reason, which is why MF-M toe2_j1 stays at margin 0.
- **What the ring does do.** The chosen ring raises the plantar side: MF-M 2 → 3, C1R 1 → 2, SK-F 2 → 3.

I did **not** move vertices to change the probe's endpoint choice. That would satisfy an undefined measurement, which the standard forbids.

### 4.4 Proposed D5 (not applied as authoritative)

**Rule.** For digit stations, a side is undefined when either selected endpoint lies farther from its probe line than W. It is then excluded as in D1. This is D1 made literal for inter-digital webs.

**Blast radius on v004, all 69 × 4 stations:**
- `toe2_j1_l/r` C1R 1 → 2 and SK-F 1 → 3;
- `toe1_j2_l/r` SK-F 3 → 4 (already passing);
- nothing else changes;
- Marchfolk is unchanged;
- 4–16 sides per configuration become undefined.

On frozen v003, D5 alone does not rescue C1R toe2. The new ring is needed for the plantar side.

### 4.5 Validator semantics note (for the record; no verdict changes)

In the left-handed analysis frame, the probe facing test (`VN · side > 0.3`, from RP2 `audit.py`) uses vertex normals that point inward numerically. A side's endpoint therefore usually lies on the surface facing **away** from the named direction ("+q" samples the −q surface of a digit). On thick segments it can land on another body part (for example hip "+p"). This applies equally to every gate since RP2. It is documented in the standard §6.

## 5. Anatomy, landmarks and identity (order §9)

`anatomy/*_v004_anatomy.json`, `region_deviation_pelvis_shoulder.json`, `lm/landmark_shift_v003_v004.json`.

T-1 / T-2 / T-3 / T-7 pass on all four. Maxima in mm, production → source / source → production:

| | MF-M | MF-F | SK-C1R | SK-F |
|---|---|---|---|---|
| body | 1.763 / 0.784 (= v003) | 1.998 / 0.793 (=) | 2.047 / 1.028 (=) | 2.025 / 0.975 (=) |
| head / ears / hands | = v003 | = | = | = |
| feet | 1.449 → **0.918** / 0.784 | 0.826 / 0.793 | 1.704 → **1.195** / 1.028 | 0.865 / 0.887 |
| pelvis-groin max | 1.682 / 0.425 (=); p95 0.441 → 0.426 | = | = | = |
| shoulder | = | = | = | = |
| stature diff | −0.415 | 0.000 | −0.508 | 0.000 |
| min silhouette IoU (4 views) | 0.99730 | 0.99747 | 0.99836 | 0.99823 |

- All 124 landmarks are identical to the v003 fit, including the hip-joint landmark.
- **C1R identity** (`face_identity.py`, same comparison for the v003 fit and v004): the v004 face equals the v003 fit. Face → C1R source median 0.000 / p95 0.089 / max 1.016 mm; face → aligned pre-C1R median 1.096 / p95 2.775 mm; identity signal mean 1.55 / p95 3.30 mm.
- **Method change.** The face region is now defined explicitly (head > 0.5, no ear, anterior to the ear centroid: 3,172 hm08 vertices). The prior gate's inline set had 3,480; its numbers (1.65 / 0.090 / 1.016 / 1.22) agree within that definition change.
- Sheet: `v004_C1R_face.jpg`.

## 6. Contact (order §10)

`contact/*_v004_contact.json`. Self-intersection pairs, v003 fit → v004:

| MF-M | MF-F | C1R | SK-F |
|---|---|---|---|
| 60 → 60 | 122 → 122 | 54 → 54 | 94 → 94 |

- Pairs touching any changed or new vertex: **0** in all four.
- New family-base contact defects: **none**. No hand, foot, toe, web, sole or groin change.

## 7. Density and T-4 (order §12 / §13)

**Density.** 9 / 9 zones pass in all four.
- v004 means equal v003 except foot −0.001 and trunk −0.002 % of stature.
- Foot p95: 0.58 / 0.56 / 0.62 / 0.61 % (the contract ceiling applies to the mean).
- Size is +180 V / +180 Q (+0.31 %); not over-dense.

**T-4 union:**

| | MF-M | MF-F | SK-C1R | SK-F |
|---|---|---|---|---|
| v003 | 4.026 % | 3.938 % | 5.233 % | 3.943 % |
| v004 | 4.150 % | 4.050 % | 5.352 % | 4.045 % |
| Δ (budget 0.15) | **+0.124** | **+0.112** | +0.119 | +0.102 |

- All the increase is in the feet: angle +26–31, aspect +66–80. Trunk, legs, hands and face are unchanged.
- **Local slivers.** The toe-root strips taper to about 0.8 mm rungs at the web, where v003 already had aspect about 6. Splitting them gives aspect 12–13 halves: +18–24 quads with aspect > 10 per configuration. The body maximum aspect is an unchanged v003 quad.
- **Fairing tried.** Umbrella / parallelogram, 2–12 iterations, ring-only and +1-ring patches. It removed only 7–11 % of the toe-patch violations, did not lower the maximum aspect, and cost loops (MF-M toe3 6 → 2; toe2 plantar 3 → 2). It was not applied.

Sheets: `v004_T4_*.jpg`, `v004_density_*.jpg`.

## 8. Face / UFCA (order §14)

Unchanged on all four, and equal to v003:
- mouth rings MF 35 / C1R 29 / SK-F 35;
- orbit rings 43 / 43;
- mouth-corner poles 0; poles within 2 cm of the mouth 0; eye-region poles 4 / 4;
- open pockets kept;
- face density unchanged.

No face topology changed.

## 9. Deformation sanity (order §15)

`deformation/MPFB_v004_deformation_comparison.json` and `MPFB_v004_flip_parentage.json`. All 18 poses, native | v003 fit | v004.

- **Unchanged:** every pose that does not touch the patches, including ankle dorsiflexion and knee 90 / 140 (0 change).
- **Hip flex 90:** flips v003 → v004 are 48 → 56, 34 → 40, 52 → 61, 41 → 49. Of these, 56 / 39 / 60 / 49 sit inside v003 faces that already flipped: the same LBS groin crease collapse (**weights / setup**) split into more faces. 0 / 1 / 1 / 0 are new, on the hip ring.
- **Toe extension 30:** flips 64 → 70, 50 → 58, 65 → 71, 31 → 37. Of these, **4 / 8 / 4 / 6** are new, all in the toe-2 / toe-3 ring quads. That is **topology-attributable**: thin web-side half-quads at the toe-root crease under one-bone LBS. Toe flex 30 adds 0–1.
- **Native for scale:** toe ext 20 / 12 / 20 / 9 flips; hip flex 13 / 9 / 14 / 10.

Sheet: `v004_deform_*.jpg`.

## 10. Decision options for the author

1. **Accept D5 (+ toe-ring local cost)**, which gives 69 / 69 on all four. Then:
   - freeze `MF_{M,F}_REF_RP3_retopo_v004` by record as the active MPFB Family Base v2 / margin-hardened (v003 = historical v1);
   - Skarn returns PASS — READY FOR AUTHOR FREEZE;
   - promote the standard.
2. **Reject D5.** Then toe2_j1 needs a family-wide toe-1/2 / 2-3 web topology redesign (not a ring, not a Skarn branch) in a further bounded cycle. Hip, heel and toe-3 can be kept as they are.
3. **Keep hip + heel + toe-3 only, drop the toe-2 ring.** That removes about half of the toe slivers and flips. But C1R toe2 stays 1 / 2 even under D5, because the plantar side then reads 1.

## 11. Skarn decision (order §18)

**Not PASS under the accepted validator** (67 / 69, `toe2_j1_l/r`).
- **Not NEEDS RACE-SPECIFIC BRANCH:** the residual is a web-side probe condition at a family toe-2 loop, not a Skarn anatomy feature.
- **Not FAIL:** the issue is not new; it was already the Skarn toe-root residual.

With D5 accepted, Skarn meets every §18 criterion:
- family topology unchanged;
- C1R identity passes;
- T-1, T-2, T-3 and T-7 pass;
- 69 / 69;
- density passes;
- face readiness passes;
- the only new deformation item is the toe-ring local flips.

## 12. Files

**Production** (E: and session outputs; `NOT FROZEN` in the `RAC_status` property). Face topology hash `2bd4c8b3…` for all four:

| File | SHA-256 prefix |
|---|---|
| `MF_M_REF_RP3_retopo_v004.blend` | `398dbd26` |
| `MF_F_REF_RP3_retopo_v004.blend` | `2729750d` |
| `SK_M_REF_RP3_retopo_v002.blend` | `05616b80` |
| `SK_F_REF_RP3_retopo_v002.blend` | `e595a6c6` |

Each comes with its sidecar, `_hm08_map.npz` (identical, `19a83550…`) and landmarks.

**Manifest:** `MPFB_FAMILY_BASE_v004.json` (CANDIDATE).

**Evidence** (`reviews/rac-rp3-evidence/mpfb_family_base_v004/`):
- `maps/`: core, hm08 map, v003 → v004 map, transfer proof;
- `provenance/`: heel rows, rings, pole slides;
- `validator/`, `audit/`, `anatomy/`, `contact/`, `deformation/`, `landmarks/`, `readback/`;
- `sheets/` with all 12 §19 visuals;
- `immutable_hashes_before_after.txt`, `production_files_sha256.txt`.

**Tools:**
- `tools/rac/rp/marchfolk_rp3_v001/`: `val2lib.py` (D4 library; `validator_v2.py` is now its CLI), `v004_lib.py`, `v004_ringsearch.py`, `v004_build.py`, `make_v4cand.py`, `contact_v4.py`; `audit.py` adds density p95.
- `tools/rac/rp/mpfb_family/`: `face_identity.py`, `margin_table.py`, `deform_cmp_v4.py`, `v4_sheets.py`, `family_manifest_v4.py`.

**Standard:** `specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md` (D4 accepted, D5 proposed, successor metrics; still DRAFT).

**STOP FOR CHATGPT REVIEW.** No other race, rig, morph, UV, LOD or UE5 work was started.
