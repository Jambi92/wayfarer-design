# RAC W3D — C1R central Skarn face and RM-CF-05 FPI-margin author gate

**Order:** `reviews/chatgpt-rac-w3c-final-acceptance-w3d-fpi-margin-order.md`
**Evidence:** `reviews/rac-w3d-evidence/` — `c1r.json`, `saurin_fpi.json`, `human_fpi.json`, `geometry/` (C1R central reference assets), `overrides/`, `builds/`, and 3 sheets.
**Drivers:**
- `tools/rac/w1/w3c_drivers/w3d_c1r.py`, `w3d_c1r_sheets.py`, `w3d_fpi_pitch.py`;
- `tools/rac/w1/w3b_drivers/w3d_saurin_fpi.py`, `w3d_fpi_sheet.py`.

**Pointer / recipe:** `tools/rac/w1/cfg/w3d/SK-C1R.json`.
**Scope:** Skarn reference-face correction and writeback, plus the RM-CF-05 evidence package. **The margin is not chosen here.** No UE5.

---

## 0. Verdicts

| Item | Verdict |
|---|---|
| **W3C** | **FINAL ACCEPT.** The W3C gate wording "the body carries the Skarn read, so the face does not need to" is struck through and corrected to the author ruling (W3C gate §8). |
| **C1R central Skarn face** | **ACCEPT.** Fully human, neutral, clean-shaven-valid. It expresses the selected C1 direction plus a more substantial neck. Validated on all 7 required bodies. Body vertices outside the head / neck are unchanged (0.0000 cm; stature Δ ≤ 0.001 cm; body ratios Δ 0). |
| **Neck-to-jaw correction** | **CONSTRAIN.** One change: `neck-scale-horiz-incr` 0.10 → 0.30, the smallest step tested that restores the relationship.<br>• **Configuration 1** (208 / 190 / 203 / Broad): the neck-to-jaw ratio (NJT) is **+1.7 to +2.0 %** over matched Marchfolk. C1 alone gave +0.6 %.<br>• **Configuration 2 and Narrow + low muscle:** the ratio is at Marchfolk parity (+0.2 % / −0.2 %), inside NJT repeatability (±2 %). The C1 jaw widening responds more strongly on those faces (bigonial +8.1 % / +6.8 %). Absolute neck breadth ÷ head height is still **+8.3 % / +6.6 %** over Marchfolk.<br>• Forcing the ratio to +1.5 % there would need neck 0.50, which over-widens the configuration-1 neck (sheet 2). That option was not used. |
| **Configuration-2 replication** | **PASS.** The complete-face read is the same strength class as configuration 1.<br>• Absolute brow shift +0.011 HL (configuration 1: +0.012 HL). The +129 % brow figure is inflation from a near-flat baseline glabella.<br>• No Skarn sex stereotype and no separate range. |
| **RM-CF-09** | **FINAL CLOSED** (SKARN_V1 reference-anatomy status, REFERENCE_ANATOMY §7 / §9, RMQ, STATUS). The W3C evidence, F-1 and the six overlap cases are retained. |
| **Mandibular-body depth** | **OPEN** — reference-generator capability gap. |
| **Anterior maxillary depth** | **OPEN** — reference-generator capability gap. |
| **Body-to-face soft-tissue coupling** | **OPEN** — reference-generator capability gap. |
| **RM-CF-05 evidence package** | **CONSTRAINED.**<br>• Every term is measured, including a new direct W2 Saurin remeasure and pitch at the Saurin minimum corner.<br>• Only Marchfolk has an accepted maximum-valid projection face. GR-FACE-14 and GOR-FACE-05 were never built, so Grask and Gorrund maxima are **NOT DEMONSTRATED**.<br>• The demonstrated Marchfolk maximum exists only on configuration 1. |
| **Tightest demonstrated FPI gap** | **0.101** (Saurin minimum corner 0.2920 − MF-FACE-PROJ-MAX 0.1905). |
| **Tightest fully-authoritative FPI gap** | **0.101** (same pair). Conservative, after the uncertainty allowance: **~0.08**. |
| **Option A margin** | **0.02** r3 FPI |
| **Option B margin** | **0.05** r3 FPI |
| **Option C margin** | **0.10** r3 FPI |
| **Claude recommendation** | **B — advisory only** (§7). |
| **Author decision required** | **YES** |

---

## 1. C1R reference face

### 1.1 Reference-construction values

These are not creator limits, not population statistics and not membership tests. They are merged into each accepted Skarn body build with the height macro held.

| Target | Value | Region |
|---|---|---|
| `head-scale-horiz-incr` | 0.12 | cranial breadth |
| `head-scale-depth-incr` | 0.08 | cranial depth |
| `eyebrows-trans-forward` | 0.30 | brow / supraorbital geometry (not hair) |
| `chin-bones-incr` | 0.30 | jaw breadth |
| `chin-jaw-drop-incr` | 0.15 | gonial angle |
| `LR:cheek-bones-incr` | 0.30 | malar breadth |
| `nose-scale-vert-incr` / `-horiz-incr` / `-depth-incr` | 0.15 each | nose |
| **`neck-scale-horiz-incr`** | **0.30** (C1: 0.10) | **neck-to-jaw — the only change from C1** |

**Neck sweep (190 cm, configuration 1; NJT difference against matched Marchfolk):** C1 0.10 → +0.6 %; 0.20 → +1.3 %; **0.30 → +1.9 %**; 0.40 → +2.6 %; 0.50 → +3.2 %.

Using `measure-neck-circ-incr` instead was weaker per unit (0.55 → +2.0 %). Both routes widen the gonial band slightly, so bigonial breadth rises +1.1 % against C1. That is a leak of the neck morph into the jaw-angle region; the jaw targets themselves are unchanged.

### 1.2 Results on the validation set (C1R − matched Marchfolk, %)

| Body | Stature Δ | Body vertices moved | Head height ÷ stature | Cranial breadth | Brow (BGP) | Bigonial | NJT | Malar | Nasal projection | FPI |
|---|---|---|---|---|---|---|---|---|---|---|
| **SK208-C1R** (central; vs MF203 **endpoint**) | +0.001 | 0.0000 | +0.9 | +2.0 | +53 | +3.5 | +1.7 | +4.2 | +6.5 | 0.1467 |
| SKM190-C1R (configuration 1) | +0.001 | 0.0000 | +1.6 | +2.2 | +56 | +3.8 | **+1.9** | +4.5 | +6.9 | 0.1462 |
| SKF190-C1R (configuration 2) | +0.001 | 0.0000 | +1.6 | +2.1 | +129† | +8.1 | +0.2 | +3.5 | +7.1 | 0.1699 |
| SKM183-C1R | +0.001 | 0.0000 | +1.7 | +2.2 | +56 | +3.9 | +7.1* | +4.6 | +7.0 | 0.1460 |
| SKM203-C1R | +0.001 | 0.0000 | +1.6 | +2.1 | +54 | +3.6 | **+1.9** | +4.3 | +6.4 | 0.1465 |
| SKM190 Narrow + low muscle | +0.001 | 0.0000 | +1.7 | +2.2 | +55 | +6.8 | −0.2 | +4.5 | +6.9 | 0.1462 |
| SKM190 Broad, reference composition | +0.001 | 0.0000 | +1.6 | +2.2 | +55 | +3.8 | **+2.0** | +4.5 | +6.9 | 0.1462 |

† Near-flat baseline glabella on configuration 2; the absolute shift equals configuration 1.
\* Band-sampling noise at 183, as in W3C.
SKF208-C1R (configuration-2 central) also has its body unchanged (0.000 cm).

**Visual read** (sheets `w3d_1_c1r_validation.jpg` and `w3d_2_neck_correction.jpg`):
- every C1R face is human, neutral (no scowl) and clean-shaven-valid;
- the brow is stronger with no shelf, and the jaw angle is firmer without a squared chin;
- the malar region is broader and the nose fuller;
- the neck is more substantial but not cylindrical, not bodybuilder-like and not Gorrund-like;
- it is not a "Viking face": no hair, beard or presentation carries the read.

### 1.3 Old and new reference assets

| Role | Old (provenance, retained) | New canonical pointer |
|---|---|---|
| SK central, configuration 1, 208 cm | `reviews/rac-w1c-evidence/geometry/SK_r6.npz`; scratch `w1f/final/SK_r6.npz` (identical geometry) | `reviews/rac-w3d-evidence/geometry/SK208-C1R_r6.npz` (+ `_rest`) |
| SK configuration 2, 208 cm | scratch `w2b/st/SKF208_r6.npz` | `reviews/rac-w3d-evidence/geometry/SKF208-C1R_r6.npz` (+ `_rest`) |

SHA-256 values for both columns are in `tools/rac/w1/cfg/w3d/SK-C1R.json`. The validation-variant hashes (old and new) are in `c1r.json`.

**Variant rule:** apply the C1R face layer to any accepted Skarn body build. Historical W1 / W2 files are not overwritten.

### 1.4 Overlap validators

The six W3C cases (light-brow Skarn, lighter-jaw Skarn, lighter-midface Skarn, strong-brow Marchfolk, robust-jaw Marchfolk, substantial-midface Marchfolk) remain **PASS** as permanent anti-stereotype evidence (`reviews/rac-w3c-sk-evidence/`).

C1R changes only the neck width. It moves no overlap-relevant brow, jaw-target or midface value. Bigonial breadth rises +1.1 % from the neck leak, which still sits below the robust-jaw Marchfolk case (0.5112 against 0.5171).

---

## 2. FPI convention and the Saurin datum

- **Convention:** r3 FPI = (FAL.f − eye-centre.f) ÷ HL, where HL = FAL.f − Op.f.
- **Saurin datum (W2 remeasure).** The Saurin r3 FPI was measured directly on the **canonical W2 reference** for the first time. The W1 figures used aff1b52. It uses the same `fpi()` definition as `saurin_w1.py`, rebuilt on the W2 base (`w3d_saurin_fpi.py`):

| Saurin case | Part 7 index | r3 FPI | Pitch −3° / +3° | HL (cm) | FAL top-20 spread |
|---|---|---|---|---|---|
| W2 reference | 0.28793 | **0.32539** | 0.31794 / 0.33286 | 31.871 | 0.024 cm |
| Rostrum −15 % | 0.25950 | 0.29846 | 0.29058 / 0.30641 | 30.648 | 0.021 cm |
| **Coupled minimum corner** (rostral length 0.8847 at cranial length 1.08) | **0.25499** | **0.29196** | **0.28444 / 0.29954** | 32.301 | 0.022 cm |

- W2 reproduces W1 exactly (W1: 0.32539 and 0.29196). The W2 head geometry is the aff1b52 head (W2 Part 7 identical), and W3B moved no FPI landmark.
- **0.2920 therefore remains the Saurin minimum-projection comparison point.**
- The 1.194 cm conversion holds on W2: Part 7 recomputed from r3 gives 0.25499. It applies only to this eye / cranial geometry and is not universalized.
- **New:** pitch sensitivity at the corner itself is ±0.0075.

## 3. Comparator set (highest valid r3 FPI per population, `human_fpi.json`)

| Population | Case | r3 FPI | Pitch −3° / +3° | Evidence class | Used for the margin? |
|---|---|---|---|---|---|
| **Marchfolk** | **MF-FACE-PROJ-MAX** | **0.1905** | 0.1803 / 0.1991 | **accepted maximum-valid diagnostic** (W1c; configuration 1; "not a complete envelope") | **yes — controls** |
| Marchfolk | MF-F-R / W2 configuration-2 maximum (MFF147-NAT) | 0.1693 / 0.1701 | 0.1596 / 0.1782 | accepted central / variant | central context |
| Marchfolk | MF-M-R | 0.1435 | 0.1318 / 0.1537 | accepted central | context |
| Marchfolk | MFF-PROJ-SENS: configuration 2 + the accepted 1.2 cm projection displacement | 0.2157 | 0.2080 / 0.2230 | **builder-chosen sensitivity, validity NOT DEMONSTRATED** | **no** (sensitivity only) |
| Skarn | SKF190-C1R (configuration-2 central) | 0.1699 | 0.1602 / 0.1791 | accepted central reference (C1R) | yes, as central, not maximum |
| Skarn | SKM190-C2 | 0.1479 | 0.1358 / 0.1580 | valid stronger diagnostic | yes, not a maximum |
| Skarn | SK208-C1R / SKM190-C1R | 0.1467 / 0.1462 | 0.1350 / 0.1568 | accepted central reference | context |
| Skarn | SKM190-C3 | 0.1495 | — | **rejected** | **never** |
| **Grask** | GR-FACE-14 | — | — | **NOT DEMONSTRATED (never built)** | no global claim |
| Grask | GR239 (W2 body maximum; generator face) / central GR | 0.1453 / 0.1437 | 0.1328 / 0.1562 | accepted body variant / central, **not a face maximum** | provisional only |
| **Gorrund** | GOR-FACE-05 | — | — | **NOT DEMONSTRATED (never built)** | no global claim |
| Gorrund | GO251 (W2 body maximum; generator face) / central GO | 0.1485 / 0.1481 | 0.1368 / 0.1586 | accepted body variant / central, **not a face maximum** | provisional only |

**Other populations.** The original audit set was Marchfolk, Grask and Gorrund only (r3 §7; SAURIN_V1 L758). Sagekin, the elves, Halvren, Durrim, Pipkin and Cogling have central readings of 0.138–0.146 and W2 maxima of ≤ 0.146 on generator faces. **Their maximum-valid faces are NOT DEMONSTRATED.**

## 4. Gaps (Gap = 0.29196 − X)

**Uncertainty allowance** = worst-case opposing pitch (Saurin −3° plus comparator +3°) plus landmark repeatability on both terms. Landmark repeatability: Saurin FAL ±0.03 cm ÷ HL = ±0.0009; human profile-section FAL ±0.05 cm ÷ HL = ±0.0022–0.0024.

| Comparator X | Raw gap | Allowance | Conservative gap | Basis |
|---|---|---|---|---|
| **MF-FACE-PROJ-MAX** | **0.1015** | 0.0075 + 0.0086 + 0.0023 + 0.0009 = **0.0193** | **0.0822** | **actual accepted maximum-valid — tightest demonstrated and fully authoritative** |
| SKF190-C1R | 0.1221 | 0.0199 | 0.1022 | central, not a maximum |
| MF configuration-2 central (0.1701) | 0.1219 | 0.0198 | 0.1021 | central |
| SKM190-C2 | 0.1441 | 0.0206 | 0.1235 | valid stronger, not a maximum |
| GO251 (provisional) | 0.1435 | 0.0186 | 0.1249 | body variant, not a face maximum |
| GR239 (provisional) | 0.1467 | 0.0186 | 0.1281 | body variant, not a face maximum |
| *MFF-PROJ-SENS (sensitivity)* | *0.0763* | *0.0181* | *0.0582* | *builder-chosen; validity NOT DEMONSTRATED* |

- **No comparator's uncertainty band approaches or crosses the Saurin minimum.**
- The closest number in the package is the *undemonstrated* configuration-2 projection sensitivity: 0.0763 raw, 0.058 conservative. Applying the same accepted 1.2 cm displacement to the configuration-2 face would set a higher Marchfolk maximum (+0.025 over MF-FACE-PROJ-MAX) **if** that face were accepted as valid.

## 5. Uncertainty firewall

- **Pitch:** ±3° about the eye midpoint moves r3 FPI by ±0.0075 on Saurin (reference and corner) and −0.010 / +0.009 on human faces. This is the largest term. Both conventions pitch about the eye midpoint.
- **Landmark repeatability:**
  - Saurin FAL ±0.001 FPI (top-20 spread ≤ 0.024 cm);
  - human FAL ±0.002 FPI: the profile section is sampled every 0.05 cm on a low-resolution mesh of 19,158 vertices;
  - human FPI is stable across stature and frame within ±0.0006 per configuration.
- **Convention differences between architectures (structural, not noise):**
  - **FAL:** Saurin FAL is the anterior-most midline head point (the rostral tip). Human FAL is the more anterior of subnasale and A′ (the nose is excluded).
  - **Eye centre:** Saurin OC is the tracked eyeball centre; human OC is the 2.40 cm eye-helper globe centre.
  - **Op:** Saurin Op is above u 176; human Op is above OC − 2 cm.
  - All of these are the accepted r3 / D-1 conventions. The FPI gap is therefore an index separation under accepted conventions, not a like-for-like bone measurement.
- **Geometry and cameras:** the W1 → W2 Saurin geometry difference is zero for FPI (§2). Every face uses the accepted neutral R-6 / reference pose with no expression.
- **Precision:** the combined allowance is ~0.02. Margins are meaningful to **hundredths at most**. A thousandth-level margin would be false precision.

## 6. Author options (not chosen)

| | **A — minimum defensible** | **B — robust** | **C — conservative / visually stronger** |
|---|---|---|---|
| **Margin (r3 FPI)** | **0.02** | **0.05** | **0.10** |
| **Controlling evidence** | the measurement allowance (pitch + landmarks ≈ 0.019–0.021) | allowance plus headroom for comparator maxima not yet demonstrated (the configuration-2 projection sensitivity, GR-FACE-14, GOR-FACE-05) | the tightest demonstrated gap itself (0.1015) |
| **What becomes constrained** | future non-Saurin maximum-valid faces must stay ≤ 0.272 r3, and the Saurin floor ≥ comparator maximum + 0.02 | future non-Saurin maximum-valid faces must stay ≤ **0.242** r3 (0.2920 − 0.05); the 0.2157 sensitivity case would pass with 0.026 to spare | non-Saurin maximum-valid faces must stay ≤ 0.192 r3 |
| **Saurin Part 7 floor 0.255 unchanged?** | **yes** | **yes** | **only nominally.** MF-FACE-PROJ-MAX passes by 0.0015, below the uncertainty. With the allowance, or if the configuration-2 projection face is later accepted, the floor would have to rise to Part 7 ≈ **0.27–0.28**. That removes the rostrum −15 % region and the coupled minimum corner. |
| **Accepted comparator invalidated?** | none | none | none today, but MF-FACE-PROJ-MAX sits inside the noise band. A configuration-2 Marchfolk projection maximum could not be accepted without raising the Saurin floor. |
| **Visual / biological trade-off** | Index-level separation only. Weak as an identity guard if a future comparator maximum rises (e.g. a large GR-FACE-14). | Keeps the full accepted Saurin rostral range. Leaves human-family maximum projection room above today's demonstrated maximum. The visual gap (sheet 3) is unmistakable. | Visually larger guaranteed gap, but the Saurin rostral envelope narrows and human-family projection is capped near today's single demonstrated maximum. That spends Saurin biology to buy separation that is already visually obvious. |

## 7. Claude recommendation (advisory only)

**Option B, 0.05.**
- It is about 2.5 times the measured uncertainty.
- It keeps the accepted Saurin 0.255 floor and coupled minimum corner unchanged.
- It invalidates nothing.
- It still holds if a configuration-2 Marchfolk projection maximum (sensitivity 0.2157) or a moderately projecting GR-FACE-14 / GOR-FACE-05 is later accepted.

Option C would buy little visual separation beyond what sheet 3 already shows, at the cost of Saurin rostral range. Option A leaves no allowance for maxima that are not yet demonstrated. **Not canonized; the author decides.**

## 8. Visual evidence

`w3d_3_fpi_comparison.jpg`: matched 44 cm orthographic camera, profile / three-quarter / front.
- **Rows:** Saurin W2 reference; Saurin minimum-valid corner; MF-FACE-PROJ-MAX; Grask GR239; Gorrund GO251; Skarn SK208-C1R; Skarn SKM190-C2.
- **Labelling:** the Grask and Gorrund rows are generator-face body variants, labelled as such, because their face diagnostics were never built.
- **Read:** even the minimum Saurin corner keeps a fully projecting rostrum, while every non-Saurin face stays flat-faced human-family. The ~0.10 gap is a real architecture separation, not a numerical artifact.

## 9. Required reports

1. **Old / new Skarn assets and pointers:** §1.3 and `cfg/w3d/SK-C1R.json`.
2. **C1R reference-construction values:** §1.1.
3. **C1R results at 208 / 190 / 183 / 203, Narrow and Broad:** §1.2.
4. **Overlap validators:** §1.4 — PASS.
5. **Comparator FPIs and evidence classes:** §3.
6. **Uncertainty terms:** §5.
7. **NOT DEMONSTRATED:**
   - GR-FACE-14 and GOR-FACE-05 maxima;
   - maximum-valid faces of every other population;
   - a configuration-2 Marchfolk projection maximum (sensitivity only);
   - mandibular-body depth, anterior maxillary depth and body-to-face coupling (OPEN generator gaps);
   - a Skarn creator facial envelope and population frequency.
8. **Persistent files changed:** §10.
9. **Creator facial min / max canonized:** **NO.**
10. **Accepted non-Skarn anatomy modified:** **NO.** Marchfolk, Grask, Gorrund and Saurin assets are only read. The Saurin warps are diagnostic copies, and the canonical W2 files are untouched.

## 10. Persistent files changed

- `reviews/claude-rac-w3d-fpi-margin-author-gate.md` (this gate)
- `reviews/rac-w3d-evidence/` (new)
- `reviews/claude-rac-w3c-skarn-craniofacial-gate.md` — §8 wording corrected per the author ruling
- `specs/skarn/SKARN_V1.md` — reference-anatomy status note (C1R; RM-CF-09 FINAL CLOSED). The v1.2 facial principle is preserved, and no numbers were added to the biological prose.
- `decisions/REFERENCE_ANATOMY_V1.md` — §7 C1R candidate row; §9 W3 row
- `specs/STATUS.md`, `reviews/claude-pass2-r5-reference-mesh-queue.md` — status lines; RM-CF-09 row closed
- `tools/rac/w1/cfg/w3d/SK-C1R.json` — pointer / recipe
- New drivers: `tools/rac/w1/w3c_drivers/w3d_*.py` and `tools/rac/w1/w3b_drivers/w3d_*.py`
- **Not changed:** the SAURIN_V1 Part 7 floor, the Saurin W2 asset, all Marchfolk / Grask / Gorrund assets, and the historical Skarn W1 / W2 files.

## 11. Stop

W3D stops here for the author's RM-CF-05 decision. Not begun: RM-CF-05 canon writeback, RM-UF-05, RM-OT-05, later biology, posture, equipment, UE5, rigging, animation and gameplay.

---

## Closure status (added October 10, 2026)

Author ruling `reviews/chatgpt-rac-w3d-final-ruling-rm-uf-05-order.md`: W3D accepted; C1R FINAL ACCEPT with neck width 0.30; configuration-2 replication PASS; RM-CF-09 FINAL CLOSED; **RM-CF-05 = option B, 0.05 r3 FPI, FINAL CLOSED** (SAURIN_V1 §268; floor 0.255 unchanged; operational comparison limit 0.24196 conditional; collision = author review). **Neck-to-jaw interpretation (author clarification, October 10, 2026; `reviews/chatgpt-rac-w3d-final-ruling-rm-uf-05-order.md` §2):** the C1R neck width 0.30 is final for the reference construction. The more substantial neck-to-jaw transition is a central / reference population tendency, not an invariant clamp: configuration-1 C1R (+1.7 to +2.0 % NJT over matched Marchfolk) is valid evidence of it, and configuration-2 / Narrow-low-muscle parity is not a failure while the absolute Skarn neck stays substantial and the complete read is canon-valid. No neck widening to force a percentage, no creator minimum from NJT, no neck-breadth membership test, no jaw change to recover a ratio. RAC W3 FINAL CLOSED.
