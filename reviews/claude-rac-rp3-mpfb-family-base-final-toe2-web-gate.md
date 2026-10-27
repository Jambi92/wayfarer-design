# RAC RP3 — MPFB Family Base final toe-2 web-architecture correction — gate

**Date:** 2026-10-27
**Order:** `reviews/chatgpt-rac-rp3-mpfb-family-base-final-toe2-web-order.md` (33a2dfe)
**Evidence:** `reviews/rac-rp3-evidence/mpfb_family_base_final_toe2/`
**Production candidates:** `E:/…/production/Marchfolk/RP3/` and `E:/…/production/Skarn/RP3/`, with copies in the session outputs.

## Verdict

**FAMILY BASE PASS WITH DOCUMENTED TOE2 EXCEPTION — AUTHOR DECISION.** Nothing was frozen.

The final successor v005 keeps the accepted v004 heel, hip and toe-3 work row for row. It replaces the rejected toe-2 closed ring with a **dorsal racetrack**: a short transverse support loop over the wide dorsal sector of the toe-2 root that never enters the thin plantar / web quads.

What it achieves:

| Gate | Result |
|---|---|
| Validator, D1 + D3 + D4 + D5 | **69 / 69 firm on all four** configurations |
| Toe-2 slivers | No quad with aspect > 10 (v004 had 10–16 per configuration in the patch). Patch aspect max 4.3–4.7 (v004 12.4–16.8). |
| T-4 | +0.05–0.08 pp vs frozen v003 (budget 0.15) |
| Contact | No new pairs |
| Anatomy, C1R identity, density, face | Unchanged |
| Maps / transfer | Pass |

**The exception.** In toe extension 30°, on the two **female** configurations only, the new patch has 3 (MF-F) and 2 (SK-F) flipped faces. They are not explained by a fold of their parent quad, so they count as topology-attributable. Both male configurations have 0, and toe flexion has 0 everywhere. This misses the §13 hard gate of 0.

I used the full candidate budget (TW1–TW3, §7). The only refinement that lowered the count (TW3: 2 / 1) worsened local T-4, so it was not taken (§6).

A finding the author should weigh: when the same fold test is applied to the rejected v004 ring, its toe-extension flips turn out to be parent-quad folds (0 topology-attributable). The ring was rejected for its slivers (still true) and, in part, for flips that this finer test reclassifies.

## Answers to §21

| Question | Answer |
|---|---|
| Are D4 and D5 both implemented as accepted standard rules? | **Yes.** `val2lib.py` / `validator_v2.py --scale-ref 173.143 --d5` is authoritative. D5 sides are excluded as in D1, the status records `+D5_INTERDIGITAL_UNDEFINED`, and every station lists `valid_sides` / `D5_undefined_sides`. Without the flag, verdicts are regression-identical to the earlier outputs. |
| Did toe2 j1 reach valid support on all four? | **Yes.** Loops / minimum: MF-M 2 / 2 (dorsal 3, web side 2), MF-F 3 / 2, C1R 2 / 2 (dorsal; both web sides D5-undefined), SK-F 3 / 2. No own-digit crease pole; no counted single-edge web pseudo-path on Skarn. |
| Did severe toe2/web slivers decrease? | **Yes, to zero.** Aspect > 10 in the toe-2 patch: v004 14 / 10 / 16 / 12 → **0 / 0 / 0 / 0**. Whole mesh, vs the ring-free parent: v004 ring added +14 / +10 / +16 / +12; v005 adds 0. |
| Were topology-attributable toe flips eliminated? | **Not fully.** Toe flexion 0 / 0 / 0 / 0. Toe extension MF-M 0, C1R 0, **MF-F 3, SK-F 2** (§6). |
| Did any new contact appear? | **No.** Rest self-intersection pairs equal v004 (60 / 122 / 54 / 94), and no pair touches a changed vertex. |
| Did all four reach 69/69? | **Yes**, under D1 + D3 + D4 + D5. |
| Did heel/hip/toe3 improvements remain? | **Yes, bit-identical rows.** Feet T-2 0.918 / 0.826 / 1.195 / 0.865 mm. Hip 6 / 15 / 5 / 12. Toe-3 j1 6 / 3 / 3 / 3. The C1R toe-3 crease pole stays cleared. |
| Did anatomy and C1R identity remain valid? | **Yes.** Every T-1 / T-2 / T-3 / T-7 value equals v004. All 124 landmarks are identical. Toe tips, forefoot width and sole contact are unchanged. Patch vertices lie on the source (0.000 mm). The C1R face equals v003 / v004. |
| Did density and face readiness remain valid? | **Yes.** 9 / 9 zones, with means equal to v004. Mouth / orbit rings, corner and eye poles unchanged. |
| Is the final successor ready to freeze as active MPFB Family Base? | **Technically yes, except the toe-extension item.** It needs the author to accept the exception (§9). |
| Is Skarn ready for freeze? | **Tied to the same decision.** C1R meets every §19 / §18 criterion (0 new flips). SK-F carries the 2-face toe-extension item. Both use the shared topology unchanged. |
| Is MPFB Family Propagation Standard v1 ready for acceptance? | **Ready pending this one decision.** It has been updated with D4 + D5 accepted, the v005 metrics, the family margin table and a propagation checklist. Status stays DRAFT because §18 promotion needs every gate. |

## 1. Provenance firewall

Hashes were verified before the work and again before commit. Nothing changed (`immutable_hashes_before_after.txt`):
- the four accepted sources and builds;
- frozen v003 blends, maps and freeze record;
- all v001–v003 files;
- every v004 candidate file and the v004 evidence;
- the PC copies (`pc_readback_sha256.txt`).

## 2. Architecture

**Retained base.** The v004 build without the toe-2 ring: heel rows, hip ring, toe-3 ring and toe-3 pole slides. Their rows are bit-identical to v004.
- Command: `v004_build.py … RINGS_SPEC=hip_support:195:790,toe3_root:508:1264 --relocate-toe3`.
- On this base, Skarn toe2_j1 is 1 / 2 (C1R) on its only D5-valid side, the dorsal one. So toe 2 still needs support there.

**Toe-2 dorsal racetrack** (`tw_build.py`, mirrored):
- **Where it sits.** Around frozen-v003 loop 497 (the loop the dorsal band path crosses).
- **Outbound strip: 497 | 1262**, which the band path crosses. On the dorsum its quads are long along the toe (ratio 0.4–0.8), so splitting makes them squarer.
- **Return strip: 497 | 1119**, the distal neighbour.
- **Span.** Loop edges at ≥ 100° from plantar, plus one corner-turn quad at each end of each strip.
- **Turns.** Each is a 3-quad turn: one valence-3 centre plus one valence-5 corner.
  - 4 + 4 poles per toe.
  - All lie at |axial| ≥ 1.2 local loops from the toe2_j1 plane on every configuration, well outside the 0.5-loop crease window.
- **Size.** +18 V per side; 57,842 V / 57,840 Q in all.
- **On-surface rows.** New vertices are rung / loop-edge midpoints and turn centres re-expressed as on-surface barycentric rows (36 / 36).
- **Turn optimisation.** Each turn's centre, valence-5 corner and joined midpoints were slid on the reference surface (Powell) to reduce angle and aspect excess across all four configurations. 8 valence-5 corners moved ≤ 2.0 mm along the surface (row class 7).

## 3. Candidates (order §7)

Commands and results: `provenance/TW_candidates.json`.

| Candidate | What | Result |
|---|---|---|
| TW1 | sector 110°, no optimisation | **Rejected.** C1R own-digit crease pole: a turn corner at 0.42 local loop. Turn angles 24–157°. |
| **TW2** | sector 100° (turns out of the crease window) + per-turn optimisation | **Selected.** 69 / 69 × 4, patch aspect ≤ 4.7, residual female toe-extension flips 3 / 2. |
| TW3 | TW2 with the return-strip split moved toward loop 497 (`--dfrac 0.35`) | **Rejected.** Flips 2 / 1, but toe-2 region T-4 +4–6 and aspect p95 4.7–5.0. Still not 0. |

Refinements tried inside TW2 and rejected (disclosed):
- tangential fairing: no gain, and the plantar toe-2 count fell 3 → 2;
- quad-centroid smoothing: more angle violations;
- a wider optimisation neighbourhood: asymmetric, worse on MF-M / C1R;
- a hard 45–135° penalty / 3 passes: more violations.

## 4. Validator (D1 + D3 + D4 + D5 authoritative)

Files:
- `validator/*_v005_validator_v2{,_D4,_D4_D5}.json`;
- `audit/MPFB_FAMILY_v005_margin_table.{json,csv}`, giving loops, minimum, margin, mode, valid / undefined sides and pole ownership per station;
- sheet `v005_validator_D5.jpg`.

| | MF-M | MF-F | SK-C1R | SK-F |
|---|---|---|---|---|
| Firm, D1 + D3 + D4 + D5 | **69** | **69** | **69** | **69** |
| Firm, D1 + D3 + D4 (reference only) | 69 | 69 | 67 | 67 |

**At margin 0 in all four:** `toe1_j1_l/r`. **Elsewhere:**
- MF-M: `thumb_mcp`, `toe2_j1`, `toe2_j2`, `toe4_j1`;
- MF-F: `toe4_j1`;
- C1R: `hip`, `thumb_mcp`, `toe2_j1`, `toe4_j1`.

## 5. Local quality (order §12)

Files: `audit/MPFB_v005_toe2_local_audit.json` and `T4_union_v003_tw0_v004_v005.json`; sheets `v005_T4_local_*`, `v005_aspect_*`, `v005_pole_valence_*`.

**Toe-2 patch, v004 ring → v005 racetrack:**

| | MF-M | MF-F | SK-C1R | SK-F |
|---|---|---|---|---|
| T-4 quads | 52 → **28** | 62 → **28** | 52 → **30** | 56 → **26** |
| aspect > 10 | 14 → **0** | 10 → **0** | 16 → **0** | 12 → **0** |
| aspect max | 12.4 → **4.7** | 16.8 → **4.3** | 12.4 → **4.7** | 16.0 → **4.3** |
| aspect p95 | 11.7 → **4.6** | 11.3 → **4.2** | 11.7 → **4.6** | 11.5 → **4.2** |
| angle violations | 22 → 24 | 36 → 24 | 22 → 26 | 30 → 24 |

- **Angle extremes.** They come from existing web-root quads next to the turn corners: the ring-free parent already has minima of 20.9 / 23.9 / 21.1 / 27.8°, unchanged in v005. The new violations are the corner-turn quads, which carry an inherent ~45° split at the valence-5 corner. That is the justified cost of terminating a support loop with quads only.
- **Whole-mesh T-4 union added over the ring-free parent:** v004 ring +30 / +42 / +30 / +36; v005 +6 / +12 / +8 / +8.
- **v005 vs frozen v003:** +0.084 / +0.061 / +0.082 / +0.054 pp (budget 0.15).

## 6. Deformation (order §13)

Files:
- `deformation/MPFB_v005_deformation_comparison.json` (native | v003 | v004 | v005);
- `MPFB_v005_flip_parentage.json` and `MPFB_v004_ring_vs_tw0_flip_fold.json`;
- sheet `v005_toe_deform_*`.

**Family poses.** Shoulder abd 90, elbow 90, fist, hip flex 90 and knee 90 / 140 are **identical to v004** on all four. Ankle dorsiflexion 20 gives 0 flips everywhere.

**Toe flexion 30:** 0 new flips on all four.

**Toe extension 30:** new flips are faces whose ring-free parent face did not flip.

| | MF-M | MF-F | SK-C1R | SK-F |
|---|---|---|---|---|
| New flips | 0 | 9 | 0 | 8 |
| Parent-quad folds | – | 6 | – | 6 |
| **Topology-attributable** | **0** | **3** | **0** | **2** |

- A **parent-quad fold** is a fold the parent quad already makes in the posed parent mesh, seen at finer resolution: LBS crease, rig class.
- The **topology-attributable** faces are on the D-strip return turn / split and one X turn at the lateral end of the racetrack.
- They sit inside the known toe-extension MTP crease, where frozen v003 already shows 50–71 flips against 12–20 native: single-ball-bone LBS.
- SK-F toe extension also shows self-intersection pairs 8 → 12 and folds 12 → 15 vs v004.
- **Same test on the rejected v004 ring:** MF-F 6 new, SK-F 6 new, **all parent folds** (0 topology-attributable).

## 7. Anatomy, contact, maps (order §8 / §9 / §14)

**Anatomy.** All four pass, and every zone maximum equals v004:
- feet T-2 0.918 / 0.826 / 1.195 / 0.865 mm;
- stature diff −0.415 / 0.000 / −0.508 / 0.000 mm;
- min IoU 0.99730 / 0.99747 / 0.99810 / 0.99804.

**Foot detail:**
- toe-tip shift v004 → v005: 0.000 mm on all toes;
- forefoot width unchanged (9.44 / 9.37 / 11.99 / 11.82 cm);
- sole minimum and contact counts unchanged;
- source → production near the patch equals v004;
- MTP / IP joints are rig-defined and unchanged.

**Contact.** `contact/*_v005_contact_vs_v004.json`: 0 new pairs, and 0 pairs touching changed vertices.

**Maps** (`maps/`):

| Map | SHA-256 prefix | Notes |
|---|---|---|
| hm08 → v005 | `e690fbaf…` | row sums 1, no negative weights, support ≤ 4 |
| v003 → v005 | `928bec17…` | |
| v004 → v005 | `cdb401a1…` | exact for 57,802 rows |

- 57,798 of the 57,806 retained rows are identical to v004.
- Weights: sums 0.9999–1.0000, identical on the unchanged rows.
- UVs: unchanged faces identical; 0 new seam vertices from the racetrack.
- MPFB targets: linear to 6e-14 cm.
- Every new vertex carries parents in `provenance/MPFB_FAMILY_v005_toe2_racetrack.json`.

**Read-back** of all four blends is exact.

## 8. Face / density / regression (order §15)

- Face rings and poles are unchanged: mouth 35 / 35 / 29 / 35, orbits 43 / 43, corner poles 0.
- C1R face → C1R source median 0.000 / p95 0.089 / max 1.016 mm; → pre-C1R median 1.10 mm.
- Density is 9 / 9, with means equal to v004.
- Hand, shoulder and face topology are unchanged.

## 9. Decision for the author

1. **Accept the exception** (3 / 2 female toe-extension faces inside the known MTP crease). Then:
   - freeze v005 by record as **ACTIVE MPFB FAMILY BASE — MARGIN-HARDENED FINAL** (v003 historical v1; v004 provenance);
   - Skarn returns SKARN FAMILY PROPAGATION PASS — READY FOR AUTHOR FREEZE;
   - promote the standard.
2. **Take TW3 instead:** 2 / 1 flips, at a small local T-4 cost (+4–6 quads per configuration).
3. **Treat it as rig class.** The fold test says most of the female toe-extension flipping is LBS crease folding. A later rig / weight stage (not authorised here) is where it would be fixed.

## 10. Files

**Production** (E: and outputs; `RAC_status` NOT FROZEN). Face hash `ec768ae2…` for all four:

| File | SHA-256 prefix |
|---|---|
| `MF_M_REF_RP3_retopo_v005.blend` | `e560386c` |
| `MF_F_REF_RP3_retopo_v005.blend` | `f2f2f9dc` |
| `SK_M_REF_RP3_retopo_v003.blend` | `76229b35` |
| `SK_F_REF_RP3_retopo_v003.blend` | `4ff0ce6f` |

Each has its sidecar, hm08 map and landmarks. Manifest: `MPFB_FAMILY_BASE_v005.json`.

**Sheets** (§17, `sheets/`):
- `v005_toe2_topology_*` (dorsal / plantar / toe-1/2 web / toe-2/3 web, v004 vs v005);
- `v005_pole_valence_*`, `v005_validator_D5`, `v005_T4_local_*`, `v005_aspect_*`;
- `v005_source_deviation_*`, `v005_toe_deform_*`, `v005_retention_*`;
- `v005_change_diagram`, `v005_C1R_face`, `v005_body_*`.

**Tools:**
- `marchfolk_rp3_v001/`: `tw_build.py`, `make_v5cand.py`; `val2lib.py` / `validator_v2.py` (D5 accepted, `--d5`); `v004_build.py` (`RINGS_SPEC`); `v004_ringsearch.py` (`--base`, `--d5`).
- `mpfb_family/`: `toe2_local_audit.py`, `deform_cmp_v5.py`, `v5_sheets.py`, `family_manifest_v5.py`.

**Standard:** `specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md` (D4 + D5 accepted, v005 metrics, margin table, propagation checklist; DRAFT pending §9).

**STOP FOR CHATGPT REVIEW.** No other race, rig, morph, UV, LOD or UE5 work was started.
