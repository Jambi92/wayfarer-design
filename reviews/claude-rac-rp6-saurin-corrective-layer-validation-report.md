# Saurin RP6 — creator-state corrective layer validation report

Order: [chatgpt-rac-rp6-saurin-corrective-layer-validation-order.md](chatgpt-rac-rp6-saurin-corrective-layer-validation-order.md) (3e76b509)
Status: **RP6 RIG PILOT / NOT FROZEN**

## Verdict

**NOT PASS: gates remain open for use between states. Escalated for an author decision.** The pass line is not submitted.

- **What passes:**
  - The layer package rebuilds exactly from disk.
  - Every endpoint identity is exact.
  - Every accepted body passes all gates at 25 / 50 / 75 / 100 % of all 34 poses: both base controls and all 19 states, after the layer-v002 refit described below.
  - The plain linear blend passes on the narrow, broad, LT90 and NAR→BRD paths at w = 0.25 / 0.50 / 0.75.
- **What fails:**
  - On the tissue paths (MUHI, FAHI, MUFAHI) and, mildly, on T80, M208-B and F-N, the proposed linear blend leaves rig-owned folds, tears or contact on intermediate bodies.
  - Bounded layer fixes (creator-weight keys) make every *fitted* weight pass, but bodies *between* fitted weights still fail.
  - A dense scan shows failures at 6.25 % muscle+fat, where the production corrective is still 94 % base.
- **Diagnosis:** the corrective representation is a fixed rest-space offset fitted to one exact body. It does not transfer to nearby creator bodies on the heavy-tissue paths, and adding more knots does not converge.
- **Decision needed:** choosing the representation or workflow (see *Options*) is an author decision outside this order.

## 1. Package and harness

| Item | Result |
|---|---|
| Packaging defect 1 | `SA_RP6_correctives_v001.json` had no pose-key driver metadata: c1 has 7 base pose keys, c2 has 8. Fixed by `SA_RP6_correctives_v002.json`, with byte-identical arrays. |
| Packaging defect 2 | `SA_RP6_creator_layers_v001.json` had no family or pose-key metadata, so the sets could not be rebuilt without the fitted files. Fixed by `SA_RP6_creator_layers_v002.json`. |
| Rebuild from package only | `sa6_layer_harness.py` (B, S_i and the blend). |
| Identities | `layer_validation/SA_RP6_layer_identity_v001.json` (v002) and `SA_RP6_layer_identity_v004.json`, both all-exact. Each checks that manifest hashes match, that the base rebuilt equals production (keys and delta(T), max diff 0.0), and that every state rebuilt equals its fitted set (0.0). It also checks Blend(B,{}) = B, Blend(B,{S:1}) = S, Blend(B,{S:0}) = B, and neutral = 0.0 for B, every S and every blend. |
| Harness = closure audit | END_MUHI reproduces `pd2_final` on all 34 poses with 0 mismatches. |

Blend rule implemented (header of `sa6_layer_harness.py`):

> production = (1 − Σw) B(T) + Σ w_i S_i(T, w_i)

- **Evaluation:** every set is evaluated on the blended body's own joint frames, with dense accumulation, before LBS. The base is counted once.
- **Key handling:** inherited keys cancel exactly. A changed sample alters the interpolation only inside S_i. New samples and pose keys enter at w_i × their own driver weight.
- **Creator keys (layer v003+):** S_i(T, w) = S_i(T) + Σ h_n(w) K_n(T). Here h_n is a hat over the knots 0 < w_n < 1, equal to zero at w = 0 and w = 1. The endpoint, zero-influence and neutral identities therefore stay exact.

## 2. Bodies and method

- **Geometry:** convex blend of the dense accepted creator bodies, VB = (1 − Σw) VB_base + Σ w_i VB_i, using the same weights as the corrective blend.
  - The frozen cage is placed through the frozen barycentric embedding.
  - Joints come from the RP6 landmark transfer.
  - Weights are the base configuration's production weights.
  - Bodies are listed in `layer_validation/SA_RP6_blend_bodies_v001.json`, with weights, pre-rig folds and hashes.
- **Coverage:**
  - Controls: BASE_c1 and BASE_c2.
  - 19 endpoints.
  - Base→extreme on c1: MUHI, FAHI, MUFAHI, NAR, BRD, T80, LT90 and M208-B at 0.25 / 0.50 / 0.75. Held-out weights 0.375 / 0.625 on the five paths that carry creator keys.
  - c2→F-N at 0.25 / 0.50 / 0.75.
  - Two-layer paths: MUHI–FAHI, NAR–BRD, FAHI–MUFAHI and T55–T80.
  - Mixes: MIX1 (MUHI .4, FAHI .3, BRD .3) and MIX2 (NAR .3, FAHI .3, T80 .3, base .1).
  - Every body runs the anatomical 34-pose suite at 25 / 50 / 75 / 100 %. Each pose produces three columns: plain LBS, base only, and production.
- **Gates:** unchanged closure gates and ownership rules (`sa6_blend.py` header):
  - rig folds, new contact and tears (> 2.5× and > 0.75 cm) count as failures;
  - |dV| > 100 cm³ fails, except on jaw poses;
  - rigid set ≤ 0.05 cm;
  - neutral displacement must be 0.
- **Steering scan:** `sa6_path_scan.py` runs each path at 1/16 creator-weight steps. It covers only the poses that ever failed on that path, at all four fractions, with the same evaluator and rules. It is a steering tool, not a gate.

## 3. Layer revisions within the order

| Package | Change | Why |
|---|---|---|
| v002 (metadata) | The packaging fixes in §1 | Rebuild from the package |
| v003 | (a) State layers re-solved at 100 / 75 / 50 / 25 %, starting from the accepted layers (`FRACS=1.0,0.75,0.5,0.25`). All 19 converge. (b) Creator keys at w = 0.50 on 9 paths (`sa6_node_fit.py`; empty where the linear blend already passed). | (a) END_BRD and END_B-T80 failed at 75 % / 25 % because the layers had only been fitted at 100 / 50 %. (b) The linear blend failed on intermediate tissue bodies. |
| v004 | Creator keys added at 0.25 and 0.75 on MUHI, FAHI, MUFAHI, T80 and M208-B, and at 0.25 on F-N. All knots converge. Guarded solver: a solve that worsens its pose is reverted, and a local fade fallback is re-verified on the whole suite. | v003 still failed at 0.25 / 0.75 |
| v005 (not packaged) | Composite knots: a knot inserted between existing knots starts from their interpolation. MUHI@0.375, 0.625 and 0.875 and FAHI@0.375 converged. | Held-out 0.375 / 0.625 failed. Stopped when the scan showed the failures do not converge (§5). |

## 4. Results

### Endpoints and controls (layers v003 = v004 at w = 1; `eval_layers_v003/`)
All 21 bodies are **clean** at 25 / 50 / 75 / 100 % of all 34 poses: BASE_c1, BASE_c2 and END_* × 19. There are 0 rig folds, 0 rig contacts, 0 rig tears and 0 volume misses. Neutral displacement is 0.0. Maximum rigid movement is 0.0013 cm (END_MUFAHI).

### Paths with the plain linear blend (`eval_layers_v003/`)
| Path | w = 0.25 | 0.50 | 0.75 |
|---|---|---|---|
| c1→NAR | clean | clean | clean |
| c1→BRD | clean | clean | clean |
| c1→LT90 | clean | clean | clean |
| NAR→BRD | clean | clean | clean |
| c2→F-N | 1 rig contact, at elbow_130_xneg 100 % | clean | clean |

### Paths that needed creator keys (`eval_layers_v002/`, `v003/`, `v004/`)
Each cell lists rig folds / contact / tears / volume misses, summed over 34 poses × 4 fractions.

| Body | layers v002 (linear) | v003 (knot 0.5) | v004 (knots .25 / .5 / .75) |
|---|---|---|---|
| c1-MUHI@0.25 | 3/0/0/1 | 1/0/0/0 | clean |
| c1-MUHI@0.375 (held out) | – | – | **1/0/0/0**: shoulder_abd90_xneg 100 % |
| c1-MUHI@0.50 | 3/0/0/3 | clean | clean |
| c1-MUHI@0.625 (held out) | – | – | **2/0/0/0**: shoulder_abd90_xneg 75, 100 % |
| c1-MUHI@0.75 | 0/0/0/3 | 1/0/0/0 | clean |
| c1-FAHI@0.25 | 7/5/0/2 | 4/3/0/0 | clean |
| c1-FAHI@0.375 (held out) | – | – | **5/0/0/0** |
| c1-FAHI@0.50 | 15/0/0/3 | clean | clean |
| c1-FAHI@0.625 (held out) | – | – | **5/0/0/0** |
| c1-FAHI@0.75 | 26/0/0/2 | 22/0/0/0 | clean |
| c1-MUFAHI@0.25 | 14/5/0/1 | 10/3/0/0 | clean |
| c1-MUFAHI@0.375 (held out) | – | – | **5/0/0/0** |
| c1-MUFAHI@0.50 | – | – | clean |
| c1-MUFAHI@0.625 (held out) | – | – | **18/0/0/0** |
| c1-MUFAHI@0.75 | – | – | clean |
| c1-T80@0.25 / 0.50 / 0.75 | – | 0/0/3/0, –, 1/0/0/0 | clean, clean, clean |
| c1-T80@0.375 (held out) | – | – | **0/0/1/0**: hip_flex70_xpos 100 % |
| c1-M208-B@0.25 / 0.50 / 0.75 | – | 0/2/0/0, –, 2/0/0/0 | clean, clean, clean |

Not evaluated at v004:
- M208-B held-out 0.375 / 0.625 (see the scan below);
- c2-F-N with its 0.25 knot;
- the two-layer paths MUHI–FAHI, FAHI–MUFAHI and T55–T80;
- MIX1 and MIX2.

Each of these involves a path whose layer is still open, so its result would not be final.

### Dense scan, layers v004 (`scan_v004/`, 1/16 steps, failing-pose subset)
Rig defects per body (folds / tears) over the scanned poses × 4 fractions:

| w | MUHI | FAHI | MUFAHI | T80 | M208-B | F-N |
|---|---|---|---|---|---|---|
| 0.0625 | 0 | 0 | **1** | 0 | SCAN_M208_0625 | SCAN_FN_0625 |
| 0.125 | 0 | 0 | 0 | 0 | SCAN_M208_125 | SCAN_FN_125 |
| 0.1875 | 0 | 0 | 0 | **1 t** | SCAN_M208_1875 | SCAN_FN_1875 |
| 0.3125 | **1** | **2** | **8** | **1 t** | SCAN_M208_3125 | SCAN_FN_3125 |
| 0.375 | **1** | **5** | **3** | **1 t** | SCAN_M208_375 | SCAN_FN_375 |
| 0.4375 | **1** | **4** | **5** | 0 | SCAN_M208_4375 | SCAN_FN_4375 |
| 0.5625 | 0 | **2** | **6** | 0 | SCAN_M208_5625 | SCAN_FN_5625 |
| 0.625 | **2** | **5** | **13** | 0 | SCAN_M208_625 | SCAN_FN_625 |
| 0.6875 | **1** | **14** | **9** | 0 | SCAN_M208_6875 | SCAN_FN_6875 |
| 0.8125 | 0 | **18** | **20** | 0 | SCAN_M208_8125 | SCAN_FN_8125 |
| 0.875 | **2** | **12** | **22** | 0 | SCAN_M208_875 | SCAN_FN_875 |
| 0.9375 | 0 | **19** | **19** | 0 | SCAN_M208_9375 | SCAN_FN_9375 |

The knots at 0.25 / 0.50 / 0.75 and the endpoint at 1.0 are clean on every path, as shown above.

## 5. Diagnosis

1. **Base corrective near the base body.**
   - The c1 base corrective folds a pelvis quad in trunk_twist_30 at 100 % on the MUFAHI@0.0625 body. The base-only column shows 2 folds; production, still 94 % base, shows 1.
   - On BASE_c1 the same pose is clean, and no quad is within 0.02 of folding (`layer_validation/SA_RP6_layer_margin_v004.txt`, tool `sa6_layer_margin.py`: 0 quads with relcos < 0.1 for that pose).
   - So a 6 % move in tissue changes the local geometry enough that the fixed rest-space offset overshoots.
   - Close-up: `renders/SA_RP6_layer_c1-MUFAHI_0p0625_trunk_twist_30_100.png`.
2. **Heavy-tissue paths.**
   - On FAHI and MUFAHI near w = 1 (0.8125–0.9375) most production folds are composition-owned. Example: FAHI@0.9375 hip_flex70_xneg 100 % has 30 folds, 28 of them composition.
   - 1–2 quads per pose fall outside the closure ownership because the pre-rig crease zone moves with w (FAHI@0.9375 has 714 composition quads, END_FAHI 787). Those quads are folded by the corrective and not by LBS, so they are rig-owned under the rules.
   - The accepted END_FAHI and END_MUFAHI fits are exact for their own crease layout only.
   - Close-ups: `renders/SA_RP6_layer_c1-FAHI_0p8125_trunk_twist_30_075.png` and `renders/SA_RP6_layer_c1-MUFAHI_0p625_shoulder_abd90_xneg_050.png`.
3. **Knots do not converge.**
   - Every knot fit converges: 21 knots in v004/v005, all at 0 open defects on the full suite.
   - But defects reappear between knots at every spacing tried (1/2 → 1/4 → 1/8).
   - On MUHI the defects are always the same single shoulder_abd90 quad, from 0.3125 to 0.875.
   - On FAHI and MUFAHI they grow toward w = 1.
   - Composite knots that start from the neighbours' interpolation keep the knots consistent but cannot remove the cause.
4. **What is not the cause:**
   - packaging (the identities are exact);
   - the blend algebra (it reproduces the endpoints exactly);
   - poses or driver ranges (endpoints pass at all fractions);
   - geometry (no topology-owned defects).

## 6. Options for the author decision

| Option | What it means | Cost / scope |
|---|---|---|
| A. Bake per body at creator commit | When a body is finalised, run the existing PD-2 layer solver on that body, starting from the blended layer. | Uses the solver already proven here: 19 states plus 21 knot bodies all converged at all fractions. About 10–45 min per body on 1 core. Needs creator / bake implementation, which is outside this order. |
| B. Restrict the creator to validated presets and paths | Allow only accepted states and the validated knot weights, with linear paths only where proven: NAR, BRD, LT90, NAR→BRD. | No new technology. It limits freedom between states. |
| C. Body-relative corrective representation | Express the deltas in local surface frames scaled by local tissue thickness or body measurements, so one key adapts to nearby bodies. | Research and refit of base + layers; re-runs RP6 closure. |
| D. Robust refit with a safety margin | Refit base and layers so folds must clear a relcos margin and must hold across a neighbourhood of bodies (multi-body fit). | Changes the accepted c1 / c2 correctives; RP6 closure re-run; may not cover the crease-edge cases (§5.2). |

Recommendation: decide between **A** (full creator freedom; the proven solver runs at bake time) and **B** (ship presets now). **C** and **D** are longer research tracks.

## 7. Not run

- The driver-transition sweeps (`sa6_layer_sweep.py`) and the full worst-case render set were planned for the passing state. They were not run because the gates did not close.
- Endpoint driver continuity is unchanged from the accepted closure.

## 8. Evidence and reproduction

**Evidence** in `reviews/rac-rp6-evidence/saurin/rig_pilot/`:
- packages: `SA_RP6_correctives_v002.json`; `SA_RP6_creator_layers_v002/v003/v004.json` + `.npz`;
- under `layer_validation/`:
  - `SA_RP6_blend_bodies_v001.json`;
  - `SA_RP6_layer_identity_v001.json` (layers v002) and `SA_RP6_layer_identity_v004.json`;
  - per-body results in `eval_layers_v002/`, `eval_layers_v003/` and `eval_layers_v004/`;
  - `scan_v004/` (per-weight JSON);
  - `renders/`.

**Tools** in `tools/rac/rp/saurin_rp6_v001/`:
- `sa6_pkg_v002.py` and `sa6_pkg_v003.py` (`PKG_VER`);
- `sa6_layer_harness.py`, `sa6_layer_identity.py`, `sa6_blend.py`;
- `sa6_pd2_fit.py` (`FRACS`), `sa6_node_fit.py`, `sa6_node_fade.py`;
- `sa6_path_scan.py`, `sa6_layer_render.py`.

Commands (`SA_W` = the clean RP5 workspace; WORK = the RP6 work directory):

```
python3 sa6_pkg_v002.py WORK WORK/pd2fit
python3 sa6_blend.py bodies BODIES
FRACS=1.0,0.75,0.5,0.25 INIT_LAYER=WORK/pd2fit python3 sa6_pd2_fit.py <STATE> WORK/pd2fit_v2
python3 sa6_node_fit.py <STATE>@<w> BODIES WORK/pd2fit_v2 NODES
PKG_VER=v004 python3 sa6_pkg_v003.py WORK/pd2fit_v2 NODES_ALL
RP6_LAYERS=SA_RP6_creator_layers_v004.json python3 sa6_layer_identity.py BODIES OUT.json FITDIR
RP6_LAYERS=SA_RP6_creator_layers_v004.json python3 sa6_blend.py eval BODIES OUT <names|all>
python3 sa6_path_scan.py <STATE> M|F <weights> <poses> OUT SA_RP6_creator_layers_v004.json
RP6_LAYERS=SA_RP6_creator_layers_v004.json python3 sa6_layer_render.py OUT BODIES:NAME:POSE:FRAC ...
```
