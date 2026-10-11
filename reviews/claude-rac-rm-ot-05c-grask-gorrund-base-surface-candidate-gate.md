# RAC RM-OT-05C — Grask / Gorrund base-surface candidate gate

**Order:** `reviews/chatgpt-rac-rm-ot-05c-grask-gorrund-base-surface-order.md`
**Evidence:** `reviews/rac-rmot05c-evidence/`
**Status:** AUTHOR CANDIDATE GATE — **acceptance standard §10 NOT MET for either race.**
- All candidates are PENDING AUTHOR / NOT ACCEPTED.
- RM-OT-05 stays OPEN.
- Nothing promoted. No D4. No canon rewrite. The exhaustive W2C / W2D suite was not run.

## 1. Summary

### What was built

A dedicated race base-surface stage, `tools/rac/w1/race_base.py`. It replaces the soft-tissue organization of the **whole composed surface** with authored race anatomy. 05B only remapped the composition tissue on top of the MPFB minimum body.

- It is applied to every composition state on the accepted 05A / 05B skeleton.
- The skeleton itself (`-LEAN`, joints, bone scales, statures) is untouched.
- A skeleton guard keeps the composition-infimum bony readings of the accepted route. With the guard, the readings at the 05B station levels moved by ≤ 0.07 cm.

### Candidates built

Six candidate directions: Grask A / B / C and Gorrund A / B / C. Each was built at:
- reference composition;
- low composition (muscle 0 / weight 0.5);
- Narrow and Broad frames;
- Grask also at a matched 229 cm.

That is 27 bodies in total, all passing the minimal guards.

### Blind read

Three independent uninformed scorers saw 20 bodies, including 8 human-family controls, with written reasons.

**Gorrund**
- 18 / 18 placements put all six Gorrund bodies in one group. No human control was pulled in, and the read holds at low composition.
- Every scorer still called them **"heavy / stocky human"**. The driver they named was the deep flat-backed slab trunk with no waist, plus thick thighs.
- An earlier run, before the corrected skeleton guard, had one scorer of three read all six as a distinct non-human organization. The delivered bodies lost that read.

**Grask**
- The references and the C-low state sit in the thin / lanky group (12 / 12 placements).
- The A and B low states fall back to "slim / ordinary human" (1 / 6).
- One scorer pulled two Marchfolk controls into the lean group.
- Every scorer called them **"thin / lanky human"**.

**Non-human reads on the delivered bodies: 0 / 36.**

### Recommendation (for author review only)

- **Grask C (assertive).** It is the only Grask direction whose organization survives low composition.
- **Gorrund B (balanced).** It reads the same as C. It carries fewer extra features (no lateral load ridges, no neck-root mass, no extended joint columns), and the A-vs-B/C difference was not visible to the scorers.

Neither recommendation is a "credible candidate" by §10, because both still read as human variants.

### Why

Every uninformed scorer judged "non-human" by **body plan**:
- limb count;
- joint arrangement;
- plantigrade feet;
- shoulder–waist–hip layout;
- proportions.

Canon locks all of those to an upright plantigrade humanoid (GRASK_V1 L65 / L138; GORRUND_V1 equivalent), and the accepted skeletons fix the proportions. Soft-tissue organization alone moved the read from "human" to "unusual human". It did not move it to "non-human".

## 2. Construction (`race_base.organize`, spec in `candidates.json`)

| Stage | What it authors |
|---|---|
| Limb sections | Each segment section r(t, φ) about its own bone axis is rebuilt as **bony floor + authored musculature**. The joint zones are held exactly, so condyles, malleoli, epicondyles and wrist keep their breadths. The shaft floor is fb × the narrowest section, with optional **tendon cords** (narrowed floor) over a t band. Muscle primitives are **bellies** (t0 → peak → t1) or **plateaus** in angular sectors. Their amplitude is solved so that **segment volume is conserved**: the organization moves mass, it never adds or removes it. |
| Trunk loft | Human relief (pectoral shelf, nipples, navel, abdominal segmentation) is removed by non-shrinking Taubin smoothing, leaving a residual `detail`. Every trunk section, including the buttock shell above the crotch, is then re-lofted as a periodic cubic through 9 authored control radii (0 … 180°) along r = (u − hip) / (sst − hip). The control curves start from the smoothed own section and are edited by authored ops: hull (no waist / lumbar hollow), line (flat wall), smooth (no gluteal apex), bump (authored mass), scale. The loft fades out round the axilla so it never folds into the arm. |
| Gluteal fold | Masked Laplacian relaxation of the posterior hip–thigh shell, posterior-facing only, so sacrum, buttock and hamstring origin form one column. |
| Yoke | Grask frontal shoulder outline pressed toward a neck-base → lateral-arm line, within the soft cap only (≤ 2–2.5 cm inward, no outward fill). |
| Skeleton guard | In the trunk / pelvis / proximal-thigh region where the ALPC stations S2–S7 are read, three rules apply. (1) An outward-normal clamp: never inside the skeleton surface. (2) A horizontal-section clamp: no vertex closer to the section centre line than its skeleton vertex. (3) Exact restoration of composition states already inside the skeleton, which is where the infimum comes from. |

The hooks are `skeleton_envelope.make(racebase=…)`, `gn3.build(racebase=…)` and `gr_body.build` / `go_body.build(racebase=…)`. The default is off, so every accepted body rebuilds unchanged.

### Route guarantee

Joints, bone scales and the skeleton surface are identical to 05B: 0.000 cm on all 27 bodies (`guards/guard_all.json`, `skeleton_unchanged`).

The composition-infimum stations read at the 05B levels differ by:
- ≤ 0.05 cm for Grask;
- ≤ 0.07 cm for Gorrund.

## 3. Candidate directions

| | Grask (218 cm) | Gorrund (230.9 cm) |
|---|---|---|
| **A — restrained** | Long-tendon limbs at half strength: high, short calf / forearm / thigh / upper-arm bellies with distal cords at k × 0.5. Pectoral relief smoothed. Gluteal mass flattened over the sacrum and lowered at the fold. Light fold relaxation. | Axial chain only: flat abdominal wall from sternum to pubis; no waist (lateral hull); continuous posterior column from upper back to sacrum (posterior hull + smoothing); pectoral plastron; gluteal fold relaxed. Human limbs. |
| **B — balanced** | A at 0.8 tendon strength, plus scapular / latissimus "wing" mass along the long back (2.5 cm), plus soft-cap yoke (integrated girdle), plus stronger fold relaxation. | A, plus columnar limb musculature: plateau muscle profile on thigh / shank / upper arm / forearm, no human calf or biceps bellies, column meeting the joints. |
| **C — assertive** | Full tendon strength (shank cord k 0.38, forearm 0.35), 4 cm scapular / latissimus wing, soft-cap yoke, sternal keel ridge, strongest fold relaxation. | B, plus graviportal joints (column carried down to j1 0.96: thick ankles / wrists), lateral load ridges on thigh and shank, upper-back / neck-root mass. |

None of the six differs from its siblings by composition, stature or global width. All share the same skeleton and composition amount; volume vs 05B is −2.4 … −3.0 % for Grask and +0.9 … +2.4 % for Gorrund.

## 4. Visual evidence (§7.1)

All sheets are in `sheets/`:
- body only, matched orthographic camera, one ground plane, neutral grey, R-6 stance;
- Skarn at matched height, the Marchfolk reference control and the provisional 05B body on every candidate sheet.

The sheet sets are:
- **Candidates:** `c_GR_{F,Q,P,RQ}_grey`, `c_GR_{F,P}_sil`, and the same for `c_GO_*`.
- **Low composition:** `c_GR_low_*`, `c_GO_low_*`, in grey and silhouette.
- **Frames:** `c_GR_frames_*`, `c_GO_frames_*` (Narrow / reference / Broad for every candidate).
- **Grask matched 229:** `c_GR_229_*`, against Skarn 229.
- **Close architecture strips:** `c_218_*` (Grask) and `c_229_*` (Gorrund), covering shoulder, thorax, pelvis, knee, elbow, hand, foot and ankle.

## 5. Blind read (§7.2)

**Set:** 20 bodies, shuffled with a fixed seed, codes R01–R20, key never shown. Body only, height-normalized, front + profile, one grey sheet and one silhouette sheet. The bodies were:
- 8 human-family controls: Marchfolk and Skarn × reference / Narrow / Broad / low;
- Grask A / B / C at reference and low;
- Gorrund A / B / C at reference and low.

**Scorers:** 3 independent uninformed scorers. Each gave a grouping, a per-body description and an (a) ordinary human / (b) unusual human / (c) non-human class, with written reasons and the driving feature.

**Gate run** (delivered bodies, `blind/blind_results.json`):

| Body | Scorer 1 | Scorer 2 | Scorer 3 |
|---|---|---|---|
| GO-A / B / C ref | heavy / stocky group, (b) | broad deep heavy group, (b) | deep slab-torso group, (b) |
| GO-A / B / C low | same group, (b) | same group, (b) | same group, (b) |
| GR-A / B / C ref | lean group, (b) thin | narrow slim group, (b) thin | slim long-limbed group, (b) thin / lanky |
| GR-C low | lean group, (b) | narrow slim group, (b) | slim group, (b) |
| GR-A low | average, (a) | average, (a) slightly thin | ordinary, (a) / (b) stocky legs |
| GR-B low | average, (a) | narrow slim group, (a) slightly thin | ordinary, (a) / (b) stocky legs |
| Human-family controls | MF ref + MF Narrow pulled into the lean group; rest ordinary / soft | all ordinary / soft | all ordinary / soft |

### Scorers' words

- **Gorrund:** "deep, flat-backed slab trunk with no waist or glute curve and thick thighs … without the torso depth they would merge into ordinary humans."
- **Grask:** "narrow, shallow torso and thin limbs … without it they would look ordinary."

### Earlier runs (search, same protocol)

- **Run 1** (bodies before the outward-normal guard): one scorer of three classed all six Gorrund bodies **(c) non-human**: "the profile trunk is a flat-backed oval with no waist or buttock, and the thigh-to-shin step is abrupt." The other two read stocky human. Grask was lanky in all three.
- **Run 2:** 0 / 3 non-human.

The guard restores pelvic / gluteal skin where the organization had cut inside the skeleton surface. That is exactly where the strongest non-human Gorrund cue came from (§8).

## 6. Minimal guards (§8) — `guards/guard_all.json`, 27 bodies

| Guard | Result |
|---|---|
| Stature | Identical to 05B on every body: GR 217.99 / 228.99, GO 230.90; low states 217.21 / 230.75 |
| Ground contact | Pass on all bodies: lowest vertex at u = 0, both feet < 0.3 cm |
| No uniform scaling / skeleton unchanged | Pass: joint and `-LEAN` vertex Δ = 0.000 cm |
| Gross self-intersection | Pass. Piercing-edge count ≤ the same route without 05C (+10), and the axilla / crotch contacts of the MPFB route remain. GR ref 146 / 150 / 158 vs route 157. GO ref 62 / 53 / 48 vs route 67. Lows ≤ route + 6. 05B was lower than the route for Gorrund (13), because its surface stage pulled the axilla in. |
| Arm / trunk clearance | Pass on all 27 bodies: 0 vertices inside the closed trunk section; minimum arm–trunk gap 1.14–1.64 cm |
| Composition firewall | Limb organization is volume-conserving per segment. Trunk loft and fold are not strictly volume-conserving: body volume vs 05B is −2.4 … −3.0 % for Grask and +0.9 … +2.4 % for Gorrund. The same spec is applied to every composition state, so composition still sets the amount. The organization survives low composition for Grask C and all Gorrund candidates, but not for Grask A or B (blind). |
| **GR-P2b** (bitrochanteric ÷ crest ≥ MF 1.1918) | 218 cm and frames: pass (1.1953–1.1968 vs 05B 1.1968–1.1972). 229 cm: 1.1912–1.1916 vs MF 1.1918. This is **the same marginal non-pass as 05B GR5B229 (1.1916)**, not introduced by 05C. |
| **GR-P6** (pelvis ÷ thorax breadth ≈ MF) | Unchanged from 05B at every height and frame (Δ ≤ 0.0001) |
| **Gorrund deep pelvis** | The skeletal pelvic depth ÷ thoracic depth at the 05B levels is unchanged (0.8623 / 0.8600 / 0.8686 = 05B). Skin pelvic AP at the hip is 32.9–33.1 cm vs 05B 33.3 cm, so the deep pelvis is not trivially destroyed. The old human glute / belly morphology was not restored to satisfy skin rows. |
| Posture / presentation tricks | None. Same R-6 stance, camera and material as every prior gate. |

### Measurement note

The skeletal proxy's own ALPC level search re-anchors the thorax-maximum (S2) and waist-minimum (S4) levels on each body's **reference skin**. The Gorrund organization removes the waist and re-lofts the thorax, so the own-level S2 search lands at a different height. The own-level Gorrund pelvis ÷ thorax breadth therefore reads 1.219 vs 1.016, although the bony stations at the same anatomical levels are unchanged.

The full numerical gate (next order) needs skeleton-anchored station levels for organized surfaces, or this will read as false regressions.

## 7. Rejected / not carried

| Tried | Why rejected |
|---|---|
| Tissue-only reorganization on the unmodified MPFB minimum body | The human calf / deltoid / waist / gluteal organization lives in the `-LEAN` surface, and tissue is only 1–4 cm. Visually indistinguishable from 05B (search s1–s3). |
| Writing the race base back into the skeleton (`-LEAN`) | Changes the skeleton that the CIB, skeletal proxy and ALPC read. Rejected for "accepted skeleton unchanged". |
| Radial trunk ops (hull / flat / shift) on raw sections | Section-centre jumps made horizontal creases and lumps; it read as fat (s3–s5). Replaced by the smoothed-centre loft. |
| Taubin relaxation of the gluteal fold | Non-shrinking smoothing inflated the buttocks (f1). Replaced by masked Laplacian. |
| Laplacian fold at 200–600 iterations | Destroyed the crotch and thigh separation (f2). |
| Outward yoke fill (trapezius concavity) | Pushed shoulder surface into the arm: piercing edges 157 → 194–208. Inward-only cap pressing kept. |
| Unblurred loft field | Bin noise wrinkles (s9). The loft field is now smoothed; relief removal is never blurred. |
| Strong muscle-belly contrast at a low floor (fb 0.78) | 9–13 cm belly amplitudes, caricature "lumps" (s1). Floor raised to 0.95 for Grask, with tendon cords instead. |
| Very low trunk `detail` (0.1) for Gorrund | Read as juvenile / infant (round, featureless). Rejected under the adult-read rule. Gorrund `detail` is 0.35. |
| Organization below the composition infimum (first two full builds) | GR-P2b and the Gorrund bony stations moved, because grid states cut inside the skeleton or relieved states that were already inside it. Replaced by the three-part skeleton guard. |

## 8. Does either race still read human, and why

**Yes, both.**

**Gorrund** is a stable, separable cluster, but read as a heavy / stocky human. The cues that pushed one scorer to "non-human" in run 1 were:
- the posterior hip region becoming one flat slab with the back, with no buttock;
- the abrupt thigh-to-shin step.

The skeleton guard removed most of the first cue. Wherever the MPFB skeleton surface carries a human buttock, the guard restores it, because the CIB / ALPC pelvic stations are read there. The remaining cues (deep slab trunk, no waist, columnar limbs) are read as human bulk.

**Grask** reads thin / lanky.
- The long-tendon organization (high short bellies, distal cords, knobby knees and elbows) is visible in profile and in the close strips. At body scale, though, it reads as "thin limbs".
- The integrated girdle cannot pass the bony humeral head and acromion; the cap is ≤ 2.5 cm of soft tissue.
- Pelvis-to-thigh organization is bounded by GR-P2b / GR-P6.
- At low composition, A and B lose their tendon/belly contrast with the tissue and fall back to "slim human".

## 9. Canon guards that prevented a stronger solution

1. **Plantigrade humanoid body plan, five digits, normal joint arrangement, no posture tricks.** GRASK_V1 L65, L138, L644; Gorrund equivalent. Every scorer's criterion for "non-human" is a body-plan change, which canon forbids.
2. **Accepted skeleton and proportions locked** (§2). Stature, limb / torso shares and joint breadths are fixed. Soft tissue cannot change the silhouette's proportion read.
3. **Skeleton surface as the bony guard (AD-G14 CIB / ALPC on the `-LEAN` surface).** The `-LEAN` is the MPFB minimum body and still carries a human buttock, chest and shoulder cap. These count as "bone" for the guards, so the organization may not go inside them. This guard removed Gorrund's strongest non-human cue (run 1 → gate run).
4. **GR-P2b / GR-P6** (Grask pelvic relations, with external hip width kept distinct from skeletal pelvis). This blocks Grask hip and gluteal reshaping beyond the soft shell.
5. **Shoulder joint not moved by muscle** (GRASK_V1 L72) **and the bony humeral head.** The Grask "no deltoid cap" girdle is limited to ≤ 2.5 cm of soft cap.
6. **Adult read; no juvenile, caricature or sex-coded anatomy.** This limits relief removal: a fully smoothed Gorrund reads infantile.

## 10. Provenance finding (05B)

`race_surface._normals()` returns **inward** normals on this mesh (negative signed volume; the chest-front normal points −y). The 05B "skeleton guard" therefore blocked *outward* growth beyond the original and did not block inward cuts. That is the opposite of its documented intent (05B gate §2 table, "never cuts inside the skeleton-envelope surface").

This did not decide the 05B bony readings checked here. Where a 05B composition-infimum station lies inside the skeleton (for example the Gorrund crest S5, set by the muscle-0.5 grid state), the same value appears on the plain route. It comes from the donor's own negative tissue difference, not from the guard.

05B is not promoted, so nothing accepted depends on it. A comment now documents this in `race_surface.py`, and the behaviour is unchanged so the 05B evidence reproduces. 05C uses outward normals (`race_base._onormals`).

## 11. Files

### Added

- `tools/rac/w1/race_base.py`: the 05C base-surface organization.
- `tools/rac/w1/rmot05c_drivers/`: `c_build.py`, `c_package.py`, `c_blind.py`, `c_guard.py`, `c_evidence.py`, `c_preview.py`, `c_try.py`, `c_lean.py`, `c_sx.py`, `c_blindq.py`.
- `reviews/rac-rmot05c-evidence/`: README, `candidates.json`, `sheets/` (57), `blind/`, `guards/`, `construction/`, `search/`.
- `reviews/reference-assets/r6/`: GR5C{A,B,C}, GR5C{A,B,C}-LOW, GR5C{A,B,C}229, GR5C{A,B,C}{N,B}, GO5C{A,B,C}, GO5C{A,B,C}-LOW, GO5C{A,B,C}{N,B} (`_r6.npz`, 27 files).

### Changed

- `tools/rac/w1/skeleton_envelope.py`: `racebase=` hook; the spec rides in the skeleton meta and organizes every composition state; guard against the skeleton.
- `tools/rac/w1/w1g_drivers/gn3.py`, `w2c_drivers/gr_body.py`, `w2d_drivers/go_body.py`: `racebase=` pass-through; recorded in build records.
- `tools/rac/w1/race_surface.py`: comment only (§10).
- `reviews/reference-assets/manifest.json`: 27 entries, PENDING AUTHOR / NOT ACCEPTED.
- `specs/STATUS.md`, `reviews/claude-pass2-r5-reference-mesh-queue.md`: status lines.
- `specs/grask/GRASK_V1.md`, `specs/gorrund/GORRUND_V1.md`: RM-OT-05C status line only; no canon change.

## 12. Stop

Stopped at the RM-OT-05C candidate gate, as ordered:
- no candidate promoted;
- RM-OT-05 not closed;
- no exhaustive validator suite;
- no D4.

### Author decisions needed

1. **Select a candidate** for biology (or none). Claude recommends Grask C and Gorrund B for review, with the caveat above.
2. **Decide whether a guard in §9 may be relaxed.** The most consequential is §9.3, the MPFB minimum body standing in for bone at the pelvis and shoulder.
3. **Decide whether the gate needs an externally hand-sculpted base mesh** made in a DCC tool. That is not available in this environment.
