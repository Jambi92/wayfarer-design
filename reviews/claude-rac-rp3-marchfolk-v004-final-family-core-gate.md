# RAC RP3 — Marchfolk v004 final family-core gate (toe-IP reroute / D1 validator)

**Date:** 2026-10-26
**Order:** `reviews/chatgpt-rac-rp3-marchfolk-v004-final-toe-reroute-order.md` (2d34a0c)
**Parent:** v003, `reviews/claude-rac-rp3-marchfolk-family-core-v003-gate.md` (29321e2)
**Evidence:** `reviews/rac-rp3-evidence/marchfolk_v004_final_family_core/`. Unchanged v003 measurements stay in `reviews/rac-rp3-evidence/marchfolk_family_core_v003/`.
**Tools:**
- `tools/rac/rp/marchfolk_rp3_v001/validator_v2.py`: D1 fallback, plus proposed D3.
- `mf4_sheets.py`.
- `mf_deform.py`: adds toe flexion / extension poses.

## Result: FAMILY BASE PASS WITH DOCUMENTED TOE-IP EXCEPTION — READY FOR AUTHOR DECISION

**v003 is returned as the freeze candidate. No v004 was produced.**

- **D1 is implemented as ordered.** Under it, thumb MCP (both configurations) and both configuration-2 shoulders pass, reported as fallback passes.
- **The D2 premise does not hold.** The toe-IP "crease poles" (toe3 j3 in both configurations, toe4 j2 in configuration 2) are not on the toe being audited.
  - Each one is a valence-3 tip-cap pole of the neighbouring toe:
    - toe3 j3 picks up a pole of **toe 4**;
    - toe4 j2 picks up a pole of **toe 5**.
  - Each pole lies 0.26–0.58 cm from its own toe's axis and 1.04–1.29 cm from the audited toe's axis.
  - The validator counts them because the toe-station pole radius (1.0–1.5 cm) is larger than the spacing between toes.
  - On the audited toes themselves, there are **0 crease poles and 0 poles within 2 loops**.
- **No topological reroute is applicable.** There is no pole on the toe-3 or toe-4 tube to reroute.
  - The only way to clear the flagged pole is to rework the neighbouring toe's tip cap.
  - A quad-mesh disc cap requires its four valence-3 poles. Each flagged pole is one of a group of 4 on its owning toe (`toe_ip_pole_attribution.json`).
  - Reworking the cap is outside the authorised scope: §6 says preserve toe-pad and nail-region flow, and §3 says no other station.
  - The v003 relocation trials, which moved exactly these poles, created 16–326 new contact pairs.
- **Decision needed (D3, proposed).** For digit stations, scope crease poles to the station's own digit. Under D1 + D3, **both configurations have 0 firm failures across all 69 stations**. The only strict-only items left are middle / ring MCP poles 1.7–2.0 loops off the crease.

## 0. Answers to the §16 questions

| Question | Answer |
|---|---|
| Did D1 fallback stations pass? | **Yes.** thumb_mcp_l in both configurations: `PASS_FALLBACK_CLOSED_RING` (all four band sides undefined; 3 / 4 closed rings at the 3.0 cm thumb radius, 3 required). Configuration-2 shoulder_l and shoulder_r: `PASS_FALLBACK_DEFINED_SIDES` (defined-side minimum 7 and 7, 5 required). |
| Were the toe-IP poles successfully rerouted? | **No reroute was performed, because none is applicable.** The flagged poles belong to the neighbouring toes' tip caps (§2). The audited toe tubes carry no crease pole. |
| Were any new self-intersections introduced? | **No.** v003 geometry is unchanged: 60 (configuration 1) / 122 (configuration 2) pairs, all accepted source contact. |
| Are both configurations on identical topology? | **Yes**, v003 shared topology: 57,674 V / 57,672 Q, face hash `68f7b6a9…`, identical maps. |
| Are all true mandatory stations now passing? | Under D1 alone (authorised): all pass except the four toe-IP stations, which fail only on adjacent-digit poles. Under D1 + D3 (proposed): **all 69 pass firm in both configurations.** |
| What fallback-pass stations remain? | `PASS_FALLBACK_CLOSED_RING`: thumb_mcp_l (configurations 1 and 2). `PASS_FALLBACK_DEFINED_SIDES`: configuration-2 shoulder_l and shoulder_r. Under D3 also `…+SCOPED_ADJACENT_DIGIT_POLE`: toe3_j3_l/r (both configurations) and toe4_j2_l/r (configuration 2). |
| What T-4 change occurred? | **None.** There is no geometry change from v003: 4.03 % (configuration 1) and 3.94 % (configuration 2). |
| Did anatomy remain within tolerance? | **Yes** (v003 values unchanged). T-1, T-2, T-3 and T-7 pass in both configurations. Noted below: configuration-1 sole contact. |
| Did density remain valid? | **Yes**, all 9 zones in both configurations (unchanged). |
| Did face readiness remain valid? | **Yes**, unchanged: mouth rings 35, orbits 43 + 43, 0 mouth-corner poles. |
| Did any new topology-class deformation failure appear? | **No.** The new toe flexion / extension diagnostic matches v002 (§5). The sanity set matches v003. |
| Is the family base ready for freeze? | **v003 is ready for freeze, subject to author acceptance of D3** (or of the toe-IP items as documented exceptions). |
| If the toe reroute failed, is v003 ready with a documented exception? | **Yes.** The exception is a validator attribution issue, not a mesh defect. The audited toes have no crease pole. |

## 1. D1 validator — standardised (`validator_v2.py`)

The band and ring maths are identical to `audit.py`. The legacy verdict reproduces `audit.py` exactly for both configurations.

**Rules:**
1. **Defined sides.** A band side is *undefined* when no vertex in the ray-exit probe ball faces the side direction (normal · side ≤ 0.3 for every candidate). The legacy method then picks an endpoint by tie order. Undefined sides are excluded, and the band minimum uses defined sides only. A pass produced this way is reported as `PASS_FALLBACK_DEFINED_SIDES`.
2. **Closed-ring fallback.** If no side is defined, the station uses the literal closed-ring test with an anatomical radius. For thumb MCP that is 3.0 cm, the thenar cross-section; every other station keeps its station radius. A pass produced this way is reported as `PASS_FALLBACK_CLOSED_RING`.
3. **Reporting.** Fallback statuses are always reported separately from plain `PASS` and from failures. No geometry was modified for D1.

**Results** (`validator/MF-{M,F}-R_v003_validator_v2.json`; tables in `sheets/MF4_validator_{M,F}.jpg`):

| | Legacy firm fail | D1 firm fail (authorised) | D1 + D3 firm fail (proposed) | D1 + D3 strict fail |
|---|---|---|---|---|
| Configuration 1 | thumb_mcp_l, toe3_j3_l/r | toe3_j3_l/r | **none** | middle_mcp_l/r, ring_mcp_l/r |
| Configuration 2 | shoulder_l/r, thumb_mcp_l, toe3_j3_l/r, toe4_j2_l/r | toe3_j3_l/r, toe4_j2_l/r | **none** | ring_mcp_l/r |

## 2. Toe-IP residuals — the flagged poles are on the neighbouring toes

Source: `toe_ip_pole_attribution.json` and `sheets/MF4_toe_attribution_{M,F}.jpg`. In the sheets, faces are tinted by their owning toe, the station's crease slab is red, and the flagged poles are yellow.

| Configuration | Station | Flagged pole (valence) | Distance to owning-toe axis | Distance to audited-toe axis | Owning toe | Valence-3 poles in the owning toe's cap group |
|---|---|---|---|---|---|---|
| 1 | toe3_j3_l / r | 12629 / 6032 (3) | 0.38 cm | 1.29 cm | toe 4 | 4 |
| 2 | toe3_j3_l / r | 12629 / 6032 (3) | 0.58 cm | 1.28 cm | toe 4 | 4 |
| 2 | toe4_j2_l / r | 13188 / 6592 (3) | 0.26–0.27 cm | 1.04–1.05 cm | toe 5 | 4 |

- **Audited toes:** 0 own-toe crease poles and 0 own-toe poles within 2 loops. Loops are 5–6 against 2 required.
- **The crease slab** (|axial| ≤ 0.5 loop, radius = station pole radius 1.35–1.5 cm) reaches across the web into the neighbouring toe's tip cap. That cap sits at the same axial level because the toes are staggered.
- **Why a topological reroute is not the fix:**
  - A closed quad cap must carry four valence-3 vertices, by the Euler characteristic of a disc.
  - Rerouting would mean moving the neighbouring toe's tip-cap poles distally into the nail cap or proximally into that toe's own IP region. That changes the owning toe's tip / nail flow (§6) and another station (§3). It also cannot clear the slab without moving the cap beyond its own toe tip.
  - The v003 trials moved exactly these vertices (5 displacement variants, 2 directions, 2 projection modes). Every trial produced 16–326 new self-intersecting face pairs in the 0.7–1.2 mm toe / web gap.
  - Per §7 ("If every plausible reroute introduces new self-intersections, STOP … Do not solve it by changing anatomy"), no v004 is produced.

### Proposed D3: digit pole ownership

For finger, thumb and toe stations, count a pole as a station crease pole only when its nearest digit axis is the station's own digit. The axes are bone or joint chains on the same hand or foot, with the toes extended to the tip.

- This is analogous to D1: a measurement-scope correction, not a geometry change.
- It removes exactly the 6 toe-IP failures above.
- It changes no other station's firm verdict, and no hand station's.

## 3. Topology / valence / pole audit

There is no topology change: v003 is unchanged.
- Poles: 164 valence-3 / 156 valence-5+.
- Changed vertices, faces and poles: **0**.
- Local valence map at the flagged sites: `sheets/MF4_toe_attribution_{M,F}.jpg`. Black marks poles; each toe tip shows its 4-pole cap.
- Family-core topology summary (v002 → v003 junction changes): `reviews/rac-rp3-evidence/marchfolk_family_core_v003/sheets/MF3_core_diagram.jpg`.

## 4. Contact / anatomy / density / T-4 / mapping / face

All unchanged from v003. Evidence: `marchfolk_family_core_v003/` (`audit/`, `anatomy/`, `v3_report.json`, `mapping/`, sheets `MF3_body`, `MF3_overlay`, `MF3_quality`, `MF3_density`, `MF3_closeups`).

- **Self-intersection pairs:** 60 / 122 (v002 68 / 122). There are 0 hand / foot pairs in configuration 1 and the source baseline of 12 in configuration 2.
- **Anatomy:** T-1, T-2, T-3 and T-7 pass in each configuration.
  - Production → source max 1.76 / 2.00 mm.
  - Source → production max 0.78 / 0.79 mm.
  - IoU ≥ 0.9973.
- **Toe-specific checks:** no geometry change, so the following are all v003 values:
  - toe tips are pinned surface-fit landmarks (drift ≤ 0.0007 mm);
  - MTP and IP positions are source-joint landmarks, unchanged;
  - web boundaries and forefoot width: production → source on the feet is max 1.45 / 0.83 mm (identity zone T-2 ≤ 1.5 mm).
- **Sole contact** (`foot_ground_contact.json`):
  - Configuration 2: v003 equals v002 (lowest point 0.000 mm; 10–11 vertices within 1 mm).
  - **Configuration 1:** the v003 lowest sole point sits **0.41 mm above ground**, with 6–8 vertices within 1 mm against v002's 11. This comes from the v003 ankle / sole pole relocation sliding the lowest heel vertex along the surface. It is inside T-3 (stature −0.41 mm, limit ±1 mm), and the sole stays flat-capable. I am recording it as a note for the freeze decision; it is not a defect.
- **Density:** all 9 zones pass.
- **T-4:** 4.03 / 3.94 % (v002 6.61 / 6.26 %).
- **Face:** unchanged.
- **Mapping:** hm08 → v003 and v002 → v003 maps are identical for both configurations. Weight, UV and morph transfer paths are as documented in the v003 gate §2.

## 5. Deformation sanity (§12)

Source rig and weights through the v003 map: `deformation/deform_MF-{M,F}-R_v003_sanity.json`. Toe poses for native and v002: `deform_*_{native,v002}_toe.json`.

| Pose | Configuration 1: native / v002 / v003 (in-zone self-x · folds · flips) | Configuration 2: native / v002 / v003 |
|---|---|---|
| toe flexion 30° (ball bone) | 0·1·0 / 0·0·0 / 0·1·0 | 25·16·11 / 54·30·40 / 58·26·42 |
| toe extension 30° | 31·23·20 / 87·48·76 / 85·41·64 | 22·16·12 / 73·23·47 / 74·25·50 |
| ankle dorsiflexion 20° | 0 / 0 / 0 | 0 / 0 / 0 |

- **Toe flexion / extension** is a contact / rig-class result:
  - the MPFB game_engine rig has a single ball bone for all toes;
  - inter-toe and big-toe web contact appears in native too;
  - counts scale with the 4.3× face count from v002 onward.
- **v003 ≈ v002**, so there is no topology-class change.
- **The sanity set** (shoulder abd90, elbow 90, fist, hip flex90, knee 90) reproduces the v003 values exactly.
- **Sheets:**
  - `sheets/MF4_toe_deform_{M,F}.jpg` (native | v002 | v003);
  - `marchfolk_family_core_v003/sheets/MF3_deform_{M,F}.jpg` (whole-body set).

## 6. Hashes (§1)

Before and after this order, everything is identical (`hashes_after.txt`, also checked before the work started).

| Item | sha256 (prefix) |
|---|---|
| MF-M-R R-6 | `2caaf056…` |
| MF-F-R R-6 | `c254fb4b…` |
| MF-M-R build | `c5be9ca0…` |
| MF-F-R build | `252907fd…` |
| v001 blends | `0c2b13c9…` / `2ad7dcb5…` |
| v002 blends | `c02f77bf…` / `9f228ad1…` |
| v003 blends | `5b793eda…` / `a5d8adfe…` |
| v002 map | `28d4e46e…` |
| v003 map | `bc3b7c54…` |
| v002 → v003 map | `0829d1dc…` |

The PC re-stage of both v003 blends gives identical hashes.

## 7. Visual evidence (§15)

| # | Item | File |
|---|---|---|
| 1–2 | Toe dorsal / plantar wire with attribution | `sheets/MF4_toe_attribution_{M,F}.jpg` (dorsal, plantar, front, lateral). There is no v004, so there is no v003-vs-v004 pair. |
| 3 | Pole / valence | same sheets (black poles, yellow flagged, 4-pole tip caps visible) |
| 4 | Crease ring / slab | same sheets (red slab) |
| 5 | Web / contact | `MF4_toe_attribution_*` front and lateral views; `MF4_toe_deform_*` |
| 6 | Local source deviation | `marchfolk_family_core_v003/sheets/MF3_overlay_{M,F}.jpg` (unchanged) |
| 7 | T-4 foot heat | `marchfolk_family_core_v003/sheets/MF3_quality_{M,F}.jpg` (unchanged) |
| 8 | Foot / toe deformation | `sheets/MF4_toe_deform_{M,F}.jpg` |
| 9 | Whole body | `marchfolk_family_core_v003/sheets/MF3_body_{M,F}.jpg` |
| 10 | Family-core summary | `marchfolk_family_core_v003/sheets/MF3_core_diagram.jpg`, plus the validator tables `sheets/MF4_validator_{M,F}.jpg` |

## 8. Decisions requested

- **Freeze candidate:** `MF_{M,F}_REF_RP3_retopo_v003` (unchanged).
- **D3:** accept digit-ownership pole scoping. That makes all 69 stations firm-PASS in both configurations. Alternatively, accept the 4 / 6 toe-IP station entries as documented validator-attribution exceptions.
- **Note:** configuration-1 sole lowest point is +0.41 mm, within T-3. Accept, or authorise a one-vertex sole re-pin in a later cycle.

## 9. Stop

**STOP FOR CHATGPT REVIEW.** Nothing is frozen. Not started: Skarn, Sagekin, propagation, rig or weights, morphs, UV / materials, LODs, UE5.
