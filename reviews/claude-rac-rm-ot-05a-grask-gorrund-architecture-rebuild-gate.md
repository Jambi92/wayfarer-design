# RAC RM-OT-05A — Grask / Gorrund body-architecture rebuild gate

**Order:** `reviews/chatgpt-rac-rm-ot-05a-grask-gorrund-architecture-rebuild-order.md`
**Parent:** RM-OT-05 stays **OPEN**. This gate does not close it.
**Evidence:** `reviews/rac-rmot05a-evidence/` (README there).
- `sheets/`: 30 matched lineup sheets and 26 close architectural sheets.
- `blind/`: blind sets, keys and scores.
- `validators/`: W2C / W2D reruns, contour and arm-clearance results, measurement tables.
- `construction/`: build records for every candidate and every transported body.
- `search/`: every sculpt recipe tried and the uninformed-reviewer probe history.
- `arch_final.json`: the final recipe.

**Tool:** `tools/rac/w1/arch_sculpt.py`, the new race-architecture sculpt layer.
- It is wired into `skeleton_envelope.make(arch=…)`, `w1g_drivers/gn3.build`, `w2c_drivers/gr_body.build` and `w2d_drivers/go_body.build`.
- Its default is off, so every accepted body rebuilds unchanged.

**Drivers:** `tools/rac/w1/rmot05a_drivers/` (`a_build`, `a_transport`, `a_eval`, `a_package`, `a_blind`, `a_tables`, `a_evidence`, `a_preview`, `a_try`, `a_blindq`).

---

## 0. Verdicts (§12)

| Item | Verdict |
|---|---|
| Author decision Option (a) acknowledged | **YES** |
| Sagekin configuration-2 canonical acceptance applied | **YES**. SGF152-NAT and SGF208 are marked canonical in `SAGEKIN_V1` and the reference-asset manifest. SGF178 is recorded as construction base only. |
| CG76H-NAT canonical acceptance applied | **YES**. `COGLING_V1` and the manifest are updated. CG76-NAT is kept as provenance. |
| Grask old reference retained as provenance | **YES**. All W2C bodies are untouched. The manifest tags them as constraint / provenance references, and they appear as "W2" rows in every sheet and validator file. |
| Gorrund old reference retained as provenance | **YES**. Same treatment for all W2D bodies, including GOREF 230.9. |
| **Grask new architecture candidate** | **CONSTRAIN**. It is canon-valid: W2C non-pass rows fall from 12 to 6, with no new canonical failure except the reading-noise residuals in §4. It transports 198 → 239 cm with exact stature. It measurably moves the canon-named architecture: forearm / lower-leg / hand / foot emphasis, joint presence, scapular depth and girdle slope. It does **not** make an uninformed viewer read a non-human body (§3). |
| **Gorrund new architecture candidate** | **CONSTRAIN**. Joint structure, columnar long bones, ALPC depth chain and feet are rebuilt. ALPC-7 and the hip rows hold, with marginal residuals (§4). Stature is exact at 208–251 cm. The read is still "heavy / stocky human" (§3). |
| **Grask body-only neutralized readability** | **CONSTRAIN**. Blind assignment **11 / 12** (W2 set: 8 / 12), and no Grask is read as Gorrund. All three uninformed scorers still called every Grask a "tall lanky human", not a non-human body. |
| **Gorrund body-only neutralized readability** | **FAIL**. Blind assignment **8 / 12** (W2 set: 7 / 12). The **reference Gorrund was assigned human-family by 2 of 3 scorers**, as in RM-OT-05. Low-muscle Marchfolk / Skarn were assigned Gorrund (4 of 6 reads). Scorers read Gorrund as "heavy / stocky / paunchy human". |
| **Grask vs Gorrund contrast is architectural rather than thin-vs-broad** | **CONSTRAIN**. The two races were never confused with each other (0 of 24 reads). The measured contrast is now architectural: knee / ankle / wrist / elbow joint scale, lower-leg and forearm share, ALPC depth chain, hand vs foot emphasis. But every scorer said their calls followed thin vs broad (§3.2). |
| **Skarn remains clearly human-family** | **PASS**. Skarn is unmodified. Its reads were human-family 9 / 12. Deviations: Broad Skarn → Gorrund 0 of 3 (it was 2 of 3 at R1); low-muscle Skarn → Gorrund 2 of 3; Narrow Skarn → Grask 1 of 3. These deviations are composition-driven, not architectural. |
| **Recommendation** | **FURTHER CORRECTION**. RM-OT-05 cannot be finally closed on this gate. The smallest next structural correction is in §7. |

---

## 1. What was rebuilt

### 1.1 Construction route

`arch_sculpt.apply` runs on the **skeleton surface** (the AD-G14 `-LEAN` body), after the accepted bone scales and trunk sculpt.
- It is written back as the skeleton, the same way as the W1 trunk sculpt.
- Soft tissue is then added **unchanged** from the race's own donor (`skeleton_envelope.make`). The composition firewall (AD-G15) therefore holds by construction: no field touches muscle or fat.
- The composition grid, CIB, skeletal proxy and ALPC readings all measure the rebuilt skeleton.
- Rest and R-6 are sculpted separately, in each body's own joint frames.
- There is **no uniform scale**. Stature, hip-joint height and shoulder height are held:
  - Grask: 198.01, 208.00, 217.99, 228.99, 239.01 cm.
  - Gorrund: 208.27, 218.00, 228.99, 230.90, 239.01, 251.00 cm.
  - These are identical to W2 to within 0.01 cm.

### 1.2 Field families

| Field | Function |
|---|---|
| **limb-chain section shaping** | Separate lateral, medial, anterior and posterior half-section factors along each limb chain (hip-knee-ankle-ball and shoulder-elbow-wrist-knuckle), in each bone's frame. This shapes joint **structure** (condylar / epicondylar / malleolar breadth, flat vs round sections, shaft taper) rather than circumference. The factor fields are mesh-smoothed. The sole never moves, so ground contact and stature are held. |
| **segment redistribution** | The elbow or knee moves along its segment at held limb length (shoulder / hip and wrist / ankle fixed). Joints are updated. |
| **trunk section shaping** | Anterior / posterior depth and anterior-half / posterior-half breadth by trunk height, about each section's centre. This changes section **shape**, for example a posterolaterally broad thorax. |
| **girdle top** | The superior shoulder contour is lowered (Grask) or raised (Gorrund) laterally of the neck base. Joints are not moved. |
| **distal integration** | Hands are scaled about the wrist. Feet are scaled horizontally about the ankle line, so sole and ankle heights are held. |

### 1.3 Exact new geometry in the final recipe (`arch_final.json`), tied to canon

**Grask**

| Change | Canon reference | Measured result (218, vs W2) |
|---|---|---|
| Forearm-dominant arm: elbow 2.5 cm toward the shoulder at held arm length; forearm shaft leaner distally (×0.94–0.96); wrist ×1.10 | GRASK L59 (forearm emphasis), L164–174, L233–253 | upper-arm ÷ arm −10.4 %, forearm ÷ arm +2.0 %, wrist ÷ segment +5.5 %, elbow ÷ segment +9.0 % |
| Lower-leg-dominant leg: knee 3 cm toward the hip at held leg length; long lean distal shank (calf ×0.92 / Achilles region ×0.86); malleolar ankle ×1.06–1.08 | GRASK L54 (lower-leg emphasis), Part 2 §14–20 (lower-leg-dominant individuals valid) | femur ÷ leg −5.6 %, lower leg ÷ leg +5.1 %, knee ÷ segment +6.6 %, ankle ÷ segment +6.5 % |
| Large integrated hands (×1.14 about the wrist) and feet (×1.12 horizontal) | GRASK L62, L253 ("large in absolute terms"); resolves RM-OT-05 contradiction 2 | hand share +13.9 % (0.134 vs Skarn 0.117); foot share +11.3 % (0.163 vs Skarn 0.159) |
| Vertically extended, close-seated scapular bed: posterior thorax depth ×1.03–1.06 from mid to lower thorax; anterior ×1.01–1.03 | GR-G2 (AD-G2); GRASK thorax row ("meaningful depth") | thoracic depth ÷ breadth +5.1 % (skeletal); thorax depth share +3.2 % |
| Open, sloped girdle top (−2 cm lateral drop) and integrated arm origin (deltoid cap ×0.94–0.97) | GR-G1, GR-G3, GR-G5 | arm–trunk clearance improved: min gap 0.72 → 1.37 cm, section clearance 0.94 → 1.82 cm, no vertex inside the trunk |

**Gorrund**

| Change | Canon reference | Measured result (229, vs W2) |
|---|---|---|
| Structural joints by shape: knee condylar platform (lateral / medial ×1.26), malleolar ankle ×1.30, elbow epicondyles ×1.22, broad flat distal radius-ulna ×1.20–1.22 | GORRUND L74–76 ("one of the strongest body signals"), GO-G3 | ankle ÷ segment +18.3 %, wrist ÷ segment +20.1 %, knee ÷ segment +7.7 %, elbow ÷ segment +6.7 % |
| Columnar long bones: distal thigh ×1.18, distal shank ×1.22 (reduced human taper) | GORRUND L76 (long-bone cross-section) | visible in `c_229_knee_F/P`, `c_229_ankle_F` |
| ALPC depth chain: posterior lumbar / sacral depth ×1.08–1.12, anterior pelvis ×1.05–1.06, lumbar breadth ×1.05–1.06, thorax ×1.02–1.05 | ALPC-1 / -2 / -7, GO-P1, GO-P4, GO-P6 | AP pelvic depth ÷ stature +3.7 %, S4/S2 depth +2.8 %; ALPC-7 vs Broad Skarn holds (S5/S2 by < 1 %, §4) |
| Broad neck base / girdle carried by the thorax: girdle top +1.5 cm, deltoid cap ×0.96 | GO-G1, GO-G4 | `c_229_shoulder_F/RQ` |
| Large supportive feet (×1.14 horizontal), hands ×1.08 | GORRUND L32 | foot share 0.170 vs Skarn 0.159 |

- No tusks, barrel, hunch, ogre, digitigrade, claw, ape-arm or other unsupported novelty was added.
- No culture, class or sex coding was added.
- Skarn was not modified.

---

## 2. Visual package (§7 / §8)

`sheets/a_<H>_<view>_<mode>.jpg` covers H = 208 / 218 / 229 with front, profile, front 3/4 and rear 3/4 views.

| Mode | Contents |
|---|---|
| grey | Neutral grey, head on |
| body | Head / neck removed |
| sil | Front and profile pure silhouette, body only |

Rows:
- Marchfolk 203 (max, 208 sheet only).
- Skarn at matched height.
- Grask W2 (provenance) and Grask 05A.
- Gorrund W2 (provenance) and Gorrund 05A.
- Gorrund 230.9 ARM on the 229 sheet.

`sheets/c_229_*` (Skarn, Grask W2, Grask 05A, Gorrund W2, Gorrund 05A) and `sheets/c_218_*` (Skarn, Grask W2, Grask 05A) are close architectural views. Each tile is centred on that body's own joint, at a fixed cm width per sheet:
- shoulder / scapular region, front and rear 3/4;
- pelvis / proximal femur, front 3/4 and profile;
- thorax / lower trunk, profile and rear 3/4;
- knee, front and profile;
- elbow / forearm, front and profile;
- hand, profile;
- foot, front 3/4;
- ankle, front.

Camera, ground, scale, R-6 stance, reference composition and the grey material are all matched. Lighting is unchanged.

---

## 3. Blind readability rerun (§9)

### 3.1 Protocol

- 16 bodies per set:
  - Marchfolk and Skarn human-family controls (reference, Narrow, Broad, low-muscle);
  - Grask and Gorrund (reference, Narrow, Broad, low-muscle).
- Each set was shown twice: neutral grey body only, and black silhouette body only.
- Front + profile, height-normalized, shuffled with a fixed seed, codes only.
- **Scorers:** three independent agents per set. None of them built the bodies or saw the keys. They were given only the three population descriptions and the 8 / 4 / 4 count. Claude did not score this time, because in RM-OT-05 the builder scored.
- The accepted W2 set was scored under the identical protocol, as the baseline.
- Raw answers, keys and scoring are in `blind/blind_results.json`.

### 3.2 Results

| Set | Scorer 1 | Scorer 2 | Scorer 3 | Grask correct | Gorrund correct | Human-family correct |
|---|---|---|---|---|---|---|
| **RM-OT-05A (final)** | 16 / 16 | 12 / 16 | 10 / 16 | **11 / 12** | **8 / 12** | 19 / 24 |
| W2 (provenance) | 10 / 16 | 10 / 16 | 12 / 16 | 8 / 12 | 7 / 12 | 17 / 24 |

**Confusions in the final set:**

| True | Assigned | Reads |
|---|---|---|
| Gorrund reference | human-family | 2 / 3 |
| Gorrund Narrow | human-family | 1 / 3 |
| Gorrund Broad | human-family | 1 / 3 |
| Marchfolk low-muscle | Gorrund | 2 / 3 |
| Skarn low-muscle | Gorrund | 2 / 3 |
| Skarn Narrow | Grask | 1 / 3 |
| Grask Narrow | human-family | 1 / 3 |

**The order's three questions:**

- **Do errors still follow thin vs broad?** **Yes.** Every scorer said so explicitly. Low-composition humans are read as Gorrund because soft tissue looks like "bulk". The Gorrund reference is read as a "heavy human". The Grask reads rest on "lean + long limbs".
- **Are human-family bodies still misread as Grask / Gorrund?** **Yes:** 5 of 24 reads, mostly low-muscle humans → Gorrund.
- **Are Grask / Gorrund still misread as human-family?** Grask rarely (1 / 12). Gorrund often (4 / 12).

**The decisive finding: no scorer called any Grask or Gorrund body non-human.**
- Grask: "tall, lanky / marfanoid human".
- Gorrund: "heavy, stocky, barrel-chested or paunchy human".

This held across this gate's scorers and the search-stage uninformed reviewers (`search/search_history.json`).

### 3.3 Search history (honest record)

Thirteen preview recipes and seven built rounds were tried.

**Round R1** had the strongest silhouette cues. It scored 14 / 14 / 14 with the same blind protocol. Its cues:
- Grask: narrowed, torso-proportioned pelvis plus a ribcage lengthened into the lumbar interval.
- Gorrund: thorax enlarged above a flatter abdomen.

Those cues **broke canon**:
- **GR-P6:** pelvis ÷ thorax breadth ≈ MF, with no authored departure.
- **GR-P2b:** bitrochanteric ÷ crest ≥ MF.
- **ALPC-1 / -2 / -7:** the lower trunk and pelvis must keep pace with the thorax.

R2–R6 removed them. The final recipe is the strongest canon-valid one found.

The search also produced readings that were rejected:
- a **juvenile** Grask read (v12 / v13);
- a **female-coded / lumpy** Gorrund read (v11 / v13);
- an **obese** Gorrund read (v9 / v10).

---

## 4. Validators rerun (§10)

Every affected chain was rerun with the rebuilt bodies in the race slots, using the same evaluators, specs and accepted comparators (`validators/`). Nothing was carried over from W2:
- the W2C chain and the W2D chain;
- CIB and skeletal proxy at t = 0 / 0.5 / 1 for every rebuilt skeleton;
- exact-plane joint sections and stature-scaled slab joints;
- contour, arm clearance, frames, composition states and named extremes.

**Transport.** Every accepted W2C / W2D body was rebuilt with the final recipe, prefixed `A_`. W2 search frames that were never accepted (GRN2–4, GON3/4, GOB3–6 …) were not transported.

| Group | Bodies |
|---|---|
| Frames | Grask Narrow / Broad 218; Gorrund Narrow / Broad 230.9 and 218 |
| Named extremes | GR-BODY-10…14, 17, 18; GOD14_9 (GOR-BODY-14), GOLP218 |
| Composition states | GR-BODY-06…09, 15, 16, GR-LOW; GOR-BODY-06…11, 16 at 230.9 / 208 / 218 |

**Totals:**

| Chain | Rebuild | W2 | Notes |
|---|---|---|---|
| W2C | 310 PASS, 44 REPORT, **6** NOT ALL PASS, 4 NON-MONOTONIC, 1 NOT DEMONSTRATED | 308 / 44 / **12** / 6 / 1 | |
| W2D | 477 PASS, 116 REPORT, **17** NOT ALL PASS, 3 FAIL, 3 NOT DEMONSTRATED, 2 T-SENSITIVE | 481 / 116 / **38** / 4 FAIL / 3 NON-MONOTONIC | 0 NOT RUN |

### 4.1 Rows that are worse than W2

These are listed in full. All are residuals of the rebuild.

| Row | Rebuild | W2 | Reading |
|---|---|---|---|
| ALPC-7, Gorrund 208 > Broad Skarn 208 / 218 / 229: S5/S2 breadth | NOT DEMONSTRATED (holds, < 1 %) | PASS | thorax broadened ×1.02–1.05 with crest held (GO-P2b) |
| ALPC-7 at 218: S5/S2 | T-SENSITIVE | PASS | same |
| Gorrund 218 / 229 / 239 / Broad / Broad-218 canonical skeletal rows | T-SENSITIVE: ALPC-1b ribcage vertical ÷ breadth ≥ MF; bitrochanteric ÷ crest ≈ MF | PASS | marginal at t = 0 only |
| GOR-BODY-14 (lower-depth extreme) thoracic depth ÷ breadth > Grask 229 | T-SENSITIVE | PASS | the Grask rebuild deepened its thorax (+5 %), so the low-depth Gorrund extreme approaches it |
| Narrow Gorrund 218 keeps knee scale (GO-G6) | **FAIL −1.15 %** | PASS (−0.76 %) | the knee-hold compensation was applied only to the 230.9 Narrow body (which passes); not yet transported to 218 |
| Grask Narrow moves elbow breadth below central by ≥ 1 % | NOT DEMONSTRATED (−1.0 %) | PASS | |
| Gorrund 208 only: ALPC-1 lumbar depth ÷ thorax > MF and ALPC-7 S4/S2 depth > Skarn central (skin / directional rows) | **FAIL** | PASS | the trunk-section field at 208 cm deepens the thorax more than the lumbar section; 218–251 pass. GOR-BODY-16 (low composition): ALPC-1 lumbar depth NOT DEMONSTRATED (holds, < 1 %) |
| Gorrund 208 / 218 / GOREF / 251: AP pelvic depth ÷ crest > MF (PV-D14) | NOT DEMONSTRATED (holds, < 1 %) | FAIL or NOT DEMONSTRATED in W2 | improved but still under the 1 % margin |
| GR198 canonical row joint scale GO > GR (elbow) | FAIL | PASS | Against the **W1 Gorrund comparator** fixed in the W1 row set (0.351). Against the rebuilt Gorrund the cross-race elbow ordering holds at every matched height (§5). |

### 4.2 Rows that are better than W2

- **Grask** (W2C): the W1 canonical rows "lower leg ÷ leg emphasized vs MF / SK" and "forearm ÷ arm emphasized" now PASS at 229 and 239, where W2 failed them.
- **Gorrund:** ALPC-2b hip-level ÷ lumbar breadth ≤ MF now PASSES on GO208, GO218, GO229, GOREF, GO239, GO251 and Broad (Narrow MARGINAL), where W2 failed it.
- **Gorrund:** palm depth (GO218), the "thoracic breadth GO > SK" row (GO239, GOR-BODY-16), ALPC-7 pelvic depth ÷ thoracic depth > Skarn (GO229, Narrow) and ALPC-2b crest ÷ lumbar ≤ MF (Narrow, Broad) now pass; AP pelvic depth ÷ crest > SK now passes on 208 / 218 / 229 / 230.9.
- **Gorrund:** knee joint scale GO > GR now PASSES at 208 / 218 / 229 / 239.

### 4.3 Other checks

- **Contour (soft-tissue diagnostic):**
  - Grask 218 buttock index 0.075, up from 0.039. It is still below MF (0.082), and comes from the leaner posterior thigh. GR229 returned NaN: the posterior-profile window failed.
  - Gorrund abdomen index 0.0065, up from 0.0. This is a small anterior protrusion beyond the chest-to-pelvis line, above MF's 0.0024, and it matches the "paunchy" reads.
  - These are reported only, not canon rows.
- **Arm clearance (GR-G3):** PASS on every rebuilt Grask and Gorrund. There are no vertices inside the trunk.
- **No-uniform-scale invariant:** holds. Statures are identical to W2, and nothing is scaled about a body centre.

---

## 5. Cross-race ordering checks (matched height, skin layer + exact-plane joints)

| Relation | 208 | 218 | 229 | Result |
|---|---|---|---|---|
| torso share GO > SK > GR | 0.304 > 0.296 > 0.266 | 0.302 > 0.294 > 0.266 | 0.301 > 0.292 > 0.265 | holds |
| leg share GR > SK > GO | 0.561 > 0.524 > 0.517 | 0.563 > 0.529 > 0.521 | 0.566 > 0.533 > 0.525 | holds |
| forearm ÷ arm GR > SK ≥ GO | 0.389 > 0.355 > 0.354 | 0.385 > 0.353 > 0.352 | 0.381 > 0.351 > 0.350 | holds (GO ≈ SK, never copying Grask emphasis) |
| lower leg ÷ leg GR > SK, GO | 0.562 > 0.510, 0.487 | 0.550 > 0.500, 0.479 | 0.537 > 0.490, 0.470 | holds |
| skeletal thoracic depth ÷ breadth GO > SK > GR | 0.843 > 0.809 > 0.764 | 0.833 > 0.804 > 0.767 | 0.834 > 0.799 > 0.761 | holds (GO-G7 / AD-G7) |
| hand share GR > SK ≈ GO | 0.135 > 0.118 = 0.118 | 0.134 > 0.117 = 0.117 | 0.133 > 0.116 ≈ 0.116 | holds |
| foot share GO > GR > SK | 0.171 > 0.163 > 0.160 | 0.170 > 0.163 > 0.159 | 0.170 > 0.163 > 0.159 | holds; Grask feet no longer smaller than Skarn's (RM-OT-05 contradiction 2 resolved) |
| knee ÷ femur GO > GR | 0.315 > 0.290 | 0.296 > 0.272 | 0.278 > 0.258 | holds |
| knee ÷ femur GO vs SK | 0.315 > 0.309 | 0.296 ≈ 0.297 | **0.278 < 0.290** | **not resolved** at 218 / 229 (RM-OT-05 contradiction 3). Gorrund now leads Skarn on ankle (0.390 vs 0.337), wrist (0.317 vs 0.254) and elbow (0.373 vs 0.333) at 229, but not on the knee normalized by its long femur. |

**Accepted stature / allometry relations changed:**
- **Stature transport and head allometry:** unchanged.
- **Segment allometry, Grask:** upper-arm ÷ arm −10 %, femur ÷ leg −5 to −6 %, hands +14 %, feet +11 %.
- **Segment allometry, Gorrund:** hands +8 %, feet +13 %.
- These move away from the W2 numbers in the canon direction. The W2 values were TARGET-free central tendencies, not envelopes, but they are recorded here as changed.

---

## 6. Canon contradictions encountered

1. **The neutralized "non-human read" standard against the canon guards.**

   Every cue that made the bodies read less human to uninformed scorers is **forbidden by an accepted relation**:
   - Grask: narrow torso-proportioned pelvis below a long ribcage (GR-P6, GR-P5).
   - Gorrund: flat abdomen under a dominant thorax (ALPC continuity).

   The cues that remain canon-legal are proportional and joint-structural, and uninformed viewers read them as **human build variation**:
   - Grask: tall, lanky.
   - Gorrund: heavy, stocky.

   The canon simultaneously requires a human-homologous bone plan (GR-P2b / P3, GO-P1), no caricature, ALPC continuity, GR-P6 and no muscle-carried identity. **The author needs to decide which standard the gate tests:**
   - **(i)** informed equal-height discrimination: distinct populations under matched presentation. The rebuild substantially improves this: Grask 11 / 12, never confused with Gorrund.
   - **(ii)** an uninformed "non-human body" read. This is not met, and probably not meetable inside the current guards with an MPFB-derived surface. See 2.

2. **Soft-tissue relief is human.**

   The AD-G14 envelope adds each race's tissue from an MPFB human-template donor at the reference composition (0.5 / 0.5). The scorers' cues were:
   - pectoral / navel / abdominal relief;
   - the gluteal shelf;
   - calf belly;
   - the belly at reference fat.

   These come from that layer, which the firewall forbids changing to carry identity. Gorrund's reference-composition tissue makes the ALPC-continuous trunk read as "paunchy" (contour abdomen index 0.0065).

3. **Gorrund knee joint presence vs Skarn** (GORRUND L74–76) is still not demonstrated at 218 / 229 when normalized by femur length (§5).

---

## 7. Smallest next structural correction (recommendation: FURTHER CORRECTION)

1. **Author ruling on contradiction 6.1.** This is the smallest step, because it decides whether more geometry is needed at all.
   - If the gate standard is (i), the rebuild needs only the §4.1 residual clean-up (Narrow-218 knee hold; Gorrund 208 lumbar depth; S5/S2 and PV-D14 margins) to be submitted for closure.
   - If the standard is (ii), go to step 2.
2. **Race-specific soft-tissue relief layer,** authored on the rebuilt skeleton. This is not muscle amount: muscle-attachment and relief topology that follows the non-human skeleton. Comparable to the Saurin W2I surface work.
   - **Gorrund:** no human gluteal shelf or lumbar hollow; a deep axial back mass continuous to the sacrum; an abdominal wall that follows the depth-led pelvis instead of the MPFB belly; flat structural joint relief.
   - **Grask:** long-tendon distal limb relief (high short calf and forearm bellies); a vertically extended scapular / latissimus relief; an integrated shoulder without a human deltoid cap.

   This needs either a hand-sculpted race base mesh or a race tissue donor, and author scope. It cannot be done honestly by more field tuning on the MPFB human tissue. The field search shows that tuning trades readability against canon rows.
3. **Gorrund knee:** decide whether the GORRUND L74–76 knee row is read per stature (where it holds at 208) or per femur (where it fails at 218 / 229). Then fix the condylar field accordingly.

---

## 8. Candidate assets and manifest

All candidates are listed in `reviews/reference-assets/manifest.json` as **PENDING AUTHOR (not accepted)**, with SHA-256 hashes. R-6 files are in `reviews/reference-assets/r6/`; build records are in `reviews/rac-rmot05a-evidence/construction/`.

| Race | Asset | Role |
|---|---|---|
| Grask | **GRA218** | central reference |
| Grask | GRA208, GRA229 | scale transport |
| Grask | GRA198, GRA239 | envelope ends |
| Grask | GRAN, GRAB | Narrow / Broad |
| Grask | GRA218-LOW (0 / 0.5), GRA-LOW (0.25 / 0.25) | composition states |
| Gorrund | **GOA229** | 229 nominal design reference |
| Gorrund | **GOAREF** | 230.9 ARM realization; bookkeeping kept distinct |
| Gorrund | GOA208, GOA218, GOA239 | stature transport |
| Gorrund | GOA251 | current world-validation upper end, not permanent; nothing beyond it |
| Gorrund | GOAN, GOAB | Narrow / Broad |
| Gorrund | GOAREF-LOW, GOA-L16 | composition states |

Transported `A_*` bodies are in `construction/transport.json`; their geometry is kept in scratch. The accepted W2 bodies stay as provenance and are tagged in the manifest.

## 9. Persistent files changed

**New**
- `reviews/claude-rac-rm-ot-05a-grask-gorrund-architecture-rebuild-gate.md` (this gate)
- `reviews/rac-rmot05a-evidence/`
- `tools/rac/w1/arch_sculpt.py`
- `tools/rac/w1/rmot05a_drivers/*.py`

**Edited (additive)**
- `tools/rac/w1/skeleton_envelope.py`: optional `arch=` stage. Default off; accepted outputs unchanged.
- `tools/rac/w1/w1g_drivers/gn3.py`, `tools/rac/w1/w2c_drivers/gr_body.py`, `tools/rac/w1/w2d_drivers/go_body.py`: `arch=` pass-through.

**Edited (records and status)**
- `reviews/reference-assets/manifest.json` and `reviews/reference-assets/r6/` (19 candidate assets; Sagekin / Cogling acceptances; Grask / Gorrund provenance tags)
- `specs/sagekin/SAGEKIN_V1.md`, `specs/cogling/COGLING_V1.md` (§2 acceptances)
- `specs/grask/GRASK_V1.md`, `specs/gorrund/GORRUND_V1.md` (RM-OT-05A status; W2 bodies = constraint / provenance)
- `specs/STATUS.md`, `reviews/claude-pass2-r5-reference-mesh-queue.md`

**Not changed**
- Any accepted body geometry.
- Skarn.
- Any canon relation.
- The D4 stature writeback, which still waits for RM-OT-05 closure.

## 10. Stop

Stopped after the RM-OT-05A gate. RM-OT-05 is **not** self-closed.

Not begun: posture / locomotion, equipment fit, environment-scale implementation, collision, camera, UE5 creator, MetaHuman, rigging, animation, gameplay, and craniofacial / ear / pigmentation polish.
