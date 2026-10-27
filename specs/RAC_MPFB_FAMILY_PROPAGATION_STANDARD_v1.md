# RAC — MPFB Family Propagation Standard v1 (DRAFT)

**Status:** DRAFT, written from the first reuse validation (Skarn, order 85b7c1c). It is not yet accepted.
**Frozen base:** Marchfolk RP3 v003, `MF_RP3_v003_FREEZE.json` (sha256 `4af62f81…`), face topology hash `68f7b6a9…`, 57,674 V / 57,672 Q.
**Scope:** the **technical** pipeline only. The anatomy and identity judgement for each race stays an explicit human / author gate and is not standardised here.

## 1. Source regeneration identity

Rebuild each accepted race source from its build record:
- MPFB 2.0.17 and Blender 5.2.2;
- `tools/rac/w1/arm_lib.py` build → ground → `pose_r6` → ground;
- `height_macro` taken from the record.

The rebuilt source must be geometry-identical to the committed R-6: sha256(float32 V + int32 F) equal, max |dV| = 0. **Stop on mismatch.**

```
stc/python3 tools/rac/rp/marchfolk_rp3_v001/regen.py BUILD.json R6.npz src/
```

## 2. hm08 → frozen family base

1. Export the hm08 body from the regenerated source: `native_export.py SRC.blend src/ID_native.npz`.
2. Fit with `tools/rac/rp/mpfb_family/propagate.py FROZEN_BASE.blend FROZEN_HM08_MAP.npz src/ID_native.npz cand/ID_fam.npz`.

**Preconditions** (stop on failure): the race hm08 face list, `src_index` and UV layout equal the frozen map's.

**Rule:** production V = M @ (race hm08 R-6 V), where M is the frozen map. Faces, vertex order and per-corner UVs are the frozen base's.
- No topology change.
- No per-race relaxation or fitting.
- A race-specific branch needs an explicit author order.

## 3. Helper removal

Joint cubes and the eye, tongue, teeth, tights, skirt and hair helpers are excluded by `native_export.py`. The eye centres are kept as landmarks.

## 4. Production frame / origin

m, Z up, faces −Y, subject left +X. The origin is the MPFB `pelvis` head projected to the ground (`landmarks.py` → `frame.origin_translation_cm`). Write the file with `make_prod.py CAND LANDMARKS NAME OUTDIR "STATUS"`.

## 5. Topology identity check

- Production face topology hash = frozen hash.
- Verts / quads = 57,674 / 57,672.
- Map arrays identical to the frozen map.
- 1 component, 0 boundary edges, 0 non-manifold edges or vertices, 0 degenerate faces, outward normals (`audit.py`, `freeze_check.py`).

## 6. Joint validator v2 (`tools/rac/rp/marchfolk_rp3_v001/validator_v2.py`)

The base is the RP2 band method (loops crossed on four sides of a band, plus poles within 2 local loops) together with closed encircling rings: loops = max(rings, band).
- **firm** = loops ≥ minimum and no crease pole.
- **strict** = additionally no pole within 2 loops.

| Rule | Status | Effect |
|---|---|---|
| **D1** | accepted, 85b7c1c | A band side whose ray exit is undefined (no candidate faces the side, normal · side ≤ 0.3) is excluded. If no side is defined, the station uses closed rings at an anatomical radius (thumb MCP 3.0 cm). Statuses `PASS_FALLBACK_DEFINED_SIDES` and `PASS_FALLBACK_CLOSED_RING` are reported separately. |
| **D3** | accepted, 85b7c1c | For digit stations, a pole counts only if its nearest digit axis is the audited digit. Neighbouring tip-cap poles are not crease poles (`…+SCOPED_ADJACENT_DIGIT_POLE`). |
| **D4** | **proposed, not accepted** | Station geometry (band W, probe R, pole radius Rp, ring radius / window, anatomical radius) is defined on the family reference body (Marchfolk configuration 1, stature 173.143 cm) and scaled by race stature / 173.143 (`--scale-ref 173.143`). Without it, absolute-cm bands sample fewer loops on taller races with identical topology (Skarn ×1.20). |

Report legacy, D1 + D3 and (when proposed) D1 + D3 + D4 verdicts. **Never modify geometry to satisfy an undefined measurement.**

## 7. Density audit

`audit.py`: mean, median and p90 edge / stature per zone, against the contract §8 ceilings (face and ears 0.25 %, hands and feet 0.3 %, trunk and limbs 0.6 %). Do not decimate for tall races.

## 8. Anatomy T-1 / T-2 / T-3 / T-7

`anatomy.py R6 CAND OUT`:
- deviation in both directions, body and identity zones (head, ears, hands, feet);
- stature and bbox;
- silhouette IoU at 3 px/cm with 4× supersampling. The canvas grows to fit taller sources; Marchfolk-size results are unchanged.

Each configuration is judged on its own source. The race identity gate (for example Skarn C1R face) adds a race-specific comparison against the pre-identity source.

## 9. Face readiness

`face_rings.py`: mouth rings about the lip-slit centre, orbit rings, poles near the mouth, at its corners and near the eyes. The open orbit and lip pockets are kept.

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

Classify every failure as topology, weights, joint placement or contact / setup. Pair, fold and flip counts scale with face count (×4.3 from hm08).

## 11. Visual evidence set

`tools/rac/rp/mpfb_family/family_sheets.py WORK RACE ID:LABEL …`, one set per configuration with identical cameras:
- body (clay and wire);
- face (source vs family, wire, rings);
- close-ups (shoulder, elbow, hand, pelvis, knee, foot) with validator status;
- overlay (deviation and silhouette);
- density;
- the 69-station validator table;
- deformation pairs.

## 12. Manifest / gate template

`family_manifest.py WORK OUTDIR EVIDIR RACE ID:NAME:R6:BUILD …` writes:
- per-file sidecars;
- `<RACE>_RP3_family_propagation_manifest.json`: frozen base and map hashes, source and regeneration hashes, production hashes, topology identity.

**Gate decision:** PASS — ready for author freeze / NEEDS RACE-SPECIFIC BRANCH / FAIL, with the race identity gate answered explicitly.

## Known family-base margins (from the Skarn run)

These items are at zero margin on the reference body, so they can tip over on races with other proportions:
- hip band 5 / 5;
- toe-root (j1) bands 2 / 2;
- posterior-heel linear quad-centre deviation 1.45 mm against the 1.5 mm T-2 limit.

Treat them as watch items in every propagation.
