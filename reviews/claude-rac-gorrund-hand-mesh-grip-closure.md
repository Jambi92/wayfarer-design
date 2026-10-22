# Gorrund hands — production mesh and grip validation: closure report

**Date:** 2026-10-22
**Order:** `reviews/chatgpt-rac-gorrund-hand-mesh-grip-completion-order.md`
**Executor:** Claude. This is self-inspection only; no independent acceptance is claimed.

**Result:** **HOLD.**
- **Production hand mesh: complete and verified.**
- **Movement and grip: partially complete.** The thumb tests and the left-hand handle grip do not pass. See §5.

The section is **not** complete under the order's own rule, because not every movement and grip check passes. Nothing has been frozen or promoted.

## 1. Inputs and protected files

| Item | State |
|---|---|
| Accepted visible reference | `outputs/Gorrund_Rounded_Fingertips_Review.blend` (rev 107), SHA256 `cdc9e3a9…9179`. Unchanged; read only. |
| Frozen production | `GO_U_REF_RP1F_refine_v015.blend`, SHA256 `dfba363e534359193c63dc1700eb54d80f2ee34dbfa3a3cad06b5f87943e5e75`. Verified before and after; unchanged. |
| Manual cage | `work/Gorrund_manual_hand108.blend` (cage `Gorrund_left_hand_MANUAL_CAGE`, 146 vertices / 144 faces). Not edited; see §2. The Blender window that had it open was left alone. |
| Native height | 204.51981985 cm. Production stature delta vs rev 107: 0.000 mm. No rescale. |
| Unreal / Turnfall / other races | Untouched. |

## 2. Construction method (read this first)

The production topology is **not** a new generator output, and it does **not** use the 108 cage.

**What it is:** the accepted RP1E/RP1F v015 production quad mesh, which was built and accepted under M-B, refitted to the accepted rev 107 shape.

- **Outside the hands:** all 952 556 vertices are copied bit-exactly. Max difference: 0.000 mm.
- **Hand skin away from the fingertips:** vertex-only projection onto rev 107, using the v015 normals plus a light relax.
- **Ten fingertip patches:** each v015 disk patch is draped onto the matching fused claw-and-fingertip disk of rev 107. Steps:
  - a bijective parameter domain (mean-value embedding with stretch reweighting);
  - surface relaxation with a fold guard (area-equalising, Laplacian and square-shape targets);
  - the claw apex pinned;
  - local repair until there are no folds.

  The quad connectivity of each patch is unchanged.
- **One explicit topology change:** the distal R middle/ring tissue bridge. rev 107 separates it; v015 had it.
  - The bridge strip (230 quads) is cut at a minimum s–t cut.
  - Each side's hole is closed with a quad grid cap (92 × 92 and 90 × 90).
  - Grid corners sit on boundary vertices that already have two quads, so there are no valence-2 doublets.
  - The body therefore goes from **genus 1 (v015) to genus 0**, matching rev 107 (Euler 2).

**Why not the 108 cage:** it is a 144-face early blockout. Finishing it by screenshot clicking to production density was not credible inside this pass. Reusing the already accepted M-B topology keeps the established loop and density structure.

**Not used:** automatic remeshing and QuadriFlow.

**Blender UI:**
- The final mesh was imported through the UI on Tyler's PC: two PLY halves → Join → Merge by Distance 0.000001 m → rename → Save As.
- The saved file was then reopened in the cloud and checked against the cloud mesh: bijective, faces identical, max 0.00012 mm, identity transform.

This is a method substitution. It needs owner review before it can be called M-B-equivalent.

## 3. Production mesh gates (final mesh, saved file verified)

**File:** `work/claude109/Gorrund_hand_production109.blend`, SHA256 `ba668cce…090c`. Object `GO_hand_production109`.

### 3.1 Topology

| Check | Result |
|---|---|
| Vertices / faces | 1 443 272 / 1 443 270 |
| Quads | 100 % |
| Components | 1 |
| Boundary edges | 0 |
| Non-manifold edges | 0 |
| Directed-edge duplicates | 0 |
| Unused vertices | 0 |
| Coincident vertices | 0 |
| Degenerate quads | 0 |
| Min edge | 0.0023 mm (same as v015) |
| Euler characteristic / genus | 2 / **0** (rev 107 is genus 0; v015 was 1) |
| **Global self-intersections** | **0** (quad BVH) |

### 3.2 Face shape and loops

**T-4 face shape (quality target):**

| Mesh | Angles 45–135° | Aspect ≤ 4 |
|---|---|---|
| Production | 87.5 % | 95.4 % |
| v015 | 91.6 % | 96.4 % |

The drop is concentrated on the claws and claw roots, which are rigid keratin. R middle and R ring are the weakest digits: about 30 % of their fingertip quads are within the angle range, and the claw tips have dense sliver fans. **This is reported as a regression, not a pass.**

**T-5 loops and density:** inherited unchanged from v015. That means the L4 subdivision of the M-B cage, at about 0.56 mm median hand edge, well below the 6 mm (0.3 % of stature) ceiling. Knuckle, IP and wrist loop counts are far above 3 / 2 / 3.

### 3.3 Surface deviation (T-2, hands, vs rev 107)

| Hand | prod → ref max | ref → prod max |
|---|---|---|
| L | 0.50 mm | 0.61 mm |
| R | 1.23 mm | 1.11 mm, outside the mask below (p95 0.059 mm, median 0.003 mm) |

**Excluded region:** a 1.3 cm sphere at the R thumb base, centre (−25.66, −47.84, 97.76) cm, containing 1 809 rev 107 vertices. rev 107 has a pit full of thin spikes there: a sculpt or remesh artifact, deviation up to 7.5 mm. The production mesh smooths over it instead of copying it. Evidence render: `05_R_crater_exclusion.jpg`, sent to Tyler in chat (not committed).

**This exclusion must be reviewed; it is not a silent waiver.**

### 3.4 Other measurements

| Item | Result |
|---|---|
| T-3 | Stature delta 0.000 mm. Bbox vs rev 107 within 0.02 mm. |
| Outside-hand vertices | Exact. |
| T-6 / T-7 | Not re-run. Only hand vertices changed, and the bbox is unchanged. The wrist landmark sections lie outside the edited region. |
| Old nail projection gate (±0.15 mm, frozen source) | **Not applicable to the claws and not claimed.** The Tyler-approved claw direction replaced the nail target. The fingernail projection values are superseded, not passed. |

## 4. Diagnostic rig (derived copy)

**File:** `work/claude109/Gorrund_hand_grip_tests109_DIAG.blend`. Hand crops at rest, two armatures, and one Action per validated test.

**Bones per hand:** hand, 4 × (MCP, PIP, DIP) and thumb (CMC, MCP, IP).

**Joint estimates:**
- Joints are placed on centerlines made from geodesic ring centroids.
  - MCP: 0.9 ring radius proximal to the web ring.
  - PIP and DIP: human P1 : P2 : P3 = 1 : 0.58 : 0.40.
  - Thumb: MC1 : P1 : P2 = 46 : 32 : 24.
- These are estimates, not bible landmarks.
- Flexion axis: across the hand. Thumb axis: palm normal.

**Weights:**
- Explicit connected-surface digit ownership, with no bleeding across touching digits.
- Smooth joint blends.
- A harmonic palm transition, with per-digit geodesic falloff on the palm.
- **Claws 100 % on their distal bone**, so they move rigidly.

**Skinning:** Blender DQS (Preserve Volume).

**Solver:** a contact-aware greedy pose solver.
- It advances each digit in 5 % steps.
- After every step it checks the actual skinned mesh: new intersections vs rest, the penetration depth of every cluster, claw contacts, and fixture penetration.
- Every accepted state is a checked intermediate keyframe.

**Tolerances (stated, not hidden):**
- Skin-to-skin contact: up to 1.0 mm interpenetration, as a stand-in for soft-tissue contact.
- Claw contact: up to 0.5 mm.
- Fixture: no penetration deeper than 0.5 mm; contact means a distance of 0.5 mm or less.

**Blender cross-check of every final pose (Blender's own armature evaluation):**
- matches the solver geometry to ≤ 0.0007 mm;
- return to rest: exact (0.000 mm);
- posed bone-length change: ≤ 0.00007 mm.

## 5. Movement and grip results

Angles below are the **added** flexion beyond the reference curl, in degrees.

| Test | L | R | Verdict |
|---|---|---|---|
| Individual finger bends (MCP/PIP/DIP) | pinky 35/38/25 · ring 14/53/35 · middle 28/60/40 · index 25/38/25 | index 11/53/35 · middle 7/53/35 · ring 21/45/30 · pinky 32/34/23 | No violations. Ranges are limited by contact with neighbours and the palm; MCP is especially small on the R middle and index. **Partial.** |
| Individual thumb bend | MCP 4°, IP −5° | MCP 10°, IP 3° | **FAIL.** Blocked by thenar/palm crease self-contact deeper than 1 mm. |
| Full clench (thumb spread, fingers curl, thumb wrap) | fingers 21–42 / 36–46 / 25–32; thumb wrap 0 | fingers 21–36 / 36–46 / 25–32; thumb wrap MCP 4.5° | Fingers close until pad/claw contact with the palm, with no penetration. **The thumb cannot wrap over the fingers.** **Partial.** |
| Precision pinch (22 × 2 mm coin) | index and thumb both in contact (0.43 / 0.45 mm), no penetration | index and thumb both in contact (−0.33 / −0.13 mm), no penetration | **PASS**, both hands. Thumb palmar abduction about 50°. |
| Handle grip (Ø 32 × 180 mm, diagonal) | middle, ring and pinky in contact; index blocked and still extended (−15.6°); thumb 26 mm away; palm 3.2 mm | 4 fingers and thumb in contact (≤ 0.5 mm); palm 1.1 mm; no penetration | **R PASS; L FAIL** (index and thumb). |
| Claw collisions in all saved poses | max claw contact 0.36 mm, 0 fixture claw penetration | max 0.33 mm | Within tolerance. |

## 6. Blocker and remaining requirements

There is no external blocker. The remaining work is concrete:

1. **Thumb deformation.** CMC flexion and palmar abduction from the spread position fold the thenar skin into the palm by more than 1 mm. Joint placement and skinning need a corrective: for example a thenar helper bone, a better-placed CMC, or a corrective shape. Then the thumb-wrap clench, the thumb bend and the L handle thumb can be re-run.
2. **L index in the handle grip.** It needs the same thumb clearance, plus a better handle seat. The handle currently rests 3.2 mm off the L palm.
3. **Individual finger ranges.** These are contact-limited because the reference sculpt's fingers are packed side by side. Larger isolated bends need either softer contact handling at the creases or an owner ruling on acceptable contact depth.
4. **Owner review** of:
   - (a) the method substitution in §2;
   - (b) the genus 1 → 0 bridge cut, which follows rev 107;
   - (c) the R thumb-base artifact exclusion;
   - (d) the T-4 regression at the claws;
   - (e) the 1.0 / 0.5 mm contact tolerances.

## 7. Reproduction

- **Tools:** `reviews/rac-rp1f-evidence/claude-hand-mesh-grip/tools/`.
  - `stage1_topo` → `stage2_proj` → `stage3_drape` (with `drape.py`, `cap.py`) → `stage4_assemble`;
  - `build.sh`, using `fixall` from rp1e plus `twoway`;
  - gates: `gate_topo`, `sx`, `gate_dev`;
  - rig: `skel2`, `rig`, `fastpose`;
  - tests: `gripsolve`, `placefix`, `placecoin`, `blendcheck`, `packtests`.
- **Inputs:** rev 107 (local), v015 (repo).
- **Per-test reports:** `work/claude109/claude109_reports.zip` on Tyler's PC: solver outputs, gate JSONs, fixtures and the Blender cross-check.
- **Not published:** new raw geometry and images (not uploaded here).
