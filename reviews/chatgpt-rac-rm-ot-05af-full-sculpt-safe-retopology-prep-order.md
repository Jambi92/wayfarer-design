# RAC RM-OT-05AF — comprehensive sculpt-safe seam consolidation before any further sculpting

**Authority:** Tyler-authorized autonomous continuation after RM-OT-05AE final AC1 stop.
**Date:** October 16, 2026.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05ae-extended-seam-weld-final-ac1-gate.md` (06c68d6).

## 1. Route ruling

Honor the 05AE stop condition:

**Do not perform another AC1 sculpt retry in this order.**

The repeated failures now demonstrate that the limiting factor is the source mesh's large population of coincident duplicate seam vertices, not the artistic sculpt direction.

Move to the promised **retopology / sculpt-preparation route**:

> Build one comprehensive sculpt-safe working derivative in which all exact/coincident duplicate seams that can be safely consolidated for AC1–AC3 are welded in advance, while preserving visible surface geometry and protected anatomical interfaces.

This is a preparation block only. No composition sculpt is authorized here.

## 2. Advancement source

Start from the cleanest passed sculpt-safe baseline:

`GO-05AE_sculpt_safe_baseline.blend`
SHA-256:
`f1df5b334c6d21c06d39cceeff2a2ddaf4282cba79873a25d3454732192bfca8`

Review GLB:
`GO-05AE_sculpt_safe_baseline.glb`
SHA-256:
`6b2c672f5139112ed58a8830e6b0ed9da7dda3a66fe499f27f5f15f710d3ef40`

Rejected 05AE AC1 remains evidence only and must not be used as the source.

## 3. Goal

Create a single **full sculpt-working derivative** that removes the seam-opening failure mode before any more manual sculpt work.

The result is not production topology and not canon. It is a reference-anatomy sculpt workspace.

Target output:

`GO-05AF_full_sculpt_safe_baseline.blend`
`GO-05AF_full_sculpt_safe_baseline.glb`

## 4. Allowed seam consolidation

Use exact/coincident duplicate groups only.

### Merge threshold

Maximum pairwise merge distance:

**0.01 mm**

Prefer groups whose actual spread is 0.000 mm.

Do not merge visibly distinct surfaces simply because they are near each other.

### Coverage

Evaluate the entire organism, not just a z-band.

Merge exact duplicate seam groups across regions expected to receive AC1–AC3 sculpt brush falloff:

- torso;
- chest;
- abdomen;
- flanks;
- shoulders / axilla;
- upper and lower arms;
- thighs;
- knees;
- calves;
- posterior pelvis / gluteal region where later AC3 may sculpt;
- neck-base transition used by AC1.

The purpose is to prevent a future mask edge or brush falloff from encountering another unwelded duplicate seam a few millimetres beyond an arbitrary band.

## 5. Protected / excluded interfaces

Do **not** automatically weld every duplicate group in the file.

First classify all remaining duplicate groups by anatomical region and interface risk.

Preserve from automatic consolidation unless proven to be harmless display/import duplication:

- face / muzzle / eyelids / lips / nostrils;
- ears and ear folds;
- finger-to-finger or toe-to-toe proximity;
- nail boundaries if they encode distinct surfaces;
- genital opening / crease landmarks;
- tail-body junction and current tail-root/gluteal fusion;
- any duplicate group whose members lie on genuinely distinct opposing surfaces;
- any group whose consolidation changes genus / manifold interpretation unexpectedly.

Head, hands, feet and free tail remain **non-sculpt regions** for AC1–AC3, so there is no need to chase seams there unless they are merely passive duplicates needed for overall topology consistency.

## 6. Classification pass before applying

Before any merge:

1. enumerate all remaining coincident duplicate groups;
2. group them by anatomical region;
3. report:
   - group count;
   - vertex count;
   - group-size distribution;
   - bounding boxes / z-ranges;
   - exact max spread;
4. identify:
   - **SAFE_SCULPT_SEAM** — exact duplicate representation of one continuous surface;
   - **PROTECTED_INTERFACE** — possible meaningful separate surface / opening / fold;
   - **UNKNOWN** — cannot safely classify.

Only `SAFE_SCULPT_SEAM` groups may be merged automatically.

If a large number of groups remain UNKNOWN in an area AC1–AC3 must sculpt, STOP with a map/report rather than guessing.

## 7. Topology-prep method

Allowed:
- Blender/bmesh Merge by Distance / weld_verts;
- scripts for exact-duplicate classification, mapping, validation and reporting;
- removal of UV/custom-normal/display-only attributes on the sculpt-working derivative if required.

Forbidden:
- remesh;
- voxelization;
- decimation;
- Dyntopo;
- shrinkwrap;
- surface projection;
- coordinate smoothing;
- sculpting;
- moving vertices;
- filling holes;
- deleting anatomy;
- changing joint positions;
- altering tail-root geometry;
- changing head/hands/feet shape.

No vertex position may change except through collapse of exact/coincident duplicates onto the same existing position.

## 8. Required gates

The 05AF baseline must satisfy all of the following.

### Surface identity
- old-to-new vertex/surface deviation: **0.000 mm** for merged groups;
- new-to-old Hausdorff / nearest-surface deviation: **0.000 mm**;
- triangle surfaces position-identical after remap wherever topology is collapsed;
- stature unchanged;
- bounding box unchanged;
- macro Gorrund proportions unchanged.

### Geometry integrity
- one position-welded organism;
- 0 position-welded boundary edges;
- 0 non-manifold edges;
- 0 self-intersections;
- 0 flipped faces;
- 0 degenerate faces.

### Protected anatomy
- head: 0.000 mm positional change;
- hands: 0.000 mm positional change;
- feet: 0.000 mm positional change;
- free tail: 0.000 mm positional change;
- major pelvis landmarks: 0.000 mm positional change;
- digit counts unchanged;
- topology of protected meaningful interfaces unchanged unless specifically documented as a duplicate-only collapse.

### Sculpt-safety diagnostics
Simulate / report whether coincident duplicate groups remain in the intended AC1–AC3 sculpt zones.

Required target:
- **0 SAFE_SCULPT_SEAM duplicate groups remaining inside intended AC1–AC3 sculptable regions.**

Any remaining duplicates there must be listed explicitly as protected/intentional and mapped.

## 9. Diagnostic dry test — no sculpt

After the weld passes, perform a **non-authoring seam-stability diagnostic** only.

Allowed diagnostic:
- duplicate the prepared mesh in memory/scratch;
- apply a tiny uniform test displacement or Blender brush-equivalent diagnostic to selected seam-neighborhood samples solely to detect whether coincident copies separate.

This diagnostic must not become the saved baseline and must not be a composition sculpt.

Alternatively, if a purely topological proof suffices, document why brush separation cannot occur in the consolidated regions.

## 10. PASS / FAIL

### PASS

Return:

**05AF FULL SCULPT-SAFE RETOPOLOGY PREP PASS / READY FOR NEW 05AC SCULPT ORDER**

Freeze:
- exact baseline hashes;
- classification report;
- old→new vertex map;
- protected-interface map;
- evidence views.

Then STOP.

Do not perform AC1, AC2 or AC3 in 05AF.

### FAIL

Return:

**05AF SCULPT-SAFE RETOPOLOGY PREP NOT SAFE / HUMAN RETOPOLOGY REQUIRED**

if:
- meaningful anatomical interfaces cannot be separated from display duplicates safely;
- surface identity cannot be maintained;
- topology becomes invalid;
- sculpt zones still contain unavoidable duplicate seams likely to open.

Then STOP.

## 11. State

No canon promotion.

- Gorrund UNACCEPTED;
- Grask E3 FROZEN;
- RM-OT-05 OPEN;
- Stage C BLOCKED;
- no LOW / blind final acceptance / scaffold;
- no D4 / UE5 / production rigging / creator implementation.

## 12. Return

Commit:

`reviews/claude-rac-rm-ot-05af-full-sculpt-safe-retopology-prep-gate.md`

Evidence:

`reviews/rac-rmot05af-evidence/`

Preserve all 05AB1/05AD/05AE baselines and rejected AC1 attempts unchanged.
