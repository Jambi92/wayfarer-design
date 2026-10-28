# RAC RP3 — Vael ear prototypes (VA-E1 / VA-E2 / VA-E3) on the proven elf engineering topology — gate

**Date:** 2026-10-28
**Order:** `reviews/chatgpt-rac-rp3-vael-ear-prototype-order.md` (87eab2c)
**Evidence:** `reviews/rac-rp3-evidence/vael_rp3_ear_prototype/` (22 sheets in `sheets/`)
**Final-consolidation plan:** `reviews/claude-rac-rp3-vael-final-consolidation-plan.md` (prepared, not executed)

**Tools** (`tools/rac/rp/vael_rp3_v001/`):

| Tool | Role |
|---|---|
| `run_va_ear.sh` | builds, guard, audit, measure, blends, probes |
| `va_ear_summary.py` | summary record, firewall, regression |
| `va_ear_export.py` | topology / map / geometry records |
| `va_ear_sheets.py` | sheets |

**Shared Fenn ear tools** (additive, inert for Fenn / Aelari):
- `ear_branch_lib.py`: `CAND` VA-E1 / E2 / E3 (`W1V`).
- `ear_build.py`: candidate-level `geo` override.
- Frozen Fenn E2 and Aelari AE-E2 rebuild byte-identically with the edited tools (`VAEL_EAR_frozen_ear_reproducibility.json`, dV 0).

**E: (review files, not frozen):** `…/RaceBodies/production/Vael/RP3/ear_branch/` (6 prototype blends + records). Read back byte-identical.

## RESULT — VAEL EAR PROTOTYPE PASS — VA-E2 RECOMMENDED

All three candidates pass every hard technical gate on both configurations, on one topology. VA-E2 gives the clearest Vael ear read and carries the shape probes.

Two measured points are disclosed for author selection (§6). Both are measurements, not failures:
- The ear tip stands off the skull a little further than Fenn's.
- The measured length is shorter than the proposal estimated.

## 1. Author decisions recorded (§1–§2)

- **Accepted and unchanged:**
  - R1 + VD2 + VF2 body;
  - VC2 face;
  - pelvis 9 / 9;
  - human and three-elf firewalls PASS.
- **Unchanged inputs:** sha256 of every VF2 / VC2 source, the v004 family, v005, the frozen Fenn / Aelari records and the Fenn ear topology are equal to the previous gate (32 / 32, `immutable_hashes.txt`).
- **VAEL-CF-SHOULDER-1:** registered in `specs/RAC_PRODUCTION_RIG_CARRY_FORWARD_REGISTER.md` (new Vael RP3 section) and in the STATUS notes. Class: RIG / WEIGHT / SHOULDER-CORRECTIVE CARRY-FORWARD; VF2 anatomy not reopened.

## 2. Topology (§3, §4, §6, §11, §13)

**Reuse is engineering connectivity only.** `topology/VAEL_EAR_BRANCH_TOPOLOGY_v001.json` proves equality to `FENN_EAR_BRANCH_TOPOLOGY_v002`:
- sheet layout (s, t) and faces;
- cuff canon (read-only);
- face list, part / side labels;
- v005 → branch map (`mapping/VAEL_EAR_BRANCH_MAP_v005_v001`).

All 6 realizations and all 12 probes have the identical face list:
- 58,944 V / 58,942 Q, 100 % quads;
- face-topology sha equal to frozen Fenn and frozen Aelari.

| Reused | Not carried |
|---|---|
| 52-vertex root interface per side (v005 root loop, valence 4 on all 52) | No Fenn vertex geometry, projection, taper, tip, base width or orientation |
| cuff; tapered-leaf block; guard | Every vertex position is Vael (VA parameters on the VF2 + VC2 heads) |

- No universal elf-ear design is declared.
- **c1 / c2:** one topology, one parameter set per candidate. Geometry adapts only through head scale (HH 23.04 / 22.19 cm), root frame and the deterministic construction.
- **Determinism:** VA-E2 rebuilt independently, dV 0 on both configurations (`VAEL_EAR_determinism.json`).

**Was a Vael-derivative topology needed? No.** The broad Vael base did stress the reused **engineering pipeline**, not the connectivity. Two bounded, documented settings resolved it:

| Setting | Problem it fixes | Effect |
|---|---|---|
| **Concha clearance 0.15 cm** (Fenn / Aelari 0.05), a Vael geometry value in `CAND VA-E*` | At 0.05 the broad, backward base sits on the cuff. The v002 quality pass then freezes contact faces (VA-E3 c2: min corner 4.2°, cuff T-4 56). | At 0.15: cuff T-4 17, min corner 19.8°. Cost: about +0.1 cm tip stand-off. |
| **`EAR_UNT_MODE=contacts`** | The v002 "full" untangle adds cuff-aspect rounds that lower cuff vertices toward the head. On VA-E2 c2 these created 3 contacts at the 80-round cap. | The 3-D quality pass and aspect repair are unchanged. |

## 3. Technical gates (§11, §12, §15)

`VAEL_EAR_prototype_summary.json`; zones in `ear/VAEL_EAR_zone_report.json`.

| | VA-E1 c1 | VA-E2 c1 | VA-E3 c1 | VA-E1 c2 | VA-E2 c2 | VA-E3 c2 | Frozen Fenn E2 | Frozen AE-E2 |
|---|---|---|---|---|---|---|---|---|
| T-4 (of 3,718) | 132 | **127** | 123 | 135 | **132** | 125 | 165 / 145 | 117 / 120 |
| cuff T-4 | 14 | 15 | 17 | 15 | 18 | 17 | 57 / 39 | 9 / 12 |
| aspect max (> 10) | 9.30 (0) | 9.26 (0) | 9.44 (0) | 9.30 (0) | 9.26 (0) | 9.46 (0) | 9.29 / 8.71 | 8.28 / 8.55 |
| min corner | 26.4° | 25.9° | 13.6° | 26.4° | 14.4° | 19.8° | 7.9° / 12.7° | 20.0° / 20.0° |
| branch self-intersection | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ear–head clearance min (cm) | 0.97 | 0.95 | 0.89 | 0.85 | 0.83 | 0.74 | 0.38 / 0.45 | 0.73 / 0.71 |
| root crease max | 60° | 58° | 57° | 62° | 59° | 57° | 64° | 52° |
| transition ring max (cm) | 0.057 | 0.058 | 0.059 | 0.061 | 0.062 | 0.063 | 0.057 | 0.065 |
| density, mean edge / stature | 0.103 % | 0.106 % | 0.109 % | 0.099 % | 0.102 % | 0.105 % | 0.098 % | 0.103 % |
| guard iterations | 0 | 0 | 1 | 0 | 1 | 0 | 1 | 0 |
| head / neck poses: new contacts / flips / root inversions | 0 / 0 / 0 on all 8 (every candidate, both configurations) | | | | | | | |

Notes on the table:
- **Every realization:** 1 component, 0 boundary / non-manifold / degenerate, outward normals, root valence 4 (52 / 52 per side). The density limit is 0.25 %.
- **T-4** sits between the frozen Aelari and Fenn classes, with the cuff close to Aelari. There is no regression to Fenn v001-style tip / cuff distortion. The sharpest cells (13.6–14.4°) are root-band / band-0 cells, sharper than Aelari and at or above the accepted Fenn class.
- **Root deviation** (cuff skin vs the hidden-ear skull) has a mean of 0.38–0.46 cm, in the Aelari class (0.35–0.41).
- **Head / neck poses:** neck flex / extension 30°, yaw ±45°, pitch ±20°, roll ±20° (sheet 21). No seam opening and no ear–head / ear–neck collision.

**Anatomy (sheet 12, 13a):** every system is present on every candidate:
- helix continuous into the upper extension;
- antihelix stem + superior / inferior crura;
- triangular fossa, cymba / cavum, crus of helix;
- tragus, antitragus, intertragic notch;
- integrated lobe (no lobe-cuff knob).

The point grows from the helix / leaf structure, not from an extruded human tip.

**Thickness** (median / p05 / upper extension): about 0.31 / 0.29 / 0.43 cm on every candidate (Fenn 0.29 / 0.28 / 0.41). No paper-thin tip.

## 4. Hidden-ear regression (§14)

**Outside the ear branch, every realization is byte-identical to the accepted VF2 family body:**
- 55,378 v005 vertices, max |dV| 0;
- only the bounded 102-vertex transition ring moves (≤ 0.063 cm), as for Fenn and Aelari.

So the following are unchanged by construction:
- VF2 body and VC2 face;
- hidden-ear human firewall PASS, three-elf body firewall PASS, pelvis 9 / 9.

The sources themselves are untouched (sheet 20; `hidden_ear_regression` in the summary).

## 5. Three-elf visible-ear firewall (§10)

Same configuration, matched presentation (head-height / length normalised). Values are mean of both sides, c1 (c2 within 0.004 / 0.1°).

| Measure | Frozen Fenn E2 | VA-E1 | **VA-E2** | VA-E3 | Frozen AE-E2 | Rule | E2 |
|---|---|---|---|---|---|---|---|
| Projection (auricle–body angle) | 52.7° | 32.3° | **37.4°** | 42.4° | 27.2° | Fenn > Vael > Aelari | ✓ all |
| Upward extension (tip above root / HH) | 0.185 | 0.152 | **0.149** | 0.149 | 0.202 | Aelari > Vael, ≈ Fenn | ✓ (Vael −19 % vs Fenn) |
| Max width / length | 0.378 | 0.444 | **0.448** | 0.451 | 0.335 | Vael broadest | ✓ all |
| Max width / HH | 0.132 | 0.139 | **0.147** | 0.155 | 0.130 | Vael broadest | ✓ all |
| Length / HH | 0.349 | 0.312 | **0.327** | 0.343 | 0.388 | shorter than Aelari; may overlap Fenn | ✓ all |
| Side-view chord, lobe → tip (backward) | 19.5° | 24.6° | **26.0°** | 26.6° | 22.9° | more backward than both | ✓ all |
| Upper-extension axis from vertical (backward) | 32.3° | 39.9° | **45.7°** | 49.8° | 38.0° | more backward than both | ✓ all |
| Tip angle at 1 cm (blunter = larger) | 32.9° | 37.7° | **34.5°** | 30.5° | 31.4° | shorter / blunter taper than Aelari | ✓ E1, E2; **✗ E3** |
| Tip stand-off from the skull / HH (reported) | 0.113 | 0.116 | **0.136** | 0.155 | 0.102 | — | see §6 |

**Read (sheet 19):** the ears are clearly related (same anatomy class, same root / cuff integration) but distinct populations.
- **Fenn:** the most laterally projected auricle body (largest auricle–body angle) and the most upright, narrow leaf.
- **Aelari:** long and upward, lies close to the head.
- **Vael:** the broadest base, an intermediate auricle angle, a tip carried clearly backward, a shorter / blunter taper.

None is bat-like, horn-like or a thick fin.

**Measurement note.** The earlier gates labelled the upper-extension axis angle (Aelari 38° vs Fenn 32°) "more upward". That angle is measured from vertical toward posterior, so a larger value is more **backward**.
- Upward extension is reported here directly as tip height above the root.
- On that measure Aelari remains the most upward (0.202 vs Fenn 0.185).

## 6. Points for author selection (disclosed)

**1. Tip stand-off.**
- Fenn keeps the greatest **projection angle**. That is the auricle–body (auriculocephalic) angle used by every elf gate so far: 52.7° vs Vael 37.4° vs Aelari 27.2°.
- But the VA-E2 tip stands **further off the skull than Fenn's**: 3.1 vs 2.6 cm on c1, 0.136 vs 0.113 HH.
- The cause: the reused construction bends the ear about a near-vertical hinge. A broader, more backward ear therefore carries its tip further behind the hinge and, at the same angle, further out.
- VA-E1 matches Fenn (0.116 / 0.112 vs 0.113 / 0.118), and VA-E3 exceeds it most.
- The probes show the levers. Projection −10° gives −0.016 HH; tilt −8° gives −0.009; sweep −0.6 gives −0.009.
- Reaching Fenn's stand-off at VA-E2's backward orientation would need about Aelari's angle (proj ≈ 25°), which would erase "intermediate projection".
- If the author wants stand-off ≤ Fenn as a rule, VA-E1 is the candidate, or VA-E2 with projection about 30°. That is a bounded refinement.

**2. Measured length vs the proposal estimate.**
- The proposal expected VA-E2 at length / HH 0.35–0.36, width / length 0.40–0.43 and an "upper extension" of 30–34°.
- Measured: **0.327, 0.448 and 45.7°**.
- The estimate mapped `L_ref` to measured lobe-to-tip length as Fenn's did. The higher Vael tilt and shorter taper shorten the lobe-to-tip chord (VA-E2 7.54 cm from `L_ref` 8.5 × 0.986).
- The 30–34° figure used the mislabelled angle above.
- VA-E3 lands at the expected length (0.343), but its taper is sharper than Aelari's.
- The order's construction targets were built as ordered. If the author wants the expected length on VA-E2's shape, the bounded refinement is `L_ref` about 9.0–9.1 with VA-E2's other values. The `len_p10` probe shows it stays clean: T-4 116.

## 7. Shape probes (§16, VA-E2, c1; sheet 22)

All 12 probes keep:
- the identical face list;
- 0 branch self-intersection, 0 boundary / non-manifold;
- root valence 4;
- aspect < 10.

Each measure moves in the intended direction.

| Probe | Measure | Value (base) | T-4 |
|---|---|---|---|
| projection −10 / +10° | auricle–body angle | 27.4 / 47.4° (37.4) | 126 / 129 |
| tilt −8 / +8° | side-view chord | 22.9 / 29.1° (26.0) | 121 / 146 |
| sweep −0.6 / +0.6 | sweep / length | 0.111 / 0.176 (0.143) | 148 / 138 |
| length −10 / +10 % | length | 6.69 / 8.39 cm (7.54) | **196** / 116 |
| tip blunt / sharp | tip angle | 55.0 / 21.1° (34.5) | 131 / 124 |
| base width −8 / +8 % | width / length | 0.419 / 0.479 (0.448) | 113 / 154 |

- The largest excursion is length −10 % (+69 T-4 cells in the front / back sheet; aspect 9.67, min corner 10.9°).
- It is comparable to the accepted Aelari probe excursion (tip sharp 117 → 165). It is not a catastrophic spike.
- These are readiness probes, not creator morphs.

## 8. Candidate scoring (§17)

`VAEL_EAR_candidate_scoring.json`; scores 1–5.

| Criterion | VA-E1 | **VA-E2** | VA-E3 |
|---|---|---|---|
| Vael identity | 3 | **4** | 4 |
| three-elf distinction | 3 | **4** | 3 |
| anatomical coherence | 4 | **4** | 4 |
| root integration | 5 | **5** | 4 |
| silhouette | 3 | **4** | 4 |
| backward orientation | 3 | **4** | 5 |
| broad-base read | 5 | **5** | 5 |
| non-caricature | 5 | **4** | 3 |
| topology quality | 4 | **5** | 4 |
| creator-readiness | 4 | **5** | 4 |
| c1 / c2 consistency | 5 | **5** | 5 |
| **Total** | 44 | **49** | 45 |

- **VA-E1:** clean and restrained, stand-off equal to Fenn. Its backward lead over Aelari is small (chord +1.7°), so it reads closest to a generic short elf ear.
- **VA-E2:** the clearest Vael read on every canon direction.
- **VA-E3:** strongest backward read, but its taper is sharper than Aelari's (the one canon direction it misses), it has the largest stand-off, and its root cell is sharper.

**Recommendation: VA-E2.** It is provisional until author selection; see the §6 options.

## 9. Visual package (`sheets/`)

| Sheets | Content |
|---|---|
| 01–06 | front, rear, profile, 3/4 front, 3/4 rear, top |
| 07 / 08 | close profile / close rear |
| 09 / 10 / 11 | root closeup, wireframe, poles / valence |
| 12 | annotated anatomy |
| 13a / 13b | thickness; sections c1 / c2 |
| 14 | T-4 / aspect |
| 15 | density |
| 16 | root deviation |
| 17 | VF2 + VC2 head / body with the ears |
| 18 | c1 vs c2 VA-E2 |
| 19 | Fenn E2 \| Vael VA-E2 \| Aelari AE-E2 |
| 20 | hidden-ear regression |
| 21 | deformation readiness |
| 22 | shape probes |

Identical camera per configuration, true scale.

## 10. Answers (§21)

| Question | Answer |
|---|---|
| Is VF2 unchanged and accepted? | **Yes.** Hashes equal; byte-identical outside the branch. |
| Is VC2 unchanged and accepted? | **Yes.** |
| Is VAEL-CF-SHOULDER-1 recorded? | **Yes**: rig carry-forward register + STATUS. |
| Was the Fenn-v002 engineering topology reused cleanly? | **Yes.** Identical connectivity, cuff canon and map; frozen Fenn / Aelari reproduce byte-identically. Two documented engineering settings: concha clearance 0.15 cm, contacts-only untangle. |
| If not, why was a Vael derivative required? | Not required. |
| Do c1 / c2 and VA-E1 / E2 / E3 share one topology? | **Yes**: one face list for all 6 realizations and 12 probes. |
| Is required ear anatomy present? | **Yes**, every system on every candidate. |
| Is Vael clearly distinct from frozen Fenn / Aelari ears? | **Yes**: broadest base, intermediate angle, backward tip, shorter / blunter taper. |
| Does Fenn retain greatest average lateral projection? | **Yes by projection angle** (52.7° vs 37.4°). **No by tip stand-off:** VA-E2 tip 3.1 vs 2.6 cm; VA-E1 ≈ Fenn (§6). |
| Is Vael the broadest-base elf ear? | **Yes** (w/L 0.45 vs 0.38 / 0.34; w/HH 0.147 vs 0.132 / 0.130). |
| Do integrity, T-4, aspect and density pass? | **Yes** on all 6. |
| Is root integration clean? | **Yes**: valence 4, crease ≤ 62°, transition ≤ 0.063 cm, no seam / floating / buried root. |
| Does static deformation readiness pass? | **Yes**: 0 / 0 / 0 on 8 poses × 6 realizations. |
| Do shape probes pass? | **Yes**: 12 / 12. |
| Which VA-E candidate is recommended? | **VA-E2.** |
| Is Vael ready for final consolidation after author selection? | **Yes.** The plan is prepared (not executed); a bounded refinement per §6 is the alternative. |

**Not done, per the stop rules:**
- no Vael freeze, no Halvren;
- frozen Fenn / Aelari, v005, VF2 and VC2 not modified;
- no low-light physiology;
- no creator morphs, production ear rig, UV / materials, LODs or UE5.

**STOP FOR CHATGPT REVIEW.**
