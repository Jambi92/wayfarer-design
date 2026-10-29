# RAC RP3 — Halvren bounded central mixed body + craniofacial source gate

Order: `reviews/chatgpt-rac-rp3-halvren-body-face-source-order.md` (d2cac0e, 2026-10-29).
Evidence: `reviews/rac-rp3-evidence/halvren_rp3_body_face_source/` (22 sheets `HVBF_01..20b`).
Tools: `tools/rac/rp/halvren_rp3_v001/` (`hv_defs.py`, `build_hb.sh`, `hv_eval.py`, `run_hveval.sh`, `hv_bf_technical.py`, `build_hp.sh`, `hv_pelvis_pkg.py`, `hv_bf_manifest.py`, `run_hv_bf_prod.sh`, `hv_bf_sheets.py`).
Workspace: `/tmp/claude-0/rt/hv/{hb,hbe,hp,hbprod}`.

## RESULT

## HALVREN CENTRAL MIXED BODY/FACE PASS — READY FOR PELVIS AUTHOR DECISION

### PELVIS AUTHOR DECISION REQUIRED (HP-A / HP-B / HP-C, §6)

- **Recommended central pair: HB2 + HF2**, on both configurations.
- It departs materially from Marchfolk across 7 of 9 body systems and in 3 of 7 face regions (12–13 / 15 descriptors).
- It stays distinct from every frozen elf.
- It is not a scalar blend (see §3 for the one caveat).
- It carries cleanly on frozen v005: 69 / 69 D1–D6, exact topology, 0 new contact class.
- The pelvis is held. Ears stay locked. Nothing is frozen.

## Answers (§23)

| Question | Answer |
|---|---|
| HVF178 construction foundation still accepted? | **Yes.** c2 = MF-F-R route + the same overrides as c1, stature re-solved. |
| Recommended body candidate | **HB2** |
| Recommended face candidate | **HF2** |
| Recommended body × face pair | **HB2 + HF2** |
| Body departs materially from Marchfolk across multiple systems? | **Yes.** 10 / 11 of 31 metrics are material (current HVC1: 2). Signal in torso, shoulder / clavicle, leg, joints, foot, head / neck, and the pelvis-ratio coupling (7 / 9 groups). |
| Still distinct from all frozen elves? | **Yes.** Material differences: c1 FN 16, AE 11, VA 12; c2 FN 13, AE 11, VA 9. |
| Arithmetic-average firewall passes? | **Yes, with one caveat.** The best single-α fits are R² 0.51 (c1) and 0.70 (c2), both MF→Fenn with α 0.24–0.27. There is no t clustering at 0.5 (t medians 0.37–0.42). The neck runs opposite to Fenn and the knee / ankle stay human. The c2 MF→Fenn coherence is the weakest point (§3). |
| Face departs materially from Marchfolk across multiple regions? | **Yes.** Cranium, cheeks / midface and jaw / chin (3 / 7 regions; c1 and c2 alike). |
| Anti-beauty firewall passes? | **Yes.** No eye-size, nose or jaw-breadth target is used. The lower face gets *longer* (+2.0 %). The mixed read comes from the cranial form, cheek placement and chin height. |
| c1 / c2 share one mixed design logic? | **Yes.** One definition (`HVDEF1`) with identical overrides. Per-metric Halvren − Marchfolk offsets agree between configurations. |
| v005 technically sufficient? | **Yes.** All 10 propagated candidates are 69 / 69 and pass the technical gates. |
| Non-ear topology branch required? | **No.** |
| HP-A / HP-B / HP-C, and recommendation | See §6. **Recommend HP-B (mild mixed relational)** with HP-A as the conservative fallback. |
| Ears still locked? | **Yes.** No HT / HV-E work was done. |
| Next author decision | Accept HB2 + HF2 as the central pair and choose the pelvis direction (§8). |

## 1. Source definition `HVDEF1` (`hv_defs.py`; `definitions/HV_source_definitions.json`)

It uses existing MPFB targets and bone scales only:
- no custom field;
- no mesh blending;
- no copied source geometry.

One shared definition is applied at three strengths:
- body HB1 / HB2 / HB3 = ×0.6 / 1.0 / 1.5;
- face HF1 / HF2 / HF3 = ×0.85 / 1.1 / 1.45.

c1 = HVC1 record + overrides (the HVC1 keys are rewritten). c2 = MF-F-R base + the same overrides. Stature is re-solved to 178 cm.

**Body systems (HB2), each with its own mixed relation rather than an elf package:**
- **Axial:** ribcage girth reduced (`measure-underbust-circ-decr` 0.25) with depth kept near human (`torso-scale-depth-decr` 0.05). The result is a smaller ribcage of human proportion (thorax d / b −0.2 %, breadth −2.2 %). This is not Fenn's shallow torso or Vael's depth.
- **Shoulder / neck:** `measure-shoulder-dist-decr` 0.15 and `measure-neck-height-incr` 0.15. The neck is longer, in the Aelari direction but far from Aelari's neck package.
- **Arm:** upper arm +0.08 and forearm +0.15 length, with upper / lower arm shaft X / Z 0.98 (Fenn uses 0.95), and wrist −0.2.
- **Leg:** thigh +0.08 and lower leg +0.15, with shaft X / Z 0.985 and ankle −0.15. The knee stays human (no knee target).
- **Hand:** fingers +0.18, hand +0.06.
- **Foot:** foot +0.10, depth +0.05. Breadth stays human.
- **Pelvis:** **no pelvic target or bone scale** (held).

**Face (HF2):**
- **Cranium:** occipital depth reduced (`head-back-scale-depth-decr` 0.275) plus a mild oval.
- **Forehead:** forehead height +0.066, temple −0.165.
- **Cheeks / midface:** cheekbone placement raised (`cheek-trans-up` 0.385) with slightly reduced cheek volume.
- **Jaw / chin:** chin height +0.13. Jaw width untouched.
- **Orbit:** orbits slightly wider-set (`eye-trans-out` 0.11).
- **Nose and mouth:** untouched.
- **Eye size:** untouched.

**Determinism:**
- independent rebuild of HB2HF2: max |dV| 0 on both configurations;
- regeneration identical (dV 0) on all 10 propagated candidates;
- the 16 candidate records are in `reviews/reference-assets` (r6 / build / meas; CANDIDATE).

## 2. Body gate (178 cm, ears hidden; the parent gate's 31-metric architecture)

`eval/HB_eval_c{1,2}.json`. Material metric differences (of 31):

| | vs MF | vs SG | vs SK | vs FN | vs AE | vs VA | groups with signal vs MF |
|---|---|---|---|---|---|---|---|
| current HVC1 / HVF178 | 2 / 2 | 3 / 2 | 26 / 24 | 14 / 11 | 18 / 12 | 10 / 8 | 2 / 2 |
| HB1 | 5 / 4 | 3 / 3 | 24 / 23 | 16 / 11 | 14 / 11 | 14 / 10 | 7 / 6 |
| **HB2** | 8 / 8 | 7 / 9 | 25 / 23 | 15 / 13 | 12 / 13 | 14 / 10 | 7 / 7 |
| HB3 | 15 / 14 | 9 / 9 | 26 / 24 | 14 / 12 | 14 / 15 | 13 / 12 | 9 / 9 |
| **HB2 + HF2** | **10 / 11** | 10 / 11 | 23 / 21 | 16 / 13 | 11 / 11 | 12 / 9 | 7 / 7 |

(c1 / c2.)

**HB2 + HF2 minus Marchfolk:**

| System | c1 | c2 |
|---|---|---|
| Torso share | −1.7 % | −1.7 % |
| Thorax depth | −2.4 % | −2.7 % |
| Thorax breadth | −2.2 % | −2.3 % |
| Shoulder joint | −2.0 % | −2.3 % |
| Arm share | +1.9 % | +2.0 % |
| Forearm / upper arm | +2.2 % | +2.5 % |
| Elbow / humerus | −2.7 % | −3.1 % |
| Wrist / forearm | −4.5 % | −4.6 % |
| Knee / femur | −0.5 % | −4.5 % (the c2 thigh shaft) |
| Shin / thigh | +1.6 % | +1.7 % |
| Hand share | +3.6 % | +3.9 % |
| Finger / hand | +4.0 % | +4.3 % |
| Foot share | +1.8 % | +2.3 % |
| Neck share | +3.5 % | +3.1 % |
| Neck / torso | +5.3 % | +4.9 % |

**Nearest source per metric (HB2 + HF2):**
- c1: SG 9, VA 8, AE 7, MF 3, SK 2, FN 2.
- c2: AE 9, VA 7, SG 5, SK 4, FN 4, MF 2.

So no source dominates. Compare current HVC1: MF 12, SG 7.

**Visual (sheets 01–05):**
- HB2 reads as one organism: a longer neck and limbs on a slightly smaller ribcage, slimmer wrists and ankles, longer hands and feet. The joints stay coupled to their shafts.
- It is visibly more mixed than HVC1, and not a generic half-elf (the torso keeps human proportion).
- HB1 is the human-forward end. HB3 starts to read lean / elf-coded in the limbs and hands (its 15 / 14 Marchfolk departures push toward the thin guard of §6).

## 3. Arithmetic-midpoint firewall (sheet 06)

For each pair: n metrics with a material gap, t median [IQR], metrics in the 0.35–0.65 zone, and the single-α blend fit (α, R²):

| Pair | HB2 + HF2 c1 | HB2 + HF2 c2 |
|---|---|---|
| MF ↔ FN | 18: 0.37 [0.11, 0.42]; 10 in zone; α 0.24, R² 0.51 | 14: 0.37 [0.19, 0.44]; 8 in zone; α 0.27, R² 0.70 |
| MF ↔ AE | 17: 0.39 [0.16, 0.54]; 7; α 0.37, R² 0.61 | 13: 0.42 [0.38, 0.66]; 6; α 0.41, R² 0.59 |
| MF ↔ VA | 11: 0.57 [−0.09, 0.62]; 3; α 0.07, R² 0.06 | 10: 0.67 [−0.15, 0.70]; 0; α 0.12, R² 0.07 |
| SG ↔ FN | 15: 0.22 [0.09, 0.45]; 5; α 0.18, R² 0.24 | 12: 0.30 [0.09, 0.50]; 4; α 0.17, R² 0.26 |

The SK ↔ VA pair is reported but not used: the 178 cm Skarn diagnostic is far from every non-Skarn body.

**PASS.** The design is domain-specific:
- the neck sits at t ≈ −1.4 vs Fenn and ≈ +0.9 vs Aelari;
- the knee and ankle stay near the human end (t ≈ 0.1);
- the torso, shoulders and limbs move about a third of the way toward the elves.

No pair is fit at R² ≥ 0.8. The midpoint zone is not the centre of mass.

**Caveat for the author:** on c2 the MF→Fenn single-α fit explains 70 % of variance. The limb / torso systems share a recognisable "about a third toward Fenn" tendency, and the domain specificity is carried mainly by the neck, knee / ankle and the Vael-independent relations.

## 4. Face gate (hidden-ear, pigment-neutral; `eval/*`, sheets 08–15)

Aligned RMS vs Marchfolk (mm) by region; the departure threshold is 0.5 % HH (about 1.16 mm).

| Region | HF1 | **HF2** | HF3 |
|---|---|---|---|
| Cranium | 2.38 | **3.09** | 4.08 |
| Forehead | 0.51 | 0.66 | 0.87 |
| Orbit / eye | 0.36 | 0.46 | 0.61 |
| Nose | 0.25 | 0.32 | 0.42 |
| Cheeks / midface | 1.02 | **1.32** | 1.74 |
| Mouth | 0.17 | 0.22 | 0.29 |
| Jaw / chin | 1.21 | **1.56** | 2.06 |
| Regions departing | 2 / 7 | **3 / 7** | 3 / 7 |
| Descriptors departing | 8 | **12–13** | 14 |

(c1; c2 within 0.05 mm.)

**HF2 vs the frozen elves** (regions with RMS > threshold):
- vs Fenn 6 / 7;
- vs Aelari 5 / 7;
- vs Vael 3 / 7 (cranium 2.1, cheeks 1.75, jaw / chin 2.37 mm). Vael's own face is close to human in the forehead, orbit, nose and mouth.
- Descriptors also separate it from Vael: face height / bizygomatic +5.9 %, midface −6.4 %, cranial / face −3.3 %.

**HF2 descriptors** (Halvren vs Marchfolk; position 0 = human mean, 1 = elf mean):

| Descriptor | vs MF | Position |
|---|---|---|
| Cranial height / stature | +1.9 % | 0.90 |
| Skull breadth / HH | −1.5 % | 0.73 |
| Brow projection | −2.2 % | 0.88 |
| Cheekbone height | +2.3 % | 1.26 |
| Midface projection | −2.7 % | 1.20 |
| Bizygomatic / HH | −1.5 % | 0.82 |
| Jaw width / bizygomatic | −1.2 % | 0.59 |
| Lower-face height / HH | +2.0 % | (longer) |
| Nose, mouth, eye size | 0 | unchanged |

This is a regional mosaic: an elf-leaning cranium and cheek placement, a human nose / mouth / mandibular breadth, and a longer chin.

**Anti-beauty firewall: PASS.**
- No eye enlargement and no nose change.
- No jaw-breadth target. The jaw / bizygomatic ratio falls 1.2 % only because the cheek width shifts.
- The lower face gets longer, not smaller.
- No symmetry or smoothing change.

HF3's cheekbone height (position 1.65) and midface (1.57) overshoot the elf mean. **HF3 is elf-coded in the cheeks.**

**Expression sanity** (`expression/HV_expression_sanity.json`, sheet 16):
- Neutral, blink, look up / down (lid follow), smile, anger, surprise and sadness all match the current face's generic MPFB pattern: the same contact / flip classes.
  - blink: 122–154 lid pairs (current 122 / 140);
  - sadness: 228–232 / 191–197;
  - anger: 108 / 60.
- These are generic MPFB expression-unit artifacts, not source-anatomy failures.
- **Fear** has no distinct skin unit in the MPFB 2.0.17 unit set used by `cf_expr.py`. It is covered by the surprise + sadness units. Eye movement is eyeball-only.

## 5. Body × face pair matrix (sheets 17, 18)

| Pair | Body vs MF (c1 / c2) | Face regions | Read |
|---|---|---|---|
| HB1 + HF1 | 7 / 8 | 2 | human-forward mixed |
| **HB2 + HF2** | **10 / 11** | **3** | **balanced central** |
| HB3 + HF3 | 15 / 14 | 3 | strongest; limbs and cheeks elf-coded |
| HB2 + HF1 | 9 / 10 | 2 | mixed body with a subtle face (valid) |
| HB2 + HF3 | 10 / 11 | 3 | mixed body with a stronger face (valid) |

The face results are identical across bodies (HB1 + HF1 = HB2 + HF1 to 0.01 mm), so body and face vary independently. There is no locked phenotype package.

**Recommended central production-anchor pair: HB2 + HF2.** It is the most balanced: not the most obviously mixed, clear in both domains, with human-family overlap kept.

## 6. Pelvis

**Held during this pass.** There is no pelvic term. Every pelvic delta of HB2 + HF2 vs the current anchor is ratio coupling from the longer neck / legs at the same stature:

| Measure | c1 | c2 |
|---|---|---|
| Bitroch / crest | −0.25 % | similar |
| Pelvic depth | −1.0 % | similar |
| Pelvic vertical | −0.8 % | similar |
| Crest share | −1.0 % | similar |
| Waist / torso | −0.3 % | similar |
| Leg share (hip-joint height) | −0.2 % | similar |

All are disclosed in `pelvis_package/HV_pelvis_package.json → candidates`.

**Author-decision package** (diagnostic builds on HB2 + HF2; skeletal proxy at t = 0.5; sheet 19). Values are vs MF / FN / AE / VA:

| | Construction | Pelvic vertical / crest | Crest / stature | AP depth | Hip-joint height |
|---|---|---|---|---|---|
| **HP-A** human-family-dominant | HB2 + HF2 as is | +0.2 / −0.2 / −9.6 / −3.4 % | −1.3 / +0.3 / +6.0 / −2.1 % | −1.7 % vs MF | +0.5 % vs MF |
| **HP-B** mild mixed relational | pelvis Y × 1.02 + `hip-scale-horiz-decr` 0.05 | +3.3 / +2.9 / −6.8 / −0.4 % | −2.5 / −0.9 / +4.7 / −3.3 % | −1.5 % | +0.3 % |
| **HP-C** stronger mixed | pelvis Y × 1.035 + `hip-scale-horiz-decr` 0.10 | +6.0 / +5.6 / −4.4 / +2.2 % | −3.7 / −2.1 / +3.4 / −4.5 % | −1.4 % | +0.3 % |

(c1; c2 is the same pattern within about 0.6 %.)

**Biomechanics:**
- **HP-A:** the stock human pelvis under a mixed body, with the lowest risk.
- **HP-B:** a slightly taller, slightly narrower iliac relation. Hip-joint height and bitroch / crest are unchanged, so leg alignment is unaffected. Its pelvic vertical / crest sits near Vael's (−0.4 %), but every other pelvic relation differs from Vael by 1–4 %.
- **HP-C:** a visibly narrower crest with a taller ilium. It is still not a copy (between FN and AE on vertical / crest), but it moves the waist / torso continuity 1.1 % and is the most likely to need corrective review at the hip.

**Recommendation: HP-B**, with HP-A as the conservative fallback. Neither is canonical.

## 7. Technical regression on frozen v005 (`technical/HV_bf_technical.json`, sheet 20)

All 10 propagated candidates (5 pairs × c1 / c2) are **technical PASS**:
- exact v005 topology (faces / UV / map identical), V = M @ hm08 max 0, 100 % quads;
- 1 component; 0 boundary / non-manifold / degenerate / coincident; normals outward;
- **69 / 69**;
- T-1 / T-2 / T-3 / T-7 (IoU ≥ 0.997);
- density (worst zone at 0.82–0.85 × its limit);
- 0 new contact class;
- face rings: mouth 33–36 rings, orbit 43 / 43, 0 poles at the mouth corners.

**Standard v1 deformation:**
- **Flips:** worst excess over Marchfolk v005 is +1 (c1) and 0 (c2).
- **Contacts, c1 thumb opposition:** 44–50 vs Marchfolk 24.
- **Contacts, c2 knee 90°:** 102–108 vs Marchfolk 87.
- Both contact excesses are already on the native source (21–25 vs Marchfolk native 12; 28–30 vs 22). This is the finger / lower-leg length (source anatomy), the same class as the accepted HVC1.

**Diagnostic production blends of HB2 + HF2:**
- `HV_M_REF_RP3_bodyfam_v002.blend` (`19697552…`) and `HV_F_REF_RP3_bodyfam_v002.blend` (`d06a5697…`);
- they read back equal to the candidate;
- they are on E: `Halvren/RP3/` with maps, landmarks, the candidate manifest and the definition file, read back byte-identical (`pc_readback_sha256.txt`).

Records:
- family candidate manifest: `HALVREN_RP3_bf_candidate_manifest.json`;
- source sidecars: `sources/`.

## 8. Next author decisions

1. **Accept HB2 + HF2** (`HVDEF1`) as the central Halvren mixed-expression body / face anchor.
   - The source records `HVC1-HB2HF2` / `HVF178-HB2HF2` are candidates. On acceptance they would be versioned like Vael R1.
   - Alternatively: ask for a bounded local revision to reduce the c2 MF→Fenn limb / torso coherence (§3), or tone down the cheekbone height if the author reads it as high-cheekbone styling.
2. **Choose the pelvis direction: HP-A, HP-B (recommended) or HP-C.** A pelvis author order then builds it into the anchor.
3. **Ears stay locked** until steps 1 and 2. Then the HT1 / HT2 / HT3 architecture study can be ordered.

## Not done (stop rules)

None of the following were done:
- no Halvren freeze;
- no ears;
- no pelvis canon;
- no change to frozen races or v005;
- no genealogy / randomization / ancestry-percentage controls;
- no creator morphs, rigging, UV, LODs or UE5.

**STOP FOR CHATGPT REVIEW.**
