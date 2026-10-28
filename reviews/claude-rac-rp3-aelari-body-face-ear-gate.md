# RAC RP3 — Aelari configuration-2 central reference + hidden-ear identity + ear-branch prototype — gate

**Date:** 2026-10-27
**Order:** `reviews/chatgpt-rac-rp3-aelari-body-face-ear-order.md` (fd71f15)
**Evidence:** `reviews/rac-rp3-evidence/aelari_rp3_v001/`
**Tools:** `tools/rac/rp/aelari_rp3_v001/`, plus the Standard v1 pipeline and the Fenn ear tools.
- The Fenn ear tools gained switches whose defaults keep frozen Fenn byte-reproducible:
  - Aelari candidates `AE-E1..E3`;
  - env `EAR_CAND`, `EAR_CF`, `EAR_LAYOUT_METRIC`, `EAR_HEADS`, `EAR_BLEND_STATUS`.
**E: (review files, not frozen):** `E:/…/RaceBodies/production/Aelari/RP3/` (body-family blends, maps, sidecars, manifest) and `…/Aelari/RP3/ear_branch/` (6 prototype blends). Read back byte-identical.

## Result

**AELARI BODY/FACE PASS + EAR BRANCH READY FOR AUTHOR SELECTION**

| Stage | Result |
|---|---|
| Part A | **AELARI C2 CENTRAL REFERENCE PASS.** AELF190 is 190.00 cm, deterministic, and replicates the AEL1 design. Two **inherited AEL1 ties** are flagged for the author (§A3). |
| Part B, technical | Both body-family candidates pass Standard v1 on unchanged v005: **69 / 69 D1–D6**. |
| Hidden-ear **body** | **PASS.** Aelari reads vertically continuous; Fenn reads compact-centred / extremity-emphasised. |
| Hidden-ear **face** | **PASS.** 7 / 7 Aelari face systems are material on both configurations, and Aelari is distinct from Fenn. |
| Part C | **REUSE PASS.** The Fenn ear topology v002 engineering template carries wholly Aelari geometry with the identical face list. AE-E1 / E2 / E3 pass every technical gate. **AE-E2 is recommended.** |

Nothing is frozen. Frozen Fenn and MPFB Family Base v005 are unchanged (`immutable_hashes.txt`).

---

# PART A — configuration-2 central reference (AELF190)

## A1. Construction and provenance

**No existing Aelari c2 build was found:** neither the workspaces nor the repository contained one before construction.

AELF190 was built on the shared MPFB c2 route used for MF-F / SGF178 / FNF181:
- **Builder:** `build_variant.py`.
- **Base:** `MF-F-R_build.json`.
- **Overrides:** exactly the AEL1 targets (20) and bone scales (7), plus stature 190 with `resolve_stature`.

**The resulting cfg equals AEL1's in every key except `gender` and `id`.** No configuration-specific Aelari anatomy was invented, and there is no sex-specific pelvic or ear difference.

| | |
|---|---|
| Height macro | 0.661865234375 (re-solved) |
| R-6 stature | **190.0008 cm** |
| Envelope | AE168N-NAT 168.0 < AELF190 190.0 < AE221 221.0 cm — inside |
| Files | `reviews/reference-assets/r6/AELF190_r6.npz` (`a81407ff…`), `builds/AELF190_build.json` (`040de50a…`), `builds/AELF190_meas.json`; manifest entry is CANDIDATE |
| Sidecar | `AELF190_central_reference_sidecar.json` |

## A2. Determinism and integrity

- **`regen.py` from the record:** geometry identical, max \|dV\| 0.
- **A second independent full height re-solve:** identical (max \|dV\| 0, same macro).
- **AEL1 rebuild:** max \|dV\| 0, and the measurement reproduces `AEL1_meas.json` to 1e-16.
- **Native hm08 integrity:** both bodies have 1 component; 0 boundary, non-manifold, degenerate or coincident defects; outward orientation (`native_integrity` in the sidecars).

## A3. Aelari body identity at matched stature (~190 cm, both configurations)

**Comparators:** MFM/MFF190, SGM/SGF190 and frozen-Fenn CF2 FNM/FNF190, all re-solved to 190 cm (diagnostic builds in `partA/cmp/`). Measurement is `run_candidate.py` with the common MF-M-R eye reference.

**Canon** (`AELARI_V1` v1.0 / v1.1, order §1 / §5): **c1 14 / 19, c2 16 / 19**.

| Measure (Aelari vs frozen Fenn / vs Marchfolk) | c1 | c2 |
|---|---|---|
| **Central vertical share** (cranium + neck + torso) | **+2.26 % / −0.70 %** | **+2.23 % / −0.65 %** |
| **Extremity share** (arm + hand + leg + foot) | **−2.36 % / +1.34 %** | **−2.40 % / +1.48 %** |
| Torso share > Fenn | +1.67 % | +1.80 % |
| Neck share > Fenn and humans | +5.84 % / +3.25 % | +4.43 % / +2.19 % |
| Cranial vertical share > Fenn and humans | +1.82 % / +2.86 % | +2.02 % / +3.08 % |
| Waist interval / torso > Fenn, ≥ MF | +2.43 % / +1.67 % | +1.59 % / +1.77 % |
| Arm share > human; elongation more even than Fenn (forearm / upper arm closer to MF) | +1.65 %; yes | +1.85 %; yes |
| Leg share > human | +0.75 % | +0.71 % |
| Hand / foot share > human | +3.51 % / +1.01 % | +3.96 % / +1.57 % |
| Thorax depth < MF (shallow ribcage) | −6.15 % | −6.52 % |
| Elbow breadth < MF; wrist < MF | −3.3 %; +0.4 % (tie) | −3.3 %; −4.6 % |
| **Ribcage (thoracic) vertical > Fenn** | **−0.62 % (tie, not >)** | **−0.33 % (tie)** |
| **Leg evenness (shin / leg closer to MF than Fenn)** | **0.5163 vs Fenn 0.5157 (tie)** | 0.4883 vs 0.4890 (holds) |

**Inherited AEL1 ties (author notes, not changed):**
1. **Ribcage vertical ≈ Fenn.** The thoracic interval itself is not longer than Fenn's at 190 cm. The longer Aelari torso comes from the waist interval (+1.6–2.4 % vs Fenn), the neck and the cranium.
2. **AEL1 lower-leg weighting ≈ Fenn's.** AEL1 carries a calf bone scale of 1.0523 and a thigh scale of 0.9875, so its shin / leg equals Fenn's on configuration 1.

Both are properties of the accepted W1m AEL1 source. AELF190 replicates them, as it must ("preserve the accepted AEL1 architecture"). Changing either needs an AEL1 source decision, not a c2 construction change.

**Skin knee / ankle breadth readings are unstable across the height macro.** MFM's knee breadth drops from 11.9 to 10.3 cm between 173 and 190 cm. They are reported as diagnostics only.

**Configuration consistency:**
- AELF190 − AEL1 has the same sign as the human-family architecture (MFF190 − MFM190) on 18 / 19 rows. The exception is knee breadth, the unstable reading.
- All 18 / 19 c1 signs relative to MF are replicated in c2.

## A4. Pelvis (skeletal proxy, t = 0 / 0.5 / 1.0 cm; a direction counts only if it holds at all three)

| Rule | c1 | c2 |
|---|---|---|
| AE-P2a hip-joint height / stature > MF | +0.75 % ✓ | +0.71 % ✓ |
| AE-P2b / E-A2 bitrochanteric / crest not lower than MF | +0.75 … +0.85 % ✓ | +0.47 … +0.55 % ✓ |
| AE-P3 pelvic vertical / crest > MF | +10.3 … +10.9 % ✓ | +10.2 … +10.8 % ✓ |
| AE-P3 pelvic vertical / crest > Fenn | +10.1 … +10.6 % ✓ | +9.9 … +10.4 % ✓ |
| AE-P6 waist interval / torso > Fenn | +2.48 % ✓ | +1.61 % ✓ |
| AE-P6 waist interval / torso ≥ MF | +1.72 % ✓ | +1.80 % ✓ |

The pelvic vertical contribution comes from iliac height, not narrowing: bitrochanteric / crest is not lower. Lean-build alignment residuals are reported in `partA/skp/`.

**Part A verdict: AELARI C2 CENTRAL REFERENCE PASS.** The c2 is a faithful, deterministic replication of the accepted AEL1 design. The two inherited ties are recorded for the author.

---

# PART B — body-family propagation and hidden-ear gates

## B1. Body-family candidates (diagnostic; carry the family human ear)

| | `AE_M_REF_RP3_bodyfam_v001.blend` (AEL1) | `AE_F_REF_RP3_bodyfam_v001.blend` (AELF190) |
|---|---|---|
| sha / geometry hash | `7be4dd30…` / `1ba6df57…` | `608c127e…` / `291f3572…` |
| Face topology hash | **`ec768ae2…` = family** | **= family** |
| V / Q, quads | 57,842 / 57,840, 100 % | same |
| Map / UV / faces; V = M @ hm08 | identical; 0.0 | identical; 0.0 |
| Regen from record | geometry identical (\|dV\| 0) | identical |
| Read-back (Blender, no save) | faces equal, ≤ 6e-8 m | same |

Manifest: `AELARI_RP3_bodyfam_propagation_manifest.json`.

## B2. Standard v1 gates

| Gate | AEL1 (c1) | AELF190 (c2) |
|---|---|---|
| Validator D1 + D3 + D4 + D5 + D6 | **69 / 69** | **69 / 69** |
| Without D6 (D4 + D5) | 67 (hip ±p: the long-forearm probe artefact D6 was accepted for, as Fenn FNL4) | 69 |
| Margin-0 | thumb_mcp l/r, toe1_j1 l/r | toe1_j1 l/r |
| T-1 / T-2 / T-3 / T-7 | pass (body max 1.83 mm; IoU min 0.9978) | pass (2.02 mm; 0.9979) |
| Ear zone (non-final source: MPFB human auricle) | max 0.47 mm — **not a final Aelari-ear PASS** | 0.45 mm — same |
| Density, 9 zones | pass (face 0.131 / ears 0.097 %) | pass (0.128 / 0.098 %) |
| Face rings: mouth / orbit; mouth-corner poles | 30 / 43 / 43; 0 | 36 / 43 / 43; 0 |
| Contact | 60 source + 4 family-class, **0 new** | 158 source, **0 new** |
| Deformation (18 poses) vs Marchfolk v005, worst flip excess | +4 | +1 |

- No new topology-class failure.
- Fallback statuses, D5 / D6 exclusions and per-station margins are in the sidecars and sheet AE_07.
- D6 excludes one side each at hip l/r and elbow l/r, the same as Sagekin / Fenn.

## B3. Hidden-ear BODY identity — HARD GATE: **PASS**

`ae_hidden_ear.py`.
- **Setup:** matched stature ~190 cm, matched frame, composition and age, R-6; ears (hm08 `w_ears` > 0.05) are excluded and collapsed.
- **Region correspondence RMS:** each comparison is shown against the human–human baseline (Sagekin vs Marchfolk).

| Region | c1 Aelari vs Fenn (× baseline) | c1 Aelari vs MF (×) | c2 Aelari vs Fenn (×) | c2 Aelari vs MF (×) |
|---|---|---|---|---|
| trunk | 10.0 mm (1.13) | 11.0 (1.24) | 10.4 (1.17) | 10.9 (1.23) |
| arm | 8.3 (1.90) | 11.0 (2.52) | 7.9 (1.81) | 10.8 (2.49) |
| hand | 16.2 (1.46) | 14.1 (1.27) | 15.1 (1.38) | 14.4 (1.32) |
| leg | 15.7 (2.05) | 14.0 (1.83) | 16.1 (2.12) | 13.4 (1.76) |
| foot | 8.2 (6.20) | 7.6 (5.71) | 7.8 (6.00) | 7.3 (5.67) |
| neck | 4.9 (2.88) | 5.1 (3.03) | 6.5 (3.86) | 6.2 (3.67) |

**Equal-height Fenn / Aelari test** (§9, sheets AE_03 / AE_05):
- **Aelari is vertically continuous:** central vertical share +2.2 % over Fenn (neck +4.4–5.8 %, torso +1.7–1.8 %, waist +1.6–2.4 %, cranium +1.8–2.0 %; pelvic vertical / crest +10 %).
- **Fenn is extremity-emphasised:** Fenn has +2.4 % extremity share (arm +3.1 %, hand +3.2 %, leg +1.6 %, foot +2.5 % over Aelari) and lighter joints.
- **Not the same elf body at different heights:** the body differs by 1.1–6.2× the human–human baseline in every region.
- **Related by ancestry:** the trunk is closest at 1.1–1.2×, the shared elven foundation.

The ribcage-vertical tie (§A3) is part of that shared trunk. The overall vertical distribution still separates the two races.

## B4. Hidden-ear FACIAL identity — HARD GATE: **PASS**

`ae_hidden_ear.py`.
- Descriptors are taken on fixed hm08 landmarks (`fn_face_metrics`).
- A system counts as material when the direction holds against both humans by at least 1 % and by more than 2× the human baseline.

| Aelari canon system | c1 vs MF / Fenn | c2 vs MF / Fenn | Material |
|---|---|---|---|
| 1 facial verticality (face height / bizygomatic) | +6.9 % / +5.4 % | +7.1 % / +5.8 % | ✓ / ✓ |
| 2 cranial-height contribution (vertex–nasion / stature) | +2.7 % / +1.7 % | +3.0 % / +2.0 % | ✓ / ✓ |
| 3 longer forehead-to-chin (/ bizygomatic) | +6.6 % / +4.4 % | +6.7 % / +4.6 % | ✓ / ✓ |
| 4 narrower lower face (/ bizygomatic) | −2.2 % / +0.7 % | −2.3 % / +0.7 % | ✓ / ✓ |
| 5 lighter mandible (gonial / bizygomatic) | −4.0 % / −1.8 % | −4.5 % / −1.9 % | ✓ / ✓ |
| 6 vertically oriented cheek / mid-face | +3.1 % / +1.9 % | +3.6 % / +2.2 % | ✓ / ✓ |
| 7 lighter brow (glabella projection) | −6.0 % / −5.3 % | −9.1 % / −7.3 % | ✓ / ✓ |
| Eye presentation longer / narrower than Fenn (aperture width / height) | +36.7 % vs Fenn | +29.2 % vs Fenn | Fenn relation ✓ |

- **Region RMS:** Aelari departs materially from humans in the cranium, forehead, orbit, cheeks and jaw (nose and mouth are not required). It departs from Fenn in the cranium, orbit, cheeks, mouth and jaw.
- **Shared ancestry:** the elven orbit and lighter brow are shared with Fenn, but Aelari is **not** "CF2 Fenn stretched" or "Fenn with narrower eyes". The lower face is not narrower than Fenn's (+0.7 %); the difference is in verticality, the cheek / mid-face and the eye presentation.
- The `cranial_height_over_face` ratio falls (−2.3 % vs humans) because the face is longer, so it is reported only. The canon "cranial-height contribution" is read at matched stature (system 2).
- **No craniofacial source authoring is required:** AEL1's existing craniofacial targets express the face canon. Unlike Fenn, there is no source gap.

---

# PART C — Aelari ear-branch prototype (unlocked)

## C1. Source limitation

- No accepted Aelari external-ear production source exists; AEL1 / AELF190 carry the MPFB human auricle, which is non-final.
- Geometry comes from the W1e **AE-elven** evidence (`ear_families.py` / `_v2.py`): L 9.4, wb 1.70, taper 0.25 / 0.95, lobe 0.14, projection 24°, tilt 30°, sweep 1.7, thickness 0.25, with full relief.

## C2. Fenn v002 topology reuse test (§14) — **REUSE PASS**

**What is reused** is engineering only, unmodified:
- the frozen Fenn ear topology v002 sheet layout (connectivity and (s, t) parameterisation);
- the cuff canon (read-only);
- the root interface;
- the deformation-aware guard.

**Every vertex position is Aelari.** The Aelari parameters (`ear_branch_lib.W1A`) are evaluated on the Aelari heads.

- **All 6 realizations have a face list identical to the frozen Fenn production body.** One topology serves c1 / c2 × AE-E1 / E2 / E3.
- **Tested alternative:** the same connectivity with sheet positions re-optimised in the Aelari metric (`EAR_LAYOUT_METRIC=AE-E2`) gave AEL1 AE-E2 T-4 106 vs 117. It isn't needed, so strict reuse was kept.
- No universal elf-ear topology is declared. Reuse is a Fenn → Aelari engineering result only.

## C3. Candidates (one topology, geometry only differs)

| | L | wb | projection | tilt | sweep |
|---|---|---|---|---|---|
| AE-E1 restrained | 8.3 | 1.65 | 19° | 27° | 1.3 |
| **AE-E2 balanced central** (= evidence) | 9.4 | 1.70 | 24° | 30° | 1.7 |
| AE-E3 stronger | 10.4 | 1.75 | 29° | 34° | 2.0 |

AE-E3 is still well inside Fenn central (50°).

## C4. Technical gates (all six realizations)

| | AEL1 E1 | AEL1 E2 | AEL1 E3 | AELF190 E1 | AELF190 E2 | AELF190 E3 |
|---|---|---|---|---|---|---|
| T-4 / 3,718 | 103 (2.8 %) | 117 (3.1 %) | 135 (3.6 %) | 106 (2.9 %) | 120 (3.2 %) | 136 (3.7 %) |
| Aspect max; > 10 | 8.34; 0 | 8.29; 0 | 8.41; 0 | 8.34; 0 | 8.55; 0 | 8.32; 0 |
| Branch self-intersections | 0 | 0 | 0 | 0 | 0 | 0 |
| Root crease max (l / r) | 53 / 58° | 47 / 52° | 41 / 47° | 55 / 61° | 46 / 52° | 45 / 52° |
| Transition max | 0.062 | 0.066 | 0.069 | 0.066 | 0.070 | 0.073 cm |
| Ear–head clearance min | 0.97 | 0.73 | 0.69 | 0.87 | 0.72 | 0.78 cm |
| Measured chord / body angle | 8.66 cm / 22.3° | 9.70 / 27.2° | 10.56 / 32.0° | 8.37 / 22.3° | 9.37 / 27.2° | 10.20 / 32.0° |
| Head / neck readiness (8 poses) | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |

On every realization:
- 100 % quads; one mesh; 0 boundary, non-manifold or degenerate faces; outward normals;
- root valence 4 (52 / 52);
- outside the branch byte-identical to the family realization;
- no seam, float or burial;
- density 0.095–0.109 % of stature.

**Quality is better than the Fenn v002 benchmark** (T-4 4.4 / 3.9 %). The guard held 2 faces on AELF190 AE-E1 and none elsewhere.

**Anatomy is present on all candidates** (sheet AE_12): helix, antihelix stem and crura, triangular fossa, cymba / cavum, crus of helix, tragus, antitragus, intertragic notch, lobe, upper extension and a continuous taper.

**Probes on AE-E2, c1** (projection 14 / 34°, tilt 22 / 38°, sweep 1.1 / 2.3, length ±10 %, tip blunt / sharp):
- T-4 91–165, aspect ≤ 8.34;
- 0 self-intersections; no broken root;
- **10 / 10 move the intended measure in the intended direction.**

## C5. Fenn-vs-Aelari visible-ear firewall (§18)

Comparison is at matched presentation (head-height / length normalised): Aelari AE-E2 on AEL1 vs frozen Fenn E2 on FN_M.

| | Aelari AE-E2 | Fenn E2 |
|---|---|---|
| Projection (auricle–body angle) | **27.2°** | 52.7° |
| Lateral extent / length (closeness to the skull) | **0.26** | 0.32 |
| Upper extension (side-view axis) | **38.0°** (more upward) | 32.3° |
| Width / length (taper) | **0.33** (cleaner, narrower) | 0.38 |
| Length / head height | **0.39** (moderate-to-long) | 0.35 |
| Sweep / length | 0.12 | 0.10 |

This is a coordinated difference in trajectory, projection, upward orientation, taper distribution and head integration (sheet AE_18). It is not "Fenn scaled longer" or "Fenn rotated up".

Shared ancestry is visible in the same root interface and in the internal cartilage layout: the W1e elven relief family, where Aelari has a slightly lower antihelix and concha.

**Recommendation: AE-E2** (balanced central = canon evidence).
- AE-E1 reads restrained but still clearly non-human.
- AE-E3 is the stronger option; it stays closer-set than Fenn.
- No refinement is technically required (T-4 3.1–3.2 %, no residual cluster).

---

## Visual package (`sheets/`, 21 sheets)

| Sheets | Content |
|---|---|
| AE_01 | AEL1 vs AELF190 |
| AE_02 | source vs production |
| AE_03 | equal-height Aelari vs Fenn, ears hidden |
| AE_04 | vs Marchfolk / Sagekin |
| AE_05 | body regions |
| AE_06 | hidden-ear face |
| AE_07 | validator margins |
| AE_08 | density |
| AE_09 | deformation |
| AE_10 – AE_15 | ears: head / rear-top / anatomy / wire-poles / T-4 / root, for c1 and c2 |
| AE_16 | sections |
| AE_17 | c1 vs c2 AE-E2 |
| AE_18 | Fenn E2 vs Aelari AE-E2 |
| AE_19 | hidden-ear confirmation |
| AE_20 | readiness poses + probes |

## Required answers (§21)

| Question | Answer |
|---|---|
| Was a valid ~190 cm c2 central reference created? | **Yes.** AELF190, 190.00 cm, deterministic (\|dV\| 0 three ways), inside 168–221 cm. Candidate pending author acceptance. |
| Does it preserve Aelari vertical-continuity anatomy? | **Yes.** Central vertical share > Fenn, extremity share < Fenn, and neck / torso / waist / cranium / pelvic vertical all > Fenn. Two **inherited AEL1 ties** for the author: ribcage vertical ≈ Fenn, and AEL1 lower-leg weighting ≈ Fenn. |
| Are both body realizations 69 / 69 D1–D6? | **Yes.** |
| Does equal-height hidden-ear Aelari vs Fenn body identity pass? | **Yes.** Vertically continuous vs compact-centred / extremity-emphasised; 1.1–6.2× the human baseline per region. |
| Does hidden-ear Aelari facial identity pass? | **Yes.** 7 / 7 systems material on both configurations; distinct from Fenn. |
| Is craniofacial source authoring required? | **No.** |
| Does the current source lack final Aelari ear anatomy? | **Yes.** It is the MPFB human auricle (reported as non-final). |
| Could Fenn v002 topology engineering be reused without reusing Fenn geometry? | **Yes — REUSE PASS.** Identical face list; wholly Aelari geometry. |
| Were AE-E1 / E2 / E3 built on one topology? | **Yes**, for both configurations. |
| Which ear candidate is recommended? | **AE-E2.** |
| Does Aelari remain clearly related to but distinct from Fenn? | **Yes.** Shared elven foundation (trunk, orbit, brow, ear root and relief family); distinct vertical distribution, facial verticality, eye presentation and ear trajectory / projection / taper. |
| Is any non-ear topology branch required? | **No.** |
| What should the next author decision be? | (1) Accept AELF190 as the c2 central reference. (2) Rule on the two inherited AEL1 ties: keep, or order an AEL1 source refinement (ribcage vertical, thigh / shin distribution). (3) Select the Aelari ear (AE-E2 recommended) and confirm the Fenn v002 engineering reuse. (4) Then order Aelari final consolidation. |

**STOP FOR CHATGPT REVIEW.** The following were not started or changed: Aelari freeze, Vael, Halvren, frozen Fenn, MPFB Family Base v005, any universal elf topology, ear rigging, creator morphs, UV / materials, LODs, UE5.
