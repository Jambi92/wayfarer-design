# RAC RM-OT-05AM — controlled AC2 filter buildup: return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05am-gorrund-ac2-controlled-filter-buildup-order.md` (a23fc10)
**Source:** `GO-05AL_AK1.blend` (sha256 `a2336442…37cc`, verified). Its saved mask was read back first: all protected sets and the 05AI torso/glute/pelvis_other are at 1.0, and geometry matches 0.000 mm (`checks/ak1_mask_readback.json`).

## Verdict

**05AM AC2 CONTROLLED BUILDUP NOT CREDIBLE / STOP — author ruling required on the displacement limits**

- The active AC2 checkpoint stays **`GO-05AL_AK1`** (05AL stability pass).
- The passed 05AI AC1 torso is preserved inside it.
- AC3 was not started.

Two findings drive the stop.

1. **AM1 failed the technical gate with one flip.** The AM1 Surface Smooth was authored with 0 predicted flips, yet the real checkpoint flipped **1 face (202188)** against the 05AL baseline. My predictor had judged flips against the start of the step instead of cumulatively against the frozen baseline (§2). I fixed the predictor and used the one allowed bounded repair. The repaired candidate now predicts 0 flips (§3).
2. **The visual target cannot be reached within this order's displacement limits** (§4). A calibrated simulation of the authorised AM2 Smooth filter shows:
   - **At the AM2 limits** (median ≤ 0.6, p95 ≤ 1.8, max ≤ 4.0 mm incremental), and even with the AM3 cumulative ceiling (p95 ≤ 6, max ≤ 10 mm), the limbs are visually unchanged from AC1.
   - **A clearly softened AC2 read appears only at about 7 mm median, 18 mm p95 and 28 mm max** cumulative displacement, roughly 3× the AM3 ceiling.

   Running AM2/AM3 would use up the three-filter budget on a predictable visual fail, so I stopped before authoring them. That limit is the author's to change, not mine.

## 1. AM1 — Surface Smooth on GO-05AL_AK1 (authored, then failed the gate)

**Prediction before authoring** (step-relative, as in 05AL): 0 flips and 0 adjacent > 60° faces, for both AM1 and the 2× stress case. Predicted incremental displacement was median 0.126 mm, p95 0.353, max 1.36. The watch-list faces were tracked (`checks/am1_prediction_step_relative.json`).

**UI settings, identical to 05AL AK1:**

| Setting | Value |
|---|---|
| Tool | Mesh Filter |
| Filter Type | Surface Smooth |
| Strength | 1.000 |
| Deform Axis | X Y Z |
| Orientation | Local |
| Shape Preservation | 0.500 |
| Per Vertex Displacement | 0.500 |
| Application | one 200 px drag |

The file was opened from the PC copy of GO-05AL_AK1, filtered, and saved as `05AM/GO-05AM_AM1.blend` (sha256 `4481f779…27c4`).

### Gate (`checks/am1_real_gates.json`, `checks/am1_real_extra.json`)

| Gate | Result |
|---|---|
| seams / SI / degenerates | 0 / 0 / 0 |
| position-welded components / boundary / non-manifold | 1 / 0 / 0 |
| protected regions; 05AI torso, glute, pelvis_other | 0.000 mm |
| stature | unchanged |
| joint-centre drift | ≤ 0.002 mm |
| mean limb radius | unchanged (≤ 0.003 %) |
| displacement | incremental median 0.128 mm, p95 0.357, max 1.29 (exactly as predicted); cumulative from 05AL: median 0.40, p95 1.18, max 4.29 |
| **flipped faces** | **1 — FAIL**: face 202188, left forearm/elbow, z 125 cm |

**How face 202188 failed:**
- In the 05AL baseline it lay 7° from its 1-ring surface.
- After AK1 it had drifted to 44°.
- After AM1 it reached 106°: a genuine progressive inversion.

Within the AM1 step alone it rotated only 62°, so a step-relative predictor could not see it. Measured cumulatively, the replica predicted 77° against the real 99°.

`GO-05AM_AM1.blend` is **rejected**, evidence only. Per §8 the active checkpoint reverted to GO-05AL_AK1.

## 2. Predictor correction (`tools/rac/w1/rmot05am_drivers/predict3.py`)

The new predictor judges every face **cumulatively against the frozen 05AL baseline** (the gate reference). It flags:
- flips (normal dot < 0);
- a **> 60° normal-rotation margin**, which catches 202188;
- > 60° folds adjacent to either of those.

It does this for the proposed step and for the 2× stress case.

**Rotated triangles:** a triangle created by an edge rotation has no counterpart in the baseline, so its reference normal is taken from the repaired checkpoint itself. Judging such a triangle against baseline positions produced a spurious "flip" (face 613370 sits at 2.9° to its local surface). The repair log shows that artefact as non-convergence in cycles 2–4.

## 3. One bounded repair of the AM1 step (§8 authority; `checks/am_repair_log.json`, `checks/am_repair_gates.json`)

| Item | Result |
|---|---|
| source | GO-05AL_AK1 |
| method | 05AL method: Laplacian half-steps on flagged-face vertices, capped 0.5 mm from **this checkpoint**, plus 05AI-condition edge rotations |
| repair cycles | 3 (limit 3) |
| neighbourhoods | 12 + 5 + 3 = **20** (budget 40) |
| vertices moved | 40 |
| edge rotations | 111 |
| faces changed | 191, all inside the union (403 vertices) |
| movement outside the union | **0.000 mm** |
| max move | 0.5 mm |
| patch deviation | 0.394 / 0.438 mm |
| SI / degenerates / inverted vs local surface / duplicates | 0 / 0 / 0 / 0 |
| topology | 1 / 0 / 0 |
| protected regions; 05AI torso, glute, pelvis_other | 0.000 mm |
| stature / bbox | unchanged |
| patch folds > 60° | 15 → 9 |

**Corrected prediction on the repaired state:**
- AM1 step: **0 flips**.
- 2× stress (8 sequential applications): **0 flips**.
- Two faces (224765, 549805) stay above the 60° margin. They plateau at 73° and 69° under stress and sit 11° and 1° from their local surface, so they are stable, not inverting.

**Pre-existing defect:** face 262682 (watch-list) is an inverted micro-crimp that was already present (102° to its local surface). Smoothing *reduces* it to 73°.

**Candidate file:**
- `05AM/GO-05AM_AK1_predictive_repair.blend`, sha256 `cc3adee1a9d37c9faf55a742f47346a3702365ab389ed63a33b74a8dec522a24`.
- It is a **candidate baseline only**. I made no AM1 rerun on it, because §4 shows the order's remaining budget cannot deliver AC2.

## 4. Feasibility of the visual target (diagnostic only; `views/feas_*.jpg`)

**Smooth filter replica:** `smoothsim.py` reproduces Blender's Mesh Filter **Smooth**. Every modal mouse-move event re-applies `co = orig + fade·(avg(current neighbours) − orig)` with fade clamped to ±1, so each event acts as one Jacobi smoothing iteration. Starting from the predicted AM1 rerun state with the saved mask:

| Smooth events | Incremental median / p95 / max (mm) | Cumulative from 05AL |
|---|---|---|
| 5 | 0.41 / 1.12 / **4.47** | 0.68 / 1.94 / 7.9 |
| 20 | 0.60 / 1.58 / 6.26 | 0.82 / 2.25 / 9.0 |
| 80 | 0.85 / 2.11 / 7.31 | 1.02 / 2.65 / **9.7** |
| ~420 | — | **6.99 / 17.9 / 28.4** |
| ~1620 | — | 13.3 / 40.9 / 56.2 |

On this roughly 2 mm-edge, 1 M-face mesh, smoothing spreads only about edge-length × √iterations. The heroic forms are 5–10 cm wide and 1–2 cm deep. The renders compare AC1 against three simulated states at identical cameras: whole front, arms, calves profile/back, and thighs (`views/feas_*.jpg`).

| Simulated state | What the renders show |
|---|---|
| **Within the 05AM limits** (AM1 + AM2 up to max ≈ 4.5 mm incremental) | Visually indistinguishable from AC1. |
| **~420 iterations** (≈ 3× the AM3 p95 ceiling) | The quad channels and teardrop are essentially gone; the calves and biceps are clearly softer, and the joints are still large. This is close to the AC2 read. It also shows **hard mask-box edge steps** at the upper-thigh/hip box and the shoulder-top box, plus mild Laplacian slimming. |
| **~1620 iterations** | Over-smoothed mannequin with large steps at the mask boundaries. |

## 5. Recommendation for the next order

1. **Re-scope the AC2 displacement ceilings to the measured need.** For example, cumulative limb p95 around 15–18 mm and max around 30 mm, with an explicit limb-radius preservation gate (mean radius change ≥ −3 %) so the larger movement softens forms without slimming.
2. **Replace the hard thigh/hip and shoulder-top mask box edges with feathered transitions** before any large filter. Shape them in the UI and feather them before the final hard masks, keeping the torso/pelvis at 1.0 via the regions_05AI sets. This removes the boundary steps the simulation shows.
3. **Prefer a volume-preserving route.** For example, alternate Smooth iterations with an Inflate correction, or use Surface Smooth with high shape preservation over many events. The new replicas (`smoothsim.py`, `dryrun.py`) let the author tune these numerically before any authoring.
4. **Start from `GO-05AM_AK1_predictive_repair.blend`,** which has 0 predicted flips for the next Surface Smooth step. Keep the cumulative-reference predictor (`predict3.py`) as the pre-author gate.
5. **Use multi-event drags.** Large Smooth amounts will need many events, which can be scripted as a press, many small moves, then release in the UI. They remain UI-authored.

## 6. Files

On the PC, in `RaceBodies/source/Gorrund-Neutral-C/05AM/`:

| File | Status |
|---|---|
| `GO-05AM_AM1.blend` | **REJECTED**, 1 flip |
| `GO-05AM_AK1_predictive_repair.blend` | candidate baseline |
| `05AM_README.txt` | marks the folder |

`05AL/GO-05AL_AK1` stays active and unchanged.

Scripts are in `tools/rac/w1/rmot05am_drivers/`: `predict3.py`, `am_repair.py`, `smoothsim.py`, `amcheck.sh`, `amextra.py`.

Blender was closed after the work.

## State

**Gorrund UNACCEPTED; Grask E3 FROZEN; RM-OT-05 OPEN; Stage C BLOCKED.** No LOW, no blind final acceptance, no scaffold, no D4/UE5/rigging/creator work. AC2 is incomplete; the active AC2 checkpoint is GO-05AL_AK1.
