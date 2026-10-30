# ChatGPT Order — RAC RP3 Halvren Whole-Character Final Author Acceptance / Freeze Closure

**Repository:** `Jambi92/wayfarer-design`  
**Branch:** `main`  
**Reviewed Claude commit:** `e93f90cde863ebab31a5d5a588f8a1a9d357b94a`  
**Scope:** Halvren RP3 whole-character final freeze / closure only  
**Author ruling:** FINAL WHOLE-CHARACTER PRODUCTION FREEZE APPROVED  
**Stop condition:** complete the record-only freeze closure, then STOP FOR CHATGPT REVIEW.

## 1. Author acceptance

Author / ChatGPT review accepts the final Halvren RP3 whole-character production references.

The following are APPROVED and are to be frozen as the final RP3 whole-character references:

- **HV_M_REF_RP3_v001** — c1 final production reference
- **HV_F_REF_RP3_v001** — c2 final production reference

Frozen composition:

- Body: **HB2**
- Face: **HF2**
- Pelvis: **HP-B**
- Central ear: **HE2 HVEAR3**
- Root: **HR2**
- Ear production triangulation: **TRI-HV1**
- Ear LOD rule: **LOD-HV1**

No geometry, topology, proportions, or subsystem design changes are authorized by this order.

## 2. Freeze source

Use the already-reviewed candidate state from:

- `reviews/claude-rac-rp3-halvren-final-whole-character-consolidation-report.md`
- `reviews/rac-rp3-evidence/halvren_rp3_final_whole/HALVREN_RP3_FREEZE_CANDIDATE.json`

Reviewed candidate commit:
- `e93f90cde863ebab31a5d5a588f8a1a9d357b94a`

This closure must be **freeze-by-record**.

Do not:
- rebuild;
- resave the blend files;
- alter embedded geometry;
- change sidecars;
- change ear diagonals;
- change LOD rules;
- change any accepted residual.

## 3. Promote candidate record to final freeze record

Create:

`reviews/rac-rp3-evidence/halvren_rp3_final_whole/HALVREN_RP3_FREEZE.json`

from the existing candidate record.

Final record state must read:

**HALVREN RP3 WHOLE CHARACTER — AUTHOR ACCEPTED / FINAL PRODUCTION FROZEN**

Preserve all candidate hashes exactly.

The record must include:
- c1 / c2 production file hashes;
- geometry hashes;
- face topology hashes;
- branch-map hashes;
- landmark hashes;
- TRI-HV1 sidecar hashes;
- frozen triangle hashes;
- source lineage;
- family realization hashes;
- body / face / pelvis / ear system identities;
- production contract;
- accepted residuals;
- immutable-reference verification;
- carry-forwards.

## 4. Production references remain byte-identical

Re-hash the existing production files at:

`E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Halvren/RP3/`

Required:
- no blend resave;
- no sidecar rewrite unless project convention requires a metadata-only file outside the frozen blend;
- geometry and topology unchanged;
- all 11 production files remain byte/array identical to the reviewed candidate state.

The freeze record is authoritative over any embedded `CANDIDATE ... NOT frozen` string, following the established Fenn / Aelari / Vael precedent.

## 5. Freeze the whole-character composition

Record as final:

### c1
- `HV_M_REF_RP3_v001`
- source: `HVC1-HB2HF2-HPB`
- body HB2
- face HF2
- pelvis HP-B
- HE2 HVEAR3 + HR2
- frozen TRI-HV1

### c2
- `HV_F_REF_RP3_v001`
- source: `HVF178-HB2HF2-HPB`
- body HB2
- face HF2
- pelvis HP-B
- HE2 HVEAR3 + HR2
- frozen TRI-HV1

No third central reference.

## 6. Preserve accepted residuals

Do not reopen or "fix" the following in this closure:

- frozen HE2 surface relief residuals;
- cuff / back-sheet crumple;
- HR2 lobe-base crease;
- residual folded / warped quads accepted under TRI-HV1;
- subtle hidden-ear read;
- MPFB expression-unit blink / surprise issues;
- HR2 root-zone anatomy-mask exception;
- normal 25 % LOD skin softening behind the root.

These are either previously accepted or carried to downstream rig / expression / engine integration.

## 7. Preserve production rules

The final whole-character freeze must explicitly carry:

### TRI-HV1
Mandatory baked ear triangulation.

Do not export ear quads for importer-side triangulation.

### LOD-HV1
Mandatory ear LOD protection.

### Ear normals / tangents
- smooth normals on baked triangles;
- MikkTSpace-compatible tangents;
- preserve/import, do not regenerate in a way that changes the frozen surface.

### Ear skinning
Ear branch effectively rigid to the head / skull at final skinning.

## 8. Carry-forwards

Preserve without modification:

### HALVREN-CF-EAR-TRI-LOD-1
At first UE5 integration:
- verify exact triangle count / topology;
- confirm no importer re-triangulation;
- verify normals / tangents;
- verify root seam;
- verify LOD-HV1 silhouettes.

### Ear-root skinning
Carry the same rigid-head binding requirement already documented for the frozen ear family.

### Expression-stage carry-forward
Keep the existing MPFB expression-unit lid-closure / expression-flip class as a rig / expression-stage issue, not a source-geometry blocker.

Do not invent new carry-forward IDs unless a real unrecorded issue is found during record verification.

## 9. Canon / status / handoff updates

Update:

- `specs/STATUS.md`
- `specs/halvren/HALVREN_V1.md`
- `reviews/claude-session-handoff.md`
- any final reference manifest / freeze index used by Fenn / Aelari / Vael convention

The new top status must state:

**HALVREN RP3 WHOLE CHARACTER — AUTHOR ACCEPTED / FINAL PRODUCTION FROZEN**

Also state:
- final references = `HV_M_REF_RP3_v001` and `HV_F_REF_RP3_v001`;
- final composition = HB2 + HF2 + HP-B + HE2 HVEAR3 / HR2;
- ear family already frozen;
- TRI-HV1 / LOD-HV1 remain mandatory;
- no geometry change in the closure.

Mark the previous "WHOLE-CHARACTER FINAL FREEZE RECOMMENDED" status as superseded by the final freeze.

## 10. Immutable references

Re-verify unchanged:

- Marchfolk production references;
- Fenn final references;
- Aelari final references;
- Vael final references;
- Halvren ear-family freeze record;
- HE2 + HR2 freeze record;
- TRI-HV1 baked ear files;
- HB2 / HF2 / HP-B accepted source records.

No frozen reference outside Halvren may change.

## 11. Final closure report

Return one concise closure report containing:

- final freeze record path;
- final c1 / c2 file hashes;
- final geometry hashes;
- TRI-HV1 hashes;
- confirmation that production files remained byte-identical;
- immutable-reference verification;
- canon / STATUS / handoff updates;
- carry-forwards retained;
- explicit final state:

**HALVREN RP3 WHOLE CHARACTER — AUTHOR ACCEPTED / FINAL PRODUCTION FROZEN**

## 12. STOP CONDITION

This is a record-only closure.

Do not:
- modify Halvren geometry;
- reopen HB2 / HF2 / HP-B;
- reopen HE1 / HE2 / HE3;
- reopen HR2;
- alter TRI-HV1 / LOD-HV1;
- begin UE5 integration;
- begin character creator implementation;
- begin hair / clothing / materials;
- begin another race.

Complete only the freeze record, production re-hash, canon/status/handoff updates, and closure report, then **STOP FOR CHATGPT REVIEW**.
