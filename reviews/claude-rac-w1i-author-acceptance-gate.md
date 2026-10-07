# RAC W1i — Gorrund Structural-Continuity Gate

**Author:** Claude **Date:** October 6, 2026
**Order:** `reviews/chatgpt-rac-w1i-gorrund-structural-continuity-resolve-order.md`
**Evidence:** `reviews/rac-w1i-evidence/` (`tables.md` holds every number quoted here; `README.md` maps the files)
**ARM record:** `reviews/rac-w1i-arm/claude-rac-w1i-arm-GO.md`. Only Gorrund changed. Every other race is the W1h body, untouched (order §10–11).

## Recommendation: CONSTRAIN — Gorrund is not ready for final acceptance

What W1i achieved:
- **Every Gorrund skeletal relation passes at every stature tested, with larger margins than W1h:**
  - the reference body;
  - 208 cm, two ways: GOR-BODY-02 on its usual donor (now 210.8 cm), and a new true-208 body at 208.3 cm;
  - 217, 224 and 253 cm;
  - the three frame bodies;
  - all 10 Gorrund vs Broad Skarn height pairs (ALPC-7), including the 5 cross-height pairs that W1h left NOT DEMONSTRATED.
- **Thoracic breadth > Skarn: +1.41 %**, beyond the 1 % convention.
- **No arm interpenetration** anywhere it can be tested, on both tests and every body.
- **More continuous trunk on the numbers** (§4):
  - skin flank flare −0.0115 (W1h −0.0077);
  - skeleton waist ÷ hip-block 0.700 (W1h 0.684; references 0.624–0.665);
  - skeleton waist ÷ thorax 0.799 (W1h 0.765; references 0.678–0.731).
- **A low-composition waist exists, but it is weaker than W1h and the human references** (crest ÷ narrowest level above it: 1.105 vs W1h 1.124, MF 1.111, SK 1.110). Most of the W1h "no waist" FAIL was a measurement artifact (§5). The low-composition body also shows more hip shelf than any reference (§4).

Why still CONSTRAIN:
1. **Still knife-edge (order §9).** Of 32 ±2 % single-value perturbations, 23 keep every accepted relation, 9 lose one, and 1 reaches FAIL (§6).
   - This is better than the solver point before centering (18 / 32, 3 FAIL) and than W1h, which was tested more weakly.
   - But it is not robust.
   - The rib-cage breadth value sits between two sets of relations, and both directions break:
     - below it: thoracic breadth > Skarn;
     - above it: thoracic depth ÷ breadth > SK (AD-G7), rib-cage vertical ÷ breadth (ALPC-1b) and ALPC-7 crest ÷ thorax.
2. **Values near bounds (order §3).** These need the author's ruling (§3):
   - **Femur robusticity 1.386** (W1h 1.28; the order warned against assuming even 1.28). I raised its solver bound from 1.25 to 1.40. **I have not demonstrated, as order §3 asks, that the 1.25 bound was an invalid method assumption** — only that the relations could not be met under it with the stature series and margins in the loop.
   - kb44, kb60 and kb80 sit within 1.3 % of their bounds (by value).
   - Upper-thorax length 1.240 sits within 0.8 % of its bound.
3. **Giant-pelvis read is not settled by numbers (§4).**
   - A cap on skeleton hip ÷ thorax at the largest human reference (1.106) could not be met together with ALPC-7 under the solver's margins (runs I1–I7). On the same profile reading, the equal-height Broad Skarn skeletons already read 1.097–1.100 (`skeletal/skb_continuity.json`). ALPC-7 itself uses a different reading (CIB crest ÷ thorax), so this is an empirical conflict under margins, not a proof that the cap and ALPC-7 cannot coexist at the bare 1 % convention.
   - I dropped the cap (reported only) and guarded "giant pelvis" by lumbar fill (no shelf) instead. Gorrund's skeleton reads hip ÷ thorax 1.141.
   - Whether the result looks like one load-bearing system is the author's visual call.
4. **The armpit band** (top ~8 cm) still cannot be tested for interpenetration. The new close renders and sections show a continuous arm–trunk junction there, not a closure (§7).

No canon conflict was found (§9). No UE5, topology, rig, animation, IK, equipment, camera, first-person, serialization, gameplay or class work was done.

**Independent audit.** An independent audit of this pass was run. Its verified findings are corrected or disclosed:
- the pelvis-cap reasoning (now evidenced in `skeletal/skb_continuity.json` and stated as an empirical conflict under margins);
- an overstated closure claim;
- the low-composition shelf and waist regressions;
- the femur-bound justification not meeting order §3;
- the C2 description;
- the knife-edge relations;
- the lowest ALPC-7 margin (the true 208 cm body);
- one row that lost margin;
- bound wording;
- the armpit-section band;
- tables.md text and labels. The trunk-crop and axilla sheets were re-rendered with the true statures.

## 1. What was done (order §2, §3, §6, §8)

**Solver gn6** (`w1i_drivers/gn6.py`; logs `solver/gn6_I1…I9.log`). Changes from W1h:
- **All stature bodies in the loop.** The reference, 208 / 215 / 222 / 251 cm, and every cross-height ALPC-7 pair are solved together.
- **Robustness margins** wider than the 1 % convention:

| Item | Margin |
|---|---|
| Strict > / < rows | 2.5 % |
| ≥ / ≤ rows | 0.8 % |
| '~' rows | within 0.006 |
| Arm clearance | ≥ 0.5 cm |
| Skin thoracic breadth > SK | 2.5 % |

- **Smoother sculpt.** The trunk sculpt is a smooth monotone cubic between nodes, with no slope break.
- **Fewer, more distributed parameters.** Posterior depth uses 2 values, not 4. A rib-cage bone breadth value (spine_02 / spine_03 X) was added, so thoracic breadth can be carried by bone rather than the upper-thorax tissue sculpt alone (W1h needed kb80 1.1684).
- **Continuity constraints** with limits taken from the accepted references (MF, SK, SG, GR, DU), not invented:
  - skeleton waist ÷ thorax ≥ least-pinched reference;
  - skeleton waist ÷ hip-block ≥ least-shelved reference;
  - crease (second-difference) readings ≤ reference maximum;
  - skin waist ÷ hip-block ≥ lowest reference;
  - a low-composition waist above the crest.
- **A barrier** keeps values away from bounds.

**Two constraint decisions, both disclosed in `gn6.py`:**
- **Skeleton hip-block ÷ thorax cap dropped (run I8).** It could not be met together with ALPC-7 under the solver margins (§4).
- **Femur-robusticity bound raised from 1.25 to 1.40 (run I6).**
  - With the stature series in the loop, runs I1–I5 pinned the femur at 1.25. The proximal-femur rows at 208–222 cm stayed short.
  - The 1.25 bound was a W1h search-range choice, not anatomy. The order itself names "robust proximal legs" and "proximal-femur robusticity" (§2, §6).
  - Femur length is unchanged.
  - This is not the demonstration order §3 asks for. The value is returned for a ruling.

**Final point:**
- The I9 solver point did not reach the robustness margins: summed shortfall 0.024, mostly skin thoracic breadth and the 208 cm rib-cage row.
- Then a **centering step C2** (`solver/i9point/center2.py`). 8 of the 16 values moved:
  - pelvis X / Y / Z, kb18 and kb31 moved 1 % toward the side their ±2 % sensitivity showed safe; the clavicle moved −1 %.
  - Upper-thorax length (+0.5 %) and rib-cage breadth (+0.3 %) had **no** safe side (both directions failed at the I9 point). They were nudged to recover thoracic breadth > SK, which pushed upper-thorax length closer to its bound.
  - Probe C1 also lowered three upper-thorax values; it dropped thoracic breadth > SK below 1 % and was not used.
- C2 was rebuilt, and every check below was re-run on it.
- **C2 is a manual step, not a solver result.** It was checked on all five solver bodies plus frames and composition.

## 2. Results (tables §3–§6)

| Body | Stature (cm) | Skeletal ALPC result | W1h |
|---|---|---|---|
| Reference | 230.90 | 35 / 35 reference rows; ALPC-0…4 15 / 15 | pass, thinner margins |
| GO-H208 (true minimum; not a solver body) | 208.27 | 15 / 15; ALPC-7 vs Broad Skarn 208 / 215 / 222 / 229 all pass | — |
| GOR-BODY-02 (W1f 208 cm donor) | 210.79 | 15 / 15 | 1 T-SENSITIVE |
| 215 donor | 217.03 | 15 / 15 | 1 MARGINAL |
| 222 donor | 224.08 | 15 / 15 | 1 T-SENSITIVE |
| GOR-BODY-03 | 252.97 | 15 / 15 | 15 / 15 |
| Frames 04 / 12 / 14 | 230.9 | 15 / 15, 15 / 15, 3 / 3 | all pass |
| ALPC-7, 10 height pairs | — | all pass; lowest margin +1.26 % over the convention (GOR-BODY-02 at 210.8 cm vs Broad Skarn 229). The true 208 cm body vs Broad Skarn 229: +1.11 % | 5 cross pairs NOT DEMONSTRATED |
| ALPC-6 skeletal half | — | 15 / 15 (same skeleton as the reference, so not an independent test) | 15 / 15 |
| ALPC-8 vs Durrim | — | all 5 readings GO > DU (torso +1.3 %, W1h +0.4 %); silhouette IoU front 0.839, side 0.771 | — |

**Statures are higher than the donor labels.** The W1i skeleton adds height: the reference is 230.9 cm (W1h 229.6). So the "208" donor now lands at 210.8 cm. GO-H208 was built at a lower height macro so the true 208 cm end of the range is tested. **No stature range was narrowed.**

**Margins.** Every Gorrund reference row but one gained margin over the pass threshold (tables §4). The exception is shoulder-joint breadth ÷ stature > GR, which fell from +19.96 % to +19.22 %. For example:

| Row | W1h | W1i |
|---|---|---|
| ALPC-7 crest ÷ thorax (equal height) | +0.50 % | +2.44 % |
| ALPC-1b rib-cage vertical ÷ breadth | +0.41 % | +2.19 % |
| Proximal femur ÷ crest ≥ SK | +0.72 % | +3.93 % |
| Bitrochanteric ÷ crest ≈ MF (two-sided) | +0.21 % | +0.48 % (still the thinnest) |

**Directional and skin rows:**
- Directional: 0 FAIL. The only NOT DEMONSTRATED rows are the Skarn elbow and knee (unchanged, direction only).
- Skin diagnostics, Gorrund (never a pass condition; tables §11):
  - lumbar depth ÷ thorax, crest ÷ lumbar and ALPC-7 pelvic depth now PASS;
  - pelvic depth ÷ crest vs SK is NOT DEMONSTRATED;
  - still FAIL: pelvic depth ÷ crest vs MF, bitrochanteric ÷ crest ≈ MF, pelvic AP ÷ thoracic depth, hip-level ÷ lumbar.

## 3. Construction values (R-14; all CONSTRAINED; tables §2)

| Value | W1h | W1i | Note |
|---|---|---|---|
| Pelvis [X, Y, Z] | [1.191, 1.036, 1.274] | [1.214, 1.045, 1.251] | inside bounds |
| Femur robusticity (breadth / depth) | 1.28 (outside the W1h bound) | **1.386** (bound 1.40; within 1 %) | needs author ruling |
| Clavicle length | 1.012 | 1.007 | |
| Upper-thorax length | 1.210 | **1.240** (bound 1.25) | |
| Rib-cage bone breadth (new) | — | 1.046 | carries thoracic breadth in bone |
| ka amplitude | 1.098 | 1.072 | moved off its bound |
| kp lower / upper | 1.23 / 1.26 · 1.38 / 1.29 | 1.62 / 1.28 | |
| kb r 0 / 0.18 / 0.31 | 1.00 / 1.18 / 1.22 | 1.02 / 1.16 / 1.30 | |
| kb r 0.44 / 0.6 / 0.8 | 0.94 / 1.04 / 1.17 | **0.91 / 0.91 / 1.14** | all within 1.3 % of a bound |

ka is anterior depth, kp posterior depth and kb breadth.

**Biological reading:**
- Width is carried by bone: a wider pelvis, a broader rib cage, more robust proximal femora.
- Lumbar soft tissue (kb31, posterior kp) is fuller, so the lumbar column reads as a load-bearing transition rather than a waist.
- The lower and mid thorax (kb44, kb60) are reduced to keep the rib-cage proportion rows.
- These remain CONSTRAINED construction values.

**Bound reliance is reduced but not removed.** The femur needed a larger bound. Four sculpt / length values sit near their bounds (0.64–1.27 % by value), and ka, kb60 and kb80 are inside the solver's 3 %-of-range barrier zone. The femur value is the one most in need of the author's view. It is what lets the crest, hip joints and thorax all satisfy their rows together.

## 4. Structural continuity (order §2, §5, §6; tables §7)

Readings use trunk-only plane sections every 2.5 % of hip-to-sternum height. Limits come from the accepted references.

| Reading | Skeleton W1h | Skeleton W1i | Skeleton references | Skin W1h | Skin W1i | Skin references |
|---|---|---|---|---|---|---|
| waist ÷ thorax (pinch; higher = less pinched) | 0.765 | **0.799** | 0.678–0.731 | 0.840 | 0.860 | 0.798–0.815 |
| waist ÷ hip-block (shelf; higher = less shelf) | 0.684 | **0.700** | 0.624–0.665 | 0.839 | 0.849 | 0.839–0.868 |
| hip-block ÷ thorax | 1.119 | 1.141 | 1.062–1.106 | 1.001 | 1.012 | 0.922–0.971 |
| crease (second difference), breadth / depth | 0.0084 / 0.0025 | 0.0081 / 0.0018 | ≤ 0.0147 / 0.0027 | 0.0029 / 0.0023 | 0.0040 / 0.0021 | ≤ 0.0062 / 0.0021 |

**Pinched-waist failure (order §2):** avoided.
- Gorrund's waist is fuller relative to its thorax than any reference, on skeleton and skin.
- The same holds at every stature, both frames and low composition (skin waist ÷ thorax 0.843–0.863).

**Giant-pelvis failure (order §2):**
- Lumbar fill relative to the pelvis is above every reference skeleton (0.700). Skin flank flare is negative at every body (−0.0104 to −0.0149) except GOR-BODY-16, whose 0.0000 is degenerate. The skeleton body's flare is +0.0196 (W1h +0.0220; minimum-composition references +0.022 to +0.030).
- **Exceptions:**
  - **Low composition (GOR-BODY-16):** skin waist ÷ hip-block 0.821, below the lowest skin reference (0.839); hip-block ÷ thorax 1.051, the highest of any skin body. So the low-composition body has more hip shelf than any reference. The solver applied the skin shelf guard to the reference body only.
  - **208 cm bodies:** skin depth crease 0.0025 (GOR-BODY-02) and 0.0026 (true 208), above the skin reference maximum 0.0021.
- **But hip-block ÷ thorax is above every human reference, on skeleton (1.141) and skin (1.012).**
- A cap at human values was tried (runs I1–I7) and could not be met together with ALPC-7 under the solver margins. On the same reading the equal-height Broad Skarn skeletons read 1.097–1.100 (`skeletal/skb_continuity.json`), while ALPC-7 requires Gorrund's CIB crest ÷ thorax to exceed theirs. That is a different reading, so this is an empirical conflict, not a proof.
- So the pelvis is proportionally the broadest of any body by canon. Whether it reads as an "independent oversized block" is the render question.

**Render sheets** (`sheets/`; one scale per sheet; side / front / front 3/4 / back 3/4):
- `go_stature_series_4view.jpg`: 208.3, 210.8, 217.0, 224.1, 230.9, 253.0 cm.
- `go_frames_composition_4view.jpg`: reference, Narrow, Broad, low composition, skeleton, W1h reference.
- `references_4view.jpg`: GO, SK, GR, MF, DU.
- `trunk_crop_noarms.jpg`: closer thorax → lumbar → pelvis crop, arms removed. Shows GO W1h vs W1i, both skeletons, low composition, 208 / 251 cm, Narrow, Broad, and SK, SK skeleton, GR, MF, DU.

My reading, for the author to confirm or reject:
- The W1i skin trunk reads as one column from chest to hips, with no flank shelf and no hourglass. The waist is subtle.
- **The skeleton (minimum-composition) body still shows a visible rib-margin edge at the lower thorax**, though softer than W1h. The accepted SK skeleton also shows a rib margin. It is a feature of the generator's minimum-composition mesh, not something I could remove with the sculpt.
- At the low-composition body a waist reads above the crest.

## 5. Low composition and ALPC-6 (order §5)

**Method finding (proven before acting, as order §11 asks for method changes).**
- The official measurement layer reads skin stations with ±1 cm vertex slabs. At the crest level of the stretched Gorrund mesh, that slab holds only 21 vertices and misses the crest ring.
- GOR-BODY-16 W1h: slab 36.6 cm vs exact section 42.2 cm. The slab therefore reports "no waist above the crest" when the section shows a clear one (crest ÷ narrowest level above it: slab 0.974 vs section 1.124; MF and SK at the same composition read 1.11).
- Evidence: `skeletal/waist_slab_vs_section.log`.
- **The official measurement layer was not changed.** The re-read is an attribution table only.

**ALPC-6 skin half (diagnostic; AD-W1H-4):**

| | Official slab reading | Plane-section re-read |
|---|---|---|
| W1h | 7 / 12 | 8 PASS, 1 NOT DEMONSTRATED, 3 FAIL |
| W1i | 7 / 12 | **10 PASS, 1 MARGINAL** (hip-level ÷ lumbar, 1.3003 vs 1.2991), **1 FAIL** (pelvic AP ÷ thoracic depth 0.936 vs 0.984) |

- The pelvic-depth row is the same one that has failed on skin since W1g. It passes on the skeleton.
- The low-composition waist reading (section) is 1.105 (W1h 1.124; MF 1.111, SK 1.110).
- No flank fat was added. The crest flare did not return.

## 6. Sensitivity (order §9; tables §9; `solver/sensitivity_w1i.json`)

**The test.** Each of the 16 values was perturbed alone by ±2 % (ka amplitude ±0.05). For each perturbation, five bodies were rebuilt: the reference and 208 / 215 / 222 / 251 cm. Every relation was re-checked with the ordinary rule:
- all reference rows;
- ALPC-0…4 at each stature;
- ALPC-7 at every cross-height pair;
- thoracic breadth > SK beyond 1 %.

This test is stricter than W1h's, which only covered the reference and 251 cm.

| Question (order §9) | Answer |
|---|---|
| Perturbations that keep every accepted relation | **23 of 32** (I9 point before centering: 18 of 32) |
| Any FAIL? | **1**: crest breadth kb18 −2 % breaks bitrochanteric ÷ crest ≈ MF. This is a two-sided ±0.010 row; pelvis X +2 % makes it T-SENSITIVE from the other side |
| Thoracic breadth > SK beyond 1 % | holds in **30 of 32**. Falls below 1 % at rib-cage breadth −2 % (−0.25 %, i.e. below SK) and upper-thorax length +2 % (+0.94 %). Next lowest: kb80 −2 % (+1.03 %) and kb60 −2 % (+1.06 %) |
| 251 cm stable? | **yes**: no row lost under any of the 32 |
| Shorter statures stable? | mostly. The rib-cage vertical ÷ breadth row is lost under: upper-thorax length −2 % (208 / 215 / 222 cm), kb60 or kb80 +2 % (208 cm only), and rib-cage breadth +2 % (208–222 cm). Rib-cage breadth +2 % also costs the ALPC-7 crest ÷ thorax row at the 208 and 215 cm cross pairs |
| Sensitive values | rib-cage breadth (both directions), upper-thorax length (both), pelvis X / Y, crest breadth kb18, kb60 / kb80 |
| Insensitive values | pelvis Z, femur, clavicle, ka, kp lower / upper, kb0, kb31, kb44 |

Arm clearance stays ≥ 1.71 cm and flank flare ≤ −0.0104 under every perturbation.

## 7. Arm clearance and armpit (order §7; tables §8; `sheets/axilla_close.jpg`)

**Tests:**
- Trunk-section test: 0 vertices inside in every body; clearance 2.07–3.54 cm.
- Arm-tube test (8.0–26.5 cm below the shoulder joint on the reference): 0 inside in every body.

**The close render** (`axilla_close.jpg`) covers GO reference, GOR-BODY-02, GOR-BODY-03, Broad and SK. Each has side / front / front 3/4 / back 3/4 from 16 cm above to 30 cm below the shoulder joint, plus horizontal sections at 2–14 cm below the joint (arm red, trunk grey).
- From about 10 cm down, the arm section is a closed ring with a visible gap to the trunk wall.
- At 2–8 cm the arm section is open or notched on its inner side. This is the junction where arm and trunk are one continuous skin, so there are no two surfaces that could interpenetrate.
- The accepted SK shows the same pattern.

**Status:** the band is **not demonstrated by measurement.** The renders show no fold or overlap there; the author should confirm visually. I am not claiming the band closed.

## 8. Other races (order §10–11)

- **No other race was retuned.**
- **Aelari:** the head / neck-base share option stays deferred. AE geometry is unchanged.
- **Grask:** the W1h body is kept.
- **Method change:** the `confine_legs` / PCHIP sculpt change applies only to the Gorrund recipe.
- **Directional, skin, ocular (all fit) and ear rows (22 PASS + 10 REPORT)** are unchanged except where Gorrund is the subject.

## 9. Canon-conflict statement

**No accepted canon was changed, overridden or found contradictory.** No stature range was narrowed; the true 208 cm body was added.

**One method finding the author should know:**
- In this construction, "no giant pelvis" could not be expressed as "pelvis ÷ thorax within the human references" together with ALPC-7 and the robustness margins. Canon ALPC-7 places Gorrund's crest ÷ thorax above Broad Skarn, whose skeleton already reads at the top of the human range on the profile reading (`skeletal/skb_continuity.json`). This was shown empirically, under margins, not proven.
- I therefore used lumbar continuity (no shelf, no pinch) as the numeric guard and leave the "oversized block" read to the renders.
- This is not a conflict between canon items; it is a limit on how the order's visual target can be measured.

## 10. Residual FAIL / MARGINAL / NOT DEMONSTRATED

**Skeletal:** none at any stature, frame or height pair.

**Composition / skin diagnostics:**
- ALPC-6 skin, official slab reading: 5 FAIL. On sections: 1 FAIL (pelvic AP ÷ thoracic depth) and 1 MARGINAL.
- Low composition: skin waist ÷ hip-block 0.821, below every reference; waist reading 1.105, below MF / SK (§4, §5).
- 208 cm bodies: skin depth crease above the reference maximum (§4).
- GO skin rows GO-P2a and ALPC-3 are NOT RUN in the skin table by design; both are run on the skeleton (reference skeletal table) and pass.
- GO skin: 4 FAIL, 1 NOT DEMONSTRATED (§2).
- VA skin pelvic depth FAIL (unchanged).

**Directional:** SK elbow and knee NOT DEMONSTRATED (direction only).

**Not demonstrated by measurement:**
- the armpit band;
- the "single load-bearing system" read (render);
- biological defensibility of femur 1.386 beyond "required by the accepted relations in this construction".

**Robustness:** 9 of 32 ±2 % perturbations lose a relation; 1 reaches FAIL.

**NOT RUN:**
- a re-solve with a smaller femur bound and relaxed robustness margins (to map the femur–margin trade);
- composition bodies at the shorter statures.

## 11. Recommendation: CONSTRAIN

Every Gorrund skeletal relation now holds across 208–253 cm, all frame bodies tested (the Broad body is render-only) and the shared low-composition skeleton. The margins are larger and the reference trunk is numerically more continuous.

The low-composition skin is not closed: ALPC-6 skin 1 FAIL + 1 MARGINAL on sections, a weaker waist than W1h and the references, and more hip shelf than any reference.

But the solution still has a two-sided knife edge (rib-cage breadth), several values sit at bounds, and the femur relies on a raised bound. The giant-pelvis question is visual.

**Rulings requested:**
1. The render read: one load-bearing system, or a torso on a pelvis?
2. Femur robusticity 1.386 and the raised bound.
3. Whether the remaining sensitivity is acceptable, or W1j should trade margin for interior values.
4. The armpit band, by render inspection.

STOP.

— Claude
