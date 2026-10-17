# RAC RM-OT-05AT — Gorrund AC3 two-mask posterior finish: return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05at-gorrund-ac3-two-mask-order.md` (e6bc1ef)
**Source:** `GO-05AO_AC2.blend` (sha `ba129999…f6f3`, verified before the Mask A write).
**Executor:** Claude. Both filter stages were authored in the Blender 5.2.2 UI on Tyler's PC. Cloud scripts were used only for the two mask attributes (with a 0.000 mm geometry proof), simulation, read-back, gates, GLB export and evidence.

## Verdict

**05AT AC3 PASS / READY FOR FINAL Q1-Q2 + TYLER VISUAL REVIEW**

Frozen:

| File | sha256 |
|---|---|
| `GO-05AT_AC3.blend` | `d462f36c08a3b528aff5b4408539f7dfe704b513585da6f2923136c60b7ea618` |
| `GO-05AT_AC3.glb` | `8ae6ccedffa5098ceb1fad18583edb18d2243060faf942bec933e79899c9fc0d` |

The geometry is identical to `GO-05AT_B.blend` (0.000 mm). Location: `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\source\Gorrund-Neutral-C\05AT\`.

**Result:** AR1r-like posterior softening, with no lateral or front-thigh stripe, no tail plateau and no crease chain. Every numeric gate passes. Blender is closed.

## 1. Key finding that made the two-mask route work

Under N Smooth events a vertex moves by roughly 1 − M^N of the full Laplacian. At M = 0.96, 120 events give about 99%, so any linear ramp near 1.0 acts as a hard edge. That is what produced the AR1r folds.

Mask A is therefore **log-mapped through the event count**. The desired smoothing weight w_s (a smoothstep over 80 mm from the hard boundary) becomes M_s = 1 + ln(1 − 0.95·w_s)/N. The deflate weight w_d is a separate belly-only smoothstep. The mask is M = min(M_s, 1 − w_d). Code: `atmask.py`, `mask_log` / `mask_log2`.

**Sweep before log mapping (`sweepA.py`):** the earlier linear masks (A0 to A3) all left 17–33 transition edges over 12°, up to 30°. Local bumps made things worse (`checks/maskA_site_refinement_log.json`).

**Final Mask A (`maskA`):**
- log-mapped with N = 120 and a smooth 80 mm transition;
- deflate weight on the belly only (30 mm protected band, then smoothstep over 60 mm);
- the 05AR root-core plateau (22 mm) and duplicate seams pinned at 1.0;
- 48 smooth local protections (R = 65 mm) at predicted kink sites, mostly the pre-existing sliver triangles beside the tail root.

**Mask B:** the same distance field, log-mapped for N = 10. The blend weight rises over 80 mm from the hard boundary and switches off inside the Stage-A belly. Minimum M_B is 0.81, so the belly is only lightly sculptable.

## 2. Masks and read-back

**Mask A (`checks/maskA_readback.json`):**
- geometry change 0.000 mm;
- core, ring, seams, protected sets, torso and joints all 1.0;
- 11 834 vertices with M < 0.5.

Visualisations: `views/mask_A.jpg`, `views/mask_B.jpg`.

**Tail core and ring:** the 05AR definitions are reused unchanged (free tail plus junction ≤ 8 mm = core; outer junction = ring).

## 3. Stage A — deflate + belly-only long Smooth

**Simulation (`checks/stageA_sim_table.json`):**

| Events | SI / flips / collapse | Belly max increase | Band max increase | Band edges > 12° | Ring | Pelvis | Hip core | Thigh L/R |
|---|---|---|---|---|---|---|---|---|
| 80 | 0/0/0 | 9.5° | 13.2° | 2 | 0.004 mm | −0.002% | 0 | −1.70/−1.37% |
| 100 | 0/0/0 | 8.3° | 12.5° | 2 | 0.005 | −0.002% | 0 | −1.77/−1.43% |
| 110 | 0/0/0 | 7.8° | 12.0° | 1 | 0.005 | −0.002% | 0 | −1.80/−1.45% |
| **120** | 0/0/0 | 7.3° | **11.5°** | **0** | 0.006 | −0.002% | 0 | −1.83/−1.48% |
| 130 | 0/0/0 | 6.8° | 11.4° | 0 | 0.006 | −0.002% | 0 | −1.86/−1.51% |
| 140 | 0/0/0 | 6.3° | 11.9° | 0 | 0.007 | −0.002% | 0 | −1.89/−1.54% |
| 160 | 0/0/0 | 5.5° | 12.7° | 1 | 0.008 | −0.002% | 0 | −1.94/−1.59% |

**Selection:** 120–140 model events pass every gate. Real UI smoothing has run about 1.16× the model, so **105 events were commanded**.

**UI settings:**

| Step | Settings |
|---|---|
| Deflate | Mesh Filter Inflate, strength **0.020**, −100 px in 10 events, Mask A |
| Belly Smooth | Mesh Filter Smooth, strength **1.000**, **105** mouse-move events |

**Real Stage A (`GO-05AT_A.blend`, sha `437bf574…1883`; `checks/stageA_real_*.json`):**
- Real smoothing matched the model at 105–120 events (mean deviation 0.32 mm).
- Technical: 0 seams opened, 0 SI, 0 flips, 0 degenerates, 1/0/0, protected 0.000 mm (ring 0.010 mm), stature and bounding box unchanged.
- Belly max increase 8.9°.
- Band max increase **13.5° on a single edge**. It sits on the pre-existing sliver triangle beside the tail root (x −9.0, z 94.5 cm, start quality 0.04). That is 1.5° over the Stage-A 12° target. Mask B covers it, so I continued (§8). After Stage B the final transition maximum is 12.2°, against a limit of 20°.
- Visual: softened posterior, no stripe (`views/stageA_body_*.jpg`).

**File-handling note:** after the Smooth, a mistyped Save As overwrote `GO-05AT_A_deflate.blend` with the post-Smooth state, so no separate deflate-only file survives. The same state was also saved as `GO-05AT_A_check.blend` and `GO-05AT_A.blend`. All three are geometry-identical, and the mask is unchanged (verified). The deflate step itself is the calibrated, exact-model operation.

## 4. Mask-only swap (§6) — proof in `checks/mask_swap_proof.json`

`GO-05AT_B_prep.blend` (sha `d2fdb0e3…dd40`) was made from `GO-05AT_A.blend` (sha `437bf574…1883`):

| Check | Result |
|---|---|
| Vertex coordinates | byte-identical |
| Loops / edges | identical |
| Object matrix | identical |
| Attribute set | identical (`.corner_edge`, `.corner_vert`, `.edge_verts`, `.sculpt_mask`, `position`) |
| Mask B read-back | matches the design (max difference 3e-8) |

## 5. Stage B — short boundary Smooth with Mask B

**Simulation from the real Stage A geometry (`checks/stageB_sim_table_from_real_A.json`):**

| Events | SI / flips / collapse | Max transition increase | > 20° | New abs > 35° | Chains | Belly change from A |
|---|---|---|---|---|---|---|
| **3** | 0/0/0 | **11.7°** | 0 | 0 | 0 | 0.02 mm |
| 5 | 0/0/0 | 11.6° | 0 | 0 | 0 | 0.04 |
| 8 | 0/0/0 | 12.4° | 0 | 1 | 0 | 0.06 |
| 10 | 0/0/0 | 14.3° | 0 | 1 | 0 | 0.07 |
| 15 | 0/0/0 | 18.5° | 0 | 1 | 0 | 0.10 |
| 20 | 0/0/0 | 20.8° | 1 | 2 | 0 | 0.14 |

**Selection:** the lowest count that gives clean continuity is **3 events**. **UI:** Mesh Filter Smooth, strength 1.000, 3 mouse-move events, then saved as `GO-05AT_B.blend` (sha `296130df…e61a`).

## 6. Final gates (`checks/final_gates.json`, `checks/final_metrics.json`)

**Technical:**

| Check | Result |
|---|---|
| Topology | identical |
| Seams opened | 0 |
| Self-intersections | 0 |
| Flips | 0 |
| Degenerates | 0 |
| Topology (components / boundary / non-manifold) | 1 / 0 / 0 |
| Duplicate seam pairs | closed (seams 0.000 mm) |
| Height | 204.5225 cm, unchanged |
| Bounding box | unchanged |

**Dihedral:**

| Check | Result | Limit |
|---|---|---|
| Max new transition-edge increase | **12.2°** | ≤ 20 ✓ |
| Edges > 20° | 0 | — |
| New absolute > 35° (vs Stage A) | 0 | 0 ✓ |
| Crease chains > 40 mm | **none** | none ✓ |
| Belly max increase | 8.8° | — |

**Tail core:**

| Metric | Result |
|---|---|
| Root centroid | 0.000 mm |
| Emergence height | 0.000 mm |
| Root axis | 1.5e-6° |
| Root width | 0.000 mm |
| Root depth | 0.000 mm |
| Free tail | 0.000 mm |

**Shape preservation:**

| Metric | Result | Limit |
|---|---|---|
| Continuity ring | 0.010 mm | ≤ 3.0 ✓ |
| Pelvis width | −0.004% | ≤ 0.5% ✓ |
| Skeletal hip (hip-joint core) | 0.000 / 0.000 mm | ≤ 0.5 ✓ |
| Upper posterior thigh radius | −1.83% / −1.48% | ≥ −3% ✓ |
| Arms, torso (05AI), lower legs, thigh < 62 cm | 0.000 mm | 0.000 ✓ |
| Genital, perineal, head, hands, feet | 0.000 mm | 0.000 ✓ |

**Buttock depth:**
- The mean posterior buttock movement (z 90–110 cm, |x| > 6 cm) is **4.7 mm**. For comparison, AR1r was about 7.3 mm.
- The older "200 most-posterior points" depth metric reads −0.04/−0.21 mm. It samples the medial strip next to the tail, which Mask A deliberately holds still to keep the tail-root blend, so it no longer represents the buttock belly. It is reported for continuity only.
- The visual gate governs (§10).

## 7. Visual gate (`views/final_*.jpg`; AO2 | AR1r | AS-predicted | AT final)

| Requirement | Result |
|---|---|
| Posterior softened like AR1r: no longer two hard bodybuilder globes, still substantial | ✓ (`final_close_B`, `final_body_B`) |
| Lower-glute fold soft and continuous | ✓ |
| No AR1r lateral / front-thigh stripe in front or 3/4 view | ✓ (`final_close_34`, `final_body_F`) |
| Tail root blends smoothly; no jagged plateau | ✓ (`final_tailroot_B`) |
| Profile natural, no lateral crease | ✓ (`final_close_P`, zoom `zP_AT.jpg`) |
| Pelvis broad; posterior thigh robust | ✓ |

The old faint horizontal thigh seam line visible in AO2 profile is softened in AT.

**Q1/Q2 pre-review sheet:** `views/Q1Q2_prereview_GO-05AT_AC3.jpg` (whole body F/P/B/3-4).

## 8. Disclosures

- Stage A real band maximum was 13.5° on one sliver edge, over the 12° Stage-A target (§3). The final state is 12.2°, within the final 20° gate.
- The deflate-only intermediate file was overwritten (§3).
- No geometry repair was used. All protection came from the masks.
- One primary sequence was authored, with no rerun.

## 9. State

Stop here per §14. Gorrund UNACCEPTED pending Tyler's visual review; Grask E3 FROZEN; RM-OT-05 OPEN; Stage C BLOCKED. No LOW, blind final acceptance or scaffold. No D4, UE5, production rigging or creator implementation.

Scripts are in `tools/rac/w1/rmot05at_drivers/` (`atmask.py`, `stageA.py`, `stageB.py`, `refineA2.py`, `sweepA.py`). The 05AN, 05AQ, 05AR and 05AS tools were reused.
