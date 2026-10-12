# RAC RM-OT-05D — True skeletal-envelope separation + Grask / Gorrund race anatomy gate

**Order:** `reviews/chatgpt-rac-rm-ot-05d-true-skeletal-envelope-race-anatomy-order.md`
**Evidence:** `reviews/rac-rmot05d-evidence/`

**Result:**

| Race | Verdict |
|---|---|
| Grask | **PASS** on the focused species-readability gate (candidate E3), conditional on an author canon check (§8.3) |
| Gorrund | **CONSTRAIN** |

Because Gorrund did not pass cleanly, the gate stops at Stage B (order §8):
- no Stage C validator suite;
- nothing promoted;
- RM-OT-05 stays OPEN;
- no D4, no UE5, no canon rewrite.

## 1. Summary

### What changed

- **True skeletal floor.** The guard that froze the MPFB minimum-body (`-LEAN`) soft tissue as if it were bone is replaced by a true skeletal floor (`tools/rac/w1/true_envelope.py`). The floor is the `-LEAN` moved inward by a documented soft-tissue depth map, with bony landmarks held at subcutaneous depth and limb floors radial to the accepted bone axes.
- **Outward normals proven.** An automated test, run on every body, confirms the outward-normal convention.
- **Skeleton-anchored measuring levels.** Station levels now come from the skeleton (`tools/rac/w1/skeletal_stations.py`), so a changed surface can no longer move the measuring height.
- **Composition amount restored.** Volume is restored exactly (ratio 1.0000 vs the route), so the organization moves soft tissue without changing composition amount.

### Candidates

| Race | Candidates | Developed from |
|---|---|---|
| Grask | E1 (moderate), E2 (strong), E3 (assertive) | 05C Grask C |
| Gorrund | E1 (moderate), E2 (strong) | 05C Gorrund B |

Every candidate was built at reference, low composition, Narrow and Broad: 20 bodies. All pass the §9 minimal technical guards.

### Blind read

Three blind runs, each with 3 independent uninformed scorers, using the revised A / B / C question:

**Grask E3:** C from **3 / 3 scorers for both reference and low composition in both runs that included it (runs 2 and 3)**.
- It formed a stable cluster with the other Grask bodies.
- No human control was pulled in.
- Every scorer attributed the read to anatomical organization: arm-to-trunk proportion, a high / forward upper-chest and scapular mass, and leg-segment contour.

**Gorrund E1 and E2:** met the 2-of-3 C threshold in runs 1 and 3, but got **0 / 3 in run 2**.
- Gorrund always formed its own exact cluster.
- Two of the three run-3 scorers called its C read low-confidence or partly due to bulk.

**Grask vs Gorrund:** in run 3 all three scorers distinguished two separate non-human groups without labels. In run 1 one scorer did.

### Canon caution for Grask E3

Scorers describe its upper body as "hunched / forward-rounded" and its leg as "bent, zig-zag, knee set back, digitigrade-like".
- Joints, bone lengths and the R-6 pose are **identical** to the accepted skeleton (Δ = 0.000 cm).
- These reads are produced by soft tissue: scapular / thoracic mass, a keel chest, and a high calf belly with a long tendon cord.
- The order forbids digitigrade legs, posture tricks and caricature. The author must judge whether this *reading* is acceptable before E3 is used as the Grask direction.

## 2. True skeletal envelope (Stage A)

**Definition** (`true_envelope.py`): floor = `-LEAN` − d(v)·n_out, authored in each body's own anatomical coordinates and blended by skin weight.

| Region | Depth d removed from `-LEAN` |
|---|---|
| Joint condyles / epicondyles, patella, malleoli, olecranon, wrist, hands, feet, head / neck | 0.4 cm (subcutaneous) |
| Clavicle, acromion, sternum, spinous line, sacrum, ASIS | 0.5–1.0 cm |
| Iliac crest | 1.2 cm |
| Trochanter | 1.5 cm |
| Ribs laterally | 1.2 cm |
| Pectoral | 2.0 cm |
| Abdominal wall (cavity kept) | 1.5 cm |
| Flank | 2.0 cm |
| Scapular cover | 2.0 cm |
| Trapezius | 2.0 cm |
| Erector / lumbar | 3.0 cm |
| Gluteal mass | 6.0 cm |
| Deltoid cap over the humeral head | 2.5 cm |
| Limb shafts | down to a bone-radius model around the accepted bone axis (humerus 0.35, radius + ulna 0.50, femur 0.32, tibia + fibula 0.45 × narrowest lean section) |

Two further rules: the anteromedial tibia and the ulnar border are held subcutaneous, and limb floors are radial to the axis, because a normal offset folds the floor.

**Not preserved** (order §3.1): the human gluteal apex, abdominal curvature, waist indentation, pectoral contour, deltoid cap, calf and biceps belly pattern, and lumbar hollow.

**Allowed movement** (`stageA/stageA_*_allowed.json`). Median floor depth below the old guard, and how far 05D actually moved inside the old guard:

| Region | Floor below old guard, Grask / Gorrund (cm, median, p90) | 05D inside old guard, Grask / Gorrund (max cm, vertices) |
|---|---|---|
| Gluteal (posterior pelvis) | 3.4, 4.9 / 3.6, 5.1 | 0.8, 7 / 2.4, 54 |
| Deltoid cap | 1.6, 2.5 / 1.7, 2.7 | 0.9, 25 / 0.6, 18 |
| Pectoral / chest front | 1.9, 2.0 / 1.8, 2.0 | 0.3, 4 / 0.7, 44 |
| Thigh shaft | 4.4, 8.0 / 6.2, 10.0 | 2.0, 140 / 3.6, 114 |
| Shank shaft | 2.0, 4.8 / 2.3, 5.5 | 0.7, 76 / 1.3, 69 |
| Hands / feet (held) | 0.4 / 0.4 | ≤ 0.46 (subcutaneous) |

**Section strips:** `stageA/stageA_{GR,GO}_{shoulder,pelvis}.png`. Each shows the old `-LEAN` boundary (red), the true floor (blue), the 05C baseline (grey) and the 05D surface (black). The cuts are:
- horizontal at the shoulder joint, through the thorax, at the hip joint and at the gluteal level;
- coronal through the shoulder;
- sagittal through the gluteal mass.

**Floor guard result:** every organized vertex is outside the floor (min signed −0.00002 cm on all 20 bodies). Head, neck and hands are not organized, so they stay identical to the route.

**Dependencies that could not be separated** (§3.1, recorded in `true_envelope.DEPENDENCIES`):
1. **Posterior hip-level depth (ALPC S6 depth, "pelvic AP").** On the `-LEAN` the posterior extreme there is gluteal mass over the ischium, and the accepted W2 pelvic-depth relations were read on that surface. The bony AP cannot be separated from gluteal tissue without a bone mesh, so the relation is held on the unorganized skeleton proxy (§3).
2. **S2 breadth.** It sits on latissimus / serratus cover over the ribs; 1.2 cm is kept there.

## 3. Normal orientation and skeleton-anchored measurement

**Normals.** `true_envelope.test_outward` orients normals by the kept mesh's signed volume. It then checks anatomical probes: chest front +y, back −y, crown +z, sole −z, lateral thigh ±x. It passes on every body and every `-LEAN` (`guards/guard_all.json`, `outward_normal_test`). 05B is left unchanged for reproducibility, as the order requires.

**Measurement** (`skeletal_stations.py`). The ALPC thorax-maximum and waist levels are taken from the skeleton surface (`-LEAN`), not from the reference skin. Every comparison uses those levels. Four readings are reported per body:

| Reading | Meaning |
|---|---|
| Protected | Composition-infimum envelope (CIB) of the *unorganized* route at skeleton levels: the locked skeletal relation |
| Organized | CIB of the organized grid at the same levels: a surface diagnostic |
| True floor | The floor itself, sectioned at the same levels |
| Legacy | The old own-skin-level reading |

| Body | Protected: bitroch ÷ crest / pelvis ÷ thorax b / pelvic d ÷ thorax d | Organized | True floor | Legacy (own-skin) |
|---|---|---|---|---|
| Grask E1 / E2 / E3 (218) | 1.1970 / 1.0275 / 0.8267 (unchanged) | 1.153–1.145 / 1.045–1.030 / 0.79–0.78 | 1.1465 / 0.920 / 0.753 | 1.153–1.145 / 0.98–1.06 / 0.81–0.78 |
| Gorrund E1 / E2 (230.9) | 1.1846 / 1.0234 / 0.8570 (unchanged) | 1.110–1.105 / 1.055–1.051 / 0.83–0.80 | 1.1384 / 0.976 / 0.786 | 1.110–1.105 / 1.275 / 0.83–0.81 |

- **GR-P2b (bitrochanteric ÷ crest ≥ MF 1.1918):** protected 1.1968–1.1972 at every frame. Pass, unchanged.
- **GR-P6:** protected unchanged at every frame.
- **Gorrund deep pelvis:** protected pelvic depth ÷ thoracic depth unchanged (0.8545–0.8634 across frames). Skin pelvic AP is 31.2–32.0 cm, vs 33.3 cm for 05C.

**Author attention.** On the *organized* surface the composition-infimum bitroch ÷ crest reads 1.145–1.154, below MF's legacy value 1.1918. The reason is that the organization removes donor soft tissue over the trochanter / gluteal region that the old CIB counted. 05D treats this as soft tissue, as the order directs, and keeps the relation on the skeleton. The author should confirm that reading of GR-P2b before any Stage C.

## 4. Candidates

Specs are in `candidates.json`. All candidates add the true floor and volume restoration. "Strong" and "assertive" mean more of the same organization, not more composition.

| | What it adds to its baseline |
|---|---|
| **Grask E1** (from 05C C) | Freed girdle (soft-cap yoke to 4 cm), sacral / gluteal organization (posterior sacral plane, high posterolateral gluteus-medius mass, lower buttock reduced 16 %), abdominal tuck-up (anterior lower trunk × 0.88), erector mass, fold relaxation of the hip–thigh junction to r 0.35 |
| **Grask E2** | E1 + 5 cm scapular / latissimus wing, tuck-up × 0.82, tendon cords × 1.2, sternal keel 1.5 cm, quad / hamstring bellies set lower (no groin bulge) |
| **Grask E3** | E2 + 9 cm scapular / latissimus mass and 4 cm flank, keel 3.5 cm, deep keel chest (+2 cm), tuck-up × 0.72, paraspinal columns with a midline groove, proximal bellies higher, cords × 1.2 |
| **Gorrund E1** (from 05C B) | Freed posterior column: the buttock folds into one sacral–hamstring column (masked Laplacian of the posterior hip–thigh shell, r −0.5…0.45), straight posterior line, columnar limbs with abrupt transitions |
| **Gorrund E2** | E1 + dorsal load arc (posterior line convex 5 cm, mass at r 0.78), thoracolumbar mass, neck-root mass |

## 5. Stage B evidence

All sheets are in `sheets/`. Matched camera, ground and stature; body only. Each sheet includes Skarn at matched height, the Marchfolk reference control and the 05C developmental baseline.
- Front / front ¾ / profile / rear ¾ grey: `d_{GR,GO}_{F,Q,P,RQ}_grey`.
- Black silhouette, front and profile: `d_*_{F,P}_sil`.
- Low composition (all views, plus silhouettes): `d_*_low_*`.
- Narrow / reference / Broad: `d_*_frames_*`.
- Close strips: shoulder / thorax (`*_shoulder_*`, `*_thorax_*`); pelvis / sacrum / proximal thigh (`*_pelvis_{Q,P,RQ}`); knee / shank (`*_knee_*`, `*_shank_P`); forearm / wrist / hand (`*_elbow_*`, `*_wrist_P`, `*_hand_P`). Grask strips are `c_218_*`, Gorrund `c_229_*`.

## 6. Blind protocol and raw classifications

**Protocol.**
- Body only, head and neck removed, height-normalized, front + profile, neutral grey + silhouette.
- Shuffled with a fixed seed, codes only; the key was never shown.
- 3 independent uninformed scorers per run (fresh agents).
- Wording given to every scorer: "The set may contain ordinary humans and bodies of fictional humanoid races; you are not told which or how many."
- Classes: A ordinary human-family / B unusual-extreme human-family / C distinct humanoid race-species.
- Scorers gave driving features, groupings, whether two races could be told apart, and whether each C read came from thinness / fatness / muscularity / a single feature or from anatomical organization.
- Raw answers are in `blind/blind_results_run{1,2,3}.json`; counts are in `blind/blind_summary.json`.

**C count out of 3 scorers (reference / low):**

| Candidate | Run 1 (16 bodies) | Run 2 (18 bodies, E3 added) | Run 3 (18, replication) |
|---|---|---|---|
| **Grask E3** | — | **3 / 3** | **3 / 3** |
| Grask E2 | 0 / 0 | 3 / 3 | 2 / 3 |
| Grask E1 | 0 / 0 | 1 / 3 | 2 / 2 |
| **Gorrund E1** | **2 / 2** | **0 / 0** | **2 / 2** |
| **Gorrund E2** | **2 / 2** | **0 / 0** | **2 / 2** |
| Human controls (8) | no C | no C | no C |

**Clusters.**
- The Gorrund bodies formed an exact cluster for every scorer in every run.
- The Grask bodies formed an exact cluster for every scorer in run 3.
- In run 2, one scorer placed the Skarn Narrow control as a "borderline milder member" of the Grask group. Another put it in a separate long-limbed borderline group. No scorer needed the control to form the cluster.

**Scorers' words.**
- Grask: "arm-to-torso ratio, upper-body posture and shoulder placement, a distinct lower-leg structure (displaced calf, knee angle), narrow waist… not thinness" (run 2). "Lean humans … do not show the arm length, forward shoulder / back mass, or bowed leg line" (run 3).
- Gorrund: "deep boxy trunk, flat back, no waist, thick columnar thighs and a thick-to-thin leg transition … fatness or muscularity alone would not produce [it]" (run 1). Also "mostly overall bulk … least confident C" (run 3, scorer 2) and "mostly mass, depth distribution odd → B" (run 3, scorer 1).

**Context effect.** In run 2, with the strongly organized Grask E3 in the set, every scorer re-anchored "non-human" on E3's organization and moved Gorrund down to A/B. In runs 1 and 3, Gorrund reached the threshold. Gorrund's read is therefore real but not robust.

## 7. Technical guards (§9) — `guards/guard_all.json`, 20 bodies

| Guard | Result |
|---|---|
| Exact stature | Pass: identical to the 05C / 05B skeleton route (GR 217.99, GO 230.90; low 217.21 / 230.75) |
| Ground contact | Pass |
| No uniform scaling; joint centres, bone scales, long-bone axes unchanged | Pass: joint Δ 0.000 cm, `-LEAN` Δ 0.000 cm, bone scales equal |
| Outward-normal test | Pass, body and `-LEAN` |
| True floor respected | Pass: 0 organized vertices inside the floor by more than 0.2 cm |
| Gross self-intersection vs the same route without 05D (+10) | Pass: GR ref 124–127 vs 157, low 140–148 vs 165, frames 117–127 vs 157/169; GO ref 53 vs 67, low 64–72 vs 78, frames 34–38 vs 53/57 |
| Arm / trunk clearance | Pass: 0 inside the closed trunk section; min gap 0.70 cm (Grask E3 low) to 1.39 cm |
| No posture trick | Pass: R-6 joints identical |
| Composition ordering (low vs reference, skin S2 / S5 / S6) | Pass: same sign as the route |
| Frame ordering (N < ref < B, skin S2 / S5 / S6) | Pass |
| Surface volume vs route | 1.0000 on every body (amount restored; reported separately as the order requires) |
| Fixed anatomical-station relations | Pass: protected readings unchanged (§3) |

## 8. Regressions, non-passes and risks

1. **Gorrund readability is not robust:** 0 / 3 in run 2, and low-confidence C reads partly attributed to bulk in run 3.
2. **Organized-surface GR-P2b reading** is 1.145–1.154, below MF's legacy 1.1918. This is a definitional question for the author (§3). The protected skeletal relation passes.
3. **Grask E3 canon risk.** The reads cite "hunched / forward-rounded shoulders", a "back hump", and a "bent / zig-zag / digitigrade-like" knee. The skeleton and pose are unchanged; the effect is soft tissue (9 cm scapular mass, keel chest, high calf bellies with long tendon cords). The author must rule whether that read violates the no-posture-trick / no-digitigrade / no-caricature rules (order §5.1).
4. **Grask E1 / E2 depend on context.** They failed with only Gorrund in the set (run 1) and passed alongside E3 (runs 2 and 3). Only E3 is robust.
5. **True-floor dependency.** Posterior hip-level pelvic depth cannot be split into bone and gluteal tissue without a bone mesh (§2).
6. **Earlier build pass superseded.** The first full 05D build pass had more self-intersections at the head (the floor offset folds on the ears) and lost 6–8 % volume. These were fixed by leaving head / neck / hands unorganized and by volume restoration before the gate. The superseded runs are recorded in `search/`.

## 9. Verdicts

| Race | Verdict | Basis |
|---|---|---|
| **Grask** | **PASS** (E3), conditional on the §8.3 author canon ruling | ≥ 2 / 3 C for reference and low in both runs that included it (3 / 3, 3 / 3); stable cluster; no control collapse; attributed to organization |
| **Gorrund** | **CONSTRAIN** | Exact, stable cluster in every run, and 2 / 3 C in runs 1 and 3, but 0 / 3 in run 2; C reads low-confidence and partly attributed to bulk |
| Grask vs Gorrund | Distinguishable without labels | All 3 scorers in run 3; 1 of 3 in run 1 |

**Stop (order §8 / §13).** One race did not pass the focused gate, so the gate stops here: no exhaustive W2C / W2D suite, no roster checks, no acceptance package.

## 10. Recommendation for the author

1. **Rule on Grask E3.** Decide whether its soft-tissue "forward chest / scapular mass" and "high calf with long tendon cord" read is acceptable Grask biology, or too close to hunch / digitigrade. If accepted, E3 becomes the Grask direction for Stage C.
2. **Gorrund.** An external hand-sculpt is **not yet shown to be necessary.** Gorrund already forms an exact cluster and reaches C in 2 of 3 runs. Its weakness is the "extreme bulk" alternative explanation, which is bounded by three things:
   - canon (not fatter, wider or more muscular);
   - the locked deep-trunk / short-leg proportions;
   - human hands and feet.

   Recommended next step: one more *Gorrund-only* local bracket aimed at non-bulk organizational cues, such as joint-pad / load-column structure at the knee, ankle, elbow and wrist, a load-path back profile, and limb-section shape rather than mass. Then a fresh replicated blind read. Escalate to a hand-sculpted Gorrund base mesh only if that bracket also fails.
3. **Confirm the measurement rule** (§3). Protected skeletal relations should be read on the skeleton, with organized-surface CIB as a diagnostic. This must be confirmed before Stage C, or GR-P2b will read as a regression.

## 11. Files

### Added

- `tools/rac/w1/true_envelope.py`: true skeletal floor, outward-normal convention and test, dependencies.
- `tools/rac/w1/skeletal_stations.py`: skeleton-anchored ALPC levels; protected / organized / floor / legacy readings.
- `tools/rac/w1/rmot05d_drivers/`: `d_build.py`, `d_guard.py`, `d_stageA.py`, `d_package.py`, `d_blind.py`, `d_floorview.py`, `d_evidence.py`.
- `reviews/rac-rmot05d-evidence/`: README, `candidates.json`, `stageA/`, `sheets/`, `blind/` (3 runs plus summary), `guards/`, `construction/`, `search/`.
- `reviews/reference-assets/r6/`: GR5DE{1,2,3}{,-LOW,N,B} and GO5DE{1,2}{,-LOW,N,B} (20 files).

### Changed

- `tools/rac/w1/race_base.py`:
  - `floor: "true"` guard mode (outward-normal clamp to the true floor; head / neck / hands excluded);
  - `keep_volume` composition-amount restoration;
  - `_crotch` / `_armfade` / fold refinements;
  - smoothed section-centre line.
- `tools/rac/w1/skeleton_envelope.py`: builds the true floor for `race_base` when the spec asks for it.
- `tools/rac/w1/rmot05c_drivers/c_preview.py`: true-floor preview.
- `reviews/reference-assets/manifest.json`: 20 entries, PENDING AUTHOR / NOT ACCEPTED.
- `specs/STATUS.md`, `reviews/claude-pass2-r5-reference-mesh-queue.md`: phase state only. No race canon file was changed.
