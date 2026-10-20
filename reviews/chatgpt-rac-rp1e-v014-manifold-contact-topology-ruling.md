# RAC RP1E — v014 manifold-contact topology, visible-handle, T-6, and nail recovery ruling

**Date:** 2026-10-20  
**Authority:** Tyler-authorized autonomous technical ruling through ChatGPT.  
**Parent:** `reviews/chatgpt-rac-rp1e-v014-local-stack-and-contract-ruling.md` (2995ef4).  
**Returned gate:** `reviews/claude-rac-rp1e-v014-local-stack-recovery-gate.md` (51599e8).

## 1. Ruling

Continue RP1E from v013.

The normal-sign per-sheet projection pilot is closed. Do not repeat it.

No v014 cage was promoted, so the next promoted production candidate may still use the v014 name.

The next route is a **manifold-contact topology solution**:

- visible source openings/handles must be preserved as visible production topology;
- hidden source handles may be omitted from the production surface;
- two production sheets must never overlap merely because the source gap tapers to zero;
- where two visible source sheets actually meet, the production topology must terminate them into a **shared manifold rim/crease edge**.

The zero-production-self-intersection requirement remains unchanged.

## 2. Revised genus ruling — preserve the visible R-hand handle

The prior genus-0-only interpretation is amended based on the new localisation evidence in 51599e8.

The source genus-3 handles are now classified:

1. **R hand B–C through-slit:** externally visible 3 mm through-opening from crotch to fused block.
2. **L hand tunnel:** hidden/deferred interior handle.
3. **L axilla void:** hidden/deferred interior handle.

### 2.1 Production genus target

The Gorrund production body is now expected to have **genus 1**, not genus 0, because the visible R-hand through-slit is legitimate exterior anatomy and must not be filled merely to satisfy an abstract topology count.

Required final topology:

- 1 connected component;
- 0 boundary;
- 0 non-manifold;
- **genus 1**;
- 0 degenerate faces;
- 0 self-intersections.

No additional handles are allowed unless separately proven visible and author-approved.

### 2.2 R hand rebuild

Rebuild the B–C fused-digit region as one continuous manifold surface containing a genuine through-hole.

Do **not**:
- leave separate internal digit sheets crossing inside the fused block;
- fill the visible 3 mm slit with a mid-plane web;
- artificially separate the fused block.

The correct topology must:
- preserve the visible B and C digit shapes;
- preserve the actual fusion;
- wrap continuously around the through-slit;
- contain no hidden overlapping/internal sheets;
- produce exactly one visible handle in the final body.

This rebuild supersedes the current 818+ fused-block contact pairs.

## 3. Hidden-handle D zones — explicit topological masks, not visibility beams

Do not use the beam-width exterior-visibility mask as the acceptance definition.

The beam study proved that the result is resolution-dependent.

Instead create **explicit source-face D masks** for only:

- the hidden L-hand tunnel interior;
- the hidden L-axilla void interior.

### 3.1 Mask construction

For each hidden handle:

1. identify an interior seed face set from the already-proven source slices;
2. identify the throat/contact boundary loop(s) where the hidden interior meets the exterior surface;
3. flood-fill the source faces from the seed, stopping at those explicit boundary loops;
4. freeze the resulting source face/vertex set;
5. show cross-sections and exterior views proving the mask contains only the inaccessible interior wall.

The D mask must not include:
- the visible mouth/rim;
- any exterior crease wall;
- silhouette faces;
- any surface visible through an actual open slit.

### 3.2 Deviation accounting

Report both:
- raw full-source T-1/T-2;
- production-envelope T-1/T-2 excluding only the two frozen D masks.

The numerical T-1/T-2 tolerances remain unchanged.

No third D mask may be added without a new author ruling.

## 4. Contact-aware manifold termination rule

This is the new governing rule for thin fins, webs, rims and zero-gap contacts.

### 4.1 Finite thickness

Where the source has a measurable finite gap/thickness, preserve two distinct production surfaces.

### 4.2 Actual zero-gap/taper termination

Where those two source surfaces converge to the same physical rim/contact edge:

**Do not keep two independent production sheets through the zero-gap.**

Instead:
- terminate both sides into the same production edge/vertex chain;
- make that shared chain the manifold rim/crease;
- preserve the exterior silhouette and crease location;
- keep the mesh closed and manifold.

This is standard manifold representation of a tapered membrane/rim, not a geometry waiver.

### 4.3 No artificial thickening

Do not thicken a source feature simply to separate faces.

If the source membrane genuinely tapers to zero, the production membrane may taper to a shared edge.

If the source remains finitely thick, keep its thickness within T-1/T-2.

## 5. Replace whole local patches, not narrow bands stitched into coarse faces

The v014 pilots show that narrow bands stitched into much larger surrounding faces are the main failure mechanism.

For the remaining thin features, replace the local region back to a clean attachment loop and rebuild the **entire local patch** at compatible density.

Do not insert a narrow fin/slit band into an otherwise coarse patch and then rely on projection to untangle the stitch.

Every rebuilt local patch must have:
- graded density from attachment loop to feature;
- explicit side identity;
- shared manifold rim where the source closes;
- no T-junctions;
- no internal duplicate sheets;
- 0 coarse self-x;
- clean L1 survival.

## 6. Source-side ownership — explicit face patches, not normal sign

For curled/rotating surfaces such as the ear rim, normal-sign ownership is retired.

Use explicit source face sets.

Allowed methods:
- hand-selected/frozen source face masks;
- seeded geodesic/face-graph flood bounded by manually verified rim/crease loops;
- source-loop tracing from diagnostic slices.

For every side mask:
- save the source face ids;
- show its boundary;
- show that the two side masks meet only at the intended rim/crease;
- do not classify sides solely from one global normal axis.

## 7. Feature-specific route

Proceed in this order.

### M1 — R hand B–C visible handle

Do §2 first.

Gate locally before continuing:
- exactly one visible handle in the rebuilt hand region;
- no internal duplicate sheets;
- coarse self-x 0;
- L1 regional self-x 0;
- L4 regional self-x 0;
- visible slit preserved;
- hand T-2 met in the rebuilt region.

If this cannot be done with a true manifold tunnel, stop and return a specific hand-handle block.

### M2 — R thumb-web fin

Replace the entire thumb-base/web local patch to a clean attachment loop.

Build:
- palm-side wall;
- thumb-side wall;
- graded support;
- shared outer rim where the 2 mm membrane tapers to zero.

No narrow band-to-coarse-patch stitch.

Use explicit source side masks.

Required:
- feature survives L1;
- regional self-x 0 at L1 and L4;
- T-2 <= 1.5 mm max;
- no silhouette thickening.

### M3 — L axilla visible knob / pinch mouth / z153 pocket

Separate the visible exterior surface from the frozen D-void boundary.

Rebuild the visible local patch so:
- the knob/ridge is represented;
- visible slit walls remain distinct where the source gap is finite;
- actual zero-gap contact terminates at shared crease topology;
- no production faces enter the hidden D void.

Required regional self-x 0.

### M4 — ear rims / knobs

Rebuild each remaining failing rim patch with:
- explicit source-side face masks;
- an authored rim centerline;
- two sides meeting on the shared rim edge;
- graded attachment topology.

No normal-sign split.

Required:
- regional self-x 0;
- head T-2 <= 1.5 mm;
- ear identity unchanged.

### M5 — philtrum / upper-lip / nose positive folds

Use the same manifold-termination rule:
- visible finite slot remains open;
- zero-width crease closes to shared edge;
- no overlapping lip sheets.

Preserve muzzle identity.

### M6 — remaining small Class-A folds

Apply the same rule only where evidence shows a real open/exterior defect:
- R axilla A tip;
- natal-cleft nub;
- L palm crease;
- R hand ulnar web;
- remaining exposed toe/rim folds.

Do not reopen already-passing areas unnecessarily.

## 8. T-6 measurement ruling

The tolerance remains unchanged:
- target <= 1.0 mm;
- none > 1.5 mm;
- values >1.0 mm reported.

### 8.1 Hip component rule — ACCEPTED

Adopt `rp1_landmarks_comp.py` connected-curve selection for hip landmarks.

The v013 hip_R result of 0.086 mm demonstrates that the old 6.98 mm value was a hand-contamination measurement artifact.

Apply the same deterministic component rule to source and candidate.

### 8.2 Exact radial-window clipping — ACCEPTED as the T-6 implementation

The midpoint-in-radius test is replaced by exact geometric clipping of each section segment against the landmark radius circle before length-weighted centroid accumulation.

Reason:
- the contract defines a radius-limited length-weighted section centroid;
- clipping the actual segment at the radius boundary is the geometrically exact implementation;
- midpoint inclusion can add/remove an entire segment because of a sub-mm boundary crossing.

Apply exact clipping **identically to source and production for every T-6 landmark and tail station**, not only tail_12.

Do not change landmark planes, centres, or radii.

Rerun all T-6 values.

The tolerance itself is unchanged.

## 9. Nails — geometry correction authorized

Recovered nail tooling is accepted because it reproduces all 8 historical source-tip values to <=0.003 mm.

Use it as the production nail gate.

Current v013 has 7/8 nails short by 0.18–0.71 mm because the subdivision limit surface rounds the free edges.

Claude is authorized to repair each nail locally.

### 9.1 Nail method

For each failing nail:
- preserve the source nail plate, taper, curl and silhouette;
- add a local free-edge support loop/ring or equivalent quad support;
- use nail-specific ownership/projection if needed;
- keep the support confined to the nail-bearing distal surface;
- do not lengthen the toe/finger globally.

The free edge may be made sharper only to the extent required to reproduce the frozen source.

### 9.2 Nail gate

All 8:
- projection delta within ±0.15 mm;
- no new local self-x;
- no visible nail shape change relative to source;
- foot/hand T-2 still passes.

## 10. Local direct-final patch fallback

If a feature passes as a manifold local patch at the evaluated final density but the global subdivision stack cannot preserve it, Claude may use a bounded **final-resolution patch replacement** for that feature.

This is allowed only after the M-route topology is clean.

Method:
1. evaluate the surrounding production mesh to the final L4 state;
2. remove the failing local final-resolution patch back to a clean boundary loop;
3. author a quad-dominant final-resolution replacement directly against the frozen source / explicit side targets;
4. weld it exactly to the final boundary;
5. preserve the surrounding production vertices;
6. validate the final whole mesh.

This fallback is allowed for:
- thumb web;
- ear rim;
- axilla flap/knob;
- philtrum/lip;
- nails.

It is **not** permission to auto-remesh the body.

Final output must still be:
- one manifold component;
- correct genus;
- 0 self-x;
- 0 boundary/non-manifold;
- visually faithful.

If used, keep the low-resolution cage as construction history and clearly mark that the promoted production surface contains authored final-resolution local patches.

## 11. Candidate naming / promotion

Because no v014 was promoted previously, the next consolidated passing candidate is:

`design_v014.npz`
`design_v014_col.npy`
`design_v014_info.json`

PC:

`GO_U_REF_RP1E_retopo_v014.blend`

If final-resolution local patches are used, record them in `design_v014_info.json` and in the gate.

Do not overwrite v013.

## 12. v014 gate

Required production result:

### Topology
- 1 component;
- 0 boundary;
- 0 non-manifold;
- **genus 1**;
- 0 degenerates;
- 0 self-intersections;
- quad-dominant.

### Surface
Production-envelope T-1:
- median <=0.5 mm;
- p95 <=1.5 mm;
- max <=3.0 mm.

Production-envelope T-2:
- median <=0.3 mm;
- p95 <=0.8 mm;
- max <=1.5 mm.

Report raw full-source metrics too.

### T-3
Unchanged.

### T-6
Use:
- hip connected-curve rule;
- exact radius-circle clipping;
- unchanged tolerance.

### T-7
>=0.995.

### Nails
8/8 within ±0.15 mm.

### Visual veto
Unchanged.

## 13. Stop logic

### PASS

If all production gates pass:

**RP1E GORRUND PRODUCTION RETOPO PASS / READY FOR FAMILY-PILOT AUTHOR REVIEW**

STOP.

### Geometry complete, only D-mask contract evidence needs author review

If the mesh itself is clean and all visible/exterior gates pass but only the exact two D-mask boundaries remain an acceptance documentation question:

**RP1E EXTERIOR PRODUCTION MESH PASS / D-MASK AUTHOR REVIEW REQUIRED**

STOP.

### Manifold-contact route fails

If M1–M6 plus the allowed final-resolution-patch fallback still cannot eliminate production self-intersections while meeting exterior T-1/T-2:

**RP1E MANIFOLD-CONTACT TOPOLOGY FAILED / AUTHOR DECISION REQUIRED**

For each failed feature provide:
- source cross-sections;
- source side/rim masks;
- low-res patch;
- L1 result;
- final-resolution patch attempt if used;
- exact failure mechanism.

STOP.

No further blind projection-stack experiments.

## 14. Project scope

No RP2.
No rigging.
No creator implementation.
No UE5 production implementation.

## 15. Return

Return:

`reviews/claude-rac-rp1e-v014-manifold-contact-gate.md`

Evidence:

`reviews/rac-rp1e-evidence/`

Update:
- `reviews/rac-rp1e-evidence/RP1E_progress.md`
- `reviews/claude-session-handoff.md`
- `specs/STATUS.md` only with the substantive result.
