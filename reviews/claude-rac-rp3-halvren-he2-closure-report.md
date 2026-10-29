# RAC RP3 — Halvren HE2 realization / ear architecture closure report

**Order:** `reviews/chatgpt-rac-rp3-halvren-he2-realization-ear-architecture-closure-order.md` (40b46e6; reviewed commit 35cde9f).
**Evidence:** `reviews/rac-rp3-evidence/halvren_rp3_he2_closure/`

| File | Contents |
|---|---|
| `HE2_closure_record.json` | consolidated record |
| `HE2_authored_vs_realized.md` / `.json` | authored vs realized domains |
| `calibration/` | control Jacobian and every trial |
| `records/` | per-realization build / audit / measure / deformation / guard / repair |
| `topology_audit/` | topology audit records |
| `HE_production_checks.json` | production checks |
| `HV_ear_definitions_HVEAR3.json` | ear definitions |
| `immutable_hashes.txt` | frozen-reference hashes |
| `boards/` | boards `HE2C_A..F` |

**Tools** (`tools/rac/rp/halvren_rp3_v001/`):
- `hv_ear_try.py` — one rest-state calibration build;
- `hv_ear_jac.py` — control Jacobian;
- `hv_he2_drift.py` — authored-vs-realized table;
- `hv_cuff_repair.py` — HR1 cuff sliver repair;
- `hv_run_head.sh` — Halvren guarded path;
- `hv_he2_closure.py` — closure record;
- `hv_ear_prodcheck.py` — mirroring / export / LOD;
- `hv_he2_boards.py` — boards.

**Shared-library changes** (`fenn_rp3_v001`), both inert unless set:
- `ear_branch_lib.realize` placement bias `place_db` / `place_du`;
- `ear_build.py` probe keys `taper_st` and the geometry controls.

Frozen Fenn E2 and Aelari AE-E2 were rebuilt on the Halvren head with the final library: dV 0, faces identical.

## FINAL RECOMMENDATION

## HE2 FREEZE APPROVED

All twelve §10 gates are met for HE2. Two family carry-forwards are recorded explicitly, outside the HE2 freeze:
- **HE3** sits close to the Marchfolk → Aelari line (R² 0.87) and has one posed contact on c2.
- **HE1** has a bounded size floor.

Nothing is frozen by this report. The freeze itself waits for ChatGPT / author review.

## 1. Root-cause diagnosis (§2, §4)

The authored HE2 was not the problem; the realization system was. Two mechanisms flattened HVEAR2 HE2 onto a Marchfolk → elf line.

**1. Calibration: authored "human-family" values do not land on the Marchfolk auricle.** The HVEAR2 human-family domains used W1 MF-human parameters. Realized on the shared engineering sheet, those parameters measure half-way to the elves:

| Parameter | Realizes (measured) | Marchfolk auricle |
|---|---|---|
| proj 22 | 23–25° | 6.5° |
| tilt 12 | ~14° backward | 4.8° |
| L 6.4 | 0.28–0.30 HH | 0.24 HH |

So a "human" projection, tilt or length authored that way always lands at t ≈ 0.5. On top of that, the junction-centred placement puts every branch auricle top about 1.9 cm above the root-loop top (Marchfolk 0.3 cm). Upward extension is therefore elf-like for any parameter set (t ≈ 1).

**2. Coupled controls.** Finite-difference Jacobian of the measured domains, 16 controls (`calibration/HE2_control_jacobian.json`). Each order-listed link was checked:

| Suspected link | Measured coupling (source-SD units per probe step) | Linked? |
|---|---|---|
| point extension → total length | L +0.6 cm → length +0.43, upward extension +0.41, **free lobe +0.69**, concha / L −0.33 | **yes** (length drags lobe and upward extension) |
| taper → width loss | early continuous taper (start 0.36) leaves an elf apex (tip 58°) and a narrow upper ear; the exponent alone barely moves the tip (−0.12 per +0.25); start / shoulder move fullness (+0.52 / +0.29) | **yes** (via taper *start*, not exponent) |
| root rotation → projection | φ0 −8° → projection −0.07; τA −8° → +0.03 | **no** (root rotation drives width +0.42 and root line −0.68) |
| upper-helix shaping → overall elongation | lift_top / shoulder → length 0.00 | **no** |
| concha depth → projection | concha +0.25 → projection +0.07, but **width +0.45, root line −1.70, and the anterior junction rises** (root mound 0.12 → 0.33 cm) | **concha → mound / width, not projection** |
| lobe reduction → taper | lobe parameter → realized free lobe 0.00 (inert) | **lobe control is dead**; the free lobe follows length (+0.69) and placement height (+1.15) |
| upper attachment → elf deformation path | placement height place_du: lobe +1.15, root line +2.53, width +0.55, upward extension −0.46 | **yes** (placement height is a strong hidden control) |

**Why the realized fit was high, and which domains drove it.**
- **Before (HVEAR2):** the realized HE2 sat at t 0.55–1.3 on length, width, projection, upward extension, backward angle, tip, concha and helix fullness.
- **Drivers of the one-α fit:**
  - **MF→AE:** upward extension, concha depth, tip, length.
  - **MF→VA:** tip, root line, backward angle.
- **Collinearity.** These are the domains where the realized HE2 moved collinearly with Aelari and Vael. Calibration (1) pulled the human-family domains to t ≈ 0.5, and the coupled controls (2) pulled length, lobe and concha with them.

## 2. Authored vs realized domain table (§4; `HE2_authored_vs_realized.md`)

How to read the table:
- **Authored target:** the authored HVEAR2 parameter position (t on the Marchfolk → elf-mean parameter line), transported onto the measured Marchfolk / elf values of that domain.
- **Realized:** HVEAR2 guarded HE2 on c1.
- **Pull:** the source the drift moved toward, or "interpolation line" when the realized t sits on the realized one-α MF→AE fit (α 0.78).

| Domain | Authored t | Authored target | Realized HVEAR2 (t) | Drift (SD) | Pull | Suspected cause | Corrected HVEAR3 (t) |
|---|---|---|---|---|---|---|---|
| width / length | (wb, L) | 0.356 | 0.407 (1.11) | +0.79 | Marchfolk | early taper start narrows the upper ear; coupled to concha, φ0, placement | 0.435 (0.88) |
| length / HH | 0.58 | 0.315 | 0.358 (0.90) | +0.70 | **interpolation line** | W1 L calibration; L also drives lobe / upward extension | 0.328 (0.68) |
| upward extension / HH | 0.69 | 0.063 | 0.103 (1.27) | +1.12 | Aelari | junction-centred placement + length + tilt | 0.092 (1.11) |
| tragus / cavum level | −0.19 | 0.418 | 0.273 (1.70) | −3.13 | Fenn | cavum stays at the base as the upper ear lengthens | 0.264 (1.82) |
| tip angle | 0.92 | 62.4° | 58.4° (0.98) | −0.14 | on target (elf apex) | early continuous taper | **82.6° (0.62)** |
| root line | 0.00 | −1.5° | −20.4° (6.53) | −2.29 | Vael | junction placement / concha depth | −22.6° (7.3) — unchanged |
| projection | 0.07 | 8.8° | 25.4° (0.55) | +0.99 | **interpolation line** | W1 projection calibration (not root rotation) | **17.7° (0.33)** |
| lobe fraction | −0.67 | 0.000 | 0.075 (0.40) | +2.30 | Aelari | lobe parameter inert; length / placement drive it | **0.043 (−0.05)** |
| helix fullness | 0.81 | 0.628 | 0.642 (0.65) | +0.37 | **interpolation line** | early taper start removes the upper helix body | **0.753 (−0.66)** |
| concha depth / L | −0.08 | 0.273 | 0.195 (1.19) | −2.14 | **interpolation line** | concha diluted by length and the −0.50 seat | 0.220 (0.79) |
| backward angle | 0.49 | 14.4° | 19.1° (0.72) | +0.53 | **interpolation line** | W1 tilt calibration + sweep | **14.6° (0.50)** |

The one domain the correction did not move is the root line. It stays Vael-like and is the main remaining Vael-pair driver.

## 3. Exact topology / control changes (the Halvren ear realization path)

The connectivity is unchanged: the Fenn v002 sheet + RI3 six-ring cuff, read-only, with the 52-vertex v005 root.
- One face topology for HE1 / HE2 / HE3 on c1 and c2 (sha `f8367ab09385…`).
- No mesh proliferation.

Path = authored domain targets → calibrated controls → HR1 realization:

1. **HVEAR3 calibrated HE2** (`ear_branch_lib.CAND['HE2']`). The parameters were solved against **measured** targets (Jacobian + trials, `calibration/`), not W1 values:

   | Parameter | HVEAR2 | HVEAR3 |
   |---|---|---|
   | L | 7.8 | 7.0 |
   | wb | 2.00 | 2.00 |
   | taper (start / exponent / shoulder) | 0.36 / 1.10 / 0.06 | 0.50 / 0.90 / 0.12 |
   | proj | 23 | 16 |
   | tilt | 16 | 12 |
   | sweep | 1.4 | 1.0 |
   | concha | 0.86 | 1.00 |
   | concha seat | −0.50 | −0.58 |

   Intent: a broad, full, deep-concha human-family auricle body with an elevated, moderately elongated upper extension ending in a controlled shouldered point.
2. **HR1 seat rule.** Concha seat = −0.50 − 0.8 × (concha − 0.90) cm. A deeper concha seats deeper, so concha depth no longer raises the anterior junction (the concha → mound coupling).
3. **HR1 cuff sliver repair** (`hv_cuff_repair.py`).
   - Tangential relaxation of cuff vertices of any cuff quad with a corner < 12°, kept on the skin surface, topology unchanged, deterministic.
   - Not needed by HE2 on either configuration; HE2 passes cleanly. It is active in the path (HE3 c2: one face 12 → 15°, 0.011 cm).
4. **Placement-bias control** (`place_du` / `place_db`).
   - Interpretable "set height in the root footprint", clipped to keep the junction ≥ 0.15 cm inside the footprint.
   - Characterised in the Jacobian. Not used by HE2. Tested for HE3 but not adopted (c2 contact).
5. **Guard** (`hv_run_head.sh`). The Fenn deformation-aware guard plus the repair. It iterates until no problem face remains, not only until no new one appears.

## 4. HE2 before / after measurements and firewall (§8; board F)

**Measuring rule:** the same measured-domain firewall, on one common Halvren head and one root frame.
- **Cavum-level domain now stable.** It is the depth-weighted centroid of the deepest cavum region (was an argmax). Under the old argmax rule the "before" HE2 values were 0.68 / 0.93 / 0.80, the numbers quoted in the order.
- **Fail rule:** R² ≥ 0.80 with n ≥ 6.

| HE2 | MF ↔ Fenn | MF ↔ Aelari | MF ↔ Vael | Result |
|---|---|---|---|---|
| **before** (HVEAR2) | R² 0.73, α 0.81, n 11 | **R² 0.84, α 0.78, n 10 — FAIL** | R² 0.76, α 0.95, n 11 | FAIL |
| **after** (HVEAR3) | **R² 0.36**, α 0.50, n 11 | **R² 0.38**, α 0.43, n 10 | **R² 0.32**, α 0.54, n 11 | **PASS, wide margin** |

**What still correlates with each pair after the correction:**
- Fenn: tragus / cavum level, upward extension, width.
- Aelari: upward extension, length, concha.
- Vael: root line, tragus / cavum level, tip.

Corrected HE2 differs by > 0.5 SD from Marchfolk in 10 / 11 domains, and from Fenn / Aelari / Vael in 8 / 9 / 9.

The corrected HE2 is a non-linear trait combination, in its own basin (boards A, B):
- **Human-family** helix fullness (above Marchfolk), free lobe and lower projection / backward angle;
- **Elven** elevated upper extension and controlled point (82°, between human 124° and elf 53–64°);
- **Moderate** length (t 0.68);
- **Integrated** concha and tragus.

It reads as neither a stretched human ear nor a reduced Aelari / Vael ear.

## 5. HR1 root, c1 and c2 (§6; board C)

| Corrected HE2 | c1 | c2 |
|---|---|---|
| Technical (100 % quads, 1 component, 0 boundary / non-manifold / degenerate, outward, 0 branch self-intersections) | PASS | PASS |
| Min corner / aspect max | 23.5° / 9.24 | 20.6° / 9.24 |
| Anterior cuff mound p90 / anterior junction above skin | **0.12 / 0.27 cm** | **0.05 / 0.14 cm** |
| Concha floor vs hidden-ear skull | −0.58 cm | −0.58 cm |
| Root valence / crease max | 4 × 52 / 61.6° | 4 × 52 / 64.0° (v005 human root 69°) |
| Density (mean edge / stature) | 0.105 % | 0.102 % |
| Ear–head clearance min | 0.33 cm | 0.37 cm |
| 8 head / neck poses (contacts / flips / root inversions) | 0 / 0 / 0 | 0 / 0 / 0 |
| Guard iterations / cuff repair | 0 / none needed | 0 / none needed |
| Determinism (independent rebuild) | dV 0, faces identical | dV 0, faces identical |

Neutral-clay root / concha read: one auricle on both configurations. There is:
- no stacked ear, visible cuff or duplicated root;
- no floating concha or disconnected tragus;
- no root pinch;
- a natural anterior junction;
- no collision.

**Rejected alternatives with the same HVEAR3 geometry (board E):**
- rigid Fenn cuff: mound 0.66 cm, the stacked read;
- exact Vael RI3 root: mound 0.45 cm.

## 6. HE3 firewall re-check (§7)

**Before.** The HVEAR2 HE3 re-measured as **R² 0.98 vs Marchfolk → Aelari**, effectively a scaled Aelari interpolation.

**Recalibration.** I recalibrated it with the HE2 logic: long elevated upper extension, sharper taper and strong sweep, with a human-family body (wb 1.95, concha 1.00 seated, fuller shouldered helix).
- A 0.35 cm upward placement brought it to R² 0.78, a narrow pass on c1.
- But that placement drives the back sheet into the cuff on c2: 29 back / cuff self-intersections.

**Adopted, c2-safe version** (projection 26, root flare 38, no placement bias):

| | MF ↔ Fenn | MF ↔ Aelari | MF ↔ Vael |
|---|---|---|---|
| HE3 | R² 0.76 | **R² 0.87 (α 0.82) — FLAG** | R² 0.72 |

- It differs from Aelari in 7 / 11 domains, so it is not a duplicate.
- But it realizes close to the Marchfolk → Aelari line, driven by upward extension, length and concha.
- **Technical:**
  - c1: clean.
  - c2: one posed contact, 2 pairs at head yaw right 45°. The right lower postauricular back sheet meets the cuff and survives the guard.
- **Flagged, not silent.** The elf-forward bound of this realization path is open: it trades firewall margin against c2 clearance. It is a carry-forward, outside the HE2 freeze.

## 7. HE1 size-floor disposition (§7)

**This is a real constraint of the shared engineering sheet, now a deliberate family bound. It is not an artifact of measurement.**
- **Length sweep (rest state, c1):**
  - L 5.8 aspect 10.09 — fails;
  - L 6.2 / 6.3 / 6.5 clean.
- **Floor.** The clean floor is L ≈ 6.2, measuring 0.306 HH against the Marchfolk auricle's 0.240 (+27 %).
- **Why it can't go shorter.** The sheet layout is fixed (the E2-metric canonical layout), so a shorter ear compresses the front sheet.
- **HE1 within this path.** HE1 stays at L 6.3 and is the human-forward member of the bounded path:
  - firewall R² ≤ 0.28 with every elf;
  - clean on c1 and c2;
  - shares HE2's orientation (proj 16, tilt 12);
  - shares HE2's calibrated body (wb 2.00, concha 1.00, seat −0.58), needed for c2 — the narrow HVEAR2 HE1 body gave 22 self-intersections there;
  - keeps its own late, blunt shouldered apex.
- **Human-size HE1** (0.24–0.26 HH) needs the human-scale scaffold of the dedicated-branch proposal. It is not required for HE2.

## 8. Continuum, mosaic, production checks (§5, §9D, §10)

- **Continuum (board B).**
  - Composite elf-ward position: HE1 0.46 < HE2 0.60 < HE3 0.98.
  - Backward angle, cavum level and helix fullness are non-monotone across HE1 → HE3, so the family is not lockstep.
  - One root path and one topology for all three.
- **Mosaic (board D).** HB2 + HF2 + HP-B with HE1 / HE2 / HE3: one organism each. Corrected HE2 sits naturally on the central face.
- **Production regression** (`HE_production_checks.json`; frozen Vael parameters on the same head for comparison):

| | Corrected HE2 c1 / c2 | Frozen Vael (same head) |
|---|---|---|
| Mirroring: L/R sheet correspondence | 0.024 / 0.031 cm max; sheet connectivity identical | 0.024 cm; identical |
| Export: .blend write / reload | dV 6e-6 cm (float32), faces equal | same |
| LOD: Decimate 50 % / 25 % | 0 non-manifold, 0 zero-area faces in the ear region | same |

  - The cuff transition band is canonical per side, as in the frozen elf ears.
- **Character creator.**
  - The realization path exposes the same interpretable controls plus seat rule and placement height. The Jacobian is the creator-facing sensitivity map.
  - The lobe-size control is inert on this sheet. Lobe size is expressed through length / placement; it is documented, not hidden.

## 9. §10 acceptance gates

| # | Gate | Result |
|---|---|---|
| 1 | One-auricle visual read | **PASS** (boards A, C) |
| 2 | HR1 root on c1 and c2 | **PASS** (mound 0.12 / 0.05, junction 0.27 / 0.14 cm) |
| 3 | No cuff / stacked-ear read | **PASS** (rigid cuff 0.66 / RI3 0.45 rejected, board E) |
| 4 | Topology / connectivity | **PASS** (one face topology, all-quad, 4 × 52 root) |
| 5 | Drift diagnosed and corrected | **PASS** (§1–§3) |
| 6 | HE2 arithmetic firewall vs all three elves | **PASS** (R² 0.36 / 0.38 / 0.32) |
| 7 | HE1 / HE2 / HE3 coherent continuum | **PASS** (order 0.46 < 0.60 < 0.98; non-lockstep; one path). HE3 flags in §6 |
| 8 | Corrected HE2 natural on HB2 + HF2 | **PASS** (board D) |
| 9 | Frozen Marchfolk / Fenn / Aelari / Vael untouched | **PASS** (`immutable_hashes.txt` identical to the previous gate; frozen ears rebuild dV 0) |
| 10 | No deformation / LOD / mirroring / export / creator regression | **PASS** for HE2 (§5, §8) |
| 11 | HE1 size floor resolved or bounded | **BOUNDED** (§7) |
| 12 | HE3 re-checked, not silently collapsing | **RE-CHECKED AND FLAGGED** (§6) |

**Carry-forwards (not HE2 blockers):**
- **HE3:** R² 0.87 vs Marchfolk → Aelari, and one posed contact on c2.
- **HE1:** floor at about +27 % of the Marchfolk auricle.
- **HE2:** the root line remains Vael-like (−23°).
- **Lobe control:** inert on this sheet.

## STOP

STOP FOR CHATGPT REVIEW.
- No freeze executed.
- No other Halvren system or race touched.
- No retopology beyond the bounded realization path.
