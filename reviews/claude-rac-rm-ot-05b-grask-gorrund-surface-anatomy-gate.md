# RAC RM-OT-05B — Grask / Gorrund surface-anatomy gate

**Order:** `reviews/chatgpt-rac-rm-ot-05b-grask-gorrund-surface-anatomy-order.md`
**Parent:** RM-OT-05 stays **OPEN**. Not self-closed.
**Evidence:** `reviews/rac-rmot05b-evidence/` (see its README).
**New tool:** `tools/rac/w1/race_surface.py`. It is the race-surface stage. It defaults to **OFF**, and every accepted non-Grask / non-Gorrund body rebuilds unchanged.

---

## 0. Result

**Overall: does NOT pass. NEEDS ART / BASE-SURFACE ESCALATION.**

Gorrund now meets every numeric blind criterion: 12 / 12 correct, all three scorers placed the reference in the right family, and no human-family control was pulled in. But every scorer still says an uninformed viewer would call it a "stocky / heavy human".

Grask reaches exactly the 10 / 12 floor in the final run (8–10 across three runs), but a thin Marchfolk control is pulled into Grask by 2 of 3 scorers, and every scorer says Grask reads as a "lanky human" whose call follows thinness.

The §9 standard requires both the counts and that the explanations stop being "lanky / stocky human". Neither race meets the explanation criterion.

| Item | Result |
|---|---|
| Author ruling (standard kept; 05A = structural intermediate) | acknowledged; nothing in canon rewritten |
| Race surface-anatomy stage built, separate from architecture and composition, default OFF | **YES** (§1) |
| Gorrund knee vs Skarn (femur-normalized, existing row) | **PASS** at 208 / 218 / 229: 0.334 / 0.314 / 0.295 vs Skarn 0.309 / 0.297 / 0.290 (+8.1 / +5.8 / +1.6 %). Ankle, wrist and elbow ordering kept (§4). |
| 05A residuals | **Fixed:** Narrow Gorrund 218 knee hold (now −0.6 %); Gorrund 208 lumbar-depth rows; S5/S2 margins (ALPC-7 at 208 and 218 now PASS); Gorrund GO218 / 229 / 239 canonical skeletal rows. **Still open:** Grask Narrow elbow margin (−1.0 %, NOT DEMONSTRATED). **PV-D14 skin rows got worse:** 05B's gluteal / abdominal flattening makes them FAIL on 5 bodies (§4, §5). |
| **Gorrund blind gate (§9)** | counts **PASS** (12 / 12; reference 3 / 3; no human control drawn in); explanations **FAIL** ("stocky / heavy / boxy human") → **CONSTRAIN** |
| **Grask blind gate (§9)** | 10 / 12 at the floor (8 and 9 in the two earlier runs of the same build line); reference 3 / 3; Marchfolk Narrow drawn into Grask 2 / 3; explanations "lanky / thin human" → **FAIL** |
| Validators rerun (§10) | **all chains, no row dropped** (§4). Skeletal rows improve, but the Gorrund surface stage **breaks skin-layer pelvic-depth rows**: ALPC-7 pelvic AP ÷ thoracic depth > Skarn FAILS on 12 bodies, and PV-D14 AP pelvic depth ÷ crest > MF / SK FAILS on 5 bodies. Grask is at the 05A level plus a skin-row MARGINAL on GR-G1. |
| Promotion / RM-OT-05 closure / D4 writeback | **NOT DONE** (§11, not passed) |
| Hand-authored race base mesh / tissue donor required | **YES** (§6) |

---

## 1. Construction route (order §7)

```
accepted skeleton → 05A architecture (arch_sculpt) → RM-OT-05B race surface (race_surface) → composition (donor tissue amount) → final surface
```

**Where the stage sits.** The stage is called inside `skeleton_envelope.make(surface=…)`.
- Its spec is stored in the skeleton's metadata.
- Every composition-grid body, CIB input and composition state of that skeleton therefore gets the same anatomy.
- Composition stays free to vary the **amount**.

**What it changes.** It changes the **topology** of the soft tissue only:

| Operation | Effect |
|---|---|
| **Limb belly / tendon remap** | Along a limb segment, the section profile is resampled from a mapped source position (e.g. Grask calf and forearm bellies move high and short, with a long distal tendon run), or low-passed (Gorrund columnar thigh / shank / forearm, upper-arm deltoid integration). Each segment is renormalized per angular sector to **its own volume**. |
| **Trunk relief redistribution** | Inside a height band and angular sector, the radial relief is mesh-smoothed and re-centred on the band mean. This keeps band volume constant and flattens the human gluteal shelf, lumbar hollow, abdominal bulge and pectoral relief (Gorrund), or the scapular / latissimus and pectoral relief (Grask). |
| **Base-surface route (§7, authorized)** | The skeleton-envelope surface's own soft relief (the surface minus a non-shrinking Taubin core) is remapped together with the tissue. The skeleton itself is never written. |
| **Skeleton guard** | The layer never cuts inside the skeleton-envelope surface: (tissue′ · n) ≥ min(tissue · n, 0). It was added after a first build moved the composition-infimum crest and trochanter stations (GR-P2b / GR-P6 skeletal rows; §5). |

Grask pelvic and gluteal bands were removed from the final recipe for the same reason (§5).

**What is unchanged:**
- stature: Grask 198.01 / 208.00 / 217.99 / 228.99 / 239.01 cm; Gorrund 208.27 / 218.00 / 228.99 / 230.90 / 239.01 / 251.00 cm;
- ground contact;
- arm clearance: min gap 0.79–1.61 cm, no vertex inside the trunk;
- muscle and fat amounts;
- face, ears, pigmentation and materials;
- Skarn.

### 1.1 Final recipe (`cfg_final.json`)

**Grask:**
- calf belly and forearm belly remapped high and short; distal 40 % carries tendon-level section;
- upper-arm cap integrated, low-passed over the proximal 55 %;
- scapular / latissimus relief extended along the back (r 0.4–1.0, posterior);
- pectoral relief softened;
- relief route with a 60-iteration core.

**Gorrund:**
- columnar thigh / shank / forearm low-pass;
- deltoid integration;
- gluteal shelf, lumbar hollow and abdominal relief redistributed;
- pectoral relief softened;
- 05A architecture with the knee condylar field ×1.06 and lumbar / pelvic depth raised;
- thorax breadth reduced to keep the S5/S2 margin.

### 1.2 Measured surface effect (contour diagnostic, `validators/contour.txt`)

| Body | Buttock index (gluteal shelf) | Abdomen index |
|---|---|---|
| Gorrund 229, 05A | 0.0187 | 0.0065 |
| **Gorrund 229, 05B** | **0.0109** | **0.0056** |
| **Gorrund 230.9, 05B** | 0.012 | **0.0** |
| Grask 218, 05A | 0.0754 | 0.0014 |
| Grask 218, 05B | 0.0755 | 0.0014 |
| Marchfolk / Skarn | 0.082 / 0.025 | 0.0024 / 0.0015 |

- Gorrund: the gluteal shelf is roughly halved and the "paunch" index is lower.
- Grask: the gluteal / pelvic form is unchanged, because the bands that changed it were removed to keep GR-P2b / GR-P6 (§5).

---

## 2. Evidence package (order §8)

Matched ortho camera, ground, stature, R-6 stance, reference composition and grey material. Lighting is unchanged.

| Sheets | Contents |
|---|---|
| `sheets/b_{208,218,229}_{F,P,Q,RQ}_body` and `b_{208,218,229}_{F,P}_sil` | W2 → 05A → 05B for both races, against Marchfolk 203 (208 sheet) and Skarn at matched height; Gorrund 230.9 on the 229 sheet |
| `sheets/b_stature_GR_*` | Grask transport: 198 / 208 / 218 / 229 / 239 |
| `sheets/b_stature_GO_*` | Gorrund transport: 208 / 218 / 229 / 230.9 / 239 / 251 (251 = current world-validation upper end, not permanent; nothing beyond it) |
| `sheets/b_frames_comp_{F,P,RQ}` and silhouettes | Skarn Narrow / Broad / low-muscle controls; Grask 218 and Gorrund 230.9 each as Narrow / reference / Broad / low muscle (0 / 0.5) / low muscle + fat (0.25 / 0.25) |
| `sheets/c_229_*`, `sheets/c_218_*` | close anatomy: shoulder / scapula (front and rear 3/4), thorax / lower trunk (profile and rear 3/4), pelvis / hip (front 3/4 and profile), knee (front and profile), elbow / forearm (front and profile), hand, foot, ankle |

---

## 3. Blind readability gate (order §9)

**Protocol.** Same as RM-OT-05A:
- 16 bodies: Marchfolk / Skarn reference, Narrow, Broad and low-muscle as human-family controls, plus Grask and Gorrund in the same four states.
- Body only, height-normalized, front + profile, grey + silhouette, shuffled (seed 20261013), codes only.
- Three independent uninformed scorer agents per run. The builder did not score.
- Raw assignments, the key and all runs are in `blind/blind_results.json`.

### 3.1 Results

| Run | Scorer totals | Grask correct | Gorrund correct | Human-family correct |
|---|---|---|---|---|
| **Final** (`cfg_final`) | 14 / 16 / 14 | **10 / 12** | **12 / 12** | 22 / 24 |
| Guarded, with Grask pelvic bands (superseded; GR-P2b / P6 rows failed) | 14 / 16 / 10 | 8 / 12 | 12 / 12 | 20 / 24 |
| Unguarded first build (superseded; surface cut into the skeleton envelope) | 14 / 16 / 12 | 9 / 12 | 12 / 12 | 21 / 24 |
| *RM-OT-05A, for reference* | 16 / 12 / 10 | 11 / 12 | 8 / 12 | 19 / 24 |
| *W2, for reference* | 10 / 10 / 12 | 8 / 12 | 7 / 12 | 17 / 24 |

### 3.2 Final-run confusions

| True | Assigned | Reads |
|---|---|---|
| Grask low muscle | human-family | 2 / 3 |
| **Marchfolk Narrow** | **Grask** | **2 / 3** |

### 3.3 §9 criteria, per race

| Criterion | Gorrund | Grask |
|---|---|---|
| Reference assigned correctly by a majority | **3 / 3** | **3 / 3** |
| ≥ 10 / 12 across reference / Narrow / Broad / low-composition | **12 / 12** | **10 / 12**. At the floor only, and 8 and 9 / 12 in the two earlier runs, so not robust. |
| Human-family controls not systematically pulled in | **YES**: 0 of 24 human reads went to Gorrund. In 05A, low-muscle humans went to Gorrund 4 of 6 times; now 0 of 6. | **NO**: Marchfolk Narrow → Grask in 2 of 3 reads. All three scorers say B calls "follow thinness". |
| Explanations no longer "thin vs broad / lanky / stocky / paunchy human" | **NO.** All six final-run scorer reports say an uninformed viewer would call Gorrund "stocky / heavy-set / boxy human". They also say the decisive cue is now **anatomical**: "the profile back-line (hollow vs straight) was the only cue that separated populations independently of build"; "exactly four bodies have a flat, deep trunk with no glute shelf". | **NO.** Every report says B is "lanky / thin human … not distinguishable from lean A at this resolution". High calf belly and large hands are noticed only on the reference body. |
| Cues anatomical and present in silhouette and grey | **YES** for the trunk back-line (profile silhouette) | weak |
| **Verdict** | **CONSTRAIN** (numeric gate met; non-human read not met) | **FAIL** |

---

## 4. Validator rerun (order §10)

Every W2C and W2D validator was rerun with the 05B bodies in the race slots: the same evaluators, specs and accepted comparators.

**Bodies covered:**
- all statures;
- Narrow / Broad at reference and at 218;
- named extremes (GR-BODY-10…18, GOD14_9 / GOR-BODY-14, GOLP218);
- every composition state (GR-BODY-06…09 / 15 / 16 / LOW; GOR-BODY-06…11 / 16 at 230.9 / 208 / 218).

**No row was dropped.** The only W2 search frames not transported are the never-accepted ones. Files: `validators/`.

| Chain | 05B | 05A | W2 |
|---|---|---|---|
| W2C (Grask) | 307 PASS, 44 REPORT, **12 NOT ALL PASS**, 1 NON-MONOTONIC, 1 NOT DEMONSTRATED | 310 / 44 / 6 / 4 / 1 | 308 / 44 / 12 / 6 / 1 |
| W2D (Gorrund) | **488 PASS**, 116 REPORT, **11 NOT ALL PASS**, 1 FAIL, 1 T-SENSITIVE, 1 NON-MONOTONIC | 477 / 116 / 17 / 3 FAIL / 2 T / 3 ND | 481 / 116 / 38 / 4 FAIL / 3 NM |

**Worse than 05A (per-body canonical rows):**
- **Gorrund skin / directional pelvic-depth rows. This is the material regression.**
  - ALPC-7 pelvic AP ÷ thoracic depth > Skarn central: **FAIL on 12 bodies**, NOT DEMONSTRATED on 5.
  - PV-D14 AP pelvic depth ÷ crest > MF and > SK: **FAIL on 5 bodies each**, NOT DEMONSTRATED on 3.
  - Low composition (GOR-BODY-16): ALPC-1 / ALPC-7 lumbar and lower-thorax depth rows FAIL.
  - Cause: the surface stage removes the gluteal shelf and abdominal bulge, so the **skin** pelvic AP depth falls. The skeletal pelvic rows still pass. See §5.
- Gorrund GO-P2b bitrochanteric ÷ crest ≈ MF and GO-P2a hip-joint scale ÷ crest: T-SENSITIVE on 4 and 2 bodies (skeletal, marginal at one t).
- Grask GR208, GR218, Broad, GR-BODY-10, 13 and 14: GR-G1 shoulder-joint ÷ thoracic breadth ≤ MF is **MARGINAL** (skin row; misses by < 1 %), because the pectoral / scapular relief softening slightly narrows the skin thorax.
- Gorrund continuity of S3/S2 depth: **NON-MONOTONIC** (−0.4 / +0.8 / −1.1 / +1.3 % per step).
- GON5_218: ALPC-4 biacromial ÷ thoracic breadth MARGINAL.

**Better than 05A:**
- Gorrund skeletal ALPC-7 S5/S2 (4 bodies) and ALPC-1b ribcage (4 bodies);
- directional ALPC-1 / ALPC-7 lumbar rows on the reference-composition bodies;
- ALPC-0 / -2a shape rows;
- GO218 / 229 / 239 skeletal rows;
- GO208, GOB7, GOB7_218 and GOD14_9_218 directional / skin rows;
- ALPC-7 S5/S2 at 208 and 218;
- Narrow-218 knee hold;
- Grask thoracic-breadth continuity.

**Inherited from W2, unchanged:**
- GOR-BODY-14 thoracic depth ÷ breadth > Skarn: FAIL (W2 also failed);
- Grask GR229 / 239 / extremes canonical rows.

**Specific §10 checks:**
- stature exact;
- no uniform scaling;
- arm clearance PASS;
- composition firewall: the surface volume is renormalized per region and the same remap is applied to every composition state;
- CIB / skeletal proxy unchanged from 05A for Grask (once the pelvic bands were removed and the guard added);
- ALPC rows: better than 05A;
- joint sections: Gorrund > Skarn on knee / ankle / wrist / elbow at 208 / 218 / 229; Gorrund > Grask on all four;
- Grask segment emphasis and hand / foot relations unchanged from 05A.

**Matched-height orderings (`validators/tables.json`):** all hold:
- torso GO > SK > GR;
- leg GR > SK > GO;
- forearm ÷ arm GR > SK ≥ GO;
- lower leg ÷ leg GR > SK, GO;
- skeletal thoracic depth ÷ breadth GO > SK > GR;
- hand share GR > SK ≈ GO;
- foot share GO > GR > SK;
- knee ÷ femur GO > SK at all three heights, GO > GR.

---

## 5. Canon guards that block the stronger corrections (order §11)

| Stronger correction tried | Observed effect | Blocking guard |
|---|---|---|
| Grask gluteal / posterior-hip relief and proximal-thigh remap (to stop the MPFB gluteal shelf) | changed the composition-infimum crest and trochanteric stations: skeletal bitrochanteric ÷ crest 1.205 → 1.186 vs MF 1.199; crest ÷ thoracic 0.966 → 0.977 vs MF 0.964 | **GR-P2b** (bitrochanteric ÷ crest ≥ MF), **GR-P6** (pelvis ÷ thorax ≈ MF). Removed from the final recipe. |
| Surface layer allowed to cut into the skeleton-envelope surface (free volume-conserving redistribution) | moved CIB stations, so skeletal readings changed | **REFERENCE_ANATOMY** CIB method and the AD-G14 construction (skeleton readings are composition infima). Guard added. |
| Grask narrow pelvis under a long ribcage (05A R1); Gorrund flat abdomen under a dominant thorax (05A R1) | strongest non-human cues seen | **GR-P5 / GR-P6**, **ALPC-1 / -2 / -7** (unchanged since 05A) |
| Gorrund gluteal-shelf and abdominal-bulge removal (the main 05B Gorrund cue: "no lumbar hollow, no glute shelf") | lowers skin pelvic AP depth: ALPC-7 pelvic ÷ thoracic depth > Skarn FAILS on 12 bodies, PV-D14 FAILS on 5 | **PV-D14 / GO-P4** (depth-led pelvis, skin rows) and **ALPC-7** skin comparison. Restoring them means adding posterior / anterior pelvic mass back, which is the human gluteal / belly read the order asks to remove. A skeletal pelvic-depth increase could offset part of it, but was not run in this block. |
| Pushing Grask distal leanness / tendon run further | the uninformed probe read it as "youthful / slight / female-leaning" (`search/blindq_s7`) | anti-juvenile and sex-coding guards (order §2) |

---

## 6. Escalation (order §9 / §11): a hand-authored race base surface is required

**YES.** Three findings support this:

1. **The procedural surface stage has reached what an MPFB-derived surface supports honestly.**
   - It flattened the Gorrund gluteal shelf, lumbar hollow and paunch enough that build stopped confounding Gorrund (12 / 12; no human pulled in).
   - Scorers still read that body as a heavy human.
   - The remaining human read is carried by whole-body MPFB anatomy that a field cannot replace without either cutting into the skeleton envelope (CIB / GR-P rows) or inventing relief: pectoral / abdominal masses, thigh-to-knee muscle topology, the glute–thigh junction, and the overall muscle-group layout.
2. **Grask's distinctness is mostly proportion.**
   - The canon-legal surface cues (high calf / forearm bellies, integrated shoulder, scapular extension) are below what scorers resolve at body scale.
   - The canon guards forbid the pelvic and trunk relief that would carry more.
3. **Recommended next block (scope for the author):** a hand-sculpted, race-specific **base mesh / tissue donor** for each race, retopologized to the MPFB vertex order so the whole validator chain still runs.
   - Built on the 05B skeletons (Gorrund) and 05A skeletons (Grask), honouring every row in §4.
   - **Grask:** long-tendon limb musculature, an integrated girdle with no human deltoid cap, a non-human gluteal / hip muscle organization within GR-P2b / P6 bony relations, and distal joint relief.
   - **Gorrund:** an axial back mass continuous to the sacrum, an abdominal wall following the depth-led pelvis, structural joint relief, and columnar limb musculature.
   - This is an art task; it cannot be faked procedurally. Validate with the same §9 protocol.

## 7. Assets and persistent files

**Candidates** (`reviews/reference-assets/manifest.json`, **PENDING AUTHOR, not accepted**):

| Race | Assets |
|---|---|
| Grask | GR5B198 / 208 / **218** / 229 / 239, GR5BN, GR5BB, B_GR-BODY-06, B_GR-LOW |
| Gorrund | GO5B208 / 218 / **229** / **5BREF (230.9)** / 239 / 251, GO5BN, GO5BB, B_GOR-BODY-06, B_GOR-BODY-16 |

Transported bodies: `construction/transport.json`. W2 and 05A assets are kept as provenance.

**New files:**
- `reviews/claude-rac-rm-ot-05b-grask-gorrund-surface-anatomy-gate.md` (this gate)
- `reviews/rac-rmot05b-evidence/`
- `tools/rac/w1/race_surface.py`
- `tools/rac/w1/rmot05b_drivers/*.py`

**Additive edits:** `surface=` hook, default off, in:
- `tools/rac/w1/skeleton_envelope.py`
- `w1g_drivers/gn3.py`
- `w2c_drivers/gr_body.py`
- `w2d_drivers/go_body.py`

**Small edits to 05A drivers** (no behaviour change for 05A):
- `rmot05a_drivers/a_blind.py`: code prefix
- `rmot05a_drivers/a_package.py`: sheet title prefix

**Records:**
- `reviews/reference-assets/manifest.json` and `r6/` (candidate assets)
- `specs/grask/GRASK_V1.md`, `specs/gorrund/GORRUND_V1.md` (status lines)
- `specs/STATUS.md`, `reviews/claude-pass2-r5-reference-mesh-queue.md`

**Not changed:**
- canon relations;
- accepted bodies;
- Skarn;
- face / ear / pigmentation;
- the D4 writeback (still blocked).

## 8. Stop

Stopped at the gate. RM-OT-05 is **not** closed and nothing was promoted.

Not begun: posture / locomotion, equipment fit, collision, camera, UE5 creator, MetaHuman, rigging, animation, gameplay, and face / ear / pigmentation polish.
