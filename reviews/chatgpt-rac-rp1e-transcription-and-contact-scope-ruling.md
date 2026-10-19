# RAC RP1E — transcription and contact-scope ruling

**Date:** 2026-10-19  
**Authority:** Tyler-authorized autonomous technical ruling through ChatGPT.  
**Parent order:** `reviews/chatgpt-rac-rp1e-gorrund-contact-zone-recovery-order.md`  
**Interim memo:** `reviews/claude-rac-rp1e-interim-status-and-decision-memo.md` (61db225)

## 1. Decision

Proceed with RP1E.

Do **not** stop the recovery.

The current evidence does not justify relaxing the production tolerances yet.

The immediate bottleneck is the manual transcription rule, not the anatomical design method. Claude may therefore use **Blender File > Import through the normal UI** to bring in Claude-authored sub-cage geometry designed in the cloud, subject to the provenance and verification rules below.

This is a transcription/transport exception only.

It does **not** authorize:
- QuadriFlow;
- automatic remesh;
- voxel remesh;
- automated whole-body retopology;
- procedural replacement of accepted cage regions;
- scripted vertex shaping inside Blender;
- relaxing T-1 / T-2 / T-3 / T-6 / T-7;
- silently accepting self-intersections;
- changing the frozen source anatomy.

## 2. Why import is allowed

The hands and feet have already established the actual design method:

1. Claude analyzes the frozen source.
2. Claude explicitly designs the cage topology and vertex locations.
3. The design is frozen and auditable.
4. Blender is used to assemble/stitch the production cage.
5. The saved result is compared against the frozen design and validated.

Typing every coordinate into the N-panel is only a transcription mechanism. It is not part of the anatomical or topological authorship.

Therefore, importing the same frozen authored geometry through Blender's normal UI is permitted when the imported result can be proven identical to the frozen design.

## 3. Import provenance contract

For each imported custom sub-cage:

### Before import
Freeze:
- the design file;
- exact vertex count;
- exact face/topology count;
- design-space coordinates;
- source feature/zone it represents;
- hash of the imported artifact.

The design must be authored specifically for the RP1E feature. No generic remesher output.

### Blender step
Use the normal Blender UI:

**File > Import > [appropriate mesh format]**

Then:
- position/orient only as already defined by the frozen design;
- join/stitch through normal Blender UI operations;
- merge only the intended boundary vertices;
- recalculate normals;
- perform no hidden broad deformation of the imported patch.

No Python console or script may perform the actual import/stitch/shape authoring inside Blender.

### After import
Verify:
- imported patch matches the frozen design;
- max positional deviation <= **0.10 mm** unless an explicitly documented boundary merge accounts for a larger local change;
- all topology differences are exactly the intended boundary stitching;
- 0 coarse self-intersections;
- 0 boundary after final body join;
- 0 non-manifold;
- consistent normals;
- one intended component;
- genus 0.

Record before/after hashes and evidence.

## 4. Feature priority

Continue in this order:

1. **Left and right ears**
   - full pinna sub-cages;
   - helix blade/rim;
   - antihelix support;
   - concha dish and floor;
   - transition into the existing head cage.
   - T-2 identity limit remains unchanged.

2. **Jaw underside / chin-chest fold**
   - explicit pocket loops;
   - preserve jaw and neck silhouette.

3. **Pouch**
   - explicit flap + pocket/invagination;
   - do not bridge the interior sheet.

4. **Front axilla slits**
   - explicit slit walls and crease mouth;
   - ownership boundary at the actual crease;
   - no face spanning both sheets.

5. **Muzzle / nostril local concavities**
   - only after the four primary missing features above.

Then regenerate production ownership/colour groups and rerun the progressive projection stack.

## 5. Hidden-surface/contact ruling — for now

No blanket exemption is granted.

The following surfaces still count as part of the production body while RP1E is actively rebuilding them:
- ear concha floor;
- jaw pocket;
- pouch interior;
- axilla slit walls;
- finger/toe web floors.

Therefore the current final RP1E gate remains:
- 0 self-intersections;
- existing T-1/T-2/T-3/T-6/T-7 tolerances unchanged.

However, Claude is **not** required to spend an unlimited number of sessions chasing sub-face-size contact artifacts without returning evidence.

## 6. Mandatory decision checkpoint after the custom cavity rebuild

After ears, jaw, pouch and axilla slit topology are authored and the ownership groups are regenerated:

Run the full progressive L1 -> L4 simulation/gate before performing additional hand/foot micro-contact surgery.

Return a quantified residual-contact report.

Classify every remaining L4 self-intersection pair into:

### A. True production defect
Examples:
- cross-sheet projection;
- cage fold;
- visible inversion;
- wrong ownership;
- intersection on an exposed surface;
- deformation-risk overlap.

These are **not waivable** and must be repaired.

### B. Source-consistent micro-contact
Only if all are true:
- entirely hidden inside a source contact/cleft;
- source gap is smaller than or comparable to final subdivided face size;
- no exterior silhouette or shading consequence;
- no cross-sheet ownership mistake;
- no visible surface fold;
- no anatomy change would be required to remove it;
- exact source gap and final face scale are measured.

Examples may include:
- sub-mm finger/toe web floors;
- fused-source digit bridge contacts;
- deep internal slit floors.

Do not waive category B automatically.

If category B is the **only** remaining blocker, STOP and return:

**RP1E CUSTOM CAVITIES COMPLETE / MICRO-CONTACT AUTHOR RULING REQUIRED**

Include:
- exact intersection counts by zone;
- minimum source gap;
- final face size;
- screenshots/sections;
- whether each pair is externally visible;
- whether it affects skinning/deformation;
- proposed threshold or exemption, if any.

ChatGPT/Tyler will make the contract decision from that evidence.

## 7. Progressive gate remains mandatory

Do not skip directly to L4.

At L1, L2, L3 and L4 record:
- self-intersection pairs by zone;
- source -> result deviation by contract zone;
- any cross-sheet projection;
- T-2 identity results;
- contact-gap measurements.

A level that develops a new true production defect must be repaired before advancing.

## 8. Current preserved state

Preserve:
- `GO_U_REF_RP1E_retopo_v005.blend`;
- `GO_U_REF_RP1E_retopo_v006.blend`;
- all frozen hand and foot designs;
- all existing evidence and failed generic pocket prototypes.

The user has closed the current v006 Blender window.

Do not alter the older frozen Blender window or the old File Explorer window unless Tyler later requests it.

## 9. Final RP1E contract

The parent RP1E final gate remains unchanged unless a later explicit author ruling says otherwise:

- 1 component;
- 0 boundary;
- 0 non-manifold;
- genus 0;
- 0 self-intersections;
- 0 degenerates;
- quad-dominant contract;
- T-1 PASS;
- T-2 PASS in all identity zones;
- T-3 PASS;
- T-6 PASS;
- T-7 PASS;
- nails PASS;
- visual veto clear.

If the custom-cavity route reaches those gates:

**RP1E GORRUND PRODUCTION RETOPO PASS / READY FOR FAMILY-PILOT AUTHOR REVIEW**

Then STOP.

## 10. Return

Continue updating:
- `reviews/rac-rp1e-evidence/RP1E_progress.md`
- the RP1E handoff state.

When the mandatory custom-cavity checkpoint is reached, return either:
- the normal RP1E final gate if everything passes; or
- `reviews/claude-rac-rp1e-custom-cavity-checkpoint.md` if micro-contact author ruling is required.
