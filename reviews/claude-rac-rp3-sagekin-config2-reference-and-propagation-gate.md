# RAC RP3 — Sagekin configuration-2 central reference + MPFB family propagation — gate

**Date:** 2026-10-27
**Order:** `reviews/chatgpt-rac-rp3-sagekin-config2-reference-and-propagation-order.md` (c6c7940)
**Evidence:** `reviews/rac-rp3-evidence/sagekin_rp3_v001/`
**Tools:** `tools/rac/rp/sagekin_rp3_v001/` (new); standard pipeline in `tools/rac/rp/marchfolk_rp3_v001/` and `tools/rac/rp/mpfb_family/`
**Production candidates (NOT FROZEN):** `E:/…/RaceBodies/production/Sagekin/RP3/`

## Results

**Part A: SG CONFIG-2 CENTRAL REFERENCE PASS — READY FOR PROPAGATION.** `SGF178`, 178.00 cm. Part B was run.

**Part B: SAGEKIN NEEDS AUTHOR DECISION — VALIDATOR RULE D6 (proposed). No race-specific branch is needed.**

None of the order's three §20 returns fits exactly, so I am reporting the mismatch rather than forcing one:
- **PASS** needs 69 / 69 on both configurations. Configuration 1 (SG) scores **67 / 69** under the authoritative validator (D1 + D3 + D4 + D5). The two fails are `hip_l` and `hip_r`, at 4 loops where 5 are needed.
- **NEEDS RACE-SPECIFIC BRANCH** does not apply. The hip topology is not at fault. The failing band side does not measure the hip: its probe lands on the **forearm** hanging beside the hip in the R-6 stance (§B3).
- **FAIL** does not apply. Sources, propagation, topology identity and every other gate pass.

What each ruling leads to:
- **D6 accepted:** SG scores 69 / 69 (hip 6 / 5). The result becomes **SAGEKIN FAMILY PROPAGATION PASS — READY FOR AUTHOR FREEZE.**
- **D6 rejected:** the family topology needs one more loop under SG's forearm-band sample. A diagnostic ring search found single-ring options that make all six configurations firm (§B3). That would be a Sagekin branch or a family v006, and would need a new order.

**Nothing was frozen, and no topology was changed.**

---

# PART A — configuration-2 central reference

## A1. Provenance (§5)

An existing local `SGF178` was found, committed with the reference assets in 7a7b016:
- `reviews/reference-assets/r6/SGF178_r6.npz`, sha `52ff5e04…`
- `reviews/reference-assets/builds/SGF178_build.json`, sha `7f502543…`
- manifest role: "configuration-2 construction base for SGF152-NAT / SGF208 (not itself accepted as a reference)"

It was not assumed accepted because it exists. It was checked against canon:

| | |
|---|---|
| Built in | RM-OT-05 §4 / RM-OT-05A (`claude-rac-rm-ot-05-visual-readability-closure-gate.md` §4) |
| Route | `tools/rac/w1/build_variant.py`, "height macro re-solved" |
| Base | accepted `MF-F-R_build.json` |
| Overrides | exactly the accepted Sagekin targets used by configuration-1 `SG`: upper/lower-leg height +0.12, nape-to-waist −0.15, torso depth −0.20, lower-arm length +0.20, finger length +0.25, hand scale +0.05, finger diameter −0.20 |
| Stature | 178.0, `resolve_stature` |
| MPFB / Blender | 2.0.17 / 5.2.2 LTS (`arm_lib.py`) |
| cfg | gender 0.0, age 35 (0.5769), muscle 0.5, weight 0.5, proportions 0.5 |
| Height macro | **0.630126953125**, 12 solver iterations |
| Pose | build → ground → `pose_r6` (arm abduction 8°, palm twist ±0.04°) → ground |
| Stature R-6 | **178.0013 cm** |

**This is the canonical configuration-2 architecture, not an interpolation between the two bounds.**
- SGF208 is the same route at 208 cm.
- SGF152-NAT is the native short-adult route started *from SGF178's height macro*; its record has `base_height_macro` 0.630126953125.
- So both accepted bounds were built from this body.

**No second plausible central build exists.** The only alternative route, "height macro held from MF-F-R", gives a 173 cm body, not the 178 cm reference. So **NEEDS AUTHOR DECISION does not apply**.

Full record: `partA/…` and `SGF178_central_reference_sidecar.json` (also copied to E:).

## A2. Rebuild identity (deterministic)

| Rebuild | Geometry identical | max \|dV\| |
|---|---|---|
| `regen.py` (recorded macro) | **yes** (sha256 float32 V + int32 F) | **0.0** |
| Full height re-solve from scratch (`build_variant.py`, MF-F-R + overrides) | **yes**; height macro re-solved to exactly 0.630126953125; cfg and pose equal | **0.0** |

Geometry hash: `7755a8f0…`.

`run_candidate.py` on the from-scratch rebuild reproduces the committed `SGF178_meas.json` ratios exactly (max diff 0.0).

## A3. Geometry integrity (native hm08 body, helpers removed)

| | SGF178 | SG (c1, accepted) | MF-F-R (accepted) |
|---|---|---|---|
| V / Q | 13,380 / 13,378 | same | same |
| Components | 1 | 1 | 1 |
| Boundary / non-manifold edges | 0 / 0 | 0 / 0 | 0 / 0 |
| Orientation-inconsistent edges | 0 | 0 | 0 |
| Degenerate faces / coincident vertices | 0 / 0 | 0 / 0 | 0 / 0 |
| Signed volume (left-handed frame; negative = outward) | −60.3 L | −65.0 L | −57.7 L |

## A4. Stature and envelope

| Body | Stature (cm) |
|---|---|
| SGF152-NAT | 152.00 |
| **SGF178** | **178.00** |
| SGF208 | 208.01 |
| SG (c1) | 177.99 |

SGF178 sits at the canonical 178 cm reference (`SAGEKIN_V1` §2 / §10: 178 for both configurations), inside the 152–208 envelope.

**20 stature-normalised shares** (`partA/SGF178_reference_validation.json`; sheet `Sagekin_config_comparison`):
- **16 / 20** lie inside [SGF152-NAT, SGF208]. Most sit near mid-envelope (position 0.4–0.6): head, shoulders, ribcage depth, pelvis.
- **3** are torso share +0.43 %, forearm / arm +0.7 % and foot −0.44 % outside the range. **The accepted configuration-1 triple SG152-NAT / SG / SG208 shows exactly the same pattern.** The 152 bound is a different (native short-adult) allometry, so shares are not monotone in stature.
- **1** is thorax depth / breadth, −1.22 % below the range. Its two components (thorax breadth, position 0.38; thorax depth, 0.53) are both inside. The ratio is outside only because SGF208's ratio rises at 208.

**Configuration consistency.** The c2 − c1 differences at 178 cm (SGF178 − SG) agree in sign with Marchfolk's own c2 − c1 (MFF178 − MFM178) on **20 / 20** shares.
- Most agree within 0.1 %.
- The largest disagreements are thorax breadth (−8.4 vs −10.3 %) and thorax depth / breadth (+1.6 vs +4.7 %).

## A5. Race identity at matched stature (no exaggeration)

MFF178 and MFM178 are diagnostic comparators only: the accepted MF-F-R / MF-M-R builds with stature re-solved to 178. They are not reference assets.

| Share of stature | c2: SGF178 − MFF178 | c1: SG − MFM178 | RM-OT-05 c2 at 152 / 208 |
|---|---|---|---|
| torso | −1.93 % | −1.95 % | −2.37 / −1.95 |
| leg | +1.36 % | +1.34 % | +1.85 / +1.53 |
| arm | +2.61 % | +2.48 % | +2.99 / +2.44 |
| head | −0.61 % | −0.60 % | −0.64 / −1.20 |
| hand | +5.45 % | +4.95 % | +5.74 / +4.61 |
| thorax depth | −3.83 % | −2.96 % | −3.31 / −3.53 |
| shoulder | −0.60 % | −0.60 % | −1.20 / −1.18 |
| span | +1.97 % | +1.85 % | +2.14 / +1.76 |

- **8 / 8** signs match the accepted bound rows, and magnitudes lie in their range.
- This is a plausible Sagekin tendency with intended human overlap: slightly longer limbs, slightly shorter torso, shallower ribcage.
- Human hands, feet and auricle (MPFB hm08) are kept. There is no caricature and nothing elf-like (sheet `Sagekin_vs_Marchfolk_178`).

**Part A verdict: PASS — READY FOR PROPAGATION.**

---

# PART B — Sagekin family propagation

## B1. Sources and topology identity (§10, §11)

| | SG (c1) → `SG_M_REF_RP3_retopo_v001.blend` | SGF178 (c2) → `SG_F_REF_RP3_retopo_v001.blend` |
|---|---|---|
| Source regen | identical, max \|dV\| 0 (R-6 `fe45866f…`) | identical, max \|dV\| 0 (`52ff5e04…`) |
| File sha | `bb156e9c…` | `0ef62ffc…` |
| Geometry hash | `56a73d8f…` | `9dcc5000…` |
| Face topology hash | **`ec768ae2…` = family** | **`ec768ae2…` = family** |
| V / Q, quads | 57,842 / 57,840, 100 % | 57,842 / 57,840, 100 % |
| Components / boundary / non-manifold E, V / degenerate | 1 / 0 / 0, 0 / 0 | 1 / 0 / 0, 0 / 0 |
| Normals | outward | outward |
| Face list / UVs = family base | yes / yes | yes / yes |
| hm08 map | byte-identical to the family map `e690fbaf…`; arrays equal | same |
| V = M @ Sagekin hm08 | max error **0.0** | **0.0** |
| Blender read-back | ≤ 6e-8 m from candidate | ≤ 6e-8 m |

- PC copies were read back: sha256 identical (`pc_readback_sha256.txt`).
- No fitting, no relaxation, no topology change.
- Proof: `SAGEKIN_RP3_topology_identity_proof.json`; manifest: `SAGEKIN_RP3_family_propagation_manifest.json`.

## B2. Validator, D1 + D3 + D4 + D5 (authoritative, §12)

| | Firm | Fails | Margin-0 stations |
|---|---|---|---|
| **SG (c1)** | **67 / 69** | `hip_l`, `hip_r`: 4 / 5 (FAIL_LOOPS) | thumb_mcp ×2, toe1_j1 ×2, toe2_j1 ×2, toe4_j1 ×2 |
| **SGF178 (c2)** | **69 / 69** | none | toe1_j1 ×2, toe4_j1 ×2 |

- Every other station keeps the same verdict class as the frozen v005 realizations.
- Fallback modes, D5 undefined sides and same-digit pole ownership are listed per station in `SAGEKIN_RP3_margin_table.json` / `.csv`, with the heat table in sheet `Sagekin_margin`.
- D5 undefined sides:
  - SG: pinky_ip1, toe2_j1, toe4_j1 (both sides of the body).
  - SGF178: toe1_j1, toe2_j1, toe5_j3.

  No verdict changes between D4 and D4 + D5 (same firm counts and fail lists).
- No station on either configuration has a crease pole owned by its own digit.
- Non-plain passes:
  - SG: fallback defined sides at index / pinky MCP; closed ring at thumb MCP L; scoped adjacent-digit pole at toe3_j3.
  - SGF178: fallback defined sides at shoulder; closed ring at thumb MCP L; scoped adjacent pole at toe3_j3 and toe4_j2.

## B3. Why the hip fails: a foreign-segment probe, not the hip (sheet `Sagekin_hip_diag`)

`tools/rac/rp/sagekin_rp3_v001/hip_diag.py`; `hip_diagnostic/hip_diag.json`.

**What the failing side measures.**
- At `hip_l` the band side **+p** (lateral, W 3.08 cm, probe radius 12.3 cm) selects both band-end vertices on the **forearm**, which hangs beside the hip in the R-6 stance.
- The side path is 6 vertices, all in the arm zone, at x ≈ 23–24 cm, with dominant skin bone `lowerarm_l`.
- The other sides measure the hip: −p 6, −q 6, +q undefined (D1). So the station minimum (4) comes from forearm loops.

**This artefact is in every family realization.** In all six, hip +p lands on the forearm or hand (MF-M 6, MF-F 16, SK-C1R 14, SK-F 12, SGF178 12 forearm loops) and elbow −p lands on the trunk (`spine_02`). It never showed before because the forearm happened to carry ≥ 5 loops inside the band. Sagekin's accepted longer forearm (lower-arm length +0.20) spaces the same forearm loops wider, so SG counts 4.

**Probe validity.**
- Both +p endpoints lie within 0.42 cm of their probe lines, so neither D1 (facing test) nor D5 (digit stations only) excludes the side.
- So the authoritative verdict is FAIL and is reported as such.
- **No geometry or topology was changed to satisfy it** (order §12, standard §6).

**Proposed D6 (diagnostic only; not applied to any verdict).** Implemented as `val2lib.evaluate(..., d6=(W, bones))` and `validator_v2.py --d6-native NATIVE.npz`. It is off by default: the authoritative output is byte-identical with and without it.
- **Rule:** for non-digit stations, a band side is undefined when either selected endpoint's dominant skin bone is not one of the station's own bones.
  - The skin weights are the native hm08 weights carried through the family map.
  - Own bones: hip = pelvis / spine_01 / thigh; elbow = upperarm / lowerarm; and so on (`val2lib.D6_OWN`).
- **Effect on all six realizations** (`validator_D6_proposed/D6_effect_summary.json`):

| | Authoritative | With D6 | Sides excluded by D6 |
|---|---|---|---|
| SG | 67 | **69 / 69** (hip 4 → 6) | hip ±p (lowerarm), elbow ∓p (spine_02) |
| SGF178 | 69 | 69 | same pattern |
| MF-M-R | 69 | 69 | same pattern |
| MF-F-R | 69 | 69 | same pattern |
| SK208-C1R | 69 | 69 | same pattern |
| SKF208 | 69 | 69 | same pattern |

  **No station's loop count or verdict is lowered anywhere.**

**Alternative if D6 is rejected (diagnostic only, no branch built).** `v004_ringsearch.py` on the v005 core with SG / SGF178 added as scoring configurations (`EXTRA_NAT`; `hip_diagnostic/hip_ringsearch_v005.json`):
- 4 single-ring candidates make all six configurations firm. Example: strip 424 | 1043, a 40-vertex ring, 80 new faces, 0 T-4, max aspect 1.9.
- SG reaches 5 (margin 0) in each.
- Any of these is a topology change: a Sagekin branch or a family v006 that re-propagates every race. It needs an explicit order.

## B4. Anatomy gates (§13)

| | SG | SGF178 |
|---|---|---|
| T-1 / T-2 / T-3 / T-7 | pass | pass |
| Family → source, body (median / p95 / max) | 0.000 / 0.196 / 1.79 mm | 0.000 / 0.165 / 2.02 mm |
| Identity zones, max (head / ears / hands / feet) | 0.89 / 0.47 / 0.84 / 0.94 mm | 0.92 / 0.45 / 0.76 / 0.82 mm |
| Source → family, max | 0.94 mm | 0.91 mm |
| Stature diff | −0.42 mm (head-top vertex) | −0.0001 mm |
| bbox diff, max | 0.42 mm | 0.20 mm |
| Silhouette IoU (front / profiles / 3-4) | 0.9976 / 0.9978 / 0.9977 | 0.9980 / 0.9976 / 0.9983 |

Race-relevant proportions (§A5) are carried unchanged, because production = M @ source:
- slightly longer limbs;
- shorter torso;
- shallower ribcage;
- human hands, feet and auricle.

Nothing is exaggerated.

## B5. Sagekin identity gate (§14)

`sagekin_rp3_v001/sg_identity.py`; `anatomy/*_identity.json`.

**Method.**
- Sagekin have no identity sculpt; the identity source is the accepted Sagekin R-6 body.
- **Fit** = distance from the family realization to its own source surface.
- **Signal** = per-vertex correspondence displacement \|M @ (Sagekin hm08 − comparator hm08)\| to the matched-stature Marchfolk body and the other Sagekin configuration.

| Zone | SG fit p95 | SG signal median (vs MFM178) | SGF178 fit p95 | SGF178 signal median (vs MFF178) |
|---|---|---|---|---|
| all | 0.20 mm | 2.70 mm | 0.17 mm | 2.85 mm |
| face | 0.08 | 0.99 | 0.07 | 1.16 |
| head | 0.18 | 0.74 | 0.15 | 0.99 |
| ears | 0.14 | 0.82 | 0.15 | 1.08 |
| hands | 0.08 | 10.4 | 0.07 | 10.1 |
| trunk | 0.38 | 7.6 | 0.34 | 7.7 |
| legs | 0.40 | 4.8 | 0.30 | 5.0 |

- Identity holds in **every zone on both configurations**: fit p95 < 25 % of the nearest-other signal; the ratio is 4–143×.
- **No regression toward Marchfolk.** No clothing, hair or culture is used.
- Configuration 1 vs configuration 2 is shown in sheet `Sagekin_config_comparison`.
- This is a technical gate. The author's anatomy and identity review stays open (standard §11).

## B6. Face / UFCA readiness (§15)

| | Mouth rings | Orbit rings L / R | Poles at mouth corners / within 2 cm of mouth / near eyes |
|---|---|---|---|
| SG | 32 (source 16) | 43 / 43 (21 / 21) | 0 / 0 / 0 |
| SGF178 | 34 (source 16) | 43 / 43 (21 / 21) | 0 / 0 / 0 |

- Open lip and orbit pockets are kept, with no face topology change.
- Face density is 0.135 / 0.132 % of stature.
- The human auricle (MPFB hm08) is family-compatible: ears deviation max 0.47 / 0.45 mm.

## B7. Creator density, 9 zones (§16)

All zones pass on both configurations. Values are mean / p95 edge length as % of stature.

| Zone | Ceiling | SG | SGF178 |
|---|---|---|---|
| face | 0.25 | 0.135 / 0.373 | 0.132 / 0.360 |
| ears | 0.25 | 0.101 / 0.192 | 0.101 / 0.183 |
| hand | 0.30 | 0.142 / 0.304 | 0.130 / 0.280 |
| foot | 0.30 | 0.194 / 0.577 | 0.183 / 0.554 |
| head | 0.25 | 0.236 / 0.506 | 0.223 / 0.519 |
| neck | 0.60 | 0.319 / 0.427 | 0.290 / 0.444 |
| trunk | 0.60 | 0.496 / 0.805 | 0.498 / 0.828 |
| arm | 0.60 | 0.485 / 1.004 | 0.446 / 0.922 |
| leg | 0.60 | 0.514 / 0.884 | 0.502 / 0.811 |

- Values are within a few % of Marchfolk v005 (MF-M trunk 0.507, arm 0.48).
- SG's arm and leg are slightly looser because the Sagekin limbs are longer, still under the ceilings.
- No region is unusually tight or loose. Nothing was decimated or densified.

## B8. Contact (§17)

`sagekin_rp3_v001/contact_prop.py`; `contact/`.

| | Family rest self-intersection pairs | Inherited from source (≤ 1 cm of a native pair) | New |
|---|---|---|---|
| SG | 70 (arm 50, trunk 20); native 38 | **70** | **0** |
| SGF178 | 122 (arm 96, trunk 14, foot 12); native 66 | **122** | **0** |

All pairs are documented source contact (axilla, arm against trunk, toe contact). There is **no new rest, hand, foot, groin, toe or web defect** from propagation.

## B9. Limited deformation sanity (§18)

All 18 Standard v1 poses were run with the source rig and weights carried through the map. Comparisons are in `SAGEKIN_RP3_deformation_comparison.json` and the deformation sheets.

**Compared with Sagekin's own native hm08:** counts scale with the ×4.3 face count, as on every family realization.

**Compared with the frozen, accepted Marchfolk v005 on the same topology:**

| | SG vs MF-M v005 | SGF178 vs MF-F v005 |
|---|---|---|
| Flipped faces, worst pose difference | at most +2 | at most 0 |
| Poses worse by more than 5 flips | none | none |

Examples:
- SG: knee140 76 = 76; hip_flex90 56 vs 55.
- SGF178: fist 14 vs 45; knee90 33 vs 36.

**Classification.** Every residual is LBS weights or joint-placement class, identical in kind to the accepted family behaviour.

**Toe extension 30°:**
- SGF178: 58 flips (MF-F 60). Same class as accepted MPFB-CF-1 / CF-2; recorded, not failed.
- SG: 71 (MF-M 70).

**No new topology-class deformation failure. The frozen family topology behaves at least as well as on Marchfolk.** No corrective weighting was started.

## B10. Visual evidence (§19)

`reviews/rac-rp3-evidence/sagekin_rp3_v001/sheets/`:

| # | Sheet |
|---|---|
| 1–3 | `Sagekin_body_{SG,SGF178}`: clay front / rear / profile / 3-4; source vs family wire, full and upper / lower |
| 4 | `Sagekin_face_{SG,SGF178}`: face close-up, wire, face rings |
| 5–10 | `Sagekin_closeups_{SG,SGF178}`: shoulder, elbow, hand, pelvis, knee, foot (source wire, family wire, counted loops, per-station verdict) |
| 3 | `Sagekin_overlay_{SG,SGF178}`: deviation heat, front / rear / profile silhouette overlays |
| 11 | `Sagekin_validator_{SG,SGF178}` (authoritative) and `Sagekin_margin` (margin heat next to the four frozen v005 realizations) |
| 12 | `Sagekin_density_{SG,SGF178}` |
| 13 | `Sagekin_deform_{SG,SGF178}` |
| 14 | `Sagekin_config_comparison`: SGF152-NAT, SGF178, SGF208 and SG at true scale, with the Part A table |
| 15 | `Sagekin_vs_Marchfolk_178`: neutralised, with silhouette overlays |
| — | `Sagekin_hip_diag`: the hip +p probe on the forearm, SG vs MF-M, with the D6 effect |

## Required answers (§21)

| Question | Answer |
|---|---|
| Was a proper ~178 cm config-2 central reference created? | **Yes.** SGF178, 178.00 cm. It is the existing canonical configuration-2 construction base, validated (not newly invented). |
| Is it deterministic and rebuild-identical? | **Yes.** Both the regen and the full re-solve give max \|dV\| 0. |
| Does it sit coherently inside the 152–208 cm envelope? | **Yes.** 16 / 20 shares inside, 3 follow the accepted c1 pattern, 1 is a ratio whose components are inside. |
| Did both Sagekin configs propagate onto the active family topology unchanged? | **Yes.** Face hash `ec768ae2…`, identical map, V = M @ hm08 exactly. |
| Are both 69 / 69 under D1 + D3 + D4 + D5? | **No.** SGF178 is 69 / 69. **SG is 67 / 69** (hip ±, a forearm-sampled probe). With the proposed D6, both are 69 / 69. |
| Do anatomy gates pass? | **Yes** (T-1 / T-2 / T-3 / T-7, IoU ≥ 0.9976). |
| Does Sagekin identity remain intact without exaggeration? | **Yes.** Every zone; directions match canon and the accepted bounds. |
| Does face / UFCA readiness pass? | **Yes.** |
| Does density pass? | **Yes**, 9 / 9 zones on both. |
| Did any new topology-class deformation failure appear? | **No.** |
| Is a Sagekin-specific topology branch needed? | **No**, if D6 is accepted. If D6 is rejected, one additional ring would be needed (diagnostic options in §B3). |
| Is Sagekin ready for freeze? | **Not yet.** Ready once the author rules D6 accepted; until then the authoritative validator holds SG at 67 / 69. |

## Other notes

- **Tool changes.**
  - `val2lib.py` / `validator_v2.py`: proposed D6, off by default. The authoritative output was regression-checked as identical.
  - `family_sheets.py`: `FAM_VAL` / `FAM_VAL_LABEL` environment variables so the sheets show the authoritative D4 + D5 verdict.
  - `v004_lib.py`: an `EXTRA_NAT` diagnostic hook.
- **No accepted asset was modified.** Source hashes are in `source_hashes_after.txt`; v005 / Skarn frozen files and records are untouched.
- `reviews/reference-assets/manifest.json` is unchanged. SGF178's manifest role stays "construction base" until the author accepts it as the configuration-2 central reference.

**STOP FOR CHATGPT REVIEW.** Fenn, the other races, rig, morphs, UV / materials, LOD and UE5 were not started.
