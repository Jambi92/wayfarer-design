# RAC W3C — Skarn craniofacial tendencies (RM-CF-09) author gate

**Order:** `reviews/chatgpt-rac-w3b1-final-acceptance-w3c-skarn-craniofacial-order.md`
**Evidence:** `reviews/rac-w3c-sk-evidence/`:
- `tables.md`, `pairs.json`, `metrics.json`;
- `overrides/`, `builds/`;
- `accepted_asset_hashes.json`;
- 4 sheets.

**Drivers:** `tools/rac/w1/w3c_drivers/` (`w3c_face.py`, `w3c_measure.py`, `w3c_sheets.py`, `w3c_tables.py`, `AS_RUN.sh`); configuration record `tools/rac/w1/cfg/w3c/SK-face.json`.
**Scope:** W3B canon writeback, plus a diagnostic W3C measurement and candidate study. No UE5. SKARN_V1 numeric ranges are unchanged.

---

## 0. Verdicts

| Item | Verdict |
|---|---|
| **W3B canon writeback** | **COMPLETE** — SAURIN_V1 §267 (with §259 / §262 / §265 pointers), REFERENCE_ANATOMY_V1 §9 and §10, STATUS and RMQ. Committed as af84f63 (§1). |
| **W3B / W3B1** | **FINAL CLOSED** — with the explicit note that PD-1 … PD-4 are not solved. |
| **PD-1 assignment** | **RECORDED** — owner: procedural surface / skin-detail transport (SAURIN_V1 §267.5). |
| **PD-2 assignment** | **RECORDED** — owner: character-body deformation / composition solver. |
| **PD-3 assignment** | **RECORDED** — owner: procedural scale-field generation plus the validity / resampling layer. |
| **PD-4 assignment** | **RECORDED** — owner: procedural scale-field generator robustness. |
| **RM-CF-09 skull-size tendency** | **CONSTRAIN** — measured from accepted anatomy: at matched stature the Skarn head is **+1.6 % larger relative to stature** (head height ÷ stature). This holds at 183, 190 and 203 cm, in both configurations, on Narrow and Broad frames. Head *shape* is identical: breadth, depth and lower-cranial breadth differ by ≤ 0.1 %. "More robust skull" is therefore **not present in accepted anatomy**. A builder-chosen candidate (+2 % breadth, +1 % depth) is returned. |
| **RM-CF-09 brow tendency** | **CONSTRAIN** — **not present in accepted anatomy**: glabellar projection differs by ≤ 1.5 %, which is noise. A builder-chosen candidate shift is returned: restrained +56 % glabellar / +26 % supraorbital projection; stronger +115 % / +53 %; first caricatured +193 % / +99 %. AUTHOR DECISION REQUIRED. |
| **RM-CF-09 jaw-mass tendency** | **CONSTRAIN** — **not present in accepted anatomy**: bigonial breadth ÷ head height differs by +0.2 to +1.0 %. Builder-chosen candidate: bigonial +2.6 % (restrained) / +10.6 % (stronger), with the gonial angle lower. Mandibular body depth is unchanged in every case: the generator's "jaw drop" moves the gonial angle, not the menton. The neck-to-jaw transition is **+1.5 to +2.3 % in accepted anatomy**, from the accepted Skarn neck girth. |
| **RM-CF-09 midface tendency** | **CONSTRAIN** — **not present in accepted anatomy**: bizygomatic, malar, cheek-depth and nose metrics differ by ≤ 0.8 %, except noise-level alar-breadth rows. Builder-chosen candidate: malar breadth +4.5 %, nasal projection +6.9 %, nasal height +1.0 %, alar breadth +7.7 % (restrained). Anterior cheek projection is unchanged. |
| **Individual-overlap / anti-stereotype requirement** | **PASS** — all six overlap cases are valid. Each Skarn case falls below the matched-height Marchfolk value on its region, or crosses below a strong Marchfolk case. No metric separates the populations: accepted Skarn and Marchfolk faces are identical on every face metric. No hair, beard, scars or texture are used anywhere. |
| **Skarn complete-face result** | **CONSTRAIN** — restrained (k 1.0) and stronger (k 2.0) candidates are valid, human, neutral faces. k 2.0 is the upper end: its profile brow is marginal. k 3.3 is the first caricatured candidate, with a brow shelf and an over-broad head. The configuration-2 replication (k 1.0) behaves the same way. Which candidate becomes the Skarn central tendency is an author decision. |
| **RM-CF-09 overall** | **CONSTRAIN** — accepted anatomy supports only a small head-size and neck-to-jaw tendency. Brow, jaw and midface tendencies exist only as builder-chosen diagnostic candidates. No creator envelope was demonstrated, and no frequency is inferred. |
| **RM-CF-05 input package** | **CONSTRAINED** — FPI / MPI / MdPI readings are given for every W3C face (Appendix A). Candidate readings are builder-chosen. MPI is confounded by brow forward-projection, because N* moves forward. |

### Required reports (§16)

1. **Metrics and landmarks:** §2.
2. **Normalized readings:** §3, §4 and `tables.md`.
3. **Values from accepted anatomy:** §3; classes are marked in `metrics.json`.
4. **Builder-chosen values:** §4.1 and `cfg/w3c/SK-face.json`.
5. **Creator envelope or central tendency only:** **central-tendency evidence and candidates only.** No creator envelope was demonstrated.
6. **Overlap cases:** §5.
7. **FAIL / MARGINAL / NOT DEMONSTRATED / NOT RUN:** §7.
8. **Persistent files changed:** §9.
9. **SKARN_V1 numeric ranges changed:** **NO** (status pointer text only).
10. **Accepted Skarn or Marchfolk anatomy reopened:** **NO.** All accepted meshes are unchanged (`accepted_asset_hashes.json`; files predate W3C; the committed SK reference geometry is identical). Finding F-1 (§3) is reported for the author, not acted on.

---

## 1. W3B canon writeback (§2–§4)

- **SAURIN_V1 §267** (new):
  - §267.1 value categories (biological bound / conditional biological reach / unconditional production-safe / creator-safe cap / construction-only);
  - §267.2 IOD −8 % … +3 %, with the +14.x % conditional headroom, no interpolation across cranial width 0.92–1.00, vertical / AP locked, and the integrated orbit system;
  - §267.3 ridge m 0.60 … 1.30; m ≥ max(0.60, temporal-legibility floor); C-R1 retained; one global control; temporal line binding; scales never create skull identity; ridges cannot be toggled off; C-R2 retired. The calibration equation and constants are excluded.
  - §267.4 region-specific facial and body field tables; C-B2 as a biological relationship; "creator cap ×1.5" stated explicitly as **not a species maximum**, and no "maximum Saurin scale size". Eyelid ~×1.3 and shin ~×0.6 are conditional biological reach, while ×1.0 / ×0.8 are unconditional production-safe values; the fold tolerance is not raised. Auricular ×1.3 is the seed-robust creator-safe endpoint only.
  - §267.5 PD-1 … PD-4 with owners; C-B1 is not biology; no range is reduced.
  - §267.6 construction-only values.
  - Closure note: PD-1 … PD-4 are not solved; the thigh art-pass item is unchanged.
- **Pointers** in SAURIN_V1 §259 (horizontal spacing resolved), §262 (ranges now in §267.4) and §265 (two OPEN items marked resolved).
- **REFERENCE_ANATOMY_V1:** §9 W3 row marks W3B / W3B1 closed. A new §10 method rule covers surfaced-envelope measurement, the value categories, the production-dependency separation and the resampling rule.
- **STATUS / RMQ:** a closure line, plus RM-UF-03 / RM-UF-04 / RM-UB-08 rows marked CLOSED with pointers.
- **Not touched:** UFCA / UCCA (no pointer was needed), the canonical W2 Saurin asset, the evidence directories and the diagnostic code.

## 2. Metrics and landmarks

All metrics are surface (skin) proxies on the R-6 MPFB ARM meshes (x lateral, f anterior, u up, cm). Landmarks come from the W1c `cranio()` set (`arm_measure.py`; framework `reviews/claude-pass2-r3-craniofacial-framework.md`): G*, N*, prn, sn, sto, Pg, Me, V, Op, Po* (concha proxy), Eu–Eu, Zy–Zy, Or* / Os* / Mf* / Ec*.

**HL** = head length (FAL–Op). **HH** = head height (V–Me).

| Family | Metric | Definition | Repeatability on identical-shape pairs |
|---|---|---|---|
| Skull | HH_H, HL_H | head height or head length ÷ stature | ±0.1 % |
| | Eu_HH | cranial breadth ÷ HH | ±0.1 % |
| | HL_HH | cranial depth ÷ HH | ±0.1 % |
| | LCB_HH | head breadth at the Po* level (ears excluded) ÷ HH: lower-cranial / jaw-support proxy | ±0.1 % |
| | cranial volume | **not used** — no closed cranial surface exists without inventing internal anatomy | — |
| Brow | **BGP** | (G*.f − N*.f) ÷ HL — glabellar projection over nasion | ±1.5 % |
| | BSO | front-most surface 0.6–2.4 cm above each eye centre (within ±0.5 cm of the eye's x) minus the corneal apex, ÷ HL | **±10 %** (vertex sampling); secondary |
| | BOR | supraorbital front minus infraorbital front ÷ HL | ±15 %; secondary |
| Jaw | **BGB_HH** / BGB_Zy | bigonial breadth ÷ HH or ÷ Zy. Go* = lateral-most head surface (ears excluded) in the gonial band: u from Me + 0.8 to sto − 0.6, f between Po* + 0.5 and Ec* − 2 | ±0.3 %; +1 % on low-muscle bodies (both populations) |
| | MDH | (sto.u − Me.u) ÷ HH — mandibular body depth | ±0.7 % |
| | RAM | (Po*.u − Go*.u) ÷ HH — ramus / gonial-angle height | ±0.2 % (frame / low muscle +9 %, equal in both populations) |
| | CW_Zy | chin breadth at the Pg level within 1.2 cm behind Pg ÷ Zy (secondary) | ±0.1 % |
| | **NJT** | neck breadth (neck-weighted skin) 3 cm below Me ÷ bigonial breadth — neck-to-jaw transition | ±2 % |
| Midface | **BZY** | Zy–Zy ÷ HH (bizygomatic) | ±0.1 % |
| | **MAL** | anterior malar breadth: 0.10–0.19 HH below the eye centres, anterior to 0.10 HH behind them, ÷ HH | ±0.9 % |
| | CHK | cheek front (1.6–3.2 cm below the eye centre, at the eye's x) minus Po*.f, ÷ HL — maxillary depth | ±0.1 % |
| | MPI | W1c midface projection (Pr − N*) ÷ HL | ±1 %; **confounded by brow** |
| | **NH / NP / AB_Zy** | nasal height (N* − sn) ÷ HH; nasal projection (prn − sn) ÷ HL; alar breadth ÷ Zy | ±1 % / ±0.4 % / **±5 %** |

**Separation of soft tissue from skeletal structure.**
- The generator's face does not respond to body composition: SK208 high-fat and high-muscle faces are identical to the reference on every face metric.
- Fat or neck muscle therefore cannot masquerade as jaw mass in these meshes. The flip side is that the generator has **no body-to-face soft-tissue coupling at all** (SKARN_V1 v1.2 §7 remains pending; §7 below).
- The Narrow + low-muscle frame moves the gonial-band metrics by about 1–2 % equally in both populations, through neck slimming. It is reported, not scored as jaw mass.

## 3. Accepted anatomy — matched-stature readings (SK − MF, % of MF)

| Pair | HH_H | Eu_HH | HL_HH | LCB | BGP | BGB_HH | MDH | NJT | BZY | MAL | CHK | NP | NH |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 183 config 1 (lower overlap) | **+1.7** | 0.0 | −0.1 | 0.0 | −0.7 | +0.2 | −0.3 | +6.9* | 0.0 | 0.0 | +0.1 | +0.2 | −0.7 |
| 190 config 1 (mid overlap; equal-height test) | **+1.6** | 0.0 | −0.1 | 0.0 | −0.8 | +0.2 | −0.7 | **+1.7** | 0.0 | 0.0 | +0.1 | +0.3 | −0.7 |
| 203 config 1 (MF maximum) | **+1.6** | 0.0 | −0.1 | 0.0 | −0.2 | +0.2 | −0.3 | **+1.7** | 0.0 | −0.8 | +0.1 | +0.2 | +0.1 |
| SK208 reference vs MF203 (**endpoint, not matched**) | +0.9 | 0.0 | −0.1 | −0.1 | −0.8 | +0.2 | −0.2 | +1.5 | 0.0 | −0.8 | +0.1 | +0.4 | +0.1 |
| 190 Narrow + low muscle | **+1.7** | 0.0 | −0.1 | 0.0 | −0.3 | +1.0 | +0.1 | +1.2 | 0.0 | 0.0 | +0.1 | +0.3 | +1.1 |
| 190 Broad, reference composition | **+1.6** | 0.0 | −0.1 | 0.0 | −0.5 | +0.2 | +0.5 | +1.8 | 0.0 | 0.0 | +0.1 | +0.3 | +0.1 |
| 190 config 2 (replication) | **+1.6** | −0.1 | 0.0 | −0.1 | +1.5 | +0.8 | −0.6 | **+2.3** | −0.1 | −0.1 | +0.1 | +0.4 | −1.6 |
| 203 config 2 (replication) | **+1.6** | 0.0 | 0.0 | −0.1 | +0.8 | +0.7 | +0.4 | **+2.1** | −0.1 | −0.1 | +0.1 | +0.3 | −0.7 |

\* The 183 neck reading includes band-sampling noise. Absolute head height: SK 23.8 / 24.4 / 25.6 cm against MF 23.4 / 24.0 / 25.2 cm at 183 / 190 / 203. Full table, including the noise-level BSO / BOR / AB rows, is in `tables.md` §1–§2.

**Finding F-1 (reported, not acted on).**
- The accepted Skarn ARMs (W1 SK 208 and the W2B stature / frame / composition variants) use body targets only. Their faces are the generator's default human face, the same face as Marchfolk.
- At matched height every face-shape metric agrees within measurement noise. The only measured Skarn facial tendencies in accepted anatomy are:
  - a **slightly larger head relative to stature (+1.6 %)**, consistent with "skull suited to body size";
  - a **slightly more substantial neck-to-jaw transition (+1.5 to +2.3 %)**, from the accepted Skarn neck girth.
- This is not a contradiction of canon: SKARN_V1 v1.0 §8 deferred craniofacial ranges, and the SK ARM was accepted with "generator-target magnitudes as reference construction values". It does mean the canonical brow, jaw, midface and nose tendencies (v1.2 §1) are **not yet embodied in any accepted Skarn asset**.

## 4. Builder-chosen diagnostic candidates (REFERENCE_ANATOMY §7)

### 4.1 Declared builder-chosen values

The **tendency package per unit k** is applied on copies of the accepted SKM190 (configuration 1) and SKF190 (configuration 2). Stature is re-solved to 190 cm; the body is otherwise unchanged.

| Target | Value per k | Region |
|---|---|---|
| `head-scale-horiz-incr` / `head-scale-depth-incr` | 0.12 / 0.08 | skull breadth / depth |
| `eyebrows-trans-forward` | 0.30 | brow / supraorbital region forward (geometry, not hair) |
| `chin-bones-incr` / `chin-jaw-drop-incr` | 0.30 / 0.15 | jaw breadth / gonial angle |
| `LR:cheek-bones-incr` | 0.30 | malar |
| `nose-scale-vert/horiz/depth-incr` | 0.15 each | nose |
| `neck-scale-horiz-incr` | 0.10 | neck-to-jaw |

- **Candidates:** C1 k 1.0 (restrained), C2 k 2.0 (stronger), C3 k 3.3 (first caricatured), SKF190-C1 (configuration-2 replication).
- **Overlap cases:** per-region substitutions (§5).
- None of these values is canon.

### 4.2 Candidate readings vs matched Marchfolk (190 cm, %)

| Candidate | Eu_HH | HL_HH | LCB | **BGP** | BSO | **BGB_HH** | RAM | MDH | NJT | BZY | **MAL** | CHK | MPI | **NP** | NH | AB |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 restrained | +2.2 | +0.9 | +2.1 | +56 | +26 | +2.6 | +7.0 | −0.7 | +0.6 | +2.1 | +4.5 | +0.1 | −6.6 | +6.9 | +1.0 | +7.7 |
| C2 stronger | +4.3 | +1.8 | +4.2 | +115 | +53 | +10.6 | +3.4 | −0.7 | −5.5 | +4.2 | +9.0 | +0.2 | −9.9 | +13.6 | +6.2 | +10.1 |
| C3 caricatured | +7.2 | +2.9 | +7.0 | +193 | +99 | +15.5 | +3.5 | −0.7 | −8.1 | +7.0 | +15.1 | +0.4 | −8.0 | +23.4 | +13.2 | +24.0 |
| SKF190-C1 (config 2) | +2.1 | +0.9 | +2.1 | +129† | +18 | +7.4 | +1.0 | −0.6 | −2.4 | +2.1 | +3.5 | +0.2 | −5.3 | +7.1 | +4.6 | +9.4 |

All candidates also carry the accepted +1.6 % head height ÷ stature.

† Configuration 2 has a near-flat reference glabella (BGP 0.009), so the percentage is large. The absolute shift (+0.011 HL) matches configuration 1 (+0.012 HL).

**What the package does and does not express:**
- **Jaw:** "jaw drop" lowers the gonial angle (RAM) but does not deepen the mandibular body (MDH is unchanged). A deeper mandibular body would need a target the generator lacks.
- **Midface:** cheekbones widen the face (MAL) but do not add anterior depth (CHK is unchanged).
- **MPI:** falls because the brow moves N* forward. MPI cannot read midface projection when brow strength changes.

### 4.3 Complete-face read

Sheets `w3c_4_complete_face.jpg` and `w3c_2_tendency_closeups.jpg`. Checks: skull ↔ brow, brow ↔ orbit, midface ↔ nose, midface ↔ jaw, jaw ↔ neck, head ↔ body.

- **C1:** reads as the same human face with a slightly stronger brow, broader cheeks, a fuller nose and a firmer jaw angle. Neutral, with no scowl. Valid.
- **C2:** clearly robust. In profile the brow forms a pronounced ridge over a still-open orbit. The jaw is broad but not square, and the chin is unchanged. Valid, marginal at the brow.
- **C3:** caricatured. The brow becomes a shelf that overhangs the orbit in profile, and the head reads over-broad and heavy. That is the stereotype the order forbids. **First invalid.**
- **SKF190-C1:** the same reading on the configuration-2 face.

## 5. Individual overlap / anti-stereotype (§10)

Sheet: `w3c_3_overlap.jpg`. All cases are at 190 cm. Each Skarn case keeps the C1 package except the named region.

| Case | Change | Key reading | Matched-height comparison |
|---|---|---|---|
| Light-brow Skarn | brow `eyebrows-trans-backward` 0.30 | BGP 0.0137 | **below** accepted MF (0.0208) and strong-brow MF (0.0506) |
| Strong-brow Marchfolk | `eyebrows-trans-forward` 0.60 | BGP 0.0506 | above Skarn C1 (0.0324) and C2 (0.0447) |
| Lighter-jaw Skarn | `chin-bones-decr` 0.30 | BGB_HH 0.5018, RAM 0.2333 | below robust-jaw MF (0.5171 / 0.2424) |
| Robust-jaw Marchfolk | `chin-bones-incr` 0.60, jaw drop 0.30 | BGB_HH 0.5171 | above Skarn C1 (0.5055) |
| Lighter-midface Skarn | cheekbones −0.30, nose breadth / depth −0.15 | MAL 0.5703, NP 0.0488 | below substantial-midface MF (0.5887 / 0.0648); NP below accepted MF (0.0563) |
| Substantial-midface Marchfolk | cheekbones +0.60, nose +0.30 | MAL 0.5887, NP 0.0648 | above Skarn C1 (0.5870 / 0.0602) |

Fail conditions checked:
- **No candidate makes every Skarn square-jawed or heavy-browed:** C1 is mild, and light-brow / light-jaw Skarn remain valid.
- **Not every Marchfolk is gracile:** strong-brow, robust-jaw and substantial-midface Marchfolk are valid human faces.
- **No single metric identifies race:** every family overlaps, and accepted Skarn and Marchfolk are identical on face shape.
- **Clean-shaven Skarn read as valid:** no facial hair is modelled anywhere.
- **Facial composition stays separate from skull anatomy:** composition does not change the generator face.

## 6. Answers in the requested output form (§11)

| Family | Reference Skarn | Matched MF | Normalized difference | Observed overlap | Candidate central-tendency shift | Creator envelope | First invalid | Source |
|---|---|---|---|---|---|---|---|---|
| Skull size | HH_H 0.1285 (190); shape Eu_HH 0.649 | 0.1265; 0.649 | size +1.6 %; shape 0 % | complete on shape | size: as accepted. Robustness: +2 % breadth, +1 % depth (C1) to +4 % / +2 % (C2) | NOT DEMONSTRATED | C3 (+7 % breadth, with the package) | size **MEASURED FROM ACCEPTED ANATOMY**; robustness **BUILDER-CHOSEN** / **AUTHOR DECISION REQUIRED** |
| Brow | BGP 0.0207 | 0.0208 | −0.8 % (noise) | complete | BGP +0.012 HL (C1) to +0.024 HL (C2) | NOT DEMONSTRATED | C3 (+0.040 HL, brow shelf) | **BUILDER-CHOSEN** / **AUTHOR DECISION REQUIRED** |
| Jaw mass | BGB_HH 0.4936; NJT 1.415 | 0.4926; 1.391 | jaw +0.2 % (noise); neck-to-jaw +1.7 % | complete | bigonial +2.6 % (C1) to +10.6 % (C2); gonial angle lower; mandibular body depth not expressible | NOT DEMONSTRATED | C3 (+15.5 %, with the package) | neck-to-jaw **MEASURED FROM ACCEPTED ANATOMY**; jaw **BUILDER-CHOSEN** / **AUTHOR DECISION REQUIRED** |
| Midface | MAL 0.5616; NP 0.0565 | 0.5618; 0.0563 | ≤ 0.3 % | complete | malar +4.5 %, nose projection +7 % (C1) to +9 % / +14 % (C2); anterior depth unchanged | NOT DEMONSTRATED | C3 (+15 % / +23 %) | **BUILDER-CHOSEN** / **AUTHOR DECISION REQUIRED** |

No mean, standard deviation, percentile or frequency is stated or implied. Population frequency remains OPEN.

## 7. FAIL / MARGINAL / NOT DEMONSTRATED / NOT RUN

- **FAIL (deliberate bracket):** C3, k 3.3 (caricatured).
- **MARGINAL:**
  - the C2 profile brow;
  - BSO / BOR and alar-breadth metric repeatability (±10 % / ±15 % / ±5 %): secondary metrics only; BGP and NP carry the conclusions;
  - the 183 neck-to-jaw reading (band noise).
- **NOT DEMONSTRATED:**
  - any creator envelope (min / max) for Skarn brow, jaw, midface or skull robustness;
  - mandibular body depth, which the generator has no target to express;
  - anterior midface (maxillary) projection, where the cheekbone target only widens;
  - skeletal versus soft-tissue separation beyond the generator: all metrics are skin proxies and the ARMs have no skull model;
  - a cranial volume proxy;
  - body-to-face soft-tissue coupling (SKARN_V1 v1.2 §7): the generator face ignores composition.
- **NOT RUN:**
  - Skarn above 203 against matched Marchfolk (not allowed; the 208 row is endpoint-labelled);
  - candidate faces at 183 / 203 or on Narrow / Broad bodies: the package is a face-only target set, independent of stature and frame by construction, verified by configuration-2 replication only;
  - Gorrund separation check: not required by §9, and the candidates stay far from Gorrund facial architecture (human-family face).
- **Measurement limits:**
  - MPI is confounded when brow strength changes;
  - the Narrow + low-muscle frame moves the gonial-band metrics about 1–2 % equally in both populations;
  - the meshes are low-resolution (19,158 vertices), so close-up shading is coarse.

## 8. Cross-canon audit (§15)

| Reference | Result |
|---|---|
| SKARN_V1 v1.0 §8 / v1.2 §1–§7 | Kept: fully human faces; no mandatory square jaw, heavy brow or facial hair; tendencies, not requirements. **F-1:** the accepted Skarn ARMs do not yet embody the v1.2 facial tendencies, apart from head size and neck girth. Reported, not "fixed". The candidate package is returned for author decision. v1.4 §6 equal-height test at 190 cm: on accepted anatomy the Skarn face is distinguished only by head size and neck. ~~The body carries the Skarn read, so the face does not need to.~~ **Corrected (author ruling, W3D order §1, October 10, 2026):** the body may independently preserve Skarn identity, but the Skarn central / reference face must still embody the authored Skarn facial tendencies (now the C1R reference face); they remain soft population tendencies, not membership tests. |
| MARCHFOLK_V1 (human reference; breadth / diversity wording) | Kept. Strong-brow, robust-jaw and substantial-midface Marchfolk are valid. The FPI 0.191 diagnostic (MF-FACE-PROJ-MAX) is not a ceiling and was not used as one. |
| UFCA_V1 (§10.1 Skarn robust tendencies are SOFT, never mandatory; slots 3–6) | Kept. All controls used map to shared human-family slots (head, brow / orbit, nose, cheeks, jaw / chin). There is no Skarn-only control. |
| REFERENCE_ANATOMY_V1 (§5 diagnostic faces, §7 builder-chosen values, §10) | All builder-chosen values are declared (§4.1, `cfg/w3c/SK-face.json`). Matched-height comparisons sit inside the 183–203 overlap. The 208 row is endpoint-labelled (§10 unavailable-endpoint rule). No Iteration-3 or Rodin asset was used. |
| Accepted Skarn W1 / W2 anatomy | Unchanged (hashes; files predate W3C). New bodies are copies built through the accepted routes and frames. |
| Accepted Marchfolk W1 / W2 anatomy | Unchanged. MFM183, MFM190-NLOW and MFM190-B were built through the accepted MF route, frame sets and composition. |
| RM-CF-02 / FPI Marchfolk evidence | Consistent. MF190 FPI 0.1442 equals SK190 0.1443; MF-M-R 0.143 (W1c). |

**Contradictions with accepted canon:** none. F-1 is an asset-coverage gap, surfaced.

## 9. Persistent files changed

**W3B writeback (commit af84f63):**
- `specs/saurin/SAURIN_V1.md` (§267, plus §259 / §262 / §265 pointers);
- `decisions/REFERENCE_ANATOMY_V1.md` (§9 row, §10 rule);
- `specs/STATUS.md`, `reviews/claude-pass2-r5-reference-mesh-queue.md`.

**W3C:**
- `reviews/claude-rac-w3c-skarn-craniofacial-gate.md` (this gate);
- `reviews/rac-w3c-sk-evidence/`;
- `tools/rac/w1/w3c_drivers/` (new);
- `tools/rac/w1/cfg/w3c/SK-face.json`;
- `specs/skarn/SKARN_V1.md` (status pointer only);
- `specs/STATUS.md`, `reviews/claude-pass2-r5-reference-mesh-queue.md` (status lines and the RM-CF-09 row).

**Not changed:** SKARN_V1 numeric ranges, MARCHFOLK_V1, UFCA / UCCA, all accepted meshes.

## 10. Stop

W3C stops here for author review. Not begun: the RM-CF-05 margin decision, RM-UF-05, RM-OT-05, posture, equipment, UE5, rigging, animation and gameplay.

---

## Appendix A — RM-CF-05 INPUT ONLY

FPI / MPI / MdPI on every W3C face (`tables.md` §5). This appendix makes no margin choice.

| Body | FPI | MPI | MdPI | Class |
|---|---|---|---|---|
| SKM183 / MFM183 | 0.1441 / 0.1439 | 0.0499 / 0.0506 | −0.0035 / −0.0035 | accepted |
| SKM190 / MFM190 | 0.1443 / 0.1442 | 0.0502 / 0.0508 | −0.0036 / −0.0035 | accepted |
| SKM203 / MFM203 | 0.1447 / 0.1446 | 0.0495 / 0.0501 | −0.0037 / −0.0037 | accepted |
| SK208 | 0.1449 | 0.0496 | −0.0037 | accepted |
| SKF190 / MFF190 | 0.1681 / 0.1683 | 0.0495 / 0.0501 | −0.0325 / −0.0327 | accepted |
| SKF203 / MFF203 | 0.1675 / 0.1676 | 0.0495 / 0.0499 | −0.0321 / −0.0323 | accepted |
| SKM190-C1 / C2 / C3 | 0.1462 / 0.1479 / 0.1495 | 0.0474 / 0.0457 / 0.0467 | −0.0062 / −0.0078 / −0.0096 | builder-chosen |
| SKF190-C1 | 0.1699 | 0.0475 | −0.0341 | builder-chosen |
| MF overlap brow / jaw / midface | 0.1442 / 0.1442 / 0.1467 | 0.0508 / 0.0508 / 0.0469 | −0.0035 / −0.0035 / −0.0080 | builder-chosen |

FPI is invariant to stature and frame within each configuration (±0.0006). The Skarn tendency candidates raise FPI by at most +0.005 (C3).
