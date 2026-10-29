# RAC RP3 — Halvren HE2 ear root visual integration correction report

**Order:** `reviews/chatgpt-rac-rp3-halvren-ear-root-visual-integration-correction-order.md` (651d7f5; reviewed commit 29f2c16).
**Evidence:** `reviews/rac-rp3-evidence/halvren_rp3_he2_root_visual/`

| File | Contents |
|---|---|
| `HE2_root_visual_record.json` | consolidated record: technical regression HR1 vs HR2, secondary-silhouette measures, sheet preservation, domains / firewall, determinism, outside-root identity, frozen-ear rebuild |
| `HE2_root_visual_prodcheck.json` | mirroring / export-reload / LOD |
| `boards/HE2RV_A..G` | A critical silhouette, B before / after, C wireframe, D / D2 standard views + ear-only lineup, E body / face / ear, F firewall, G HE1 / HE3 |
| `diagnosis/` | root cross-sections HR1 vs HR2 (posterior and inferior) |
| `trials/HR2_root_trials.json` | every rest-state root trial (98) |
| `records/` | per-realization build / audit / deform / guard / repair / measure (HE1 / HE2 / HE3, c1 / c2) |
| `HV_ear_definitions_HVEAR3_HR2.json` | HVEAR3 definitions + HR2 root (and the HR1 "before" variants) |
| `immutable_hashes.txt` | frozen references re-hashed: 14 / 14 unchanged |
| `blind_visual_review.md` | independent blind visual review of boards A / B / D |

**Tools** (`tools/rac/rp/halvren_rp3_v001/`): `hv_root_sectors.py` (pedestal / loop-crease / lower-fork measures), `hv_root_xsec.py` (root cross-sections), `hv_he2_rootvis.py` (record), `hv_he2_rootvis_boards.py` (boards); `hv_cuff_repair.py` gains a stage-2 sliver / stretch repair; `hv_ear_quick.py` gains true posterior cameras.
**Shared library** (`fenn_rp3_v001`, all inert unless set; Fenn / Aelari / Vael rebuilt dV 0): `ear_build.py` HR2 controls `root_lower*`, `sulcus_h` / `sulcus_r`, `fair_rings`; `ear_branch_lib.py` `HV_ROOT2` on HE1 / HE2 / HE3 (HE*-HR1 keep the old root). `grask_rigprep_v001/render_attr.py`: optional `RENDER_REVEAL` cavity shading for the boards.

## DISPOSITION

## HE2 ROOT VISUAL INTEGRATION APPROVED — READY FOR CHATGPT/AUTHOR FREEZE REVIEW

The corrected HR2 root reads as one auricle on both c1 and c2. In every rear, rear-3/4, stronger rear-3/4, direct-rear and lower-rear view:
- the posterior pedestal / flange is gone;
- the lower fork is gone;
- the lobe is the lowest form.

HE2 morphology is preserved. The auricle sheet is moved rigidly (seated 0.5 cm onto the head, 2° rotation; non-rigid residual mean 0.05 cm).

The firewall stays below 0.80 (0.51 / 0.44 / 0.23). The ear is technically clean on c1 and c2, including the 8 deformation poses.

A blind reviewer agent, given only the boards, also returned PASS on c1 and c2, calling both narrow passes. HE2 is not frozen. The non-gate polish items it raised are listed in §4.

## 1. Root-cause diagnosis

The secondary silhouette was not in the auricle. It came from what the auricle was mounted on: the v005 MPFB root zone.

**1. The auricle sat on the old human-ear pedestal.** The 52-vertex v005 root loop is the base of the MPFB human auricle. Against the head surface extrapolated over the ear zone from the skin outside it, the loop stands up to 0.93 cm high posteriorly and 1.16 cm inferiorly (p90, HE2 c1). The inferior part is the old human lobe base.

HR1 seated the auricle on the hidden-ear skull field fitted to that raised loop. Its skin-hugging cuff then followed the loop level. The result was a plateau whose rim, the loop, read as a second contour behind and below the pinna:

| Sector (HE2 c1, HR1) | Root height above head, p90 |
|---|---|
| posterior | 0.93 cm |
| superior | 0.60 cm |
| anterior | 0.35 cm |
| inferior | 1.16 cm |

Behind the ear the head falls away steeply toward the mastoid / neck. The loop therefore ended in a cliff: in the posterior sections (`diagnosis/HE2_root_sections_posterior_c1.png`) the transition ring drops 0.3–0.5 cm within one ring.

**2. The root loop was a crease.** The loop was a fixed boundary of the biharmonic root fairing, so the cuff met the head at a crease along it:

| Sector (HE2 c1, HR1) | Loop crease, mean |
|---|---|
| posterior | 32° |
| superior | 25° |
| inferior | 28° |
| anterior | 4° |

Under any light, that crease draws the loop as an outline parallel to the helix.

**3. The lower fork was a raised cuff tab beside the free lobe.** The loop's inferior bump (the old lobe base) lifted the cuff into a tab 0.53 cm above the head, reaching down to u −2.79 cm next to the lobe tip (−2.95 cm). Lobe-edge lift 0.70 left a notch between the two (`diagnosis/HE2_root_sections_inferior_c1.png`). Two downward forms plus a notch made the fork.

**What it was not.**
- Not mound p90 or the junction: both were already low.
- Not the concha seat.
- Not connectivity.

The 29f2c16 "one-auricle" metrics measured the anterior cuff only. All three cues above are posterior / inferior.

**Note on the reviewer's view.** The 29f2c16 board camera labelled "3/4 rear" (`etqr`) actually sits anterior-lateral and looks backward. The defect is visible both there and from true posterior cameras. Both are on the boards: "Board-E rear 3/4" is the old camera; rear 3/4, stronger rear 3/4, direct rear and lower-rear 3/4 are true posterior cameras.

## 2. Exact loops / controls changed (HR2; topology unchanged)

Face connectivity is identical to HR1 (face sha256 equal, c1 and c2). Root valence is 4 × 52 on both sides. No shell, no duplicate surface, no rigid Fenn cuff, no RI3 root. Board C marks every altered vertex.

| # | Control | What moves |
|---|---|---|
| 1 | **Root-loop lowering** (`root_lower 0.10, root_lower_cap 0.30, root_lower_cap_inf 0.60, root_lower_smooth 10`) | The 52 loop vertices per side move along the root normal onto the head extrapolated from the skin 3+ rings outside the loop (thin-plate; a stiff fit invents a bump below the ear). Each is capped at 0.30 × head scale, 0.60 on the inferior third (lobe base), and loop-smoothed. |
| 2 | **Skin fall-off** (`root_lower_fall 1.0, root_lower_fall_own`) | v005 skin within 1.0 × head scale cm of the loop follows the loop drop with a smooth fall-off, never below the head fit (no trough). Moved: 316 / 322 v005 vertices (c1 / c2), all within 0.78 cm of the loop. Every other v005 vertex is byte-identical (body, face, pelvis). |
| 3 | **Seat** | The ear frame stays the unlowered one. The auricle is seated on the lowered head (skull field re-fitted): it now sits on the head instead of on the pedestal. Rigid seat shift 0.51 / 0.49 cm along the root normal, rotation 2.0 / 1.8° (c1 / c2). |
| 4 | **Postauricular sulcus** (`sulcus_h 0.15`) | Back / rim sheet within 0.9 × scale cm of the non-front junction is lowered so that junction sits 0.15 cm above the skull. The anterior attachment and the free auricle are untouched. |
| 5 | **Lobe edge** (`lift_lobe 0.70 → 0.30`) | The free lobe edge stays close to the head, so no notch opens under it. |
| 6 | **Wide root fairing** (`fair_rings 1`) | The root loop and one more v005 ring join the biharmonic unknowns (1,028 unknowns), so the base blends into the head over a band instead of creasing at the loop. |
| 7 | **Cuff repair stage 2** (`hv_cuff_repair.py`) | Per-vertex tangential search for slivers at the cuff / rim seam and for over-stretched (aspect > 10) cuff quads. Fixed HE2 c2 (9.0° → 13.4°) and HE3 c1 (aspect 10.6 → 9.2). |

**Rejected on the way** (all in `trials/`; the exploratory controls were removed from the code):
- Posterior skin pull on the cuff: self-intersections.
- Lowering the lower front junction: no effect.
- Inferior cuff ramp: no effect, because the bump was in the loop.
- Crease softening: no effect, because the slit was the loop crease.
- Larger caps (0.5 / 0.7): cuff folds.
- Decoupled seat (auricle left on the pedestal; skin lowered under it): the pedestal goes, but a deep lower notch remains, and R² rises to 0.55–0.74.

HE3 takes HR2 without the sulcus (item 4). On its longer, more projecting back sheet the sulcus pushes the sheet into the cuff (86–113 self-intersections).

## 3. Before / after silhouettes and lower-root closeups

Boards A and B use identical cameras and cavity (ridge / valley) shading.

- **Board B, BEFORE (29f2c16 HR1).** The defect is visible in every view:
  - Board-E rear 3/4: a raised root mass left of the concha with its own contour, plus a hanging tab and a notch beside the lobe.
  - Rear 3/4 and direct rear: a second, ear-shaped pedestal contour behind the helix.
  - Lower root, anterior: tab, then notch, then lobe.
  - Lower root, posterior: a second lobe-shaped outline under the lobe.
- **Board B, AFTER (HR2).**
  - The pinna rises straight out of the head.
  - Behind it, a shallow faired postauricular sulcus.
  - The lower root ends in one rounded lobe outline.
  - No raised mass, tab, notch or parallel contour.
- **Board A** shows the same on c1 and c2 with all six required angles (strict side, Board-E rear 3/4, rear 3/4, stronger rear 3/4, direct rear, lower-rear 3/4).
- **Boards D / D2 / E:**
  - the front, side and front 3/4 views are natural;
  - the ear-only lineup keeps HE2 between Marchfolk and the elves;
  - in body / face context the ear stands off the head (not flattened).

| Measure (left side) | HE2 c1 HR1 | HE2 c1 HR2 | HE2 c2 HR1 | HE2 c2 HR2 |
|---|---|---|---|---|
| Root above extrapolated head p90, posterior / superior / anterior / inferior (cm) | 0.93 / 0.60 / 0.35 / 1.16 | 0.23 / 0.06 / 0.19 / 0.28 | 0.87 / 0.65 / 0.34 / 1.08 | 0.17 / 0.07 / 0.17 / 0.22 |
| Root-loop crease, posterior / superior / inferior (mean deg) | 32 / 25 / 28 | 6 / 2 / 7 | 34 / 25 / 31 | 9 / 3 / 7 |
| Lowest raised cuff point (> 0.15 cm) vs lobe tip, u (cm) | −2.79 vs −2.95 (tab beside lobe) | +0.44 vs −3.00 (none below attachment) | −2.74 vs −2.89 (tab) | +0.54 vs −2.94 (none) |

## 4. c1 / c2 visual-gate decision

| | Two ear-like contours from rear-3/4? | Lower fork / notch? | Side view | Postauricular depth | Decision |
|---|---|---|---|---|---|
| **c1** | no | no | natural | believable (sulcus; ear stands off the head in front / rear views) | **PASS** |
| **c2** | no | no | natural | believable | **PASS** |

**Independent check.** A blind reviewer agent saw only boards B, A and D, with the rejection criteria but not this report. It returned **PASS / PASS** and called both narrow. It flagged non-gate polish items, which are recorded here rather than hidden:

- **Root-related (HR2):**
  - A soft skin crease just below the lobe in the lower-rear views, which can read as the lobe sitting slightly off the skin.
  - A short horizontal crease where the lobe base meets the cheek (side view). Both are the inferior end of the faired root band (inferior loop crease 7°).
  - A slightly uneven back-of-concha strip inside the rim in the direct-rear view.
  - Wider fairing (2 rings) removes both creases but is not robust: 3–128 branch self-intersections across c1 / c2 (`trials/`).
- **Pre-existing in the HVEAR3 sheet (unchanged by this pass, outside the root):**
  - a Z-shaped kink of the inner rim on the posterior surface;
  - streaky cavity shading across the concha bowl.

## 5. Wireframe / topology evidence (board C)

- **Connectivity:** HR1 and HR2 have identical connectivity (face sha256 equal per configuration).
- **Marking:** red = the root loop (now lowered and faired); orange = v005 skin in the fall-off band / extra ring; magenta = sheet vertices moved non-rigidly > 0.06 cm (sulcus band on the back / rim near the junction; lobe edge); blue = cuff; green = transition ring.
- **Sheet:** the auricle sheet is otherwise rigid. Non-rigid residual after the seat shift: mean 0.05 cm, p95 0.13, max 0.51 (lobe edge) on c1; 0.04 / 0.10 / 0.40 on c2.

## 6. Technical regression

| Gate | HE2 c1 HR1 | **HE2 c1 HR2** | HE2 c2 HR1 | **HE2 c2 HR2** |
|---|---|---|---|---|
| components / boundary / non-manifold / degenerate | 1 / 0 / 0 / 0 | 1 / 0 / 0 / 0 | 1 / 0 / 0 / 0 | 1 / 0 / 0 / 0 |
| outward normals | yes | yes | yes | yes |
| branch self-intersections | 0 | 0 | 0 | 0 |
| min corner (deg) | 23.5 | 13.0 | 20.6 | 15.3 |
| max aspect | 9.24 | 9.67 | 9.24 | 9.28 |
| density (% stature) | 0.105 | 0.101 | 0.102 | 0.098 |
| root valence | 4 × 52 both | 4 × 52 both | 4 × 52 both | 4 × 52 both |
| 8 deformation poses (contacts / flips / root inversions) | 0 | 0 | 0 | 0 |
| guard iterations | 0 | 0 | 0 | 0 |
| mound p90 (cm) | 0.12 | −0.02 | 0.05 | −0.03 |
| anterior junction (cm) | 0.27 | −0.23 | 0.14 | −0.34 |
| concha floor (cm) | −0.58 | −1.11 | −0.58 | −1.08 |
| head / ear clearance min (cm) | 0.33 | 0.16 | 0.37 | 0.18 |
| **technical pass** | yes | **yes** | yes | **yes** |

**How to read mound / junction / floor.** These are measured against the fixed hidden-ear skull of the unlowered family head, as in 29f2c16. Negative values mean the cuff and junction now sit at or below the old pedestal level. Against the extrapolated head they sit at +0.17 to +0.28 cm (table §3). The floor is 0.5 cm deeper because of the seat shift.

**Clearance.** It falls to 0.16 / 0.18 cm, with 6 / 3 sheet vertices under 0.2 cm, because the lobe edge now hugs the head. None of the 8 poses produces a contact.

**Other checks:**
- **Mirroring:** sheet left vs mirrored right 0.029 / 0.010 cm max, connectivity identical (Vael reference 0.024).
- **Export / reload:** dV 6e-6 cm, faces equal.
- **LOD:** decimate 50 % / 25 %: 0 non-manifold edges, 0 zero-area faces in the ear region (as Vael).
- **Determinism:** independent HE2 rebuild with the recorded guard set and the repair: dV 0, faces identical, c1 and c2.
- **Frozen references:**
  - Fenn E2, Aelari AE-E2 and Vael VA-E2-RI3 rebuilt on the common head with the final `ear_build.py`: dV 0, faces identical.
  - 14 / 14 frozen reference files re-hashed unchanged: v005 blend and map, MPFB / Fenn / Aelari / Vael freeze JSONs, Fenn / Vael topology and canon, r6 heads.

## 7. HE2 firewall re-check

Same domains, same sources (MF / FN / AE / VA on the common c1 head), same normalisation.

| Pair | HVEAR3 (HR1, 29f2c16) | **HR2 c1** | HR2 c2 | Limit |
|---|---|---|---|---|
| MF ↔ Fenn | 0.36 | **0.51** | 0.45 | < 0.80 |
| MF ↔ Aelari | 0.38 | **0.44** | 0.41 | < 0.80 |
| MF ↔ Vael | 0.32 | **0.23** | 0.22 | < 0.80 |

All three pairs stay well below 0.80. MF ↔ Fenn rose by 0.15. The fit is driven by tragus height, width, upward extension and tip angle.

**Domain changes (HE2 c1)** and why:

| Domain | HR1 | HR2 | t HR1 → HR2 | Why |
|---|---|---|---|---|
| length / HH | 0.328 | 0.328 | 0.68 → 0.68 | unchanged |
| upward extension / HH | 0.092 | 0.090 | 1.11 → 1.08 | unchanged (seat) |
| backward angle | 14.6° | 14.6° | 0.50 → 0.50 | unchanged |
| tip angle | 82.6° | 82.6° | 0.62 → 0.62 | unchanged |
| helix fullness | 0.753 | 0.758 | −0.66 → −0.72 | unchanged |
| projection | 17.7° | 18.6° | 0.33 → 0.36 | +0.9°: 2° seat rotation; not flattened |
| width / length | 0.435 | 0.388 | 0.88 → 1.27 | measurement: width counts "free" auricle > 0.25 cm above the unlowered skull, so the 0.5 cm seat drops part of the broad base under that threshold; the sheet shape is unchanged (rigid residual mean 0.05 cm) |
| root line | −22.6° | +0.1° | 7.3 → −0.5 | intended: the anterior skin-attachment line is the root relation the order changes |
| concha depth / L | 0.220 | 0.195 | 0.79 → 1.19 | the seat and sulcus change the skin level the concha closing reads from |
| tragus height | 0.264 | 0.289 | 1.82 → 1.49 | the cavum centroid reads relative to the new attachment |
| lobe fraction | 0.043 | 0.051 | −0.05 → 0.07 | lobe edge lift 0.30 |

The auricle morphology (L, upward extension, tip, backward angle, fullness, projection) is preserved. The changed values are root relations or seat-sensitive measurements, not a return to the Marchfolk → elf line.

## 8. HE1 / HE3 (shared root, consistency only; not frozen)

| | HE1 c1 | HE1 c2 | HE3 c1 | HE3 c2 |
|---|---|---|---|---|
| technical (HR2) | clean (min 18.1°, aspect 9.78) | clean | clean (12.4°, 9.17; guard 3) | clean (13.9°, 8.54; 0 posed events) |
| pedestal p90 post / inf (cm), HR1 → HR2 | 0.90 / 1.10 → 0.22 / 0.28 | 0.86 / 1.03 → 0.14 / 0.22 | 1.00 / 1.24 → 0.33 / 0.45 | 0.92 / 1.12 → 0.28 / 0.35 |
| loop crease post / inf (deg), HR2 | 7 / 6 | 7 / 7 | 8 / 6 | 19 / 6 |
| firewall best R² (c1) | 0.37 (HR1 0.28) | — | 0.88 MF ↔ Fenn (HR1 0.87 MF ↔ Aelari) | — |

Board G shows neither member with the secondary root silhouette. HE3 has no sulcus, so a slightly stronger back-sheet edge is visible behind its lower helix (c2 posterior crease 19°).

**Carry-forwards (open, not closed by this pass):**
- **HE1 size floor:** unchanged (L / HH 0.275).
- **HE3 firewall:** R² 0.88, now nearest MF ↔ Fenn rather than MF ↔ Aelari. Still open.
- **HE3 c2 posed contact:** the HR2 HE3 c2 build has 0 posed events (HR1 had one). This is recorded, not claimed as a family fix.

## 9. Immutable references

`immutable_hashes.txt`: 14 / 14 frozen references unchanged (sha256 against the HE2 closure list). Frozen Marchfolk, Fenn, Aelari and Vael ears are untouched. HB2 + HF2 + HP-B is unchanged outside the 0.8 cm root band.

## 10. Acceptance gates

| # | Gate | Result | Evidence |
|---|---|---|---|
| 1 | Rear-3/4 reads as exactly one auricle | **PASS** | A, B (c1, c2); blind review PASS |
| 2 | No posterior flange / cuff / pedestal as a second structure | **PASS** | pedestal p90 posterior 0.93 → 0.23 (c1), 0.87 → 0.17 (c2) cm; loop crease 32 → 6° / 34 → 9° |
| 3 | No lower fork / notch | **PASS** | no raised cuff below the attachment (lowest +0.44 / +0.54 cm vs lobe −3.0 / −2.9); B lower-root closeups |
| 4 | Side view natural | **PASS** | A, D (soft lobe-base crease noted) |
| 5 | Postauricular depth believable | **PASS** | faired sulcus; ear stands off the head (D, E); projection 18.6° |
| 6 | HVEAR3 HE2 morphology preserved | **PASS** | sheet rigid residual mean 0.05 cm; L, upward extension, tip, backward angle, fullness unchanged; changes explained in §7 |
| 7 | Firewall R² < 0.80, all three pairs | **PASS** | 0.51 / 0.44 / 0.23 (c2 0.45 / 0.41 / 0.22) |
| 8 | c1 and c2 pass the visual gate | **PASS** | §4 |
| 9 | Topology / deformation production-safe | **PASS** | §6: all integrity gates, 8 poses 0 events, mirroring, export, LOD, determinism dV 0 |
| 10 | Frozen references untouched | **PASS** | 14 / 14 hashes; Fenn / Aelari / Vael rebuild dV 0 |

## STOP

STOP FOR CHATGPT REVIEW. Nothing is frozen. No other race, Halvren system or ear redesign was started.
