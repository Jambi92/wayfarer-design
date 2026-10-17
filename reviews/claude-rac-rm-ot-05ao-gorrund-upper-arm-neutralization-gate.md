# RAC RM-OT-05AO — Gorrund upper-arm neutralization: return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05ao-gorrund-upper-arm-neutralization-order.md` (4f6540a)
**Base:** `GO-05AN_AN1.blend` (sha `f058e439…d531`), accepted by the author as the partial AC2 base (face 224765 = CRIMP_RESOLVED).
**Executor:** Claude. Filters were authored in the Blender 5.2.2 UI on Tyler's PC. Cloud scripts were used for the mask attribute, simulation, bounded repair, gates and evidence.

## Verdict

**05AO AC2 PASS / READY FOR AC3 DECISION**

Frozen AC2 output:

| File | sha256 | Note |
|---|---|---|
| `GO-05AO_AC2.blend` | `ba129999cfe71c1ab7afc2f11c1b911bd1e85fc06f301e1bad9a483fcba4f6f3` | identical bytes to `GO-05AO_AO2.blend` |
| `GO-05AO_AC2.glb` | `1f60fb33fa0c75c9d0f9aa0c1315143005473fd5c72ada67ad922782240de434` | |

**Filter sequence from AC1 to AC2:**
1. 05AL AK1: Surface Smooth, one application.
2. 05AN AN1: Smooth Mesh Filter, 100 events, whole-limb feathered mask.
3. **05AO AO2: Smooth Mesh Filter, 180 events, upper-arm-only mask.**

Each step was preceded by the bounded predictive repairs documented in its gate. AC3 was not started.

## 1. Upper-arm mask

The order asks for an upper-arm-only mask with no hard edge through a belly.

**Why box masks could not do it:** in every view, the inner upper arm overlaps the hard torso core in X (05AN finding), so a box cannot separate them. The order's "hide the torso" UI route would need a weight-threshold selection that Blender does not offer: every upper-arm vertex also carries a non-zero trunk or forearm weight.

**What I did:** I built the mask from the rig's dominant-weight regions by vertex ID (`armmask.py`). This follows the 05AL §3 precedent of transferring and rebuilding masks by shared vertex ID. Only the `.sculpt_mask` attribute was written; the geometry is unchanged (0.000 mm, verified).

- **Sculptable:** upper-arm-dominant vertices only.
- **Hard (mask 1.0):** everything else (torso, shoulder/trunk, forearms, hands, legs, head, tail, pelvis).
- **Inside the arm:** the mask ramps from 1.0 at the shoulder, armpit and elbow boundaries to about 0.1–0.2 mid-belly. The ramp comes from a 300-iteration graph diffusion, so no hard edge crosses a muscle belly (`views/ao_masks.jpg`).

**Read-back (v1; `checks/ao_mask_v1_readback.json`):**

| Check | Result |
|---|---|
| all 05AF protected sets; 05AI torso / glute / pelvis_other | min 1.0 |
| elbow joint centres | 0.75 / 0.78 |
| upper-arm sculptable share | 0.75 |
| forearm / thigh / shin sculptable share | 0.0 |

**Clearance prep (§5) was not used.** The simulation showed 0 self-intersections between the arm and the torso. The instability turned out to be folding inside the arm's own surface, not contact with the torso.

## 2. AO1 — failed checkpoint, then one bounded rerun

**Prediction.** The calibrated Smooth model (1 event = 1 Laplacian iteration; 05AN calibration corr 0.991) sized the step at about 200 events:
- upper-arm radius L −3.2 % / R −6.0 %;
- forearms untouched;
- 0 self-intersections.

**Bounded repair before AO1** (`checks/ao_prep_repair_log.json`, `checks/ao_prep_gates.json`):

| Item | Result |
|---|---|
| neighbourhoods | 4 + 2 + 2 = 8 |
| vertex moves | ≤ 0.5 mm |
| rotations | 50 |
| faces changed | 86 |
| movement outside the union | 0.000 mm |
| patch deviation | 0.22 / 0.50 mm |
| changed faces folded > 60° against their 1-ring | 0 |
| distance from the changed faces to the torso core | ≥ 27 mm |

The prep gate's nearest-surface "inverted" heuristic reported 10 faces. I checked them topologically: all sit at most 58° from their local 1-ring, so none is folded.

**AO1 result:** `GO-05AO_AO1.blend` (190 events, sha `2fd6702b…aa4c`) produced **10 flipped faces against the preceding state**. They were at the inner left upper arm (X ≈ 23.4 cm, z 145–155 cm) and are a real fold of the arm's own surface. My pre-AO1 predictor had wrongly dismissed these surface-reorientation flags. The simulator does reproduce them (8 of 10 overlap). **AO1 is REJECTED** (`checks/ao1_rejected_gate.json`; `05AO/GO-05AO_AO1_REJECTED.glb` kept as evidence).

**Rerun of the same step.** I went back to the pre-filter state `GO-05AO_AO1_prep`. The geometry was not changed. Only the mask was raised, with 1–3 cm feathered protection discs (25 sites, 2 559 vertices) around every simulated fold site; real AO1 flip sites were added as well. That mask is v3 (`refine.py`, `checks/ao_mask_v3_readback.json`). The simulation then predicted 0 flips, 0 new local inversions and 0 new folds over 60°, at both 190 and 230 events. The file is `GO-05AO_AO2_prep.blend` (sha `3f29c344…05ad`).

## 3. AO2 — Smooth Mesh Filter, 180 events (authored, PASS)

**UI settings:**

| Setting | Value |
|---|---|
| Tool | Mesh Filter |
| Filter Type | Smooth |
| Strength | 1.000 |
| Deform Axis | X Y Z |
| Orientation | Local |
| Application | one drag: mouse down, 10 ramp moves, 170 small moves, mouse up = 180 events |

The checkpoint is `GO-05AO_AO2.blend`.

### Gate (`checks/ao2_gate.json`)

| Gate | Result |
|---|---|
| seams / SI / **flips** / degenerates vs the preceding state | 0 / 0 / **0** / 0 |
| topology | 1 / 0 / 0 |
| head, tail, tail junction, genital, perineal, hands, feet; 05AI torso / glute / pelvis_other | **0.000 mm** |
| legs (thigh, shin, foot labels) vs AN1 | 0.000 mm |
| forearm-L vs AN1 | 0.000 mm |
| forearm-R vs AN1 | 0.5 mm (bounded-repair vertices only) |
| trunk-labelled vertices outside the torso core vs AN1 | 0.5 mm (bounded repair) |
| upper-arm mean radius from 05AL | **L −3.61 % / R −6.51 %** (allowed ≥ −8 %) |
| forearm mean radius | −1.91 % / −1.51 % (allowed ≥ −3.5 %), unchanged from AN1 |
| elbow (upper-arm/forearm) joint-centre drift | 0.42 / 0.41 mm (ceiling 0.75) |
| shoulder joint | inside the hard trunk region, so 0 |
| stature / bbox | unchanged |
| cumulative limb displacement from 05AL | median 3.70, p95 9.39, max 18.2 mm |
| AO2 incremental | median 4.28, p95 9.11, max 14.9 mm |
| orientation vs 05AL | only face 224765, CRIMP_RESOLVED (as ruled) |
| local inversions | 2 now vs 4 in the baseline |

### Visual gate (`views/ao2_cmp_*.jpg`, at identical cameras across 05AI AC1 | 05AN AN1 | 05AO AO2)

Covered: whole F / P / B / 3/4, body-only F / P / B / 3/4, arms front and 3/4, each arm in profile, thighs and calves.

**Arms:**
- **Biceps peak:** gone in front and 3/4. The arm reads as a broad, rounded upper arm.
- **Triceps:** bulge and biceps–triceps groove clearly reduced in profile.
- **Silhouette:** no longer bodybuilder.
- **Shoulder caps:** still broad (protected).
- **Elbows:** still large.
- **Forearms:** unchanged from AN1.
- **Whole body:** now reads as large-frame, ordinary-untrained, with arms in harmony with the neutralised legs and the AC1 torso.
- **No defects:** no skinny read, armpit collapse, torso/arm gap or dents.

**Residuals for author / Tyler review:**
- **Elbow line:** a faint transition line remains around the top of each forearm at the elbow mask ramp. It is visible in close profile and is mild.
- **Thigh-top line:** the faint AN1 thigh-top line remains. The optional §10 continuity touch was **not** used, because a brush touch risks a stroke shelf, which is the failure mode of 05AJ.

Both could be addressed by a single tiny continuity touch each in a follow-up, if wanted.

## 4. Files

On the PC, in `RaceBodies/source/Gorrund-Neutral-C/05AO/`:

| File | Status |
|---|---|
| `GO-05AO_AC2.blend` / `.glb` | **frozen AC2** |
| `GO-05AO_AO2.blend` | passing checkpoint (same bytes as AC2) |
| `GO-05AO_AO2_prep.blend` | refined mask v3 |
| `GO-05AO_working.blend` | AN1 + mask v1 |
| `GO-05AO_AO1_prep.blend` | bounded repair |
| `GO-05AO_AO1.blend` / `GO-05AO_AO1_REJECTED.glb` | rejected, evidence only |
| `05AO_README.txt` | marks the folder |

Scripts are in `tools/rac/w1/rmot05ao_drivers/`: `armmask.py`, `ao_repair.py`, `refine.py`. The 05AN driver set (predictor, gate, metrics) was reused.

Blender was closed (both of my instances).

## State

**Gorrund UNACCEPTED** until composition, Q1/Q2 and Tyler visual acceptance. **Grask E3 FROZEN; RM-OT-05 OPEN; Stage C BLOCKED.** No LOW, no blind final acceptance, no scaffold, no D4/UE5/rigging/creator work. AC2 is complete; AC3 awaits the author's decision.
