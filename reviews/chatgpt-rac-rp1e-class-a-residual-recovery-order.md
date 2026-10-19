# RAC RP1E — Class-A residual recovery after custom-cavity checkpoint

**Date:** 2026-10-19  
**Authority:** Tyler-authorized autonomous continuation through ChatGPT.  
**Parent ruling:** `reviews/chatgpt-rac-rp1e-transcription-and-contact-scope-ruling.md` (3816926).  
**Checkpoint:** `reviews/claude-rac-rp1e-custom-cavity-checkpoint.md` (03cdfe5).

## 1. Ruling

Continue RP1E.

The custom-cavity checkpoint is **interim**, not a stop condition, because definite Class-A production defects remain.

Do **not** grant or assume any Class-B waiver in this order.

The objective of this order is to eliminate or materially reduce the remaining **Class-A** defects while preserving the current production contract.

## 2. Current source state

### PC cage
The last UI-verified imported cage is:

`GO_U_REF_RP1E_retopo_v009.blend`

Recorded state:
- design v009;
- 3013 V / 3113 F;
- 0 boundary;
- 0 non-manifold;
- genus 0;
- 1 component;
- consistent normals;
- 0 coarse self-intersections;
- imported-vs-design max deviation 0.00025 mm.

Preserve it unchanged.

### Current cloud design
The current cloud design is:

`reviews/rac-rp1e-evidence/designs/design_v010c.npz`

with:
- 3037 V / 3118 F;
- rebuilt axilla trunk rings;
- current regional smoothing group `fsm_v3.txt`.

v010c is not yet the authoritative PC cage until it passes the normal UI-import provenance verification.

## 3. First action

Import v010c into Blender through the normal UI under the already-authorized transcription exception.

Create a new versioned PC file. Do not overwrite v009.

Verify:
- design/import vertex correspondence;
- max deviation <= 0.10 mm;
- intended topology identical;
- 0 boundary;
- 0 non-manifold;
- genus 0;
- 1 component;
- consistent normals;
- 0 coarse self-intersections.

If v010c cannot pass the import/provenance gate, STOP and report before doing further design work.

## 4. Class-A repair priority

Proceed in this order.

### A1. Hands — explicit web-floor creases

The frozen hand sub-cages currently start their digit tubes above several source cleft floors and bridge the inter-digit webs.

For every Class-A hand cleft:

Author an explicit **lip / floor / lip** web-floor crease analogous to the successful groin-crease topology.

Required:
- follow the actual source cleft floor;
- preserve the existing palm/digit proportions;
- no bridge across visible cleft space;
- no new hand self-intersections in the coarse cage;
- preserve nail-bearing distal surfaces;
- preserve five-digit anatomy;
- do not separate a truly fused source surface merely to satisfy topology.

Special case:
- the known R fused-digit region remains a Class-B candidate unless the new web-floor topology naturally resolves it.
- Do not distort the fused source anatomy to force separation.

### A2. Feet — explicit toe-cleft web floors

The current foot sub-cages improved the toes substantially but still bridge several cleft floors.

For every Class-A toe cleft:
- add explicit lip / floor / lip topology;
- preserve the four free source toes and the fused fifth-toe anatomy;
- preserve the established shin -> foot -> toe cage design;
- preserve nail-bearing distal surfaces;
- do not alter the accepted foot silhouette merely to clear a hidden contact.

The specific R foot cleft cluster around approximately (-33.8, -43.4, 2.2) cm is a mandatory Class-A repair target.

### A3. Left axilla Class-A pockets

Repair:
- the exposed/bridged L axilla pinch around approximately (23.5, -41.4, 146.7) cm;
- the narrow sub-pocket near z ~153 cm;
- any remaining Class-A slit-tip miss where source gap exceeds final face size.

Do not treat the enclosed zero-gap void behind the pinch as waived Class B in this order.

If the visible/exposed Class-A surface can be corrected while the inaccessible zero-gap interior remains, leave the interior for the later author ruling.

### A4. Head / muzzle Class-A residuals

Add explicit local topology where needed for:
- nostril slits;
- philtrum slot residual;
- chin underside;
- any remaining exposed ear fold;
- mouth/crease residual if still above T-2.

Do not broadly resculpt or re-author the accepted muzzle identity.

### A5. Pelvis / posterior small Class-A residuals

Repair:
- natal-cleft top;
- R groin crease end;
- perineum micro-folds that are true cage/product folds rather than pure source-contact artifacts.

Do not alter the accepted tail-root anatomy.

## 5. Design/import method

Cloud-designed custom patches remain allowed under the transcription ruling.

For every design revision:
1. freeze the cloud design artifact;
2. record vertex/face counts and hash;
3. import through Blender File > Import;
4. save to a **new versioned .blend**;
5. verify design/import identity and topology;
6. preserve all prior PC versions unchanged.

Do not reintroduce manual N-panel transcription except for tiny local edits where it is genuinely faster.

## 6. Coarse-cage gate

Every new imported production cage must pass before projection:

- 1 component;
- 0 boundary;
- 0 non-manifold;
- genus 0;
- 0 coarse self-intersections;
- consistent normals;
- no face bridging a visible opposed source sheet;
- no unintended cage fold.

If the coarse cage fails, repair at coarse resolution before running subdivision.

## 7. Progressive projection gate

After the Class-A repair design is complete, rerun L1 -> L4 progressively.

At each level record:
- total self-intersection pairs;
- pairs by zone;
- source -> product deviation by T-1/T-2 zones;
- exposed vs hidden clusters;
- source opposed-sheet gap;
- final face edge scale;
- intersection amplitude;
- any cross-sheet ownership/projection errors.

True Class-A defects must not be allowed to accumulate upward merely because they are small at L1.

## 8. Class-B candidates remain provisional

Do not waive any of these yet:
- R toe-web floor contact;
- R axilla apex crushed contact;
- R axilla slit contacts;
- L axilla hidden slit-floor contact;
- R fused-digit contact;
- any other source-consistent micro-contact.

A proposed B pair still requires the later author ruling.

If a Class-A repair naturally eliminates a B candidate, that is acceptable and preferred.

Do not intentionally worsen B candidates.

## 9. Required checkpoint after this order

When the Class-A recovery has been completed as far as technically credible, classify every remaining L4 pair again.

### If any definite Class-A defects remain
Continue local repair if:
- the anatomy can be preserved;
- the repair is bounded;
- there is a clear topology solution.

If further Class-A repair would require changing source anatomy, stop with:

**RP1E CLASS-A RECOVERY BLOCKED / AUTHOR DECISION REQUIRED**

and provide exact evidence.

### If only Class-B candidates remain
STOP and return:

**RP1E CLASS-A CLEAR / MICRO-CONTACT AUTHOR RULING REQUIRED**

This is the desired next decision checkpoint.

Do not silently apply the proposed threshold from the interim memo.

### If all final gates pass with 0 self-intersections
Return the normal parent-order result:

**RP1E GORRUND PRODUCTION RETOPO PASS / READY FOR FAMILY-PILOT AUTHOR REVIEW**

Then STOP.

## 10. Final contract remains unchanged

Until a later explicit author ruling:

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
- all nails PASS;
- visual veto clear.

No RP2, rigging, creator implementation or UE5.

## 11. Evidence and return

Continue updating:
- `reviews/rac-rp1e-evidence/RP1E_progress.md`
- `reviews/claude-session-handoff.md`

Return the next decision report as:

`reviews/claude-rac-rp1e-class-a-recovery-gate.md`

Evidence remains under:

`reviews/rac-rp1e-evidence/`
