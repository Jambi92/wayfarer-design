# RAC RM-OT-05E — Gorrund structural-readability closure gate

**Order:** `reviews/chatgpt-rac-rm-ot-05e-gorrund-structural-readability-closure-order.md`
**Evidence:** `reviews/rac-rmot05e-evidence/`

**Result:** **Gorrund FAIL on the replicated structural-readability gate (§7).**
- No 05E candidate cleared both replicated blind runs.
- Stopped under order §12 (2). Stage C did **not** run.
- Escalation recommended: an **external hand-sculpted Gorrund base mesh** (§10 below).
- Grask E3 stays the accepted developmental direction, still awaiting Stage C.
- RM-OT-05 stays OPEN. Nothing was promoted. No canon change, no D4, no UE5.

## 1. Author rulings acknowledged

1. **Grask E3 accepted as the developmental race-anatomy direction for Stage C.** This covers its demonstrated organization:
   - forward / high upper-chest and scapular organization;
   - shoulder-to-trunk integration;
   - keel / thoracic organization;
   - high calf belly with long tendon cord;
   - non-human limb-section and back-profile read.

   Not accepted, and not introduced: digitigrade feet or joint geometry, altered joint order, crouched or forced posture, pathological or caricatured hunch, pose tricks.

   Skeleton and R-6 posture are unchanged. Grask was not re-searched in 05E. E3 was used unchanged as the blind context control.
2. **GR-P2b semantics accepted.** Protected relations are evaluated on the skeleton at skeleton-anchored stations. The organized skin is a diagnostic reading only. No donor soft tissue was restored.
3. **Gorrund CONSTRAINED / NOT ACCEPTED.** 05E is the one final Gorrund-only local structural bracket, with Gorrund 05D E1 as the baseline and E2 as a provenance control. If it fails, stop and recommend a hand-sculpt.

The 05D technical basis is kept unchanged:
- true skeletal floor;
- outward-normal test;
- skeleton-anchored stations;
- composition-volume restoration.

## 2. Baseline and candidates

**Baseline:** Gorrund 05D E1, which has:
- the freed posterior column (buttock folded into one sacral–hamstring column);
- a straight posterior line;
- plateau limb columns.

**New tool** (`race_base.limb_base`, spec key `pads`): a periarticular pad / collar. It is a Gaussian in t along the accepted bone axis (t = 0 / 1 is the joint) × an angular sector, in cm outward. It moves no joint, axis or bone. Everything else uses existing organization keys.

**Common to all three candidates** (specs in `candidates.json`):

*Limb / joint organization: constant-section load columns.*
- Segment tissue is redistributed along each limb so it no longer tapers.
- Shank and forearm mass is moved distally, with a light proximal belly and a full distal column (two plateau muscles).
- Segment volume factors move tissue from the proximal to the distal segment. The whole-body volume is then restored exactly.
- Periarticular collars:
  - at the knee (thigh distal + shank proximal);
  - at the ankle (supramalleolar collar);
  - at the elbow (posterior olecranon pad);
  - at the wrist.
- Feet stay plantigrade. Hands and feet are not organized.

*Axial / trunk organization: box-section slab trunk.*
- Human surface relief kept only at 10 % (`detail` 0.1).
- Flat anterior plate from sternum to pubis.
- Straight lateral flank lines from axilla to hip, with no waist.
- Squared section corners at 45° and 135°.
- Posterior plane straight from upper back to sacrum (`line` 135–180°, convex 0.5).
- E1's sacral / hamstring column fold.

| | Limb collars (k) | Segment volume (thigh / shank / upper arm / forearm) | Trunk corners | A-frame (upper flank − / lower flank +) |
|---|---|---|---|---|
| **P1** (moderate) | 1.0 (knee 1.6–1.8 cm, ankle 1.8, elbow 1.2, wrist 1.3) | 0.85 / 1.25 / 0.90 / 1.20 | +5 % | — |
| **P2** (strong) | 2.2, no fade into the joint | 0.75 / 1.45 / 0.80 / 1.35 | +8 % | 4 % |
| **P3** (P2 + axial) | as P2 | as P2 | +12 % | 8 % |

**Search** (in `search/`):
- **F:** squared limb sections with knee / ankle pads. Too subtle at sheet scale.
- **G:** pillar shank with an A-frame trunk. Subtle.
- **H:** box trunk. The trunk changed, but the limbs still read as thick thigh / thin shin.
- **I:** constant-section columns with segment volume redistribution. This was the first legible change, and it became P1 / P2.

All of these stayed within the three-candidate limit; only P1–P3 were built.

## 3. Organization, not circumference

Files: `sections/e_limb_profiles.{png,json}`, `e_sections.png`, `e_posterior_profile.png`.

**Taper index** = rms section radius at t 0.85 ÷ at t 0.30. Below 1 means the limb tapers distally.

| | Thigh | Shank | Upper arm | Forearm |
|---|---|---|---|---|
| Skarn 229 | 0.65 | 0.71 | 0.88 | 0.77 |
| Grask E3 | 0.57 | 0.54 | 0.74 | 0.55 |
| Gorrund E1 (baseline) | 0.86 | 0.94 | 0.97 | 0.87 |
| Gorrund P1 | 0.88 | 1.04 | 0.98 | 0.97 |
| Gorrund P2 | 0.90 | 1.06 | 0.99 | 1.00 |
| Gorrund P3 | 0.90 | 1.06 | 0.99 | 1.00 |

- **Volume.** Whole-body volume is 1.0000 vs the route on every body. Thigh and upper-arm tissue moved distally; it was not added.
- **Cross-sections at skeleton-anchored heights.** At mid-shank and supramalleolar levels, the 05E sections are larger and rounder than E1's; mid-forearm and distal forearm likewise. This is offset by smaller proximal segments. At lumbar and sacral levels the trunk sections become squarer, with flatter posterior and anterior planes.
- **Proxy-floor dependency** (order §8). The posterior plane, the pelvis–thigh transition and the S2 trunk corners sit over regions whose floor is still a skeleton proxy rather than bone:
  - S6 depth / gluteal tissue over the ischium;
  - latissimus / serratus cover at S2.

  All limb-collar and column cues sit over real bone-axis floors.

## 4. Technical guards (§8) — `guards/guard_all.json`, 12 bodies

| Guard | P1 / P2 / P3, at reference, low, Narrow and Broad |
|---|---|
| Exact stature, ground contact | Pass (230.90; low 230.75) |
| No uniform scaling; joint centres, `-LEAN`, bone scales / long-bone axes unchanged | Pass (Δ 0.000) |
| Outward-normal test | Pass |
| True floor respected (organized region) | Pass (0 vertices inside by > 0.2 cm) |
| No posture trick (R-6 joints equal) | Pass |
| Plantigrade foot (heel and ball on the ground plane) | Pass |
| Hand / foot topology and digit count | Pass: faces identical to baseline; hands and feet unchanged vs route |
| Gross self-intersection vs route (+10) | Pass: ref 36–40 vs 67; low 66–69 vs 78; frames 38 vs 53/57 |
| Arm / trunk clearance | Pass: 0 inside; min gap 1.49–1.83 cm |
| Composition and frame ordering | Pass |
| Protected Gorrund relations (05D semantics) | Unchanged: bitroch ÷ crest 1.1846, pelvis ÷ thorax breadth 1.0234, pelvic d ÷ thorax d 0.8570 |
| Surface volume vs route | 1.0000 on all bodies |

## 5. Visual evidence (§6)

All files are in `sheets/`. Matched camera, ground and stature; body only. Controls: Marchfolk, Skarn 229, Grask E3, Gorrund E1 baseline and E2 provenance.

1–4. Grey views: `e_GO_{F,Q,P,RQ}_grey`
5–6. Silhouettes: `e_GO_{F,P}_sil`
7. Knee / shank / ankle: `c_229_knee_{F,P}`, `c_229_shank_P`, `c_229_ankle_{F,P}`
8. Elbow / forearm / wrist: `c_229_elbow_{F,P}`, `c_229_forearm_F`, `c_229_wrist_P`
9. Posterior thoracolumbar / sacral load path: `c_229_back_R`, `c_229_sacrum_RQ`, `c_229_thorax_{P,RQ}`
10. Pelvis / proximal thigh: `c_229_pelvis_{Q,P,RQ}`
11. Cross-sections: `sections/`

States:
- low composition: `e_GO_low_*` (4 views + 2 silhouettes);
- Narrow / reference / Broad: `e_GO_frames_{F,P,RQ}`.

## 6. Replicated blind gate (§7)

**Protocol.**
- Body only, head and neck removed, height-normalized, front + profile, neutral grey + black silhouette.
- Shuffled codes. 3 fresh uninformed scorers per run; the key was never shown.
- Classes: A ordinary human-family / B unusual-extreme human-family / C distinct humanoid race-species.
- Scorers gave confidence, drivers, bulk vs organization, groups, whether Grask and Gorrund can be told apart, and axial and limb cues.

**Set** (18 bodies, the same in both runs):
- 8 human controls (Marchfolk and Skarn × reference / Narrow / Broad / low);
- **Grask E3** reference + low (in every run, as §7 requires);
- Gorrund E1 reference + low;
- P1, P2, P3 reference + low.

| Run | Set | Seed | Sheets | Raw outputs |
|---|---|---|---|---|
| A | J | 20261018 | `blind/blind_J_*` | `blind_results_runA.md` |
| B | K | 20261019 | `blind/blind_K_*` | `blind_results_runB.md` |

Summary: `blind_summary.json`.

**C count out of 3 scorers (reference / low):**

| Body | Run A | Run B | Gate (≥ 2 / 3 at ref and low in each run) |
|---|---|---|---|
| **Gorrund P1** | 1 / 3 | 3 / 0 | **fail** |
| **Gorrund P2** | 3 / 3 | 0 / 0 | **fail** |
| **Gorrund P3** | 3 / 3 | 0 / 0 | **fail** |
| Gorrund E1 (baseline) | 3 / 1 | 3 / 3 | fail (low in run A) |
| Grask E3 (context control) | 3 / 3 | 3 / 3 | robust (3 / 3 in all 4 runs that have included it, 05D runs 2–3 and 05E runs A–B) |
| Human controls (8) | no C | no C | no control collapse |

**What happened.**

*Run A.* Every scorer formed one stable "slab / pillar" cluster, with the core six being P2 and P3 at reference and low, P1 low, and E1 reference. All three scorers:
- called the cluster C;
- attributed it to **organization**: "no waist, thorax and pelvis fused into one slab", "flat deep column, no lumbar lordosis", "pillar legs … thigh barely differing from shin", "knee a bulge rather than a transition", "thick ankles", "abrupt step-like knee and ankle transitions";
- named axial and limb cues;
- told it apart from Grask without labels.

*Run B,* same 18 bodies with a new shuffle. All three scorers again told the Grask pair and a Gorrund group apart. But they split the Gorrund bodies along the **limb taper contrast**:
- **C, 3 / 3:** E1 reference, E1 low and P1 reference. These are the bodies with the most visible thick-thigh → thin-shin contrast.
- **B or A, 0 / 3:** P2 and P3 at reference and low, and P1 low. These are the constant-section pillar bodies. Scorers called them "could be an ordinary heavy-human or low-contrast cluster that merely resembles Group 2. I would not call them non-human with any confidence", "can't separate these cleanly from heavy humans", "the group boundary unstable".

**Reading.**
- The 05E constant-section columns *are* recognized as organization when the set is read as one Gorrund group (run A).
- But they also sit inside the "heavy human" interpretation, and a different shuffle tips them there (run B).
- The baseline's thigh / shin contrast survives at reference but not reliably at low composition (run A: E1 low 1 / 3).
- No variant holds C at both reference and low across both replicated contexts.
- Per §7, "a pass in one context and failure in another is still a failure."

**Criteria check**, best candidate P2:

| # | Criterion | P2 |
|---|---|---|
| 1 | Reference ≥ 2 / 3 C in each run | ✗ (3, 0) |
| 2 | Low ≥ 2 / 3 C in each run | ✗ (3, 0) |
| 3 | Stable cluster | run A ✓, run B ✗ (boundary unstable) |
| 4 | Distinguishable from Grask E3 | ✓ in both runs |
| 5 | Majority explanation is organization | run A ✓, run B ✗ (bulk / heavy-human) |
| 6 | Axial and limb cues cited | ✓ |
| 7 | No human-control collapse | ✓ |

**Gorrund verdict: FAIL** on the 05E focused gate. Gorrund remains NOT ACCEPTED.

## 7. Stage C

**Not run.** It is conditional on a Gorrund pass (order §9).

## 8. Regressions and risks

- **None technical.** All §8 guards pass, and the protected relations are unchanged.
- **The 05E cues lower Gorrund's distinctness against heavy humans in some contexts.** In run B, P2 and P3 read *less* non-human than the E1 baseline. The constant-section organization is not adopted for Gorrund.
- **New tool.** `pads` in `race_base.limb_base` is a generic tool. It is inert unless a spec uses it, and no accepted spec does.

## 9. Conclusion on the procedural route

**The procedural generator is exhausted for Gorrund body readability under current canon.**

Over 05C, 05D and 05E, every Gorrund organization the generator can make sits inside one of two failure modes. Either it reads as bulk, or the read depends on set context. The causes:

- **Fixed silhouette.** The accepted skeleton, the locked deep-trunk / short-leg proportions and the "not fatter, wider or more muscular" canon fix the silhouette envelope.
- **Smooth soft tissue cannot carry the read.** Within that envelope the generator can only move smooth soft tissue: section radii, lofted curves, Laplacian folds. Smooth tissue redistribution on a heavy, deep-trunked human frame can always be explained as a heavy human.
- **Different situation from Grask.** Grask's read survives because its cues (dorsal / scapular mass, keel, calf-cord) *contradict* any human composition. Gorrund's cues so far *coincide* with the high-composition end of human variation.

## 10. Hand-sculpt escalation (order §10)

**Recommendation.** Commission an external hand-sculpted Gorrund base mesh, then put it through the existing guards and a fresh replicated blind gate.

**Constraints** (unchanged):
- the accepted Gorrund skeleton, joint centres, long-bone axes and bone scales;
- the stature route (230.9 cm reference, with the accepted range);
- plantigrade feet; five digits; human-compatible hands and feet;
- the protected deep-pelvis / load-path relations at skeleton-anchored stations;
- topology compatible with the MPFB / R-6 rig, so the existing composition, frame and guard tooling applies;
- 05D true-floor and volume semantics;
- no posture trick;
- no identity by fat or muscle amount;
- no canon rewrite.

**What the sculpt must change** relative to the generated body. Each cue needs **hard-form** definition: planes, edges and bony or tendinous landmarks that a heavy human cannot have, and that persist at low composition.

1. **Trunk section, S2–S5.**
   - Replace the smooth human torso with a planar, faceted slab.
   - Defined lateral edges where the anterior and lateral planes meet.
   - A broad flat sternal–abdominal plate with a crisp lower border at the costal / pubic line, not a soft belly.
   - No human pectoral shelf, nipple or navel relief, and no waist hollow.
   - Thoracolumbar depth held constant, as a structure rather than a fat mass.
2. **Posterior axial load path, from scapula to the proximal hamstring.**
   - Paired broad paraspinal load columns.
   - A flat interscapular plane.
   - A defined sacral plate with a hard transverse upper border.
   - Continuous with the hamstring origin, with no gluteal apex and no buttock fold.
   - In profile: a straight, inclined line from the upper back to mid-thigh.
3. **Pelvis → thigh.**
   - A structural hip plate with a sharp trochanteric shelf and a planar lateral thigh.
   - No round human buttock.
   - The transition as a defined step, not a smooth taper.
4. **Knee / shank / ankle.**
   - Architectural periarticular forms: a broad, flat patellar plate and defined femoral and tibial condyle blocks.
   - A shank with a squarish section, a flat anteromedial tibial plane and a defined posterior tendon column.
   - An ankle collar formed by broad malleolar blocks.
   - The leg must read as a jointed column with hard knee and ankle landmarks, not as a uniform pillar (05E run B) and not as thick thigh / thin shin (05D / E1).
5. **Elbow / forearm / wrist.**
   - A defined olecranon / epicondyle block.
   - A squarish or flattened forearm section with flat planes and a tendon border.
   - A broad wrist plate.
   - Hands unchanged in size and digit count.
6. **Shoulder girdle / neck root.**
   - A low, broad girdle integrated with the slab trunk: a trapezius plane continuous with the trunk planes.
   - No human deltoid cap; a planar shoulder block over the accepted joint.

**Acceptance path for the sculpt:**
- import onto the R-6 / MPFB topology;
- 05D / 05E guards;
- composition and frame states through the existing pipeline;
- the same replicated blind protocol (Grask E3 in every run; ref and low ≥ 2 / 3 in every run; hard-form cues cited).

Stage C for Grask E3 plus Gorrund then follows as order §9.

## 11. Files

### Added

- `tools/rac/w1/rmot05e_drivers/`:
  - `e_guard.py`: §8 guards; baseline Gorrund E1; plantigrade, hand / foot topology and proxy-floor report.
  - `e_package.py`: §6 sheets and close strips.
  - `e_sections.py`: limb profiles, taper index, sections, posterior profile.
  - `e_blind.py`: replicated blind sets J / K, Grask E3 always included.
- `reviews/rac-rmot05e-evidence/`: README, `candidates.json`, `sheets/`, `sections/`, `blind/` (2 runs: sheets, keys, raw outputs, summary), `guards/`, `search/`, `construction/`.
- `reviews/claude-rac-rm-ot-05e-gorrund-structural-readability-closure-gate.md` (this file).

### Changed

- `tools/rac/w1/race_base.py`: `limb_base` gains the `pads` periarticular collar term. It is inert without the key, so every earlier spec reproduces unchanged.
- `specs/STATUS.md`, `reviews/claude-pass2-r5-reference-mesh-queue.md`: phase state only.

No race canon file was changed. The candidate meshes are not registered as reference assets because none passed; they rebuild from `candidates.json` with `rmot05d_drivers/d_build.py` (names `GO5EP1…P3[N|B|-LOW]`).
