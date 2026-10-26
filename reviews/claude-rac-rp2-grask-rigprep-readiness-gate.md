# RAC RP2 — Grask rig-preparation readiness and landmark review — gate (proposal v001)

**Date:** 2026-10-25  
**Order:** `reviews/chatgpt-rac-rp2-grask-rigprep-readiness-and-landmark-review-order.md` (c6db89c)  
**Parents:** freeze `59aacfe`, closure hash record `59ffd1c`  
**State:** **retopology frozen; rigprep readiness proposal awaiting ChatGPT review.**

This stage is **not passed**, and Grask is **not production-rig-ready**. The internal joint centres are not determinable from the frozen surface to better than about ±5 cm (§5). Several required components are missing: the scapular medial border, a jaw/oral anatomy and eyeballs (§4). The deliverable is evidence plus a concrete proposal.

Nothing was built, weighted or posed:
- no armature (final or diagnostic);
- no skin weights, no posing, no corrective deformation, no creator morphs;
- no UVs, materials, LODs or UE5 work;
- no other race.

No mesh was edited or saved.

**Evidence:** `reviews/rac-rp2-evidence/grask_rigprep_readiness_v001/`

| Item | Location |
|---|---|
| Proposal | `GR_U_REF_RP2_rigprep_landmarks_v001.json` |
| Readable tables | `GR_U_REF_RP2_rigprep_landmarks_v001_tables.md` and `.csv` |
| Raw measurements | `raw/fit_v005.json`, `raw/fit_v003.json` |
| Sheets | `sheets/` |
| Parent hashes | `hashes/` |

**Tools:** `tools/rac/rp/grask_rigprep_v001/` (`run_rigprep.sh` reproduces everything).

---

## 1. Parent integrity: before and after

All parents were re-staged fresh from the PC (`E:/…/RaceBodies/production/Grask/RP2/`) and hashed before any inspection, then again after all work. Before and after are identical (`hashes/hashes_before.txt`, `hashes/hashes_after.txt`).

| Parent | SHA-256 | Geometry hash |
|---|---|---|
| `GR_U_REF_RP2_retopo_v003.blend` | `03bfe7d9…7ce0` ✔ | `f9c4a7ac…702f` ✔ (170,466 V / 170,464 faces) |
| `GR_U_REF_RP2_SOURCE_3D_v005.blend` | `7bba8d2d…ab14` ✔ | `2697929d…d7bc` ✔ (590,764 V / 1,181,524 tris) |
| v003 sidecar | `808cf772…8ed5b` ✔ | |
| v003 landmarks | `aafbe617…ff09` ✔ | |
| v003 FREEZE record | `6ed226bb…2172355` ✔ | |
| v002 blend / sidecar / landmarks | `49ae8a6e…` / `2dbd7221…` / `48887566…` ✔ | |
| v001 blend / sidecar / landmarks | `82c10a64…` / `ed579e0b…` / `a22c3959…` ✔ | |
| v005 sidecar / masks / glb | `77498cdb…` / `b5640e79…` / `81f872e7…` | |

The analysis copies used for measurement were proven equal to the blends (`hashes/npzcheck.txt`):
- v005 npz vs blend: max difference 1.2e-5 cm (float32 rounding);
- v003 freeze read-back npz vs blend: 0.0, with the production translation undone.

All measurement is in the v005 source frame. v003 was compared in the same frame, with no display offset.

---

## 2. Audit of the frozen landmark package

The audit covers all 74 records of `GR_U_REF_RP2_retopo_v003_landmarks.json`; table §1 of the tables file lists each one.

| Audited provenance | Records | Independent measurement? |
|---|---|---|
| Independently measured surface landmark (`surface-fit`) | 12 | yes (surface only) |
| Fitted joint-centre estimate (`prior-seed+surface-fit`) | 18 | the T-6 *re-measurement* is independent; the *placement* is not (see below) |
| Copied construction coordinate | 42 | **no** (drift 0 by construction) |
| Rule-based estimate (heuristic offset) | 2 (`jaw_hinge_l/r`) | **no** |

### 2.1 Findings

1. **The 18 internal centres are not independent of the superseded MPFB skeleton.**
   - Their placement is the old Grask E3 (MPFB) joint, shifted by a section-centroid difference.
   - Their T-6 drift (max 0.06 mm) shows only that v003 reproduces v005. It says nothing about whether the centres are anatomically right.
2. **Several frozen E3-seeded centres sit close to the skin of v005:**

   | Centre | Distance to surface |
   |---|---|
   | hips | 2.9 / 3.1 cm (near the gluteal skin) |
   | `glenohumeral_r` | 1.7 cm (0.43 cm below its acromion marker) |
   | `glenohumeral_l` | 2.8 cm |
   | elbows | 2.8 / 3.0 cm (posterior) |

   The frozen sternoclavicular centres are 7–8 cm deep, about 10 cm behind the anterior skin summit beside the jugular notch.
3. **`jaw_hinge_l/r` is mislabelled.** The frozen package tags it "construction coordinate (copied)". It is really an offset rule from the ear root (2.2 cm anterior, 2 cm below, 1.5 cm medial), because there is no jaw in the source. The frozen file is not changed; the proposal records the correct class.
4. **The frozen axes are single vectors, not frames.** Only 12 records carry an axis. Knee and ankle use pure +x, and the hip uses the thigh direction. None is an orthonormal frame.
5. **The frozen surface markers are fine as surface markers.** These are the acromion, scapular inferior proxy, crown, chin, ear root/tip and mouth corners. They are carried unchanged. The acromion is defined by a ray above the frozen glenohumeral centre, so it inherits that seed's lateral position.

---

## 3. Method: how the proposal was built

**Code:** `rigprep_fit.py` measures, `compose.py` assembles.

**Superseded skeleton not used:** the MPFB/E3 skeleton is **not read**. Its only trace is the frozen package value, which appears as alternative **C**.

**Internal centres (18):**
- each is measured on v005 by one or two independent surface definitions (**A**, **B**), with the frozen value **C** as a further alternative;
- **proposal** = coordinate median of A, B and C (the midpoint when there are two);
- **uncertainty** = the largest distance from the proposal to any alternative;
- **status:** "usable (diagnostic)" only if that distance is ≤ 1.0 cm, otherwise "provisional".

Small numerical fitting residuals are reported but are not counted as anatomical certainty.

**Construction joints:**
- these are the hand/foot MCP, PIP, DIP, tips, thumb CMC/MCP/IP, toe MTP/IP, wrist and eyes;
- they are carried exactly from the frozen v005 construction model (`/tmp/claude-0/src3d/v5/tools`);
- each is validated against the v005 surface: inside test, depth, digit-section centroid offset and surface tip.

**Surface markers:** carried from the frozen package.

**v003 cross-check:**
- the same code was re-run on the frozen v003 read-back;
- Δ = how far the proposal moves;
- this shows method stability on the production surface. It is **not** accuracy, and it is 0 by construction for copied joints.

**Asymmetry:** each side was measured separately (§7). Nothing was mirrored.

**Frames:**
- production cm = source + (−0.11180, +5.72272, 0);
- Blender m = (x, −f, u)/100;
- the analysis frame is **left-handed** (x × f = −u). Local frames are therefore defined right-handed in Blender and have det −1 when written in analysis coordinates. Both forms are in the JSON.

---

## 4. Contract §12 coverage

| §12 item | Status | Reason |
|---|---|---|
| Pelvis root | **provisional** (±4.8 cm) | Internal. A = hip midpoint, B = torso-section centroid, C = frozen. The production origin stays the frozen pelvis_root projection; the proposed root lies 2.8 cm anterior of the frozen point at the same height |
| Hip centres L/R | **provisional** (±5.9 / ±5.6 cm) | Femoral head is internal. The source has **no trochanteric relief** (lateral hip contour monotonic, widest at the thigh). A = soft-tissue thigh axis at the inguinal fold (z 115.8 / 116.0), C = frozen (z 122.3, 2.9–3.1 cm under the gluteal skin) |
| Knee centre + flexion axis | **provisional** (±4.6 / ±6.3 cm) | **No condylar relief.** A = knee waist (z 67.2 / 65.7), B = patellar flattening (z 75.7 / 73.7), C = frozen (z 71.2). Axis = mediolateral |
| Ankle centre + axis | **provisional** (±6.1 / ±6.5 cm) | **No malleolar relief** (medial/lateral extents show no bump), so the talocrural obliquity is unsupported. A = anterior ankle crease (z 13.5 / 13.75), B = Achilles concavity (z 19.5 / 20.25), C = frozen (z 9.2 / 9.3). Axis = mediolateral |
| Ball (MTP) line | **usable** (construction) | Hallux → toe5 MTP construction joints, 1.0–2.1 cm inside the forefoot |
| Toe joints + tips (5 per foot) | **usable** (construction) | Every IP joint within 0.14 cm of its toe-section centroid; tips 0.4–0.95 cm inside the surface tip |
| Sternoclavicular | **provisional** (±5.1 cm) | Joint depth is not expressed by the surface. A = skin summit beside the jugular notch, C = frozen (about 10 cm deeper) |
| Clavicle end / acromion | **usable** (surface marker) | Frozen measured marker. Its lateral position derives from the frozen glenohumeral seed |
| Scapular proxy: inferior angle | **provisional** (surface proxy only) | Frozen posterior-summit proxy; no bony scapula in the source |
| Scapular proxy: medial border | **missing** | Not measured, and not invented (GR-G2 rule: "Do not invent a scapula landmark") |
| Glenohumeral centre | **provisional** (±6.0 / ±9.3 cm) | The upper arm is free only below the armpit contact (z ≈ 154); above it, arm and torso are one mass. A = sphere on the lateral/superior cap (r 9.5 / 13.1 cm), B = sphere on the lateral deltoid (r 9.7 / 10.2 cm), C = frozen. The spheres sit 6–7.6 cm below the acromion; C sits 0.4–2.2 cm below it |
| Elbow centre + axis | **provisional** (±5.1 / ±4.8 cm) | A = minimum-area section (z 142.8 / 143.0), B = cubital fossa (z 141.3 / 141.5), C = frozen (z 147.5 / 147.6, 2.8–3.0 cm under the posterior skin). Axis = the bend axis of the reference-stance arm (stance flexion 7.0° L / 15.6° R) |
| Wrist centre + axis | **usable** (construction) | v005 hand-frame origin; the section centroid there lies within 0.1 cm. Longitudinal placement is construction-defined (the forearm waist is 7.0 cm proximal). Frame = construction hand frame |
| Finger roots (MCP) and tips | **usable** (construction) | MCP 1.5–1.8 cm inside the palm; tips 0.42–0.50 cm from the surface tip |
| Finger PIP/DIP | **usable** (construction) | Digit-section offset ≤ 0.10 cm |
| Thumb CMC (+ MCP, IP, tip) | **usable** (construction) | CMC 2.15 cm inside the thenar mass; IP section offset 0.03 cm |
| Spine stations (3) | **provisional** (±2.7 / ±1.4 / ±1.5 cm) | No vertebral anatomy. A = torso-section centroid, C = frozen. Heights are carried from the frozen package, which inherits the MPFB station heights. **The spine_03 → neck_base gap is 39.2 cm** |
| Neck base | **usable (diagnostic)** (±0.7 cm) | A = section centroid, C = frozen |
| Head (atlanto-occipital) pivot | **provisional** (±1.3 cm) | Internal. A = neck/head section centroid at the mean ear-root height, C = frozen |
| Crown | **usable** (surface marker) | |
| Jaw hinge L/R | **provisional / no jaw anatomy** | **Closed sculpted mouth:** 0 inward-facing faces behind the lip seam; no oral cavity and no mandible. Rule-based offset only |
| Chin | **usable** (surface marker) | |
| Eye centres L/R | **usable** (construction) | v003 eyeball-volume centre, confirmed by an independent sphere fit on the eye surface (offset 0.10 / 0.15 cm, r 1.51 / 1.38 cm). **No separate eyeball objects:** eyes are sculpted surface on the single body mesh |
| Mouth corners | **usable** (surface marker) | Closed mouth, as above |
| Ear root / tip | **usable** (surface marker) | |
| Tail | **not applicable** | Grask has no tail |

**Totals:** 116 proposal records.

| Status | Records |
|---|---|
| usable (construction) | 84 |
| usable (surface marker) | 10 |
| usable (diagnostic) | 1 |
| provisional | 17 |
| provisional (surface proxy only) | 2 |
| provisional (no jaw anatomy) | 2 |
| missing | 1 item (scapular medial border, both sides) |

---

## 5. Proposed internal centres

Production cm (x = subject left, f = forward, u = up). Full alternatives are in tables §3, and Blender metres in tables §2 and the JSON.

| Joint | Proposal L | Proposal R | Uncertainty L / R (cm) | Depth in v005 (cm) | v003 Δ (cm) |
|---|---|---|---|---|---|
| pelvis_root | (0.00, 2.80, 123.93) | — | 4.84 | 11.3 | 0.002 |
| hip | (12.11, 2.85, 119.03) | (−12.11, 2.76, 119.16) | 5.87 / 5.61 | 6.7 / 6.6 | 0.002 |
| knee | (13.66, 1.01, 71.17) | (−13.16, 1.25, 71.20) | 4.65 / 6.27 | 5.9 / 5.7 | ≤ 0.002 |
| ankle | (15.53, 0.23, 13.50) | (−15.50, −1.11, 13.75) | 6.05 / 6.54 | 4.4 / 4.2 | ≤ 0.001 |
| sternoclavicular | (3.30, 6.41, 179.48) | (−2.32, 6.40, 179.53) | 5.10 / 5.08 | 3.7 / 3.9 | 0.45 / 0.20 |
| glenohumeral | (17.85, −1.36, 173.71) | (−19.23, 1.63, 170.82) | 5.97 / 9.28 | 6.7 / 5.7 | 0.37 / 0.28 |
| elbow | (26.06, −2.62, 142.77) | (−26.82, −2.88, 142.99) | 5.09 / 4.82 | 3.5 / 3.8 | ≤ 0.003 |
| spine_01 / 02 / 03 | (0.00, −0.02, 133.88) / (−0.21, 0.62, 142.42) / (−0.47, 0.19, 150.04) | — | 2.74 / 1.42 / 1.52 | 8.0–8.4 | ≤ 0.001 |
| neck_base | (0.28, 2.06, 189.14) | — | 0.69 | 5.4 | 0.001 |
| head_pivot | (−0.08, 8.49, 200.18) | — | 1.28 | 7.4 | 0.002 |

**Reading this table:**
- All proposals lie inside v005, at least 3.5 cm from the surface.
- The v003 deltas are ≤ 0.003 cm for every section-based definition and ≤ 0.45 cm for the sphere and skin-summit fits (GH, SC). The definitions are stable on the frozen production surface.
- The uncertainties say the surface does not pin these centres. For example, the knee alternatives span 8.5 cm along the leg.

**The three largest disagreements:**

| Joint | Disagreement |
|---|---|
| Glenohumeral | Spheres vs frozen: 5–9 cm. The fitted spheres are large (r 9.5–13 cm), so they describe the deltoid/trapezius mass, not a humeral head |
| Ankle level | 9.2–20.3 cm: no malleoli |
| Hip AP depth | Thigh axis at the fold f = 7.7, frozen f = −2.0: about 9.6 cm |

---

## 6. Construction joints: surface validation

Per-joint values are in tables §5.

| Joints | Result |
|---|---|
| 40 hand joints | All inside v005. Finger/thumb IP section-centroid offsets 0.01–0.10 cm. MCP depth 1.46–1.78 cm; thumb CMC 2.15 cm; MCP and CMC sit inside the palm mass, where no digit section exists |
| Fingertip construction ends | 0.42–0.50 cm short of the surface tip (the pad) |
| 38 foot joints | All inside v005. Toe IP offsets 0.00–0.14 cm (toe5 PIP: no isolable section). MTP depth 1.0–2.1 cm; tips 0.41–0.95 cm from the surface tip |
| Wrists | Section centroid within 0.1 cm (ML/AP) |
| Eyes | Independent sphere within 0.10 / 0.15 cm |

**Limitation:** construction joints are exact *by definition* of the source build. Their validation shows they are centred in the digits. It does not show they are anatomical joint centres in the biological sense.

---

## 7. Axes, segments and asymmetry

### 7.1 Frames (tables §4)

- **Convention:** right-handed in Blender; **X** = flexion axis, oriented toward the subject's left (+X) on **both** sides; **Y** = toward the child joint; **Z** = X × Y.
- **Flexion sign:** recorded per joint as positive or negative rotation about local +X, with the technical flexion direction used to test it.
  - knee: positive = ankle moves posterior;
  - hip, glenohumeral and elbow: negative;
  - wrist and digits: positive = palmar/plantar.
- **Where X comes from:**
  - elbow: the reference-stance bend axis (upper-arm axis × forearm axis);
  - wrist: the construction hand frame (v = radial);
  - digits: the construction lateral axis;
  - knee, ankle, hip, shoulder and trunk: mediolateral (+x orthogonalised to Y). No anatomical evidence supports an oblique axis there.
- **Not defined:** girdle (SC), jaw and eye axes.

### 7.2 Segments and asymmetry (tables §6–7)

**Segment lengths (L / R, cm):**

| Segment | L | R |
|---|---|---|
| pelvis → hip | 13.06 | 13.02 |
| hip → knee | 47.92 | 47.99 |
| knee → ankle | 57.70 | 57.54 |
| SC → GH | 17.47 | 19.61 |
| GH → elbow | 32.03 | 29.20 |
| elbow → wrist | 39.24 | 39.44 |
| ankle → ball | 22.88 | 24.18 |

- **Digits are bilaterally identical.** The construction is mirrored.
- **Largest asymmetry: the shoulder.** The GH proposals differ by 3.0 cm in f and 2.9 cm in u. This is partly the documented source shoulder-line asymmetry (`claude-rac-rp2-grask-asymmetry-adjudication.md`) and partly unstable sphere fits on a broad cap. It is not mirrored away.
- **Ankle:** L sits 1.3 cm more anterior than R. The frozen ankles show the same 1.4 cm difference.

---

## 8. Visual review package

All sheets are under `sheets/`. Each has a v005 clay version and a v003 clay + wireframe version, rendered with identical orthographic cameras in the v005 frame, with no display offset.

| Sheet | Content |
|---|---|
| `Sa1_body_v005`, `Sb1_body_v003w` | Whole body front, left side, rear and 3/4 with labelled centres, uncertainty circles and X/Y/Z axes |
| `S2_girdle_shoulder_*` | Shoulder/girdle closeups, both sides (front and side) |
| `S3_pelvis_hip_*` | Pelvis/hip front and both sides (side views with the hanging arm removed, so the hip is unobstructed) |
| `S4_elbow_*`, `S5_knee_*` | Elbow and knee, front and side, both sides |
| `S6_wrist_*`, `S7_ankle_*` | Wrist and ankle, front and side, both sides |
| `S8_hand_l_*`, `S8_hand_r_*` | Isolated hand crops (dorsal, palmar, radial, ulnar) with every MCP/PIP/DIP/tip and thumb CMC/MCP/IP/tip and 2 cm axes |
| `S9_foot_l_*`, `S9_foot_r_*` | Isolated foot crops (top, medial, lateral) with the MTP line and toe joints |
| `S10_head_neck_jaw_*` | Head front/side/3-4, jaw closeup and neck side, with the missing-anatomy notes |

**Legend (on every sheet):**
- red diamond = new fitted proposal, with its uncertainty circle;
- orange ring = alternative A/B;
- grey × = frozen value C;
- green square = copied construction joint;
- blue disc = measured surface landmark;
- purple triangle = rule-based estimate.

**Rendering notes:**
- Markers are projected onto the image; internal centres lie inside the body.
- Side views show only the near side.
- Overlays are 2-D only. The clay scenes are derived inspection scenes built from the npz and never saved.

---

## 9. Diagnostic deformation test proposal (plan only; nothing was run)

### 9.1 How a later diagnostic copy would work

This runs only after the author decisions in §10 and a separate execution order.

1. **Copy, never overwrite.** Copy the frozen v003 to `GR_U_REF_RP2_rigdiag_v001.blend`. The v003 file, its sidecars, landmarks and freeze record are never written.
2. **Build the diagnostic armature from the accepted centres and frames.** Bone heads and tails sit exactly on the landmark centres. Bone lengths equal the landmark segment lengths (§4 rule 2a; checked to T-6 ≤ 1.0 mm).
3. **Diagnostic weights only.** Automatic heat weights, which are not production weights.
4. **Rest pose = reference stance,** with the 8° arm abduction kept.
5. **Run each test pose, then return to rest.** On return the mesh must match the frozen v003 within T-1 (body max ≤ 3.0 mm; identity zones max ≤ 1.5 mm), measured by the existing deviation tool. LBS is exactly invertible, so the expected result is about 0.
6. **Re-measure the T-6 surface landmarks on the returned mesh.** Target ≤ 1.0 mm, none above 1.5 mm.

### 9.2 Measurements used by every test

- self-intersection pairs (sxq), excluding listed contact zones;
- new folded edges (dihedral > 120°) and flipped faces, counted against the reference;
- per-zone volume change, using the loop-tagged zones;
- p95 edge-length strain;
- loop-spacing collapse at the joint loops;
- identical-camera clay and wireframe sheets, before and after.

### 9.3 Defects vs intentional anatomy

Every test reports these areas separately and does not count them as defects:
- **Intentional source hollows:** the accepted v005 thumb–index web hollow.
- **Contact anatomy:**
  - arm–torso contact below the armpit at z ≈ 154 in the stance;
  - palm-to-thigh proximity;
  - belly–thigh, calf–thigh and chin–chest contact in deep flexion;
  - the ring–pinky web with its accepted quad exception.

A defect is a change that is not explained by the contact or the hollow: a fold, a flip, a non-contact intersection, a collapse, or volume loss beyond the threshold.

### 9.4 Tests

The angles are technical test proposals. They are **not** canon range-of-motion limits, and no biological constraint is implied.

| # | Test | Poses (from the reference stance) | Purpose / risk zones | Evidence views | Pass / fail (proposed) |
|---|---|---|---|---|---|
| D1 | Shoulder elevation + axillary clearance | Abduction to 45° and 90°; flexion 90°; extension 30° | GH placement; axillary fold, deltoid cap, lat/pectoral borders, trapezius slope (GR-G2 girdle read) | Front, rear, 3/4, axilla closeup | 0 non-contact intersections; axillary gap > 0 at 45°; shoulder-zone volume within ±5 %; no fold or flip; acromion marker stays on the cap |
| D2 | Elbow flexion | 90° and 130° | Elbow centre level; cubital crease, olecranon | Side, front, crease closeup | Crease contact depth ≤ 2 mm and inside the crease zone only; forearm and upper-arm volume within ±3 %; no flip |
| D3 | Wrist | Flexion and extension ±60°; radial/ulnar ±20° | Construction frame origin; dorsal / palmar wrist | Radial, ulnar, dorsal | No intersection; wrist-ring loop spacing ≥ 50 % of rest |
| D4 | Finger curl and spread | Fist: MCP 90°, PIP 100°, DIP 70°; spread ±10° | Knuckle and IP creases; palm webs, nails | Hand dorsal, palmar, radial, ulnar | No finger-to-finger intersection outside the pad contact; nail-plate rigid-deviation ≤ 0.3 mm; no flip |
| D5 | Thumb opposition | CMC + MCP to the index tip and to the pinky base | Thumb CMC; thenar mass, thumb–index web | Palmar, radial | Accepted hollow reported, not failed; no non-contact intersection; thenar volume within ±5 % |
| D6 | Hip flexion and abduction | Flexion 45° and 90°; abduction 30° | Hip depth/level; groin, inguinal fold, gluteal fold | Side, front, rear | Belly–thigh contact marked as contact; gluteal-fold no fold or flip; zone volume within ±5 % |
| D7 | Knee flexion | 90° and 140° | Knee level; popliteal crease, patella | Side, front, rear | Calf–thigh contact only in deep flexion and marked as contact; patella read kept; no flip |
| D8 | Ankle and toes | Dorsiflexion 20°; plantarflexion 40°; toes ±30° | Ankle level (no malleoli); MTP line; toe joints | Medial, lateral, top | Sole returns flat at rest (T-1); MTP crease no collapse |
| D9 | Trunk twist and flexion | Twist ±30° across the spine stations; flexion 30° | Spine station spacing (39 cm thoracic gap); abdomen | Front, side, top | Candy-wrapper index (loop twist variance) reported; no fold; abdomen-zone volume within ±5 % |
| D10 | Neck | Flexion and extension ±30°; rotation ±45° | Neck base and head pivot; chin–chest contact | Side, front, 3/4 | Chin–chest contact marked as contact; neck loops no collapse. **No jaw test:** there is no jaw |

**Not decided here:** this proposal does not choose a final game skeleton, a UE5 compatibility policy or a performance budget.

---

## 10. Blockers and the precise author decisions needed

### 10.1 Blockers to "production rig ready"

1. Internal joint centres are not determined by the surface. Hip, knee, ankle, glenohumeral, elbow, sternoclavicular, pelvis root, spine and head pivot are all > 1 cm (1.3–9.3 cm).
2. The scapular medial border is missing; this is GR-G2 relevant.
3. There is no jaw anatomy and no oral cavity.
4. There are no eyeball objects.
5. Thoracic spine stations are sparse: there is a 39 cm segment.

### 10.2 Decisions needed (for each, the options are listed in tables §3)

| ID | Decision | Options |
|---|---|---|
| AD-R1 | **Hip centre** | Accept the consensus (z ≈ 119.1, f ≈ 2.8), choose the inguinal-fold thigh axis (A) or the frozen value (C), or author-place it |
| AD-R2 | **Knee and ankle levels** along the limb | The source has no condylar or malleolar relief. Accept the consensus (knee z 71.2, ankle z 13.5 / 13.75) or choose A, B or C. Also: accept a mediolateral ankle axis without obliquity? |
| AD-R3 | **Glenohumeral centre** | Sphere-fit vs frozen differ by 5–9 cm. Choose the consensus, a sphere, the frozen value or an author placement. Keep L/R asymmetric (documented shoulder-line asymmetry) or not? |
| AD-R4 | **Elbow level** | The cubital / waist level (z ≈ 141–143) vs frozen (z ≈ 147.5) |
| AD-R5 | **Sternoclavicular depth** | Between the skin summit and the frozen point (10 cm apart) |
| AD-R6 | **Spine** | Accept the inherited MPFB station heights, or add thoracic stations across the 39 cm spine_03 → neck_base gap. Spine AP depth: centroid vs frozen |
| AD-R7 | **Rig root vs production origin** | The proposed pelvis root lies 2.8 cm anterior of the frozen pelvis_root (same height) that defines the origin. The origin stays; is the rig root an offset? |
| AD-R8 | **Jaw / eyes** | Does Grask need a jaw joint and eye joints? Both need source-anatomy work (a mandible / oral cavity, eyeballs) that this order does not authorise. Until then the jaw hinge is a placeholder |
| AD-R9 | **Scapula** | How should the medial border be provided (author placement or a later anatomy order), given "do not invent a scapula landmark"? |
| AD-R10 | **Axis convention** | X toward subject-left on both sides (as proposed) or a mirrored per-side convention. Confirm the flexion-sign definitions |
| AD-R11 | **Frozen-package label correction** | `jaw_hinge` is mislabelled "construction". Correct it only in a future versioned package; the frozen file is never edited |
| AD-R12 | **Diagnostic test thresholds** | Approve or revise the §9 proposal before any execution order |

---

## 11. Files

| Location | Files |
|---|---|
| `reviews/rac-rp2-evidence/grask_rigprep_readiness_v001/` | `GR_U_REF_RP2_rigprep_landmarks_v001.json` (proposal); `*_tables.md`, `*.csv`; `raw/fit_v005.json`, `raw/fit_v003.json`; `hashes/` (before, after, npzcheck); `sheets/` (24 sheets, jpg) |
| `tools/rac/rp/grask_rigprep_v001/` | `run_rigprep.sh`, `hash_parents.sh`, `geomhash.py`, `npzcheck.py`, `fitlib.py`, `rigprep_fit.py`, `compose.py`, `tables.py`, `crops.py`, `render.py`, `render_all.sh`, `views.sh`, `overlay.py`, `README.md` |

**STOP FOR CHATGPT REVIEW.** A later execution order is required before any rig is built or tested.
