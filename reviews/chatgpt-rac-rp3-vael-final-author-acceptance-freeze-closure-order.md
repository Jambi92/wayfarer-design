# RAC RP3 — Vael final author acceptance / carry-forward registration / freeze-by-record closure order

**Date:** 2026-10-29  
**Authority:** Tyler / ChatGPT review of Claude final consolidation return `4df3e0c4bcff77cb6e0e2b77299f9304d23ebb74`.  
**Parent order:** `reviews/chatgpt-rac-rp3-vael-final-consolidation-freeze-order.md`.  
**Parent report:** `reviews/claude-rac-rp3-vael-final-freeze-report.md`.  
**Freeze candidate:** `reviews/rac-rp3-evidence/vael_rp3_final/VAEL_RP3_FREEZE_CANDIDATE.json`.

This order resolves the only remaining author decision in Vael RP3.

The Vael body, face, ear geometry, ear topology and production blends are accepted.

Do not rebuild, relax, resculpt, retopologize or resave the final Vael production meshes.

---

# 1. AUTHOR RULING — ACCEPT THE c1 neck_rot45 EAR-CUFF FOLD AS A RIG/WEIGHT CARRY-FORWARD

The final consolidation found one new Standard-v1 deformation residual:

### Configuration
Vael c1 / `VA_M_REF_RP3_v001`

### Pose
`neck_rot45`

### Location
Left ear cuff, lobe-to-cheek junction.

### Observed effect
- one new fold pair;
- faces 57125 / 57126;
- no flipped faces;
- no self-intersection/contact;
- no root inversion;
- configuration 2 clean;
- right ear clean;
- every other Standard-v1 pose equals the accepted family behavior.

### Cell scale
Affected cuff edges are sub-millimeter to ~1.6 mm.

### Rest/pose dihedral
- rest ~112°;
- pose ~155°;
- crosses the 120° diagnostic fold threshold.

This residual is **accepted as non-blocking**.

---

# 2. ROOT CAUSE — WEIGHTING, NOT GEOMETRY

Accept Claude's diagnostic classification.

Affected ear-root/cuff vertices carry approximately:

- 98.4–99.0 % `head`;
- 1.0–1.6 % `neck_01`.

That tiny neck-weight tail shears the small cuff quads under plain LBS during c1 neck rotation.

Diagnostic evidence:

> When the ear branch is bound 100 % to the head bone, all 18 Standard-v1 poses become identical to the VF2 family realization in folds / flips / contacts.

Therefore:

**RI3 geometry is not implicated.**  
**VAEL_EAR_BRANCH_TOPOLOGY_v002 is not implicated.**  
**The source body is not implicated.**

The owning stage is final production skin weighting / rigging.

---

# 3. REGISTER NEW CARRY-FORWARD

Add the following item to:

`specs/RAC_PRODUCTION_RIG_CARRY_FORWARD_REGISTER.md`

## VAEL-CF-EARROOT-1

### Configuration
Vael configuration 1, final RP3 production body:
`VA_M_REF_RP3_v001`

### Item
At Standard-v1 `neck_rot45`, two very small left ear-cuff quads at the lobe/root junction cross the fold diagnostic threshold under carried MPFB weights.

### Measured state
- fold pair: faces 57125 / 57126;
- rest dihedral ~112°;
- posed dihedral ~155°;
- edge lengths ~0.14–1.56 mm;
- 0 flips;
- 0 self-intersections/contacts;
- 0 root inversions;
- c2 clean;
- all dedicated ear-readiness poses remain 0 / 0 / 0.

### Cause
The affected vertices inherit a ~1.0–1.6 % `neck_01` weight tail instead of behaving rigidly with the skull.

### Diagnostic proof
With the ear branch bound 100 % to `head`, all 18 Standard-v1 poses equal the family realization.

### Classification / owner
**RIG / WEIGHT / EAR-ROOT CORRECTIVE CARRY-FORWARD**

Production-rig / skin-weighting stage.

### Required production action
At final skinning:
- bind the Vael external-ear branch effectively rigidly to the head/skull;
- remove the inherited neck-weight tail from the external ear/root cuff as appropriate;
- revalidate neck rotation;
- preserve the accepted RI3 root/concha geometry.

This is not a source or topology blocker.

### Evidence
- `reviews/rac-rp3-evidence/vael_rp3_final/sheets/VA_FINAL_18b_c1_neck_rot45_fold.jpg`
- `reviews/rac-rp3-evidence/vael_rp3_final/diagnostics/deform_VAL4-R1-VD2-VF2_rigid_head_ear_weights.json`
- `reviews/claude-rac-rp3-vael-final-freeze-report.md`

---

# 4. EXISTING CARRY-FORWARD REMAINS

Preserve unchanged:

## VAEL-CF-SHOULDER-1
Configuration 1 shoulder flex 90°:
- 19 flips vs Marchfolk v005 13;
- +6;
- rig/weight/shoulder-corrective stage.

Do not reopen VF2 anatomy or topology for it.

The final Vael freeze must therefore carry:

- `VAEL-CF-SHOULDER-1`
- `VAEL-CF-EARROOT-1`

---

# 5. FINAL ACCEPTANCE OF THE PRODUCTION MESHES

Accept the already-written final production blends exactly as they are:

## Configuration 1
`VA_M_REF_RP3_v001.blend`

SHA-256:
`42f0cebbf9588bb9acc7fd7746ff804f84fa104cf2d672285372375af2de855b`

Geometry hash:
`887c93176058ddc007de28f3cfab47a50cc409c969ab9cfb2be4f5d68e410719`

## Configuration 2
`VA_F_REF_RP3_v001.blend`

SHA-256:
`516b18e8933a2d33f62cf51472408d9588af2c23179ff7b2f5119775dd75bc3a`

Use the already-recorded geometry hash from the freeze candidate.

Both:
- 59,076 vertices;
- 59,074 quads;
- 100 % quads;
- face-topology hash:
  `f8367ab09385d218559b6d3cac52ed159a9249cf12d91807e93e3b095d9ac297`.

Do not modify them.

---

# 6. PROMOTE THE FREEZE CANDIDATE — NO REBUILD

The current:

`VAEL_RP3_FREEZE_CANDIDATE.json`

already contains the completed validated state.

Promote it to:

`VAEL_RP3_FREEZE.json`

with only the minimum record/status edits required to reflect final author acceptance.

Do **not**:
- rebuild either production blend;
- rerun geometry generation to create a "final" version;
- resave either blend;
- change vertex positions;
- change faces;
- change branch maps;
- change RI3;
- change VF2;
- change VC2.

The freeze must remain a **freeze-by-record**.

---

# 7. FREEZE RECORD CHANGES

The authoritative `VAEL_RP3_FREEZE.json` must record:

## Final status
**VAEL RP3 FINAL PASS — AUTHOR ACCEPTED / FROZEN**

## Carry-forwards
- VAEL-CF-SHOULDER-1
- VAEL-CF-EARROOT-1

## Accepted residuals
Retain:
- c1 normalized free-ear stand-off secondary residual;
- expected unmasked source-vs-new-ear anatomy divergence;
- placeholder UV state on branch faces.

Add:
- c1 neck_rot45 ear-cuff fold classified as `VAEL-CF-EARROOT-1`, rig/weight stage, non-topology-blocking.

## Validation state
Preserve the existing validated results:
- 69 / 69 D1–D6 both;
- integrity PASS;
- T-1/T-2/T-3/T-7 ear-excluded PASS;
- human firewall PASS;
- three-elf firewall PASS;
- body canon 20 / 20;
- pelvis 9 / 9;
- face systems 6 / 6;
- elf face rows 9 / 9;
- RI3 ear gate PASS;
- root/concha visual gate PASS;
- density PASS;
- ear readiness PASS;
- probes 12 / 12;
- read-back PASS.

---

# 8. FREEZE RECORD / READ-BACK INTEGRITY

Because the production files have already been written and read back successfully:

- preserve the recorded file SHA-256 values;
- preserve geometry hashes;
- preserve face hash;
- preserve branch-map hashes;
- preserve landmark / sidecar hashes;
- preserve PC read-back results.

You may re-run **verification-only** scripts if needed to confirm nothing changed.

Do not resave the blends.

The authoritative freeze record must state that final acceptance was achieved through record promotion after author acceptance of `VAEL-CF-EARROOT-1`.

---

# 9. MANIFEST / SPEC / STATUS FINALIZATION

After the authoritative freeze record is written:

update:

- `reviews/reference-assets/manifest.json`
- `specs/vael/VAEL_V1.md`
- `specs/STATUS.md`
- `specs/RAC_PRODUCTION_RIG_CARRY_FORWARD_REGISTER.md`
- `reviews/claude-session-handoff.md`

Required status:

> **Vael RP3 — AUTHOR ACCEPTED / FROZEN**

Lineage:

### c1
VAL4 → R1 / VC2 → VD2 / VDF1.2 → VF2 / VEF1 → `VA_M_REF_RP3_v001`

### c2
VALF178 → R1 / VC2 → VD2 / VDF1.2 → VF2 / VEF1 → `VA_F_REF_RP3_v001`

### ear
VA-E2 → RI3 → `VAEL_EAR_BRANCH_TOPOLOGY_v002`

No universal elf topology declaration.

---

# 10. FINAL VAEL FREEZE REPORT

Update/finalize:

`reviews/claude-rac-rp3-vael-final-freeze-report.md`

The final report must state clearly:

- the prior author-decision status is resolved;
- no geometry/topology rebuild was performed;
- production blends remain byte-identical;
- `VAEL-CF-EARROOT-1` is registered;
- final status is frozen;
- both final carry-forward items are owned by production rigging;
- Halvren is next but not started.

---

# 11. REQUIRED RESULT

Return exactly:

## VAEL RP3 FINAL PASS — AUTHOR ACCEPTED / FROZEN

provided the record promotion and verification succeed.

A FAIL is only appropriate if:
- an existing file/hash unexpectedly changed;
- the candidate record cannot be promoted without inconsistency;
- read-back no longer matches.

No new geometry judgment is required.

---

# 12. NEXT RACE

After successful Vael freeze:

recommend:

**Halvren**

Do not start it.

The handoff must preserve:

- Fenn frozen;
- Aelari frozen;
- Vael frozen;
- three distinct elven population references now available;
- Halvren mixed ancestry must not be a numeric or visual average of them;
- shared engineering may be tested, but Halvren anatomy needs its own author gate.

---

# 13. STOP RULES

After committing the final Vael freeze closure:

**STOP FOR CHATGPT REVIEW.**

Do not:
- start Halvren;
- edit Vael geometry/topology;
- edit frozen Fenn or Aelari;
- edit active MPFB Family Base v005;
- invent low-light physiology;
- implement production ear rigging yet;
- implement creator morphs;
- finalize UV/materials;
- generate LODs;
- integrate UE5.

---

## FINAL AUTHOR RULING

- Accept the c1 `neck_rot45` cuff fold as a weighting issue.
- Register `VAEL-CF-EARROOT-1`.
- Preserve `VAEL-CF-SHOULDER-1`.
- Do not reopen RI3.
- Do not modify the final Vael production blends.
- Promote the validated freeze candidate to the authoritative freeze record.
- Freeze Vael RP3 by record.
- Stop before Halvren.
