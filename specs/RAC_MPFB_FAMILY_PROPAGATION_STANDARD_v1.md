# RAC — MPFB Family Propagation Standard v1 (DRAFT)

**Status:** DRAFT — **ready for promotion pending one author decision.** It is not yet promoted to AUTHOR-ACCEPTED TECHNICAL STANDARD v1.
- Written from the first reuse validation (Skarn, order 85b7c1c); revised by orders a18371c and 33a2dfe.
- **D4 and D5 are accepted** (order 33a2dfe §2). The authoritative validator is D1 + D3 + D4 + D5 (§6).
- The final family-base candidate v005 is 69 / 69 firm on all four configurations. Promotion (order 33a2dfe §18) needs every gate to pass. One deformation item is open: 3 (MF-F) / 2 (SK-F) toe-extension flips in the new toe-2 support. The gate returned FAMILY BASE PASS WITH DOCUMENTED TOE2 EXCEPTION — AUTHOR DECISION (`reviews/claude-rac-rp3-mpfb-family-base-final-toe2-web-gate.md`).

**Family base**

| | Role | Record | Face topology hash | Verts / quads | hm08 map |
|---|---|---|---|---|---|
| Frozen v003 (MPFB Family Base v1) | **active** (historical v1) | `MF_RP3_v003_FREEZE.json` (`4af62f81…`) | `68f7b6a9…` | 57,674 / 57,672 | `bc3b7c54…` |
| v004 (margin hardening) | provenance only | `MPFB_FAMILY_BASE_v004.json` | `2bd4c8b3…` | 57,854 / 57,852 | `19a83550…` |
| **v005 (final successor)** | **candidate, NOT frozen** | `MPFB_FAMILY_BASE_v005.json` | `ec768ae2…` | 57,842 / 57,840 | `e690fbaf…` |

v005 becomes the active base only when the author freezes it. **Technical process is standardised; race anatomy and identity remain explicit author gates.**

**Scope:** the **technical** pipeline only.
- The anatomy and identity judgement for each race stays an explicit human / author gate. It is never automated away.
- Not standardised here: race anatomy judgements, face identity judgements, ear branches, compact-race branches and biological creator ranges.

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

**Map invariants (proven for v004):**
- every row is convex: row sum 1, no negative weight, at most 4 hm08 weights;
- weights, UVs and MPFB targets transfer through M by linearity (`MPFB_FAMILY_v004_transfer_proof.json`).

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

Implementation: `tools/rac/rp/marchfolk_rp3_v001/val2lib.py`, with CLI `validator_v2.py CAND OUT [--scale-ref 173.143]`. Its verdicts were regression-checked as identical to the v003 / Skarn outputs.

**Method.** The base is the RP2 band method (loops crossed on four sides of a band, plus poles within 2 local loops) together with closed encircling rings: loops = max(rings, band).
- **firm** = loops ≥ minimum and no crease pole.
- **strict** = additionally no pole within 2 loops.

**Hierarchy:** ordinary band → D1 → D3 → D4 → D5. Authoritative CLI: `validator_v2.py CAND OUT --scale-ref 173.143 --d5`.

| Rule | Status | Effect |
|---|---|---|
| **D1** | accepted, 85b7c1c | A band side whose ray exit is undefined is excluded (no probe candidate passes the facing test, normal · side ≤ 0.3). If no side is defined, the station uses closed rings at an anatomical radius (thumb MCP 3.0 cm). Statuses `PASS_FALLBACK_DEFINED_SIDES` and `PASS_FALLBACK_CLOSED_RING` are reported separately. |
| **D3** | accepted, 85b7c1c | For digit stations, a pole counts only if its nearest digit axis is the audited digit (`…+SCOPED_ADJACENT_DIGIT_POLE`). |
| **D4** | **accepted, a18371c** | station_scale = race stature / 173.143 (Marchfolk configuration 1). It scales band width W, probe radius R, pole radius Rp, ring radius / axial window and the anatomical fallback radius. **Authoritative.** |
| **D5** | **accepted, 33a2dfe** | For digit stations only: a band side is undefined when the endpoint selected at either band end lies farther from its probe line than W (no vertex of the digit's own cross-section answers the probe; the selection fell across an inter-digital web). The side is excluded exactly as D1 excludes one and never lowers a topology verdict. The status records it (`…+D5_INTERDIGITAL_UNDEFINED`); every station lists its `valid_sides` and `D5_undefined_sides`. **Authoritative with D4.** |

**Reporting.**
- Report legacy, D1 + D3, D1 + D3 + D4 and D1 + D3 + D4 + D5 verdicts. **D1 + D3 + D4 + D5 is authoritative.**
- Every station also reports its margin (loops − minimum); every band side reports its endpoint offsets.
- `tools/rac/rp/mpfb_family/margin_table.py` writes the family margin table.

**Never modify geometry to satisfy an undefined measurement.**

**Measurement note (a18371c).** In the left-handed analysis frame the probe's facing test uses vertex normals that point *inward* numerically.
- A side's endpoint therefore usually lies on the surface facing **away** from the named side direction: "+q" samples the −q surface of a thin digit.
- On thick segments it can land on another body part.
- This holds for every gate since RP2 and changes no verdict. Read D1 / D5 in that light.

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

**For a family-base change**, trace flipped faces to their parent-base faces (`MPFB_v004_flip_parentage.json` method). A flip whose parent face also flipped is the same defect on more faces; one whose parent did not flip is topology-attributable.

## 11. Visual evidence set

- `family_sheets.py` (propagation);
- `v4_sheets.py` (family-base change): topology overview, changed-patch close-ups, before / after maps, overlay, density, T-4, deformation, identity, validator and margin table, change diagram.

Cameras are identical across configurations.

## 12. Manifest / gate template

- `family_manifest.py` (propagation) or `family_manifest_v4.py` (family-base successor) writes:
  - per-file sidecars;
  - the manifest: parent base and map hashes, source hashes, production hashes, topology identity, row classes.
- **Propagation gate decision:** PASS — ready for author freeze / NEEDS RACE-SPECIFIC BRANCH / FAIL, with the race identity gate answered explicitly.

## Family-base margins (D1 + D3 + D4 + D5, final candidate v005)

Table: `reviews/rac-rp3-evidence/mpfb_family_base_final_toe2/audit/MPFB_FAMILY_v005_margin_table.{json,csv}`. Firm 69 / 69 on MF-M, MF-F, SK-C1R and SK-F.

**At margin 0 in all four:** `toe1_j1_l/r` (2 / 2). **At margin 0 somewhere:**

| Station | Configurations at the minimum |
|---|---|
| `toe2_j1_l/r` | MF-M (web side valid, 2 / 2), SK-C1R (dorsal side, 2 / 2) |
| `thumb_mcp_l/r` | MF-M, SK-C1R |
| `toe2_j2_l/r` | MF-M |
| `toe4_j1_l/r` | MF-M, MF-F, SK-C1R |
| `hip_l/r` | SK-C1R (5 / 5) |

**Heel:** foot T-2 max MF-M 0.92, MF-F 0.83, SK-C1R 1.19, SK-F 0.87 mm (retained from v004).

**Toe 2:** dorsal racetrack (no closed ring). Its patch has aspect ≤ 4.7 and no quad with aspect > 10.

**Open deformation item:** toe extension 30°, female configurations only. 3 (MF-F) / 2 (SK-F) newly flipped faces are not explained by a fold of their parent quad.

## Propagation checklist (per new MPFB-family race)

1. Regenerate the accepted source; prove geometry identity (§1). Stop on mismatch.
2. Export hm08; check face list / `src_index` / UV against the active family map (§2).
3. Realise V = M @ race hm08 with the active map; no topology change, no fitting (§2).
4. Write the production file in the production frame (§4); read it back exactly (`freeze_check.py`, §5).
5. Topology identity and integrity (§5).
6. Validator D1 + D3 + D4 + D5, 69 / 69 firm; family margin table (§6).
7. Density, 9 zones (§7).
8. Anatomy T-1 / T-2 / T-3 / T-7; contact against the family parent; race identity gate (§8).
9. Face readiness (§9).
10. Deformation sanity, classified (§10).
11. Visual evidence set (§11); manifest and sidecars (§12).
12. Author gates: race anatomy and identity (never automated).
