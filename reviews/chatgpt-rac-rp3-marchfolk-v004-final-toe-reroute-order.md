# RAC RP3 — Marchfolk v004 final toe-IP pole-reroute / family-base freeze-candidate order

**Date:** 2026-10-26  
**Authority:** Tyler / ChatGPT review of Claude Marchfolk v003 gate `29321e2b0bef76e0b6bf9af9bb72b1c48b88ec8d`.  
**Parent gate:** `reviews/claude-rac-rp3-marchfolk-family-core-v003-gate.md`.  
**Program references:** `specs/RAC_PRODUCTION_MESH_CONTRACT.md`, RP3 Marchfolk baseline + v003 family-core work.

This is the **final bounded family-core correction cycle** before author freeze.

The v003 architecture is accepted as the correct shared MPFB-family core. This order resolves D1 and authorizes exactly one narrow D2 correction attempt.

No broader retopology work is authorized.

---

# 1. Immutable parents / firewall

Do not modify or overwrite:

- accepted Marchfolk R-6 sources;
- source build records;
- v001 production files;
- v002 production files;
- v003 production files;
- mapping/provenance packages;
- Grask / Gorrund assets;
- any other race.

The following v003 assets remain immutable parents:

- `MF_M_REF_RP3_retopo_v003.blend`
- `MF_F_REF_RP3_retopo_v003.blend`

Both source configurations and all prior files must hash identically before/after.

Stop immediately on mismatch.

---

# 2. AUTHOR DECISION D1 — ACCEPTED

## 2.1 Thumb MCP

Accept the thumb-MCP stations as **PASS** using the literal closed-ring criterion when the band-ray method is geometrically undefined.

Reason:
- band-ray exit is undefined on all relevant sides because the MCP sits within the thenar mass;
- literal closed rings exist around the thumb axis:
  - config 1: 3 rings;
  - config 2: 4 rings;
- required minimum is satisfied;
- forcing additional loops into the short axial span would create unjustified over-density / T-4 degradation.

### Standardize validator behavior

Update the audit logic so that:

1. use the normal band method when a valid outward-facing exit exists;
2. if the band-ray endpoint is undefined, do **not** use tie-order as a geometry verdict;
3. fall back to a documented closed-ring test using a radius appropriate to the anatomical segment;
4. report that fallback explicitly.

Do not modify thumb geometry for this issue.

---

## 2.2 Configuration-2 shoulders

Accept the config-2 shoulder stations as **PASS** where the band-ray side is undefined but the geometry/loop structure is otherwise valid.

Reason:
- one failing side is undefined;
- the right shoulder geometry is bit-identical to v002 while the reported count changed only due to invalid-candidate tie order;
- other sides carry adequate loop support;
- modifying valid shoulder geometry solely to satisfy an undefined ray result is prohibited.

Apply the same validator fallback principle as above.

Do not modify shoulder geometry.

---

# 3. AUTHOR DECISION D2 — ONE FINAL TOE-TUBE POLE REROUTE AUTHORIZED

Target only these residual crease poles:

### Both configurations
- toe3 j3 left
- toe3 j3 right

### Configuration 2 only
- toe4 j2 left
- toe4 j2 right

No other station may be changed unless required as a directly adjacent topological transition and explicitly reported.

---

# 4. Correction type

The prior **vertex-relocation** approach is exhausted and rejected because it created new self-intersections in the tightly packed toe/web anatomy.

This order authorizes a **topological pole reroute only**.

Allowed:
- edge-flow rerouting inside the local toe tube;
- local split/merge of quad flow;
- moving the valence transition away from the active flexion crease;
- adding/removing the minimum local support quads required to keep clean quad flow.

Not allowed:
- separating toes;
- widening web spaces;
- moving toe tips;
- changing toe lengths;
- changing toe spacing;
- changing sole contact;
- changing source silhouette;
- changing anatomy to make room for topology;
- global foot remesh;
- broad density increase;
- triangles/ngons in the deformation crease;
- configuration-specific final topology.

---

# 5. Shared-topology requirement

The final v004 topology must remain **identical for both Marchfolk configurations**.

If a reroute is only required anatomically on configuration 2, the topological pattern must still exist identically in configuration 1, with geometry fitted to its own source.

Required:
- identical vertex count;
- identical quad count;
- identical face list;
- identical topology hash;
- identical mapping structure;
- same local reroute pattern on both configurations.

Do not create topology branching between M/F.

---

# 6. Local topology requirements

For each corrected toe-IP station:

- crease pole count = 0;
- minimum support loops = 2;
- no new pole on the immediate flexion crease;
- preferably pole >= 1–2 usable loops away from the active crease;
- maintain clean longitudinal toe flow;
- no isolated valence spike directly in the web;
- preserve toe web continuity;
- preserve toe-pad and nail-region flow.

Keep the correction as small as practical.

Return changed:
- vertices;
- faces;
- poles;
- local valence map.

---

# 7. Contact / self-intersection hard gate

This is the decisive technical constraint.

The v004 reroute must introduce:

- **0 new self-intersection pairs** in the foot/toe region relative to v003;
- no new inter-toe penetration;
- no new web penetration;
- no new sole overlap;
- no new contact artifact.

Existing accepted source-contact pairs may remain but must not increase.

If every plausible reroute introduces new self-intersections, STOP and return FAIL. Do not solve it by changing anatomy.

---

# 8. Anatomy preservation

For both configurations rerun local + global preservation.

Mandatory:
- T-1;
- T-2;
- T-3;
- T-7;
- stature;
- bbox;
- silhouette;
- hand/foot identity zones;
- local foot/toe source deviation.

Toe-specific:
- toe lengths;
- toe-tip positions;
- MTP positions;
- IP positions;
- web boundaries;
- sole contact;
- forefoot width.

No meaningful anatomy drift is allowed.

---

# 9. T-4 quality

The toe reroute must not materially worsen v003 T-4 quality.

Required:
- global v004 T-4 union failure % <= v003 + 0.1 percentage point;
- local corrected toe patches should improve or remain comparable;
- no new severe aspect/angle outlier created by the reroute.

Report v003 -> v004:
- total violations;
- angle violations;
- aspect violations;
- local foot violations.

Do not reopen unrelated face/hand T-4 cleanup.

---

# 10. Loop audit / validator rerun

Rerun all 69 stations for both configurations using the standardized D1 fallback logic.

Required freeze result:

### Mandatory
- 0 **real** firm failures at all required deformation stations.

### Measurement fallback
Stations using the D1 fallback must be reported separately as:
- `PASS_FALLBACK_CLOSED_RING`
or equivalent.

Do not mix measurement-undefined fallback cases with true topology failures.

If a toe station still has a real crease pole after the one reroute attempt, report it as the final documented exception candidate.

---

# 11. Density / face readiness / mapping

Reconfirm:
- all 9 density zones pass;
- face/UFCA readiness unchanged;
- mouth/orbit rings unchanged;
- jaw/cheek flow unchanged;
- UV transfer remains valid;
- weight transfer remains valid;
- hm08 -> v004 map valid;
- v003 -> v004 map valid;
- both configurations share identical topology.

No facial or shoulder edits are authorized.

---

# 12. Limited deformation regression

Rerun only the affected / verification set plus a compact family sanity set:

Required toe/foot:
- ankle dorsiflexion;
- toe flexion/extension diagnostic if available;
- foot-ground contact sanity.

Plus sanity:
- shoulder abd90;
- elbow 90;
- fist;
- hip flex90;
- knee 90.

Purpose:
prove the local toe reroute did not introduce a new topology-class failure.

Do not start a corrective-weight cycle.

---

# 13. Acceptance logic

Return exactly one:

## FAMILY BASE PASS — READY FOR AUTHOR FREEZE

Use if:
- D1 fallback validator is implemented and documented;
- toe-IP crease poles are removed cleanly;
- 0 new foot/toe self-intersections;
- identical topology across both configs;
- anatomy gates pass;
- density passes;
- face readiness passes;
- mapping passes;
- no topology-class deformation regression;
- T-4 does not materially regress.

### OR

## FAMILY BASE PASS WITH DOCUMENTED TOE-IP EXCEPTION — READY FOR AUTHOR DECISION

Use if:
- every bounded reroute attempt demonstrably causes contact/self-intersection or other unacceptable damage;
- v003 remains otherwise valid;
- D1 is accepted;
- the remaining toe pole(s) are clearly documented as unavoidable contact-zone topology exceptions.

Do not continue iterating.

### OR

## FAMILY BASE FAIL

Use only if a new blocking problem appears beyond the known toe-IP issue.

---

# 14. Production files

If a valid v004 candidate is produced:

- `MF_M_REF_RP3_retopo_v004.blend`
- `MF_F_REF_RP3_retopo_v004.blend`

Do not overwrite v003.

Provide:
- sidecars;
- common topology manifest;
- maps;
- hashes;
- change log;
- local toe-reroute provenance.

---

# 15. Required visuals

Provide actual inspectable sheets:

1. v003 wire vs v004 wire — toe3/toe4 dorsal;
2. same — plantar;
3. pole/valence visualization;
4. crease-ring visualization;
5. web/contact closeups;
6. local source-deviation heat;
7. T-4 before/after foot heatmap;
8. foot/toe deformation sanity;
9. whole-body confirmation;
10. family-core final topology summary sheet.

Do not return a gate without the visual evidence.

---

# 16. Required return

Commit:

1. `reviews/claude-rac-rp3-marchfolk-v004-final-family-core-gate.md`;
2. v004 files if produced;
3. D1 validator/fallback update;
4. toe-reroute configs/tools;
5. topology/valence/pole audit;
6. full 69-station audit;
7. self-intersection/contact audit;
8. anatomy-preservation audit;
9. density audit;
10. T-4 audit;
11. mapping proof;
12. deformation sanity;
13. visual sheets;
14. source/v003 before-after hashes;
15. narrow `specs/STATUS.md` update;
16. session handoff.

The gate must explicitly answer:

- Did D1 fallback stations pass?
- Were the toe-IP poles successfully rerouted?
- Were any new self-intersections introduced?
- Are both configs on identical v004 topology?
- Are all true mandatory stations now passing?
- What fallback-pass stations remain?
- What T-4 change occurred?
- Did anatomy remain within tolerance?
- Did density remain valid?
- Did face readiness remain valid?
- Did any new topology-class deformation failure appear?
- Is the family base ready for freeze?
- If the toe reroute failed, is v003 ready to freeze with a documented exception?

---

# 17. Stop rules

After committing the gate:

**STOP FOR CHATGPT REVIEW.**

Do not:
- freeze v004/v003 without explicit author acceptance;
- start Skarn;
- start Sagekin;
- propagate family topology;
- finalize rig/weights;
- implement morphs;
- finalize UV/materials;
- generate LODs;
- integrate UE5.

---

## FINAL AUTHOR RULING

- D1 is accepted: thumb MCP + configuration-2 shoulder undefined band-ray cases use documented closed-ring fallback and are treated as PASS when the fallback passes.
- One final, narrow toe-IP **topological pole-reroute** attempt is authorized.
- No toe separation or anatomy change is authorized.
- No other Marchfolk topology region may be reopened.
- If the reroute succeeds, return v004 for freeze.
- If the reroute fails because of contact/self-intersection, stop and return v003 as the freeze candidate with the residual toe-IP pole documented.
