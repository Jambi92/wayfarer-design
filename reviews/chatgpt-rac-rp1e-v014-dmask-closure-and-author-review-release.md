# RAC RP1E — v014 D-mask closure ruling and family-pilot author-review release

**Date:** 2026-10-20  
**Authority:** Tyler-authorized technical canon/project ruling through ChatGPT.  
**Returned gate:** `reviews/claude-rac-rp1e-v014-resume-execution-gate.md` (7e030467).  
**Production file:** `GO_U_REF_RP1E_retopo_v014.blend`.

## 1. Ruling

The two frozen v014 D masks are **ACCEPTED for RP1E production-envelope accounting**.

No geometry change is requested.

This ruling closes the D-mask technical review and converts the current result to:

**RP1E GORRUND PRODUCTION RETOPO PASS / READY FOR FAMILY-PILOT AUTHOR REVIEW**

This is a release to Tyler's visual/family-pilot review only.

It does **not** authorize RP2, rigging, creator implementation, or UE5 production work.

## 2. Accepted D masks

Exactly these two masks are accepted:

1. `D_Lhand_tunnel`
   - 229 source faces / 125 source vertices;
   - 3.4113 cm²;
   - 0.00912% of total source area.

2. `D_Laxilla_void`
   - 144 source faces / 87 source vertices;
   - 3.001 cm²;
   - 0.00802% of total source area.

Combined excluded source area is approximately **0.01714%**.

No third D mask is authorized.

## 3. Why the hand-tunnel boundary is accepted

The hand-tunnel mask uses throat loops defined where the frozen source passes through the frozen v014 production envelope at the zero-gap necks.

This is accepted for RP1E because:

- the mask is frozen and reproducible;
- the excluded region is a proven hidden source handle interior;
- the visible pocket mouths/rims remain outside the mask;
- the production mesh preserves the visible hand envelope and legitimate R-hand through-handle;
- all deep hand-L misses are inside this mask;
- the production-envelope hand-L maximum is 1.444 mm, inside T-2;
- the mask is only 0.00912% of source area.

The production-envelope-relative throat definition is therefore accepted as a **candidate-specific retopology accounting boundary**, not as a general rule for future races.

For future races, prefer a source-only topological throat definition where practical.

## 4. Why the axilla-void lids are accepted

The L-axilla void mask uses the last closed source cavity sections as its throat boundaries.

The production closes those two hidden throats with manifold lids while preserving the externally visible finite-gap slots outside the mask.

This is accepted because:

- the omitted region is a proven hidden genus-handle interior;
- visible slit walls outside the throat remain represented;
- the lids do not extend into the visible open-slot region;
- the lid displacement remains inside the established production-envelope tolerance;
- the general production-envelope max is 2.909 mm, inside T-1;
- the mask is only 0.00802% of source area;
- the final body is one closed manifold genus-1 production surface with 0 self-intersections.

The lids are considered legitimate production closure surfaces for the omitted hidden handle.

They are not a precedent for capping visibly open cavities.

## 5. Accepted final v014 technical gate

The following returned results are accepted as the RP1E production gate:

### Topology
- 1 component;
- 0 boundary edges;
- 0 non-manifold edges;
- genus 1;
- 0 degenerate faces;
- 0 loose vertices;
- consistent winding;
- 100% quads;
- **0 production self-intersections**.

### Production-envelope T-1
- prod→src max 2.816 mm;
- src→prod max 2.909 mm;
- PASS.

### Production-envelope T-2
- head/muzzle/ears max <=1.496 mm;
- hand L max <=1.459 / 1.444 mm by direction;
- hand R max <=1.376 / 1.335 mm;
- foot L max <=1.381 mm;
- foot R max <=1.494 mm;
- tail root max <=0.281 mm;
- PASS.

Raw full-source maxima remain recorded and explained only by the two accepted hidden D interiors.

### T-3
- stature delta -0.027 mm;
- bbox within 0.47 mm;
- PASS.

### T-6
- ruled exact-clipping / connected-hip implementation;
- max 1.122 mm;
- tail_00 1.122 and tail_05 1.119 individually reported;
- none >1.5 mm;
- PASS.

### T-7
- front 0.99857;
- profile 0.99786;
- rear 0.99859;
- PASS.

### Nails
- 8/8 within ±0.15 mm;
- returned values 0.000 mm;
- PASS.

## 6. Production freeze

Freeze the following as the current RP1E Gorrund production-retopo candidate:

### PC
`GO_U_REF_RP1E_retopo_v014.blend`

Returned file hash:
`18df4197…850b`

### Repository production data
- `reviews/rac-rp1e-evidence/designs/design_v014.npz`
- `reviews/rac-rp1e-evidence/designs/design_v014_col.npy`
- `reviews/rac-rp1e-evidence/designs/design_v014_crease_edges.json`
- `reviews/rac-rp1e-evidence/designs/design_v014_production_L4.npz`
- `reviews/rac-rp1e-evidence/v014_final/D_masks/`
- `reviews/rac-rp1e-evidence/v014_final/gate/`
- `reviews/rac-rp1e-evidence/v014_final/visual/`

Do not change v014 while Tyler performs the author review.

## 7. Required bookkeeping return

Claude should make **documentation/status changes only**.

Update the RP1E gate/status records so the final technical result is exactly:

**RP1E GORRUND PRODUCTION RETOPO PASS / READY FOR FAMILY-PILOT AUTHOR REVIEW**

Create:

`reviews/claude-rac-rp1e-v014-final-pass.md`

That file should:
- reference the accepted D-mask ruling;
- summarize the frozen v014 gate;
- state that the technical retopology pass is complete;
- point Tyler to the visual evidence needed for author review;
- explicitly state that no later production phase is authorized.

Update:
- `reviews/rac-rp1e-evidence/RP1E_progress.md`;
- `reviews/claude-session-handoff.md`;
- `specs/STATUS.md`;
- any RP1/RAC queue status that still describes Gorrund RP1E as blocked.

Do not modify production geometry.

## 8. Visual author-review stop

After the bookkeeping commit, STOP.

Tyler's next review is a genuine author visual/family-pilot checkpoint.

The technical numeric pass does not override the visual veto.

The review should show, at minimum:
- full front/profile/rear source vs v014;
- head/muzzle/ears;
- both hands, especially the R B-C through-slit and L web/tunnel exterior;
- both axillae;
- feet/toes/nails;
- perineum/pouch/natal region;
- tail root;
- any final-resolution region with >5 mm production-vertex movement, especially the L axilla slot entry.

Do not begin RP2 or any downstream work until Tyler accepts the family-pilot visual result.

## 9. Scope

No RP2.
No rigging.
No creator implementation.
No UE5 production implementation.
