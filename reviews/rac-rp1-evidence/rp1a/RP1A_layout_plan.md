# RP1-A — welded source, landmarks and manual topology layout plan

**Checkpoint 1 of 4** for the Gorrund manual retopology pilot.
**Order:** `reviews/chatgpt-rac-rp1-gorrund-manual-retopo-execute-order.md` §7. No production topology is built in this checkpoint.

## 1. Source and welded working copy

**Source:** `GO-05AW4_nails_final.blend`, sha256 `5a4e45d4…2d5e`. Hash checked at entry and again after RP1-A. It was opened read-only in the cloud and never written.

**Welded copy:** `GO_U_REF_RP1_weldsrc_v001.blend`, sha256 `1d7adbe16564f1823b0a3f6ee2da1ab268c172209993b04735eb6c872dd59f8b`.
- Location: PC `RaceBodies\production\Gorrund\RP1\`.
- Tool: `tools/rac/rp/rp1_weld.py`.

| Item | Value |
|---|---|
| Positions merged | 36,452 coincident positions (UV-seam split duplicates, distance ≤ 1e-6 m) |
| Position change | **0.0** |
| Vertices | 598,717 → **562,265** |
| Triangles | 1,124,538 (unchanged) |
| Result | 1 component / 0 boundary / 0 non-manifold, genus 3 |
| Vertex groups | All 27 kept |

## 2. Identity zones (`zones_weldsrc.npz`; contract T-2 zones)

The zones are built from the sculpt's segment labels plus geometry:

| Zone | Definition | Vertices |
|---|---|---|
| Head / muzzle / ears | Trunk label above 0.845 H | 59,831 |
| Hands | `hand_L` / `hand_R` labels | 27,058 / 21,542 |
| Feet / toes / nails | `foot_L` / `foot_R` labels | 63,790 / 48,567 |
| Tail root | Within 14 cm of the posterior tail emergence point (2.3, 9.8, 104.4 cm; 51.1 % H) | 6,528 |
| General | Everything else | 334,949 |

## 3. Source landmarks (`landmarks_source.json`; tool `tools/rac/rp/rp1_landmarks.py`)

**Method.** Each joint landmark is the centroid of the mesh cross-section in a fixed plane. The planes come from the boundaries between the sculpt's segment labels.

| Landmark | Points | Plane |
|---|---|---|
| Shoulder, elbow, wrist, hip, knee, ankle | L / R | Segment-label boundary plane |
| Pelvis root | Midpoint of the two hip sections | — |
| Neck | Minimum-breadth section, z 183.4 cm | Horizontal |
| Crown | Midline, z 203.8 cm | — |
| Highest point | **Left ear tip**, z 204.52 cm | — |
| Tail chain | 12 segments / 13 stations over a 98.0 cm surface path; section radius about 4.3 cm | Perpendicular sections |
| Toe tips | 5 per foot | Foot frame |

**Note:** the ear tip sets the stature, so T-3 is governed by the ear.

**Re-measurement on production.** The same planes are re-sectioned on the production mesh, giving the T-6 drift.

**Placed by hand in RP1-C** (an extreme-point rule is not anatomical here):
- eyes;
- jaw hinge, chin, mouth corners;
- ear root / tip;
- sternoclavicular joint, acromion, scapular proxy;
- finger tips and MCP;
- MTP line;
- head pivot.

## 4. How dense the production mesh must be (`density.json`; tool `tools/rac/rp/rp1_density.py`)

**Method.** The chord error of a projected mesh is about κ·h²/8. The required edge length h is solved from the source curvature (p95 against the p95 tolerance; p99.9 against the max tolerance).

| Zone | Required final edge h | Quads (estimate) |
|---|---|---|
| General | 0.79 cm | 45.7 k |
| Head | 0.49 cm | 16.2 k |
| Hands | 0.43 / 0.51 cm | 7.3 k / 4.9 k |
| Feet | 0.32 / 0.38 cm | 10.9 k / 8.0 k |
| Tail root | 1.46 cm | — |

**Total ≈ 93 k quads** if density is adapted by zone. A uniform subdivision level gives more (§6).

## 5. Projection feasibility, diagnostic only (`projsim_*.json`, `projsim_err_map.png`)

**Method.** Automatic QEM-decimated stand-in cages were subdivided (Loop) and projected onto the source at every level. They were measured and **discarded**; none is production topology.

| Stand-in cage | Final vertices | Result |
|---|---|---|
| 3,000-face cage, 3 levels | 96 k | General zone **p95 0.82 mm**, inside T-1. **Fingers, toes and ears are lost entirely**: source→production max 42–70 mm |
| 24,000-face cage, 2 levels | 192 k | General p95 0.35 mm. Identity zones p95 1.2–2.6 mm and max 12–19 mm: **fails T-2** |

**Where the 24,000-face cage fails** (heat map): ear rims and ear folds; lip and mouth line; nostril and eye creases; between-digit crevices; nail-plate edges; finger contact sites.

**Conclusion.** The deviation gates can be met by "manual cage → subdivision → projection" **only if** the manual cage carries **feature-following loops** in these places:
- ear rims (thin-edge support loops);
- lips, nostrils, eyelids;
- each digit, separated to the crevice floor;
- each nail plate, with an inset plate loop plus edge support.

An evenly distributed cage cannot meet them. This confirms a manual feature-following layout (M-B). It does **not** show that the gates are impossible, so this is not a stop condition.

## 6. Manual cage layout plan

**Build sequence:**
1. Build a quad cage manually in the Blender UI (operators only).
2. Apply Subdivision Surface, level 3 (Catmull-Clark).
3. Apply a Shrinkwrap (nearest surface point / project) onto the welded working copy.
4. Clean up locally by hand.

**Target cage edge length:**
- general ≈ 6 cm;
- head and hands ≈ 3–4 cm;
- feet ≈ 2.6–3 cm;
- feature loops tighter.

| Region | Cage ring size (vertices around) | Lengthwise spacing | Junction / notes |
|---|---|---|---|
| Trunk | 24 | about 6 cm; 3 cm at the waist / girdle | Front / back midline columns kept |
| Crotch | trunk 24 → two leg rings of 14 through a 1-vertex gusset (F–C–B) | — | 14 → 12 reduction pole placed on the lateral thigh, off the crease |
| Thigh / shin | 14 → 12 | about 5 cm; 3 support loops at the knee | Patellar loop |
| Ankle → foot | 12 | — | Foot box; 5 toe tubes, 6 vertices each; separated to the crevice floor |
| Nails | Inset plate loop on each toe-tip top, plus 1 support loop | — | Projection must reproduce 1.55–1.74 mm (±0.15) |
| Shoulder | Arm ring of 10 bridged to a 10-edge hole in the trunk side (3 × 2 faces) | — | 5 loops around the GH; axillary loop separates the left-axilla tunnel (D-3) |
| Upper arm / forearm | 10 | — | 3 loops plus a crease loop at the elbow; wrist 3 loops |
| Hand | Palm ring of 16; 5 digit tubes of 6 vertices; thumb from the palm side | — | 3 loops per knuckle, 2 per IP joint. Digits modelled separately, which resolves contact handles D-1 / D-2 by construction; contact sites kept to T-2 |
| Neck | Trunk 24 → neck 16 (reduction on the trapezius slope) | — | 4 loops |
| Head | Neck 16 continues | — | Muzzle loops radiating from the nose pad; orbit rings; lip ring; jaw-hinge support. Ears: an 8-edge hole on the cranium, extruded and flattened; rim loop plus inner fold loop |
| Tail | Hole of 8 edges (2 × 2 faces) on the lower back at the emergence point; tail tube ring of 8 | Along the 13 chain stations, about 8 cm; 4 rings at the root | Tip cap is a grid fill |

**Expected size:**

| Item | Estimate |
|---|---|
| Cage | ≈ 3,000 quads |
| Final at level 3 | ≈ 190 k quads, reported against the §8 density **ceilings** (no budget gate) |
| Density reduction (contract §8 allows it) | If needed, applied after level 3 by local unsubdivide in the general zone |

**Effort note.** This is a full creature retopology, normally several working days for an artist. It is executed through remote UI control in the checkpoints RP1-B (trunk / girdle / pelvis / major limbs), RP1-C (head, hands, feet, tail, identity zones) and RP1-D (close, clean up, evidence). Each checkpoint is saved as `GO_U_REF_RP1_retopo_v<NNN>.blend` and never overwritten.
