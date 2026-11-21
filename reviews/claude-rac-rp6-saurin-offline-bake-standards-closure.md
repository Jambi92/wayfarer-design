# Saurin RP6 — Offline Bake Standards: Closure

**Order:** [standards approval order](chatgpt-rac-rp6-saurin-offline-bake-standards-approval-order.md) (c65e6c93)
**Builds on:** [offline bake validation report](claude-rac-rp6-saurin-offline-bake-validation-report.md), evidence `c74bbe5cb8c0767776f994e5668010622a844b0e`; handoff `bdde9d44`
**New evidence:** [`rac-rp6-evidence/saurin/rig_pilot/offline_bake/standards_review/`](rac-rp6-evidence/saurin/rig_pilot/offline_bake/standards_review/)
**Status:** **RP6 RIG PILOT / NOT FROZEN**

## Summary

The author's decisions are recorded, and the approved recipe is now the default of the bake entry point.
- **No new bake was run.** The retained bases and the regression controls are reused as they were measured.
- **Playback and tail reviews of the existing bakes** found no positional pop, crease, collapse, tear or inversion caused by a bake.
- **The author watched real-time playback and found two visible problems that no current gate measures** (§3.6). Both are in the shared rig and initialisation layer, so every body inherits them; the bakes neither cause nor fix them.
  - **Shoulder abduction is anatomically wrong.** The arm bends low in the upper arm and armpit instead of rotating at the top of the joint.
  - **The elbow has no muscle response.** The biceps and triceps do not contract or extend with flexion.

  The hip was judged good. Both problems are reported below as new defects with a proposed correction. Fixing them needs a separate order.

## 1. Standard recipe — implemented

**Entry point.** The recipe is the default of the normal entry point, `sa6_bake_full.py` (`BAKE_RECIPE=standard`):

| Setting | Value |
|---|---|
| `BAKE_PK_MINW` | 0.25, recorded explicitly as the minimum **half-width** of a pose-key tent as a fraction of the pose's full angle |
| `BAKE_DENSE` / `DENSE_STEP` | 1 / 0.0025 |
| `BAKE_GATE_ALIGNED_ALLOW` | 1 |
| Motion rule | local |
| Adaptive refits | ≤ 3 |

- `--recipe` prints the effective recipe.
- **Standard PC runner:** `pc_bake/run_standard.py` with `START_STANDARD.bat`. It forces the standard, strips stray overrides, and writes `RECIPE.json` per body.
- **Instructions:** `tools/rac/rp/saurin_rp6_v001/BAKE_STANDARD.md`.

**Archived runs stay reproducible.** `BAKE_RECIPE=archived` restores the pre-standard defaults. `BAKE_STANDARD.md` §7 gives the exact settings for each archived runner, and `BAKE_MOTION_RULE=original|local` selects the motion verdict.

**Validation is unchanged and runs from the first pass:**
- 34 anatomical poses and 50 special gates × 25 / 50 / 75 / 100 %, plus neutral;
- the sweep at 0.025 on heavy-joint and bake-affected poses and 0.125 elsewhere;
- refitted special poses at 0.025 plus transitions;
- the dense audit;
- integrity, before/after and RP5-literal diagnostics.

Each refit reopens its artifact from disk and reruns everything.

**Motion failures now feed the fit** (new). Under the standard recipe, a motion failure enters the next refit as `motion:<pose>`:
- the failing frame pair's fractions become fit samples;
- that pose's key floor doubles, to min(1, 2 × max(floor, sample step));
- keys kept from the previous artifact are widened.

Gate, sweep and dense failures already fed the fit.

**Acceptance record** (new). `ACCEPT_<body>.json` holds:
- the effective recipe;
- the sha256 of every `sa6_*.py` tool;
- body inputs: `bodies.json`, the body npz and vertex hashes, and the recipe;
- rig inputs: the initialisation layers and base arrays;
- artifact hashes;
- the sampled poses and fractions for every stage, with verdicts.

### Checks of the change

| Check | Result |
|---|---|
| `--recipe` | standard → floor 0.25, dense 1 at 0.0025, aligned 1, motion local. archived → floor 0, dense 0, motion original. An explicit override wins under both. |
| Standard runner (dry run, missing body) | Writes `RECIPE.json` = standard and ignores a stray `BAKE_PK_MINW=0.125` from the caller. The worker then stops on the missing body, as intended. |
| Failure collection on recorded runs | END_MUFAHI repair 1, it5: standard/local gives `{'motion:shoulder_abd90_xneg': [0.875, 0.90833]}`; archived/original gives no failure, matching that run's first-rule record. END_FAHI repair 1, it2 (first-rule record): standard gives `motion:hip_flex70_xpos [0.96667, 1.0]`. |
| Motion feedback in the fit | Run on the END_MUFAHI repair-1 it5 artifact (the 0.73 cm trunk pop), with `motion:shoulder_abd90_xneg` and floor 1/8 as that run used. The pose's keys widened from 11.25° to 45° half-width (floor 0.5), and the motion rule then **passes** on that pose (excess −0.030 cm). With 2 fit rounds the pose still had 2–4 rig tears or flips at 75–100 %. With the full 8 rounds the motion rule still passes (bake 0.542 cm against blend 0.556 cm, excess −0.016 cm). Folds and contact are cleared, but 1–3 rig tears remain at 87.5–100 %, and the fit did not converge (entering per round 7, 15, 15, 11, 4, 13, 3, 7). **So the mechanism fixes the motion failure as designed, but one refit does not fully re-clear the widened pose.** In a driver run those tears would come back as refit samples, within the 3 refits allowed. That full loop was not run here, because a bake batch needs its own order. **Open point:** the doubling step may be too coarse. A smaller step, or rebaking the pose from the initialisation layer with the wider floor (which is what cleared END_MUFAHI in repair 2), may converge better. Evidence: `standards_review/motion_feedback_test/`. |

**Tool version of the archived PC fits.** They ran `sa6_bake.py` at 35c120d8, which did not write `pk_min_width` into artifacts. The floors of those artifacts are evidenced by their runner settings and key widths. Standard runs record the floor, plus the per-pose motion floor `pk_floor_per_pose`.

## 2. Tail criterion — provisionally approved, visual review recorded

**Criterion as approved:**

| Result | Rule |
|---|---|
| PASS | C ≤ 2.0° and area ≥ 0.95 |
| REVIEW | 2.0° < C ≤ 2.5°, area ≥ 0.95; needs visual review in motion |
| FAIL | C > 2.5° or area < 0.95 |

Scope: the frozen tail (181 rings, 11-junction window) and the sampled motions. The raw 2.51 ratio stays a diagnostic.

**Worst baked tail case per roster body.** It is `tail_distal_60` at 100 % on all four, and the bake equals the packaged blend there:

| Body | C | Area min |
|---|---|---|
| BASE_c1 | 1.14° | 0.985 |
| BASE_c2 | 1.12° | 0.985 |
| END_FAHI | 1.21° | 0.985 |
| END_MUFAHI | 1.21° | 0.985 |

Renders are in `standards_review/tail/`: shaded mesh in lateral and dorsal view, `TM_*`; centreline, turning profile and motion strip at 90 / 95 / 100 %, `TR_*`.

**Visual conclusion:**
- **Worst baked cases.** All four are smooth distal curls: no hard kink, root collapse, tear or inversion. The motion strip shows the curl forming steadily, and the turning peak near the tip is the neutral taper.
- **Root crease anchor.** BASE_c1 `tail_root_biased_60` at 100 %:
  - Plain LBS (C = 2.13°) shows the vertical crease line at the tail root, the calibration anchor near 2.12°.
  - The packaged blend and the bake (C = 0.19°) show no crease.
- **Smooth-bend anchor.** c1-M208-B@0.75 `tail_combined` at 100 % (`tail/renders/TM_…` in the validation evidence):
  - Plain LBS at C = 2.45° bends smoothly with no crease.
  - The blend and the bake are at 1.99°.

  This confirms the REVIEW band: the root-biased 2.12° frame creases, while the distributed 2.45° frame does not.

**No bake has a REVIEW or FAIL tail frame.** All 1,760 roster frames pass. The only frames above 2.0° on the roster are plain LBS.

## 3. Motion rule — provisionally approved, playback review recorded

**Rule as approved:** e_bake(f, g, v) ≤ max(0.50 cm, e_initialization(f, g, v) + 0.05 cm).
- Excursion is measured relative to plain LBS.
- Test speed: the full range in 1 s at 30 fps.
- Grid: 1/240 of the full angle, plus transitions.
- The first-rule verdict and the bake-only excursion are kept as diagnostics.

**Playback review** (`sa6_bake_playback.py`, `standards_review/playback/`).
- **Speed:** the documented test speed, 30 fps with the full range in 1 s, forward then reverse. A ×4 slow copy was also made.
- **What was reviewed,** for each of the four final bakes:
  - the three tightest poses under the local rule;
  - the pose with the largest bake-only excursion;
  - `elbow_130_xneg`;
  - END_MUFAHI's formerly failing `shoulder_abd90_xneg`.

  That is 15 cases.
- **What each case produced:**
  - a still sheet of the frames around the worst frame;
  - a sheet around the largest change of per-frame speed;
  - a per-frame curve of the region's maximum surface change, bake vs blend;
  - a GIF (real-time GIFs for 5 representative cases are committed; the tool reproduces any case).

### Visual conclusions

**1. No positional pop in any case.**
- In every case the surface change is spatially broad and smooth, with no single-frame spike that drops back.
- The bake's curve equals the packaged blend's to ≤ 0.03 cm in 14 of 15 cases. The exception is END_MUFAHI `hip_flex70_xneg`, where the bake *lowers* the blend's peak from 0.35 to 0.28 cm per frame.

**2. Inherited from v004: frames above the 0.50 cm cap.** The packaged blend itself exceeds the cap, and the bake equals it:
- `shoulder_abd90_xneg` near 90°: 0.51–0.56 cm per frame (BASE_c1, END_FAHI, END_MUFAHI);
- END_FAHI `hip_flex70_xpos` from 56°: 0.61–0.62 cm per frame.

This is expected under the approved rule, because the bake inherits the initialisation layer's motion.

**3. Speed steps in the initialisation layer (flagged for the author).** The per-frame surface change jumps by several times from one frame to the next, where a driver crosses a family sample. The bake equals the blend at each of these steps:

| Joint | Angle | Change per frame | Bodies |
|---|---|---|---|
| Shoulder abduction | ~45–48° | 0.04–0.10 → 0.42–0.51 cm | all bodies |
| Elbow flexion | 90–95° | 0.12 → 0.39–0.43 cm | all bodies |
| Hip flexion `xpos` | 52–56° | 0.26–0.43 → 0.46–0.61 cm | END_FAHI, END_MUFAHI |
| Hip flexion `xneg` | 17–21° and 35–37° | 0.15 → 0.40 cm and back | END_FAHI |

- **What the stills show.** In every case it is a smooth bulge or crease-filling region starting to move faster. The surface shape stays continuous, with no crease, tear or fold.
- **What the stills cannot show.** Whether a ×4–10 speed step reads as a visible "kick" in real-time playback needs a human viewer.
- **Recommendation.** Watch these GIFs:
  - `PB_BASE_c1_shoulder_abd90_xneg.gif`;
  - `PB_BASE_c1_elbow_130_xneg.gif`;
  - `PB_END_FAHI_hip_flex70_xpos.gif`.

  Smoothing a step would mean adding intermediate driver samples to the initialisation-layer family: a v004 layer change, outside this order.

**4. The elbow slope break, specifically.** At 30 fps the change per frame goes 0.08 → 0.12 → 0.39 cm over 86.7 → 91.0 → 95.3°, then decays to 0.28 cm by about 108°. The crease region swells smoothly, and the shape shows no defect. It is flagged under item 3 for the author's viewing.

**5. Bake-introduced speed variation** (END_MUFAHI `hip_flex70_xneg`). The baked change per frame alternates between 0.13 and 0.28 cm over about 20–60°, as the bake's keys hand over to each other. It stays below the blend's own 0.35 cm. The bake's own excursion here is the roster maximum: 0.51 cm, recorded in the validation report. It is visible in the still sheet as a smaller, steady patch; it is flagged with item 3.

**Scope of the rule.** The numerical rule checks frame excursion at one speed only. These reviews make no claim about acceleration smoothness or other speeds.

### 3.6 Author visual review (Tyler, 2026-11-20)

**What was shown.** Whole-body real-time playback (full move in 1 s at 30 fps), plus ×4 slow copies, made with `sa6_bake_playback_view.py`. The files are in `standards_review/author_review/`, with still strips at 0 / 33 / 67 / 100 %:

| GIF | Body | Pose | View |
|---|---|---|---|
| `review_shoulder.gif` | BASE_c1 | `shoulder_abd90_xneg` | front |
| `review_elbow.gif` | BASE_c1 | `elbow_130_xneg` | side |
| `review_hip.gif` | END_FAHI | `hip_flex70_xpos` | side |

**The author's verdicts:**

| Joint | Verdict |
|---|---|
| Shoulder | *"way off — it shouldn't bend like that, it should be more of a rotation and all bending is more at the top of the joint."* **Visible defect.** |
| Elbow | *"when the arm bends, the muscles in the arm should extend and contract based off of movement."* **Visible defect: missing muscle response.** |
| Hip | *"looks pretty good."* **Accepted.** |

The author did not call out a speed "kick" at any of the steps in §3 item 3. The visible problems are of shape, not of timing.

#### New defect SAURIN-RP6-DEF-SHOULDER-1: shoulder abduction pivots and bends in the wrong place

- **Where.** Every body, since it is a rig / initialisation-layer property that the bake inherits. Shown on BASE_c1 `shoulder_abd90_xneg` (and `_xpos`), 0–90°, worst from about 45° to 90°.
- **What.**
  - The shoulder cap and deltoid stay almost fixed while the arm swings up.
  - The bend forms lower down, in the upper arm and armpit. At 60–90° the upper arm creases and crumples under the shoulder (`shoulder_strip.png`).
  - The reading is a hinge below the shoulder, not a ball joint rotating at the top.
- **Evidence.** `review_shoulder.gif` and `shoulder_strip.png`. The pose definition rotates only `upperarm_r` by 90° about its parent-frame y axis, with its head at (−19.9, −6.3, 145.0) cm. `clavicle_r` exists in the skeleton but does not move in this pose. All gates pass, because none of them measures where a joint pivots or how the shoulder girdle moves.
- **Proposed correction (for review).** Three parts, in order:
  1. **Shoulder-girdle participation.** Drive `clavicle` elevation and rotation from upper-arm abduction, roughly a 2 : 1 glenohumeral-to-girdle ratio above about 30°. The shoulder cap then rises and rotates with the arm, in the rig and runtime and in the pose suite.
  2. **Pivot location.** Check that the `upperarm` head sits at the glenohumeral centre under the acromion; move it there if it is low or medial.
  3. **Deformation.** Reweight the deltoid and shoulder cap so they follow the humerus and girdle. Then refit the shoulder correctives for the new motion.

  This changes the joint placement, the weights, the pose suite and the corrective layer. The existing bakes would be rebaked under the standard recipe afterwards.

#### New defect SAURIN-RP6-DEF-ELBOW-MUSCLE-1: no muscle response to elbow flexion

- **Where.** Every body. Shown on BASE_c1 `elbow_130_xneg` (and `_xpos`), 0–130°.
- **What.** The biceps does not shorten and bulge, and the triceps does not lengthen and flatten, as the elbow bends. The upper arm keeps its rest shape and only the crease region is corrected.
- **Evidence.** `review_elbow.gif` and `elbow_strip.png`. The current correctives only prevent folds, contact and volume loss; nothing models muscle-driven shape.
- **Proposed correction (for review).** Add flexion-driven muscle shapes, starting with the elbow (biceps / brachialis bulge, triceps stretch) and extending to the other major joints if approved. Each shape would be:
  - a smooth, bounded, volume-aware delta;
  - keyed to the elbow angle;
  - authored, or fitted from an anatomical reference, as a new layer.

  It would be validated with the existing gates plus visual playback review. This is a new feature, not a gate failure.

## 4. Retained bakes and controls

**BASE_c1 and BASE_c2 are retained exactly** as identified in `offline_bake/SA_RP6_offline_bake_results_v001.json` at `c74bbe5`:

| Body | sha256 (json) | sha256 (npz) |
|---|---|---|
| BASE_c1 | `8ba88348d2d6f037441f363aa4ef4f12ece84e73dbf8b8d6f629758573c6b2b9` | `0e6a0197f578f681c91f76afbf9415d36f6e732a83fa684e487ba9c771634cc9` |
| BASE_c2 | `acf789e3e93b253855d24206f5e443da3a16c9ee4184c4858d59eda449819b84` | `b4bd5980fefdb7ea8fb2ec35ba1245b5107127c29f18e543e97be418313f7b2c` |

**Evidence reused.** Each passes:
- the full suites;
- the 0.0025 dense audit (4,030 and 4,840 samples, 0 failing);
- the local motion rule;
- integrity;
- before/after (1 → 0 each).

**Recorded exception.** Both were fitted with the pass-2 floor of 1/8 (`run_v2.py`). The actual key half-widths are:
- BASE_c1: 22.5° = 0.25 × 90°;
- BASE_c2 `elbow_130_xneg`: 16.25° = 0.125 × 130°;
- BASE_c2 `elbow_90_xneg`: 22.5° = 0.25 × 90°.

Only BASE_c2's elbow_130 key is below the standard. This is accepted as an existing-artifact exception.

**Regression controls** keep their recorded recipes and results:
- END_FAHI repair 2, it3;
- END_MUFAHI repair 2, it2.

No shipping bodies are designated.

## 5. Records updated

| Record | Update |
|---|---|
| `tools/rac/rp/saurin_rp6_v001/BAKE_STANDARD.md` | New: the bake instructions. |
| `reviews/rac-rp6-evidence/saurin/rig_pilot/SA_RP6_PD1_PD2_interfaces_v001.md` | Adopted per-body bake interface. |
| `specs/RAC_PRODUCTION_RIG_CARRY_FORWARD_REGISTER.md` | New Saurin RP6 section and carry-forward IDs ROSTER-1, MOTION-1, TAIL-1, SLOPE-1, FIT-1. |
| `reviews/claude-session-handoff.md` | Updated. |

The original reports and measured verdicts are unchanged, as historical evidence.

**Commits:**
- standards code and records: `0911792d`;
- this closure: see the handoff.

## 6. Open for the author

1. **SAURIN-RP6-DEF-SHOULDER-1** (§3.6): approve or redirect the proposed shoulder correction, which needs a separate order.
2. **SAURIN-RP6-DEF-ELBOW-MUSCLE-1** (§3.6): decide whether muscle-response shapes are in scope for RP6 (separate order).
3. Designate the shipping-preset roster.
4. Optionally view the remaining speed-step GIFs. The author found no timing "kick" in the three reviewed.
5. **Motion feedback convergence** (§1): the motion failure is fixed, but convergence of the full refit loop is not demonstrated. The doubling step may need refinement.

Everything else listed as out of scope in the order needs a separate order. That includes:
- further bake batches;
- elbow-family or driver-family changes;
- freeze, creator and runtime integration;
- UVs, materials, LODs;
- PD-1 / PD-2;
- UE5;
- other races.

Status remains **RP6 RIG PILOT / NOT FROZEN**. Stopping for ChatGPT and author review.
