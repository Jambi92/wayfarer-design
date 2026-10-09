# RAC W2I4 — Saurin Final Asset Finish / Canonicalization-Prep Gate

**Author:** Claude (auditor) · **Date:** October 9, 2026 · **Order:** `reviews/chatgpt-rac-w2i4-saurin-final-asset-order.md` §1–§19

**Evidence:** `reviews/rac-w2i4-sa-evidence/`. `tables.md` is generated, and every number below comes from its JSON files.
**Status:** DESIGN / MEASUREMENT / REFERENCE-ASSET FINISH ONLY — NO UE5.
- **Nothing canonical was overwritten.** SA-M (aff1b52), SA-F (§263), the tool-chain sources (`tools/rodin/*`, gate-1 `g7*.py`) and Saurin canon are unchanged.
- The final candidates exist only as copies. The exact canonicalization file set, with hashes, is staged in scratch and on the PC under a separate candidates folder (§9).

## Verdicts

| Item | Verdict | One line |
|---|---|---|
| **L1 leg biology** | **ACCEPT** | Preserved exactly: hip 0.5333 H, femur / leg 0.420, lower trunk unchanged (§1). |
| **F2 forearm biology** | **ACCEPT** | Preserved exactly: forearm / arm 0.366, total arm 0.400 H (§1). |
| **Finished L1 + F2 reference asset** | **CONSTRAIN** | Measurements, regression and tail coupling are unchanged from W2I3, and the scale field is regenerated. The thigh relief is only partly re-modelled (§3, §4). |
| **Scale-field regeneration** | **ACCEPT** | The stretched / compressed field is gone and spacing is uniform everywhere. The layout is a new realization of the accepted generator, because the accepted seed file no longer exists (§2). |
| **Thigh relief quality** | **CONSTRAIN** | The anterior / lateral thigh now has native-scale relief. The medial / posterior thigh keeps the stretched W2I3 relief, and the procedural transfer leaves small artifacts at the sector boundary (§3). |
| **SAU-SILHOUETTE** | **ACCEPT WITH PRESENTATION CONTEXT** | Closed by author ruling. The caudal system was not touched, and the strict front view is shown for provenance only (§6). |
| **Tail coupling** | **ACCEPT** | The finish changes no cap, and dlean by at most 0.0005° (§5). |
| **Saurin W2I final overall** | **CONSTRAIN** | The body plan, regression, surface field and coupling are final-quality. One asset item remains: medial / posterior thigh relief (§3, §10). |
| **Canonicalization readiness** | **NOT READY** | Only the thigh relief blocks it. The file set and canon text edits are prepared (§9). |

---

## 1. Accepted measurements preserved (order §4, §12)

Ledger shares of standing height (hip = pelvic station; `tables.md` §1). W2I4 equals W2I3 to four decimals:

| SA-M188 | ground → ankle | ankle → knee | knee → hip | lower trunk | thoracic | neck | head height |
|---|---|---|---|---|---|---|---|
| frozen | 0.0511 | 0.2789 | 0.1544 | 0.1703 | 0.1544 | 0.1114 | 0.0796 |
| W2I4 final | 0.0511 | 0.2789 | 0.2033 | 0.1703 | 0.1347 | 0.0821 | 0.0796 |

| Reading (SA-M188 / SA-F188) | Frozen | W2I4 final |
|---|---|---|
| Hip / H | 0.4843 / 0.4786 | 0.5333 / 0.5276 |
| Femur / leg | 0.355 / 0.355 | 0.420 / 0.421 |
| Forearm / arm | 0.312 / 0.312 | 0.366 / 0.367 |
| Total arm / H | 0.4007 / 0.3958 | 0.4004 / 0.3955 |
| Lower trunk (cm) | 32.0 / 33.6 | 32.0 / 33.6 |
| Head length / H | 0.1696 / 0.1698 | 0.1696 / 0.1698 |
| Lean (§257 model) | 8.82° / 8.42° | 8.42° / 8.05° |

Across all 62 bodies and every scalar measurement, the largest W2I3 → W2I4 change is **0.044 %** (a centre-of-mass coordinate).

The finish cannot move a body measurement:
- The lateral-extreme vertices of the torso width bands and the thorax-depth section are held.
- The axial station vertices are held.
- The caudal system, the feet and the head are held.

A first finish pass without these holds moved the Narrow-female thoracic d/w from 0.9994 to 1.0004 and failed the §263 ≤ 1.00 guard. That pass was rejected and the holds were added.

## 2. Scale / surface field regeneration (order §7)

**Route** (`sa_surface.py`; it mirrors final-brow `build15.sh`):
1. Upsample the finished base.
2. Region fields.
3. Run the accepted gate-1 `g7surfc.py`, unchanged.
4. Produce the final normal-only delta.

**Region fields.** The accepted `g15reg` labels are carried by vertex correspondence, since topology is identical: family, size R, height, elongation, imbrication, plates, attenuation and tympanic. Each vertex therefore keeps its accepted scale family and absolute scale size.

Only the geometry-dependent fields are recomputed:
- vertex normals;
- the scale flow direction, transported through the per-face deformation gradient.

Re-running `g7regs.py` on the finished base was rejected: its band and joint construction points are the frozen `g7geo` ones, so it would mislabel the moved knee, elbow and neck bands.

**Construction anchors.** `g7surfc.py` reads `g7geo` anchors for the palmar / plantar pads and the eyes. The L1 + F2 body raises the hands by **6.06 cm**, so those anchors are carried to the finished base by a wrapper (`g7surfc_moved.py`) that leaves `g7surfc.py` itself unchanged. Without the wrapper, the hand pads would have been placed 6 cm below the palms.

**Seeds — limitation.** The accepted surface was built with a carried seed file (`seeds15.npy`). That file is not in the repo or on the PC. Recovery from the frozen delta failed (`sa_seeds.py`):
- As local maxima, correlation with the frozen field after regeneration is 0.20–0.23.
- As plateau centroids, the cells do not separate at the mesh resolution.
- Independent seeds give 0.26, so neither recovery method beats chance.

The field was therefore regenerated with fresh variable-radius Poisson seeds (rng 7, c 0.50), and the seed file is now saved with the asset (`saurin_w2i4_surface_relief.npz`).

**Consequence: every individual scale is a new placement**, including on the unchanged head and tail. Generator, family, size, height, elongation and imbrication are the accepted ones, and the head close-up is indistinguishable in character (`sheets/w2i4_scale_field.jpg`, last column).

**Continuity** (`fieldcheck.json`). The table gives the vertical / horizontal correlation-length ratio of the scale relief; a stretched field departs from the control.

| Region | frozen control | BEFORE (accepted field carried onto L1 + F2) | AFTER (regenerated) |
|---|---|---|---|
| thigh | 1.107 | **1.331** | 1.176 |
| neck | 1.071 | **0.858** | 1.071 |
| thorax | 1.079 | 0.979 | 1.126 |
| upper arm | 1.079 | 0.960 | 1.035 |
| forearm | 0.974 | 1.053 | 0.982 |
| shank (geometry unchanged) | 1.299 | 1.299 | 1.436 |

The shank row shows the realization-to-realization spread, about ±0.14. Every AFTER value lies within it of the control. Seed spacing / R is uniform across regions (median 0.511–0.541; all seeds p10 / p50 / p90 0.50 / 0.53 / 0.62), so there is no density step at the thigh, knee, neck, shoulder, forearm or pelvis.

**Other checks:**
- No new player-visible range.
- RM-UB-08 numeric creator ranges stay **OPEN / NAMED DEPENDENCY**.

## 3. Thigh relief (order §5–§6)

The accepted +9.2 cm thigh, femur / leg, hip / knee stations and girths are unchanged. The finish (`sa_finish.py`) only re-models surface relief.

**Method.**
1. Split the thigh surface at 1.5 cm into form plus fine relief.
2. Re-sample the fine relief at its native vertical scale from the frozen thigh, anchored at the knee transition (63 cm) and the hip crease (86 cm + 9.2).
3. Cross-fade the two anchor samples through mid-thigh with amplitude normalization.
4. Iterate three times so the re-measured relief equals the target.

Muscle-scale forms keep the longer thigh, which reads as longer muscles over a longer femur.

**Measured** (`thigh_relief.json`: vertical correlation length of the 1.5 cm relief in cm; native = frozen):

| | whole mid-thigh | anterior / lateral (re-modelled) | medial / posterior (kept) |
|---|---|---|---|
| frozen (native) | 3.31 | 2.63 | 3.94 |
| W2I3 rebuild | 5.47 | 4.17 | 6.67 |
| W2I4 final | 5.06 | **2.92** | 6.75 |

**What did not work:**
- **Whole-thigh transfer.** On the medial / posterior thigh (adductor, hamstring face, crotch wall), every transfer variant produced artifacts that W2I3 does not have: sharp pits, torn-looking patches and lumps. The variants tried were vertical-offset sampling, a binned cylinder parameter, a smooth fitted-axis parameter, a 3 cm split and a soft amplitude cap.
- **Why.** These faces turn toward the other leg and the pouch, so the vertically offset source points do not correspond. The final finish therefore applies the re-model to the anterior / lateral sector only, and leaves the upper inner thigh untouched.
- **Duplication.** Inserting 9.2 cm means the frozen 70–79 cm band is read from both anchors. Inside the cross-fade it appears twice, at reduced amplitude; there is no hard repeat.
- **Residual artifacts.** A few small marks remain near the sector boundary on the medial view (`sheets/w2i4_thigh_relief.jpg`, bottom row, medial column).

**Verdict: CONSTRAIN.**
- The anterior / lateral thigh — the quadriceps and iliotibial face that reads in front, side and 3/4 — is native-scale and clean.
- The medial / posterior thigh is still the stretched W2I3 relief.
- A procedural re-sample cannot invent the missing 9.2 cm of hamstring / adductor relief. **An artist sculpt pass on the medial / posterior thigh is the remaining reference-quality item** (§10).

**Anatomical continuity checklist (§6):**

| Item | State |
|---|---|
| Gluteal-to-proximal-femur flow | Faired; unchanged form |
| Hip crease | Native relief at the upper anchor |
| Adductor origin / inner thigh | Faired W2I3 form (stretched) |
| Quadriceps mass | Unchanged forms; native fine relief |
| Hamstring posterior flow | Faired W2I3 form (stretched) |
| Knee-to-thigh tendon transition and condyles | Native (lower anchor) |
| Calf entry | Unchanged |
| Female / male compatibility | 0 flips, female centre included |
| Over-bulking or human-bodybuilder anatomy | None added |

## 4. Neck / shoulder / axilla / elbow cleanup and topology (order §8, §14)

**Displacement fairing.** Forty uniform-Laplacian iterations smooth the rebuild displacement field inside the transition zones: thigh band ends, neck, shoulder cap / trapezial slope, axilla and elbow. Station vertices, measurement-carrying vertices, tail, feet and head are held.

Maximum finish displacement by zone (cm):

| Zone | Max (cm) |
|---|---|
| Thigh ends, including the relief re-model | 0.73 |
| Neck | 0.08 |
| Shoulder | 0.08 |
| Axilla | 0.14 |
| Elbow | 0.05 |
| Outside the zones and the thigh | 0 |

**Fold guards.** A fold guard runs over **all 62 bodies**. Wherever any body would get a face flipped against its own W2I3 rebuild, or (in 11 core states) a new face flipped against the frozen body, it attenuates the delta locally and smoothly. It converged in 5 rounds: 1,426 → 301 → 59 → 15 → 0.

**Results** (`quality.json`):

| Check | Result |
|---|---|
| Flipped faces vs W2I3, all 62 bodies | **0** |
| Flipped faces vs frozen, SA-M188 / SA-F188 | **0 / 0** |
| New near-fold faces vs frozen (W2I3 not already flipped there) | 139 in 18 non-core bodies: LT90 lower-trunk cases and high muscle / fat composition cases; 0 in the 11 core states |
| Pre-existing W2I3 flips vs frozen (same bodies) | 1,185, inherited from the composition / LT90 warps |
| Surfaced SA-M188 topology | Closed (0 boundary), manifold (0 non-manifold), 0 degenerate faces, Euler characteristic 2 |
| Surfaced faces flipped against their own base | 2,320 (frozen asset: 2,332) |

The 139 near-fold faces are faces the W2I3 composition warp had already turned close to 90° away from the frozen orientation.

Edge strain vs frozen, SA-M188 (W2I3 → W2I4):

| Region | p99 | p1 | Minimum |
|---|---|---|---|
| Thigh | 1.497 → 1.521 | — | 0.924 → 0.637 |
| Neck | 1.000 → 1.002 | 0.667 → 0.662 | 0.655 → 0.493 |
| Arm | 1.264 → 1.264 | — | — |

The lower minima are isolated edges inside the re-modelled relief and the faired neck band, not band-wide. The W2I3 shoulder crease stays removed, and the folded-axilla build stays rejected (axilla zone delta ≤ 0.14 cm).

## 5. Final regression and tail coupling (order §12–§13)

**Regression.** All 62 bodies were built with the final route (`bodies_F.json`) and run through the accepted evaluators, unchanged. **Result changes vs W2I3: 0 of 493 internal checks, 0 limb / cross-race row changes, 0 cross-race non-pass:**

| Suite | Result |
|---|---|
| Stature (SAU-BODY-01) | ST 64 / 64 |
| Continuity | C 26 / 26 |
| Frames (SAU-BODY-05) | FR 104 / 104 |
| Composition firewall (SAU-BODY-06 / 07) | CO 96 / 96 |
| §263 sex cases (SAU-BODY-19) | 17 PASS + the 2 canon "request exceeds" CONSTRAIN cases |
| Lower-trunk floor | LTF 8 / 8 |
| Matched-height directions (SAU-BODY-03 / 12 / 21 / 22, RM-OT-04 body) | M 138 / 138 |
| Passing, with / without tail | P 76 / 76, P0 76 / 76 |
| Gorrund never-collapse | G 6 / 6 |
| Durrim leg separation (SAU-BODY-16 body rows) | 24 / 24 |
| Cogling forearm separation (SAU-BODY-15) | 8 / 8 |
| Grask reach (SAU-BODY-13) | 14 PASS + D-B Broad 208 span +0.51 % (accepted marginal) |
| Plantigrade foot, claw coupling | Feet held, pads carried (SAU-BODY-11 / 18) |
| Caudal / pelvis continuity (SAU-BODY-04 / 17 / 18) | Tail, pelvis and caudal base held by the finish |
| SAU-BODY-10 | Lean 8.42° |

**0 new biological failures versus W2I3.**

**Tail coupling** (`tables.md` §5; same-state rule, RSI 1.19 convention). The confirmation compares three runs:
- **W2I4** — the final asset.
- **Control** — the W2I3 rebuild without the finish (`tailcap_R_control.json`).
- **W2I2** — the W2I2 study warp.

| | Balanced 188 | Broad 188 | Narrow + high fat 188 | Broad 208 |
|---|---|---|---|---|
| W2I4 cap | 78.875 % | 80.25 % | 79.625 % | 79.75 % |
| W2I4 − W2I3 control | 0 | 0 | 0 | 0 |

**Named cases:**
- dlean W2I4 − W2I3 is ≤ 0.0005° in every case.
- 55 % substantial base: A50 still binds at the low end, as before.
- Same-state lean rule: unchanged.

**Drift vs W2I2 — traced, not a W2I4 regeneration error.**
- The W2I3 clean rebuild differs from the W2I2 study warp by +0.02–0.03° dlean and −0.125 % on three caps (one 0.125 % grid step).
- The finish contributes none of this.
- This moves the beyond-anchor case "Narrow + high fat 78 % (base 1.15)" from 2.985° to 3.006°, over the +3° guard. The W2I3 `sa_eval.py` already classified that case FAIL (TL, report-only). The anchors (Balanced 78 %, Narrow + fat 72 %) pass.
- Broad 80 % stays the accepted D-B marginal.

## 6. SAU-SILHOUETTE and the presentation note (order §2–§3, §9)

Recorded as **ACCEPT WITH PRESENTATION CONTEXT**. The caudal system was not touched:
- landmark, axis origin, root area, RSI, length, taper, thickness and carriage;
- pelvis, sacral origin and leg spacing.

Tail readings are bit-identical to W2I3 (root area 529.21, RSI raw 50.09). The strict front orthographic view appears in the final sheets for provenance only.

The presentation note was added to `decisions/REFERENCE_ANATOMY_V1.md` §10 as a general rule (orthographic end-on projection is presentation context, not anatomy). No animation work was started.

## 7. Visual evidence (order §11)

All sheets are in `reviews/rac-w2i4-sa-evidence/sheets/`. Rendering is the shaded Workbench reference with cavity. The tool chain has no material / texture path, so a shaded, material-free render is the reference it supports.

| Sheet | Contents |
|---|---|
| `w2i4_SA-M188_final.jpg`, `w2i4_SA-F188_final.jpg` | Front, both sides, front 3/4, rear 3/4, rear; close thigh / hip, knee, neck / shoulder, axilla / forearm, caudal base; strict front ortho (provenance) |
| `w2i4_family.jpg` | 168 / 188 / 203 / 208 from the same regional route, surfaced |
| `w2i4_before_after_M188.jpg`, `w2i4_before_after_F188.jpg` | W2I3 rebuild (accepted field carried) vs W2I4 final |
| `w2i4_thigh_relief.jpg` | Frozen / W2I3 / W2I4 base: front, lateral, rear, medial |
| `w2i4_scale_field.jpg` | Control / before / after: thigh, knee, neck, forearm, shoulder, head |

## 8. Asset-quality verdicts (order §14)

| Item | Verdict |
|---|---|
| Topology / face integrity | **ACCEPT** — closed manifold; 0 flips vs W2I3 on 62 bodies; 0 vs frozen on SA-M / SA-F |
| Thigh anatomical relief | **CONSTRAIN** — anterior / lateral native; medial / posterior stretched (§3) |
| Knee continuity | **ACCEPT** — native lower-anchor relief; field continuous (1.182 vs 1.153 control) |
| Neck / shoulder continuity | **ACCEPT** — faired; crease gone; field 1.071 = control |
| Axillary / forearm continuity | **ACCEPT** — no fold; forearm field 0.982 vs 0.974 control |
| Regenerated scale-field continuity | **ACCEPT** — no density step; new realization (§2) |
| Male / female compatibility | **ACCEPT** — same finish; SA-F 0 flips; §263 unchanged |
| Stature-family continuity | **ACCEPT** — ST 64 / 64, C 26 / 26 |
| Caudal integration | **ACCEPT** — caudal system bit-identical; coupling unchanged |
| Reference render quality | **CONSTRAIN** — sheets complete, but medial thigh marks are visible at close range |

## 9. Canonicalization package (order §15–§16)

### 9a. Final hashes

Candidate files are staged in scratch and copied to the PC at `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/candidates/w2i4/`, beside `out/`, which is not overwritten. The 50 MB delta and the 238 MB field file stay in scratch.

| File | SHA-256 |
|---|---|
| `saurin_w2i4_base.npz` (finished SA-M188 base, `{v, f}`; faces identical to the frozen base) | `f86ae800a4ef60c7b78ca466433290b7c10e80654df9a02026abb7762353fdee` (vertices `b50a3d4b…`) |
| `saurin_w2i4_surface_relief.npz` (scalar relief + 130,949 seeds) | `3e8c3824044dab1b1afcc404bdff35b94e9641542419c4cb10cadaf450b72b7b` |
| `saurin_w2i4_surface_delta.npz` (normal-only `d`, same format as the frozen delta) | `33b94baba2f41aaa246992443e34c4b1fc704987d85b6492a435cc2a0f17bc1f` |
| `rebuild_w2i4.py` (final = `igl.upsample(base)` + s·N) | `6958eedebbf4ca1f80528ec010bf23a2c0c8957aa433f04b6716bfd66068208d` |
| `saurin_w2i4_SA-F188_realization.npz` (§263 female centre on the finished base) | `8019420a9ee5c45731698c15fa6a11047bf5e7c1a6cc547b3d52d2716c1fc187` |
| `saurin_w2i4_regfields.npz` (carried fields + recomputed N / T) | `eea2d2fc23a382798caed597fd35b13b94e20a60c432f9900c11659a4217f0af` |
| `finish_delta.npz` | `4bf8c0f345dcd60e1a29e5e1db24a1ddced4873a67151d9ab125cf5c129853e9` |
| Final surfaced SA-M188 (4,496,934 vertices) | vertex SHA `8b32dae6816c43f60badac8944238a74388487baa183715db73529b981a546a1` |

**Provenance kept, not deleted:**
- `saurin_final_base.npz` `a925e067…`
- `saurin_final_surface_delta.npz` `b72691ab…`
- `rebuild_final.py` `722b0420…`

**File checks:**
- Upsample reproduction: 1.1e-5 cm.
- The relief file reproduces the delta within 0.087 mm; the only difference is the ground-contact clamp on the soles. The delta file itself is exact.

### 9b. Exact canonicalization file list (on author acceptance)

1. **Mesh / asset:**
   - replace `RaceBodies/out/saurin_final_base.npz` with `saurin_w2i4_base.npz`;
   - replace `saurin_final_surface_delta.npz` with `saurin_w2i4_surface_delta.npz`;
   - replace `rebuild_final.py` with `rebuild_w2i4.py` (or keep the delta form);
   - re-export `SaurinFinal.blend` / `.fbx` from the final surface (not produced here: no UE5 / export work in scope);
   - add the saved seed file.
2. **Tool chain:**
   - `Lbase.pkl`: labels carry over (same topology); stations move with the rebuild;
   - Part 7 `ref_metrics.json`;
   - Gate 8 `axis.npy`: tail axis translated with the pelvis, +9.2 cm;
   - `g7geo.py` `ARM` / `LEG` construction points: elbow, knee, hip, and the hand pad / claw anchors (+6.06 cm);
   - `g15reg` → `saurin_w2i4_regfields.npz`;
   - re-verify §263 `fsets3`.
3. **Canon / decisions:**
   - `specs/saurin/SAURIN_V1.md` (§9c);
   - `decisions/REFERENCE_ANATOMY_V1.md` ARM entry: new SA-M / SA-F hashes, old hashes kept as W1 / W2I provenance;
   - `cfg/w2i/SA-boundary.json`;
   - `rac-w1-evidence/saurin_w1.json`;
   - `specs/STATUS.md`.

### 9c. Exact proposed canon text edits (not applied)

**Part 7 header (L4130).** Replace "All validation was derived from the frozen closure reference (aff1b52) without modifying it." with:

> All validation was derived from the frozen closure reference (aff1b52) without modifying it. **W2 reference update (RAC W2I4, accepted [date]):** the Saurin reference is the W2 L1 + F2 asset (`saurin_w2i4_base.npz` `f86ae800…`); aff1b52 remains the W1 / W2I provenance reference. Values below marked W2 are measured on the W2 reference; tail, head, trunk, pelvis and §263 values are unchanged by it.

**§256 opening (L4147).** Unchanged. The tail is 121.4 cm along the relaxed centreline, 64.6 % of standing height, identical on the W2 reference.

**§257 (L4164).** Replace "the frozen reference's centre of mass lies ~6.3 cm behind the heel contact and the reference stance would need ~**8.8° of forward whole-body lean**" with:

> the W2 reference's centre of mass lies ~6.2 cm behind the heel contact (aff1b52: ~6.3 cm) and the reference stance would need ~**8.4° of forward whole-body lean** (aff1b52: 8.8°)

**§258 (append after the bounds paragraph).**

> **W2 re-verification (RAC W2I4):** the bounds are unchanged and re-verified on the W2 reference (neck length ±15 %, leg length ±6 %, arm length ±6 %; full W2I regression 0 new failures). The W2 reference body plan is hip 0.533 H (pelvic station), femur / leg 0.42, forearm / arm 0.37 with total arm ~0.40 H.

**§17 upper limbs (after L298).**

> **Forearm interpretation (author ruling W2I2 → W2I3 1B):** "modest forearm emphasis" is a modest tendency inside a moderate arm system — W2 reference forearm / arm ≈ 0.366, inside the Marchfolk range and below Cogling distal redistribution and Grask reach specialization. Exact humerus / forearm ratios beyond this reference remain OPEN.

**Stature-share accounting (after the metric note, L974).**

> **W2 stature budget (RAC W2I3 / W2I4, author-accepted):** the elongated lower axial trunk (0.170 H, unchanged) is paid for by reduced thoracic (0.135 H) and neck (0.082 H) vertical shares, not by the legs; head height (0.080 H) and head length are unchanged. Legs: hip at the pelvic station 0.533 H.

**§263 reference accounting.** Unchanged figures: lower trunk 32.0 → 33.6 / 34.3 cm; external pelvic width 41.7 → 43.1 / 42.8 cm; thoracic d/w 0.880 → 0.922 / 0.922; head length / H 0.170. Append:

> Re-verified on the W2 reference (RAC W2I4): identical; waist / shoulder and waist / hip to be re-confirmed by `fsets3` at canonicalization.

**New presentation note (§256 item 8 or §257).**

> **Presentation context (author ruling W2I3 SAU-SILHOUETTE, October 8, 2026):** Do not judge the Saurin tail solely from a dead-flat orthographic front view. Final character-creator and showcase presentation should rely on complete front / 3/4 / profile context, material definition, lighting and natural tail motion. The strict orthographic end-on projection is not a biological defect.

**§265 OPEN items.** Add the accepted marginals and named dependencies, unchanged:
- D-B Broad ~80 % / Broad 208 span;
- D-D skeletal-mass measurement limit;
- RM-UB-08 creator ranges;
- facial (RM-OT-04 OPEN rows, RM-UF-04) and claw numeric ranges;
- density / neutral idle / dynamic posture;
- SAU-SILHOUETTE presentation dependency.

## 10. Complete named-dependency accounting

| Item | Classification |
|---|---|
| Medial / posterior thigh relief (stretched W2I3 form; small boundary marks) | **OPEN ASSET ITEM** — blocks canonicalization; artist sculpt pass recommended |
| Scale layout is a new realization (accepted seeds lost) | **DISCLOSED** — author to confirm; the seed file is now saved |
| `SaurinFinal.blend` / `.fbx` re-export | **CANONICALIZATION STEP** (not in W2I4 scope) |
| 139 near-fold faces in LT90 / high-composition cases (0 vs W2I3) | **REPORT** — inherited composition-warp folds |
| SAU-SILHOUETTE | **ACCEPT WITH PRESENTATION CONTEXT** |
| Broad ~80 % / Broad 208 span +0.51 % | **ACCEPTED MARGINAL D-B** |
| Skeletal-mass rows | **ACCEPTED DEPENDENCY D-D** |
| TL Balanced 80 %, Narrow + fat 78 % (beyond anchors) | REPORT-ONLY (unchanged) |
| RM-UB-08 numeric ranges | **NAMED DEPENDENCY** |
| Facial dependencies (RM-OT-04 OPEN rows, RM-UF-04), claw numeric ranges | **NAMED DEPENDENCY** |
| Final density / neutral idle / dynamic posture | **NAMED DEPENDENCY** |
| SAU-BODY-20 world-space | **OUT OF SCOPE** |

**Repository hygiene.** This commit holds only:
- Saurin W2I4 drivers and evidence;
- the W2I3 ruling records;
- one general §10 rule in `REFERENCE_ANATOMY_V1.md`.

No unrelated file changed.

## 11. Author decision requested

The thigh is the only blocker. The options:
- **(a)** Authorize an artist sculpt pass on the medial / posterior thigh over this candidate. Everything else is carried as-is, with the measurements guarded by the same regression.
- **(b)** Accept the CONSTRAIN thigh as reference quality and canonicalize now.
- **(c)** Remove the thigh relief re-model and canonicalize with the faired W2I3 thigh plus the regenerated scale field.

Please also confirm that the new scale-field realization (§2) is acceptable in place of the lost accepted layout.

**STOP.**
