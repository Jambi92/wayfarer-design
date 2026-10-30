# Claude Gate — RAC RP4 Durrim Compact-Branch Pilot

**Order:** `reviews/chatgpt-rac-rp4-durrim-compact-branch-pilot-order.md` (609c557; prior state d46a1c4)
**Date:** 2026-10-30
**Evidence:** `reviews/rac-rp4-evidence/durrim/`
**Tools:** `tools/rac/rp/durrim_rp4_v001/`
- `du_regen.py`: regen.py plus the native short-adult route.
- `run_a.sh`, `run_parta.sh`, `du_partA.py`: Part A.
- `run_b.sh`: the unbranched v005 Standard v1 pipeline.
- `du_density.py`: the §8 compact-density diagnosis.
- `du_branch.py`: compact-branch define / apply.
- `du_sheets.py`: boards.

## Result

**DURRIM RP4 COMPACT BRANCH NEEDS REVISION**

There are two exact local technical blockers. The second one, by the order's own §7 rule, stopped topology work before the production candidates.

1. **Thumb MCP (hand zone, authorized).**
   - On the unbranched Family Base v005, the authoritative D1 + D3 + D4 + D5 + D6 validator fails `thumb_mcp_l / r` (FAIL_LOOPS: 1–2 anatomical rings, 3 required) on **every** Durrim body: 122 / 137 / 152 c1 and 137 c2.
   - Equal-height Marchfolk 152 passes at margin 0.
   - The minimum ring-insertion branch (`MPFB_COMPACT_BRANCH_v001` prototype) fixes the loop count on all bodies (4–6 rings, margin ≥ 1).
   - However, the trisected rings make **100–105 thin quads above the T-4 4 : 1 aspect target** (max 9.3 : 1) on each body. I don't accept it as the branch. A clean fix needs a two-direction local densification (rings plus circumferential splits) at the thumb MCP. That is not built.
2. **Neck station on c1 137 / 152 (neck = joint, not an authorized branch zone).**
   - The validator fails `neck` with **FAIL_CREASE_POLE** on DU137C-NAT and DU152C-NAT.
   - Cause: the v005 submandibular valence-5 pole pair (v005 vertices **5299 / 11904**, face zone, under the jaw) lies inside the neck-station crease band. Durrim's short neck puts the band at the jaw underside: pole offset / h = −0.20 (137) and +0.14 (152), where the crease band is |t / h| ≤ 0.5.
   - It passes on DU122C (−0.54, just outside), DUF137C c2 (+2.92) and Marchfolk 152 (+1.97).
   - Clearing it means relocating that pole pair: a topology edit at the jaw–neck junction. Per order §7 ("If that happens, STOP and report it rather than expanding scope"), **I stopped here.**
   - The neck has **no deformation symptom**: neck_flex30 / neck_rot45 give 0 flips / 0 new self-intersections / 0 new folds on every body.

Everything before the branch passes. That covers Part A, regeneration, the unbranched density diagnosis, anatomy, contact and deformation. No production candidates (`DU_M/F_REF_RP4_v001`) were written, and nothing was frozen.

## 1. Answers to the order's questions

| Question | Answer |
|---|---|
| Did DU137C-NAT regenerate exactly? | **Yes.** Geometry identical, max dV 0.0; r6 sha256 = the order value `6149d149…`. DU122C-NAT and DU152C-NAT also regenerate exactly. This needed `du_regen.py`, because regen.py does not apply the recorded native factors. |
| Was a valid ~137 cm config-2 central reference created? | **Yes.** `DUF137C-NAT`: native short-adult route from the MF-F-R base macro 0.60596, the DU137C targets, pelvis `[1.0, 0.9, 1.04]`, stature 137.000 cm. A second independent rebuild is identical (dV 0). **DURRIM CONFIG-2 CENTRAL REFERENCE PASS — READY FOR RP4** (§2). |
| Does v005 fail any compact density requirement before branching? | **Yes, at the thumb MCP** (validator loop count, all Durrim bodies). The §8 zone means pass everywhere: face 0.145–0.154 %, hands 0.142–0.157 %, feet 0.196–0.207 % of stature, against ceilings of 0.25 / 0.3 / 0.3. The c1 neck crease pole is a second validator failure, outside the authorized zones. |
| What exact local topology was added and why? | **Prototype only.** In the two quad strips distal of the thumb MCP seed ring (v005 ring t ≈ 0.22–0.69 cm on DU137C), each strip is trisected into 2 new rings per strip per side: +160 vertices / +160 quads. New vertices are linear rows of the v005 map (V = S V, M = S M). It was rejected for T-4 (§4). |
| Are c1 / c2 on identical compact topology? | **By construction.** The branch is defined by v005 vertex indices; every realization of the prototype has 58,002 V / 58,000 Q and identical face lists. No candidates were written. |
| Does Durrim anatomy remain within accepted tolerances? | **Yes on v005:** T1 / T2 / T3 / T7 pass on all five realizations. The prototype keeps T1 / T2 / T3 / T7 on DU137C / DUF137C, because a bilinear split at iso-lines keeps the surface. |
| Does corrected DU-P4 remain intact? | **Yes.** Skeletal AP pelvic depth / stature: DU137 vs MF137 +3.0…+3.4 % (t = 0…1); DUF137 vs MFF137 +3.8…+4.4 %; DU152 vs MF152 holds. |
| Does the 152 cm equal-height Marchfolk test pass? | **Yes, on the sources.** All 19 directions DU152C vs MF152 hold (§2). The board D production comparison was not made, because there are no candidates. |
| Do face / hands / feet meet creator-density requirements? | **Zone means: yes**, at every stature (§3). **Thumb MCP loop support: no** on v005. |
| Are both candidates 69 / 69? | **No candidates.** v005: c1 66–67 / 69, c2 67 / 69. Prototype: DU122C 69, DUF137C 69, DU137C / DU152C 68 (neck). |
| Is adult read preserved? | **Not reviewed:** this needs the production candidates (boards E). The sources are the accepted W2H1 adult bodies. |
| Is any new deformation failure topology-class? | **No.** v005 vs native differences are the family-base class, and the prototype adds 0 flips / 0 folds vs v005 on all 18 poses. The +8 DUF137C hip_flex90 self-intersection pairs are the same thumb–thigh contact counted on subdivided faces; there are 0 new non-branch pairs. |
| Which branch features are safe to test later on Pipkin / Cogling? | **The method, not the prototype**: index-defined ring insertion as linear map rows (no shape, UVs and weights carried). See §5. |
| Is Durrim ready for author freeze? | **No.** The two blockers above need a revision order / ruling. |

## 2. Part A — configuration-2 central reference

Record: `partA/DU_partA.json`. Comparators are diagnostic only: MF137 / MFF137 / MF152 / MFF152 on the same native route, with no targets.

**Durrim directions vs equal-height Marchfolk:** 19 / 19 hold on c1 137, on c2 137 and on c1 152, and c2 matches c1 on all 19.

| Reading | c1 DU137 vs MF137 | c2 DUF137 vs MFF137 |
|---|---|---|
| torso share | +5.2 % | +5.3 % |
| thoracic breadth / stature (skel, t 0…1) | +10.6…+11.3 % | +11.4…+12.3 % |
| thoracic depth / stature (skel) | +13.0…+14.3 % | +13.8…+15.2 % |
| neck share | −14.0 % | −12.0 % |
| arm share / leg share (DU-P2a) | −2.6 % / −2.2 % | −2.9 % / −2.3 % |
| hip-joint spacing (DU-P2b) | +4.5 % | +4.7 % |
| pelvic vertical / crest (DU-P3) | −11.6…−11.9 % | −13.8…−14.2 % |
| AP pelvic depth (DU-P4) | +3.0…+3.4 % | +3.8…+4.4 % |
| crest / stature (DU-P5) | +4.8…+5.1 % | +7.9…+8.4 % |
| crest / thoracic breadth (DU-P6, ≤) | −5.3…−5.6 % | −3.2…−3.5 % |
| femoral shaft / femur | +7.0…+7.7 % | +7.9…+8.8 % |
| wrist / knee / ankle / elbow | +29 / +5.6 / +7.7 / +7.2 % | +31 / +13 / +11 / +10 % |
| hand share / foot share | +10.6 / +2.8 % | +11.3 / +2.6 % |
| head share (report) | +1.5 % | +1.5 % |

**Palm breadth / hand** is −0.6 % (c1) and −1.5 % (c2) against Marchfolk. It is reported only: W1 recorded palm share as MARGINAL / provisional.

**No Durrim-specific sex shift.** The Durrim c2 / c1 ratios track Marchfolk's c2 / c1 ratios:
- **Within 1.5 %:** 12 of 21 readings.
- **Residuals toward more Durrim on c2:** shoulder, DU-P3, DU-P5, and the wrist / knee / ankle / elbow joints. The largest is knee / femur, +6.1 points.
- **Residuals toward less Durrim:** neck share (+2.7 points; c2 neck is still −12 % vs MFF137) and crest / thoracic breadth (+2.4 points; DU-P6 still holds at −3.3 %).

These come from the generator's response to the same targets on the configuration-2 base. They are not an added shift, and configuration 2 is not narrower, smaller-headed or less structurally substantial.

## 3. Unbranched v005 diagnosis (§8)

Records: `unbranched/density/*_fam_density.json`, `validator/`, `audit/`.

Values are mean / p95 edge as a percentage of stature.

| Sub-zone | DU122C | DU137C | DU152C | DUF137C | MF152 |
|---|---|---|---|---|---|
| face: orbit | 0.103 / 0.212 | 0.099 / 0.203 | 0.096 / 0.197 | 0.102 / 0.207 | 0.093 / 0.191 |
| face: mouth | 0.133 / 0.302 | 0.127 / 0.289 | 0.123 / 0.280 | 0.124 / 0.272 | 0.119 / 0.271 |
| face: jaw hinge | 0.320 / 0.670 | 0.228 / 0.408 | 0.164 / 0.372 | 0.260 / 0.619 | 0.164 / 0.367 |
| face: other | 0.250 / 0.642 | 0.245 / 0.630 | 0.243 / 0.621 | 0.233 / 0.601 | 0.239 / 0.612 |
| hand: palm | 0.312 / 0.531 | 0.307 / 0.524 | 0.303 / 0.517 | 0.285 / 0.486 | 0.274 / 0.463 |
| hand: wrist transition | 0.317 / 0.513 | 0.312 / 0.504 | 0.307 / 0.497 | 0.288 / 0.464 | 0.271 / 0.450 |
| hand: MCP / IP / tip | 0.168 / 0.127 / 0.105 | 0.166 / 0.126 / 0.104 | 0.164 / 0.124 / 0.102 | 0.153 / 0.114 / 0.095 | 0.150 / 0.116 / 0.098 |
| foot: heel / forefoot | 0.421 / 0.419 | 0.419 / 0.418 | 0.416 / 0.417 | 0.372 / 0.431 | 0.382 / 0.401 |
| foot: ball / toe joints / tips | 0.247 / 0.117 / 0.152 | 0.246 / 0.117 / 0.154 | 0.246 / 0.117 / 0.143 | 0.229 / 0.109 / 0.136 | 0.234 / 0.110 / 0.152 |
| **ZONE face / hand / foot (mean)** | 0.154 / 0.157 / 0.207 | 0.149 / 0.155 / 0.206 | 0.145 / 0.153 / 0.206 | 0.147 / 0.142 / 0.196 | 0.142 / 0.141 / 0.196 |

- **Zone means:** the contract §8 ceilings are zone means, and they pass at every Durrim stature.
- **Hands relative to the human family:** Durrim's relatively large hand runs about 10–15 % sparser per stature than Marchfolk on the same topology. This shows in palm and wrist-transition means of about 0.31 % at 122–137 cm (sub-zone diagnostics). Heel and forefoot sub-zones are over 0.3 % in the human family too (MF152 0.38–0.40 %), so they are not compact-specific.
- **Jaw-hinge sub-zone:** its label is stature-sensitive. It is reported as a watch item, not a branch trigger (order: no density uniformity chasing).
- **Face rings:** mouth 33–37 rings, 0 poles at mouth corners, orbit pass on all bodies.

**Validator on v005:**

| Body | Firm passes | Firm fails |
|---|---|---|
| DU122C | 67 / 69 | thumb_mcp × 2 |
| DU137C | 66 / 69 | thumb_mcp × 2, neck |
| DU152C | 66 / 69 | thumb_mcp × 2, neck |
| DUF137C | 67 / 69 | thumb_mcp × 2 |
| MF152 | 69 / 69 | — (thumb_mcp margin 0) |

**Other v005 checks:**
- **Anatomy:** T1 / T2 / T3 / T7 pass on all; stature −0.29 to −0.37 mm (c2 0.00).
- **Contact:** classes source-only, 0 new pairs, 0 new hand / foot / groin defects.
- **Integrity:** 1 component, 0 boundary edges.

**Why the thumb MCP fails:**
- The thumb MCP has no defined band sides on any MPFB body, so the station uses the D1 closed-ring fallback: rings within 3.0 × s cm of the thumb axis and 0.8 × s cm of the MCP, with s = stature / 173.143.
- Durrim's hand is allometrically large (hand factor k^0.842 plus `hand-scale-incr` 0.3), so the v005 thumb rings near the MCP are wider than the stature-scaled radius.
- At 137 cm only the ring at t = 0.45 cm fits (r_max 2.21 cm < 2.37 cm). The rings at −0.01 and 0.22 cm are 2.79 and 2.50 cm.
- This is the contract's anticipated "compact-race hand density" case.

## 4. Compact-branch prototype (`branch_prototype/`)

**Definition:** `MPFB_COMPACT_BRANCH_v001_prototype.json`.
- Topology-only, on the v005 face hash.
- Thumb MCP rings are taken from the validator's own ring station (thumb_02 head / axis).
- Seed ring at t = −0.011 cm.
- The strips [0.217, 0.450] and [0.450, 0.688] are trisected, per side.

**Realization:**
- **Mesh and map:** `du_branch.py apply`. New vertex = (1 − u) a + u b (u = 1/3, 2/3) as rows of S. V = S V_v005 and M = S M_v005, so V = M @ hm08 V exactly.
- **Indices and UVs:** v005 vertex order is unchanged (new vertices appended); split faces keep their index; corner UVs are interpolated.
- **Surface:** splitting a bilinear quad on its iso-lines keeps the surface.

| | thumb_mcp loops (margin) | firm | T-4 aspect > 4 added | deformation vs v005 |
|---|---|---|---|---|
| DU122C | 4 (+1) | 69 / 69 | 105 | — |
| DU137C | 4 (+1) | 68 / 69 (neck) | 105 | 0 flips / 0 folds / 0 self-x on 18 poses |
| DU152C | 4 (+1) | 68 / 69 (neck) | — | — |
| DUF137C | 6 (+3) | 69 / 69 | 100 | 0 flips / 0 folds; hip_flex90 +8 pairs = same thumb–thigh contact on split faces |
| MF152 | 7 (+4) | 69 / 69 | — | — |

**Why I rejected the prototype:**
- The trisected strip quads have aspect up to 9.3 : 1 (median 3.8). The parent strip quads were ≤ 3.1 : 1.
- Midpoint-only insertion would keep aspect lower, but fails 122 cm: the new ring at t = 0.30 has r 2.12 cm > 2.11 cm, giving 2 rings.
- **Proposed revision:** a local two-direction densification of the two MCP strips (new rings plus circumferential midpoints, with valence-preserving transitions outside the MCP crease band). It should be verified for T-4, D3 crease poles and deformation at 122 / 137 / 152.

## 5. Reusability (technical only)

- **Safe to share (anatomy-neutral):**
  - index-defined branch records on the v005 face hash;
  - insertion of linear map rows (shape-preserving, UV / weight / morph path kept through M);
  - selection by the validator's own ring stations.
- **Not to share:** nothing in the prototype encodes Durrim shape. The ring selection is topological. However, the number of inserted rings needed depends on a race's hand allometry (Durrim hand factor). Pipkin / Cogling must be diagnosed on their own sources with the same tool (`du_density.py` + the validator).

## 6. Neck blocker detail (`DU_neck_station_poles.json`, board N)

**Station:** the validator neck station from core3lib (centre = midpoint of the neck_01 and head joints, vertical axis, R = 11 s). Crease poles are poles with |axial| ≤ 0.5 h, where h = median local edge.

| Body | Pole offset / h | Status |
|---|---|---|
| DU122C | −0.54 | PASS (0.04 h outside) |
| DU137C | −0.20 | FAIL |
| DU152C | +0.14 | FAIL |
| DUF137C | +2.92 | PASS |
| MF152 | +1.97 | PASS |

**The poles:** valence 5, at x ±4.3, y +10.4 cm (137 cm), in the face zone under the jaw.

**Options for the author:**
- **(a)** Authorize a local jaw–neck junction branch that moves the 5-pole pair ≥ 1 h above the neck crease band.
- **(b)** Record a c1 neck-station topology carry-forward. Deformation is clean: 0 / 0 / 0 on neck_flex30 / neck_rot45 for every body.

I do not propose any validator change.

## 7. Immutable sources / frozen references

`immutable_hashes.txt`:
- **Durrim sources:** DU122C / DU137C / DU152C build records + r6 (DU137C r6 = order value).
- **Inputs:** MF-F-R / MF-M-R builds; v005 freeze record, blend and hm08 map (= frozen values).
- **Frozen races:** Fenn / Aelari / Vael / Halvren freeze records unchanged vs d46a1c4.
- **New records only:** nothing outside `tools/rac/rp/durrim_rp4_v001/` and `reviews/rac-rp4-evidence/durrim/` was written.

## 8. Boards (`reviews/rac-rp4-evidence/durrim/sheets/`)

- **DU_A_central_sources.jpg:** DU137C c1 and DUF137C c2 on v005 — front / 3/4 / side / rear / head / hand / foot / pelvis.
- **DU_B_thumb_branch.jpg:** thumb MCP wire, v005 vs prototype (new quads blue, aspect > 4 red), 122 / 137 / c2.
- **DU_N_neck_blocker.jpg:** submandibular poles and the validator neck crease band on 122 / 137 / 152 / c2 / MF152.
- **DU_G_boundary_density.jpg:** hand / face / foot wire at 122 / 137 / 152.

Boards C–F (production candidates, 152 cm production comparison, hidden presentation, deformation) wait for the candidates.

## 9. Not done (STOP)

- No production candidates and no freeze.
- No neck / jaw topology.
- No Pipkin / Cogling / Saurin.
- No UE5, creator, rig, LOD, materials, hair or clothing.

**STOP FOR CHATGPT REVIEW.**
