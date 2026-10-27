# RAC — MPFB Family Propagation Standard v1

**Status: AUTHOR-ACCEPTED TECHNICAL STANDARD v1** (order 78a109f, 2026-10-27).
- Written from the first reuse validation (Skarn, 85b7c1c); revised by a18371c and 33a2dfe; promoted by 78a109f; D6 added by d921903.
- Validator: **D1 + D3 + D4 + D5 + D6**, all accepted and authoritative (§6).
- Active family base: **MPFB Family Base v005**, frozen by `MPFB_FAMILY_BASE_v005_FREEZE.json`.

> **The technical propagation process is standardized. Race anatomy, identity, cultural appearance, and race-specific branches remain explicit author-review gates and are never auto-approved merely because the technical pipeline passes.**

**Family base**

| | Role | Record | Face topology hash | Verts / quads | hm08 map |
|---|---|---|---|---|---|
| v003 (Family Base v1) | historical, frozen | `MF_RP3_v003_FREEZE.json` (`4af62f81…`) | `68f7b6a9…` | 57,674 / 57,672 | `bc3b7c54…` |
| v004 (margin hardening) | provenance only | `MPFB_FAMILY_BASE_v004.json` | `2bd4c8b3…` | 57,854 / 57,852 | `19a83550…` |
| **v005 (Family Base v2, final)** | **ACTIVE, frozen** | `MPFB_FAMILY_BASE_v005_FREEZE.json` | `ec768ae210ea3ee1c053d0c4cd3256d57dad6db35d515502706b74f64281bee0` | 57,842 / 57,840 | `e690fbafb53adc27…` |

The active base is used by every new MPFB-family race:
- **map:** `MPFB_FAMILY_BASE_v005_hm08_map.npz` (full hash in the freeze record);
- **base file:** `MF_M_REF_RP3_retopo_v005.blend` (UVs / face list).

Frozen realizations on it:
- Marchfolk `MF_{M,F}_REF_RP3_retopo_v005`;
- Skarn `SK_{M,F}_REF_RP3_retopo_v003`;
- Sagekin `SG_{M,F}_REF_RP3_retopo_v001` (SG / SGF178; `SAGEKIN_RP3_FREEZE.json`, d921903).

**Scope:** the **technical** pipeline only. Not standardised here:
- race anatomy judgements;
- face identity judgements;
- cultural appearance;
- ear branches and compact-race branches;
- biological creator ranges.

## 1. Source regeneration identity

Rebuild each accepted race source from its build record:
- MPFB 2.0.17 and Blender 5.2.2;
- `tools/rac/w1/arm_lib.py` build → ground → `pose_r6` → ground;
- `height_macro` taken from the record.

The rebuilt source must be geometry-identical to the committed R-6: sha256(float32 V + int32 F) equal, max |dV| = 0. **Stop on mismatch.**

```
stc/python3 tools/rac/rp/marchfolk_rp3_v001/regen.py BUILD.json R6.npz src/
```

## 2. hm08 → family base

1. Export the hm08 body from the regenerated source: `native_export.py SRC.blend src/ID_native.npz`.
2. Fit with `tools/rac/rp/mpfb_family/propagate.py FAMILY_BASE.blend FAMILY_HM08_MAP.npz src/ID_native.npz cand/ID_fam.npz`.

**Preconditions** (stop on failure): the race hm08 face list, `src_index` and UV layout equal the family map's.

**Rule:** production V = M @ (race hm08 R-6 V), where M is the family map.
- Faces, vertex order and per-corner UVs are the family base's.
- No topology change.
- No per-race relaxation or fitting.
- A race-specific branch needs an explicit author order.

**Map invariants (proven for v004 and v005):**
- every row is convex: row sum 1, no negative weight, at most 4 hm08 weights;
- weights, UVs and MPFB targets transfer through M by linearity (`MPFB_FAMILY_v005_transfer_proof.json`).

## 3. Helper removal

Joint cubes and the eye, tongue, teeth, tights, skirt and hair helpers are excluded by `native_export.py`. The eye centres are kept as landmarks.

## 4. Production frame / origin

m, Z up, faces −Y, subject left +X. The origin is the MPFB `pelvis` head projected to the ground (`landmarks.py` → `frame.origin_translation_cm`). Write the file with `make_prod.py CAND LANDMARKS NAME OUTDIR "STATUS"`.

## 5. Topology identity check

- Production face topology hash = family hash.
- Vertex and quad counts equal the family base.
- Map arrays identical to the family map.
- 1 component, 0 boundary edges, 0 non-manifold edges or vertices, 0 degenerate faces, outward normals (`audit.py`, `freeze_check.py` read-back).

## 6. Joint validator v2

Implementation: `tools/rac/rp/marchfolk_rp3_v001/val2lib.py`, with CLI `validator_v2.py CAND OUT --scale-ref 173.143 --d5` (authoritative). Its verdicts were regression-checked as identical to the v003 / Skarn outputs.

**Method.** The base is the RP2 band method (loops crossed on four sides of a band, plus poles within 2 local loops) together with closed encircling rings: loops = max(rings, band).
- **firm** = loops ≥ minimum and no crease pole.
- **strict** = additionally no pole within 2 loops.

**Hierarchy:** ordinary band → D1 → D3 → D4 → D5 → D6. Authoritative CLI: `validator_v2.py CAND OUT --scale-ref 173.143 --d5 --d6-native src/<ID>_native.npz`.

| Rule | Status | Effect |
|---|---|---|
| **D1** | accepted, 85b7c1c | A band side whose ray exit is undefined is excluded (no probe candidate passes the facing test, normal · side ≤ 0.3). If no side is defined, the station uses closed rings at an anatomical radius (thumb MCP 3.0 cm). Statuses `PASS_FALLBACK_DEFINED_SIDES` and `PASS_FALLBACK_CLOSED_RING` are reported separately. |
| **D3** | accepted, 85b7c1c | For digit stations, a pole counts only if its nearest digit axis is the audited digit (`…+SCOPED_ADJACENT_DIGIT_POLE`). |
| **D4** | **accepted (a18371c; permanent 33a2dfe / 78a109f)** | station_scale = race stature / 173.143 (Marchfolk configuration 1). It scales band width W, probe radius R, pole radius Rp, ring radius / axial window and the anatomical fallback radius. **Authoritative.** |
| **D5** | **accepted (33a2dfe; permanent 78a109f)** | For digit stations only: a band side is undefined when the endpoint selected at either band end lies farther from its probe line than W (no vertex of the digit's own cross-section answers the probe; the selection fell across an inter-digital web). The side is excluded exactly as D1 excludes one and never lowers a topology verdict. The status records it (`…+D5_INTERDIGITAL_UNDEFINED`); every station lists its `valid_sides` and `D5_undefined_sides`. **Authoritative with D4.** |
| **D6** | **accepted (proposed c6c7940; accepted d921903)** | For **non-digit** stations only (neck, shoulder, elbow, wrist, hip, knee, ankle): a band side is undefined when the endpoint selected at either band end is on a **foreign body segment**, i.e. its dominant skin bone is not one of the station's own bones (table below). The side is excluded exactly as D1 excludes one; if every side is excluded the station falls back to closed rings (D1). It never lowers a topology verdict. Each side reports `endpoint_dominant_bone` / `endpoint_dominant_weight`; the station lists `D6_undefined_sides`, and a fallback status records `…+D6_FOREIGN_SEGMENT_UNDEFINED`. **Authoritative with D4 + D5.** |

**D6 purpose.** In the R-6 stance some probe balls reach a neighbouring body part and count *its* loops: the hip lateral side (+p left / −p right) lands on the hanging forearm or hand, and the elbow medial side lands on the trunk (`spine_02`). This held on all six validated realizations (MF-M, MF-F, SK-C1R, SK-F, SG, SGF178) and passed unnoticed until the longer Sagekin forearm dropped that forearm count to 4 (SG hip 4 / 5). D6 corrects measurement ownership; it does not weaken the topology standard.

**D6 ownership method.** Skin weights are the race's native hm08 source deform weights carried through the family map (W_family = M @ W_hm08; the same linear transfer as §2). The dominant bone of an endpoint vertex is its largest weight. Implementation: `val2lib.D6_OWN`, `evaluate(..., d6=(W_family, bone_names))`.

| Station | Own bones (side s) |
|---|---|
| neck | neck_01, head, spine_03 |
| shoulder | clavicle_s, upperarm_s, spine_03, spine_02 |
| elbow | upperarm_s, lowerarm_s |
| wrist | lowerarm_s, hand_s |
| hip | pelvis, spine_01, thigh_s |
| knee | thigh_s, calf_s |
| ankle | calf_s, foot_s, ball_s |

Digit stations are not subject to D6; D3 (pole ownership) and D5 (interdigital endpoints) cover them.

**D6 regression requirement.** Any change to D6 (or to its bone table) must be re-run on every validated family realization with `tools/rac/rp/sagekin_rp3_v001/d6_regression.py`, which compares D1 + D3 + D4 + D5 with D1 + D3 + D4 + D5 + D6 and audits every non-digit band side (endpoint bones and weights, the side path's body zones). Required: no verdict or loop count lowered; no false positive (an excluded side whose path lies in the station's own body region). Baseline (d921903, `reviews/rac-rp3-evidence/sagekin_rp3_freeze/D6_regression/`): 7 joints × 6 realizations audited; exclusions only at hip (forearm / hand) and elbow (trunk); 0 false positives; 69 / 69 on all six.

**Never modify geometry or topology to satisfy a band side that D6 proves belongs to another segment.**

**Reporting.**
- Report legacy, D1 + D3, D1 + D3 + D4, D1 + D3 + D4 + D5 and D1 + D3 + D4 + D5 + D6 verdicts. **D1 + D3 + D4 + D5 + D6 is authoritative.** Earlier validator outputs remain historical evidence only.
- Every station also reports its margin (loops − minimum); every band side reports its endpoint offsets.
- `tools/rac/rp/mpfb_family/margin_table.py` writes the family margin table.

**Never modify geometry to satisfy an undefined measurement.** Legacy fixed-cm station verdicts are reference only and are never authoritative on differently sized races.

**Measurement note (a18371c).** In the left-handed analysis frame the probe's facing test uses vertex normals that point *inward* numerically.
- A side's endpoint therefore usually lies on the surface facing **away** from the named side direction: "+q" samples the −q surface of a thin digit.
- On thick segments it can land on another body part.
- This holds for every gate since RP2 and changes no verdict. Read D1 / D5 / D6 in that light.

## 7. Density audit

`audit.py`: mean, median, p90 and p95 edge / stature per zone (9 zones), against the contract §8 ceilings on the mean:
- face and ears 0.25 %;
- hands and feet 0.3 %;
- trunk and limbs 0.6 %.

Do not decimate for tall races.

## 8. Anatomy T-1 / T-2 / T-3 / T-7, contact, identity

- **Anatomy:** `anatomy.py R6 CAND OUT`.
  - Deviation in both directions, body and identity zones (head, ears, hands, feet).
  - Stature and bbox.
  - Silhouette IoU at 3 px/cm with 4× supersampling. The canvas grows for tall sources.
  - Each configuration is judged on its own source.
- **Contact:** `contact_v4.py` compares self-intersection pairs against the parent-base fit. A pair can only be new where a face touches a changed / new vertex. Any new family-base contact defect is a stop condition.
- **Race identity gate** (for example Skarn C1R): `tools/rac/rp/mpfb_family/face_identity.py`.
  - Face distance to the identity source vs to the rigidly aligned pre-identity source.
  - Identity signal on the anterior-face hm08 vertices.

## 9. Face readiness

`face_rings.py`:
- mouth rings about the lip-slit centre and orbit rings;
- poles near the mouth, at its corners and near the eyes.

The open orbit and lip pockets are kept. No face topology change is authorised by this standard.

## 10. Limited deformation sanity

`mf_deform.py NATIVE CAND OUTDIR TAG`, run on the source hm08 and on the family candidate with the source rig and weights carried through the map.

Poses:
- shoulder abd45 / abd90 / flex90;
- elbow 90 / 130;
- wrist flex / ext;
- fist;
- thumb opposition;
- hip flex90;
- knee 90 / 140;
- ankle dorsiflexion;
- toe flex / ext;
- trunk twist;
- neck flex / rotation.

**Classify** every failure as topology, weights, joint placement or contact / setup. Pair, fold and flip counts scale with face count (×4.3 from hm08).

**For a family-base change**, trace flipped faces to their parent-base faces, then apply the fold test (`MPFB_v005_flip_parentage.json` method).
- A flip whose parent face also flipped is the same defect on more faces.
- A flip whose parent quad already folds in the posed parent geometry is a parent fold: LBS rig class.
- Only the remainder is topology-attributable.

**For a propagation (no topology change)**, compare against the native hm08 and the reference realization; record rig-class items in the carry-forward register (§14).

## 11. Race-specific identity gate

- Every race with an accepted identity source (for example Skarn C1R) proves that the family realization lies on that source and has not regressed toward the pre-identity / generic face (`face_identity.py`).
- Also run any further identity comparison the race's canon requires.
- **This gate and the race anatomy review are author decisions.** A technical PASS never auto-approves them.
- A true race anatomy feature that needs different topology is returned as NEEDS RACE-SPECIFIC BRANCH. It is never patched inside the family base.

## 12. Visual evidence package

- **Propagation:** `family_sheets.py`. Body (clay / wire), face, joint close-ups, overlay, density, validator table, deformation.
- **Family-base change:** `v4_sheets.py` / `v5_sheets.py`. Topology overview, changed-patch close-ups, before / after, pole / valence, T-4 and aspect heat, source deviation, deformation, identity, validator / margin table, change diagram.
- Cameras are identical across configurations.
- No gate returns without its sheets.

## 13. Manifest / freeze template

- **Writers:** `family_manifest.py` (propagation) or `family_manifest_v4.py` / `family_manifest_v5.py` (family-base successor). They write:
  - per-file sidecars;
  - the manifest: active base and map hashes, source and regeneration hashes, production hashes, topology identity, row classes.
- **Propagation gate decision:** PASS — READY FOR AUTHOR FREEZE / NEEDS RACE-SPECIFIC BRANCH / FAIL, with the race identity gate answered explicitly.
- **Freeze by record.** Files are never re-saved to change status. The freeze record (template: `MPFB_FAMILY_BASE_v005_FREEZE.json`) carries:
  - full file / geometry / face / map / sidecar / landmark hashes;
  - read-back results (`freeze_check.py`, `freeze_v5_verify.py`);
  - validator rules and results;
  - accepted exceptions;
  - the provenance chain.
- The record is authoritative over sidecar / embedded status strings.

## 14. Carry-forward issue recording

- Items accepted at a freeze that belong to a later stage (rigging, weighting, correctives, articulation) go into `specs/RAC_PRODUCTION_RIG_CARRY_FORWARD_REGISTER.md`, each with:
  - an ID and the configuration;
  - a measured description and the owning stage;
  - the evidence path.
- A carry-forward item is never topology-blocking and never reopens a frozen base.
- Earlier race registers (for example Grask RP2) are referenced, not merged.

## 15. Stop rules

- **Stop on:**
  - any source-identity mismatch;
  - a frozen-file / map hash mismatch;
  - a topology-identity failure;
  - a new rest contact defect;
  - anatomy failure.
- **Stop** for author review after every gate. Do not start the next race, rigging, creator morphs, final UV / materials, LODs or UE5 without an explicit order.
- **Never** change the active family topology inside a race propagation.

## Active family-base margins (frozen v005)

Table (D1 + D3 + D4 + D5): `reviews/rac-rp3-evidence/mpfb_family_base_final_toe2/audit/MPFB_FAMILY_v005_margin_table.{json,csv}`. Firm 69 / 69 on MF-M, MF-F, SK-C1R and SK-F.

Table (D1 + D3 + D4 + D5 + D6, authoritative since d921903, six realizations incl. Sagekin SG / SGF178): `reviews/rac-rp3-evidence/sagekin_rp3_freeze/MPFB_family_margin_table_D1-D6.csv`, sheet `sheets/MPFB_family_margin_D1-D6.jpg`. Firm 69 / 69 on all six. D6 excludes sides only at hip and elbow, and changes loop counts only at the hip: SG 4 → 6, SGF178 12 → 15, SK-F 12 → 18 (MF-M, MF-F, SK-C1R unchanged); every other margin is unchanged.

**At margin 0 in all four:** `toe1_j1_l/r` (2 / 2). **At margin 0 somewhere:**

| Station | Configurations at the minimum |
|---|---|
| `toe2_j1_l/r` | MF-M (web side valid, 2 / 2), SK-C1R (dorsal side, 2 / 2) |
| `thumb_mcp_l/r` | MF-M, SK-C1R |
| `toe2_j2_l/r` | MF-M |
| `toe4_j1_l/r` | MF-M, MF-F, SK-C1R |
| `hip_l/r` | SK-C1R (5 / 5) |
| `thumb_mcp`, `toe2_j1`, `toe4_j1` | also SG (Sagekin c1); SGF178 at 0 only on `toe1_j1` / `toe4_j1` |

**Heel:** foot T-2 max MF-M 0.92, MF-F 0.83, SK-C1R 1.19, SK-F 0.87 mm (retained from v004).

**Toe 2:** dorsal racetrack (no closed ring). Its patch has aspect ≤ 4.7 and no quad with aspect > 10.

**Accepted exception (carry-forward MPFB-CF-1 / -2):** toe extension 30°, female configurations only. 3 (MF-F) / 2 (SK-F) topology-attributable flipped faces in the toe-2 MTP crease. Class: production-rig / toe-weighting.

## Propagation checklist (per new MPFB-family race)

1. Regenerate the accepted source; prove geometry identity (§1). Stop on mismatch.
2. Export hm08; check face list / `src_index` / UV against the active family map (§2).
3. Realise V = M @ race hm08 with the active map; no topology change, no fitting (§2).
4. Write the production file in the production frame (§4); read it back exactly (`freeze_check.py`, §5).
5. Topology identity and integrity (§5).
6. Validator D1 + D3 + D4 + D5 + D6, 69 / 69 firm; family margin table (§6).
7. Density, 9 zones (§7).
8. Anatomy T-1 / T-2 / T-3 / T-7; contact against the family parent; race identity gate (§8).
9. Face readiness (§9).
10. Deformation sanity, classified (§10).
11. Race identity gate (§11).
12. Visual evidence package (§12); manifest and sidecars (§13).
13. Carry-forward items recorded (§14).
14. STOP for author review (§15). Race anatomy and identity approval are never automated.
