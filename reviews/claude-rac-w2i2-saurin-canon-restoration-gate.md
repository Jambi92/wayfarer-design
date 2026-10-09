# RAC W2I2 — Saurin Canon-Restoration Candidate Study / Silhouette Closure Gate

**Author:** Claude (auditor) · **Date:** October 8, 2026 · **Order:** `reviews/chatgpt-rac-w2i2-saurin-canon-restoration-order.md` §1–§19
**Evidence:** `reviews/rac-w2i2-sa-evidence/`. `tables.md` is generated, and every number below comes from its JSON files.
**Status:** DESIGN ONLY / NO UE5. CANDIDATE STUDY.
- **No accepted source anatomy was modified.** SA-M (aff1b52), SA-F (§263), the tool-chain files and Saurin canon are unchanged.
- Every candidate is an in-memory displacement of a copy. No candidate is marked accepted.

## Verdicts

| Item | Verdict | One line |
|---|---|---|
| **Saurin leg-canon restoration candidate (L1)** | **CONSTRAIN** | L1 restores the canon leg relations by a measured margin and passes every cross-race regression. The cost is a shorter neck and a modestly shorter vertical thorax, plus local mesh strain that needs a re-sculpt before it could become canon (§3). |
| **Saurin forearm-canon restoration candidate (F2)** | **ACCEPT** (as a candidate) | Forearm / arm goes from 0.312 to 0.366, inside the matched Marchfolk band, while shoulder, wrist, hand, total arm and every trunk reading stay exactly unchanged. Literal "emphasis" needs F3, which sits within 1 % of Grask (§4). |
| **Combined limb candidate (L1 + F2)** | **CONSTRAIN** | 0 new failures in the accepted W2I suites (FR 104 / 104, CO 96 / 96, ST 64 / 64, M 138 / 138, P / P0 76 / 76, LTF 8 / 8). L1's neck and strain cost and the canonical re-sculpt are author decisions (§5). |
| **SAU-SILHOUETTE root-carriage candidate** | **REJECT — ROOT-CARRIAGE LEVER INSUFFICIENT** | Root pitch up to +8° cuts the visible extent from 12.7 to 5.7 cm (SA-M188), but the rounded dark mass is still read. Part of it is non-tail crotch tissue that no carriage moves (§6). |
| **Tail coupling under recommended root carriage** | **NOT RUN** | No root carriage passes. On the combined limb candidate the same-state caps rise about 0.5 point and every guard and coupling rule holds (§7). |
| **D-B marginals** | **ACCEPTED MARGINAL** (recorded) | Broad ~80 % and Broad 208 span +0.6 %. The span persists on every candidate (+0.54 … +0.68 %). Broad 80 % becomes reachable at 188 on L1 + F2 (cap 80.4 %) but stays 0.1 point short at 208. |
| **D-D structural-mass dependency** | **ACCEPTED DEPENDENCY** (recorded) | Recorded in `decisions/REFERENCE_ANATOMY_V1.md` and STATUS. |
| **Saurin W2I2 overall** | **CONSTRAIN** | The limb canon is restorable by a bounded candidate; the author must accept its cost. SAU-SILHOUETTE remains unresolved by carriage. |

---

## 1. Stature-budget ledger (order §3)

Each share is part of standing height (tail excluded). Columns:

| Column | Saurin | MPFB comparators |
|---|---|---|
| Ankle, knee, hip | J-2 construction joints (B1 axis) | rig joints |
| Hip → pelvic hip-joint station | B1 hip → station u 91 | 0 by definition |
| Lower trunk | station → costal u 123 | rig hip → costal proxy |
| Thoracic | costal → inlet u 152 | |
| Neck | inlet → chin | |
| Head height | chin → vertex | |

Every row sums exactly to standing height. Driver: `w2i2_drivers/sa_ledger.py`.

| Share of H | SA-M188 | SA-F188 | MF190 | MF168 | MF203 | DU137C |
|---|---|---|---|---|---|---|
| ground → ankle | 0.051 | 0.051 | 0.041 | 0.042 | 0.041 | 0.042 |
| ankle → knee | 0.279 | 0.276 | 0.246 | 0.256 | 0.242 | 0.243 |
| knee → hip | **0.128** | 0.126 | **0.249** | 0.228 | 0.258 | 0.228 |
| hip → pelvic transition | 0.027 | 0.027 | 0 | 0 | 0 | 0 |
| lower axial trunk | **0.170** | 0.179 | **0.130** | 0.131 | 0.130 | 0.130 |
| thoracic | 0.154 | 0.153 | 0.151 | 0.153 | 0.149 | 0.166 |
| neck | **0.111** | 0.110 | **0.057** | 0.059 | 0.056 | 0.049 |
| head height | **0.080** | 0.080 | **0.127** | 0.132 | 0.124 | 0.142 |

SA-M168, SA-M203 and SA-M208 match SA-M188 to within ±0.003 in every segment (`tables.md` §1).

**Where the Saurin budget goes** (SA-M188 vs MF190):

| Segment | Saurin vs Marchfolk |
|---|---|
| Lower trunk | +0.040 H (the canon excess) |
| Head + neck together | 0.191 vs 0.183, ≈ Marchfolk |
| Thorax | 0.154 vs 0.151, ≈ Marchfolk |
| Legs (ground → pelvic station) | 0.484 vs 0.537, −0.053 H |

- **The entire lower-trunk excess is paid by the legs.** Head and thorax are not reduced at all, which contradicts L970.
- Within the head + neck block the split is unusual: a shallow reptilian head (head height −37 % vs Marchfolk) over a long neck (inlet → chin about 2× Marchfolk). Canon says head height "near to modestly below" and neck "broadly near Marchfolk".
- **Head length / rostral bounds are not used as a lever** (order §3). Head length and head height stay unchanged in every candidate.

## 2. Candidate construction (order §4–§5, §8, §12)

All levers are smooth displacements on copies (`w2i2_drivers/sa_cand.py`). The accepted regional stature route then builds 168–208 from them.

**Legs (G cm at 188, total height constant).**
- The **thigh band** (u 63–85, between the knee fields and the crotch) is stretched by G.
- Funding comes from the open budget only:
  - **thorax** (u 124–151, above the costal station): 40 % of G;
  - **neck** (u 157–170, above the shoulder tops, below the chin): 60 % of G.
- Pelvis, lower trunk, caudal base and tail translate rigidly with the hip, so the caudal base never moves relative to the pelvis.
- Arms and head translate rigidly. Foot, ankle, shin and knee fields are untouched.
- **The lower trunk is never used as funding** (LT / H unchanged to 4 decimals in every candidate).

**Candidate hip.**
- The candidate hip is the **accepted pelvic hip-joint station** (u 91 on the frozen body). This is the station of the canon lower-trunk accounting, applying order §5 "hip station consistent with the accepted pelvis".
- The Gate 4 B1-axis hip (5 cm lower) is reported beside it in every table. On that reading every candidate's hip share is 0.027 H lower.

**Why 40 / 60.**
- A first 25 / 75 split (thorax / neck) visibly shrugged the shoulders: the neck nearly vanished at L3 and a crease formed across the shoulder tops.
- A neck band starting at u 153 caused the same crease.
- Those runs are superseded and not used. With 40 / 60 and the neck band above the shoulder tops, both blocks end about 11 % below Marchfolk: thorax 0.135 vs 0.151, head + neck 0.162 vs 0.183. That is the "modestly reduced vertical head / thoracic contribution" of L970.

**Forearm.**
- Within-arm redistribution along each shoulder → wrist chord.
- The elbow zone moves δ cm toward the shoulder.
- Shoulder, wrist, hand and the arm-to-wrist chord are fixed.
- The axillary blend tapers to zero before any torso-labelled vertex. An earlier version leaked about 0.05 cm into the Narrow-female thoracic width and moved two §263 clamp cases to d/w 1.0005 / 1.0012. It was fixed and rebuilt, and trunk readings are now exactly unchanged.

**Root carriage.** An upward pitch of the free-tail direction that ramps smoothly from 0 at the caudal base to θ over LP cm, then stays constant (§6).

## 3. Leg candidates L1 / L2 / L3 (order §4, §6–§7)

**Lever sizes.**
- L1 = **G 9.2 cm**: the smallest gain that puts hip height and leg length ≥ 1 % above Durrim for **both sexes at every stature**.
- L2 = G 10.3 cm.
- L3 = G 11.6 cm.

**Ranges over 168–208 (male / female):**

| Reading (share of H) | As-built | L1 | L2 | L3 |
|---|---|---|---|---|
| Hip height (pelvic station), M | 0.482–0.486 | **0.531–0.535** | 0.537–0.541 | 0.544–0.548 |
| Hip height, F | 0.477–0.480 | **0.525–0.530** | 0.531–0.535 | 0.538–0.542 |
| Hip height (B1 axis), SA-M188 | 0.458 | 0.507 | 0.513 | 0.520 |
| Leg to ankle, M | 0.436–0.439 | **0.485–0.488** | 0.490–0.494 | 0.497–0.501 |
| Femur / leg (SA-M188) | 0.355 | 0.420 | 0.427 | 0.435 |
| Lower leg / leg | 0.645 | 0.580 | 0.573 | 0.565 |
| Lower axial trunk / H | 0.170 | 0.170 | 0.170 | 0.170 |
| Thoracic / H | 0.154 | 0.135 | 0.132 | 0.130 |
| Neck / H | 0.111 | 0.082 | 0.078 | 0.074 |
| Head height / H | 0.080 | 0.080 | 0.080 | 0.080 |
| Standing height, head length, d/w | — | unchanged | unchanged | unchanged |
| Tail %, root area, RSI, platform − hip | — | unchanged | unchanged | unchanged |

**Margins against the boundaries (hip height; leg length where shown):**

| Boundary | As-built | L1 | L2 | L3 |
|---|---|---|---|---|
| vs Durrim (must exceed) | −6.0 … −7.8 % (FAIL) | **+1.7 … +3.5 %** (legs +1.1 … +2.8 %) | +2.8 … +4.7 % | +4.1 … +6.0 % |
| vs matched Marchfolk | −8.8 … −12.0 % | **−3.0 … +0.5 %** (legs −4.3 … −0.5 %) | −1.9 … +1.6 % | −0.7 … +2.9 % |
| vs matched Fenn / Aelari / Vael (single reading) | −9.3 … −14.0 % | **−5.2 … −0.1 %** | −4.2 … +1.0 % | −2.9 … +2.3 % |
| vs Grask 208 | −13.3 % | **−4.5 %** (legs −6.2 %) | −3.5 % | −2.2 % |

**Cross-race regression** (accepted `sa_compare.py`, unchanged, on each candidate set): LTF 8 / 8, M 138 / 138, P 76 / 76, P0 76 / 76, G 6 / 6 — **no non-pass on any candidate**.
- Lower-trunk floor at 168 / 203 still PASS. LT is unchanged, so the AD-R36 margins are unchanged.
- SAU-BODY-03 / 12 / 21 / 22 and the RM-OT-04 rows are all PASS, as are the separation counts vs Sagekin, Halvren, elves and Skarn.
- Gorrund never-collapse holds (d/w 0.82–0.86).

**Reading the three.**
- **L1** meets all four §6 boundaries:
  - exits Durrim at every stature for both sexes;
  - approaches the lower Marchfolk tendency (within 3 % instead of 8–14 % below);
  - stays below Grask and below elf single readings;
  - LTF passes.
- **L2** sits inside the Marchfolk band and touches the elf readings (+1.0 %).
- **L3** exceeds both Marchfolk and the elf single readings (+2.9 / +2.3 %) and comes within 2.2 % of Grask. It is closest to "distributed limb elongation" and is **not recommended**.
- Elf identity is a complete-body pattern (W2E rule), and every candidate keeps the +30 % Saurin lower trunk, so no candidate becomes elf-like. L1 is still the least disruptive.

**Costs of L1, honestly stated.**
- **Neck:** the vertical neck (inlet → chin) falls 26 %, from 0.111 to 0.082 H. That is still 44 % above Marchfolk, so "broadly near" is approached but not reached. It is visible as a shorter neck (`sheets/w2i2_legs_M188.jpg`).
- **Thorax:** thoracic vertical falls 13 %. Thoracic depth and d/w are unchanged, so the deep thorax is intact.
- **Local mesh strain:** the construction stretches the thigh band up to ×1.48 vertically and compresses the neck band to ×0.45. That is acceptable for a proportional study, but scale fields, musculature and folds there would have to be **re-sculpted / regenerated**, not warped, before any canonical adoption.
- **Shoulder height:** shoulders sit about 6.9 cm higher, with the arms carried rigidly. Wrist height rises with them, but arm length and reach ratios are unchanged.

## 4. Forearm candidates F1 / F2 / F3 (order §8–§9)

| SA-M188 | As-built | F1 (δ 2.2 cm) | **F2 (δ 4.2 cm)** | F3 (δ 5.0 cm) |
|---|---|---|---|---|
| Upper arm / H | 0.164 | 0.152 | **0.142** | 0.137 |
| Forearm / H | 0.125 | 0.136 | **0.147** | 0.151 |
| Arm-to-wrist / H | 0.288 | 0.288 | 0.288 | 0.288 |
| Total arm / H | 0.401 | 0.401 | 0.401 | 0.401 |
| Forearm / arm | 0.312 | 0.340 | **0.366** | 0.377 |
| Forearm / upper arm | 0.764 | 0.897 | **1.036** | 1.098 |
| Hand / arm | 0.280 | 0.281 | 0.281 | 0.281 |
| Elbow height u (cm) | 117.0 | 119.1 | 121.0 | 121.7 |
| Elbow / wrist section ÷ H (surface) | 0.058 / 0.043 | 0.058 / 0.042 | 0.058 / 0.042 | 0.058 / 0.042 |
| Span index | 1.049 | 1.049 | 1.049 | 1.049 |

**Margins.**

| Boundary | F1 | **F2** | F3 |
|---|---|---|---|
| vs matched Marchfolk forearm / arm | −6.2 … −8.1 % (still clearly below) | **−1.1 … +1.1 %** (inside the band) | +1.7 … +4.1 % (modest emphasis) |
| vs Cogling forearm / arm | −12 % | −5.5 … −5.7 % | −2.7 … −3.0 % |
| vs Grask forearm / arm (208) | −11 % | −3.7 … −4.9 % | **−0.9 … −2.2 %** (SA-F208 NOT DEMONSTRATED) |

- In every candidate total arm stays −1.1 … −3.7 % below Marchfolk (moderate).
- Hand anatomy, the hand claws and the shoulder are untouched.
- No new joint or silhouette discontinuity (`sheets/w2i2_forearm_M188.jpg`).

**Recommended: F2**, the least disruptive candidate that removes the contradiction ("no longer strongly below Marchfolk").
- Literal "modest forearm emphasis" is F3. F3 passes Cogling but meets Grask forearm share within 1 % at 208. It is offered, not recommended.

## 5. Combined candidate L1 + F2 (order §10)

Full W2I body list (62 bodies) rebuilt with L1 + F2.

**Accepted internal checks** (`sa_eval.py`, unchanged; candidate vs the as-built re-run):

| Suite | Result |
|---|---|
| Stature family (SAU-BODY-01) | ST 64 / 64 |
| Continuity | C 26 / 26 |
| Frames (SAU-BODY-05) | FR 104 / 104 |
| Composition (SAU-BODY-06 / 07) | CO 96 / 96 |
| §263 sex cases (SAU-BODY-19) | 17 PASS + the 2 canon "request exceeds" cases; **§263 clamps reproduced** (d/w 0.9994 / 0.9996) |
| Tails | TL: same as as-built except one row (below) |

**The one result change.** **SA-M208-B-T80 changes from FAIL to PASS** on the old SA-M-referenced lean guard (+3.03° → under +3°). This happens because the candidate's longer legs lower every body's lean by about 0.4–0.5°. The other two TL failures (Balanced 80 %, Narrow + fat 78 %) remain.

**Cross-race** (`sa_compare.py`): every row PASS, as for L1 (§3).

**Limb rows:**
- Durrim legs 24 / 24 PASS (+1.1 … +3.5 %).
- Cogling 8 / 8 PASS.
- Grask 14 PASS + the **D-B Broad 208 span marginal (+0.64 %)**.
- Arm vs Durrim REPORT (−0.3 … +1.5 %).

**SAU-BODY dispositions on the combined candidate:**

| Validator | Disposition |
|---|---|
| 01 / 05 / 06 / 07 / 19 | PASS (above) |
| 03 | PASS (M rows vs Marchfolk) |
| 04 integrated organism | Pelvis, caudal base and tail move as one rigid unit; tail readings unchanged to 4 decimals |
| 10 neutral stance | Lean 8.37° (as-built 8.82°); no hunch or crouch |
| 11 | Legs restored (§3), forearm inside the Marchfolk band (§4), total arm moderate. Skeletal presence stays D-D |
| 12 / 21 / 22 | PASS |
| 13 | PASS + D-B marginal |
| 15 | PASS |
| 16 | Legs PASS; joint mass D-D |
| 17 | Feet untouched (foot / H unchanged) |
| 18 | TL as above |

Before / after sheets: `sheets/w2i2_combined.jpg` (M188, F188, 168, 208).

**Same-state tail regression on the combined candidate** (D2 rule; `tailcap_L1F2.json`): see §7.

**No accepted Saurin identity rule is broken by L1 + F2.** It is still a CONSTRAIN, because of the L1 neck / strain cost and the need for a canonical re-sculpt (§3).

## 6. Root-carriage family (order §12–§14)

**Bend length.** **LP = 10 cm**, the smallest tested length (10 / 15 / 20) whose bend keeps the maximum smoothed centreline curvature (0.997°/cm) below the as-built free-tail maximum (1.52°/cm). So there is no root kink by construction.

**Invariance in every case.**
- Caudal-base point unchanged (shift 0).
- Non-tail vertices ≤ 6e-7 cm, so stance, pelvis and legs are unchanged.
- Tail length, sections and mass change ≤ 0.02 %.
- Δlean ≤ +0.04°.
- No flag: distal elevation 20.5° at +8°, against 12.5° neutral.

**Results:**

| Root pitch | SA-M188 visible extent / gap share / max width | Lowest tail point | SA-F188 visible extent | SA-M208 visible extent |
|---|---|---|---|---|
| 0° | 12.7 cm / 6.3 % / 14.8 cm | u 67.6 | 18.0 | 20.6 |
| +2° | 11.7 / 5.2 % / 14.3 | 69.4 | 16.0 | 18.6 |
| +4° | 9.7 / 4.1 % / 13.4 | 71.3 | 14.0 | 16.6 |
| +6° | 7.7 / 3.1 % / 12.3 | 73.1 | 13.0 | 14.6 |
| +8° | **5.7 / 2.1 % / 11.2** | 75.0 | **11.0** | **12.6** |

The 78 % tail goes from 17.7 to 8.7 cm and the 55 % tail from 9.7 to 3.7 cm (full table in `tables.md` §5).

**Visual answer (close front and below-front views, `sheets/w2i2_rootcarriage_*.jpg`).** Even at +8° a **dark rounded mass is still read** between the thighs. It is smaller and less pendulous, but still not clearly a caudal structure. Three things limit the lever:
- **Tail split render** (`sheets/w2i2_tail_split_M188.jpg`: full / tail removed / tail only). Even with every tail-labelled vertex removed, a dark rounded form remains at the apex of the thigh gap. It is the posterior pelvic / caudal-base blend, which the order forbids changing, and no carriage moves it.
- **The end-on tail disc** hangs below that form. Root pitch shrinks it (lowest point +7.4 cm at +8°) but does not clear it.
- **To clear it, the tail underside would have to rise above the crotch** (≈ 6 cm more on SA-M188). By the measured rate (≈ 0.9 cm per degree) that is about +14° of root pitch, beyond the +8° limit and into an alert / raised carriage. It was not tested.

→ **ROOT-CARRIAGE LEVER INSUFFICIENT.** As ordered, no lateral yaw, pelvic remodelling or tail thinning was invented.

## 7. Tail coupling (order §15) and D-B check

**Under root carriage: NOT RUN** (no passing carriage).

**On the combined limb candidate (information for D-B, `tailcap_L1F2.json`, same-state D2 rule, RSI 1.19 base):**

| State / case | As-built (W2I1) | L1 + F2 |
|---|---|---|
| Balanced 188 cap | 78.4 % | **78.9 %** |
| Broad 188 cap | 79.75 % | **80.4 %** |
| Narrow + high fat 188 cap | 79.1 % | **79.75 %** |
| Broad 208 cap | 79.4 % | **79.9 %** |
| Named: Balanced 78 % (base 1.15) | +3.00° PASS | +2.84° PASS |
| Named: Broad 80 % (base 1.16) | +3.39° FAIL | +3.21° FAIL at that base (reachable to 80.4 % on the permissive base) |
| Named: Narrow + fat 72 % / 78 % (base 1.10 / 1.15) | +1.78° PASS / +3.16° FAIL | +1.68° PASS / **+2.98° PASS** |
| Named: 208 Broad 80 % (base 1.16) | +3.51° FAIL | +3.33° FAIL at that base (cap 79.9 %) |
| Named: Balanced 80 % (rule base) | +3.78° FAIL | +3.58° FAIL |
| 55 % (base 0.85 / 0.83) | PASS | PASS; 55 % on the smallest admissible base still fails A50 (coupling unchanged) |

The longer legs lower each state's lean slightly, so every cap rises by about 0.5 point. The coupling system and guards are unchanged.

**D-B:** under L1 + F2 the Broad 188 cap reaches 80.4 %, so the marginal would no longer be needed at 188. At 208 the cap is 79.9 %, 0.1 point short, so the D-B marginal stays valid there. On the frozen as-built reference D-B applies unchanged.

## 8. Complete non-pass accounting (order §17)

| Item | Classification |
|---|---|
| Leg contradiction (hip 0.45–0.49 H; legs shorter than Marchfolk and Durrim) | **RESOLVED BY D-A CANDIDATE** (L1; candidate only, awaiting author acceptance) |
| SAU-BODY-16 leg rows vs Durrim | **RESOLVED BY D-A CANDIDATE** (24 / 24 PASS on L1 / L1 + F2) |
| Forearm contradiction (forearm / arm −15 % vs Marchfolk) | **RESOLVED BY D-A CANDIDATE** (F2 inside the Marchfolk band; F3 for literal emphasis) |
| Broad ~80 % marginal | **ACCEPTED MARGINAL D-B** (as-built). On L1 + F2: Broad 188 cap 80.4 % (anchor met), 208 cap 79.9 % (still marginal, §7) |
| Broad 208 span +0.6 % vs Grask | **ACCEPTED MARGINAL D-B** (+0.54 … +0.68 % on every candidate) |
| Skeletal-mass rows (SAU-BODY-14 / 16 joints, S7) | **ACCEPTED MEASUREMENT LIMIT D-D** |
| SAU-SILHOUETTE | **UNRESOLVED** (distal and root carriage both insufficient; part of the read is non-tail tissue) |
| TL Balanced 80 %, Narrow + fat 78 % (base 1.15) | REPORT-ONLY (W2I1: Balanced cap 78.4 %; Narrow + fat 78 % reachable on the permissive base) |
| TL 208 Broad 80 % | ACCEPTED MARGINAL D-B (now PASS on the old-reference guard under L1 + F2) |
| RM-UB-08 numeric field ranges | **NAMED DEPENDENCY** (a canonical L1 would also need the scale surface regenerated, §3) |
| Facial dependencies (RM-OT-04 OPEN rows, RM-UF-04) | **NAMED DEPENDENCY** |
| Claw numeric ranges | **NAMED DEPENDENCY** |
| Final density / neutral idle / dynamic posture | **NAMED DEPENDENCY** |
| SAU-BODY-20 world-space | **OUT OF SCOPE** |
| Neck vertical still +44 % vs Marchfolk on L1; local mesh strain | REPORT-ONLY (candidate cost, §3) |

## 9. Statement on source anatomy

**Not modified.** The following are byte-identical:
- `saurin_final_base.npz` (a925e067…);
- the §263 SA-F parameters;
- `tools/rodin/creator-biology` and the gate sources;
- `specs/saurin/SAURIN_V1.md`.

The root-pitch lever is an in-memory, asserted text extension of `vary.warp` inside `sa_cand.py`. The repo source is untouched.

## 10. Files that would need canonicalization **if** the author later accepts L1 + F2

1. **Reference mesh.**
   - A new frozen base replaces `saurin_final_base.npz`, rebuilt by re-sculpting the thigh, neck and upper-arm regions (not by warping).
   - `SaurinFinal.blend` / `.fbx`, `rebuild_final.py` and `saurin_final_surface_delta.npz` on the PC (`RaceBodies/out/`).
   - The scale surface regenerated with `gate1/g7surf.py` / `g7regs.py`.
2. **Tool chain** (`tools/rodin/creator-biology`, `female/closure`, `gate1`):
   - `Lbase.pkl` labels and stations;
   - `ref_metrics.json` (Part 7 reference metrics);
   - the Gate 8 tail axis `axis.npy`;
   - `g7geo.py` `ARM` / `LEG`: elbow and B1 hip / knee construction points, or the pelvic-station hip adopted as the hip joint;
   - `fsets3.py` §263 states, re-verified (clamps reproduce on the candidate).
3. **Canon text** (`specs/saurin/SAURIN_V1.md`):
   - the Part 7 reference metric tables and stature accounting;
   - an explicit statement of the vertical budget (thorax / neck reduction);
   - §258 creator bounds re-verified (neck length ±15 %, leg length ±6 %, arm length ±6 %);
   - §263 accounting (lower trunk 32.0 → 33.6 cm unchanged).
4. **Records:**
   - `decisions/REFERENCE_ANATOMY_V1.md` ARM entry (new SA-M / SA-F hashes);
   - `tools/rac/w1/cfg/w2i/SA-boundary.json`;
   - `reviews/rac-w1-evidence/saurin_w1.json` reference values;
   - W2I / W2I1 evidence re-runs (`w2i_drivers`, `w2i2_drivers`);
   - `specs/STATUS.md`.

---

**STOP.** SA-M / SA-F were not overwritten and canon was not rewritten. Wave 3, the final roster world-scale review, creator envelopes, the internal Saurin skeleton, UE5, rigging, animation, equipment and gameplay were not begun. This W2I2 candidate package goes to the author for review.
