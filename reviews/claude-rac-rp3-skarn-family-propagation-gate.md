# RAC RP3 — Skarn family propagation gate (first MPFB-family reuse validation)

**Date:** 2026-10-26
**Order:** `reviews/chatgpt-rac-rp3-marchfolk-freeze-and-skarn-propagation-order.md` (85b7c1c), Part B
**Part A:** `reviews/claude-rac-rp3-marchfolk-v003-family-base-freeze-report.md`. Marchfolk v003 is frozen and read-back verified.
**Evidence:** `reviews/rac-rp3-evidence/skarn_family_propagation_v001/`
**Draft standard:** `specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md`
**Tools:** `tools/rac/rp/mpfb_family/` (`propagate.py`, `family_sheets.py`, `family_manifest.py`), plus the RP3 tools.

## Result: SKARN FAMILY PROPAGATION NEEDS RACE-SPECIFIC BRANCH

**Recommendation:** treat the remaining items as a **family-base margin correction**, not as a Skarn-only branch.

The frozen family topology transfers to both Skarn configurations unchanged:
- identical face topology hash and identical map;
- C1R face identity is preserved;
- density, face readiness and transfer paths all pass;
- no topology-class deformation failure appears.

It does not clear the hard gates on its own, for two reasons:

1. **Anatomy (configuration 1, SK208-C1R).** T-2 feet maximum is **1.70 mm**, over the 1.5 mm limit. It sits at 2 mirrored vertices only: the hm08 quad centres on the posterior heel / Achilles.
   - These are the linear face-centre rows of the family map.
   - The same vertices are 1.45 mm on Marchfolk configuration 1, already at the margin.
   - Everything else passes: body max 2.05 mm (T-1 3.0); head 1.02, hands 1.07, ears 0.54 mm.
2. **§7 stations.**
   - Under the frozen D1 + D3 validator: configuration 1 has 14 firm failures and configuration 2 has 6.
   - Most of these come from **measurement scale**. The station bands are fixed in cm, and Skarn is 1.20× the Marchfolk reference, so the same topology samples fewer loops. Scaling the station geometry with stature (**proposed D4**) leaves 6 failures (configuration 1) and 2 (configuration 2).
   - What remains after D4:
     - configuration 1: hip_l/r (4 of 5 loops on one side), toe2_j1_l/r (1 of 2), toe3_j1_l/r (an own-toe pole inside the scaled crease band);
     - configuration 2: toe2_j1_l/r (1 of 2).
   - All of these are stations that sit at **exactly** the minimum on the Marchfolk reference (hip 5/5, toe roots 2/2).

None of these is a Skarn anatomy feature that needs different topology. They are zero-margin properties of the family base that tip over on a differently proportioned race. A Skarn-only branch would break shared topology. A family-wide margin update would fix every later race too. Decisions are in §9.

## 0. Answers to the §19 questions

| Question | Answer |
|---|---|
| Did the Marchfolk freeze verify exactly? | **Yes.** Both v003 blends re-stage with the accepted sha256, geometry hash and face hash. Counts, integrity, maps and validator (69/69 D1 + D3) all match. Freeze record `MF_RP3_v003_FREEZE.json` `4af62f81…`, PC read-back identical. |
| Are both Skarn configurations using the frozen family topology unchanged? | **Yes.** 57,674 V / 57,672 Q, face hash `68f7b6a9…`. Map arrays are identical to the frozen map (`hm08_faces_equal`, `src_index_equal`, `frozen_blend_faces_equal_map` all true). There is no per-race fitting. |
| Does C1R identity pass? | **Yes.** The family face lies on the C1R source (head median 0.000 / p95 0.103 / max 1.016 mm). It is **not** on the pre-C1R face, which sits median 1.22 / p95 2.68 mm away; the C1R signal itself is mean 1.65 / p95 3.03 / max 6.24 mm. Source: `anatomy/SK208-C1R_face_identity.json`, sheet `Skarn_face_SK208-C1R.jpg`. |
| Do all anatomy tolerances pass? | **Configuration 2: yes. Configuration 1: no**, by 0.20 mm at 2 heel vertices (T-2 feet). T-1, T-3 and T-7 pass in both (§3). |
| Are all 69 firm stations passing? | **No.** Frozen D1 + D3: 14 (configuration 1) / 6 (configuration 2) failures. Proposed D4: 6 / 2 (§5). |
| Do all density zones pass? | **Yes**, all 9 in both configurations. None is over-dense; see §4. |
| Is face / UFCA readiness intact? | **Yes.** Mouth rings 29 (configuration 1) / 35 (configuration 2), orbit rings 43 + 43. 0 mouth-corner poles, 0 poles within 2 cm of the mouth. Face density 0.133 / 0.129 %. Open pockets are kept. |
| Did any topology-class deformation failure appear? | **No.** Family equals or beats the source topology on zone volume in every pose. The pattern matches the accepted Marchfolk behaviour (§6). |
| Is a Skarn-specific topology branch needed? | **Not for Skarn anatomy.** The residuals are family-base margins (heel quad-centre row; hip and toe-root band margin). The recommended fix is family-wide (§9). |
| Is the propagation process ready to standardise? | **Yes, technically.** The pipeline ran end-to-end with identity proofs; the draft standard is in `specs/`. The validator needs D4 (scale normalisation) before it can be race-invariant. |

## 1. Source regeneration identity

| Configuration | Source | R-6 sha256 | Build sha256 | Committed = regenerated geometry | max \|dV\| | Stature |
|---|---|---|---|---|---|---|
| 1 | SK208-C1R (W3D C1R) | `fd8a43d2…` | `c1c54d28…` | `79f79bad…` ✔ | 0.0 | 208.006 |
| 2 | SKF208 (W2B) | `0245683e…` | `ddf77a84…` | ✔ | 0.0 | 208.009 |

Source hashes are unchanged before and after (`source_hashes_after.txt`). The Skarn hm08 face list, `src_index`, UV layout and 53-bone rig are identical to Marchfolk's.

## 2. Production candidates

Files are in `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Skarn/RP3/`, and the PC read-back is identical.

| File | sha256 | Geometry hash | Face hash |
|---|---|---|---|
| `SK_M_REF_RP3_retopo_v001.blend` (SK208-C1R) | `9d84ea36…` | `53e0733d…` | `68f7b6a9…` |
| `SK_F_REF_RP3_retopo_v001.blend` (SKF208) | `d8084ac7…` | `3c418ae6…` | `68f7b6a9…` |

- Alongside the blends: sidecars, `_hm08_map.npz` (arrays identical to the frozen map), landmark packages, and `SK_RP3_family_propagation_manifest.json` (`644687c4…`).
- **Integrity, both configurations:** 1 component; 0 boundary edges, 0 non-manifold edges or vertices; 0 degenerate faces; outward normals.
- **Self-intersection pairs** (family / source hm08): 54 / 24 (configuration 1) and 94 / 42 (configuration 2). All are source contact: arm–trunk, plus toe contact in configuration 2. The ratio matches the Marchfolk native → v002 increase, because there are 4.3× more faces on the same contact surface.

## 3. Anatomy (each configuration on its own source)

| | Stature Δ | bbox max \|Δ\| | family→source median / p95 / max | head / ears / hands / feet max | source→family max | IoU front / rear / profile L / R |
|---|---|---|---|---|---|---|
| Configuration 1 | −0.51 mm | 0.51 mm | 0.00 / 0.23 / 2.05 | 1.02 / 0.54 / 1.07 / **1.70** | 1.03 | 0.9981 / 0.9981 / 0.9984 / 0.9984 |
| Configuration 2 | +0.00 mm | 0.22 mm | 0.00 / 0.19 / 2.02 | 1.03 / 0.51 / 0.99 / 0.87 | 0.98 | 0.9980 / 0.9980 / 0.9983 / 0.9982 |

- The silhouette canvas now grows to fit 208 cm sources; Marchfolk results are bit-identical under the change.
- **Feet over 1.5 mm: 2 vertices**, at (±15.5, −4.9, 8.8) cm on the posterior heel. Each is the centre row of a strongly non-planar hm08 quad (4 hm08 weights).
- Sheets: `Skarn_overlay_*`, `Skarn_body_*`, `Skarn_face_*`, `Skarn_closeups_*`.

## 4. Density (mean edge / stature, family | source hm08; all pass)

| Zone | Configuration 1 | Configuration 2 | Ceiling |
|---|---|---|---|
| face | 0.133 (0.267) | 0.129 (0.258) | 0.25 |
| ears | 0.098 | 0.098 | 0.25 |
| hands | 0.143 | 0.133 | 0.3 |
| feet | 0.210 | 0.200 | 0.3 |
| trunk | 0.525 | 0.524 | 0.6 |
| arms | 0.480 | 0.446 | 0.6 |
| legs | 0.541 | 0.528 | 0.6 |
| neck | 0.320 | 0.292 | 0.6 |
| head | 0.230 | 0.217 | 0.6 |

- Relative density equals Marchfolk's (same topology, density relative to stature).
- In absolute terms, edges are 1.20× longer.
- No zone is over-dense or heavier than the production target, and nothing was decimated.

## 5. Joint validator (69 stations)

| Validator | Configuration 1 firm fail | Configuration 2 firm fail |
|---|---|---|
| legacy | 15 | 12 |
| **frozen D1 + D3** | **14**: ankle l/r, hip l/r, thumb_mcp l/r, toe1/2/3/4 j1 l/r | **6**: thumb_mcp l/r, toe2_j1 l/r, toe4_j1 l/r |
| D1 + D3 + **D4** (proposed stature scaling) | **6**: hip l/r, toe2_j1 l/r, toe3_j1 l/r | **2**: toe2_j1 l/r |

**Fallback statuses under D4:**
- thumb_mcp_l: `PASS_FALLBACK_CLOSED_RING` (both configurations);
- shoulder l/r (configuration 1) and hip_l (configuration 2): `PASS_FALLBACK_DEFINED_SIDES`;
- toe3_j3 (both configurations): `PASS_FALLBACK_DEFINED_SIDES+SCOPED_ADJACENT_DIGIT_POLE`.

The D4 effect on Marchfolk is nil (scale 0.9998 / 0.9991, still 69/69).

**Residuals under D4:**

| Residual | Configuration | Measured | Required | Reference value (Marchfolk) |
|---|---|---|---|---|
| hip -q side | 1 | 4 | 5 | 5, at the minimum |
| toe2 j1, two sides | 1 and 2 | 1 | 2 | 2, at the minimum |
| toe3 j1 own-toe crease pole | 1 | 1 pole in the D4-scaled crease band | 0 | — |

Strict-only notes are listed in the validator JSONs.

Tables: `sheets/Skarn_validator_{SK208-C1R,SKF208}.jpg` (frozen D1 + D3) and `validator/*_validator_v2_D4.json`.

## 6. Limited deformation (source hm08 → family, same rig and weights)

`deformation/deform_*_{native,fam}.json`, sheet `Skarn_deform_*`.

**Zone volume, family vs source:**
- equal or better in every pose;
- elbow 130: −54 → −48 % (configuration 1) and −37 → −29 % (configuration 2);
- knee 140: −69 → −65 % and −70 → −64 %.

**Counts:**
- in-zone pair, fold and flip counts rise with the 4.3× face count, in the same pattern as the accepted Marchfolk native → v002 result;
- toe flex / extension stay contact / single-ball-bone rig class;
- trunk, neck and ankle are clean.

**Classification:**
- **topology: none;**
- weights: LBS collapse at elbow, knee, hip and shoulder flex;
- contact / setup: fist, wrist, deep knee, toe extension.

The family topology behaves at least as well as the source topology.

## 7. Face / C1R

Sheet `Skarn_face_SK208-C1R.jpg` compares the C1R source and the family in front, 3/4 and profile views, plus the family wire and face rings.

- Identity metrics are in §0.
- No facial component was created, and the face was not redesigned.
- The configuration-2 face matches as well (`Skarn_face_SKF208.jpg`).

## 8. Reusable standard

`specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md` (DRAFT) packages 12 steps:
- regeneration identity;
- hm08 → frozen map;
- helper removal;
- frame;
- topology identity;
- D1 / D3 validator, with D4 proposed;
- density;
- anatomy;
- face;
- deformation;
- visual set;
- manifest / gate.

Tools are in `tools/rac/rp/mpfb_family/`. The race anatomy / identity gate stays a separate author gate. The standard also lists the **known family-base margins** that Skarn exposed.

## 9. Decisions requested

- **D4:** adopt stature-normalised station geometry as part of validator v2. Reference: Marchfolk configuration 1 = 173.143 cm.
- **Family-base margin correction**, recommended instead of a Skarn branch. It would be a v003.1, the same for all races:
  - (a) re-express the 2 posterior-heel hm08 quad-centre rows as on-surface barycentric rows. This is a map-only change; topology is unchanged.
  - (b) add support margin at the hip band and toe-2 / toe-3 roots: one more closed root ring or loop each, mirrored, re-verified on Marchfolk and Skarn.
- **Alternatively**, accept the Skarn residuals as documented exceptions: heel 1.70 mm (+0.20), hip 4/5 on one side, toe2 / toe3 root bands.

Nothing beyond Skarn was started.

## 10. Stop

**STOP FOR CHATGPT REVIEW.** Not started: Sagekin, Fenn, Aelari, Vael, Halvren, Durrim, Pipkin, Cogling, batch propagation, rig, morphs, UV, LOD, UE5.
