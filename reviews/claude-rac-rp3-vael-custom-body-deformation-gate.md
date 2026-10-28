# RAC RP3 — Vael bounded custom body-deformation gate

**Date:** 2026-10-28
**Order:** `reviews/chatgpt-rac-rp3-vael-custom-body-deformation-order.md`
**Parent gate:** `reviews/claude-rac-rp3-vael-body-face-source-gate.md` (b0d1d25)
**Evidence:** `reviews/rac-rp3-evidence/vael_rp3_custom_deformation/` (21 sheets in `sheets/`)
**Tools:**
- `tools/rac/w1/vael_body_field.py` (the field);
- `tools/rac/w1/arm_lib.py` (`vael_field_apply`, inert unless `cfg["vael_field"]` is set);
- `tools/rac/rp/vael_rp3_v001/`: `build_vd.sh`, `vd_eval.py`, `vd_selfx.py`, `vd_sheets.py`, `skp_va2.sh` (`SKP_SRC`), `va2_eval.py` (composite row retired), `va_manifest.py` / `run_va_prod.sh` (v003).

## RESULT — VAEL BODY NEEDS LOCAL REVISION — VD2 is the provisional winner — ears stay LOCKED

**One bounded issue remains: the full-body frontal / 3-4 read.**

The authorised field (order §4) is built, deterministic and technically clean, and VD2 propagates:
- **69 / 69 D1–D6** on both configurations;
- 0 new contacts;
- VC2 unchanged;
- pelvis 9 / 9.

It moves five of the six §8 systems measurably away from Marchfolk:
- ribcage depth / side-wall breadth +11 / +12 %;
- torso-to-pelvis continuity +1.8 / +3.7 %;
- pelvis band +1.9 / +2.6 %;
- palm root +10 / +9 %;
- heel base +15 / +14 %.

The changes show in torso close-ups and silhouette overlays (sheets 07, 12).

**At full-body scale, front and three-quarter, VD2 still reads as a Marchfolk body** (sheets 04, 05, 20). VD3 does too.

The reason is structural. The frontal elf signal of the accepted elves is carried by two things:
- **Shoulder span.** Bideltoid is −6.1 / −4.0 % below Marchfolk for Fenn and −4.5 / −5.0 % for Aelari. Vael VD2 sits at **−0.05 / 0.00 %**.
- **Limb-envelope gracility.**

Neither is one of the six authorised systems. The authorised systems are local (side wall, clavicle, pelvis contour, palm root, heel), and at natural magnitudes (≤ 0.9 cm) they cannot change a whole-body read.

## 1. The field (VDF1.2) — deterministic, shared c1 / c2

| Region (§4) | Mask / frame | Axis | Magnitude (VD2) | Falloff |
|---|---|---|---|---|
| Ribcage side wall | trunk weight > 0.3, arm-free, lateral azimuth 62–150°, centred on the spine_03 head | lateral, inward | −0.070 × waist half-breadth (≈ −0.9 cm per side) | Gaussian σ = 0.85 × (spine_03 − spine_02) |
| Torso-to-pelvis continuity | lumbar side wall (spine_01 → spine_02), lateral azimuth | lateral, inward | −0.030 × waist half-breadth | Gaussian; zero at / below the crest |
| Pelvis / hip | anterolateral iliac (ASIS), azimuth 50° ± 22° | radial outward | +0.030 × waist half-breadth | Gaussian in height and azimuth |
| Clavicle | front skin along clavicle → shoulder-joint line, neck excluded | forward-up | 0.35 cm × s | Gaussian in height |
| Hand base | palm root, 22–65 % of wrist → middle_01 span; digits incl. the thumb ray excluded | across the palm | +8 % breadth | smoothstep |
| Foot base | heel / proximal foot below the malleoli | transverse | +8 % breadth | smoothstep + height fade |

How it is applied:
- On the source rest mesh after targets and bone scales, as a shape key, before posing.
- Joint centres are unchanged: the stature and joints differ only by the 0.0025 cm grounding offset.
- The head moves only by that rigid offset (the head translation is uniform to 1e-5 cm).
- Ears get zero displacement.
- Trunk regions are held off the free arm; the result is mesh-smoothed (8 iterations).
- The definition rides in the build record, so `regen.py` reproduces it: geometry identical on both configurations.

**c1 / c2 normalisation:** magnitudes are fractions of the body's own dimensions, or cm × stature / 173.14.

**Candidates:** VD1 = 0.6×, VD2 = 1.0×, VD3 = 1.4× on the same field, masks and signs. Overrides are in `overrides/`.

| Version | Value |
|---|---|
| Definition | sha 9f208810… (`VD_definitions.json`) |
| Module | sha 28bebd0d… |

**Field iterations** (all disclosed):
- **Prototype — lateral fill (outward).** Rejected: it reads as a thicker human waist, toward stocky.
- **VDF1.1 — re-anchored on the spine joints.** The rib region now avoids the breast and the field is held off the arm. This removed new arm/trunk self-contact on c1.
- **VDF1.2 — digit rays excluded from the palm field.** VDF1.1 dropped the c1 `thumb_mcp` stations to 2 / 3 loops (67 / 69 validator).

No MPFB target changes.

## 2. Candidate audit (c1 / c2)

| | VD1 | VD2 | VD3 |
|---|---|---|---|
| Affected vertices (rest) | 1,317 / 1,455 | 1,446 / 1,609 | 1,529 / 1,701 |
| Max displacement (cm) | 0.56 / 0.51 | 0.93 / 0.84 | 1.30 / 1.18 |
| RMS of affected vertices (cm) | 0.19 / 0.18 | 0.30 / 0.29 | 0.41 / 0.39 |
| Rebuild drift | 0 | 0 | 0 |
| Canon (20 rows) | 20 / 20 | 20 / 20 | 20 / 20 |
| Pelvis gating | 9 / 9 | 9 / 9 | 9 / 9 |
| New self-intersection pairs (R-6 source) | c1 2 (2 removed) / c2 28 (32 removed) | c1 2 (2 removed) / c2 30 (46 removed) | c1 2 (2 removed) / c2 28 (48 removed) |

Per-region maximum at VD2:
- rib 0.93 / 0.84;
- flank 0.92 / 0.77;
- ASIS 0.20 / 0.18;
- clavicle **0.12 / 0.15**;
- palm 0.28 / 0.26;
- heel 0.24 / 0.24 cm.

**Self-intersection:** the new pairs are the arm–trunk contact patch shifting as the side wall moves. The total number of pairs falls on c2 (102 → 86) and is unchanged on c1. In the family, 0 new contacts are classified, and the c2 family self-intersection pairs drop from 126 to 114.

**Integrity:** 1 component, no boundary, non-manifold or degenerate faces, normals outward.

## 3. Human firewall (§8) — VD2 vs Marchfolk

"Human" is the Sagekin–Marchfolk difference. Region RMS is measured on the field's own masks.

| System | Descriptor vs MF, R1 → VD2 (c1 / c2) | Human variation | Region RMS vs MF (SG–MF) | Visible? |
|---|---|---|---|---|
| 1 Ribcage side wall | depth / lower-rib breadth +5.5 → **+11.2 / +12.4 %** | 2.4 / 3.2 % | 9.4 / 8.6 mm (9.4) | close-up and overlay yes; full body no |
| 2 Torso-to-pelvis continuity | waist / lower-rib breadth +0.4 → **+1.8 / +3.7 %** | 0.0 % | 8.5 / 7.6 (11.0 / 11.8) | close-up yes |
| 3 Shoulder / clavicle | — | — | 1.9 / 1.6 (2.8 / 3.7) | **no** (field ≤ 0.15 cm; the mask is too narrow at natural strength) |
| 4 Pelvis / hip | crest-band breadth +1.5 → +1.9 / +2.6 % | 0.6 % | 4.4 / 3.8 (12.7 / 12.9) | marginal |
| 5 Wrist / hand base | palm root / wrist +4 → **+10.2 / +8.7 %** | 0.1 / 1.2 % | 4.5 / 5.6 (6.5 / 6.2) | close-up, slight |
| 6 Ankle / foot base | heel / foot length +8 → **+15.0 / +13.5 %** | 0.1 / 0.2 % | 5.2 / 5.0 (0.9) | close-up, slight |

**Guard rails (/ stature, VD2 vs MF), not stocky, broad or barrel:**

| Measure | VD2 vs MF |
|---|---|
| Thorax max breadth | −0.2 / −0.5 % |
| Waist | −1.8 / −2.4 % (between MF and Fenn) |
| Iliac crest | −0.5 / −1.1 % |
| Bideltoid | unchanged (= MF) |
| Thorax depth | unchanged (+5.5 / +5.7 %, R1) |
| Bitrochanteric / crest | increased (VA-P2b holds more strongly) |

No waist pinch at VD2. VD3 begins to show a lower-rib inflection on c1 (sheet 12), so VD3 is the upper natural bound.

**Visual verdict:** at body scale (sheets 04, 05, 20) VD2 is not distinguishable from Marchfolk; the differences need a close-up. **Human firewall: NOT PASSED.**

**Scope diagnostic GX** (sheet 21; not a candidate). GX is VD2 plus:
- a stronger trunk side wall (rib −0.09, flank −0.05);
- 5 % limb-envelope slimming.

GX slims the read, but:
- on c2 it already shows a waist pinch;
- it still does not read as clearly elven.

The remaining gap is therefore not width alone. At body scale, the accepted elves differ from Marchfolk through shoulder span plus the limb proportions and envelope. The Vael canon places Vael close to humans on all of these (hip window, joint gracility window, "moderate width", "no new mandatory shoulder breadth").

## 4. Three-elf regression (§9) — holds

**Versus Fenn:**
- deeper torso (thorax depth +11 / +13 %);
- less extremity-dominant (extremity share < Fenn);
- more joint / base presence:
  - elbow, knee, wrist, ankle all > Fenn;
  - palm +8.2 / +9.0 %;
  - foot breadth +22 / +21 %;
- distinct face (VC2 rows 9 / 9).

**Versus Aelari:**
- less vertically elongated: neck share and cranial share < Aelari, VA-P6 holds;
- deeper torso: +13 / +14 %;
- more joint / base presence;
- compact, deep-mid-face craniofacial read.

VD2 moves toward neither: its trunk breadths sit between MF and Fenn, and bideltoid stays at MF. See sheet 06.

## 5. Pelvis regression (§10) — HARD — PASS for VD1 / VD2 / VD3

Skeletal proxy, all t:

| Rule | c1 | c2 |
|---|---|---|
| Hip-joint ordering MF < Vael < Aelari < Fenn | +0.10 / −0.11 / −2.37 % | +0.05 / −0.29 / −2.44 % (same as R1) |
| VA-P6 | −1.56 % | −0.29 % |
| VA-P2b | +0.95 % | +1.49 % |
| VA-P3 vertical (no iliac elongation) | −6.5 % | −5.9 % |
| VA-P4 AP depth | > Fenn / Aelari, ≈ MF | > Fenn / Aelari, ≈ MF |

- No new breadth identity: the crest narrows slightly and bitrochanteric is unchanged.
- VA-P3 "lighter than MF" stays visual-only, per §1.4.

## 6. Limb / gracility (§11) — VD2 vs MF

| Joint / base | c1 | c2 |
|---|---|---|
| Elbow | unchanged from R1 | unchanged from R1 |
| Knee | unchanged from R1 | unchanged from R1 |
| Ankle | unchanged from R1 | unchanged from R1 |
| Wrist | −2.9 % (still > Aelari +0.5 %, > Fenn) | −2.0 % |
| Palm | +1.8 % | +1.9 % |
| Foot breadth | +7.9 % | +6.9 % |

- Joint mean stays gracile vs MF.
- No large hands, thick ankles or stocky silhouette.
- Hand and foot base differentiation improved: palm root +6 / +2.5 points, heel +7 / +6 points over R1.

**Wrist note (c1):** the field never touches the ±1 cm wrist station. The measured wrist breadth comes from the principal-axis width of that station, so the change is a measurement-axis effect, not anatomy.

## 7. Propagation (§13), VC2 (§14), expressions (§15)

**Propagation:** `VA_{M,F}_REF_RP3_bodyfam_v003` (sha 212ef083… / fd5ce26b…), sources `VAL4-R1-VD2` / `VALF178-R1-VD2`.
- 57,842 V / 57,840 Q.
- Face hash, map and UV identical; |V − M·hm08| = 0.
- 69 / 69 D1–D6; `thumb_mcp` margin 0 / 1, as R1.
- T-1 / T-2 / T-3 / T-7 pass.
- Density 9 / 9.
- Face rings: mouth 37 / 33, orbit 43 / 43.
- Contact: 0 new.
- Deformation: worst flip excess vs MF v005 is 3 / 1; no pose worse by more than 5.
- Read-back: 6e-8 m. E: copies read back byte-identical.

**VC2:** unchanged.
- Head displacement is a uniform 0.0025 cm translation.
- Face systems 6 / 6; elf rows 9 / 9.
- Whole-face departure 1.138 / 1.128 mm (= R1).
- Brow −1.3 / −2.66 % (= R1).
- Jaw +0.43 / +0.72 % (= R1, no new jaw inflation).
- Hidden-ear face 5 / 7 and 6 / 7 canon systems (= R1).

**Expressions:** identical to R1 for every unit and configuration (blink 116 / 131, anger, surprise, sadness, smile).

## 8. Answers

1. **Is VC2 unchanged and accepted?** Yes. It is geometrically unchanged and accepted, per §1.1.
2. **Is R1 pelvis ordering unchanged?** Yes: same joints, 9 / 9.
3. **Which VD candidate is recommended?** VD2, as the provisional winner. VD3 adds no full-body read and begins a lower-rib inflection.
4. **Does the Vael body now pass the human firewall visually?** **No**: not at full-body front or three-quarter.
5. **Which body systems create the visible distinction?**
   - At close range: ribcage side wall with depth, torso continuity, hand base and heel base.
   - Pelvis: marginal.
   - Clavicle: none.
6. **Does Vael remain distinct from frozen Fenn / Aelari?** Yes.
7. **Did any candidate become stocky, barrel-chested or broad by default?** No. The trunk got narrower and depth is unchanged.
8. **Does MF < Vael < Aelari < Fenn still hold?** Yes.
9. **Does VA-P6 still hold?** Yes.
10. **Did hand / foot base differentiation improve?** Yes, measurably (palm root +6 / +2.5, heel +7 / +6 points). Visually it is slight.
11. **Did family topology remain unchanged?** Yes.
12. **Are both propagated bodies still 69 / 69 D1–D6?** Yes, after the thumb-ray exclusion (VDF1.2).
13. **Did any new source, contact or deformation problem appear?** No.
14. **Is Vael ready to unlock ear prototyping?** **No**: the body firewall has not passed. No ear proposal was prepared.

## 9. Author decision requested (the one bounded issue)

The authorised local systems cannot make a 178 cm Vael read non-human at body scale. Choose one:

- **(a) Authorise one frame-level elf-family term.** A modest Vael shoulder span (bideltoid / clavicle span between MF and Fenn / Aelari, for example −2 to −3 %) plus a limb-envelope gracility term (girth between MF and Aelari), both as bounded shared deterministic fields or MPFB scales.
  - This changes the "no new shoulder breadth" reading (narrower, not broader).
  - It touches arm / leg girth, which the composition firewall must keep skeletal.
- **(b) Accept a close-range / profile human-firewall standard for Vael.** Identity is carried by depth, joint and base, the face and ears, with a near-human frontal silhouette. Then unlock ears with VD2.
- **(c) Strengthen the clavicle term.** The current mask yields ≤ 0.15 cm; widen it to the infraclavicular fossa. This alone will not change the full-body read.

**STOP FOR CHATGPT REVIEW.** Nothing frozen, no ears, no Halvren, v005 / Fenn / Aelari / VC2 untouched; immutable hashes 20 / 20 equal (`immutable_hashes.txt`).
