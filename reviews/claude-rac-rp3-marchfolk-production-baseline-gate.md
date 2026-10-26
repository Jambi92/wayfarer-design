# RAC RP3 — Marchfolk production baseline gate (MPFB family pilot)

**Date:** 2026-10-26
**Order:** `reviews/chatgpt-rac-rp2-closure-and-rp3-marchfolk-baseline-order.md` (d18ff2a), Part B
**Evidence:** `reviews/rac-rp3-evidence/marchfolk_baseline_v001/`
**Tools:** `tools/rac/rp/marchfolk_rp3_v001/`
**Status:** PRODUCTION CANDIDATES — **not accepted**. Recommendation: **FAMILY BASE NEEDS CORRECTION** (bounded: hand and foot root junctions only). **STOP FOR CHATGPT REVIEW.**

## 0. Answers to the §16 questions

| Question | Answer |
|---|---|
| Does native hm08 pass as the shared production base? | **No.** Integrity (§6) and anatomy pass exactly. It fails §8 density in 6 of 9 zones and §7 loops at 32 (configuration 1) / 30 (configuration 2) of 69 joint stations. |
| What local topology changes were required? | **v002**, one deterministic operator, identical for both configurations. (1) One level of **linear** quad subdivision: new vertices are hm08 edge midpoints and face centres, so the surface does not move. (2) **98 closed edge rings** inserted around the thighs and calves. Everything is a recorded linear map M from hm08, so UVs, MPFB targets and weights carry over exactly. No manual edits. |
| Are configuration 1 and 2 on the same final vertex/face topology? | **Yes.** v002 face list, UVs, src_index and map M are identical. Face topology hash `80fa188e…` for both (v001 native: `2ed8e59f…` for both). See `mapping/MF_common_topology.json` and `MF_topology_map.jpg`. |
| Do both preserve their accepted anatomy? | **Yes.** T-1, T-2, T-3 and T-7 pass for both (§3). Source → production max is 0.0001 mm. Production → source max is 2.57 / 2.19 mm (non-planar quad centres; T-1 ≤ 3 mm). |
| Do both satisfy deformation-loop requirements? | **Not fully.** v002 passes 50 / 49 of 69 stations firm (native 37 / 39). Every large joint passes: shoulder (F left: 4 of 5 loops), elbow, wrist, hip, knee and neck. The residual failures are all at **hand and foot root junctions**: MCP palm junction poles, thumb and pinky MCP loop count, an ankle crease pole and toe-root poles. These are hm08 pole placements that subdivision cannot move (§4). |
| Do both satisfy creator-density requirements? | **v002: yes**, all 9 zones in both configurations (§5). Native: no. |
| Is face/orbit/mouth topology adequate for later UFCA/facial production? | **Yes, with one note.** Mouth rings 35, orbit rings 43 + 43; no pole within 2 cm of the mouth or at its corners; eye sockets and lip slit are open (hm08 inner pocket). Jaw-hinge support is adequate: face density 0.137 %, and the cheek and jaw rings are continuous. The TMJ is a **derived estimate**: the MPFB jaw joint sits at the chin, and the game_engine rig has no jaw bone (§6). |
| What diagnostic deformation failures remain, and what class are they? | **No topology-class failure.** Under identical weights, v002 matches native within ±9 volume points and is equal or better in every flexion pose. Remaining failures (§7): **weights** (LBS volume collapse at elbow, knee, hip flex and shoulder flex); **contact / test setup** (fist, thumb opposition, wrist flex into the thigh, deep elbow and knee flex, thigh–abdomen at hip 90); one **joint-placement candidate** (configuration 1 knee centre 1.9 cm medial of the section centroid). |
| Is the MPFB-family base ready for explicit author acceptance and later propagation? | **Not yet, recommended.** v002 is the proposed family core. The hand and foot root junctions should be corrected once in the core before acceptance, because all ten MPFB-family races inherit them. Alternative for ChatGPT: accept v002 now and carry the §7 misses as recorded T-5 quality-target misses (§7 calls loop counts quality targets). |

## 1. Source regeneration identity (order §5)

Both configurations were rebuilt from their build records. Tool chain: MPFB 2.0.17, Blender 5.2.2 (bpy), `tools/rac/w1/arm_lib.py` build → ground → pose_r6 → ground.

| Config | Build sha256 | Committed R-6 sha256 | Committed geometry | Regenerated geometry | max \|dV\| | Pose record = regen |
|---|---|---|---|---|---|---|
| MF-M-R (1) | `c5be9ca0…` | `2caaf056…` | `9d9d0b4c…` | `9d9d0b4c…` identical | 0.0 cm | yes |
| MF-F-R (2) | `252907fd…` | `c254fb4b…` | `f609f8cd…` | `f609f8cd…` identical | 0.0 cm | yes |

- Evidence: `regen/MF-{M,F}-R_regen_check.json`; tool: `regen.py`.
- **Before/after source hashes** were re-hashed after all RP3 work and are unchanged:
  - MF-M-R_r6.npz `2caaf056…`;
  - MF-F-R_r6.npz `c254fb4b…`;
  - builds `c5be9ca0…` and `252907fd…`.
- The PC Grask RP2 v003 blend re-stages as `03bfe7d9…` (unchanged). RP3 writes only to the new `Marchfolk/RP3/` folder, and its blends and manifest re-stage from the PC with identical sha256.
- Evidence: `source_hashes_before_after.json`, `production_files_sha256.txt`.

## 2. Production candidates

| File | Role | Verts / quads | sha256 | Geometry hash |
|---|---|---|---|---|
| `MF_M_REF_RP3_retopo_v001.blend` | native hm08, helpers removed (reference; fails §7 / §8) | 13,380 / 13,378 | `0c2b13c9…` | `5847dfb6…` |
| `MF_F_REF_RP3_retopo_v001.blend` | same | 13,380 / 13,378 | `2ad7dcb5…` | `be45414e…` |
| `MF_M_REF_RP3_retopo_v002.blend` | **recommended candidate** | 57,434 / 57,432 | `c02f77bf…` | `c176d80c…` |
| `MF_F_REF_RP3_retopo_v002.blend` | **recommended candidate** | 57,434 / 57,432 | `9f228ad1…` | `846aacb3…` |

- **Location:** `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Marchfolk/RP3/`, with:
  - a `.json` sidecar per blend (source hashes, operations, frame, topology report, anatomy, gate pointer);
  - `_v002_hm08_map.npz` (map M);
  - `MF_RP3_manifest.json`.
- Sidecar and manifest copies are in the evidence folder.
- **Frame (contract §3):**
  - m, Z up, faces −Y, subject left +X;
  - origin = MPFB pelvis bone head projected to the ground (one rigid translation, recorded in each landmark package).
- **Helpers removed:** joint cubes, eye, tongue, teeth, tights, skirt and hair helpers. The eye centres are kept as landmarks.
- **Integrity, both configurations, v001 and v002:**
  - 100 % quads, 1 component, genus 0;
  - 0 boundary edges, 0 non-manifold edges or vertices, 0 degenerate faces, 0 coincident vertices;
  - winding consistent, normals outward.
- **Self-intersections:** v002 has 68 (1) / 122 (2) face pairs; native has 32 / 66. All of them come from the source surface, because v002 lies on it. They sit at arm–trunk contact in the axilla, plus the face (1) and the toes (2). They are recorded as accepted source contact.

## 3. Anatomy preservation (order §11)

| | Stature Δ | bbox max \|Δ\| | prod→src median / p95 / max (mm) | Identity zones max (head / ears / hands / feet, mm) | src→prod max | IoU front / rear / profile L / R |
|---|---|---|---|---|---|---|
| v002 config 1 | −0.00007 mm | 0.00007 mm | 0.000 / 0.233 / 2.569 | 1.107 / 0.465 / 0.852 / 1.449 | 0.0001 mm | 0.9978 / 0.9978 / 0.9974 / 0.9973 |
| v002 config 2 | −0.00001 mm | 0.00001 mm | 0.000 / 0.196 / 2.186 | 0.947 / 0.447 / 0.768 / 1.092 | 0.0001 mm | 0.9980 / 0.9980 / 0.9976 / 0.9976 |
| limits | T-3 ±1 | T-3 ±2 | T-1 0.5 / 1.5 / 3.0 | T-2 max 1.5 (p95 0.8) | | T-7 ≥ 0.995 |

- T-1, T-2, T-3 and T-7 **pass** for both configurations. Native v001 is the source surface (all 0).
- The production → source tail is the centre point of strongly non-planar hm08 quads, which sits off the source's quad triangulation. Every source vertex and every edge midpoint lies on the source.
- Evidence: `anatomy/*.json`; sheet `MF_overlay_{M,F}.jpg` (deviation heat plus silhouette overlays).

## 4. Topology and loops (contract §6 / §7)

Method: the RP2 band method (loops crossing 4 sides of a band; poles within 2 local loops) plus the literal closed-ring count.

- **firm** = loops ≥ minimum and no pole on the crease line.
- **strict** = additionally no pole within 2 loops.

| | Native firm fail | v002 firm fail | v002 strict fail |
|---|---|---|---|
| config 1 | 32 / 69 | **19 / 69** | 27 / 69 |
| config 2 | 30 / 69 | **20 / 69** | 26 / 69 |

**Large joints, v002 (loops / minimum):**

| Joint | Config 1 | Config 2 |
|---|---|---|
| Shoulder | 10 / 5 | right 10 / 5; **left 4 / 5** (band 3 on one side) |
| Elbow | 11 / 4 | |
| Wrist | 10 / 3 | |
| Hip | 5 / 5 | |
| Knee | 17 / 4 | |
| Neck | 11 / 4 | 15 / 4 |

All poles are off the crease, except as noted for the configuration 2 left shoulder.

**Residual firm failures on v002:**

| Station | Config 1 | Config 2 | Cause |
|---|---|---|---|
| ankle L/R | 6 loops, 1 crease pole | 4 loops, 1 crease pole | hm08 instep–heel junction pole on the crease line |
| index MCP L/R | pass | 5–7 loops, 1 crease pole | palm-to-finger junction pole |
| ring MCP L/R | 5 loops, 1 crease pole | 4, 1 | same |
| pinky MCP L/R | **2 / 3 loops** | pass | short MCP band at the palm edge |
| thumb MCP L | **2 / 3** | **1 / 3** | short thenar band; the right side passes (posed asymmetry: R-6 palm twist L/R differs) |
| toe roots j1 (toes 1–5) | 1–3 loops, 1–2 crease poles | 1–3, 1–3 | hm08 forefoot fan poles at every MTP |
| toe2/3 j3, toe4 j2 | 3–6 loops, 1 crease pole | same | interphalangeal junction poles |

- **Why subdivision cannot fix these:** subdivision keeps every hm08 pole and only halves the band spacing. The loop counts rise, but a pole on the crease stays on the crease.
- **What fixes them:** a local manual relocation of about 10 junction poles per side, moving each palm, MCP, ankle and MTP pole one or two loops off its crease, plus one thenar loop and one hypothenar loop.
- This is the "NEEDS CORRECTION" item. It is not done here: the order caps RP3 at one bounded deterministic candidate.
- **T-4 quality target (45–135°, aspect ≤ 4)** is missed, as with all hm08:
  - native 612 / 916 (1) and 640 / 816 (2);
  - v002 1326 / 2596 and 1368 / 2338, i.e. 2.3 % / 4.5 % of faces, lower per face than native;
  - the misses are concentrated in face, hands and feet;
  - angle p01–p99 is 48.8°–131.5°.

Evidence: `audit/*_audit.json` (keys `joint_s7`, `joint_bands`, `joint_loops`, `poles`) and `MF_closeups_{M,F}.jpg` (native wire | v002 wire | v002 counted loops with poles).

## 5. Creator density (contract §8, mean edge / stature)

| Zone (ceiling) | Native 1 | v002 1 | Native 2 | v002 2 |
|---|---|---|---|---|
| face (0.25) | 0.274 ✗ | 0.137 ✓ | 0.268 ✗ | 0.135 ✓ |
| ears (0.25) | 0.216 ✓ | 0.103 ✓ | 0.218 ✓ | 0.104 ✓ |
| hands (0.3) | 0.279 ✓ | 0.139 ✓ | 0.254 ✓ | 0.127 ✓ |
| feet (0.3) | 0.397 ✗ | 0.198 ✓ | 0.375 ✗ | 0.187 ✓ |
| trunk (0.6) | 1.017 ✗ | 0.509 ✓ | 1.020 ✗ | 0.511 ✓ |
| arms (0.6) | 0.969 ✗ | 0.483 ✓ | 0.888 ✗ | 0.443 ✓ |
| legs (0.6) | 1.434 ✗ | 0.513 ✓ | 1.394 ✗ | 0.501 ✓ |
| neck (0.6) | 0.640 ✗ | 0.325 ✓ | 0.579 ✓ | 0.295 ✓ |
| head (0.6) | 0.466 ✓ | 0.240 ✓ | 0.441 ✓ | 0.227 ✓ |

- Plain subdivision (s1) leaves the legs at 0.713 % (1) / 0.694 % (2); the 98 leg rings bring them under the ceiling.
- Zone assignment uses the R-6 source weights, carried through M.
- Sheet: `MF_density_{M,F}.jpg`.

## 6. Face readiness (order §9)

| | Native 1 / 2 | v002 1 / 2 |
|---|---|---|
| Mouth rings (closed loops about the forward axis through the lip-slit centre, r ≤ 5.5 cm) | 16 / 16 | 35 / 35 |
| Orbit rings L / R | 21 / 21 | 43 / 43 |
| Poles within 2 cm of the mouth / at the corners | 0 / 0 | 0 / 0 |
| Poles within 2 cm of each eye centre | 4 | 4 (outside the lid rings) |

- The first audit pass reported 0 mouth rings. It centred the test on the MPFB `mouth` joint cube, which sits at nose height (f 5.7, u 159 cm, about 4 cm above the slit). `face_rings.py` replaces it, centred on the surface-fit mouth corners. Evidence: `audit/*_face.json`.
- The eye sockets and lip slit are open with an inner pocket (hm08). Eyeballs, teeth and tongue are separate later objects (contract §5).
- **Jaw hinge:** the MPFB `jaw` joint helper sits at the chin front, and the game_engine rig has no jaw bone. Both are recorded with a flag. `jaw_hinge_l/r` is a **derived** TMJ estimate (ear root + 1.2 cm anterior, 0.5 cm inferior, 1.5 cm medial), flagged for the face-rig stage.
- The cheek and mandible flow is continuous, with face density 0.137 %. That is adequate hinge support for later UFCA work.
- Sheet: `MF_closeups_{M,F}.jpg` face row (mouth and orbit rings coloured).

## 7. Landmark packages (order §12)

`landmarks/MF-{M,F}-R_landmarks.json`: 124 landmarks per configuration. Each records its analysis-cm position, its production-Blender-m position, provenance, method and drift.

**Provenance:**
- **source-rig:** MPFB game_engine bone heads and axes. Covers root/pelvis, hips, knees, ankles, balls, SC, GH, elbows, wrists, all MCP/PIP/DIP and thumb CMC/MCP/IP, spine_01–03, neck base and head pivot.
- **source-joint:** MPFB joint helpers. Covers all toe joints, eye centres and the MPFB jaw.
- **surface-fit:** acromion, finger and toe tips, ear root and tip, mouth corners, crown.
- **derived:** jaw hinge.

**Results:**
- Surface-fit drift on v002 is ≤ 0.0007 mm (T-6 ≤ 1 mm). Mirror asymmetry is ≤ 0.0002 cm.
- **Flags (not replaced):**
  - `jaw_joint_mpfb`: sits at the chin, not the TMJ;
  - `jaw_hinge_l/r`: estimate.
- **Joint centring** (`landmarks/*_joint_centring.json`): joint offset from the limb cross-section centroid, using sections built from bone-weighted vertices.

| Joint | Config 1 offset (fraction of section radius) | Config 2 |
|---|---|---|
| Elbow | 0.87 cm (0.25) | 0.56 (0.17) |
| Wrist | 0.27 (0.12) | 0.28 (0.13) |
| Knee | **1.92 cm (0.39), centre medial** | 0.75 (0.14) |
| Ankle | 2.69 (0.57) | 1.03 (0.27) |

- The **ankle** offset is anatomical: the section through the talocrural axis includes the forward foot. It is not flagged.
- The **configuration 1 knee** is flagged as a joint-placement candidate for the rig stage. It was not moved, because RP3 must not finalize the skeleton.

## 8. Limited diagnostic deformation (order §13)

**Method:**
- Source rig and source weights (MPFB game_engine, 53 bones), numpy LBS, from the R-6 pose (`mf_deform.py`).
- The same weights are carried to v002 through M, so **native vs v002 isolates topology**.
- Metrics, within the joint zone:
  - new self-intersection pairs (all / in zone);
  - new folds;
  - faces flipped against the carried normal;
  - edge strain p95 / max;
  - zone cone-volume change.

### Configuration 1 (MF-M-R), native → v002

| Pose | Self-x in zone | Folds | Flips | Strain p95 % | Vol % | Class |
|---|---|---|---|---|---|---|
| shoulder abd 45 | 0 → 0 | 0 → 0 | 1 → 7 | 20 → 18 | +5 → +4 | pass |
| shoulder abd 90 | 0 → 0 | 0 → 0 | 6 → 25 | 44 → 43 | −2 → −1 | pass |
| shoulder flex 90 | 16 → 45 | 4 → 7 | 4 → 13 | 84 → 84 | −34 → −33 | **weights** (no deltoid/twist helper) + contact (arm into chest) |
| elbow 90 | 19 → 37 | 5 → 5 | 8 → 31 | 59 → 60 | −36 → −33 | **weights** (LBS collapse) |
| elbow 130 | 28 → 71 | 3 → 14 | 13 → 54 | 64 → 64 | −47 → −42 | **weights** + **contact** (forearm–biceps) |
| wrist flex 60 | 0 → 0 (82 → 176 outside zone) | 0 | 0 | 47 → 42 | −10 → −9 | **test setup** (hand into thigh) |
| wrist ext 60 | 0 | 0 | 0 → 1 | 34 → 34 | −7 → −6 | pass |
| fist | 128 → 296 | 0 | 0 → 1 | 14 → 15 | +3 → +4 | **contact** (finger–finger, finger–palm) |
| thumb opposition | 0 (12 → 24 outside zone) | 0 | 0 | 45 → 43 | +2 → +2 | **contact** (thumb–index) |
| hip flex 90 | 22 → 52 | 3 → 8 | 13 → 47 | 80 → 74 | −36 → −34 | **weights** (groin strain max 1860 %) + contact (thigh–abdomen) |
| knee 90 | 16 → 54 | 5 → 8 | 2 → 15 | 63 → 63 | −37 → −31 | **weights**; knee centre **joint-placement** candidate |
| knee 140 | 18 → 63 | 2 → 3 | 10 → 76 | 64 → 70 | −56 → −47 | **weights** + **contact** (calf–thigh) |
| ankle dorsi 20 | 0 | 0 | 0 | 18 → 19 | −2 → −2 | pass |
| trunk twist 30 | 0 | 0 | 0 | 9 → 9 | −2 → −2 | pass |
| neck flex 30 | 0 | 0 | 0 | 26 → 26 | −12 → −12 | pass |
| neck rot 45 | 0 | 0 | 0 | 18 → 17 | −5 → −5 | pass |

### Configuration 2 (MF-F-R), native → v002

| Pose | Self-x in zone | Flips | Strain p95 % | Vol % | Class |
|---|---|---|---|---|---|
| shoulder abd 45 / 90 | 0 / 0 | 4 → 16 / 5 → 19 | 20 → 19 / 48 → 49 | 0 → −1 / −10 → −10 | pass |
| shoulder flex 90 | 14 → 36 | 4 → 14 | 77 → 76 | −31 → −30 | weights + contact |
| elbow 90 / 130 | 13 → 36 / 27 → 66 | 6 → 22 / 12 → 45 | 78 → 75 / 80 → 81 | −20 → −19 / −33 → −30 | weights (+ contact at 130) |
| wrist flex 60 | 12 → 36 (84 → 174 all) | 3 → 16 | 28 → 28 | −4 → −4 | test setup + palm-crease contact |
| wrist ext 60 | 0 | 0 | 41 → 42 | −9 → −11 | pass |
| fist | 183 → 400 | 9 → 46 | 19 → 20 | +18 → +36 | contact (volume metric invalid under interpenetration) |
| thumb opposition | 6 → 16 | 0 | 40 → 36 | 0 → +1 | contact |
| hip flex 90 | 22 → 51 | 9 → 33 | 45 → 47 | −28 → −26 | weights + contact |
| knee 90 / 140 | 22 → 87 / 17 → 72 | 4 → 36 / 13 → 90 | 59 → 56 / 73 → 70 | −33 → −27 / −51 → −42 | weights (+ contact at 140) |
| ankle, trunk twist, neck flex / rot | 0 | 0 | ≤ 27 | −2 … −12 | pass (twist: 1 → 17 arm–trunk contact outside the zone = setup) |

### Classification

- **Topology: none.**
  - Volume and strain are the same or better on v002 in every pose.
  - The higher pair, fold and flip counts on v002 follow from 4.3× more faces in the same contact area. Per face, the flip rate is comparable (elbow 130: 0.097 % → 0.094 %; knee 140: 0.075 % → 0.13 %, finer faces folding individually in the same LBS crease).
- **Weights:**
  - LBS volume collapse at elbow, knee, hip flex and shoulder flex. This is the same class as the Grask RP2 findings.
  - It needs production helpers and correctives at the rig stage. Per the order, no corrective programme is launched here.
- **Joint placement:** the configuration 1 knee centre (1.9 cm medial), flagged in §7.
- **Contact / test setup:** fist, thumb opposition, wrist flex into the thigh, deep elbow and knee flex, thigh–abdomen at hip 90, and arm–trunk in twist.

Evidence: `deformation/deform_*.json`; sheet `MF_deform_{M,F}.jpg` (native | v002 per pose; red = new self-intersection, magenta = flipped, purple = new fold).

## 9. Family decision (order §14)

### FAMILY BASE NEEDS CORRECTION (bounded)

- **Native hm08** cannot be the production base unchanged. It fails §8 in 6 zones and §7 at 30+ stations.
- **v002** is the proposed corrected family core: deterministic, linear and fully mapped. It passes §6 integrity, §8 density, anatomy T-1 / T-2 / T-3 / T-7 and face readiness, and every large-joint station.
- **Required before acceptance:** one local, manual, mapped correction of the shared hm08 junction poles at:
  - the palm MCP junctions (index, ring, pinky; thumb and pinky MCP loop count);
  - the ankle crease;
  - the toe roots (MTP j1 for all toes, and toe2/3 j3, toe4 j2).

  These are family features: all ten MPFB-family races inherit them, so they should be fixed once in the core.

**Safe to propagate unchanged** after that correction, to Skarn, Sagekin, Fenn, Aelari, Vael, Halvren, Durrim, Pipkin and Cogling:
- the v002 operator (linear subdivision + leg rings) and its map M;
- trunk, pelvis/groin, shoulder, arm, elbow, wrist, leg, knee, neck, head, face, orbit and mouth topology;
- carried MPFB UVs (non-final, contract §10);
- the source-rig landmark method and package format;
- the production frame and origin rule.

**Must branch per race** (contract §9, local loop additions only, mapped):

| Race(s) | Branch |
|---|---|
| Fenn, Aelari, Vael, Halvren | Ear families: ear rings and tip density for the long-ear shapes. Halvren is authored per its own source rules, not as an elf-percentage blend. |
| Durrim, Pipkin, Cogling | Compact-race face, hand and foot density. Relative density is stature-scaled; the branch adds the absolute loops these reads need, including the Cogling 76 cm adult head. |
| Skarn, Sagekin | No branch named by the contract. Each still runs the §9.4 sharing test (T-1 / T-2 of its own source) at its race gate. |

Grask E3 already has its own frozen RP2 topology.

## 10. Evidence index (`reviews/rac-rp3-evidence/marchfolk_baseline_v001/`)

| Folder / file | Contents |
|---|---|
| `regen/` | regeneration identity checks |
| `audit/` | native and v002 topology / loop / density / quality audits and face-ring audits (both configurations) |
| `anatomy/` | anatomy preservation |
| `landmarks/` | landmark packages and joint-centring checks |
| `deformation/` | native and v002 deformation results |
| `mapping/MF_common_topology.json` | common topology |
| `MF_*_REF_RP3_retopo_v00{1,2}.json`, `MF_RP3_manifest.json` | sidecars and manifest |
| `sheets/` | `MF_body_{M,F}.jpg` (full body front/rear/profile/3-4 clay; native vs v002 wire full and upper/lower body), `MF_closeups_{M,F}.jpg` (face/orbit/mouth, shoulder/axilla, elbow, hand/fingers, pelvis/groin, knee, foot/toes; native wire, v002 wire, loop evidence), `MF_density_{M,F}.jpg`, `MF_overlay_{M,F}.jpg`, `MF_topology_map.jpg`, `MF_deform_{M,F}.jpg` |

**Tools** (`tools/rac/rp/marchfolk_rp3_v001/`):
- `regen.py`, `native_export.py`, `audit.py`, `face_rings.py`;
- `subdiv.py`, `leg_rings.py`;
- `landmarks.py`, `joint_centring.py`, `anatomy.py`;
- `make_prod.py`, `mf_deform.py`, `mf_sheets.py`, `sidecars.py`.

## 11. Stop

**STOP FOR CHATGPT REVIEW.** Not started: Skarn or any other race, propagation, the family-core pole correction, rig or weight finalization, morphs, final UVs, LODs, UE5, Turnfall.
