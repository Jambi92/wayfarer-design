# RAC RP1E — v013 Class-A closure gate (order `chatgpt-rac-rp1e-v013-class-a-closure-order.md`)

**Date:** 2026-10-20
**Parent:** v012 (`GO_U_REF_RP1E_retopo_v012.blend`, sha 25e9b53c…7f9c)
**Result line:** **RP1E NON-LOCAL SUB-CAGE REBUILD BLOCKED / AUTHOR DECISION REQUIRED**

v013 clears a good share of the v012 Class-A list:

- R groin ridge end, chin lobe, L upper axilla, R axilla B tip;
- L thumb tip and wrist, R hand radial miss, R toe tips;
- the main L ear miss;
- the exposed R fused-digit gap: 8.4 → 3.65 mm.

The remaining blocked features are listed in §4:

- R thumb-web fin;
- philtrum bottom and upper-lip overhangs;
- ear rims;
- L axilla knob at z 143.6;
- R axilla A tip;
- natal-cleft nub;
- L palm crease;
- R hand ulnar web;
- fused-zone edges;
- several positive-normal folds.

Each had the two authorised support-topology attempts (§6), and each failed for the same physical reason, explained in §5.

Three further findings need an author decision:

- T-6 fails as measured.
- The source has genus 3 while the contract requires genus 0.
- Nails could not be checked per nail in this session.

No waiver was applied. The contract was not relaxed. No RP2, rigging, creator or UE5 work was done.

## 1. v013 design, import and provenance

| Item | Value |
|---|---|
| Design | `designs/design_v013.npz`: 5476 V / 5669 F (5279 quads, 390 tris); 1 component; 0 boundary; 0 non-manifold; Euler 2 (genus 0); 0 bad orientations; min edge 0.82 mm; **0 coarse self-x**. npz sha 5666d4cf…; also `_col.npy`, `_info.json` (exact repair list), `fsm_v013.txt` |
| Parent | design_v012 (v009–v012 unchanged) |
| OBJ | `RP1E_cage_v013_design.obj` sha 181a3227…, committed to `…\Gorrund\RP1\`; re-staged copy has the same sha |
| UI import | v012.blend → File > Import > Wavefront → Apply Rotation → old cage deleted → renamed `Cylinder` → Save As **`GO_U_REF_RP1E_retopo_v013.blend`** (sha 230c7b3a…d778). v012.blend was not overwritten. |
| Verify (`exp_v015/verify_import_v013.json`) | max deviation **0.00025 mm**; bijective, faces identical by index; 0 boundary; 0 non-manifold; Euler 2; 1 component; 0 bad orientations; 0 coarse self-x |

Blender was closed afterwards. The Explorer window I opened to launch it was closed; the user's original Downloads window was left alone.

### Repairs in v013 (`design_v013_info.json`, tools in `tools/rac/rp/rp1e/`)

1. **C1 R thumb web.** Graded support: two nested local Catmull-Clark refinements along the fin line (`refine.py`, `exp_v015/C1_refine1/2.json`).
   - The faces around the fin went from 3.0–7.3 cm to 0.65–1.6 cm.
2. **R fused digits** (an exposed Class-A miss: openness 0.69–1.0, so not hidden).
   - Digit C's tube now extends into the fused block, with 3 source-section rings.
   - It is capped short of digit B (`extend.py`, `exp_v015/C9_fusedR_extendC.json`).
3. **Local graded refinements** (one or two nested levels; `exp_v015/C2toC9_refinements_kept.json`):
   - chin, L thumb tip, L wrist, L toe-4 tip, R toe tips a/b;
   - L axilla upper (23.3, −40.3, 149.6), L ear, R groin ridge end;
   - R hand radial point (−26.9, −48.9, 97.8), R axilla B tip;
   - natal nub (one level).
4. **C3 mouth-line contact.** No geometry change; it is classified B (§3).

| Feature | v012 max (mm) | v013 max (mm) | Limit |
|---|---|---|---|
| R groin ridge end | 3.79 | **0.78** | 3.0 |
| L axilla upper (149.6) | 3.55 | **1.30** | 3.0 |
| R axilla B tip | 3.33 | **1.51** | 3.0 |
| Chin lobe | 2.72 | **0.44** | 1.5 |
| L ear main | 2.89 | **1.36** | 1.5 |
| L thumb tip / wrist | 2.75 / 2.52 | **1.19 / 1.18** | 1.5 |
| R hand radial | 2.03 | **0.25** | 1.5 |
| R toe tips a / b | 2.00 / 1.88 | **1.06 / 0.86** | 1.5 |
| L toe-4 tip | 2.14 | 1.62 | 1.5 |
| R thumb fin | 4.90 | 2.41 | 1.5 |
| R fused-digit gap | 8.38 | 3.65 | 1.5 |
| Natal nub | 5.06 | 3.55 | 3.0 |

## 2. Full progressive gate (v013 = sim G13 on the UI-imported cage; `gate_v013/`)

**Self-intersection pairs by level** (v012 in brackets):

| Level | Total | General | Axilla | Perineum | Head | Hand L / R | Foot L / R |
|---|---|---|---|---|---|---|---|
| L1 | 30 [23] | 10 | 6 | 4 | 4 | 11 / 5 | 0 / 0 |
| L2 | 137 [121] | 18 | 14 | 4 | 2 | 37 / 79 | 0 / 1 |
| L3 | 961 [926] | 175 | 150 | 25 | 4 | 216 / 543 | 0 / 23 |
| L4 | **1492** [1104] | 208 | 199 | 9 | 89 | 334 / 846 | 2 / 13 |

The increase at L4 is mostly the R fused-digit contact (475 → 818 pairs, §3) and the L ear fold (29 pairs).

**Deviation, source → product** (% of the zone over its max; L4 also shows median / p95 / max in mm):

| Zone (limit) | L1 | L2 | L3 | **L4** | v012 L4 |
|---|---|---|---|---|---|
| T-1 general (3.0) | 12.7 % | 2.20 % | 0.19 % | 0.023 / 0.24 / 15.5, **0.05 %** | 0.07 % |
| T-2 head (1.5) | 26.5 % | 10.1 % | 2.11 % | 0.024 / 0.25 / 2.57, **0.05 %** | 0.13 % |
| Hand L (1.5) | 16.8 % | 3.79 % | 0.63 % | 0.030 / 0.20 / 9.81, **0.49 %** | 0.63 % |
| Hand R (1.5) | 17.8 % | 2.88 % | 0.33 % | 0.033 / 0.17 / 3.65, **0.24 %** | 1.17 % |
| Foot L (1.5) | 7.6 % | 3.08 % | 0.67 % | 0.015 / 0.12 / 1.74, **0.01 %** | 0.03 % |
| Foot R (1.5) | 12.6 % | 3.83 % | 0.19 % | 0.018 / 0.15 / 1.78, **0.04 %** | 0.06 % |
| Tail root (1.5) | 12.5 % | 0.18 % | 0 % | max 0.24, 0 % | 0 % |

- **Product → source maxima:** general 2.47; head 1.73 (was 3.43); hand L 1.24 (was 2.06); hand R 10.39 mm. The hand R value comes from internal digit sheets inside the fused block (§3).
- **Final L4 face size:** about 0.5–1.4 mm in the identity zones.
- **Openness of over-limit points** (`devopen.log`):

| Zone | Points over limit | Sealed | Exposed |
|---|---|---|---|
| General | 182 | 46 % (the D void) | 4 % |
| Head | 29 | 0 % | 48 % |
| Hand L | 133 | 65 % (the D tunnel) | 1 % |
| Hand R | 51 | 0 % | 35 % |
| Feet | 6 / 17 | 0 % | 53–67 % |

- **Cross-sheet ownership:** no cage-caused ownership errors. Finger colours 17–24 each own their own digit.
- **T-1:** FAIL, because points over 3.0 mm remain outside the deferred void.
- **T-2:** FAIL. The head max is 2.57 mm, and both hands and both feet still have points over 1.5 mm.

### Other gates (`gate_v013/gate_T/rp1_gate.json`, `T6_landmarks.json`)

| Gate | Result |
|---|---|
| Topology at L4 | 1 component; 0 boundary; 0 non-manifold; genus 0; 0 degenerates; 100 % quads; no directed-edge duplicates. The signed volume is negative only because the analysis frame is y-mirrored. |
| T-3 | Stature Δ −0.027 mm; bbox Δ ≤ 0.47 mm. **PASS** |
| T-4 | 91.9 % of quads have all angles in 45–135°; 96.5 % have aspect ≤ 4 (information) |
| T-7 IoU | front 0.99857 / profile 0.99785 / rear 0.99859. **PASS** |
| T-6 | **FAIL as measured.** hip_R 6.98 mm; tail_00 1.11, tail_09 1.27, tail_12 1.51 mm; all others ≤ 0.87 mm. |
| Nails | **Not measured.** The AW4 nail-plate masks and foot frames used by `rp1_gate.py` are not in the cloud workspace now. Foot-zone deviation max is 1.74 / 1.78 mm, but that is not the per-nail ±0.15 mm test. |

**hip_R diagnosis** (`t6diag.py`):

- The hip_R landmark section (plane z ≈ 94.8, radius 24.6 cm) also cuts the R hand, which hangs at hip level.
- The hip part alone drifts **0.01 mm**.
- The drift comes from the hand part, where the product section is longer than the source (52.5 vs 46.8 cm) because of the internal fused-digit sheets. v012 measured 3.7 mm here.
- The tail stations show 3 % extra product section length with sub-0.25 mm surface deviation. I did not chase this further.

## 3. Residual classification at v013 (L4; `cls_G13.json`, `devopen_G13.npz`)

### D — deferred sealed source micro-cavities (approved cases only)

| Cluster | Max | Evidence |
|---|---|---|
| L axilla zero-gap void behind the pinch (23.8, −40.5, 146.5) | 15.5 mm, 149 points | 46 % of points sealed (openness 0) |
| L hand sealed web tunnel (38.5, −50.9, 100.5) | 9.8 mm, 100 points | Closed source slice loops (v011 evidence) |

I found no new D case.

**Source topology.** The source mesh has genus 3 (χ = −4), but the contract requires a genus-0 product. Each handle is a sealed tunnel, the void, or the fused-digit bridge. A genus-0 cage cannot represent these as true fusion or tunnels. This is a contract-level fact, stated here for the author.

### B — provisional source-consistent micro-contacts

| Pairs | Cluster | Source gap vs face | Amp / open | Visible | Deformation zone / skinning |
|---|---|---|---|---|---|
| 818 (+14 +2 +1) | R fused digits (−33.1, −38.7, 92.9): digit C cap and digit B wall inside the intentionally fused block | source fused (gap 0) | 8.1 mm interpenetration of hidden internal sheets; open 0.46 | Exterior follows the block, max 3.65 mm at the edges | **Yes (fingers).** High skinning risk: the internal sheets will cross under deformation. |
| 207 | L little/ring web beside the sealed tunnel (39.1, −46.4, 100.5) | 0.6 mm vs face 0.4 mm | 0.20 mm / 0.04 | Hidden | Yes (finger web); low amplitude |
| 25 | Mouth lip-line crease left of the corner (−0.8, −60.8, 179.7) | **C3 measured:** source is a zero- to 0.7 mm-wide lip crease (slices `exp_v015/` and `gate_v013`); L4 face 1.4 mm; the product follows the visible crease | 0.31 mm / 0.23 | Crease line only | Yes (jaw/lip); low |

### A — representable/open defects still present (self-x)

| Pairs | Cluster | Why it is not B |
|---|---|---|
| 139 | R axilla apex (−18.9, −32.8, 140.8) | Exposed (open 0.62); gap 0.4 mm is larger than the 0.09 mm face; amp 0.71 mm |
| 123 | L index/middle web (38.6, −55.9, 101.7) | Gap 3.5 mm is larger than the 1 mm face |
| 35 + 21 | L axilla pinch mouth / z153 pocket | Gap 0.4 / 1.45 mm, larger than the face |
| 29 + 5 + 5 | L ear fold (new with the ear refinement, amp 1.0 mm), ear knobs L/R | Positive-normal folds |
| 12 + 9 + 3 | Nose ridge, philtrum, nose folds | Positive-normal folds |
| 12 + 1 | R toe web | Gap 1.5 mm, larger than the face |
| 11 + 4 + 4 + 4 + 2 + … | R hand fold, L thumb-tip fold, small trunk/perineum folds, L toe-4 tip fold | Folds |

### A — deviation clusters still over their limit

The blocked features are in §4. Also over:

- small head points of 1.56–1.67 mm;
- L hand 2.05 mm (37.6, −54.7, 101.8);
- feet 1.5–1.78 mm, at L toe 4 and the L medial toe (23.0, −65.3, 2.7), and on R toes (−26.0…−27.0, −47.2…−48.1, 0.7–2.0).

## 4. Blocked features (two genuine attempts each)

| Feature | Source shape | v012 | Attempt 1 (topology → L1 / L4) | Attempt 2 (topology → L1 / L4) |
|---|---|---|---|---|
| **C1 R thumb-web fin** (−32.5, −47.0, 104.7) | Membrane about 2 mm thick, 3 mm proud, 1.9 cm long | 4.90 mm | Graded support (2 nested CC refinements) **+ fin band** (4 cols × 5 rows, walls on the membrane). L4 max 1.39 mm, but L1 hand R self-x 5 → 49 and L4 507 → 1981 (fold at the stitch). **Rejected** (`blocked_R_thumb_fin.png`, FN1) | Three nested refinements without a band (RF3): 2.36 mm, no new self-x. A crest-aligned support loop on top (RG1): 2.36 mm, +133 pairs. Kept: 2 levels (2.41 mm). |
| **C2 philtrum bottom** (2.05, −62.0, 181.7) | Notch 3 mm wide × 4 mm tall, opening down into the mouth band | 2.57 | Slot band re-oriented along the roof (normal (0, −0.82, −0.57), 3–5 cols, cells / 3dn stitches): 5–20 coarse self-x against the mouth-floor cells. Rejected before sim. | Graded refinement R 1.0 cm: 9 coarse self-x. R 0.8 cm: 1.55 mm, but L1 head 1 → 20 and L4 +1338 pairs. **Rejected** (`blocked_philtrum_bottom.png`) |
| **C2 upper-lip overhang** (4.94, −63.4, 185.0) / (−0.07, −63.5, 184.8) | 4–6 mm rounded overhang | 2.29 / 2.05 | Refinement 2.6 / 1.4 cm: 1.71 mm, but L1 head 33 and L4 +1515 pairs | Refinement 2.2 cm: 1.70 mm, +367 pairs. Smaller radii select no faces. |
| **C4 ear rims** (12.9, −49.5, 198.7), (13.6, −50.5, 200.9), R (−8.8, −49.5, 198.8) | 3–5 mm rim lobes | 2.46 / 1.94 / 2.18 | Refinement 1.8 / 1.0 cm: rim 2 → 0.68 mm, rim 1 → 1.24 mm, but the combination gives +182 pairs and rim 1 alone +526 | Refinement 1.2 / 0.7 cm: L ear 2.02 mm; rims unchanged (no faces selected). Kept only the main L ear (1.36 mm, 29-pair fold). |
| **C5 L axilla knob** (24.2, −39.0, 143.6) | 6 mm bulbous knob on a neck (`blocked_L_axilla_143.png`); open 0.15, so not part of the D void | 4.39 | Refinement 1.8 / 1.0 cm: 4.09 mm; axilla self-x 173 → 8820 | Refinement 0.9 / 0.5 cm: 3.96 mm; L1 axilla 2 → 54 (fold). Rejected. |
| **C5 L pinch-mouth / z153 folds** | Contacts at the pinch mouth (gap 0.4 mm) and in the z153 pocket (gap 1.45 mm) | 15 + 18 pairs | Covered by the C5 refinements above: no reduction (35 + 21 pairs) | — |
| **C6 R axilla A tip** (−18.6, −31.2, 141.9) | Thin flap tip about 3 mm wide, curled (`blocked_R_axilla_tip.png`) | 4.39 | Refinement 1.8 / 1.0 cm: 5.11 mm; axilla self-x 173 → 5134 | Refinement 1.4 / 0.8 cm: 4.61 mm; +448 pairs. (The B tip refinement worked: 3.33 → 1.51 mm.) |
| **C8 natal nub** (2.07, −28.75, 104.9) | Closed, externally visible protrusion about 7 × 12 × 8 mm. The source is closed and manifold (0 boundary edges); the gaps in the slice plots come from the slicer. Openness 0.15–0.69, so it is **exterior anatomy, not a micro-artifact**. | 5.06 | Refinement 1.8 / 1.0 cm: 3.60 mm, +10 pairs | Refinement 1.2 / 0.7 cm: 3.24 mm, L1 general 6 → 22 (fold). Kept one 1.2 cm level: 3.55 mm (`blocked_natal_nub.png`) |
| **C9 L palm crease** (32.1, −52.6, 104.9) | Crease continuing the thumb-web slit | 2.46 | Refinement 1.8 / 1.0 cm: 0.52 mm, but hand L self-x +1183 | Refinement 1.2 / 0.7 cm: no faces selected. Remains 2.33 mm. |
| **C9 L hand** (39.1, −46.4, 100.9) | Next to the sealed tunnel (open 0.08, 3 sealed points) | 3.51 | Hand group refinement: 2.37 mm; hand L self-x 343 → 34869 | — (tunnel-adjacent; D boundary) |
| **C9 R hand ulnar web** (−37.0, −37.2, 100.6) | Web edge | 3.08 | Refinement 1.8 cm: 4 coarse self-x, rejected | Refinement 1.2 cm: 4 coarse self-x, rejected |
| **R fused-digit edges** (−33.1, −40.3, 94.6), (−32.3, −40.7, 92.5) | Edges of the fused block | 8.38 (gap) | Digit C extension (kept): 3.65 / 3.18 mm; L1 clean | Refinements at both edges: 3.33 / 2.10 mm, but hand R self-x 842 → 11.5k / 14.5k. Rejected. |

## 5. Why further topology does not close these without a source or stack change

The remaining features share three properties:

- they are thin positive flaps, knobs or overhang lobes, or narrow notches, 2–6 mm across;
- they sit next to an existing slit, web or contact sheet;
- they are smaller than about two coarse faces of the surrounding cage.

**More support topology does move the limit surface onto them.** Every attempt reduced the deviation, often below the limit.

**But the projection stack then breaks it.** The stack is Subdivision → Shrinkwrap Project → Nearest per colour, repeated, with the final smoothing.

- On a denser local cage it drives the extra L2–L4 sheets of the neighbouring contact or slit into each other.
- Opposed-sheet self-x then grows by 10× to 100×:
  - axilla 173 → 5000–8800;
  - hand L 334 → 35k;
  - hand R 846 → 11–14k.
- Or folds appear already at L1 (fin band, natal nub, philtrum).
- For the two-walled fin band, the two walls are 2 mm apart. Nearest projection snaps them across each other at L1.

So each feature is caught between two failures: without the support it is missed (Class A deviation); with it, it folds or contacts (Class A self-x). A third topology attempt would hit the same mechanism.

Closing these needs one of the following author decisions:

1. **Projection-stack change.** For example: a contact-aware or collision-resolving final relax; limit-surface off, or a different projection order, in the identity regions; or per-sheet ownership targets for the flap tips. The parent contract fixes this stack.
2. **Source decision.** Open or seal the deferred void and tunnels; decide the R fused digits, where the source genus is 3 and the product must be genus 0; thicken or merge the 2 mm thumb-web membrane and the axilla flap tips.
3. **Contract decision.** Tolerances or Class-B acceptance for thin-flap tip rounding of 1.5–4.4 mm, and for the hidden fused-digit interpenetration.
4. **T-6.**
   - Re-define hip_R so the section excludes the hand, e.g. a smaller radius or a connected-component filter. The hip part alone drifts 0.01 mm.
   - Decide whether the tail stations at 1.1–1.5 mm need a separate look.
5. **Nails.** Restore the AW4 nail-plate masks and foot frames to the workspace so the per-nail check can run. This is a tooling matter, not geometry.

## 6. Evidence

- **Design:** `reviews/rac-rp1e-evidence/designs/design_v013.npz`, `_col.npy`, `_info.json`, `fsm_v013.txt`.
- **`reviews/rac-rp1e-evidence/gate_v013/`:**
  - G13 L1–L4 self-x log;
  - classification (`G13.cls`, `cls_G13.json`);
  - per-level deviation (`deviation_L1_L3.txt`);
  - openness (`devopen_G13.npz`, `devopen.log`);
  - T-3/T-4/T-7 and topology (`gate_T/rp1_gate.json`, IoU images);
  - T-6 (`T6_landmarks.json`);
  - blocked-feature L0/L1/L4 slices (`blocked_*.png`, `R_fused_digits.png`).
- **`reviews/rac-rp1e-evidence/exp_v015/`:**
  - all attempt logs: RF2/RF3/RG1/FN1 (thumb fin); EX2/EX8 (fused digits); RG_* and RI_* (refinement trials); RC1–RC3 (combinations);
  - attempt specs;
  - import verification.
- **Tools** (`tools/rac/rp/rp1e/`):
  - `refine.py` (local Catmull-Clark graded refinement);
  - `extend.py` (digit-tube extension from source sections);
  - `slitgen.py` (slit and fin bands);
  - `srcgap.py`, `sxdiff.py`, `t6diag.py`, `gate_nonail.py`, `rfl.py`.
