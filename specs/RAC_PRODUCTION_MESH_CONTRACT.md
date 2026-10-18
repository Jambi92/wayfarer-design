# RAC Production Mesh Contract (draft, RP0)

**Status:** DRAFT, proposed by RP0 (`reviews/claude-rac-rp0-source-inventory-contract.md`). It governs the Retopology / Rig-Prep program (`reviews/chatgpt-rac-retopology-rigprep-master-plan.md`).

**Scope.** Production / technical rules only. **Nothing here is biology canon.**
- Race anatomy stays governed by the race specs, `decisions/REFERENCE_ANATOMY_V1.md` and the accepted gates.
- The production tolerances in §16 were accepted for RP1 on October 18, 2026. Any later change needs Tyler / ChatGPT acceptance.
- **Not set here:** a final game vertex budget, final LOD counts, final UV / material policy, the final skeleton hierarchy and skin weights. Each needs its own later contract with UE5 / performance evidence.

## 1. Source immutability

1. The accepted source for each race (inventory: `reviews/rac-rp0-evidence/source_inventory.json`) is **read-only truth**. No source file is edited, re-saved, re-exported or re-hashed in place.
2. **Every production step**:
   - starts by verifying the source SHA-256 against the inventory and stops on any mismatch;
   - ends by re-hashing the source to show it is unchanged.
3. **Procedural MPFB sources** (11 races, Grask included) are regenerated from their committed build record with MPFB 2.0.17 / Blender 5.2.2. They must be **geometry-identical** to the committed R-6 asset (sha256 over float32 V + int32 F) before use. RP0 confirmed this for all 17 MPFB reference realizations.
4. **Sculpt sources** (Gorrund, Saurin) are used as delivered. Any welded or repaired working copy is a derived file, with its own hash and a derivation record.

## 2. Naming and versioning

**File name pattern:** `<RACE>_<CFG>_<STATE>_RP<phase>_<step>_v<NNN>.<ext>`.

| Field | Values |
|---|---|
| CFG | `M` = configuration 1, `F` = configuration 2, `U` = single-configuration race |
| STATE | `REF`, `MIN`, `MAX`, `N`, `B`, `LOW` |

Examples: `GO_U_REF_RP1_retopo_v001.blend`, `GR_U_REF_RP2_retopo_v003.blend`.

**Output location:** `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/<Race>/RP<n>/`. The `source/` and `out/` folders are never written.

**Every production file has a sidecar `<name>.json` recording:**
- source path and hash;
- parent production file and hash;
- the operations applied;
- tool versions;
- author;
- gate status.

**Accepted production files** are frozen like sources: hash recorded and never overwritten. A new version gets a new `vNNN`.

## 3. Units, axes and origin

| Context | Rule |
|---|---|
| Real scale | 1 Blender unit = 1 m. Analysis and evidence in **cm**. UE5 import later at 1 uu = 1 cm (import scale fixed by a later UE5 contract) |
| Axes, production `.blend` | Z up, subject faces **−Y**, subject's left = **+X** (the convention of the Gorrund sculpt and the MPFB rig) |
| Axes, R-6 analysis frame | x = subject left, f = forward, u = up (cm). Converting between the two frames is a fixed mapping, never a re-orientation of the body |
| Ground | the lowest standing-contact vertex at z = 0 (stature measured crown to ground, tail excluded) |
| Origin | (0, 0, 0) = the pelvis-root landmark projected onto the ground plane |
| Midline | X = 0 at the sagittal plane of the trunk landmarks |
| Object transforms | location, rotation and scale applied (identity). One mesh object for the body; separate component objects are parented to nothing until rig prep |

## 4. Pose strategy

Three states are kept distinct.

| State | Definition | Use |
|---|---|---|
| **Reference measurement stance** | The source's accepted stance:<br>• MPFB races: R-6, 8° arm abduction, palms to thighs, plantigrade neutral (`tools/rac/w1/arm_lib.py`);<br>• Gorrund: frozen sculpt stance;<br>• Saurin: W2 reference stance | Anatomy truth; every deviation and landmark gate |
| **Rig-prep pose** (derived) | A **derived copy** in a joint-clearance pose for skinning, e.g. MPFB generator rest A-pose or a defined A-pose (proposal: about 40–45° shoulder abduction, small elbow flexion; final angle chosen with the skeleton family, RP6) | Skinning and weight painting only |
| **Runtime idle** | Any animated neutral idle | Not part of this program |

**Rules:**
1. **Retopology is done in the reference measurement stance.** The production mesh is fitted to the source in the pose the source was accepted in.
2. **A rig-prep pose copy is never made by moving vertices freely.** It is made only by a diagnostic armature (LBS) on the finished production mesh, driven from the §12 landmarks. The copy must satisfy:
   - (a) bone lengths and landmark-derived segment lengths are identical to the reference stance (tolerance §16 T-6);
   - (b) posing back to the reference stance reproduces the reference-stance production mesh within §16 T-1;
   - (c) the reference-stance file is never overwritten.
3. **No posing is authorized in RP0 or RP1.** RP1 delivers the reference-stance production mesh and landmarks only.

## 5. Component ownership

| Component | Rule |
|---|---|
| Body skin | **One** closed, manifold, watertight mesh per race state (genus per source) |
| Nails / claws | Part of the body mesh (fused, as accepted). Gorrund toenails and fingernails and Saurin claws keep their accepted form; no separate nail objects |
| Tails (Gorrund, Saurin) | Part of the body mesh, continuous through the tail root. No separate tail object |
| Ears, Saurin cranial display, rostrum | Part of the body mesh |
| Eyes | **Separate** eyeball objects (later; none of the sources has real eyeballs; MPFB has helper geometry only). The body keeps open eye-socket topology prepared for them only when the face topology is built (RP3–RP5); in RP1 the Gorrund eyes stay as sculpted |
| Teeth / tongue / mouth interior | **Separate** objects (later). In RP1 the mouth stays as sculpted (closed) |
| Hair, eyebrows, eyelashes, mane, fur cards | Not body topology. Out of scope |
| MPFB helper geometry (eye, teeth, tongue, tights, skirt, hair, joint cubes) | **Never** part of a production body. Removed from the derived production copy; kept in the regenerated source only |

## 6. Topology quality rules

The body production mesh must have:

| Rule | Requirement |
|---|---|
| Components, boundaries | 1 component; 0 boundary edges; 0 non-manifold edges and vertices |
| Duplicates, degenerates | 0 coincident duplicate vertices; 0 hidden shells; 0 degenerate faces |
| Self-intersection | 0 self-intersections in the reference stance, except accepted contact topology recorded per race. Gorrund's genus-3 hand and axilla loops are **repaired in RP1**, per §RP1 |
| Normals | Consistent outward |
| Face types | Quad-dominant: **≥ 98 % quads** overall and 100 % quads inside the deformation zones of §7 |
| Triangles | Allowed only outside the deformation zones, at density transitions |
| N-gons | 0 |
| Poles | Valence-3 and valence-5+ poles not on joint crease lines; ≥ 2 edge loops away from a crease line where possible |
| Face shape | No zero-area or folded faces. Quad interior angles 45°–135° (**T-4**); aspect ratio ≤ 4:1 outside the tail tip and digit tips (**T-4**) |
| Seams | No unwelded position seams in the production body. UV seams (when UVs exist) are split in UV only, never in positions |
| Symmetry | Symmetric topology across X = 0 where the source is symmetric. **Shape** asymmetry in the source is preserved (Gorrund tail, Saurin, Grask E3 trunk). Symmetric topology is not symmetric shape |

## 7. Joint / deformation zones

Each zone needs the listed **minimum supporting loops**: edge loops around the limb axis, perpendicular to it, centred on the landmark. The loop counts are production quality targets (T-5, accepted as RP1 quality targets).

| Zone | Minimum loops | Notes |
|---|---|---|
| Shoulder / axilla | 5 around the glenohumeral landmark | Plus a clean axillary fold; no tunnel or contact loop |
| Clavicle / scapular region | Flow follows the girdle (Grask girdle slope preserved) | |
| Elbow | 3 + crease loop | Olecranon support |
| Wrist | 3 | |
| Fingers | 3 per knuckle; 2 per IP joint | 5 digits per hand where canon says five |
| Hip / groin / gluteal fold | 5 | Plus a gluteal-fold loop |
| Knee | 3 + crease | Patellar support |
| Ankle | 3 | |
| Ball / toes | 2 per toe joint | Plantigrade contact sole kept flat-capable |
| Neck | 4 | |
| Jaw / mouth corners | Ring loops around the mouth; jaw-hinge support | |
| Eyes / orbit | Ring loops around the orbit | |
| Tail root (Gorrund, Saurin) | ≥ 4 rings at the tail root | Plus evenly spaced rings along the tail for a later chain, ≥ 1 ring per proposed tail segment (§12) |
| Spine / abdomen | Horizontal loops for flexion and twist | Composition support |

## 8. Creator-density zones

Density must stay high enough for the accepted creator ranges to be expressible as morphs later (master plan P-4). Proposed relative density, as **mean edge length ÷ stature** (T-5):

| Zone | Density | Why |
|---|---|---|
| Face, ears, Saurin display / rostrum | Highest; ≤ 0.25 % of stature | Craniofacial controls, ear families, display morphs |
| Hands, feet, digits | ≤ 0.3 % | Hand / foot size and joint controls; Gorrund nails |
| Trunk, pelvis, gluteal | ≤ 0.6 % | Frame (Narrow / Broad), composition, sex-related soft distribution |
| Limbs | ≤ 0.6 % | Muscularity / tendon organization (Grask cords and bellies) |
| Tail | ≤ 0.6 %, tapering to the tip | |

**Reference point.** The shared MPFB body (13,380 vertices) has a median edge of about 0.39 % of stature. **No final vertex budget** is set (§16).

## 9. Topology-family policy

Proposed from RP0 evidence; the full analysis is in the RP0 report §5.

1. **MPFB-derived family:** Marchfolk, Skarn, Sagekin, Fenn, Aelari, Vael, Halvren, Durrim, Pipkin, Cogling, and **Grask E3**.
   - All 11 accepted sources already share one topology: MPFB hm08, 13,380 body vertices, 13,378 quads, identical face index list, UVs, the 53-bone game-engine rig and weights.
   - The family may share **one production base topology**.
   - Race-specific **branches** (local edge-loop additions only, never vertex-order breaks without a recorded mapping) are required where anatomy needs them:
     - elven / Fenn / Aelari / Vael / Halvren ear families;
     - compact-race face, hand and foot density (Durrim, Pipkin, Cogling; Cogling 76 cm adult read);
     - Grask joint visibility, girdle and trunk organization (front-view identity).
   - Halvren must not become an "elf-percentage" interpolation: Halvren morph space is authored per source rules, not as a blend weight between topologies.
2. **Gorrund: unique** (leonine head and muzzle, tail, feline nails, sculpt source). It may share **standards** (§6–§8, §12), not topology.
3. **Saurin: unique** (rostrum, mandatory tail, scale fields, cranial display, claws, non-mammalian head–neck). Standards only. It is never forced into a mammalian head topology.
4. **Sharing test.** Topology may be shared only if every member's accepted source is reproduced within §16 T-1 / T-2 by that topology, and the race-specific anatomy is present.

## 10. UV readiness (this program)

- **MPFB family:** the MPFB UV layout exists and is carried, but it is **not** declared final.
- **Gorrund / Saurin:** no UVs exist. RP1 / RP5 deliver a **UV seam plan** (seam edge set marked on the production mesh) only. A UV unwrap is optional and non-final.
- Final UV layout, texel density, UDIMs and materials belong to a later material contract.
- No material may be used to fake race structure (P-7).

## 11. LOD readiness

- LOD0 production topology must be **LOD-generation-friendly**:
  - loops continuous enough for edge-collapse or loop-removal;
  - silhouette-critical loops identifiable (tagged loop sets for head profile, girdle, tail, digits).
- **No LOD counts or ratios** are set without a later performance contract.

## 12. Rig-facing landmark package

Each production mesh ships a landmark file `<name>_landmarks.json`:
- position in cm, R-6 analysis frame, plus the Blender frame;
- a local axis frame where a joint axis is defined;
- the source of each landmark: `source-rig` (MPFB joint centre), `surface-fit` (sphere / section fit on the mesh, method recorded) or `manual` (author-placed, with reason).

This is landmark prep, **not** skeleton-family finalization.

| Group | Landmarks |
|---|---|
| Root / pelvis | Pelvis root; left / right hip-joint centres (femoral head) |
| Legs | Knee centre and flexion axis; ankle centre and axis; ball (MTP) line; toe tips (5 per foot where canon) |
| Girdle / arm | Sternoclavicular joint; clavicle end / acromion; scapular proxy (inferior angle and medial border, where relevant: Grask GR-G2, Gorrund); glenohumeral centre; elbow centre and axis; wrist centre and axis; finger roots (MCP) and tips; thumb CMC |
| Axial | Spine stations matching the source's spine joints (MPFB: spine_01–03); neck base; head (atlanto-occipital) pivot; crown |
| Face | Jaw hinge (left / right), chin, eye centres (left / right), mouth corners |
| Tail (Gorrund, Saurin) | Tail-root centre and axis, then a centreline chain at proposed equal arc-length segments. Count proposed per race: Gorrund 12, Saurin 16, adjustable; the final chain is set by the rig contract |
| Race display | Ear root / tip (all races with ears); Saurin crest / display root points; Gorrund mane root boundary (if any) |

**Landmark rules:**
- **MPFB family:** joint centres come from the source rig (exact) and are carried unchanged.
- **Gorrund / Saurin:** landmarks are fitted on the **source** surface first, then re-measured on the production mesh. The difference is gated by T-6.

## 13. Anatomy-preservation validation (per production mesh)

| # | Check | Requirement |
|---|---|---|
| 1 | Source integrity | Hash before and after |
| 2 | Stature and ground | Stature within T-3; ground contact at z = 0; bbox within T-3 |
| 3 | Surface deviation, production → source and source → production | Signed distance, both directions, by zone: median, p95, max (T-1, T-2) |
| 4 | Silhouettes | Identical-camera front, profile, rear and 3/4 renders at the Stage C scale (3 px/cm). Body-only silhouette IoU against the source (T-7) |
| 5 | Landmarks | Source vs production landmark drift (T-6) |
| 6 | Race-specific metrics | e.g. Gorrund nail projection 1.55–1.74 mm and foot length; Grask GR-G1 / GR-P2b station readings unchanged; Saurin tail RSI; Cogling 76 cm head |
| 7 | Topology report | §6 counts, quad %, poles in zones, loops per §7 zone, density per §8 zone |
| 8 | Visual author sheet | Front / profile / rear / 3/4 plus close-ups of head, hands, feet, tail root and race-specific regions; source and production side by side and as an overlay |

## 14. Evidence package (per RP block)

Stored at `reviews/rac-rp<n>-evidence/`:
- source hashes;
- the production sidecar JSON;
- topology report;
- deviation report (JSON plus heat-map renders);
- landmark file plus drift table;
- silhouette IoU;
- author sheets;
- tools under `tools/rac/rp/`.

Gate document: `reviews/claude-rac-rp<n>-*-gate.md`.

## 15. Family-pilot acceptance rule

1. The **first** production mesh of each topology family needs explicit Tyler / ChatGPT acceptance before the family's other races start: Gorrund (RP1), Grask (RP2), Marchfolk (RP3, MPFB family), Durrim (RP4 compact branch), Saurin (RP5).
2. A production mesh that is clean but changes accepted anatomy beyond the accepted tolerances **fails**, regardless of topology quality.
3. Production work never reopens race biology. A true anatomy contradiction found during production is **stopped and returned** to the author.

## 16. PRODUCTION TOLERANCES (ACCEPTED for RP1, October 18, 2026)

**Accepted by:** Tyler / ChatGPT, `reviews/tyler-chatgpt-rac-rp1-gorrund-release-decisions.md` (c9d50b8). Written back by `reviews/chatgpt-rac-rp1-gorrund-manual-retopo-execute-order.md` (f8aa243).

These are **production standards, not biology canon**. The values RP0 proposed are kept below as history.

| ID | Accepted tolerance | RP0 proposal (history) |
|---|---|---|
| **T-1** Surface deviation, body, both directions | median ≤ 0.5 mm; p95 ≤ 1.5 mm; **max ≤ 3.0 mm** | max ≤ 4 mm |
| **T-2** Surface deviation, identity zones (head / muzzle, ears, hands, feet / toes / nails, tail root) | median ≤ 0.3 mm; **p95 ≤ 0.8 mm; max ≤ 1.5 mm** | p95 ≤ 1.0, max ≤ 2.5 mm |
| **T-3** Stature and bbox | stature ±1.0 mm; bbox ±2.0 mm per axis | same |
| **T-4** Face shape | quad angles 45°–135°; aspect ≤ 4:1 (except digit and tail tips): **accepted as RP1 quality target** | same |
| **T-5** Loops and density | §7 loop minimums; §8 density ceilings: **accepted as RP1 quality target** | same |
| **T-6** Landmark drift, production vs source | **target ≤ 1.0 mm; none above 1.5 mm; every value above 1.0 mm reported individually** | ≤ 2 mm (joint centres) |
| **T-7** Silhouette IoU vs source, body-only, front / profile / rear, identical camera and scale | ≥ 0.995 | same |
| **Gorrund nail projection** | ±0.15 mm from the frozen source measurement | proposed ±0.15 mm |

**Micro-detail exemption** (accepted). Only fine skin creases and nail-plate micro-edge detail that changes none of projection, taper, curl or silhouette. Every exemption is listed and shown.

**Visual veto** (accepted). A numeric pass does not override a visible identity change. For Gorrund, all of these must stay visually unchanged:
- head / muzzle;
- tail origin and taper;
- hand / foot read;
- nail read;
- body composition;
- accepted proportions;
- plantigrade foot read.

**RP1 method** (accepted). **M-B, fully manual retopology in the Blender UI.**
- QuadriFlow and automatic remesh are not used as the production topology generator.
- Production topology is manual polygon construction, with snapping / projection onto the derived welded working copy.

**Not proposed here:** a game vertex budget. RP1 reports the resulting count, and a budget waits for UE5 / performance evidence.
