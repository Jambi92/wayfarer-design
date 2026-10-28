# Claude gate — RAC RP3 Vael c2 central reference + three-elf hidden-ear identity + conditional ear branch

**Order:** `reviews/chatgpt-rac-rp3-vael-body-face-ear-order.md` (2026-10-28; after Aelari freeze `40f5a8a`)
**Evidence:** `reviews/rac-rp3-evidence/vael_rp3_v001/`

**Tools** (`tools/rac/rp/vael_rp3_v001/`):

| Tool | Role |
|---|---|
| `build_va_partA.sh` | VALF178 + 178 cm comparators |
| `skp_va.sh` | lean skeletal proxies + VALF178 regen / native |
| `va_partA.py` | canon, pelvis, determinism |
| `build_va_diag.sh` | ordering diagnostics |
| `run_va_prod.sh`, `va_manifest.py` | body-family candidates |
| `va_hidden_ear.py` | three-elf hidden-ear body + face |
| `va_sheets.py` | visual package |

The Standard v1 pipeline ran through `aelari_rp3_v001/run_aeeval.sh` (`AE_C1=VAL4`, `AE_C2=VALF178`).

## Result

# VAEL BODY SOURCE/BRANCH WORK REQUIRED

Craniofacial source work is **also** required (§6). Part C (ears) was **not unlocked** and was not started. Nothing is frozen.

**What passed:**
- **Part A:** the c2 central reference **VALF178** (178.01 cm) reproduces the accepted Vael design exactly and deterministically, with no c2-specific anatomy.
- **Part B:** both diagnostic body-family candidates pass every technical gate (69 / 69 D1–D6, anatomy, density, contact, face rings, deformation).

**The hard comparative gates do not all hold.**

1. **Ordering against the frozen (R1-corrected) Aelari at equal height fails (pelvis hard gate).**
   - VA-P2a: hip-joint height / stature must be below Aelari. It is **above** — c1 +0.43 %, c2 +0.23 %.
   - VA-P6 (c2): waist interval / torso must be below Aelari. It is **above** — +0.49 %.
   - These are small inversions, and they were caused by the accepted Aelari R1 correction:
     - Against the original AEL1 / AELF190 at 178 cm, the rows hold. c1 leg share is a tie (−0.03 %).
     - At 178 cm the corrected Aelari's hip-joint height sits only +0.21 % (c1) / +0.34 % (c2) above Marchfolk. That leaves almost no room for the required MF < Vael < Aelari ordering.
   - At 190 cm (Aelari's reference stature) Vael is also above Aelari on leg share and on both waist rows.
   - This needs an author decision (§9).
2. **The Vael body is close to Marchfolk.**
   - In the ears-hidden equal-height comparison, Vael–Marchfolk region RMS is **below** the human–human baseline (Sagekin–Marchfolk) in trunk, arm, hand, leg and neck.
   - The relational canon against humans holds, but narrowly (leg share +0.64 %, arm share +1.2 %).
   - Vael remains clearly distinct from Fenn and Aelari.
   - W1n already noted that separation from humans was expected to come "mainly from face and ears".
3. **The Vael face is the Marchfolk face.**
   - VAL4 carries no Vael craniofacial source. It is the Marchfolk head plus `eye-scale-incr` and `cheek-bones-incr`.
   - No face region departs materially from humans: every region RMS vs Marchfolk is ≤ 0.54 mm.
   - The Vael-vs-Aelari face canon holds (7 / 7 c2, 6 / 7 c1), but only because Aelari has an authored elven face.
   - This is "humans with pointed ears" with the ears hidden, so **VAEL CRANIOFACIAL SOURCE WORK REQUIRED** also applies.

**Not run, by the order's logic:**
- Expression sanity (§12): the hidden-ear face gate did not pass.
- Part C (ears): body and face did not pass.

## 1. Part A — VALF178 (configuration-2 central reference)

**Search:** no committed or local Vael c2 build existed (repository and `/tmp/claude-0/rt` both searched).

**Construction:** `build_variant.py` with:
- base `MF-F-R_build.json` (the shared c2 route used for MF-F / SGF178 / FNF181 / AELF190-R1);
- overrides = **exactly the VAL4 targets and bone scales**:
  - pelvis [1.02, 1, 1.03], thigh Y 0.98849, calf Y 1.02981;
  - spine_03 Y 0.9747, upperarm Y 0.99414, lowerarm Y 1.00565;
  - torso depth, hand, foot breadth, finger spacing, eye, cheek-bone, wrist / ankle / knee and lower-leg targets;
- stature 178, re-solved.

`cfg` differs from VAL4 only in gender and id. No sex-specific pelvic, facial or ear anatomy was authored.

| Check | Result |
|---|---|
| Stature | 178.014 cm (envelope 157.0 / **178.01** / 203.0) |
| Determinism: independent second full re-solve | height macro 0.64575 both; max \|dV\| 0.0; faces identical |
| Determinism: regen from the committed record | geometry identical |
| Native hm08 integrity | 1 component; 0 boundary / non-manifold / degenerate; outward |
| Records | `reviews/reference-assets/{r6,builds}/VALF178*`: r6 `3d5111c5…`, build `0efae39e…`; manifest **CANDIDATE**; sidecar `VALF178_central_reference_sidecar.json` |
| Configuration consistency (VALF178 − VAL4 vs MFF − MFM) | same sign on 16 / 17 rows |

## 2. Matched-stature identity (178 cm; Fenn / Aelari = the frozen sources re-solved to 178)

`partA/VALF178_reference_validation.json` holds 18 canon rows (VAEL L35–47, L114–154; W1n conventions).

| Row | c1 | c2 |
|---|---|---|
| torso share > Fenn | ✓ +3.2 % | ✓ +3.3 % |
| thorax depth > Fenn / Aelari | ✓ +9.2 / +10.4 % | ✓ +10.6 / +11.4 % |
| waist interval / torso < Aelari | ✓ −0.48 % | **✗ +0.52 %** |
| central vertical < Aelari | ✓ −0.44 % | ✓ −0.20 % |
| extremity share < Fenn | ✓ −3.0 % | ✓ −3.1 % |
| leg share > MF, < Fenn, < Aelari | MF +0.64 / FN −1.84 / **AE +0.43 ✗** | +0.58 / −1.93 / **+0.23 ✗** |
| arm share > MF, < Fenn (≤ Aelari, BM-3) | ✓ | ✓ |
| joint presence > Fenn / Aelari (elbow, wrist, knee, ankle) | ✓ all | ✓ all |
| broader palms than Fenn / Aelari | ✓ +7.0 / +1.2 % | ✓ +7.8 / +1.3 % |
| broader feet than Fenn / Aelari | ✓ +23 / +16 % | ✓ +22 / +15 % |
| hand share, foot share > MF | ✓ | ✓ |
| *balanced segments ~ MF (± 0.010)* | ✗ vs MF@178 (lower leg / thigh +0.026) — ✓ vs MF-M-R native | same |
| *gracile vs MF (elbow, knee)* | ✗ +0.4 / +0.5 % vs MF@178 — ✓ vs MF-M-R native | ✗ vs MF@178; c2 knee also ✗ vs MF-F-R native (+2.1 %) |

**Comparator stature** (the italic rows):
- The W1n / W1o acceptance read the balance and gracility rows against native Marchfolk (MF-M-R, 173 cm). On that reading VAL4 passes all of them.
- Re-solving Marchfolk to 178 cm moves its own segment ratios (lower leg / thigh 1.067 → 1.041). Skin joint breadths are already accepted as unstable across the stature macro (Aelari §19 precedent).
- I report both readings and do not treat these rows as the deciding failures.

## 3. Vael pelvis hard gate (skeletal proxy, t = 0 / 0.5 / 1.0)

| Rule | c1 | c2 |
|---|---|---|
| VA-P2a hip-joint height / stature > MF | ✓ +0.64 % | ✓ +0.58 % |
| VA-P2a < Fenn | ✓ −1.84 % | ✓ −1.93 % |
| **VA-P2a < Aelari** | **✗ +0.43 %** | **✗ +0.23 %** |
| VA-P2b bitroch / crest ≥ MF | ✓ +0.40 % | ✓ +0.45 % |
| VA-P3 no Aelari-style vertical iliac elongation | ✓ −10.7 % | ✓ −10.5 % |
| VA-P4 AP depth > Fenn / > Aelari / ≈ MF | ✓ +2.1 / +2.5 / +2.3 % | ✓ +2.5 / +3.8 / +2.3 % |
| **VA-P6 waist interval / torso < Aelari** | ✓ −0.50 % | **✗ +0.49 %** |
| VA-P2c hip-joint scale (proximal-femur proxy) > Fenn / > Aelari | report ✓ +6.2 / +8.3 % | report ✓ +5.6 / +6.8 % |
| VA-P2c gracile vs MF | report ✗ +0.45 % | report ✗ (+25 %: the female MF trochanter proxy is unreliable) |
| VA-P3 iliac presence (crest × AP depth) > Fenn / > Aelari | report ✓ +5.1 / +11.5 % | report ✓ +5.6 / +13.4 % |
| VA-P3 lighter than MF | report ✗ +3.6 % | report ✗ +3.7 % |

**Gating rows:** 8 / 9 hold on c1 and 7 / 9 on c2.

VA-P2c and VA-P3 are construction rules with **no accepted numeric proxy**. PV-D17 makes them visual for W1, and W1n classed hip-joint readings as "report only (spacing, not size)". The proxy rows above are reported, not gated. The visual check is sheet VA_07: pelvis construction reads moderately robust next to the elves and close to Marchfolk.
- No breadth shortcut: the pelvis bone scales equal VAL4's.
- No configuration-specific pelvis.
- Lumbar lordosis is natural and MF-like (VA_05 profile).

### Ordering diagnostic (`partA/VAEL_ordering_diagnostic.json`, sheet VA_15)

**Hip-joint height / stature (VA-P2a):**

| | c1 | c2 |
|---|---|---|
| Vael @178 | 0.53801 | 0.52918 |
| Marchfolk @178 | 0.53457 | 0.52614 |
| **Aelari R1 @178 (frozen)** | **0.53571** | **0.52795** |
| Aelari original (pre-R1) @178 | 0.53816 | 0.52998 |
| Vael @190 / Aelari R1 @190 | 0.54354 / 0.54198 | 0.53560 / 0.53444 |

**Waist interval / torso (VA-P6):**

| | c1 | c2 |
|---|---|---|
| Vael @178 / Aelari R1 @178 | 0.26841 / 0.26970 | **0.34060 / 0.33883** |
| Aelari original @178 | 0.27225 | 0.34217 |
| Vael @190 / Aelari R1 @190 | 0.27417 / 0.27189 | 0.34237 / 0.34085 |

**Reading:**
- The Aelari R1 correction (accepted 2026-10-28) lowered Aelari's leg share by about 0.4 % and its waist interval by about 1 %.
- Against the original Aelari, Vael's ordering held (c1 leg share a tie).
- Against the corrected Aelari it is inverted by 0.2–0.5 % at equal height, at both 178 and 190 cm.
- At 178 cm the window between Marchfolk and the corrected Aelari is only 0.21 % (c1) / 0.34 % (c2). Any Vael leg correction inside it could only reach sub-1 % ("NOT DEMONSTRATED") margins on both sides.

## 4. Part B — body-family candidates on frozen v005

Candidates: `VA_M_REF_RP3_bodyfam_v001` (VAL4) and `VA_F_REF_RP3_bodyfam_v001` (VALF178). Records are in `VAEL_RP3_bodyfam_propagation_manifest.json` and the sidecars. Both are on E:, read back byte-identical.

| Gate | c1 | c2 |
|---|---|---|
| Regen geometry identical; V = M @ hm08 (0.0); faces / UV / map = v005; face hash `ec768ae2…` | ✓ | ✓ |
| **D1–D6 firm** (without D6) | **69 / 69** (69) | **69 / 69** (69) |
| Margin-zero stations | thumb_mcp, toe1_j1, toe2_j1, toe4_j1 | toe1_j1, toe4_j1 |
| T-1 / T-2, T-3, T-7; IoU min | ✓; 0.9977 | ✓; 0.9981 |
| 9-zone density | all pass | all pass |
| Integrity | 1 component, 0 boundary / non-manifold / degenerate, outward | same |
| Self-intersection pairs | 68 | 122 |
| Contact source / family / new | 66 / 2 / 0 | 122 / 0 / 0 |
| Face rings (mouth / orbit; mouth-corner poles) | 32 / 43, 43; 0 | 33 / 43, 43; 0 |
| Deformation worst flip excess vs MF v005 | 3 (no pose > 5) | 1 (no pose > 5) |
| Read-back | 6.0e-8 m | 6.0e-8 m |

The ear zone is explicitly non-final: it is the family human auricle.

## 5. Three-elf hidden-ear body gate (§10)

Equal height 178 cm, matched frame / muscle / fat / age / pose. Ears collapsed; geometry-only grey shading (complexion, hair and presentation neutral). Source: `hidden_ear/VA_hidden_ear_identity.json`; sheets VA_03 – VA_09.

Region RMS in mm, c1 (c2 is the same pattern):

| Region | Vael vs Fenn | Vael vs Aelari | Vael vs MF | Vael vs SG | **human baseline SG vs MF** |
|---|---|---|---|---|---|
| trunk | 13.5 | 12.3 | **6.0** | 6.5 | 8.8 |
| arm | 12.2 | 11.8 | **1.7** | 3.9 | 4.3 |
| hand | 24.1 | 13.0 | **5.9** | 6.6 | 11.2 |
| leg | 18.6 | 12.2 | **7.5** | 5.4 | 7.6 |
| foot | 10.4 | 11.7 | 4.2 | 5.0 | 1.4 |
| neck | 3.2 | 6.5 | **1.4** | 2.4 | 1.5 |

**Against the elves:** Vael is clearly distinct from both and reads as its own population.
- Deeper thorax: +9 to +11 % vs Fenn and Aelari.
- Less extremity emphasis than Fenn.
- More joint and base presence; broader palms and feet.
- Less vertical than Aelari on the central share.

**Against humans:** separation is weak. Vael sits closer to Marchfolk than Sagekin does in five of six regions. The relational rows hold, but by margins of about 0.6–3 % (feet +9 %, ribcage +3.5 %).

**Hard-gate failures:** VA-P2a vs Aelari (both configurations) and VA-P6 c2 (§3).

**Verdict:** body identity does not fully meet the comparative canon. → **VAEL BODY SOURCE/BRANCH WORK REQUIRED.**

## 6. Hidden-ear / neutral-complexion face gate (§11)

Source: `hidden_ear/VA_hidden_ear_identity.json`; sheets VA_10 and VA_11.

| Vael system (vs Aelari unless noted) | c1 | c2 |
|---|---|---|
| less facial verticality | ✓ −6.8 % | ✓ −7.0 % |
| more compact craniofacial vertical distribution | ✓ | ✓ |
| broader cheeks / cheek-to-mid-face integration | ✓ +6.1 % | ✓ +6.2 % |
| more mid-face depth | ✓ +8.2 % | ✓ +8.6 % |
| somewhat broader orbits | ✗ −0.9 % (unstable orbit-breadth landmark) | ✓ +8.3 % |
| stronger brow-orbit, no scowl | ✓ +5.8 % | ✓ +11.0 % (brow equals MF, +1 %) |
| more mandibular presence than Fenn / Aelari | ✓ +2.3 / +4.3 % | ✓ +2.7 / +4.9 % |

**These pass only because Aelari and Fenn have authored elven faces.** Against humans:
- Every descriptor is within ±0.3 % of Marchfolk.
- Face region RMS vs Marchfolk after similarity alignment is ≤ 0.54 mm (cranium 0.05, forehead 0.04, orbit 0.20, nose 0.08, cheeks / mid-face 0.54, mouth 0.02, jaw 0.06).
- No region departs materially.

VAL4 has no Vael craniofacial source. The written canon describes a Vael face, but the source expresses a human face with enlarged eyes and cheek bones. → **VAEL CRANIOFACIAL SOURCE WORK REQUIRED.**

- **Low-light physiology:** none invented or evaluated (no pupil, retina, eye shine, glow or gameplay).
- **Expression sanity (§12):** not run, because the face gate did not pass.

## 7. Part C — ears

**Not unlocked.** The source still carries the MPFB human auricle (no committed Vael ear source exists).
- No VA-E1 / E2 / E3 were built.
- No topology reuse was tested.
- No ear sheets 15–25.

## 8. Visual package (`sheets/`)

| # | Sheet |
|---|---|
| VA_01 | VAL4 vs VALF178 |
| VA_02 | source → family |
| VA_03 | three-elf equal height, ears hidden |
| VA_04 | Vael vs Marchfolk / Sagekin + overlay |
| VA_05 | torso depth / profile bands |
| VA_06 | shoulder / neck |
| VA_07 | pelvis / waist (+ rule table) |
| VA_08 | arm / hand base |
| VA_09 | leg / ankle / foot base |
| VA_10 | hidden-ear neutral face, five populations |
| VA_11 | face regional residual heat maps (vs MF / AE / FN) |
| VA_12 | validator margins |
| VA_13 | density |
| VA_14 | deformation |
| VA_15 | ordering diagnostic |

Expression and ear sheets were not produced (gates not passed).

## 9. Answers

1. **Valid ~178 cm c2 central reference created?** Yes: VALF178, 178.01 cm, deterministic, integrity clean; manifest CANDIDATE.
2. **Reproduces the accepted Vael design without config-specific anatomy?** Yes: VAL4's targets and bone scales exactly; differs only in gender and id.
3. **Do all Vael pelvis rules hold?** **No.**
   - VA-P2a "< Aelari" fails on c1 (+0.43 %) and c2 (+0.23 %).
   - VA-P6 fails on c2 (+0.49 %), against the frozen R1 Aelari at equal height.
   - Holding: VA-P2a > MF and < Fenn, VA-P2b, VA-P3 (no vertical elongation), VA-P4.
   - VA-P2c and VA-P3 presence are report-only proxies (PV-D17 visual).
4. **Both family bodies 69 / 69 D1–D6?** Yes.
5. **Three-elf hidden-ear body identity passes?** **No.**
   - Vael is distinct from Fenn and Aelari, but the Aelari ordering fails.
   - The body is near-human (closer to Marchfolk than the human baseline).
6. **Does Vael remain elven against humans?** Relationally yes, but narrowly: leg +0.6 %, arm +1.2 %, hands +3 %, feet broader +9 %, ribcage deeper +3.5 %, gracile wrists and ankles. Visually it is close to Marchfolk.
7. **Hidden-ear neutral-complexion face identity passes?** **No.** It passes against Aelari only because the Vael face equals the Marchfolk face.
8. **Craniofacial source authoring required?** **Yes.**
9. **Any low-light physiology invented?** **No.**
10. **Does the source lack final Vael ear anatomy?** Yes: it carries the MPFB human auricle.
11. **Can the elf-ear engineering topology express Vael?** Not tested (Part C locked).
12. **VA-E1 / E2 / E3 built on one topology?** Not built.
13. **Recommended ear candidate?** None yet.
14. **Related to but distinct from Fenn and Aelari?**
    - Body: yes, distinct (RMS 12–24 mm), though inverted against the corrected Aelari on hip-height and c2 waist ordering.
    - Face: distinct from them only by being human.
15. **Is a non-ear topology branch needed?** No. Family topology is unchanged and 69 / 69.
16. **Next author decision:**
    - **(a) Elf ordering after Aelari R1.** Choose one:
      1. Authorize a bounded Vael body correction (lower hip-joint share and c2 waist interval). At 178 cm the MF–Aelari window is only 0.21 / 0.34 %, so the result would be sub-1 % ties.
      2. Rule that VA-P2a / VA-P6 against Aelari are read as distribution overlap (ECR "overlap locked").
      3. Rule that they are read at each race's reference stature, the W1 convention, where they hold: leg −0.73 / −0.98 %, waist −1.28 / −0.07 %.
    - **(b) Authorize a Vael craniofacial source pass.** This would be the analogue of Fenn CF1–CF3 and the Aelari face targets: deterministic MPFB face targets expressing the written Vael canon (compact vertical distribution, stronger mid-face / cheek integration, somewhat broader orbits, brow-orbit definition without scowl, more mandibular presence than Fenn / Aelari, shared elven cranial-height contribution), applied identically to c1 / c2.
    - **(c)** Optionally, a bounded body-separation-from-humans review.
    - Ears follow only after (a) and (b) pass.

## 10. Immutable state

`immutable_hashes.txt` confirms the following are unchanged:
- v005 blend and map, and the v005 freeze;
- the Fenn freeze `0bafdfb4…` and the Aelari freeze `bccd7865…`;
- VAL4 (r6 `ec73819d…`, matching the order);
- the Fenn / Aelari sources and the Fenn v002 topology.

Nothing frozen was altered. The Fenn / Aelari tools were used read-only through the environment switches that already exist.

**STOP FOR CHATGPT REVIEW.**
