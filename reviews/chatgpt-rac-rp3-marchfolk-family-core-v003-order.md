# RAC RP3 — Marchfolk v003 shared family-core correction + acceptance gate order

**Date:** 2026-10-26  
**Authority:** Tyler / ChatGPT review of Claude Marchfolk RP3 return `5fd48e2e4c0b2d6c8ddfae6543bd1c9bbcdff9a2`.  
**Parent gate:** `reviews/claude-rac-rp3-marchfolk-production-baseline-gate.md`.  
**Program references:** `specs/RAC_PRODUCTION_MESH_CONTRACT.md`, `reviews/chatgpt-rac-retopology-rigprep-master-plan.md`.

The Marchfolk RP3 v002 candidate is accepted as the **correct architectural direction**, but it is **not yet frozen as the MPFB-family production base**.

This order authorizes exactly one bounded `v003` family-core correction cycle to remove the shared reusable defects before any family propagation.

Do not start Skarn or another race until this gate returns.

---

# 1. Immutable source / provenance firewall

Do not modify or overwrite:

- `MF-M-R` accepted source;
- `MF-F-R` accepted source;
- source build records;
- committed R-6 NPZ files;
- Marchfolk v001 and v002 production files;
- v002 mapping/provenance files;
- Grask / Gorrund assets;
- any other race.

Source references remain:

## Configuration 1
`MF-M-R`
- R-6 SHA-256: `2caaf056fff559c8c2c8b92dd5e2bc751be0c3efd9a98d0f8d4a7052f65be4d7`
- build SHA-256: `c5be9ca0805f8ac298181cb0da42070bc4a4843fc0aa15129d4d8ba5f686c9ee`

## Configuration 2
`MF-F-R`
- R-6 SHA-256: `c254fb4bc47225d90fcf7950514240cd74baace0ee3b48cd4d78fa38d9381761`
- build SHA-256: `252907fda37c791dd3f5d5b547dc28886a8feeb14c7b1a79719667d49089de6d`

Before and after work, re-verify hashes.

Stop on mismatch.

---

# 2. Author ruling on v002

Record:

- native hm08 is **not** accepted as the shared production base unchanged;
- Marchfolk v002 is the **accepted base architecture**;
- v002 density strategy is accepted:
  - one linear quad subdivision;
  - 98 closed leg rings;
  - deterministic hm08 map M;
  - shared topology across both Marchfolk configurations;
- v002 anatomy preservation is accepted as sufficient;
- v002 face/orbit/mouth readiness is accepted as sufficient;
- v002 diagnostic deformation does **not** demonstrate a topology-class failure.

The v003 cycle must therefore be **local and conservative**.

Do not redesign the v002 base.

---

# 3. Purpose of v003

Create a single shared MPFB-family core topology that:

1. keeps the v002 density and mapping strategy;
2. removes shared hand/foot/ankle crease poles;
3. fixes short MCP/root loop bands;
4. fixes the configuration-2 left shoulder loop shortfall;
5. materially reduces concentrated T-4 quad-quality misses in face/hands/feet;
6. preserves the accepted Marchfolk anatomy and shared topology across both configurations.

This correction is intended to become reusable across the MPFB-family races if accepted.

---

# 4. Required v003 topology corrections

## 4.1 Hand / palm / MCP junctions

Correct the shared hm08 pole organization around:

- index MCP roots;
- ring MCP roots;
- pinky MCP roots;
- thumb MCP / thenar transition;
- hypothenar / pinky root transition.

Requirements:

- no pole on the primary MCP crease;
- move shared junction poles at least 1–2 usable loops off the crease where practical;
- minimum loop targets:
  - finger MCP: >= 3 support loops;
  - thumb MCP: >= 3;
  - pinky MCP: >= 3;
- preserve digit spacing and palm silhouette;
- preserve hand proportions exactly within anatomy tolerances.

Add only the minimal thenar/hypothenar/root loops needed.

Do not increase hand density globally without justification.

---

## 4.2 Ankle crease

Correct the shared ankle/instep/heel pole currently sitting on the ankle crease.

Requirements:

- no crease-line pole;
- retain >= 3 ankle support loops;
- preserve heel, instep and malleolar silhouette from source;
- keep foot-ground contact unchanged.

---

## 4.3 Toe / MTP root junctions

Correct the shared forefoot fan topology at:

- MTP / j1 for toes 1–5;
- toe2 / toe3 j3;
- toe4 j2;
- any directly equivalent pole-induced IP failure seen in both configs.

Requirements:

- move junction poles off the active flexion crease;
- maintain >= 2 support loops per toe joint;
- preserve toe lengths, spacing, web shape and sole contact;
- no merged toes, no web thickening, no toe-tip drift.

Do not redesign the foot shape.

---

## 4.4 Configuration-2 left shoulder loop shortfall

The v002 configuration-2 left shoulder currently has only 4 of the required 5 loops under the audit.

Correct this in the **shared topology**, not by making config-2 topology unique.

Requirements:

- both configs must remain on identical topology / face list / vertex order;
- shoulder must audit >= 5 loops;
- no crease-line pole;
- preserve axillary fold and deltoid contour;
- do not alter GH position or source rig landmarks.

If a shared correction creates a problem on config 1, stop and report rather than branching topology.

---

# 5. T-4 quad-quality cleanup

The v002 architecture still has concentrated T-4 misses in face, hands and feet.

This v003 cycle should materially improve those outliers **without broad remeshing**.

Target:

- reduce total T-4 failure percentage materially versus v002;
- prioritize:
  - aspect > 4;
  - angles outside 45–135°;
  - crease-adjacent slivers;
  - badly skewed hand/foot/face transition quads.

Do not chase perfect global numbers at the cost of anatomy or clean flow.

No geometry may leave the accepted source envelope beyond T-1/T-2.

Every changed topology patch must have:
- before/after face-quality stats;
- changed-vertex / changed-face count;
- zone;
- reason.

---

# 6. Mapping / shared-family requirements

v003 must remain deterministic and reusable.

Provide:

- explicit v002 -> v003 mapping;
- hm08 -> v003 mapping;
- source weight transfer path;
- source UV transfer path;
- source morph/shape-key transfer path where technically applicable;
- common topology proof for both Marchfolk configurations.

Required:
- identical face topology hash across M/F;
- identical vertex count across M/F;
- identical face list across M/F;
- identical mapping structure across M/F.

Do not make configuration-specific topology.

---

# 7. Anatomy-preservation gates

For both configurations independently, rerun:

- T-1;
- T-2;
- T-3;
- T-7;
- stature;
- bbox;
- silhouette IoU;
- surface deviation;
- identity-zone deviation.

Also show identical-camera:

- front;
- rear;
- profiles;
- 3/4;
- head;
- hands;
- feet;
- shoulder;
- groin/pelvis.

Do not average the two configurations.

Each must preserve its own accepted source.

---

# 8. Loop audit — full §7 rerun

Rerun all 69 joint stations for both configurations.

Return:

- firm pass/fail;
- strict pass/fail;
- loop count;
- crease-pole status;
- nearest-pole distance.

The author goal for v003 is:

### Mandatory
- **0 firm failures** at:
  - shoulder;
  - elbow;
  - wrist;
  - MCP roots;
  - hip;
  - knee;
  - ankle;
  - toe joints;
  - neck.

### Preferred
- eliminate all firm failures across all 69 stations.

If a residual exists:
- identify exact station;
- show why fixing it would damage anatomy/topology;
- stop for ChatGPT decision.

Do not silently waive failures.

---

# 9. Creator-density audit

Rerun §8 for both configurations.

Every zone must continue to pass.

Do not allow local topology cleanup to make:
- face > 0.25%;
- ears > 0.25%;
- hands/feet > 0.3%;
- trunk/pelvis > 0.6%;
- limbs > 0.6%.

Also report:
- total verts/quads;
- per-zone mean edge;
- per-zone p95 edge;
- delta versus v002.

---

# 10. Face / UFCA readiness regression

Reconfirm:

- mouth rings;
- orbit rings;
- mouth-corner poles;
- eye-region poles;
- jaw/cheek flow;
- face density;
- open orbit/lip pocket behavior.

Do not reduce face readiness during T-4 cleanup.

The derived jaw-hinge estimate remains provisional for later face rigging.

Do not create final facial components.

---

# 11. Limited diagnostic deformation rerun

Use the same limited Marchfolk test suite and the same source rig/weights.

Compare:

- native;
- v002;
- v003.

Primary goal:
prove v003 topology cleanup does not create a new deformation-class failure.

Test at minimum:
- shoulder abd45 / abd90 / flex90;
- elbow 90 / 130;
- wrist flex/ext;
- fist;
- thumb opposition;
- hip flex90;
- knee 90 / deep flex;
- ankle dorsi;
- trunk twist;
- neck flex/rotation.

Classify every failure:
- topology;
- weights;
- joint placement;
- contact/setup.

Do not launch weight/corrective research.

---

# 12. Configuration-1 knee joint-placement flag

The v002 diagnostic flagged the configuration-1 knee centre as about 1.9 cm medial of the section centroid.

Do not silently alter the accepted source-rig landmark.

Perform a bounded **diagnostic comparison only**:

- source-rig knee centre;
- section-centroid-aligned candidate;
- deformation result at knee 90 / deep flex.

Return whether the source-rig knee placement is:
- mechanically acceptable;
- clearly inferior but still usable;
- implausible enough to require later rig-author review.

Do not update canonical landmarks in this order unless separately authorized.

---

# 13. Acceptance / family-base decision

At the end return exactly one:

## FAMILY BASE PASS — READY FOR AUTHOR FREEZE

Use only if:
- both configurations share identical v003 topology;
- all mandatory §7 stations pass;
- density passes;
- anatomy gates pass;
- face readiness passes;
- no topology-class deformation failure appears;
- T-4 is materially improved;
- mapping is complete.

or

## FAMILY BASE FAIL / NEEDS AUTHOR DECISION

Use if any mandatory item remains unresolved.

Do not propagate to other races before explicit author/ChatGPT freeze.

---

# 14. Production files

Suggested names:

- `MF_M_REF_RP3_retopo_v003.blend`
- `MF_F_REF_RP3_retopo_v003.blend`

Required sidecars:
- source hashes;
- parent v002 hashes;
- operations;
- changed topology zones;
- mapping hashes;
- topology counts;
- audit results;
- gate state.

Do not overwrite v001/v002.

---

# 15. Required evidence

Provide inspectable sheets for both configurations:

- full-body clay/wire;
- face/orbit/mouth;
- shoulder/axilla;
- elbow;
- hand/MCP closeups;
- ankle;
- foot/toe closeups;
- pole maps;
- counted loop rings;
- T-4 quality heatmaps;
- density heatmaps;
- source/v002/v003 overlays;
- deformation comparison sheet;
- knee-centre diagnostic comparison.

Also provide a family-core topology diagram showing exactly which local junctions changed between v002 and v003.

---

# 16. Required return

Commit:

1. `reviews/claude-rac-rp3-marchfolk-family-core-v003-gate.md`;
2. v003 production files / sidecars / manifest;
3. hm08->v003 and v002->v003 mapping files;
4. topology / pole / loop audit;
5. T-4 quality audit;
6. density audit;
7. anatomy-preservation audit;
8. face-readiness audit;
9. limited diagnostic deformation results;
10. config-1 knee placement comparison;
11. visual evidence;
12. before/after source and parent hashes;
13. reproducible tools/scripts;
14. narrow `specs/STATUS.md` update;
15. session handoff.

The gate must explicitly answer:

- Are both Marchfolk configs on identical v003 topology?
- Are all mandatory joint-loop stations passing?
- What firm/strict failures remain, if any?
- How much did T-4 improve?
- Are all density zones still passing?
- Did anatomy remain within tolerance?
- Did face/UFCA readiness remain intact?
- Did any new topology-class deformation failure appear?
- What is the result of the config-1 knee-centre comparison?
- Is v003 ready to freeze as the shared MPFB-family production base?

---

# 17. Stop rules

After committing the gate:

**STOP FOR CHATGPT REVIEW.**

Do not:
- freeze v003 without explicit author acceptance;
- start Skarn;
- start Sagekin;
- propagate topology family-wide;
- finalize production rig/weights;
- implement creator morphs;
- finalize UV/materials;
- generate LODs;
- integrate UE5.

---

## FINAL AUTHOR RULING

- Marchfolk v002 is accepted as the correct base architecture.
- One bounded v003 shared family-core correction is authorized.
- The purpose is to fix reusable MPFB-family defects once before propagation.
- No configuration-specific topology branching is authorized.
- No anatomy redesign is authorized.
- No other race begins until v003 returns for author review.
